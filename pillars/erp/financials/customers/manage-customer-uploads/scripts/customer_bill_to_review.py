"""Compare supplied after-state bill-to links; no loader-path or completion claim."""
from datetime import datetime

import customers_package as package
import customer_identity_review as identity
import customer_ownership_review as ownership
import customer_profile_set_review as catalogs

require = package.require
OWNER_TABLE = 'HZ_CUST_SITE_USES_ALL'


def validate_link(key, record):
    require(record['site_use_id'] == key and
            (record['bill_to_site_use_id'] is None or ownership.identifier(record['bill_to_site_use_id'])),
            'BILL_TO_LINK_SCOPE')


def validate_target(key, record):
    require(record['site_use_id'] == key, 'BILL_TO_TARGET_SCOPE')
    for field in ('cust_acct_site_id', 'cust_account_id'):
        require(record[field] is None or ownership.identifier(record[field]), 'BILL_TO_TARGET_ID')
    for field in ('set_id', 'account_site_set_id'):
        require(record[field] is None or catalogs.catalog_id(record[field]), 'BILL_TO_TARGET_SET')
    for field in ('site_use_code', 'status'):
        require(record[field] is None or identity.text(record[field]), 'BILL_TO_TARGET_VALUE')


def analyze(candidate, operation, environment_url, identities, owners, evidence):
    reviewed = ownership.analyze(candidate, operation, environment_url, identities, owners)
    require(owners['phase'] == 'after', 'BILL_TO_AFTER_PHASE_REQUIRED')
    require(isinstance(evidence, dict) and set(evidence) == {
        'schema_version', 'candidate_sha256', 'environment_url', 'operation_intent',
        'ownership_evidence_sha256', 'captured_at', 'evidence_reference',
        'reference_queries', 'link_queries', 'target_queries'}, 'BILL_TO_EVIDENCE_SCHEMA')
    require(evidence['schema_version'] == 'ar-customer-bill-to-evidence-v1', 'BILL_TO_EVIDENCE_VERSION')
    require(evidence['candidate_sha256'] == reviewed['candidate_sha256']
            and evidence['environment_url'] == environment_url and evidence['operation_intent'] == operation
            and evidence['ownership_evidence_sha256'] == package.fingerprint(owners), 'BILL_TO_BINDING_MISMATCH')
    require(identity.text(evidence['evidence_reference']), 'BILL_TO_PROVENANCE_REQUIRED')
    try:
        captured = datetime.fromisoformat(evidence['captured_at'].replace('Z', '+00:00'))
        owner_capture = datetime.fromisoformat(owners['captured_at'].replace('Z', '+00:00'))
        require(captured.tzinfo is not None and captured >= owner_capture, 'BILL_TO_CAPTURE_TIME')
    except (ValueError, TypeError, AttributeError) as exc:
        raise package.InvalidInput('BILL_TO_CAPTURE_TIME') from exc
    rows = [dict(zip(package.columns(), raw)) for raw in package.inspect_zip(candidate)]
    sources = {q['source_name']: q for q in identities['source_system_queries']}
    # All observed source codes are retained for schema scoping. Ambiguous source
    # evidence cannot pass the ownership gate below.
    allowed = {(r['orig_system'], row['BILL_TO_CUST_SITE_REF']) for row in rows
               if row['BILL_TO_CUST_SITE_REF'] for r in
               sources.get(row['ORIG_SOURCE_SYSTEM_NAME'], {}).get('records', [])}
    require(isinstance(evidence['reference_queries'], list), 'BILL_TO_REFERENCE_QUERIES')
    references = {}
    for query in evidence['reference_queries']:
        require(isinstance(query, dict) and set(query) == {
            'orig_system', 'owner_table_name', 'reference', 'complete', 'records'}, 'BILL_TO_REFERENCE_QUERY_SCHEMA')
        require(isinstance(query['orig_system'], str) and isinstance(query['reference'], str), 'BILL_TO_REFERENCE_KEY')
        key = query['orig_system'], query['reference']
        require(key in allowed and query['owner_table_name'] == OWNER_TABLE, 'BILL_TO_REFERENCE_OUTSIDE_SCOPE')
        require(key not in references, 'BILL_TO_DUPLICATE_REFERENCE_QUERY')
        require(type(query['complete']) is bool and isinstance(query['records'], list), 'BILL_TO_REFERENCE_QUERY_VALUES')
        for record in query['records']:
            require(isinstance(record, dict) and set(record) == {
                'orig_system_reference_id', 'orig_system', 'owner_table_name', 'reference',
                'owner_table_id', 'status', 'start_date_active', 'end_date_active'}, 'BILL_TO_REFERENCE_RECORD_SCHEMA')
            require((record['orig_system'], record['reference']) == key and record['owner_table_name'] == OWNER_TABLE
                    and ownership.identifier(record['orig_system_reference_id'])
                    and ownership.identifier(record['owner_table_id']) and identity.text(record['status']),
                    'BILL_TO_REFERENCE_RECORD_SCOPE')
            start, end = record['start_date_active'], record['end_date_active']
            for value in (start, end):
                if value is not None:
                    identity.oracle_date(value)
            require(start is None or end is None or identity.oracle_date(start) <= identity.oracle_date(end),
                    'BILL_TO_REFERENCE_DATE_ORDER')
        references[key] = query
    links = catalogs.indexed_queries(evidence['link_queries'], 'site_use_id',
        {q['owner_table_id'] for q in owners['queries'] if q['entity'] == 'account_site_use'},
        ('site_use_id', 'bill_to_site_use_id'), validate_link)
    target_ids = {r['owner_table_id'] for q in references.values() for r in q['records']}
    target_ids.update(r['bill_to_site_use_id'] for q in links.values() for r in q['records']
                      if r['bill_to_site_use_id'] is not None)
    targets = catalogs.indexed_queries(evidence['target_queries'], 'site_use_id', target_ids,
        ('site_use_id', 'cust_acct_site_id', 'cust_account_id', 'set_id', 'account_site_set_id', 'site_use_code', 'status'),
        validate_target)
    source_refs = {(q['orig_system'], q['owner_table_name'], q['reference']): q for q in identities['reference_queries']}
    owner_queries = {(q['entity'], q['owner_table_id']): q for q in owners['queries']}
    findings = []
    for number, row in enumerate(rows, 1):
        detail = {'row': number, 'bill_to_input_present': bool(row['BILL_TO_CUST_SITE_REF'])}
        if not row['BILL_TO_CUST_SITE_REF']:
            findings.append({**detail, 'status': 'NOT_REQUESTED_BLANK_EFFECTS_UNVERIFIED'})
            continue
        if row['SITE_USE_CODE'] != 'SHIP_TO':
            findings.append({**detail, 'status': 'BILL_TO_INPUT_REQUIRES_SHIP_TO'})
            continue
        if reviewed['status'] != 'SUPPLIED_OWNERSHIP_CONSISTENT':
            findings.append({**detail, 'status': 'OWNERSHIP_NOT_VERIFIED'})
            continue
        code = sources[row['ORIG_SOURCE_SYSTEM_NAME']]['records'][0]['orig_system']
        key = identity.reference_candidates(row)['account_site_use']
        use_id = source_refs[code, key['owner'], key['reference']]['records'][0]['owner_table_id']
        link, ref = links.get(use_id), references.get((code, row['BILL_TO_CUST_SITE_REF']))
        if not link or not link['complete'] or not ref or not ref['complete']:
            findings.append({**detail, 'status': 'BILL_TO_QUERY_MISSING_OR_INCOMPLETE'})
            continue
        if len(link['records']) != 1:
            findings.append({**detail, 'status': 'SOURCE_SITE_USE_NOT_FOUND' if not link['records'] else 'AMBIGUOUS_SOURCE_SITE_USE'})
            continue
        ids = [r['orig_system_reference_id'] for r in ref['records']]
        active = [r for r in ref['records'] if r['status'] == 'A']
        detail.update(observed_reference_rows=len(ids), active_reference_rows=len(active))
        if len(ids) != len(set(ids)):
            findings.append({**detail, 'status': 'DUPLICATE_REFERENCE_ROWS'})
            continue
        if len(active) != 1:
            findings.append({**detail, 'status': 'ACTIVE_REFERENCE_NOT_FOUND' if not active else 'AMBIGUOUS_ACTIVE_REFERENCES'})
            continue
        # Mirrors the reviewed fallback status predicate, not the separate dated
        # identity policy. Does not assert this loader branch actually executed.
        expected_id = active[0]['owner_table_id']
        actual_id = link['records'][0]['bill_to_site_use_id']
        if actual_id != expected_id:
            findings.append({**detail, 'status': 'BILL_TO_LINK_MISMATCH'})
            continue
        target = targets.get(expected_id)
        if not target or not target['complete']:
            findings.append({**detail, 'status': 'BILL_TO_TARGET_QUERY_MISSING_OR_INCOMPLETE'})
            continue
        if len(target['records']) != 1:
            findings.append({**detail, 'status': 'BILL_TO_TARGET_NOT_FOUND' if not target['records'] else 'AMBIGUOUS_BILL_TO_TARGET'})
            continue
        actual = target['records'][0]
        source_use = owner_queries['account_site_use', use_id]['records'][0]
        source_site = owner_queries['account_site', source_use['cust_acct_site_id']]['records'][0]
        if any(actual[f] is None for f in ('cust_acct_site_id', 'cust_account_id', 'set_id', 'account_site_set_id', 'site_use_code', 'status')):
            status = 'BILL_TO_TARGET_RELATIONSHIP_MISSING'
        elif actual['site_use_code'] != 'BILL_TO':
            status = 'BILL_TO_TARGET_PURPOSE_MISMATCH'
        elif actual['set_id'] != actual['account_site_set_id']:
            status = 'BILL_TO_TARGET_PARENT_SET_MISMATCH'
        else:
            status = 'SELECTED_BILL_TO_LINK_MATCH'
            detail.update(target_active=actual['status'] == 'A',
                          same_account=actual['cust_account_id'] == source_site['cust_account_id'],
                          same_set=actual['set_id'] == source_use['set_id'])
        findings.append({**detail, 'status': status})
    requested = [f for f in findings if f['bill_to_input_present']]
    matched = bool(requested) and all(f['status'] == 'SELECTED_BILL_TO_LINK_MATCH' for f in requested)
    return {'schema_version': 'ar-customer-bill-to-review-v1',
        'status': 'SELECTED_BILL_TO_LINKS_MATCH' if matched else
                  'NO_BILL_TO_INPUT_EFFECTS_UNVERIFIED' if not requested else 'BILL_TO_REVIEW_REQUIRED',
        'candidate_sha256': reviewed['candidate_sha256'], 'environment_url': environment_url,
        'ownership_evidence_sha256': package.fingerprint(owners), 'evidence_sha256': package.fingerprint(evidence),
        'findings': findings, 'selected_bill_to_links_match': matched,
        'business_relationship_eligibility_verified': False, 'loader_resolution_path_verified': False,
        'blank_update_effects_verified': False, 'persisted_reconciliation_complete': False,
        'execution_authorized': False, 'journey_complete': False,
        'limits': ['After-state source-reference agreement does not prove same-batch or fallback execution, causality or all effects.',
                   'Target status and cross-account/set relationships are observations; business eligibility needs separate validation.',
                   'Blank input is not a request to clear a link; before/after evidence remains necessary.',
                   'Supplied evidence is not an authenticated, transactionally consistent snapshot.']}
