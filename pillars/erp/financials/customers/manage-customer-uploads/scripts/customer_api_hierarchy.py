"""Compare selected API hierarchy/values without I/O or execution authority."""
import re
from xml.etree import ElementTree as ET

import customers_package as package

SOAP = 'http://schemas.xmlsoap.org/soap/envelope/'
ACCOUNT = 'http://xmlns.oracle.com/apps/cdm/foundation/parties/customerAccountService/'
TYPES = ACCOUNT+'applicationModule/types/'
NIL = '{http://www.w3.org/2001/XMLSchema-instance}nil'
MISSING = object()


def text(element, name):
    if element is None:
        return MISSING
    values = element.findall('{'+ACCOUNT+'}'+name)
    package.require(len(values) <= 1, 'API_HIERARCHY_AMBIGUOUS_FIELD')
    if not values:
        return MISSING
    item = values[0]
    if item.get(NIL) in ('true', '1'):
        package.require(not item.text and not len(item), 'API_HIERARCHY_CONTRADICTORY_NIL')
        return None
    return item.text if item.text is not None else ''


def collection(pages):
    package.require(isinstance(pages, list) and 0 < len(pages) <= 20,
                    'API_HIERARCHY_PAGES_REQUIRED')
    result = []
    for index, p in enumerate(pages):
        package.require(isinstance(p, dict) and isinstance(p.get('items'), list) and
            all(type(p.get(k)) is int for k in ('offset', 'count', 'limit')) and
            type(p.get('hasMore')) is bool, 'API_HIERARCHY_PAGE_SCHEMA')
        package.require(p['offset'] == len(result) and p['count'] == len(p['items']) and
            p['limit'] > 0 and p['count'] <= p['limit'] and
            all(isinstance(item, dict) for item in p['items']) and
            (index == len(pages)-1 or p['hasMore']) and
            (not p['hasMore'] or p['count'] > 0), 'API_HIERARCHY_PAGE_SEQUENCE')
        result.extend(p['items'])
    return result, not pages[-1]['hasMore']


def identifier(value):
    if type(value) is int and value > 0:
        return str(value)
    if isinstance(value, str) and re.fullmatch(r'[1-9][0-9]*', value):
        return value
    return MISSING


