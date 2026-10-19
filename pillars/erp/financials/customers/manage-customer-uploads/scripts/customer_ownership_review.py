"""Review scoped parent/child evidence offline; no Fusion calls or import approval."""
import argparse
from datetime import datetime
import json
from pathlib import Path
import re

import customers_package as package
import customer_identity_review as identity

FIELDS = {
    'party': ('party_id',),
    'location': ('location_id',),
    'account': ('cust_account_id', 'party_id'),
    'party_site': ('party_site_id', 'party_id', 'location_id'),
    'party_site_use': ('party_site_use_id', 'party_site_id', 'site_use_type'),
    'account_site': ('cust_acct_site_id', 'cust_account_id', 'party_site_id', 'set_id'),
    'account_site_use': ('site_use_id', 'cust_acct_site_id', 'set_id', 'site_use_code'),
}
LINKS = (
    ('account_party', 'account', 'party_id', 'party', 'party_id'),
    ('party_site_party', 'party_site', 'party_id', 'party', 'party_id'),
    ('party_site_location', 'party_site', 'location_id', 'location', 'location_id'),
    ('account_site_account', 'account_site', 'cust_account_id', 'account', 'cust_account_id'),
    ('account_site_party_site', 'account_site', 'party_site_id', 'party_site', 'party_site_id'),
    ('site_use_account_site', 'account_site_use', 'cust_acct_site_id', 'account_site', 'cust_acct_site_id'),
    ('site_use_reference_set', 'account_site_use', 'set_id', 'account_site', 'set_id'),
    ('party_site_use_parent', 'party_site_use', 'party_site_id', 'party_site', 'party_site_id'),
)
require = package.require


def identifier(value):
    return isinstance(value, str) and re.fullmatch(r'[1-9][0-9]*', value) is not None


