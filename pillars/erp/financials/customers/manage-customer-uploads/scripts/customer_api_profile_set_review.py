"""Review API-visible site set and current account profile; no history inference."""
import re
from xml.etree import ElementTree as ET

import customers_package as package
from customer_api_hierarchy import ACCOUNT, SOAP, TYPES, NIL, MISSING, identifier

PROFILE = 'http://xmlns.oracle.com/apps/financials/receivables/customers/customerProfileService/'
PROFILE_TYPES = PROFILE+'types/'


def scalar(parent, namespace, name):
    if parent is None:
        return MISSING
    values = parent.findall('{'+namespace+'}'+name)
    package.require(len(values) <= 1, 'API_PROFILE_SET_DUPLICATE_FIELD')
    if not values:
        return MISSING
    value = values[0]
    package.require(not len(value) and value.get(NIL) in (None, 'true', 'false', '1', '0'),
                    'API_PROFILE_SET_SCALAR_CONTRACT')
    if value.get(NIL) in ('true', '1'):
        package.require(not value.text, 'API_PROFILE_SET_CONTRADICTORY_NIL')
        return None
    return value.text if value.text is not None else ''


def result(content, namespace, operation):
    package.require(isinstance(content, bytes) and len(content) <= 16*1024*1024 and
        b'\x00' not in content and b'<!DOCTYPE' not in content.upper() and
        b'<!ENTITY' not in content.upper(), 'API_PROFILE_SET_XML_CONTRACT')
    try:
        root = ET.fromstring(content)
    except ET.ParseError as exc:
        raise package.InvalidInput('API_PROFILE_SET_INVALID_XML') from exc
    bodies = root.findall('{'+SOAP+'}Body')
    package.require(root.tag == '{'+SOAP+'}Envelope' and len(bodies) == 1 and
        len(bodies[0]) == 1 and bodies[0][0].tag == '{'+namespace+'}'+operation,
        'API_PROFILE_SET_OPERATION')
    values = bodies[0][0].findall('{'+namespace+'}result')
    package.require(len(values) == 1 and values[0].get(NIL) not in ('true', '1'),
                    'API_PROFILE_SET_RESULT')
    return values[0]


