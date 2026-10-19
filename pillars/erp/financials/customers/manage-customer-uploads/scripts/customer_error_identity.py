"""Associate complete versioned Data Loader message identities with candidate rows.

This is an offline component. The caller must separately establish complete,
authenticated diagnostics for the exact attempt. Absence of a mapped error is
never evidence that a row loaded, and this module never authorizes recovery.
"""
import json
import re

import customers_package as package
import customer_attempt_review as attempts
import customer_registration_review as registration

PREFIX = 'FSCR_ROW_V1='
FIELDS = ('ORIG_SOURCE_SYSTEM_NAME', 'PARTY_ORIG_SYSTEM_REFERENCE',
          'CUST_ORIG_SYSTEM_REFERENCE', 'CUST_SITE_ORIG_SYS_REF',
          'LOCATION_ORIG_SYSTEM_REFERENCE', 'CUST_SITEUSE_ORIG_SYS_REF', 'SITE_USE_CODE')
FALLBACKS = {'PARTY_ORIG_SYSTEM_REFERENCE': 'PARTY_NUMBER',
             'CUST_ORIG_SYSTEM_REFERENCE': 'ACCOUNT_NUMBER',
             'CUST_SITE_ORIG_SYS_REF': 'PARTY_SITE_NUMBER'}


def _unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError('duplicate identity key')
        value[key] = item
    return value


def decode(message):
    """Return a complete identity only; legacy, omitted or malformed is unknown."""
    if not isinstance(message, str) or not message.startswith(PREFIX):
        return None, 'NO_VERSIONED_IDENTITY'
    try:
        decoder = json.JSONDecoder(object_pairs_hook=_unique_object)
        identity, end = decoder.raw_decode(message[len(PREFIX):])
    except (ValueError, TypeError, RecursionError):
        return None, 'MALFORMED_IDENTITY'
    if not isinstance(identity, dict):
        return None, 'IDENTITY_SCHEMA'
    if not isinstance(identity.get('uploadId'), str) or not re.fullmatch(r'[1-9][0-9]*', identity['uploadId']):
        return None, 'UPLOAD_ID_INVALID'
    tail = message[len(PREFIX)+end:]
    if not tail.startswith(' ') or not tail.strip():
        return None, 'DIAGNOSTIC_MISSING'
    if 'identityOmitted' in identity:
        return None, 'IDENTITY_EXPLICITLY_OMITTED'
    if set(identity) != {'uploadId', *FIELDS} or any(
            identity[key] is not None and not isinstance(identity[key], str) for key in FIELDS):
        return None, 'IDENTITY_SCHEMA'
    try:
        encoded = message[len(PREFIX):len(PREFIX)+end].encode('utf-8')
        for field in FIELDS:
            if identity[field] is not None:
                identity[field].encode('utf-8')
    except UnicodeEncodeError:
        return None, 'MALFORMED_IDENTITY'
    if len(encoded) > 600:
        return None, 'IDENTITY_EXCEEDS_REVIEWED_BUDGET'
    return identity, 'COMPLETE_IDENTITY'


def associate_messages(candidate, operation, messages):
    """Map errors, preserving ambiguous duplicate rows and unknown diagnostics."""
    inspected = package.inspect_candidate(candidate, operation)
    package.require(isinstance(messages, list) and all(isinstance(x, str) for x in messages),
                    'ERROR_IDENTITY_MESSAGES_REQUIRED')
    rows = [dict(zip(package.columns(), row)) for row in package.inspect_zip(candidate)]
    keys = []
    for row in rows:
        keys.append(tuple((row.get(field) or row.get(FALLBACKS.get(field, '')) or None)
                          for field in FIELDS))
    findings = []
    upload_to_rows = {}
    for index, message in enumerate(messages, 1):
        identity, status = decode(message)
        matches = []
        if identity:
            key = tuple(identity[field] for field in FIELDS)
            matches = [i for i, value in enumerate(keys, 1) if value == key]
            status = ('NO_CANDIDATE_MATCH' if not matches else
                      'AMBIGUOUS_CANDIDATE_ROWS' if len(matches) > 1 else 'EXACT_CANDIDATE_ROW')
            previous = upload_to_rows.setdefault(identity['uploadId'], set())
            previous.update(matches)
        findings.append({'message_index': index, 'status': status, 'candidate_rows': matches,
                         'upload_id': identity['uploadId'] if identity else None})
    conflicting = {upload for upload, matched in upload_to_rows.items() if len(matched) > 1}
    for finding in findings:
        if finding['upload_id'] in conflicting and finding['status'] == 'EXACT_CANDIDATE_ROW':
            finding['status'] = 'CONFLICTING_UPLOAD_ID'
    return {'schema_version': 'ar-customer-error-identity-review-v1',
            'candidate_sha256': inspected['candidate_sha256'],
            'messages_sha256': package.fingerprint(messages), 'findings': findings,
            'all_messages_uniquely_associated': bool(findings) and all(
                x['status'] == 'EXACT_CANDIDATE_ROW' for x in findings),
            'rows_with_associated_errors': sorted({row for x in findings
                if x['status'] == 'EXACT_CANDIDATE_ROW' for row in x['candidate_rows']}),
            'attempt_association_verified': False, 'diagnostic_collection_complete_verified': False,
            'successful_rows_verified': False, 'recovery_authorized': False}


