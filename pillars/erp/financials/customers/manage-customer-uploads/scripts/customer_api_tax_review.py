"""Pure scoped tax-profile REST comparison; never certifies asynchronous effects."""
import customers_package as package
from customer_api_hierarchy import collection, identifier, MISSING

FIELDS = ('PartyTaxProfileId', 'PartyId', 'PartyTypeCode', 'RepresentativeRegistrationNumber',
          'CustomerFlag', 'SiteFlag', 'SupplierFlag')


def review(row, party_id, pages):
    require = package.require
    require(isinstance(row, dict) and isinstance(row.get('TAXPAYER_REGISTRATION_NUM'), str),
            'API_TAX_INPUT_REQUIRED')
    party_id = identifier(party_id)
    require(party_id is not MISSING, 'API_TAX_PARTY_ID_REQUIRED')
    records, complete = collection(pages)
    seen, missing = set(), False
    for record in records:
        key = identifier(record.get('PartyTaxProfileId'))
        require(key is not MISSING and key not in seen, 'API_TAX_DUPLICATE_OR_INVALID_ID')
        seen.add(key)
        require(identifier(record.get('PartyId')) == party_id, 'API_TAX_PARTY_SCOPE')
        missing = missing or not set(FIELDS) <= set(record)
        require(isinstance(record.get('PartyTypeCode'), str) and record['PartyTypeCode'], 'API_TAX_PARTY_TYPE')
        if 'RepresentativeRegistrationNumber' in record:
            value = record['RepresentativeRegistrationNumber']
            require(value is None or isinstance(value, str), 'API_TAX_VALUE_TYPE')
        for field in ('CustomerFlag', 'SiteFlag', 'SupplierFlag'):
            if field in record:
                require(record[field] is None or type(record[field]) is bool, 'API_TAX_FLAG_TYPE')
    selected = [record for record in records if record['PartyTypeCode'] == 'THIRD_PARTY']
    supplied = row['TAXPAYER_REGISTRATION_NUM']
    status = ('NO_TAX_INPUT_EFFECTS_UNVERIFIED' if not supplied else
              'TAX_API_EVIDENCE_INCOMPLETE' if not complete or missing else
              'TAX_PROFILE_NOT_OBSERVED' if not selected else
              'AMBIGUOUS_TAX_PROFILES' if len(selected) != 1 else
              'SELECTED_TAX_API_VALUE_MATCH' if selected[0]['RepresentativeRegistrationNumber'] == supplied else
              'TAX_API_VALUE_MISMATCH')
    return {'schema_version': 'ar-customer-api-tax-review-v1', 'status': status,
            'pages_complete': complete, 'observed_profile_count': len(records),
            'third_party_profile_count': len(selected), 'other_profile_count': len(records)-len(selected),
            'execution_authorized': False, 'persisted_reconciliation_complete': False,
            'callback_completion_verified': False, 'profile_effects_verified': False,
            'limits': ['Selected exact value only; neither absence nor match proves callback execution.',
                      'All visible party profile types retained; no filter to the expected tax value.',
                      'Caller binds API-resolved party identity, candidate, scope, phase and response captures.',
                      'Before/after effects, batch lineage and asynchronous completion remain separate.']}
