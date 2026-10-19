"""Offline profile-class and requested reference-set review; never grants completion."""
from datetime import datetime

import customers_package as package
import customer_identity_review as identity
import customer_ownership_review as ownership

require = package.require


def catalog_id(value):
    return value == '0' or ownership.identifier(value)


def indexed_queries(items, key_field, allowed, fields, validate_record):
    require(isinstance(items, list), 'PROFILE_SET_QUERIES_REQUIRED')
    result = {}
    for query in items:
        require(isinstance(query, dict) and set(query) == {key_field, 'complete', 'records'}, 'PROFILE_SET_QUERY_SCHEMA')
        key = query[key_field]
        require(isinstance(key, str) and key in allowed, 'PROFILE_SET_QUERY_OUTSIDE_SCOPE')
        require(key not in result, 'PROFILE_SET_DUPLICATE_QUERY')
        require(type(query['complete']) is bool and isinstance(query['records'], list), 'PROFILE_SET_QUERY_VALUES')
        for record in query['records']:
            require(isinstance(record, dict) and set(record) == set(fields), 'PROFILE_SET_RECORD_SCHEMA')
            validate_record(key, record)
        result[key] = query
    return result


def validate_set(key, record):
    require(record['set_code'] == key and catalog_id(record['set_id']), 'SET_RECORD_SCOPE_OR_ID')


def validate_class(key, record):
    require(record['name'] == key and catalog_id(record['profile_class_id'])
            and identity.text(record['status']), 'CLASS_RECORD_SCOPE_OR_ID')


def validate_profile(key, record):
    require(record['cust_account_id'] == key and record['site_use_id'] is None
            and ownership.identifier(record['cust_account_profile_id'])
            and (record['profile_class_id'] is None or catalog_id(record['profile_class_id']))
            and (record['status'] is None or identity.text(record['status'])), 'PROFILE_RECORD_SCOPE_OR_ID')
    start, end = (record['effective_start_date'], record['effective_end_date'])
    if start is not None:
        identity.oracle_date(start)
    if end is not None:
        identity.oracle_date(end)
    if start is not None and end is not None:
        require(identity.oracle_date(start) <= identity.oracle_date(end), 'PROFILE_DATE_ORDER')


def profile_finding(query, class_query, midnight):
    """Report all-row existence separately from an as-of-midnight comparison.

    This time policy is explicit evidence interpretation, not an inferred
    downstream loader date/default or a claim that its I/U branch executed.
    """
    detail = {'observed_profile_rows': len(query['records']) if query else None,
              'all_rows_complete': bool(query and query['complete'])}
    if not query or not query['complete']:
        return {**detail, 'status': 'PROFILE_QUERY_MISSING_OR_INCOMPLETE'}
    if not class_query or not class_query['complete']:
        return {**detail, 'status': 'CLASS_QUERY_MISSING_OR_INCOMPLETE'}
    if len(class_query['records']) != 1:
        return {**detail, 'status': 'CLASS_NOT_FOUND' if not class_query['records'] else 'AMBIGUOUS_CLASS_ROWS'}
    expected = class_query['records'][0]
    if expected['status'] != 'A':
        return {**detail, 'status': 'REQUESTED_CLASS_NOT_ACTIVE'}
    records = query['records']
    # Even duplicate historical rows invalidate a complete-export interpretation.
    keys = [(r['cust_account_profile_id'], r['effective_start_date'], r['effective_end_date']) for r in records]
    if len(keys) != len(set(keys)):
        return {**detail, 'status': 'DUPLICATE_PROFILE_ROWS'}
    if any(r['effective_start_date'] is None or r['effective_end_date'] is None or r['status'] is None for r in records):
        return {**detail, 'status': 'PROFILE_DATES_OR_STATUS_MISSING'}
    current = [r for r in records if r['status'] == 'A'
               and identity.oracle_date(r['effective_start_date']) <= midnight <= identity.oracle_date(r['effective_end_date'])]
    detail['active_profiles_covering_as_of_midnight'] = len(current)
    if len(current) != 1:
        return {**detail, 'status': 'NO_ACTIVE_PROFILE_AT_AS_OF' if not current else 'OVERLAPPING_ACTIVE_PROFILES'}
    actual = current[0]['profile_class_id']
    return {**detail, 'status': 'PROFILE_CLASS_VALUE_MISSING' if actual is None else
            'MATCH' if actual == expected['profile_class_id'] else 'PROFILE_CLASS_MISMATCH'}