def review(row, owners, account_xml, address_pages, purpose_pages):
    """Join exact source-resolved owners to account and organization address APIs.

    Caller binds the candidate, API-native reference review and raw central
    captures. Missing nested rows remain unverified, never global absence. This
    checks seven-owner relationships and selected explicit values only.
    """
    require = package.require
    require(isinstance(row, dict) and set(package.columns()) <= set(row), 'API_HIERARCHY_ROW_REQUIRED')
    require(isinstance(owners, dict) and set(owners) == {'party', 'location', 'party_site',
        'party_site_use', 'account', 'account_site', 'account_site_use'} and
        all(identifier(v) is not MISSING for v in owners.values()), 'API_HIERARCHY_OWNERS_REQUIRED')
    owners = {k: str(v) for k, v in owners.items()}
    require(isinstance(account_xml, bytes) and len(account_xml) <= 16*1024*1024 and
            b'<!DOCTYPE' not in account_xml.upper() and b'<!ENTITY' not in account_xml.upper(),
            'API_HIERARCHY_XML_CONTRACT')
    try:
        root = ET.fromstring(account_xml)
    except ET.ParseError as exc:
        raise package.InvalidInput('API_HIERARCHY_INVALID_XML') from exc
    require(root.tag == '{'+SOAP+'}Envelope', 'API_HIERARCHY_ENVELOPE')
    bodies = root.findall('{'+SOAP+'}Body')
    require(len(bodies) == 1 and len(bodies[0]) == 1 and
            bodies[0][0].tag == '{'+TYPES+'}getCustomerAccountResponse', 'API_HIERARCHY_OPERATION')
    results = bodies[0][0].findall('{'+TYPES+'}result')
    require(len(results) == 1, 'API_HIERARCHY_ACCOUNT_RESULT')
    account = results[0]
    require(account.get(NIL) not in ('true', '1'), 'API_HIERARCHY_NIL_ACCOUNT')
    findings = []

    def compare(name, actual, expected):
        status = ('VALUE_NOT_RETURNED' if actual is MISSING else
                  'MATCH' if actual is not None and actual == expected else 'MISMATCH')
        findings.append({'check': name, 'status': status})

    def select(elements, field, expected, xml=False):
        matches = [e for e in elements if identifier(text(e, field) if xml else e.get(field)) == expected]
        require(len(matches) <= 1, 'API_HIERARCHY_DUPLICATE_TARGET')
        return matches[0] if matches else None

    compare('account_identity', identifier(text(account, 'CustomerAccountId')), owners['account'])
    compare('account_party', identifier(text(account, 'PartyId')), owners['party'])
    sites = account.findall('{'+ACCOUNT+'}CustomerAccountSite')
    site = select(sites, 'CustomerAccountSiteId', owners['account_site'], True)
    require(site is None or site.get(NIL) not in ('true', '1'), 'API_HIERARCHY_NIL_SITE')
    uses = site.findall('{'+ACCOUNT+'}CustomerAccountSiteUse') if site is not None else []
    use = select(uses, 'SiteUseId', owners['account_site_use'], True)
    require(use is None or use.get(NIL) not in ('true', '1'), 'API_HIERARCHY_NIL_SITE_USE')
    compare('account_site_identity', identifier(text(site, 'CustomerAccountSiteId')), owners['account_site'])
    compare('account_site_account', identifier(text(site, 'CustomerAccountId')), owners['account'])
    compare('account_site_party_site', identifier(text(site, 'PartySiteId')), owners['party_site'])
    compare('account_site_use_identity', identifier(text(use, 'SiteUseId')), owners['account_site_use'])
    compare('account_site_use_parent', identifier(text(use, 'CustomerAccountSiteId')), owners['account_site'])
    compare('account_site_use_purpose', text(use, 'SiteUseCode'), row['SITE_USE_CODE'])
    set_id = text(site, 'SetId')
    set_valid = isinstance(set_id, str) and re.fullmatch(r'0|[1-9][0-9]*', set_id)
    compare('account_site_use_set', text(use, 'SetId'), set_id if set_valid else None)
    addresses, addresses_complete = collection(address_pages)
    purposes, purposes_complete = collection(purpose_pages)
    address = select(addresses, 'AddressId', owners['party_site'])
    purpose = select(purposes, 'AddressPurposeId', owners['party_site_use'])
    av = lambda key: address.get(key, MISSING) if address is not None else MISSING
    pv = lambda key: purpose.get(key, MISSING) if purpose is not None else MISSING
    compare('party_site_identity', identifier(av('AddressId')), owners['party_site'])
    compare('party_site_party', identifier(av('PartyId')), owners['party'])
    compare('party_site_location', identifier(av('LocationId')), owners['location'])
    compare('party_site_use_identity', identifier(pv('AddressPurposeId')), owners['party_site_use'])
    compare('party_site_use_parent', identifier(pv('AddressId')), owners['party_site'])
    compare('party_site_use_purpose', pv('Purpose'), row['SITE_USE_CODE'])
    for field, api in {'ACCOUNT_NUMBER':'AccountNumber', 'ACCOUNT_DESCRIPTION':'AccountName',
                       'ACCOUNT_TYPE':'CustomerType', 'CUSTOMER_CLASS':'CustomerClassCode'}.items():
        if row.get(field):
            compare(field, text(account, api), row[field])
    for field, api in {'PARTY_NUMBER':'PartyNumber', 'PARTY_SITE_NUMBER':'AddressNumber',
            'PARTY_SITE_NAME':'PartySiteName', 'ADDRESS_LINE_1':'Address1', 'CITY':'City',
            'STATE':'State', 'POSTAL_CODE':'PostalCode', 'COUNTRY':'Country'}.items():
        if row.get(field):
            compare(field, av(api), row[field])
    matched = addresses_complete and purposes_complete and all(f['status'] == 'MATCH' for f in findings)
    return {'schema_version': 'ar-customer-api-hierarchy-review-v1',
            'status': 'SELECTED_API_HIERARCHY_AND_VALUES_MATCH' if matched else 'API_HIERARCHY_REVIEW_REQUIRED',
            'findings': findings, 'collections_complete': addresses_complete and purposes_complete,
            'execution_authorized': False, 'persisted_reconciliation_complete': False,
            'limits': ['API-visible hierarchy and selected nonblank fields only.',
                'No full omitted-field, sibling-effect, profile-history, receipt, tax or DFF reconciliation.',
                'A missing nested entity is not global absence; set identity is not requested set-code resolution.']}
