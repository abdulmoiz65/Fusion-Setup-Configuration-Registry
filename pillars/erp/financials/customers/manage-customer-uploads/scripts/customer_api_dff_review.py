"""Project deployed account DFF segments without guessing physical columns."""
from xml.etree import ElementTree as ET
import customers_package as package
from customer_api_hierarchy import ACCOUNT, SOAP, TYPES, NIL, MISSING, identifier

FLEX = 'http://xmlns.oracle.com/apps/cdm/foundation/parties/flex/custAccount/'
LOCATOR = FLEX+'CustAcctInformation'
RESOURCE = '/fscmRestApi/applcoreApi/latest/flexfields/runtime/x/describe'
FIELDS = ['ATTRIBUTE_CATEGORY'] + [f'ATTRIBUTE{i}' for i in range(1,31)]

def scalar(parent, namespace, name):
    elements = parent.findall('{'+namespace+'}'+name)
    package.require(len(elements) <= 1, 'API_DFF_DUPLICATE_FIELD')
    if not elements: return MISSING
    element = elements[0]
    package.require(not len(element), 'API_DFF_NONSCALAR_VALUE')
    if element.get(NIL) in ('true', '1'):
        package.require(not element.text, 'API_DFF_CONTRADICTORY_NIL')
        return None
    return element.text if element.text is not None else ''

def account_dff(account_id, content):
    require = package.require
    require(identifier(account_id) is not MISSING, 'API_DFF_ACCOUNT_ID_REQUIRED')
    require(isinstance(content, bytes) and len(content) <= 16*1024*1024 and
            b'<!DOCTYPE' not in content.upper() and b'<!ENTITY' not in content.upper(), 'API_DFF_XML_CONTRACT')
    try: root = ET.fromstring(content)
    except ET.ParseError as exc: raise package.InvalidInput('API_DFF_INVALID_XML') from exc
    bodies = root.findall('{'+SOAP+'}Body')
    require(root.tag == '{'+SOAP+'}Envelope' and len(bodies) == 1 and len(bodies[0]) == 1 and
            bodies[0][0].tag == '{'+TYPES+'}getCustomerAccountResponse', 'API_DFF_OPERATION')
    results = bodies[0][0].findall('{'+TYPES+'}result')
    require(len(results) == 1 and results[0].get(NIL) not in ('true','1'), 'API_DFF_ACCOUNT_RESULT')
    require(identifier(scalar(results[0], ACCOUNT, 'CustomerAccountId')) == str(account_id), 'API_DFF_ACCOUNT_MISMATCH')
    children = results[0].findall('{'+ACCOUNT+'}CustAcctInformation')
    require(len(children) <= 1, 'API_DFF_AMBIGUOUS_CONTAINER')
    if not children or children[0].get(NIL) in ('true','1'): return None, MISSING
    child = children[0]
    require(identifier(scalar(child, FLEX, 'CustAccountId')) == str(account_id), 'API_DFF_PARENT_MISMATCH')
    return child, scalar(child, FLEX, '__FLEX_Context')

def metadata_contract(metadata, context):
    require = package.require
    require(isinstance(metadata, dict) and metadata.get('baseLocator') == LOCATOR and
            metadata.get('flexfieldCode') == 'HZ_CUST_ACCOUNTS' and metadata.get('flexfieldType') == 'DFF' and
            type(metadata.get('applicationId')) is int and metadata['applicationId'] > 0,
            'API_DFF_METADATA_IDENTITY')
    require('discriminatorValue' in metadata and metadata['discriminatorValue'] == context, 'API_DFF_METADATA_CONTEXT')
    require(isinstance(metadata.get('revision'), dict) and isinstance(metadata['revision'].get('id'), str) and
            metadata['revision']['id'], 'API_DFF_METADATA_REVISION')
    segments, names = metadata.get('segments'), metadata.get('segmentApiNames')
    require(isinstance(segments, dict) and isinstance(names, list) and all(isinstance(n,str) for n in names) and
            len(set(names)) == len(names) and set(names) == set(segments), 'API_DFF_METADATA_SEGMENTS')
    mapping = {}
    for api, segment in segments.items():
        require(isinstance(segment, dict), 'API_DFF_METADATA_SEGMENT')
        column = segment.get('segmentColumnName')
        if column not in FIELDS: continue  # Numeric/date DFF columns are outside these worksheet fields.
        require(segment.get('javaType') == 'java.lang.String', 'API_DFF_COLUMN_TYPE_UNQUALIFIED')
        require(column not in mapping, 'API_DFF_AMBIGUOUS_PHYSICAL_COLUMN')
        mapping[column] = api
    require(mapping.get('ATTRIBUTE_CATEGORY') == '__FLEX_Context', 'API_DFF_CONTEXT_COLUMN_REQUIRED')
    return mapping

