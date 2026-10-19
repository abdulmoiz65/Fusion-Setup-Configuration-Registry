"""Customer-only SOAP XML contract. Pure functions; no auth, transport or imports from core."""
import hashlib
import re
from xml.etree import ElementTree as ET

SOAP = 'http://schemas.xmlsoap.org/soap/envelope/'
ACCOUNT = 'http://xmlns.oracle.com/apps/cdm/foundation/parties/customerAccountService/'
PROFILE = 'http://xmlns.oracle.com/apps/financials/receivables/customers/customerProfileService/'
SOURCE = 'http://xmlns.oracle.com/apps/cdm/foundation/parties/sourceSystemService/'
LOCATION = 'http://xmlns.oracle.com/apps/cdm/foundation/parties/locationService/'
ORGANIZATION = 'http://xmlns.oracle.com/apps/cdm/foundation/parties/organizationService/'
PARTY = 'http://xmlns.oracle.com/apps/cdm/foundation/parties/partyService/'
ORGANIZATION_READS = ('organization-by-number', 'organization-by-site-number')
OPERATIONS = {
    **{op: ('/crmService/FoundationPartiesOrganizationService', 'findOrganization',
            ORGANIZATION+'applicationModule/types/', ORGANIZATION+'applicationModule/findOrganization')
       for op in ORGANIZATION_READS},
    'customer-account-by-number': ('/crmService/CustomerAccountService', 'findCustomerAccount',
                         ACCOUNT+'applicationModule/types/', ACCOUNT+'applicationModule/findCustomerAccount'),
    'location': ('/crmService/FoundationPartiesLocationService', 'getLocation',
                 LOCATION+'applicationModule/types/', LOCATION+'applicationModule/getLocation'),
    'customer-account': ('/crmService/CustomerAccountService', 'getCustomerAccount',
                         ACCOUNT+'applicationModule/types/', ACCOUNT+'applicationModule/getCustomerAccount'),
    'active-customer-profile': ('/fscmService/ReceivablesCustomerProfileService', 'getActiveCustomerProfile',
                               PROFILE+'types/', PROFILE+'getActiveCustomerProfile'),
    'source-system-by-name': ('/crmService/FoundationSourceSystemService', 'findSourceSystem',
                              SOURCE+'applicationModule/types/', SOURCE+'applicationModule/findSourceSystem'),
}


class ReadContractError(ValueError):
    """A safe, fixed diagnostic code from the read contract."""


def xml_text(value):
    return isinstance(value, str) and all(ord(c) in (9, 10, 13) or 32 <= ord(c) <= 0xD7FF
        or 0xE000 <= ord(c) <= 0xFFFD or 0x10000 <= ord(c) <= 0x10FFFF for c in value)


