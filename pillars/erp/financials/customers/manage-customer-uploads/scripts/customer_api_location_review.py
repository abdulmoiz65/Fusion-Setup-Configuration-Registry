"""Pure location SOAP value projection; no network, SQL or approval authority."""
from xml.etree import ElementTree as ET

import customers_package as package
from customer_api_hierarchy import SOAP, NIL, identifier, MISSING

LOCATION = 'http://xmlns.oracle.com/apps/cdm/foundation/parties/locationService/'
TYPES = LOCATION+'applicationModule/types/'
FIELDS = {
    **{f'ADDRESS_LINE_{i}': f'Address{i}' for i in range(1,5)},
    **{f'ADDR_ELEMENT_ATTRIBUTE{i}': f'AddrElementAttribute{i}' for i in range(1,6)},
    'FLOOR_NUMBER':'FloorNumber', 'BUILDING':'Building', 'PROVINCE':'Province',
    'COUNTY':'County', 'ADDRESS_LINES_PHONETIC':'AddressLinesPhonetic',
    'POSTAL_PLUS4_CODE':'PostalPlus4Code', 'ADDRESS_DESCRIPTION':'Description',
    'ADDR_SHORT_DESCRIPTION':'ShortDescription', 'SALES_TAX_GEOCODE':'SalesTaxGeocode',
    'SALES_TAX_INSIDE_CITY_LIMITS':'SalesTaxInsideCityLimits', 'HOUSE_TYPE':'HouseType',
    'TIMEZONE_CODE':'TimezoneCode', 'CITY':'City', 'STATE':'State',
    'POSTAL_CODE':'PostalCode', 'COUNTRY':'Country',
}


def review(row, location_id, content):
    require = package.require
    require(isinstance(row, dict) and set(FIELDS) <= set(row) and
            all(isinstance(row[k], str) for k in FIELDS), 'API_LOCATION_ROW_REQUIRED')
    require(identifier(location_id) is not MISSING, 'API_LOCATION_ID_REQUIRED')
    require(isinstance(content, bytes) and len(content) <= 16*1024*1024 and
            b'<!DOCTYPE' not in content.upper() and b'<!ENTITY' not in content.upper(),
            'API_LOCATION_XML_CONTRACT')
    try:
        root = ET.fromstring(content)
    except ET.ParseError as exc:
        raise package.InvalidInput('API_LOCATION_INVALID_XML') from exc
    require(root.tag == '{'+SOAP+'}Envelope', 'API_LOCATION_ENVELOPE')
    bodies = root.findall('{'+SOAP+'}Body')
    require(len(bodies) == 1 and len(bodies[0]) == 1 and bodies[0][0].tag ==
            '{'+TYPES+'}getLocationResponse', 'API_LOCATION_OPERATION')
    results = bodies[0][0].findall('{'+TYPES+'}result')
    require(len(results) == 1 and results[0].get(NIL) not in ('true','1'), 'API_LOCATION_RESULT')
    result = results[0]
    def scalar(name):
        nodes = result.findall('{'+LOCATION+'}'+name)
        require(len(nodes) <= 1, 'API_LOCATION_DUPLICATE_FIELD')
        if not nodes:
            return MISSING
        node = nodes[0]
        require(not len(node), 'API_LOCATION_NONSCALAR_FIELD')
        if node.get(NIL) in ('true','1'):
            require(not node.text, 'API_LOCATION_CONTRADICTORY_NIL')
            return None
        return node.text if node.text is not None else ''
    require(identifier(scalar('LocationId')) == str(location_id), 'API_LOCATION_ID_MISMATCH')
    findings, observed = [], {}
    for field, api in FIELDS.items():
        value = scalar(api)
        if value is not MISSING:
            observed[field] = value
        findings.append({'field': field, 'status':
            'VALUE_NOT_RETURNED' if value is MISSING else
            'OMITTED_INPUT_OBSERVED_NOT_EFFECT_VERIFIED' if not row[field] else
            'MATCH' if value == row[field] else 'MISMATCH'})
    return {'schema_version':'ar-customer-api-location-review-v1',
            'status':'SELECTED_LOCATION_VALUES_MATCH' if all(f['status'] in
                ('MATCH','OMITTED_INPUT_OBSERVED_NOT_EFFECT_VERIFIED') for f in findings)
                else 'LOCATION_VALUE_REVIEW_REQUIRED',
            'findings':findings, 'observed_values':observed,
            'execution_authorized':False, 'persisted_reconciliation_complete':False,
            'limits':['All mapped location fields are projected, including explicit nulls.',
                'An omitted input is not an expected null or verified default/preservation effect.',
                'No before-state, history, origin-of-change or complete customer reconciliation is inferred.',
                'MAIL_STOP is a party-site field, not a location field.']}
