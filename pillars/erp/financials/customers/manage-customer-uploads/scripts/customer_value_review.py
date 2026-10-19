"""Compare selected supplied persisted values; no query, submission or success authority."""
from datetime import datetime
import re

import customers_package as package
import customer_identity_review as identity
import customer_ownership_review as ownership

# Selected first-case targets, supported by the reviewed interface mapping and
# FSCM schema. Actual loader persistence/update semantics still need live tests.
FIELDS = {
    'PARTY_NUMBER': ('party', 'PARTY_NUMBER'),
    'PARTY_NAME': ('party', 'PARTY_NAME'),
    'DUNS_NUMBER': ('party', 'DUNS_NUMBER_C'),
    'TAXPAYER_ID_NUM': ('party', 'JGZZ_FISCAL_CODE'),
    'GSA_INDICATOR_FLAG': ('party', 'GSA_INDICATOR_FLAG'),
    'ACCOUNT_NUMBER': ('account', 'ACCOUNT_NUMBER'),
    'ACCOUNT_DESCRIPTION': ('account', 'ACCOUNT_NAME'),
    'ACCOUNT_TYPE': ('account', 'CUSTOMER_TYPE'),
    'CUSTOMER_CLASS': ('account', 'CUSTOMER_CLASS_CODE'),
    'ACCOUNT_ESTABLISHED_DATE': ('account', 'ACCOUNT_ESTABLISHED_DATE'),
    'PARTY_SITE_NUMBER': ('party_site', 'PARTY_SITE_NUMBER'),
    'PARTY_SITE_NAME': ('party_site', 'PARTY_SITE_NAME'),
    'IDENTIFYING_ADDRESS_FLAG': ('party_site', 'IDENTIFYING_ADDRESS_FLAG'),
    'MAIL_STOP': ('party_site', 'MAILSTOP'),
    'ACCT_SITE_LANGUAGE': ('account_site', 'ACCT_SITE_LANGUAGE'),
    'TRANSLATED_CUSTOMER_NAME': ('account_site', 'TRANSLATED_CUSTOMER_NAME'),
    'ADDRESS_LINE_1': ('location', 'ADDRESS1'),
    'ADDRESS_LINE_2': ('location', 'ADDRESS2'),
    'ADDRESS_LINE_3': ('location', 'ADDRESS3'),
    'ADDRESS_LINE_4': ('location', 'ADDRESS4'),
    'FLOOR_NUMBER': ('location', 'FLOOR_NUMBER'),
    'BUILDING': ('location', 'BUILDING'),
    'PROVINCE': ('location', 'PROVINCE'),
    'COUNTY': ('location', 'COUNTY'),
    'ADDRESS_LINES_PHONETIC': ('location', 'ADDRESS_LINES_PHONETIC'),
    'POSTAL_PLUS4_CODE': ('location', 'POSTAL_PLUS4_CODE'),
    'ADDRESS_DESCRIPTION': ('location', 'DESCRIPTION'),
    'ADDR_SHORT_DESCRIPTION': ('location', 'SHORT_DESCRIPTION'),
    'SALES_TAX_GEOCODE': ('location', 'SALES_TAX_GEOCODE'),
    'SALES_TAX_INSIDE_CITY_LIMITS': ('location', 'SALES_TAX_INSIDE_CITY_LIMITS'),
    'HOUSE_TYPE': ('location', 'HOUSE_TYPE'),
    'TIMEZONE_CODE': ('location', 'TIMEZONE_CODE'),
    **{f'ADDR_ELEMENT_ATTRIBUTE{i}': ('location', f'ADDR_ELEMENT_ATTRIBUTE{i}') for i in range(1, 6)},
    'CITY': ('location', 'CITY'),
    'STATE': ('location', 'STATE'),
    'POSTAL_CODE': ('location', 'POSTAL_CODE'),
    'COUNTRY': ('location', 'COUNTRY'),
    'SITE_USE_CODE': ('account_site_use', 'SITE_USE_CODE'),
    'SITE_USE_PRIMARY_FLAG': ('account_site_use', 'PRIMARY_FLAG'),
    'SITE_LOCATION': ('account_site_use', 'LOCATION'),
    'ATTRIBUTE_CATEGORY': ('account', 'ATTRIBUTE_CATEGORY'),
    **{f'ATTRIBUTE{i}': ('account', f'ATTRIBUTE{i}') for i in range(1, 31)},
}
IDENTITY_FIELDS = {
    'ORIG_SOURCE_SYSTEM_NAME', 'PARTY_ORIG_SYSTEM_REFERENCE',
    'CUST_ORIG_SYSTEM_REFERENCE', 'LOCATION_ORIG_SYSTEM_REFERENCE',
    'CUST_SITE_ORIG_SYS_REF', 'CUST_SITEUSE_ORIG_SYS_REF',
}
require = package.require


def expected_value(field, value):
    if field != 'ACCOUNT_ESTABLISHED_DATE':
        return value  # Do not trim, case-fold, coerce IDs or normalize Unicode.
    require(re.fullmatch(r'[0-9]{4}/[0-9]{2}/[0-9]{2}', value) is not None, 'VALUE_DATE_FORMAT')
    try:
        return datetime.strptime(value, '%Y/%m/%d').isoformat(timespec='seconds')
    except ValueError as exc:
        raise package.InvalidInput('VALUE_DATE_FORMAT') from exc