def review(row, owners, account_xml, profile_xml=None):
    """Compare explicit inputs; before observations do not predict loader outcomes.

    Missing fields are omitted from observed_values, explicit xsi:nil stays None.
    Capturing the active profile proves neither complete profile history nor the
    status of its profile-class catalog entry. Caller retains candidate/phase and
    central-response hashes. This function performs no I/O.
    """
    require = package.require
    require(isinstance(row, dict) and all(isinstance(row.get(k), str) for k in
        ('ACCT_ADDRESS_SET_CODE', 'CUSTOMER_PROFILE_CLASS', 'ACCOUNT_NUMBER', 'SITE_USE_CODE')),
        'API_PROFILE_SET_ROW_REQUIRED')
    required_owners = ('party', 'account')
    selected_owners = (*required_owners, 'party_site', 'account_site', 'account_site_use')
    require(isinstance(owners, dict) and all(k in owners for k in required_owners) and
            all(identifier(owners[k]) is not MISSING for k in selected_owners if k in owners),
            'API_PROFILE_SET_OWNERS_REQUIRED')
    owners = {k: str(owners[k]) for k in selected_owners if k in owners}
    account = result(account_xml, TYPES, 'getCustomerAccountResponse')
    require(identifier(scalar(account, ACCOUNT, 'CustomerAccountId')) == owners['account'] and
            identifier(scalar(account, ACCOUNT, 'PartyId')) == owners['party'],
            'API_PROFILE_SET_ACCOUNT_SCOPE')
    if row['ACCOUNT_NUMBER']:
        require(scalar(account, ACCOUNT, 'AccountNumber') == row['ACCOUNT_NUMBER'],
                'API_PROFILE_SET_ACCOUNT_NUMBER')

    def select(parent, name, id_field, expected):
        elements = parent.findall('{'+ACCOUNT+'}'+name) if parent is not None else []
        selected = [e for e in elements if identifier(scalar(e, ACCOUNT, id_field)) == expected]
        require(len(selected) <= 1, 'API_PROFILE_SET_DUPLICATE_TARGET')
        if not selected:
            return None
        require(selected[0].get(NIL) not in ('true', '1'), 'API_PROFILE_SET_NIL_TARGET')
        return selected[0]

    # Mixed creates can resolve an existing account before the new site exists.
    # Keep its current profile; never substitute a sibling site to fill that gap.
    site = (select(account, 'CustomerAccountSite', 'CustomerAccountSiteId', owners['account_site'])
            if {'party_site', 'account_site'} <= set(owners) else None)
    if site is not None:
        require(identifier(scalar(site, ACCOUNT, 'CustomerAccountId')) == owners['account'] and
                identifier(scalar(site, ACCOUNT, 'PartySiteId')) == owners['party_site'],
                'API_PROFILE_SET_SITE_SCOPE')
    use = (select(site, 'CustomerAccountSiteUse', 'SiteUseId', owners['account_site_use'])
           if 'account_site_use' in owners else None)
    if use is not None:
        require(identifier(scalar(use, ACCOUNT, 'CustomerAccountSiteId')) == owners['account_site'] and
                scalar(use, ACCOUNT, 'SiteUseCode') == row['SITE_USE_CODE'], 'API_PROFILE_SET_USE_SCOPE')

    findings, observed, profile_observed = [], {}, {}

    def compare(field, value):
        if value is not MISSING:
            observed[field] = value
        status = ('VALUE_NOT_RETURNED' if value is MISSING else 'INPUT_OMITTED_OBSERVATION_ONLY'
                  if not row[field] else 'MATCH' if value == row[field] else 'MISMATCH')
        findings.append({'check': field, 'status': status})

    set_id, use_set = scalar(site, ACCOUNT, 'SetId'), scalar(use, ACCOUNT, 'SetId')
    valid_set = isinstance(set_id, str) and re.fullmatch(r'0|[1-9][0-9]*', set_id)
    findings.append({'check': 'account_site_use_set', 'status':
        'VALUE_NOT_RETURNED' if set_id is MISSING or use_set is MISSING else
        'MATCH' if valid_set and set_id == use_set else 'MISMATCH'})
    compare('ACCT_ADDRESS_SET_CODE', scalar(site, ACCOUNT, 'SetCode'))
    for key, value in (('account_site_set_id', set_id), ('account_site_use_set_id', use_set)):
        if value is not MISSING:
            profile_observed[key] = value

    profile = None
    if profile_xml is not None:
        require(bool(row['ACCOUNT_NUMBER']), 'API_PROFILE_SET_PROFILE_NUMBER_REQUIRED')
        container = result(profile_xml, PROFILE_TYPES, 'getActiveCustomerProfileResponse')
        values = container.findall('{'+PROFILE+'}Value')
        require(len(values) <= 1, 'API_PROFILE_SET_MULTIPLE_PROFILES')
        if values:
            require(values[0].get(NIL) not in ('true', '1'), 'API_PROFILE_SET_NIL_PROFILE')
            profile = values[0]
            require(identifier(scalar(profile, PROFILE, 'CustomerAccountId')) == owners['account'] and
                identifier(scalar(profile, PROFILE, 'PartyId')) == owners['party'] and
                scalar(profile, PROFILE, 'AccountNumber') == row['ACCOUNT_NUMBER'] and
                scalar(profile, PROFILE, 'SiteNumber') is None,
                'API_PROFILE_SET_PROFILE_SCOPE')
            require(identifier(scalar(profile, PROFILE, 'CustomerAccountProfileId')) is not MISSING,
                    'API_PROFILE_SET_PROFILE_ID')
            for field in ('CustomerAccountProfileId', 'EffectiveStartDate', 'EffectiveEndDate'):
                value = scalar(profile, PROFILE, field)
                if value is not MISSING:
                    profile_observed[field] = value
    compare('CUSTOMER_PROFILE_CLASS', scalar(profile, PROFILE, 'ProfileClassName'))
    matched = all(f['status'] in ('MATCH', 'INPUT_OMITTED_OBSERVATION_ONLY') for f in findings)
    return {'schema_version': 'ar-customer-api-profile-set-review-v1',
        'status': 'SELECTED_CURRENT_PROFILE_AND_SET_MATCH' if matched else 'API_PROFILE_SET_REVIEW_REQUIRED',
        'findings': findings, 'observed_values': observed, 'observed_metadata': profile_observed,
        'selected_checks_match': matched, 'profile_observed': profile is not None,
        'execution_authorized': False, 'persisted_reconciliation_complete': False,
        'profile_history_complete': False, 'profile_class_catalog_validated': False,
        'limits': ['Exact API-visible selected account/site/use only; missing nested rows do not prove absence.',
            'Current account-level profile only; effective dates retained as returned, without raw Oracle DATE or history claims.',
            'Blank inputs are observations, not inferred defaults or proof of preservation.',
            'SetCode is observed on the selected site, not a general reference-set catalog validation.',
            'Before-state differences are not predicted loader failures; before/after effect review remains required.']}