def build_request(operation, account_id=None, account_number=None, *, source_name=None, location_id=None,
                  party_number=None, site_number=None):
    if operation not in OPERATIONS:
        raise ReadContractError('UNSUPPORTED_READ_OPERATION')
    if operation in ORGANIZATION_READS:
        site_search = operation == 'organization-by-site-number'
        number = site_number if site_search else party_number
        if any(v is not None for v in (account_id, account_number, source_name, location_id,
                                       party_number if site_search else site_number)):
            raise ReadContractError('UNRELATED_ORGANIZATION_SELECTORS')
        if not xml_text(number) or not number.strip() or len(number) > 30:
            raise ReadContractError('ORGANIZATION_NUMBER_REQUIRED')
        path, name, namespace, action = OPERATIONS[operation]
        envelope = ET.Element('{'+SOAP+'}Envelope')
        request = ET.SubElement(ET.SubElement(envelope, '{'+SOAP+'}Body'), '{'+namespace+'}'+name)
        adf = 'http://xmlns.oracle.com/adf/svc/types/'
        def sub(parent, field, text=None):
            node = ET.SubElement(parent, '{'+adf+'}'+field)
            node.text = text
            return node
        criteria = ET.SubElement(request, '{'+namespace+'}findCriteria')
        sub(criteria, 'fetchStart', '0')
        sub(criteria, 'fetchSize', '2')
        group = sub(sub(criteria, 'filter'), 'group')
        sub(group, 'upperCaseCompare', 'false')
        item = sub(group, 'item')
        sub(item, 'upperCaseCompare', 'false')
        if site_search:
            sub(item, 'attribute', 'PartySite')
            sub(item, 'operator', 'EXISTS')
            group = sub(sub(item, 'nested'), 'group')
            sub(group, 'upperCaseCompare', 'false')
            item = sub(group, 'item')
            sub(item, 'upperCaseCompare', 'false')
        sub(item, 'attribute', 'PartySiteNumber' if site_search else 'PartyNumber')
        sub(item, 'operator', '=')
        sub(item, 'value', number)
        for field in ('PartyId', 'PartyNumber', 'PartyType', 'Status', 'PartySite',
                      'PartyName', 'DUNSNumberC', 'JgzzFiscalCode', 'GSAIndicatorFlag', 'CreationDate'):
            sub(criteria, 'findAttribute', field)
        sub(criteria, 'excludeAttribute', 'false')
        control = ET.SubElement(request, '{'+namespace+'}findControl')
        sub(control, 'retrieveAllTranslations', 'false')
        return path, action, ET.tostring(envelope, encoding='utf-8', xml_declaration=True)
    if party_number is not None or site_number is not None:
        raise ReadContractError('ORGANIZATION_SELECTORS_NOT_APPLICABLE')
    if operation == 'customer-account-by-number':
        if account_id is not None or source_name is not None or location_id is not None:
            raise ReadContractError('UNRELATED_ACCOUNT_NUMBER_SELECTORS')
        if not xml_text(account_number) or not account_number.strip() or len(account_number) > 30:
            raise ReadContractError('ACCOUNT_NUMBER_REQUIRED')
        path, name, namespace, action = OPERATIONS[operation]
        envelope = ET.Element('{'+SOAP+'}Envelope')
        request = ET.SubElement(ET.SubElement(envelope, '{'+SOAP+'}Body'), '{'+namespace+'}'+name)
        adf = 'http://xmlns.oracle.com/adf/svc/types/'
        criteria = ET.SubElement(request, '{'+namespace+'}findCriteria')
        ET.SubElement(criteria, '{'+adf+'}fetchStart').text = '0'
        # Two visible matches establish ambiguity. A saturated result is never complete.
        ET.SubElement(criteria, '{'+adf+'}fetchSize').text = '2'
        group = ET.SubElement(ET.SubElement(criteria, '{'+adf+'}filter'), '{'+adf+'}group')
        ET.SubElement(group, '{'+adf+'}upperCaseCompare').text = 'false'
        item = ET.SubElement(group, '{'+adf+'}item')
        ET.SubElement(item, '{'+adf+'}upperCaseCompare').text = 'false'
        ET.SubElement(item, '{'+adf+'}attribute').text = 'AccountNumber'
        ET.SubElement(item, '{'+adf+'}operator').text = '='
        ET.SubElement(item, '{'+adf+'}value').text = account_number
        for field in ('CustomerAccountId', 'AccountNumber', 'PartyId', 'Status'):
            ET.SubElement(criteria, '{'+adf+'}findAttribute').text = field
        ET.SubElement(criteria, '{'+adf+'}excludeAttribute').text = 'false'
        control = ET.SubElement(request, '{'+namespace+'}findControl')
        ET.SubElement(control, '{'+adf+'}retrieveAllTranslations').text = 'false'
        return path, action, ET.tostring(envelope, encoding='utf-8', xml_declaration=True)
    if operation == 'location':
        if account_id is not None or account_number is not None or source_name is not None:
            raise ReadContractError('UNRELATED_LOCATION_SELECTORS')
        if not isinstance(location_id, str) or re.fullmatch(r'[1-9][0-9]{0,17}', location_id) is None:
            raise ReadContractError('POSITIVE_LOCATION_ID_REQUIRED')
        path, name, namespace, action = OPERATIONS[operation]
        envelope = ET.Element('{'+SOAP+'}Envelope')
        request = ET.SubElement(ET.SubElement(envelope, '{'+SOAP+'}Body'), '{'+namespace+'}'+name)
        ET.SubElement(request, '{'+namespace+'}locationId').text = location_id
        return path, action, ET.tostring(envelope, encoding='utf-8', xml_declaration=True)
    if location_id is not None:
        raise ReadContractError('LOCATION_ID_NOT_APPLICABLE')
    if operation == 'source-system-by-name':
        if account_id is not None or account_number is not None:
            raise ReadContractError('ACCOUNT_SELECTORS_NOT_APPLICABLE')
        if not xml_text(source_name) or not source_name.strip() or len(source_name) > 80:
            raise ReadContractError('SOURCE_SYSTEM_NAME_REQUIRED')
        path, name, namespace, action = OPERATIONS[operation]
        envelope = ET.Element('{'+SOAP+'}Envelope')
        body = ET.SubElement(envelope, '{'+SOAP+'}Body')
        request = ET.SubElement(body, '{'+namespace+'}'+name)
        criteria = ET.SubElement(request, '{'+namespace+'}findCriteria')
        adf = 'http://xmlns.oracle.com/adf/svc/types/'
        ET.SubElement(criteria, '{'+adf+'}fetchStart').text = '0'
        # Three results suffice to reject ambiguity; this is not a general search.
        ET.SubElement(criteria, '{'+adf+'}fetchSize').text = '3'
        group = ET.SubElement(ET.SubElement(criteria, '{'+adf+'}filter'), '{'+adf+'}group')
        item = ET.SubElement(group, '{'+adf+'}item')
        ET.SubElement(item, '{'+adf+'}attribute').text = 'OrigSystemName'
        ET.SubElement(item, '{'+adf+'}operator').text = '='
        ET.SubElement(item, '{'+adf+'}value').text = source_name
        return path, action, ET.tostring(envelope, encoding='utf-8', xml_declaration=True)
    if source_name is not None:
        raise ReadContractError('SOURCE_NAME_NOT_APPLICABLE')
    if not isinstance(account_id, str) or re.fullmatch(r'[1-9][0-9]{0,17}', account_id) is None:
        raise ReadContractError('POSITIVE_ACCOUNT_ID_REQUIRED')
    if operation == 'active-customer-profile':
        if not isinstance(account_number, str) or not account_number.strip() or len(account_number) > 30:
            raise ReadContractError('PROFILE_ACCOUNT_NUMBER_REQUIRED')
        if not xml_text(account_number):
            raise ReadContractError('INVALID_XML_CHARACTER')
    elif account_number is not None:
        raise ReadContractError('ACCOUNT_NUMBER_NOT_APPLICABLE')
    path, name, namespace, action = OPERATIONS[operation]
    envelope = ET.Element('{'+SOAP+'}Envelope')
    body = ET.SubElement(envelope, '{'+SOAP+'}Body')
    request = ET.SubElement(body, '{'+namespace+'}'+name)
    if operation == 'customer-account':
        ET.SubElement(request, '{'+namespace+'}customerAccountId').text = account_id
    else:
        profile = ET.SubElement(request, '{'+namespace+'}customerProfile')
        ET.SubElement(profile, '{'+PROFILE+'}CustomerAccountId').text = account_id
        ET.SubElement(profile, '{'+PROFILE+'}AccountNumber').text = account_number
    return path, action, ET.tostring(envelope, encoding='utf-8', xml_declaration=True)


