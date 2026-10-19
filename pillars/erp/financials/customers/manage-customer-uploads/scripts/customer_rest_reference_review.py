"""Review scoped hubSourceSystemReferences observations; no network or writes."""
from datetime import date

import customers_package as package

OWNER_ENTITIES = {
    'ORA_PARTIES': 'party',
    'ORA_LOCATIONS': 'location',
    'ORA_PARTY_SITES': 'party_site',
    'ORA_PARTY_SITE_USES': 'party_site_use',
    'ORA_CUST_ACCOUNTS': 'account',
    'ORA_CUST_ACCT_SITES_ALL': 'account_site',
    'ORA_CUST_SITE_USES_ALL': 'account_site_use',
}
KEY = ('SourceSystem', 'OwnerEntityObject', 'SourceSystemReferenceValue')
FIELDS = {*KEY, 'SourceSystemReferenceId', 'OwnerEntityId', 'Status',
          'StartDateActive', 'EndDateActive'}


def classify(response, expected):
    """Compare observed identities, without asserting absence or effective dates.

    Expected entries contain the full API tuple and an independently reviewed
    OwnerEntityId. They must not be manufactured from this same response.
    """
    require = package.require
    require(isinstance(expected, list) and bool(expected), 'REST_REFERENCE_EXPECTATIONS_REQUIRED')
    expectations = {}
    for entry in expected:
        require(isinstance(entry, dict) and set(entry) == {*KEY, 'OwnerEntityId'},
                'REST_REFERENCE_EXPECTATION_SCHEMA')
        require(all(isinstance(entry[k], str) and entry[k].strip() for k in KEY)
                and entry['OwnerEntityObject'] in OWNER_ENTITIES
                and type(entry['OwnerEntityId']) is int and entry['OwnerEntityId'] > 0,
                'REST_REFERENCE_EXPECTATION_VALUES')
        key = tuple(entry[k] for k in KEY)
        require(key not in expectations, 'REST_REFERENCE_DUPLICATE_EXPECTATION')
        expectations[key] = entry['OwnerEntityId']
    require(isinstance(response, dict) and isinstance(response.get('items'), list)
            and all(type(response.get(k)) is int for k in ('count', 'offset', 'limit'))
            and type(response.get('hasMore')) is bool, 'REST_REFERENCE_RESPONSE_SCHEMA')
    rows = response['items']
    require(response['count'] == len(rows) and response['offset'] >= 0
            and response['limit'] > 0 and len(rows) <= response['limit'],
            'REST_REFERENCE_PAGE_CONTRACT')
    grouped = {key: [] for key in expectations}
    unrequested = 0
    for row in rows:
        require(isinstance(row, dict) and FIELDS <= set(row), 'REST_REFERENCE_FIELDS_MISSING')
        require(all(isinstance(row[k], str) and row[k].strip() for k in (*KEY, 'Status'))
                and all(type(row[k]) is int and row[k] > 0 for k in ('SourceSystemReferenceId', 'OwnerEntityId')),
                'REST_REFERENCE_VALUE_TYPE')
        for field in ('StartDateActive', 'EndDateActive'):
            value = row[field]
            if field == 'EndDateActive' and value is None:
                continue
            try:
                require(isinstance(value, str) and len(value) == 10,
                        'REST_REFERENCE_DATE_FORMAT')
                date.fromisoformat(value)
            except (ValueError, TypeError) as exc:
                raise package.InvalidInput('REST_REFERENCE_DATE_FORMAT') from exc
        key = tuple(row[k] for k in KEY)
        if key in grouped:
            grouped[key].append(row)
        else:
            unrequested += 1
    findings = []
    for key, owner_id in expectations.items():
        matches = grouped[key]
        status = ('NO_VISIBLE_MATCH_NOT_GLOBAL_ABSENCE' if not matches else
                  'AMBIGUOUS_REFERENCE' if len(matches) > 1 else
                  'OWNER_ID_MISMATCH' if matches[0]['OwnerEntityId'] != owner_id else
                  'REFERENCE_NOT_ACTIVE' if matches[0]['Status'] != 'A' else
                  'SINGLE_VISIBLE_IDENTITY_CORROBORATED')
        findings.append({'entity': OWNER_ENTITIES[key[1]], 'key': dict(zip(KEY, key)),
                         'status': status, 'observed_rows': len(matches)})
    complete_page = response['offset'] == 0 and not response['hasMore']
    all_matched = all(f['status'] == 'SINGLE_VISIBLE_IDENTITY_CORROBORATED' for f in findings)
    status = ('INCOMPLETE_PAGINATION' if not complete_page else
              'SCOPED_IDENTITIES_CORROBORATED_PARTIAL_EVIDENCE' if all_matched else
              'IDENTITY_REVIEW_REQUIRED')
    return {'schema_version': 'ar-customer-rest-reference-review-v1', 'status': status,
            'findings': findings, 'unrequested_rows': unrequested,
            'response_sha256': package.fingerprint(response),
            'expectations_sha256': package.fingerprint(expected),
            'execution_authorized': False, 'live_ready': False,
            'persisted_reconciliation_complete': False, 'effective_date_validity_verified': False,
            'limits': ['Supplied observations do not authenticate source, environment, principal or capture time.',
                       'Reference ownership is not physical parent, field-value or complete before/after reconciliation.',
                       'Date-only REST bounds cannot substitute for Oracle DATE seconds or database as-of time.',
                       'No visible reference is not global absence or permission to create; duplicates are not deduplicated.']}
