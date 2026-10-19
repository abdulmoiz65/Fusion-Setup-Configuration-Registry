"""Candidate-bound customer identity observations using the existing core REST CLI.

This narrow projection never authorizes execution or establishes global absence.
It does not implement transport, authentication, retries or a SOAP substitute.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

import customers_package as package
import customer_api_snapshot as snapshot

ORGANIZATIONS = '/crmRestApi/resources/11.13.18.05/hubOrganizations'
ACCOUNT_SITES = '/fscmRestApi/resources/11.13.18.05/customerAccountSitesLOV'
REMAINING = ['source-system name-to-code validation', 'independent cross-party site-number matching',
             'complete account/site-use hierarchy and persisted DFF values', 'active customer profiles',
             'all required location fields', 'operation ownership and full before/after reconciliation',
             'Data Loader submission and diagnostics compatibility']

# Documented organization Address fields, not profile or account-site fields.
LOCATION_FIELDS = {
    **{f'ADDRESS_LINE_{i}': f'Address{i}' for i in range(1, 5)},
    **{f'ADDR_ELEMENT_ATTRIBUTE{i}': f'AddrElementAttribute{i}' for i in range(1, 6)},
    'FLOOR_NUMBER': 'FloorNumber', 'BUILDING': 'Building', 'PROVINCE': 'Province',
    'COUNTY': 'County', 'ADDRESS_LINES_PHONETIC': 'AddressLinesPhonetic',
    'POSTAL_PLUS4_CODE': 'PostalPlus4Code', 'ADDRESS_DESCRIPTION': 'Description',
    'HOUSE_TYPE': 'HouseType', 'CITY': 'City', 'STATE': 'State',
    'POSTAL_CODE': 'PostalCode', 'COUNTRY': 'Country',
}


def location_values(row, address, phase):
    """Compare explicit after-values only; omitted input is never expected null."""
    findings, observed = [], {}
    for field, api in LOCATION_FIELDS.items():
        expected = row.get(field, '')
        package.require(isinstance(expected, str), 'REST_LOCATION_INPUT_TEXT_REQUIRED')
        if api not in address:
            status = 'VALUE_NOT_RETURNED'
        else:
            value = address[api]
            package.require(value is None or isinstance(value, str), 'REST_LOCATION_RESPONSE_TEXT_REQUIRED')
            observed[field] = value
            status = ('BEFORE_VALUE_OBSERVED' if phase == 'before' else
                      'OMITTED_INPUT_OBSERVED_NOT_EFFECT_VERIFIED' if not expected else
                      'MATCH' if value == expected else 'MISMATCH')
        findings.append({'field': field, 'status': status, 'requested': bool(expected)})
    unexposed = [field for field in ('ADDR_SHORT_DESCRIPTION', 'SALES_TAX_GEOCODE',
                  'SALES_TAX_INSIDE_CITY_LIMITS', 'TIMEZONE_CODE') if row.get(field)]
    return {'findings': findings, 'observed_values': observed, 'requested_unexposed_fields': unexposed,
            'requested_after_values_match': phase == 'after' and not unexposed and
                all(not f['requested'] or f['status'] == 'MATCH' for f in findings),
            'all_location_values_verified': False}


def selections(candidate, operation, environment_url):
    package.inspect_candidate(candidate, operation)
    snapshot.plan(candidate, operation, environment_url, {})
    rows = [dict(zip(package.columns(), row)) for row in package.inspect_zip(candidate)]
    package.require(1 <= len(rows) <= 20, 'REST_IDENTITY_ROW_BOUND')
    for row in rows:
        for field in ('PARTY_NUMBER', 'PARTY_SITE_NUMBER', 'ACCOUNT_NUMBER'):
            package.require(bool(re.fullmatch(r'[A-Za-z0-9_.-]{1,80}', row.get(field, ''))),
                            'REST_IDENTITY_EXPLICIT_SAFE_NUMBERS_REQUIRED')
        package.require(row.get('SITE_USE_CODE') in ('BILL_TO', 'SHIP_TO'), 'REST_IDENTITY_PURPOSE_REQUIRED')
    return rows


def visible_rows(document):
    package.require(isinstance(document, dict) and isinstance(document.get('items'), list), 'REST_IDENTITY_COLLECTION_REQUIRED')
    package.require(document.get('hasMore') is False, 'REST_IDENTITY_SCOPE_INCOMPLETE')
    package.require(all(isinstance(row, dict) for row in document['items']), 'REST_IDENTITY_RECORD_REQUIRED')
    return document['items']


def identity(value):
    package.require(type(value) in (str, int) and bool(re.fullmatch(r'[0-9]+', str(value)))
                    and int(value) > 0, 'REST_IDENTITY_ID_REQUIRED')
    return str(value)


def assess(row, parties, address, sites):
    records = visible_rows(parties)
    package.require(len(records) == 1, 'REST_IDENTITY_PARTY_NOT_UNIQUE_OR_NOT_VISIBLE')
    party = records[0]
    party_id = identity(party.get('PartyId'))
    package.require(party.get('PartyNumber') == row['PARTY_NUMBER'], 'REST_IDENTITY_PARTY_NUMBER_MISMATCH')
    package.require(isinstance(address, dict) and address.get('AddressNumber') == row['PARTY_SITE_NUMBER']
                    and identity(address.get('PartyId')) == party_id, 'REST_IDENTITY_ADDRESS_OWNER_MISMATCH')
    location_id = identity(address.get('LocationId'))
    account_sites = visible_rows(sites)
    package.require(bool(account_sites), 'REST_IDENTITY_ACCOUNT_SITE_NOT_VISIBLE')
    for site in account_sites:
        package.require(site.get('AccountNumber') == row['ACCOUNT_NUMBER'] and
                        site.get('PartyNumber') == row['PARTY_NUMBER'], 'REST_IDENTITY_ACCOUNT_OWNER_MISMATCH')
    account_ids = {identity(site.get('CustomerAccountId')) for site in account_sites}
    package.require(len(account_ids) == 1, 'REST_IDENTITY_ACCOUNT_AMBIGUOUS')
    use_ids = [identity(site.get('SiteUseId')) for site in account_sites]
    package.require(len(set(use_ids)) == len(use_ids), 'REST_IDENTITY_DUPLICATE_SITE_USE')
    return {'party_id': party_id, 'location_id': location_id, 'account_id': next(iter(account_ids)),
            'visible_site_use_ids': sorted(use_ids),
            'address_to_account_site_link_proven': False}


def collect(candidate, operation, environment_url, phase, output, client):
    rows = selections(candidate, operation, environment_url)
    package.require(phase in ('before', 'after'), 'API_CAPTURE_PHASE_REQUIRED')
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    report = {'schema_version': 'ar-customer-rest-identity-v1', 'candidate_sha256': hashlib.sha256(candidate).hexdigest(),
              'environment_url': environment_url.rstrip('/'), 'operation': operation, 'phase': phase,
              'started_at': datetime.now(timezone.utc).isoformat(), 'read_only': True,
              'execution_authorized': False, 'persisted_reconciliation_complete': False,
              'full_functional_reconciliation': False, 'remaining_contracts': REMAINING,
              'implementation_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in
                  (Path(__file__), Path(__file__).with_name('customer_api_collect.py'))},
              'captures': [], 'rows': [], 'status': 'READ_INCOMPLETE'}
    def read(path, query):
        dest = output / ('read-'+str(len(report['captures']))+'.json')
        raw = client.rest(path, query, dest)
        package.require(isinstance(raw, bytes) and dest.read_bytes() == raw, 'API_RESPONSE_NOT_RETAINED')
        package.require(len(raw) <= 16*1024*1024, 'API_RESPONSE_SIZE_LIMIT')
        report['captures'].append({'path': path, 'query': query, 'response_file': dest.name,
                                   'response_sha256': hashlib.sha256(raw).hexdigest()})
        return json.loads(raw)
    try:
        for index, row in enumerate(rows, 1):
            parties = read(ORGANIZATIONS, {'finder': 'PartyNumberRF;PartyNumber='+row['PARTY_NUMBER'], 'limit': '2', 'onlyData': 'true'})
            # Resolve the party before addressing a child; stop on absent/ambiguous visibility.
            matched = visible_rows(parties)
            package.require(len(matched) == 1 and matched[0].get('PartyNumber') == row['PARTY_NUMBER'],
                            'REST_IDENTITY_PARTY_NOT_UNIQUE_OR_NOT_VISIBLE')
            identity(matched[0].get('PartyId'))
            address = read(ORGANIZATIONS+'/'+row['PARTY_NUMBER']+'/child/Address/'+row['PARTY_SITE_NUMBER'], {'onlyData': 'true'})
            sites = read(ACCOUNT_SITES, {'finder': 'ReceivablesCustomerAccountSiteFinder;SitePurpose='+row['SITE_USE_CODE']+',AccountNumber='+row['ACCOUNT_NUMBER'], 'limit': '100', 'onlyData': 'true'})
            report['rows'].append({'row': index, **assess(row, parties, address, sites),
                                   'location_values': location_values(row, address, phase)})
        report['status'] = 'PARTIAL_REST_IDENTITIES_MATCH'
        if phase == 'after' and any(not row['location_values']['requested_after_values_match'] for row in report['rows']):
            report['status'] = 'PARTIAL_REST_VALUE_REVIEW_REQUIRED'
    except Exception:
        # No arbitrary response, authentication URL or exception text in diagnostics.
        report['status'] = 'READ_INCOMPLETE'
        raise
    finally:
        report['finished_at'] = datetime.now(timezone.utc).isoformat()
        with (output/'rest-identity-review.json').open('x', encoding='utf-8') as stream:
            json.dump(report, stream, indent=2)
            stream.write('\n')
    return report
