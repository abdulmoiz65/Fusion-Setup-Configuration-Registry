"""Classify one scoped Customer Account Sites LOV response; no network calls."""
import customers_package as package

FIELDS = {'SiteUseId', 'CustomerAccountId', 'PartyNumber', 'AccountNumber', 'PrimarySite', 'SetName'}


def classify(response, expected_site_use_id, expected_account_id=None):
    require = package.require
    require(type(expected_site_use_id) is int and expected_site_use_id > 0, 'REST_SITE_ID_REQUIRED')
    require(expected_account_id is None or type(expected_account_id) is int and expected_account_id > 0,
            'REST_ACCOUNT_ID_INVALID')
    require(isinstance(response, dict) and isinstance(response.get('items'), list)
        and type(response.get('count')) is int and type(response.get('hasMore')) is bool
        and type(response.get('offset')) is int and type(response.get('limit')) is int,
        'REST_SITE_RESPONSE_SCHEMA')
    rows = response['items']
    require(response['count'] == len(rows) and response['offset'] >= 0
        and response['limit'] > 0 and len(rows) <= response['limit'], 'REST_SITE_PAGE_CONTRACT')
    for row in rows:
        require(isinstance(row, dict) and FIELDS <= set(row), 'REST_SITE_FIELDS_MISSING')
        require(type(row['SiteUseId']) is int and row['SiteUseId'] > 0
            and type(row['CustomerAccountId']) is int and row['CustomerAccountId'] > 0,
            'REST_SITE_ID_TYPE')
        require(all(row[k] is None or isinstance(row[k], str) for k in FIELDS - {'SiteUseId', 'CustomerAccountId'}),
                'REST_SITE_VALUE_TYPE')
    if any(row['SiteUseId'] != expected_site_use_id for row in rows):
        status = 'UNEXPECTED_SITE_ID'
    elif expected_account_id is not None and any(row['CustomerAccountId'] != expected_account_id for row in rows):
        status = 'ACCOUNT_ID_MISMATCH'
    elif len(rows) > 1:
        status = 'AMBIGUOUS_EXACT_MATCH'
    elif response['hasMore'] or response['offset'] != 0:
        status = 'INCOMPLETE_PAGINATION'
    elif not rows:
        status = 'NO_VISIBLE_MATCH_NOT_GLOBAL_ABSENCE'
    else:
        status = 'SINGLE_VISIBLE_MATCH_PARTIAL_EVIDENCE'
    return {'schema_version': 'ar-customer-rest-site-review-v1', 'status': status,
        'observed_rows': len(rows), 'has_more': response['hasMore'],
        'response_sha256': package.fingerprint(response),
        'live_ready': False, 'persisted_reconciliation_complete': False,
        'limits': ['LOV rows are partial visible evidence, not global source-key identity or complete hierarchy/value reconciliation.',
                   'Repeated identical rows remain ambiguous; no automatic deduplication or selection.',
                   'HTTP success, empty results and a single visible row do not authorize creation or update.']}
