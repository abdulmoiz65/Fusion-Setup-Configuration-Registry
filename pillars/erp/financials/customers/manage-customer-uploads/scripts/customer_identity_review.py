"""Offline review of explicitly scoped source-key evidence; never queries Fusion."""
import argparse
from datetime import date, datetime
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

import customers_package as package

# These expressions describe loader-side keys; they never rewrite candidate bytes.
CONTROL_SHA256 = 'c85f853f709c7adaec364476049c74f21f00ac5fc5bfdf97b6e2a96c89a548e4'
ENTITIES = {
    'party': ('PARTY_ORIG_SYSTEM_REFERENCE', 'HZ_PARTIES'),
    'account': ('CUST_ORIG_SYSTEM_REFERENCE', 'HZ_CUST_ACCOUNTS'),
    'location': ('LOCATION_ORIG_SYSTEM_REFERENCE', 'HZ_LOCATIONS'),
    'account_site': ('CUST_SITE_ORIG_SYS_REF', 'HZ_CUST_ACCT_SITES_ALL'),
    'account_site_use': ('CUST_SITEUSE_ORIG_SYS_REF', 'HZ_CUST_SITE_USES_ALL'),
    'party_site': ('SITE_ORIG_SYSTEM_REFERENCE', 'HZ_PARTY_SITES'),
    'party_site_use': ('CUST_SITEUSE_ORIG_SYS_REF', 'HZ_PARTY_SITE_USES'),
}
REFERENCE_FALLBACKS = {'party': 'PARTY_NUMBER', 'account': 'ACCOUNT_NUMBER',
                       'account_site': 'PARTY_SITE_NUMBER'}


def reference_candidates(row):
    """Derive keys from the reviewed control, without changing explicit input.

    Strings with edge whitespace need loader lexical review; do not silently strip
    them or assert the database will compare them as Python does.
    """
    result = {}
    for entity, (field, owner) in ENTITIES.items():
        if entity == 'party_site':
            inputs = [row['PARTY_NUMBER'], row['LOCATION_ORIG_SYSTEM_REFERENCE']]
            value = inputs[0] + '-partysite-' + inputs[1]
            derivation = 'CONTROL_PARTY_NUMBER_LOCATION_CONCAT'
        else:
            value = row[field]
            derivation = 'SUPPLIED_REFERENCE'
            if not value and entity in REFERENCE_FALLBACKS:
                value = row[REFERENCE_FALLBACKS[entity]]
                derivation = 'CONTROL_DISPLAY_NUMBER_FALLBACK'
            inputs = [value]
        result[entity] = {'owner': owner, 'field': field, 'reference': value,
                          'derivation': derivation,
                          'lexical_review_required': any(v != v.strip() for v in inputs)}
    return result


def check(condition, code):
    package.require(condition, code)


def text(value):
    return isinstance(value, str) and bool(value.strip())