def inspect_response(content, operation, account_id=None, account_number=None, *, source_name=None, location_id=None,
                     party_number=None, site_number=None):
    """Validate operation and identity only; do not declare complete reconciliation."""
    if operation not in OPERATIONS:
        raise ReadContractError('UNSUPPORTED_READ_OPERATION')
    if not isinstance(content, bytes) or len(content) > 16 * 1024 * 1024:
        raise ReadContractError('RESPONSE_INSPECTION_LIMIT')
    if b'\x00' in content or b'<!DOCTYPE' in content.upper() or b'<!ENTITY' in content.upper():
        raise ReadContractError('XML_DECLARATIONS_UNSUPPORTED')
    try:
        root = ET.fromstring(content)
    except ET.ParseError as exc:
        raise ReadContractError('INVALID_XML_RESPONSE') from exc
    if root.tag != '{'+SOAP+'}Envelope':
        raise ReadContractError('UNEXPECTED_RESPONSE_ENVELOPE')
    bodies = root.findall('{'+SOAP+'}Body')
    if len(bodies) != 1 or len(bodies[0]) != 1:
        raise ReadContractError('UNEXPECTED_RESPONSE_BODY')
    body = bodies[0]
    if body[0].tag == '{'+SOAP+'}Fault':
        raise ReadContractError('SOAP_FAULT')
    _, name, namespace, _ = OPERATIONS[operation]
    if body[0].tag != '{'+namespace+'}'+name+'Response':
        raise ReadContractError('UNEXPECTED_RESPONSE_OPERATION')
    results = body[0].findall('{'+namespace+'}result')
    # ADF result elements use the operation types namespace on the wire.
    if len(results) != 1:
        raise ReadContractError('MISSING_OR_AMBIGUOUS_RESULT')
    result = results[0]
    if result.get('{http://www.w3.org/2001/XMLSchema-instance}nil') in ('true', '1'):
        raise ReadContractError('NIL_OPERATION_RESULT')
    if operation in ORGANIZATION_READS:
        build_request(operation, account_id, account_number, source_name=source_name,
                      location_id=location_id, party_number=party_number, site_number=site_number)
        values = result.findall('{'+ORGANIZATION+'}Value')
        if len(values) != len(result) or len(values) > 2:
            raise ReadContractError('UNEXPECTED_ORGANIZATION_SEARCH_RESULT')
        def fields(node, namespace, names, ids):
            if node.get('{http://www.w3.org/2001/XMLSchema-instance}nil') in ('true', '1'):
                raise ReadContractError('NIL_ORGANIZATION_SEARCH_VALUE')
            found = {}
            for field in names:
                nodes = node.findall('{'+namespace+'}'+field)
                if len(nodes) != 1 or len(nodes[0]) or not nodes[0].text or nodes[0].get(
                        '{http://www.w3.org/2001/XMLSchema-instance}nil') in ('true', '1'):
                    raise ReadContractError('ORGANIZATION_SEARCH_FIELD_MISSING_OR_AMBIGUOUS')
                found[field] = nodes[0].text
            if any(re.fullmatch(r'[1-9][0-9]{0,17}', found[key]) is None for key in ids):
                raise ReadContractError('ORGANIZATION_SEARCH_INVALID_ID')
            return found
        records, seen_parties, seen_sites = [], set(), set()
        for value in values:
            record = fields(value, ORGANIZATION, ('PartyId', 'PartyNumber', 'PartyType', 'Status'), ('PartyId',))
            if record['PartyType'] != 'ORGANIZATION' or record['PartyId'] in seen_parties:
                raise ReadContractError('ORGANIZATION_SEARCH_TYPE_OR_DUPLICATE_ID')
            if party_number is not None and record['PartyNumber'] != party_number:
                raise ReadContractError('ORGANIZATION_SEARCH_NUMBER_MISMATCH')
            seen_parties.add(record['PartyId'])
            sites = []
            for node in value.findall('{'+ORGANIZATION+'}PartySite'):
                site = fields(node, PARTY, ('PartySiteId', 'PartySiteNumber', 'PartyId', 'LocationId', 'Status'),
                              ('PartySiteId', 'PartyId', 'LocationId'))
                if site['PartyId'] != record['PartyId'] or site['PartySiteId'] in seen_sites:
                    raise ReadContractError('ORGANIZATION_SITE_PARENT_OR_DUPLICATE_ID')
                seen_sites.add(site['PartySiteId'])
                sites.append(site)
            matching = [site for site in sites if site['PartySiteNumber'] == site_number]
            if site_number is not None and not matching:
                raise ReadContractError('ORGANIZATION_SITE_NUMBER_NOT_RETURNED')
            # Preserve every returned child, including nonmatching siblings and inactive sites.
            record['sites'] = sites
            record['matching_sites'] = matching
            records.append(record)
        return {'status': 'SCOPED_NUMBER_SEARCH_RESPONSE', 'operation': name,
                'response_sha256': hashlib.sha256(content).hexdigest(), 'records': records,
                'selector': 'site_number' if site_number is not None else 'party_number',
                'visible_result_complete': len(records) < 2, 'result_limit': 2,
                'scope': 'VISIBLE_ORGANIZATIONS_ONLY', 'nested_site_inventory_complete': False,
                'global_absence_proven': False, 'persisted_reconciliation_complete': False}
    if operation == 'customer-account-by-number':
        build_request(operation, account_id, account_number, source_name=source_name, location_id=location_id)
        values = result.findall('{'+ACCOUNT+'}Value')
        if len(values) != len(result) or len(values) > 2:
            raise ReadContractError('UNEXPECTED_ACCOUNT_SEARCH_RESULT')
        records, seen = [], set()
        for value in values:
            fields = {}
            if value.get('{http://www.w3.org/2001/XMLSchema-instance}nil') in ('true', '1'):
                raise ReadContractError('NIL_ACCOUNT_SEARCH_VALUE')
            for field in ('CustomerAccountId', 'AccountNumber', 'PartyId', 'Status'):
                nodes = value.findall('{'+ACCOUNT+'}'+field)
                if len(nodes) != 1 or len(nodes[0]) or nodes[0].get('{http://www.w3.org/2001/XMLSchema-instance}nil') in ('true', '1') or nodes[0].text is None:
                    raise ReadContractError('ACCOUNT_SEARCH_FIELD_MISSING_OR_AMBIGUOUS')
                fields[field] = nodes[0].text
            if fields['AccountNumber'] != account_number:
                raise ReadContractError('ACCOUNT_SEARCH_NUMBER_MISMATCH')
            if any(re.fullmatch(r'[1-9][0-9]{0,17}', fields[key]) is None for key in ('CustomerAccountId', 'PartyId')) or fields['CustomerAccountId'] in seen:
                raise ReadContractError('ACCOUNT_SEARCH_INVALID_OR_DUPLICATE_ID')
            seen.add(fields['CustomerAccountId'])
            records.append(fields)
        return {'status': 'SCOPED_NUMBER_SEARCH_RESPONSE', 'operation': name,
                'response_sha256': hashlib.sha256(content).hexdigest(), 'records': records,
                'visible_result_complete': len(records) < 2, 'result_limit': 2,
                'global_absence_proven': False, 'persisted_reconciliation_complete': False}
    if operation == 'location':
        ids = result.findall('{'+LOCATION+'}LocationId')
        if not isinstance(location_id, str) or re.fullmatch(r'[1-9][0-9]{0,17}', location_id) is None or len(ids) != 1 or ids[0].text != location_id or ids[0].get('{http://www.w3.org/2001/XMLSchema-instance}nil') in ('true','1'):
            raise ReadContractError('RESPONSE_LOCATION_ID_MISMATCH')
        return {'status': 'SCOPED_READ_RESPONSE', 'operation': name,
                'location_id': location_id, 'response_sha256': hashlib.sha256(content).hexdigest(),
                'persisted_reconciliation_complete': False}
    if operation == 'source-system-by-name':
        if not xml_text(source_name) or not source_name.strip():
            raise ReadContractError('SOURCE_SYSTEM_NAME_REQUIRED')
        values = result.findall('{'+SOURCE+'}Value')
        if len(values) != 1 or len(result) != 1:
            raise ReadContractError('MISSING_OR_AMBIGUOUS_SOURCE_SYSTEM')
        selected = values[0]
        if selected.get('{http://www.w3.org/2001/XMLSchema-instance}nil') in ('true','1'):
            raise ReadContractError('NIL_SOURCE_SYSTEM_RESULT')
        fields = {}
        for field in ('OrigSystemId', 'OrigSystemName', 'OrigSystem', 'StatusFlag', 'EnableForTcaFlag'):
            elements = selected.findall('{'+SOURCE+'}'+field)
            if len(elements) != 1 or elements[0].get('{http://www.w3.org/2001/XMLSchema-instance}nil') in ('true','1') or not elements[0].text:
                raise ReadContractError('SOURCE_SYSTEM_FIELD_MISSING_OR_AMBIGUOUS')
            fields[field] = elements[0].text
        if fields['OrigSystemName'] != source_name or re.fullmatch(r'[1-9][0-9]*', fields['OrigSystemId']) is None:
            raise ReadContractError('SOURCE_SYSTEM_IDENTITY_MISMATCH')
        if fields['StatusFlag'] not in ('true','1') or fields['EnableForTcaFlag'] not in ('true','1'):
            raise ReadContractError('SOURCE_SYSTEM_NOT_ACTIVE_TCA_ENABLED')
        return {'status':'SCOPED_READ_RESPONSE','operation':name,'source_system_name':source_name,
                'source_system_code':fields['OrigSystem'],'source_system_id':fields['OrigSystemId'],
                'response_sha256':hashlib.sha256(content).hexdigest(),
                'effective_date_eligibility_verified':False,'persisted_reconciliation_complete':False}
    values_ns = ACCOUNT
    if operation == 'active-customer-profile':
        values = result.findall('{'+PROFILE+'}Value')
        if len(values) != 1:
            raise ReadContractError('MISSING_OR_AMBIGUOUS_PROFILE')
        result = values[0]
        if result.get('{http://www.w3.org/2001/XMLSchema-instance}nil') in ('true','1'):
            raise ReadContractError('NIL_PROFILE_RESULT')
        values_ns = PROFILE
    ids = result.findall('{'+values_ns+'}CustomerAccountId')
    if len(ids) != 1 or ids[0].text != account_id or ids[0].get('{http://www.w3.org/2001/XMLSchema-instance}nil') in ('true','1'):
        raise ReadContractError('RESPONSE_ACCOUNT_ID_MISMATCH')
    if operation == 'active-customer-profile':
        numbers = result.findall('{'+values_ns+'}AccountNumber')
        if len(numbers) != 1 or numbers[0].text != account_number or numbers[0].get('{http://www.w3.org/2001/XMLSchema-instance}nil') in ('true','1'):
            raise ReadContractError('RESPONSE_ACCOUNT_NUMBER_MISMATCH')
    return {'status': 'SCOPED_READ_RESPONSE', 'operation': name,
            'account_id': account_id, 'response_sha256': hashlib.sha256(content).hexdigest(),
            'persisted_reconciliation_complete': False}
