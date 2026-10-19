"""Compare supplied party-tax-profile evidence; never infer async completion."""
from datetime import datetime

import customers_package as package
import customer_identity_review as identity
import customer_ownership_review as ownership
import customer_profile_set_review as catalogs

require = package.require
FIELD = 'TAXPAYER_REGISTRATION_NUM'
RECORD_FIELDS = ('party_tax_profile_id', 'party_id', 'party_type_code',
                 'rep_registration_number', 'site_flag', 'customer_flag', 'supplier_flag')


def validate_profile(party_id, record):
    require(record['party_id'] == party_id
            and ownership.identifier(record['party_tax_profile_id'])
            and identity.text(record['party_type_code']), 'TAX_PROFILE_SCOPE_OR_ID')
    require(record['rep_registration_number'] is None
            or isinstance(record['rep_registration_number'], str), 'TAX_VALUE_TYPE')
    for field in ('site_flag', 'customer_flag', 'supplier_flag'):
        require(record[field] is None or record[field] in ('Y', 'N'), 'TAX_FLAG_TYPE')


def analyze(candidate, operation, environment_url, identities, owners, evidence):
    owner_result = ownership.analyze(candidate, operation, environment_url, identities, owners)
    require(owners['phase'] == 'after', 'TAX_AFTER_PHASE_REQUIRED')
    require(isinstance(evidence, dict) and set(evidence) == {
        'schema_version', 'candidate_sha256', 'environment_url', 'operation_intent',
        'ownership_evidence_sha256', 'captured_at', 'evidence_reference', 'profile_queries'},
        'TAX_EVIDENCE_SCHEMA')
    require(evidence['schema_version'] == 'ar-customer-tax-evidence-v1', 'TAX_EVIDENCE_VERSION')
    require(evidence['candidate_sha256'] == owner_result['candidate_sha256']
            and evidence['environment_url'] == environment_url
            and evidence['operation_intent'] == operation
            and evidence['ownership_evidence_sha256'] == package.fingerprint(owners),
            'TAX_BINDING_MISMATCH')
    require(identity.text(evidence['evidence_reference']), 'TAX_PROVENANCE_REQUIRED')
    try:
        captured = datetime.fromisoformat(evidence['captured_at'].replace('Z', '+00:00'))
        owner_capture = datetime.fromisoformat(owners['captured_at'].replace('Z', '+00:00'))
        require(captured.tzinfo is not None and captured >= owner_capture, 'TAX_CAPTURE_TIME')
    except (ValueError, TypeError, AttributeError) as exc:
        raise package.InvalidInput('TAX_CAPTURE_TIME') from exc
    queries = catalogs.indexed_queries(evidence['profile_queries'], 'party_id',
        {q['owner_table_id'] for q in owners['queries'] if q['entity'] == 'party'},
        RECORD_FIELDS, validate_profile)
    sources = {q['source_name']: q for q in identities['source_system_queries']}
    refs = {(q['orig_system'], q['owner_table_name'], q['reference']): q
            for q in identities['reference_queries']}
    rows = [dict(zip(package.columns(), raw)) for raw in package.inspect_zip(candidate)]
    findings = []
    for number, row in enumerate(rows, 1):
        detail = {'row': number, 'field': FIELD, 'tax_input_present': bool(row[FIELD])}
        if not row[FIELD]:
            status = 'NOT_REQUESTED_EFFECTS_UNVERIFIED'
        elif owner_result['status'] != 'SUPPLIED_OWNERSHIP_CONSISTENT':
            status = 'OWNERSHIP_NOT_VERIFIED'
        else:
            code = sources[row['ORIG_SOURCE_SYSTEM_NAME']]['records'][0]['orig_system']
            ref = identity.reference_candidates(row)['party']
            party_id = refs[code, ref['owner'], ref['reference']]['records'][0]['owner_table_id']
            query = queries.get(party_id)
            if not query or not query['complete']:
                status = 'TAX_QUERY_MISSING_OR_INCOMPLETE'
            else:
                records = query['records']
                detail['observed_profile_rows'] = len(records)
                ids = [r['party_tax_profile_id'] for r in records]
                target = [r for r in records if r['party_type_code'] == 'THIRD_PARTY']
                detail['other_profile_rows'] = len(records) - len(target)
                if len(ids) != len(set(ids)):
                    status = 'DUPLICATE_TAX_PROFILE_ROWS'
                elif len(target) != 1:
                    status = 'TAX_PROFILE_NOT_OBSERVED' if not target else 'AMBIGUOUS_TAX_PROFILES'
                else:
                    status = ('SELECTED_TAX_VALUE_MATCH' if target[0]['rep_registration_number'] == row[FIELD]
                              else 'TAX_VALUE_MISMATCH')
        findings.append({**detail, 'status': status})
    requested = [f for f in findings if f['tax_input_present']]
    match = bool(requested) and all(f['status'] == 'SELECTED_TAX_VALUE_MATCH' for f in requested)
    mismatch = any(f['status'] == 'TAX_VALUE_MISMATCH' for f in requested)
    return {'schema_version': 'ar-customer-tax-review-v1',
        'status': 'TAX_VALUE_MISMATCH' if mismatch else 'SELECTED_TAX_VALUES_MATCH' if match
                  else 'NO_TAX_INPUT_EFFECTS_UNVERIFIED' if not requested else 'TAX_EVIDENCE_INCOMPLETE',
        'candidate_sha256': owner_result['candidate_sha256'], 'environment_url': environment_url,
        'operation_intent': operation, 'ownership_evidence_sha256': package.fingerprint(owners),
        'evidence_sha256': package.fingerprint(evidence), 'findings': findings,
        'selected_tax_values_match': match, 'callback_completion_verified': False,
        'profile_effects_verified': False, 'request_correlation_verified': False,
        'persisted_reconciliation_complete': False, 'execution_authorized': False,
        'journey_complete': False,
        'limits': ['A matching value can predate this attempt; it does not prove callback execution.',
                   'Tax callback is asynchronous. Missing or mismatched readback is an observation, not retry permission.',
                   'Blank input is excluded by the reviewed callback; before/after effects remain a separate check.',
                   'No site tax profile or tax-regime registration is substituted for the THIRD_PARTY profile.']}
