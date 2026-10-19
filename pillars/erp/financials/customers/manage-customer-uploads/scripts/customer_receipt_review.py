"""Offline receipt-assignment value review, not insertion/replay or completion proof."""
from datetime import datetime
import re

import customers_package as package
import customer_identity_review as identity
import customer_ownership_review as ownership
import customer_profile_set_review as catalogs
import customer_value_review as values

require = package.require


def dates(record):
    for key in ('start_date', 'end_date'):
        if record[key] is not None:
            identity.oracle_date(record[key])
    if record['start_date'] is not None and record['end_date'] is not None:
        require(identity.oracle_date(record['start_date']) <= identity.oracle_date(record['end_date']), 'RECEIPT_DATE_ORDER')


def validate_method(key, record):
    require(record['name'] == key and ownership.identifier(record['receipt_method_id']), 'RECEIPT_METHOD_SCOPE')
    dates(record)


def validate_site(key, record):
    require(record['cust_acct_site_id'] == key and ownership.identifier(record['site_use_id'])
            and catalogs.catalog_id(record['set_id']) and identity.text(record['site_use_code'])
            and identity.text(record['status']), 'RECEIPT_SITE_SCOPE')


def validate_assignment(key, record):
    require(record['customer_id'] == key and ownership.identifier(record['cust_receipt_method_id'])
            and ownership.identifier(record['receipt_method_id'])
            and (record['site_use_id'] is None or ownership.identifier(record['site_use_id']))
            and (record['primary_flag'] is None or record['primary_flag'] in ('Y', 'N')),
            'RECEIPT_ASSIGNMENT_SCOPE')
    marker = record['request_id']
    require(marker is None or (isinstance(marker, str) and re.fullmatch(r'-?[0-9]+', marker)), 'RECEIPT_REQUEST_MARKER_FORMAT')
    dates(record)