def associate_attempt(candidate, operation, environment, binding, observation, registered_record):
    """Compose request, reviewed recipe, complete errors and balanced row counts.

    Successful row classification is a constrained partition, not an inference
    from missing messages alone. Persisted values and recovery remain separate.
    """
    attempt = attempts.analyze(candidate, operation, environment, binding, observation)
    package.require(attempt['request_association_matches'], 'ERROR_ATTEMPT_ASSOCIATION')
    contract = package.load_json(registration.CONTRACT)
    package.require(isinstance(registered_record, dict), 'ERROR_REGISTRATION_RECORD')
    config = registration.parse_config(registered_record.get('LOAD_ADAPTER_CONFIG'))
    package.require(package.fingerprint(config) == package.fingerprint(contract['adapter_config'])
        and all(registered_record.get(k) == v for k,v in contract['registration_fields'].items()),
        'ERROR_REGISTRATION_RECIPE')
    normalized = {**registered_record, 'LOAD_ADAPTER_CONFIG': config}
    package.require(package.fingerprint(normalized) == binding['registration_sha256'], 'ERROR_REGISTRATION_BINDING')
    core = observation['core_status']
    dataset = core['dataSets'][0]
    diagnostic = core['fbdiDiagnostics'][0]
    bo = diagnostic['businessObjects'][0]
    record = bo['record']
    errors = bo.get('errors')
    package.require(bo.get('errorsComplete') is True and isinstance(errors,list)
        and all(isinstance(e,dict) and e.get('BusinessObject') == 'customers'
            and e.get('MessageTypeCode') == 'ERROR' and e.get('OriginatingProcessCode') == 'LOAD'
            and isinstance(e.get('MessageText'),str) for e in errors), 'ERROR_COLLECTION_INCOMPLETE')
    mapped = associate_messages(candidate,operation,[e['MessageText'] for e in errors])
    row_count = len(package.inspect_zip(candidate))
    findings = []
    def count(container,key):
        value = container.get(key)
        if type(value) is int and value >= 0: return value
        if isinstance(value,str) and re.fullmatch(r'0|[1-9][0-9]*',value): return int(value)
        findings.append('COUNT_MISSING_OR_INVALID:'+key)
        return None
    failed = count(record,'ObjectLoadErrorCount')
    loaded = count(record,'ObjectSuccessCount')
    expected_counts = [(record,'ObjectTotalCount',row_count),(record,'FileLineTotalCount',row_count),
        (record,'FileLineImportErrorCount',0),(record,'MessageCount',len(errors)),
        (dataset,'FileLineTotalCount',row_count),(dataset,'FileLineImportSuccessCount',row_count),
        (dataset,'FileLineImportErrorCount',0),(dataset,'ObjectTotalCount',row_count),
        (dataset,'ObjectLoadedCount',loaded),(dataset,'ObjectErrorCount',failed),
        (dataset,'LineUnprocessedCount',0),(dataset,'LineHeldCount',0),(dataset,'UnprocessedCount',0),(dataset,'SkippedCount',0)]
    if any(count(c,k) != expected for c,k,expected in expected_counts): findings.append('SCOPED_COUNTS_DISAGREE')
    if failed is None or loaded is None or failed <= 0 or failed+loaded != row_count:
        findings.append('TERMINAL_PARTITION_UNBALANCED')
    if record.get('ImportStatusCode') != 'SUCCESS' or record.get('LoadStatusCode') != 'ERROR' or (
            dataset.get('ImportedStatus') != 'SUCCESS' or dataset.get('LoadedStatus') != 'ERROR') or any(
            p.get('Status') != 'Succeeded' for p in diagnostic['processes']):
        findings.append('TERMINAL_PRODUCT_ERROR_NOT_ESTABLISHED')
    if not mapped['all_messages_uniquely_associated']: findings.append('ROW_ERROR_IDENTITY_UNRESOLVED')
    upload_ids = {f['upload_id'] for f in mapped['findings'] if f['status'] == 'EXACT_CANDIDATE_ROW'}
    failed_rows = mapped['rows_with_associated_errors']
    if len(upload_ids) != failed or len(failed_rows) != failed:
        findings.append('FAILED_ROW_PARTITION_INCOMPLETE')
    # Every candidate must have a distinct effective identity, including rows
    # that have no error. Otherwise aggregate conservation cannot identify them.
    values = [dict(zip(package.columns(),r)) for r in package.inspect_zip(candidate)]
    keys = [tuple(r.get(k) or r.get(FALLBACKS.get(k,'')) or None for k in FIELDS) for r in values]
    if len(set(keys)) != row_count: findings.append('CANDIDATE_IDENTITIES_NOT_DISTINCT')
    complete = not findings
    return {'schema_version':'ar-customer-error-attempt-review-v1',
        'status':'TERMINAL_ROW_PARTITION_ESTABLISHED' if complete else 'ROW_PARTITION_REVIEW_REQUIRED',
        'candidate_sha256':mapped['candidate_sha256'],'binding_sha256':package.fingerprint(binding),
        'observation_sha256':package.fingerprint(observation),'registration_sha256':binding['registration_sha256'],
        'stage_request_ids':attempt['stage_request_ids'],'message_review':mapped,'findings':findings,
        'failed_rows':failed_rows,'loaded_rows_by_partition':sorted(set(range(1,row_count+1))-set(failed_rows)) if complete else [],
        'row_partition_established':complete,'persisted_outcomes_verified':False,'recovery_authorized':False,
        'limits':['Caller must establish authentic raw core responses and approved deployment provenance.',
            'Loaded rows are derived only from complete failure identities plus balanced scoped file/object counts and distinct candidate identities.',
            'Loader classification does not prove rollback, field values, side effects or Journey synchronization.',
            'Recovery requires a separately reviewed exact candidate and normal approval.']}