def analyze(candidate, operation, environment_url, identities, owners, evidence):
    owner_result = ownership.analyze(candidate, operation, environment_url, identities, owners)
    require(owners['phase'] == 'after', 'PROFILE_SET_AFTER_PHASE_REQUIRED')
    require(isinstance(evidence, dict) and set(evidence) == {
        'schema_version', 'candidate_sha256', 'environment_url', 'operation_intent',
        'ownership_evidence_sha256', 'as_of_date', 'captured_at', 'evidence_reference',
        'set_queries', 'class_queries', 'profile_queries'}, 'PROFILE_SET_EVIDENCE_SCHEMA')
    require(evidence['schema_version'] == 'ar-customer-profile-set-evidence-v1', 'PROFILE_SET_EVIDENCE_VERSION')
    require(evidence['candidate_sha256'] == owner_result['candidate_sha256']
            and evidence['environment_url'] == environment_url and evidence['operation_intent'] == operation
            and evidence['ownership_evidence_sha256'] == package.fingerprint(owners)
            and evidence['as_of_date'] == owners['as_of_date'], 'PROFILE_SET_BINDING_MISMATCH')
    require(identity.text(evidence['evidence_reference']), 'PROFILE_SET_PROVENANCE_REQUIRED')
    try:
        captured = datetime.fromisoformat(evidence['captured_at'].replace('Z', '+00:00'))
        owner_capture = datetime.fromisoformat(owners['captured_at'].replace('Z', '+00:00'))
        require(captured.tzinfo is not None and captured >= owner_capture, 'PROFILE_SET_CAPTURE_TIME')
        midnight = datetime.fromisoformat(evidence['as_of_date'] + 'T00:00:00')
    except (ValueError, TypeError, AttributeError) as exc:
        raise package.InvalidInput('PROFILE_SET_CAPTURE_TIME') from exc
    rows = [dict(zip(package.columns(), values)) for values in package.inspect_zip(candidate)]
    sets = indexed_queries(evidence['set_queries'], 'set_code',
        {r['ACCT_ADDRESS_SET_CODE'] for r in rows if r['ACCT_ADDRESS_SET_CODE']},
        ('set_code', 'set_id'), validate_set)
    classes = indexed_queries(evidence['class_queries'], 'name',
        {r['CUSTOMER_PROFILE_CLASS'] or 'DEFAULT' for r in rows},
        ('name', 'profile_class_id', 'status'), validate_class)
    accounts = {q['owner_table_id'] for q in owners['queries'] if q['entity'] == 'account'}
    profiles = indexed_queries(evidence['profile_queries'], 'cust_account_id', accounts,
        ('cust_account_profile_id', 'cust_account_id', 'site_use_id', 'profile_class_id',
         'status', 'effective_start_date', 'effective_end_date'), validate_profile)
    sources = {q['source_name']: q for q in identities['source_system_queries']}
    refs = {(q['orig_system'], q['owner_table_name'], q['reference']): q for q in identities['reference_queries']}
    owner_queries = {(q['entity'], q['owner_table_id']): q for q in owners['queries']}
    findings = []
    for number, row in enumerate(rows, 1):
        if owner_result['status'] != 'SUPPLIED_OWNERSHIP_CONSISTENT':
            findings.extend({'row': number, 'check': check, 'status': 'OWNERSHIP_NOT_VERIFIED'}
                            for check in ('requested_reference_set', 'account_profile_class'))
            continue
        code = sources[row['ORIG_SOURCE_SYSTEM_NAME']]['records'][0]['orig_system']
        keys = identity.reference_candidates(row)
        def owner_id(entity):
            key = keys[entity]
            return refs[code, key['owner'], key['reference']]['records'][0]['owner_table_id']
        query = sets.get(row['ACCT_ADDRESS_SET_CODE'])
        detail = {'raw_set_rows': len(query['records']) if query else None}
        if not row['ACCT_ADDRESS_SET_CODE']:
            status = 'SET_INPUT_BLANK_EFFECT_UNREVIEWED'
        elif not query or not query['complete']:
            status = 'SET_QUERY_MISSING_OR_INCOMPLETE'
        else:
            # Reviewed 26D site-use staging SELECT DISTINCT permits repeated
            # metadata rows with the same ID. Preserve/count raw evidence.
            resolved_ids = {r['set_id'] for r in query['records']}
            if len(resolved_ids) != 1:
                status = 'SET_NOT_FOUND' if not resolved_ids else 'AMBIGUOUS_SET_IDS'
            else:
                expected = next(iter(resolved_ids))
                actual = [owner_queries[entity, owner_id(entity)]['records'][0]['set_id']
                          for entity in ('account_site', 'account_site_use')]
                status = 'MATCH' if actual == [expected, expected] else 'REQUESTED_SET_MISMATCH'
        findings.append({'row': number, 'check': 'requested_reference_set', 'status': status, **detail})
        class_name = row['CUSTOMER_PROFILE_CLASS'] or 'DEFAULT'
        findings.append({'row': number, 'check': 'account_profile_class',
            'expectation_basis': 'EXPLICIT_INPUT' if row['CUSTOMER_PROFILE_CLASS'] else 'REVIEWED_INTERFACE_DEFAULT',
            **profile_finding(profiles.get(owner_id('account')), classes.get(class_name), midnight)})
    match = bool(findings) and all(f['status'] == 'MATCH' for f in findings)
    mismatch = any(f['status'] in {'REQUESTED_SET_MISMATCH', 'PROFILE_CLASS_MISMATCH'} for f in findings)
    return {'schema_version': 'ar-customer-profile-set-review-v1',
        'status': 'PROFILE_SET_MISMATCH' if mismatch else 'PROFILE_SET_VALUES_MATCH' if match else 'PROFILE_SET_EVIDENCE_INCOMPLETE',
        'candidate_sha256': owner_result['candidate_sha256'], 'environment_url': environment_url,
        'operation_intent': operation, 'ownership_evidence_sha256': package.fingerprint(owners),
        'evidence_sha256': package.fingerprint(evidence), 'as_of_policy': 'EXPORTED_DATABASE_DATE_AT_MIDNIGHT',
        'findings': findings, 'profile_set_values_match': match,
        'persisted_reconciliation_complete': False, 'execution_authorized': False, 'journey_complete': False,
        'limits': ['Supplied evidence is not authenticated by this helper.',
                   'All profile rows are retained; existence is not a claim that the loader I/U branch executed.',
                   'As-of class/set agreement does not prove profile defaults, mutability, before/after effects or process success.']}