def analyze(candidate, operation, environment_url, identities, owners, evidence):
    owner_result = ownership.analyze(candidate, operation, environment_url, identities, owners)
    require(owners['phase'] == 'after', 'RECEIPT_AFTER_PHASE_REQUIRED')
    require(isinstance(evidence, dict) and set(evidence) == {
        'schema_version', 'candidate_sha256', 'environment_url', 'operation_intent',
        'ownership_evidence_sha256', 'captured_at', 'evidence_reference',
        'method_queries', 'site_use_queries', 'assignment_queries'}, 'RECEIPT_EVIDENCE_SCHEMA')
    require(evidence['schema_version'] == 'ar-customer-receipt-evidence-v1', 'RECEIPT_EVIDENCE_VERSION')
    require(evidence['candidate_sha256'] == owner_result['candidate_sha256']
            and evidence['environment_url'] == environment_url and evidence['operation_intent'] == operation
            and evidence['ownership_evidence_sha256'] == package.fingerprint(owners), 'RECEIPT_BINDING_MISMATCH')
    require(identity.text(evidence['evidence_reference']), 'RECEIPT_PROVENANCE_REQUIRED')
    try:
        captured = datetime.fromisoformat(evidence['captured_at'].replace('Z', '+00:00'))
        owner_capture = datetime.fromisoformat(owners['captured_at'].replace('Z', '+00:00'))
        require(captured.tzinfo is not None and captured >= owner_capture, 'RECEIPT_CAPTURE_TIME')
    except (ValueError, TypeError, AttributeError) as exc:
        raise package.InvalidInput('RECEIPT_CAPTURE_TIME') from exc
    rows = [dict(zip(package.columns(), raw)) for raw in package.inspect_zip(candidate)]
    methods = catalogs.indexed_queries(evidence['method_queries'], 'name',
        {r['PAYMENT_METHOD_NAME'] for r in rows if r['PAYMENT_METHOD_NAME']},
        ('name', 'receipt_method_id', 'start_date', 'end_date'), validate_method)
    sites = catalogs.indexed_queries(evidence['site_use_queries'], 'cust_acct_site_id',
        {q['owner_table_id'] for q in owners['queries'] if q['entity'] == 'account_site'},
        ('site_use_id', 'cust_acct_site_id', 'set_id', 'site_use_code', 'status'), validate_site)
    assignments = catalogs.indexed_queries(evidence['assignment_queries'], 'customer_id',
        {q['owner_table_id'] for q in owners['queries'] if q['entity'] == 'account'},
        ('cust_receipt_method_id', 'customer_id', 'receipt_method_id', 'site_use_id',
         'primary_flag', 'start_date', 'end_date', 'request_id'), validate_assignment)
    sources = {q['source_name']: q for q in identities['source_system_queries']}
    refs = {(q['orig_system'], q['owner_table_name'], q['reference']): q for q in identities['reference_queries']}
    owner_queries = {(q['entity'], q['owner_table_id']): q for q in owners['queries']}
    findings = []
    for number, row in enumerate(rows, 1):
        detail = {'row': number, 'receipt_input_present': bool(row['PAYMENT_METHOD_NAME'])}
        if not row['PAYMENT_METHOD_NAME']:
            findings.append({**detail, 'status': 'NOT_REQUESTED_EFFECTS_UNVERIFIED'})
            continue
        if owner_result['status'] != 'SUPPLIED_OWNERSHIP_CONSISTENT':
            findings.append({**detail, 'status': 'OWNERSHIP_NOT_VERIFIED'})
            continue
        code = sources[row['ORIG_SOURCE_SYSTEM_NAME']]['records'][0]['orig_system']
        keys = identity.reference_candidates(row)
        def owner_id(entity):
            key = keys[entity]
            return refs[code, key['owner'], key['reference']]['records'][0]['owner_table_id']
        account_id, account_site_id = owner_id('account'), owner_id('account_site')
        expected_set = owner_queries['account_site', account_site_id]['records'][0]['set_id']
        method, site, assignment = methods.get(row['PAYMENT_METHOD_NAME']), sites.get(account_site_id), assignments.get(account_id)
        if not method or not method['complete'] or not site or not site['complete'] or not assignment or not assignment['complete']:
            findings.append({**detail, 'status': 'RECEIPT_QUERY_MISSING_OR_INCOMPLETE'})
            continue
        detail['observed_account_assignments'] = len(assignment['records'])
        if len(method['records']) != 1:
            findings.append({**detail, 'status': 'METHOD_NOT_FOUND' if not method['records'] else 'AMBIGUOUS_METHOD_ROWS'})
            continue
        active_bill_to = [r for r in site['records'] if r['status'] == 'A' and r['site_use_code'] == 'BILL_TO']
        if len(active_bill_to) != 1:
            findings.append({**detail, 'status': 'ACTIVE_BILL_TO_NOT_FOUND' if not active_bill_to else 'AMBIGUOUS_ACTIVE_BILL_TO'})
            continue
        bill_to = active_bill_to[0]
        if bill_to['set_id'] != expected_set:
            findings.append({**detail, 'status': 'BILL_TO_SET_MISMATCH'})
            continue
        records = assignment['records']
        ids = [r['cust_receipt_method_id'] for r in records]
        if len(ids) != len(set(ids)):
            findings.append({**detail, 'status': 'DUPLICATE_ASSIGNMENT_ROWS'})
            continue
        method_id = method['records'][0]['receipt_method_id']
        matching = [r for r in records if r['receipt_method_id'] == method_id and r['site_use_id'] == bill_to['site_use_id']]
        detail['other_assignment_rows'] = len(records) - len(matching)
        if len(matching) != 1:
            findings.append({**detail, 'status': 'SCOPED_ASSIGNMENT_NOT_FOUND' if not matching else 'ASSIGNMENT_HISTORY_OR_DUPLICATE_REVIEW_REQUIRED'})
            continue
        actual = matching[0]
        expected_start = values.expected_value('ACCOUNT_ESTABLISHED_DATE', row['ACCOUNT_ESTABLISHED_DATE'] or '1900/01/01')
        expected_primary = row['PAYMENT_METHOD_PRIMARY_FLAG'] or 'N'
        detail['start_expectation_basis'] = 'EXPLICIT_ACCOUNT_DATE' if row['ACCOUNT_ESTABLISHED_DATE'] else 'REVIEWED_CONTROL_DEFAULT'
        detail['primary_expectation_basis'] = 'EXPLICIT_INPUT' if row['PAYMENT_METHOD_PRIMARY_FLAG'] else 'REVIEWED_INTERFACE_DEFAULT'
        status = ('RECEIPT_VALUE_MISMATCH' if actual['start_date'] != expected_start or actual['primary_flag'] != expected_primary else
                  'END_DATE_EFFECT_REVIEW_REQUIRED' if actual['end_date'] is not None else 'SELECTED_RECEIPT_VALUES_MATCH')
        findings.append({**detail, 'status': status})
    requested = [f for f in findings if f['receipt_input_present']]
    match = bool(requested) and all(f['status'] == 'SELECTED_RECEIPT_VALUES_MATCH' for f in requested)
    mismatch = any(f['status'] in ('RECEIPT_VALUE_MISMATCH', 'BILL_TO_SET_MISMATCH') for f in requested)
    return {'schema_version': 'ar-customer-receipt-review-v1',
        'status': 'RECEIPT_VALUE_MISMATCH' if mismatch else 'SELECTED_RECEIPT_VALUES_MATCH' if match else
                  'NO_RECEIPT_INPUT_EFFECTS_UNVERIFIED' if not requested else 'RECEIPT_EVIDENCE_INCOMPLETE',
        'candidate_sha256': owner_result['candidate_sha256'], 'environment_url': environment_url,
        'operation_intent': operation, 'ownership_evidence_sha256': package.fingerprint(owners),
        'evidence_sha256': package.fingerprint(evidence), 'findings': findings,
        'selected_receipt_values_match': match, 'assignment_delta_verified': False,
        'request_correlation_verified': False, 'persisted_reconciliation_complete': False,
        'execution_authorized': False, 'journey_complete': False,
        'limits': ['Supplied after-state values do not prove creation, harmless replay or absence of unintended changes.',
                   'Complete account assignment evidence is retained; unrelated/history rows need before/after effect review.',
                   'This increment resolves active BILL_TO scope through the account site, including for a SHIP_TO candidate sharing that site; account-level-only scope remains separate.',
                   'Method/class business validity and REQUEST_ID=-BATCH_ID correlation need separate evidence; REQUEST_ID is not an ESS request ID.']}