def review_input_limits(row, metadata):
    """Check declared string length only; value-set/business eligibility stays separate."""
    package.require(isinstance(row, dict) and all(isinstance(row.get(k), str) for k in FIELDS), 'API_DFF_ROW_REQUIRED')
    context = row['ATTRIBUTE_CATEGORY'] or None
    mapping = metadata_contract(metadata, context)
    findings = []
    for field in FIELDS:
        if not row[field] or field == 'ATTRIBUTE_CATEGORY':
            continue
        segment = metadata['segments'].get(mapping.get(field), {})
        limit = segment.get('valueFormat', {}).get('maximumLength')
        if field not in mapping:
            status = 'REQUESTED_COLUMN_NOT_EXPOSED'
        elif limit is None:
            status = 'NO_DECLARED_LENGTH_LIMIT'
        else:
            package.require(type(limit) is int and limit > 0, 'API_DFF_LENGTH_METADATA_INVALID')
            status = ('DECLARED_LENGTH_EXCEEDED' if len(row[field]) > limit else
                'WITHIN_DECLARED_LENGTH' if row[field].isascii() else 'NON_ASCII_LENGTH_SEMANTICS_REVIEW_REQUIRED')
        findings.append({'field': field, 'status': status, 'declared_maximum_length': limit})
    return {'schema_version': 'ar-customer-api-dff-input-limits-v1',
        'metadata_sha256': package.fingerprint(metadata), 'input_dff_sha256': package.fingerprint({k: row[k] for k in FIELDS}),
        'findings': findings, 'known_length_violation': any(f['status'] == 'DECLARED_LENGTH_EXCEEDED' for f in findings),
        'requested_mapping_complete': all(f['status'] != 'REQUESTED_COLUMN_NOT_EXPOSED' for f in findings),
        'loader_validation_complete': False, 'execution_authorized': False,
        'limits': ['Non-ASCII values within the code-point bound still require byte/UTF-16 length-semantics review; no truncation or blanket rejection.',
            'No byte-length, value-set membership, requiredness, regular expression or other business eligibility claim.',
            'Known length violations must be corrected; unknown business validation follows the normal named-gap policy.']}


def review(row, account_id, content, base_metadata, context_metadata=None):
    require = package.require
    require(isinstance(row,dict) and all(isinstance(row.get(k),str) for k in FIELDS), 'API_DFF_ROW_REQUIRED')
    child, context = account_dff(account_id, content)
    base = metadata_contract(base_metadata, None)
    if child is None or context is MISSING:
        return {'status':'DFF_VALUES_NOT_RETURNED', 'execution_authorized':False,
                'persisted_reconciliation_complete':False, 'requested_fields_match':False}
    mapping = base
    if context is not None:
        require(isinstance(context,str) and context, 'API_DFF_CONTEXT_VALUE')
        mapping = metadata_contract(context_metadata, context)
        require(base_metadata['revision']['id'] == context_metadata['revision']['id'] and
                base_metadata['applicationId'] == context_metadata['applicationId'] and
                all(mapping.get(column) == api for column,api in base.items()), 'API_DFF_METADATA_CHANGED_OR_BASE_MISSING')
    else:
        require(context_metadata is None, 'API_DFF_UNREQUESTED_CONTEXT_METADATA')
    findings, observed = [], {}
    for field in FIELDS:
        value = scalar(child, FLEX, mapping[field]) if field in mapping else MISSING
        if value is not MISSING: observed[field] = value
        status = ('COLUMN_NOT_EXPOSED_BY_DEPLOYED_METADATA' if field not in mapping else
                  'VALUE_NOT_RETURNED' if value is MISSING else
                  'OMITTED_INPUT_OBSERVED_NOT_EFFECT_VERIFIED' if not row[field] else
                  'MATCH' if value == row[field] else 'MISMATCH')
        findings.append({'field':field, 'status':status, 'requested':bool(row[field])})
    requested_match = all(f['status'] == 'MATCH' for f in findings if f['requested'])
    return {'schema_version':'ar-customer-api-dff-review-v1',
            'status':'SELECTED_DFF_VALUES_MATCH_WITH_COVERAGE_LIMITS' if requested_match else 'DFF_VALUE_REVIEW_REQUIRED',
            'findings':findings, 'observed_values':observed, 'physical_to_api_mapping':mapping,
            'metadata_revision':base_metadata['revision']['id'], 'requested_fields_match':requested_match,
            'unexposed_physical_fields':[field for field in FIELDS if field not in mapping],
            'execution_authorized':False, 'persisted_reconciliation_complete':False,
            'limits':['Undeployed/unexposed columns are unknown, not null; no physical-column naming inference.',
                      'Current deployed metadata is not undeployed design-time configuration.',
                      'No before/after preservation, loader validation or full thirty-column visibility claim.']}