def analyze(candidate, operation, environment_url, identity_evidence, evidence):
    identity_result = identity.analyze(candidate, operation, environment_url, identity_evidence)
    require(isinstance(evidence, dict) and set(evidence) == {
        'schema_version', 'candidate_sha256', 'environment_url', 'operation_intent',
        'identity_evidence_sha256', 'phase', 'as_of_date', 'captured_at',
        'evidence_reference', 'queries'}, 'OWNERSHIP_EVIDENCE_SCHEMA')
    require(evidence['schema_version'] == 'ar-customer-ownership-evidence-v1', 'OWNERSHIP_EVIDENCE_VERSION')
    require(evidence['candidate_sha256'] == identity_result['candidate_sha256']
        and evidence['environment_url'] == environment_url and evidence['operation_intent'] == operation
        and evidence['identity_evidence_sha256'] == identity_result['evidence_sha256']
        and evidence['as_of_date'] == identity_evidence['as_of_date'], 'OWNERSHIP_EVIDENCE_BINDING_MISMATCH')
    require(evidence['phase'] in ('before', 'after'), 'OWNERSHIP_PHASE_REQUIRED')
    require(identity.text(evidence['evidence_reference']), 'OWNERSHIP_PROVENANCE_REQUIRED')
    try:
        captured = datetime.fromisoformat(evidence['captured_at'].replace('Z', '+00:00'))
        source_capture = datetime.fromisoformat(identity_evidence['captured_at'].replace('Z', '+00:00'))
    except (ValueError, TypeError, AttributeError) as exc:
        raise package.InvalidInput('OWNERSHIP_CAPTURE_TIME') from exc
    require(captured.tzinfo is not None and captured >= source_capture, 'OWNERSHIP_CAPTURE_TIME')
    require(isinstance(evidence['queries'], list), 'OWNERSHIP_QUERIES_REQUIRED')
    # Evidence is scoped to IDs actually present in the bound source-reference
    # export. It may retain ambiguous/history rows, but may not select them away.
    allowed = {(entity, r['owner_table_id'])
        for entity, (_, table) in identity.ENTITIES.items()
        for q in identity_evidence['reference_queries'] if q['owner_table_name'] == table
        for r in q['records']}
    queries = {}
    for query in evidence['queries']:
        require(isinstance(query, dict) and set(query) == {'entity', 'owner_table_id', 'complete', 'records'},
                'OWNERSHIP_QUERY_SCHEMA')
        require(isinstance(query['entity'], str) and query['entity'] in FIELDS
            and identifier(query['owner_table_id']) and type(query['complete']) is bool
            and isinstance(query['records'], list), 'OWNERSHIP_QUERY_VALUES')
        key = query['entity'], query['owner_table_id']
        require(key in allowed, 'OWNERSHIP_QUERY_OUTSIDE_IDENTITY_SCOPE')
        require(key not in queries, 'DUPLICATE_OWNERSHIP_QUERY')
        fields = FIELDS[key[0]]
        for record in query['records']:
            require(isinstance(record, dict) and set(record) == set(fields), 'OWNERSHIP_RECORD_SCHEMA')
            require(record[fields[0]] == key[1], 'OWNERSHIP_RECORD_ID_MISMATCH')
            for field, value in record.items():
                # COMMON legitimately has SET_ID 0. This exception is specific
                # to reference sets, not entity/parent identity validation.
                if field in ('site_use_code', 'site_use_type'):
                    valid = isinstance(value, str)
                elif field == 'set_id':
                    valid = value == '0' or identifier(value)
                else:
                    valid = identifier(value)
                require(value is None or valid,
                        'OWNERSHIP_RECORD_VALUE')
        queries[key] = query

    sources = {q['source_name']: q for q in identity_evidence['source_system_queries']}
    references = {(q['orig_system'], q['owner_table_name'], q['reference']): q
                  for q in identity_evidence['reference_queries']}
    identity_findings = {(f['row'], f['entity']): f for f in identity_result['findings']}
    findings = []
    rows = [dict(zip(package.columns(), values)) for values in package.inspect_zip(candidate)]
    for number, row in enumerate(rows, 1):
        selected = {}
        source = sources.get(row['ORIG_SOURCE_SYSTEM_NAME'])
        code = source['records'][0]['orig_system'] if source and source['complete'] and len(source['records']) == 1 else None
        for entity, key_info in identity.reference_candidates(row).items():
            status = 'IDENTITY_NOT_UNAMBIGUOUS_ACTIVE_REFERENCE'
            identity_finding = identity_findings[number, entity]
            if identity_finding['status'] == 'ONE_ACTIVE_REFERENCE_OBSERVED':
                reference = references[code, key_info['owner'], key_info['reference']]
                if len(reference['records']) != 1:
                    status = 'IDENTITY_HISTORY_REVIEW_REQUIRED'
                else:
                    owner_id = reference['records'][0]['owner_table_id']
                    query = queries.get((entity, owner_id))
                    if not query or not query['complete']:
                        status = 'OWNERSHIP_QUERY_MISSING_OR_INCOMPLETE'
                    elif len(query['records']) == 0:
                        status = 'REFERENCED_TARGET_ROW_NOT_FOUND'
                    elif len(query['records']) > 1:
                        status = 'AMBIGUOUS_TARGET_ROWS'
                    else:
                        selected[entity] = query['records'][0]
                        status = 'TARGET_ROW_OBSERVED'
            findings.append({'row': number, 'check': entity, 'status': status})
        for name, child, child_field, parent, parent_field in LINKS:
            if child not in selected or parent not in selected:
                status = 'OWNERSHIP_NOT_EVALUATED'
            elif selected[child][child_field] is None or selected[parent][parent_field] is None:
                status = 'RELATIONSHIP_VALUE_MISSING'
            else:
                status = 'MATCH' if selected[child][child_field] == selected[parent][parent_field] else 'OWNERSHIP_MISMATCH'
            findings.append({'row': number, 'check': name, 'status': status})
        use = selected.get('account_site_use')
        status = 'OWNERSHIP_NOT_EVALUATED' if use is None else (
            'MATCH' if use['site_use_code'] == row['SITE_USE_CODE'] else 'SITE_USE_PURPOSE_MISMATCH')
        findings.append({'row': number, 'check': 'site_use_purpose', 'status': status})
        party_use = selected.get('party_site_use')
        status = 'OWNERSHIP_NOT_EVALUATED' if party_use is None else (
            'MATCH' if party_use['site_use_type'] == row['SITE_USE_CODE'] else 'SITE_USE_PURPOSE_MISMATCH')
        findings.append({'row': number, 'check': 'party_site_use_purpose', 'status': status})
    mismatches = any(f['status'] in {'OWNERSHIP_MISMATCH', 'SITE_USE_PURPOSE_MISMATCH'} for f in findings)
    complete = all(f['status'] in {'TARGET_ROW_OBSERVED', 'MATCH'} for f in findings)
    return {'schema_version': 'ar-customer-ownership-review-v1',
        'status': 'OWNERSHIP_MISMATCH' if mismatches else 'SUPPLIED_OWNERSHIP_CONSISTENT' if complete else 'OWNERSHIP_EVIDENCE_INCOMPLETE',
        'candidate_sha256': identity_result['candidate_sha256'], 'environment_url': environment_url,
        'operation_intent': operation, 'phase': evidence['phase'],
        'identity_evidence_sha256': identity_result['evidence_sha256'], 'evidence_sha256': package.fingerprint(evidence),
        'findings': findings, 'live_ready': False, 'execution_authorized': False,
        'persisted_reconciliation_complete': False,
        'limits': ['Coherent supplied evidence is not an authenticated or transactionally consistent database snapshot.',
            'Matched relationships do not establish field mutability, all persisted values or expected creation/update effects.',
            'Profile, receipt assignment, BILL_TO linking, tax and DFF readback remain separate obligations.',
            'Missing references or target rows are not authorization to create records.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--zip', required=True, type=Path)
    parser.add_argument('--operation', required=True, choices=['create', 'update', 'mixed'])
    parser.add_argument('--environment-url', required=True)
    parser.add_argument('--identity-evidence', required=True, type=Path)
    parser.add_argument('--evidence', required=True, type=Path)
    args = parser.parse_args()
    try:
        require(args.zip.stat().st_size <= package.LIMIT, 'LOCAL_INSPECTION_LIMIT_REQUIRES_STREAMING_REVIEW')
        result = analyze(args.zip.read_bytes(), args.operation, args.environment_url,
            package.load_json(args.identity_evidence), package.load_json(args.evidence))
        print(json.dumps(result, indent=2))
    except (OSError, ValueError) as exc:
        print(json.dumps({'status': 'BLOCKED', 'error': str(exc) if isinstance(exc, package.InvalidInput) else type(exc).__name__,
                          'execution_authorized': False}))
    return 2  # Relationship review alone never establishes complete live readiness.


if __name__ == '__main__':
    raise SystemExit(main())
