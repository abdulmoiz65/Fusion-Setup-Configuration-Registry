"""Offline staging scope observations; no runtime ID discovery or execution authority."""
from datetime import datetime
import re
from urllib.parse import urlsplit

import customers_package as package

require = package.require
ERROR_STATUSES = {'FAILED', 'FAILED_NOT_CORRECTABLE', 'BLOCKED'}
ROW_FIELDS = {'cust_upload_id', 'load_request_id', 'upload_request_id',
              'batch_id', 'file_record_num', 'upload_status'}


def positive_id(value):
    return isinstance(value, str) and re.fullmatch(r'[1-9][0-9]*', value) is not None


def text(value):
    return isinstance(value, str) and bool(value.strip())


def timestamp(value):
    try:
        result = datetime.fromisoformat(value.replace('Z', '+00:00'))
        require(result.tzinfo is not None, 'REQUEST_CAPTURE_TIME')
        return result
    except (ValueError, TypeError, AttributeError) as exc:
        raise package.InvalidInput('REQUEST_CAPTURE_TIME') from exc


def analyze(candidate, operation, environment_url, attempt, evidence):
    """Compare separately supplied IDs to a complete LOAD_REQUEST_ID readback.

    The caller must retain core responses and reviewed ID extraction evidence.
    This contract deliberately cannot certify the unverified live field mapping
    from initiation to interface/product requests, nor staging-to-ZIP lineage.
    """
    preview = package.inspect_candidate(candidate, operation)
    origin = urlsplit(environment_url)
    require(origin.scheme == 'https' and origin.hostname and not origin.username
            and not origin.password and origin.path in ('', '/')
            and not origin.query and not origin.fragment, 'REQUEST_ENVIRONMENT')
    require(isinstance(attempt, dict) and set(attempt) == {
        'schema_version', 'candidate_sha256', 'environment_url', 'operation_intent',
        'initiation_request_id', 'content_id', 'interface_request_id', 'upload_request_id',
        'initiated_at', 'initiation_evidence_reference', 'scope_evidence_reference'}, 'REQUEST_ATTEMPT_SCHEMA')
    require(attempt['schema_version'] == 'ar-customer-request-attempt-v1', 'REQUEST_ATTEMPT_VERSION')
    require(attempt['candidate_sha256'] == preview['candidate_sha256']
            and attempt['environment_url'] == environment_url
            and attempt['operation_intent'] == operation, 'REQUEST_ATTEMPT_BINDING')
    require(positive_id(attempt['initiation_request_id']) and positive_id(attempt['interface_request_id'])
            and (attempt['upload_request_id'] is None or positive_id(attempt['upload_request_id'])), 'REQUEST_ID')
    require(all(text(attempt[k]) for k in ('content_id', 'initiation_evidence_reference',
                                         'scope_evidence_reference')), 'REQUEST_PROVENANCE')
    require(isinstance(evidence, dict) and set(evidence) == {
        'schema_version', 'attempt_sha256', 'captured_at', 'evidence_reference',
        'requested_load_request_id', 'complete', 'records'}, 'REQUEST_EVIDENCE_SCHEMA')
    require(evidence['schema_version'] == 'ar-customer-request-evidence-v1', 'REQUEST_EVIDENCE_VERSION')
    require(evidence['attempt_sha256'] == package.fingerprint(attempt), 'REQUEST_EVIDENCE_BINDING')
    require(evidence['requested_load_request_id'] == attempt['interface_request_id'], 'REQUEST_QUERY_SCOPE')
    require(text(evidence['evidence_reference']), 'REQUEST_PROVENANCE')
    require(timestamp(evidence['captured_at']) >= timestamp(attempt['initiated_at']), 'REQUEST_CAPTURE_TIME')
    require(type(evidence['complete']) is bool and isinstance(evidence['records'], list), 'REQUEST_QUERY_VALUES')
    for row in evidence['records']:
        require(isinstance(row, dict) and set(row) == ROW_FIELDS, 'REQUEST_ROW_SCHEMA')
        require(positive_id(row['cust_upload_id']) and positive_id(row['load_request_id'])
                and all(row[k] is None or positive_id(row[k]) for k in
                        ('upload_request_id', 'batch_id', 'file_record_num')), 'REQUEST_ROW_ID')
        require(row['upload_status'] is None or isinstance(row['upload_status'], str), 'REQUEST_ROW_STATUS')

    records = evidence['records']
    findings = []
    counts = None
    if not evidence['complete']:
        findings.append('STAGING_QUERY_INCOMPLETE')
    elif any(row['load_request_id'] != attempt['interface_request_id'] for row in records):
        findings.append('STAGING_ROWS_OUTSIDE_INTERFACE_SCOPE')
    elif len({row['cust_upload_id'] for row in records}) != len(records):
        findings.append('DUPLICATE_STAGING_ROWS')
    else:
        counts = {'total': len(records),
                  'success': sum(row['upload_status'] == 'SUCCESS' for row in records),
                  'error': sum(row['upload_status'] in ERROR_STATUSES for row in records)}
        counts['pending'] = counts['total'] - counts['success'] - counts['error']
        if not records:
            findings.append('NO_STAGING_ROWS_OBSERVED')
        else:
            if any(row['batch_id'] is None or row['upload_request_id'] is None for row in records):
                findings.append('PRODUCT_STAMPS_INCOMPLETE')
            if len({row['batch_id'] for row in records if row['batch_id'] is not None}) > 1:
                findings.append('MULTIPLE_BATCH_IDS_REVIEW_REQUIRED')
            if len({row['upload_request_id'] for row in records if row['upload_request_id'] is not None}) > 1:
                findings.append('MULTIPLE_UPLOAD_REQUEST_IDS_REVIEW_REQUIRED')
            expected_upload = attempt['upload_request_id']
            if expected_upload is None:
                findings.append('EXPECTED_UPLOAD_REQUEST_ID_UNAVAILABLE')
            elif any(row['upload_request_id'] not in (None, expected_upload) for row in records):
                findings.append('UPLOAD_REQUEST_ID_MISMATCH')
            if counts['error']:
                findings.append('STAGING_ERRORS_OBSERVED')
            if counts['pending']:
                findings.append('STAGING_NONTERMINAL_OR_UNKNOWN_STATUS')
            if len(records) != len(package.inspect_zip(candidate)):
                findings.append('CANDIDATE_AND_STAGING_ROW_COUNTS_DIFFER')
            if not findings:
                findings.append('SUPPLIED_STAGING_SCOPE_AGREES')

    return {'schema_version': 'ar-customer-request-review-v1',
            'status': 'SCOPED_REQUEST_OBSERVATIONS',
            'candidate_sha256': preview['candidate_sha256'],
            'attempt_sha256': package.fingerprint(attempt),
            'evidence_sha256': package.fingerprint(evidence),
            'findings': findings, 'staging_counts': counts,
            'initiation_to_product_link_verified': False,
            'candidate_staging_lineage_verified': False,
            'persisted_reconciliation_complete': False,
            'execution_authorized': False, 'retry_authorized': False, 'journey_complete': False,
            'limits': ['Supplied evidence is not authenticated; matching IDs/counts do not establish attempt lineage.',
                       'FILE_RECORD_NUM can identify a party group; it is not a candidate CSV row number.',
                       'Receipt assignment REQUEST_ID=-BATCH_ID is not an ESS request ID.',
                       'All core datasets, scopes and errors must be retained separately; this checks one Customers staging scope.',
                       'SUCCESS is a staging observation, not full reconciliation, rollback proof or recovery authorization.']}