def analyze(candidate, operation, environment_url, identities, owners, evidence):
    owner_result = ownership.analyze(candidate, operation, environment_url, identities, owners)
    require(owners['phase'] == 'after', 'VALUE_AFTER_PHASE_REQUIRED')
    require(isinstance(evidence, dict) and set(evidence) == {
        'schema_version', 'candidate_sha256', 'environment_url', 'operation_intent',
        'ownership_evidence_sha256', 'captured_at', 'evidence_reference', 'queries'}, 'VALUE_EVIDENCE_SCHEMA')
    require(evidence['schema_version'] == 'ar-customer-value-evidence-v1', 'VALUE_EVIDENCE_VERSION')
    require(evidence['candidate_sha256'] == owner_result['candidate_sha256']
        and evidence['environment_url'] == environment_url and evidence['operation_intent'] == operation
        and evidence['ownership_evidence_sha256'] == package.fingerprint(owners), 'VALUE_BINDING_MISMATCH')
    require(identity.text(evidence['evidence_reference']), 'VALUE_PROVENANCE_REQUIRED')
    try:
        captured = datetime.fromisoformat(evidence['captured_at'].replace('Z', '+00:00'))
        owner_capture = datetime.fromisoformat(owners['captured_at'].replace('Z', '+00:00'))
        require(captured.tzinfo is not None and captured >= owner_capture, 'VALUE_CAPTURE_TIME')
    except (ValueError, TypeError, AttributeError) as exc:
        raise package.InvalidInput('VALUE_CAPTURE_TIME') from exc
    require(isinstance(evidence['queries'], list), 'VALUE_QUERIES_REQUIRED')
    allowed = {(q['entity'], q['owner_table_id']) for q in owners['queries']}
    queries = {}
    for query in evidence['queries']:
        require(isinstance(query, dict) and set(query) == {'entity', 'owner_table_id', 'complete', 'records'}, 'VALUE_QUERY_SCHEMA')
        require(isinstance(query['entity'], str) and isinstance(query['owner_table_id'], str), 'VALUE_QUERY_ID')
        key = query['entity'], query['owner_table_id']
        require(key in allowed, 'VALUE_QUERY_OUTSIDE_OWNERSHIP_SCOPE')
        require(key not in queries, 'VALUE_DUPLICATE_QUERY')
        require(type(query['complete']) is bool and isinstance(query['records'], list), 'VALUE_QUERY_VALUES')
        fields = {column for entity, column in FIELDS.values() if entity == key[0]}
        for record in query['records']:
            require(isinstance(record, dict) and set(record) <= fields, 'VALUE_RECORD_FIELDS')
            require(all(value is None or isinstance(value, str) for value in record.values()), 'VALUE_RECORD_TYPE')
        queries[key] = query
    sources = {q['source_name']: q for q in identities['source_system_queries']}
    refs = {(q['orig_system'], q['owner_table_name'], q['reference']): q for q in identities['reference_queries']}
    findings = []
    rows = [dict(zip(package.columns(), values)) for values in package.inspect_zip(candidate)]
    for number, row in enumerate(rows, 1):
        for field, value in row.items():
            if not value:
                continue  # Blank update semantics/default effects are not certified here.
            if field not in FIELDS:
                status = 'SEPARATE_IDENTITY_REVIEW' if field in IDENTITY_FIELDS else 'FIELD_NOT_COVERED'
            elif owner_result['status'] != 'SUPPLIED_OWNERSHIP_CONSISTENT':
                status = 'OWNERSHIP_NOT_VERIFIED'
            else:
                entity, column = FIELDS[field]
                code = sources[row['ORIG_SOURCE_SYSTEM_NAME']]['records'][0]['orig_system']
                ref = identity.reference_candidates(row)[entity]
                owner_id = refs[code, ref['owner'], ref['reference']]['records'][0]['owner_table_id']
                query = queries.get((entity, owner_id))
                if not query or not query['complete']:
                    status = 'VALUE_QUERY_MISSING_OR_INCOMPLETE'
                elif len(query['records']) != 1:
                    status = 'TARGET_NOT_FOUND' if not query['records'] else 'AMBIGUOUS_TARGET_ROWS'
                elif column not in query['records'][0]:
                    status = 'VALUE_NOT_RETURNED'
                else:
                    status = 'MATCH' if query['records'][0][column] == expected_value(field, value) else 'VALUE_MISMATCH'
            findings.append({'row': number, 'field': field, 'status': status})
    selected = [f for f in findings if f['field'] in FIELDS]
    matched = bool(selected) and all(f['status'] == 'MATCH' for f in selected)
    return {'schema_version': 'ar-customer-value-review-v1',
        'status': 'VALUE_MISMATCH' if any(f['status'] == 'VALUE_MISMATCH' for f in selected) else
                  'SELECTED_VALUES_MATCH' if matched else 'VALUE_EVIDENCE_INCOMPLETE',
        'candidate_sha256': owner_result['candidate_sha256'],
        'ownership_evidence_sha256': package.fingerprint(owners),
        'evidence_sha256': package.fingerprint(evidence), 'findings': findings,
        'selected_values_match': matched, 'persisted_reconciliation_complete': False,
        'execution_authorized': False, 'journey_complete': False,
        'limits': ['Only listed nonblank input values are compared; supplied evidence is not authenticated by this helper.',
                   'Party DUNS, taxpayer ID and GSA checks do not reconcile organization-profile history or tax registrations.',
                   'DFF checks compare stored account columns only; context definitions, value-set validation and blank/update effects require separate review.',
                   'Identity, defaults, blank/update effects, profile, reference-set resolution, receipt methods and other fields require separate review.',
                   'Value agreement does not prove creation, update/reuse intent, process success or Journey synchronization.']}