def oracle_date(value):
    """Preserve Oracle DATE seconds in database-local time, without truncation."""
    check(isinstance(value, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', value),
          'REFERENCE_DATE_FORMAT')
    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise package.InvalidInput('REFERENCE_DATE_FORMAT') from exc


def analyze(candidate, operation, environment_url, evidence):
    """Classify reference evidence, not final operation effects or permissions.

    A completeness declaration is supplied run evidence, not authenticated proof.
    Caller must verify query scope and export provenance through the declared route.
    """
    preview = package.inspect_candidate(candidate, operation)
    rows = [dict(zip(package.columns(), row)) for row in package.inspect_zip(candidate)]
    origin = urlsplit(environment_url)
    check(origin.scheme == 'https' and origin.hostname and not origin.username and not origin.password
          and not origin.query and not origin.fragment and origin.path in {'', '/'}, 'ENVIRONMENT_ORIGIN_REQUIRED')
    check(isinstance(evidence, dict) and set(evidence) == {
        'schema_version', 'candidate_sha256', 'environment_url', 'operation_intent',
        'as_of_date', 'captured_at', 'evidence_reference', 'source_system_queries', 'reference_queries'},
        'IDENTITY_EVIDENCE_SCHEMA')
    check(evidence['schema_version'] == 'ar-customer-identity-evidence-v3', 'IDENTITY_EVIDENCE_VERSION')
    check(evidence['candidate_sha256'] == hashlib.sha256(candidate).hexdigest()
          and evidence['environment_url'] == environment_url and evidence['operation_intent'] == operation,
          'IDENTITY_EVIDENCE_BINDING_MISMATCH')
    check(text(evidence['evidence_reference']), 'EVIDENCE_REFERENCE_REQUIRED')
    try:
        as_of = date.fromisoformat(evidence['as_of_date'])
        # The reviewed profile query compares TRUNC(SYSDATE) to raw Oracle DATE
        # bounds. as_of_date must be exported from that database, not the client.
        midnight = datetime.combine(as_of, datetime.min.time())
        captured = datetime.fromisoformat(evidence['captured_at'].replace('Z', '+00:00'))
    except (ValueError, TypeError, AttributeError) as exc:
        raise package.InvalidInput('EVIDENCE_DATE_FORMAT') from exc
    check(captured.tzinfo is not None, 'EVIDENCE_CAPTURE_TIMEZONE')
    check(isinstance(evidence['source_system_queries'], list) and isinstance(evidence['reference_queries'], list),
          'QUERY_EVIDENCE_LISTS_REQUIRED')
    sources = {}
    for query in evidence['source_system_queries']:
        check(isinstance(query, dict) and set(query) == {'source_name', 'complete', 'records'}, 'SOURCE_QUERY_SCHEMA')
        check(text(query['source_name']) and type(query['complete']) is bool and isinstance(query['records'], list),
              'SOURCE_QUERY_VALUES')
        check(query['source_name'] not in sources, 'DUPLICATE_SOURCE_QUERY')
        for record in query['records']:
            check(isinstance(record, dict) and set(record) == {'orig_system_name', 'orig_system'}, 'SOURCE_RECORD_SCHEMA')
            check(record['orig_system_name'] == query['source_name'] and text(record['orig_system']), 'SOURCE_RECORD_SCOPE')
        sources[query['source_name']] = query
    references = {}
    for query in evidence['reference_queries']:
        check(isinstance(query, dict) and set(query) == {'orig_system', 'owner_table_name', 'reference', 'complete', 'records'},
              'REFERENCE_QUERY_SCHEMA')
        check(all(text(query[k]) for k in ('orig_system', 'owner_table_name', 'reference'))
              and type(query['complete']) is bool and isinstance(query['records'], list), 'REFERENCE_QUERY_VALUES')
        key = tuple(query[k] for k in ('orig_system', 'owner_table_name', 'reference'))
        check(key not in references, 'DUPLICATE_REFERENCE_QUERY')
        for record in query['records']:
            check(isinstance(record, dict) and set(record) == {'owner_table_id', 'status', 'start_date_active', 'end_date_active'},
                  'REFERENCE_RECORD_SCHEMA')
            check(text(record['owner_table_id']) and record['owner_table_id'].isdigit() and text(record['status']),
                  'REFERENCE_RECORD_VALUES')
            try:
                start = oracle_date(record['start_date_active'])
                end = oracle_date(record['end_date_active']) if record['end_date_active'] is not None else None
            except (ValueError, TypeError) as exc:
                raise package.InvalidInput('REFERENCE_DATE_FORMAT') from exc
            check(end is None or end >= start, 'REFERENCE_DATE_ORDER')
        references[key] = query
    findings = []
    for number, row in enumerate(rows, 1):
        source = sources.get(row['ORIG_SOURCE_SYSTEM_NAME'])
        code = None
        source_status = 'SOURCE_QUERY_MISSING_OR_INCOMPLETE'
        if source and source['complete']:
            count = len(source['records'])
            source_status = ('SOURCE_NAME_NOT_FOUND_CONTROL_DERIVATION_UNREVIEWED' if count == 0 else
                             'AMBIGUOUS_SOURCE_NAME' if count > 1 else 'SOURCE_CODE_RESOLVED')
            if count == 1:
                code = source['records'][0]['orig_system']
        findings.append({'row': number, 'entity': 'source_system', 'status': source_status})
        for entity, key_info in reference_candidates(row).items():
            field, owner, reference = key_info['field'], key_info['owner'], key_info['reference']
            finding = {'row': number, 'entity': entity, 'field': field, 'derivation': key_info['derivation']}
            if code is None:
                status = 'SOURCE_CODE_UNRESOLVED'
            elif key_info['lexical_review_required']:
                status = 'REFERENCE_LEXICAL_REVIEW_REQUIRED'
            elif not reference:
                status = 'NO_REFERENCE_NO_CONTROL_FALLBACK'
            else:
                query = references.get((code, owner, reference))
                if not query or not query['complete']:
                    status = 'REFERENCE_QUERY_MISSING_OR_INCOMPLETE'
                else:
                    records = query['records']
                    dated = [r for r in records if oracle_date(r['start_date_active']) <= midnight
                             and (r['end_date_active'] is None or midnight <= oracle_date(r['end_date_active']))]
                    active = [r for r in dated if r['status'] == 'A']
                    # Do not select an arbitrary first result or collapse duplicated
                    # rows. Product scalar lookups and ownership need explicit review.
                    status = ('NO_REFERENCE_OBSERVED_NOT_CREATE_AUTHORITY' if not records else
                              'AMBIGUOUS_REFERENCE' if len(dated) > 1 else
                              'ONE_ACTIVE_REFERENCE_OBSERVED' if len(active) == 1 else
                              'INACTIVE_OR_OUT_OF_DATE_REFERENCE_REQUIRES_REVIEW')
                    finding.update(observed_records=len(records), dated_records=len(dated), active_records=len(active))
                    # Profile I-to-U source does not filter OSR.STATUS. Preserve this
                    # nuance; a generic active-only filter would miss potential updates.
                    if entity == 'account':
                        finding['profile_update_probe_required'] = bool(dated)
            finding['status'] = status
            findings.append(finding)
    return {'schema_version': 'ar-customer-identity-review-v2', 'status': 'IDENTITY_EVIDENCE_REVIEW_LIVE_BLOCKED',
            'candidate_sha256': preview['candidate_sha256'], 'environment_url': environment_url,
            'operation_intent': operation, 'as_of_date': evidence['as_of_date'],
            'evidence_sha256': package.fingerprint(evidence), 'findings': findings,
            'control_source_sha256': CONTROL_SHA256,
            'execution_authorized': False, 'live_ready': False, 'persisted_reconciliation_complete': False,
            'limits': ['Evidence provenance and freshness must be verified by the declared central read-only route.',
                       'No reference observed does not prove a new entity; alternate matching and business ownership remain unreviewed.',
                       'An existing reference does not establish parent relationships, supported field updates, or intended effects.',
                       'Profile, receipt assignment, DFF/value readback and complete downstream matching remain required.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--zip', type=Path, required=True)
    parser.add_argument('--operation', choices=['create', 'update', 'mixed'], required=True)
    parser.add_argument('--environment-url', required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    args = parser.parse_args()
    try:
        check(args.zip.stat().st_size <= package.LIMIT, 'LOCAL_INSPECTION_LIMIT_REQUIRES_STREAMING_REVIEW')
        result = analyze(args.zip.read_bytes(), args.operation, args.environment_url, package.load_json(args.evidence))
        print(json.dumps(result, indent=2))
    except (OSError, ValueError) as exc:
        print(json.dumps({'status': 'BLOCKED', 'error': str(exc) if isinstance(exc, package.InvalidInput) else type(exc).__name__,
                          'execution_authorized': False}))
    return 2  # This evidence review is deliberately not a live-readiness gate.


if __name__ == '__main__':
    raise SystemExit(main())
