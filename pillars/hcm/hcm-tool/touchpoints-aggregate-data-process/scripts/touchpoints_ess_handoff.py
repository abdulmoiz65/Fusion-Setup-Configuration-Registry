"""Touchpoints Full/daily coordination through the unchanged core ESS module.

No CLI, REST client, authentication flow, or automatic POST retry lives here.
The invoking nested skill must finish identity, catalog, schema,
immutable-review and immediate approval gates before calling submit_and_monitor.
Fusion enforces ESS authorization on execution. No separate privilege probe or
privilege evidence field is required or passed to the Scheduler payload.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time

from touchpoints_runbook import build
from touchpoints_workflow import CONTEXT, JOB, timestamp

ROOT = Path(__file__).resolve().parents[5]
CURRENT = Path('artifacts/pillars/hcm/hcm-tool/touchpoints-aggregate-data-process/current')
CORE_PATH = ROOT / 'core/fusion-api/ess-job-submitter/scripts/ess_job_submitter.py'
EXTRA_FIELDS = ('requestType', 'requestParameters', 'schedule', 'product',
                'requestedStartTime', 'requestedEndTime', 'absParentRequestId',
                'instanceParentId', 'lastScheduleInstanceId')


class AuditPersistenceError(RuntimeError):
    """Keep sanitized identity available when the durable checkpoint fails."""
    def __init__(self, record):
        self.result = {**record, 'failure_class': 'artifact_persistence', 'verified': False}
        super().__init__('ESS audit persistence failed; do not resubmit')


def load_core():
    name = 'touchpoints_core_ess'
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, CORE_PATH)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def instant(value):
    if not timestamp(value):
        raise ValueError('Offset-bearing schedule timestamp required')
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


def recurrence(schedule):
    if not isinstance(schedule, dict) or schedule.get('inclusions') or schedule.get('exclusions'):
        raise ValueError('Exactly one daily recurrence without exceptions required')
    rows = schedule.get('recurrences')
    if not isinstance(rows, list) or len(rows) != 1 or not isinstance(rows[0], dict):
        raise ValueError('Exactly one daily recurrence required')
    row = rows[0]
    parts = str(row.get('icalString', '')).rstrip(';').split(';')
    if len(parts) != 2 or set(parts) != {'FREQ=DAILY', 'INTERVAL=1'}:
        raise ValueError('Daily interval must be one')
    start = instant(row.get('startDate'))
    end = instant(row['endDate']) if row.get('endDate') else None
    if end and end <= start:
        raise ValueError('Schedule end must follow start')
    return start, end


def prepare_handoff(state, snapshot, contract, operation):
    """Recheck local gates; never grant approval or produce an external call."""
    if operation not in ('full', 'daily'):
        raise ValueError('Only Full and daily Incremental handoffs are supported')
    plan = build(state, snapshot)
    gate = 'daily_ready_for_preview' if operation == 'daily' else (
        'full_ready_for_preview' if plan['scope']['mode'] == 'implementation' else 'standalone_ready_for_preview')
    checkpoint = next((r for r in plan['execution']['checkpoints'] if r['key'] == operation), {})
    if (not plan['runbook_complete'] or not plan[gate]
            or state.get('run_status') in ('stopped', 'paused', 'abandoned')
            or state.get('pending_operation')
            or checkpoint.get('state') not in ('ready', 'awaiting_write_approval')):
        raise ValueError('Current Run Book, predecessors and readiness must permit this handoff')
    if not isinstance(contract, dict) or contract.get('contract_version') != '1.0' or contract.get('stage') != 'approved_submission':
        raise ValueError('Validated version 1.0 approved_submission required')
    approval = contract.get('approval', {})
    payload = contract.get('request_payload', {})
    if not isinstance(approval, dict) or approval.get('explicit_submission_approval') is not True or approval.get('approved_payload_sha256') != digest(payload):
        raise ValueError('Explicit approval must match the exact immutable payload')
    audit = contract.get('audit_context', {})
    environment = contract.get('fusion_environment_context', {})
    if (not isinstance(audit, dict) or any(audit.get(k) != state[k] for k in CONTEXT)
            or not isinstance(audit.get('approval_reference'), str) or not audit['approval_reference'].strip()
            or not isinstance(environment, dict) or environment.get('environment') != state['environment']):
        raise ValueError('Approval audit and target must match current project/environment/revision')
    if contract.get('task') != {'task_name': 'Aggregate Oracle Touchpoints Data', 'task_code': 'CUSTOM_AGGREGATE_ORACLE_TOUCHPOINTS_DATA'}:
        raise ValueError('Canonical Touchpoints ESS catalog identity required')
    if contract.get('job_contract') != {'job_definition_id': JOB, 'application': 'EarHcmEss'}:
        raise ValueError('Fixed Touchpoints job contract required')
    mode = 'ORA_HRE_INCREMENTAL_RUN' if operation == 'daily' else 'ORA_HRE_FULL_RUN'
    if operation == 'full' and plan['scope']['mode'] == 'selected_tasks' and 'daily' not in plan['scope']['selected_tasks']:
        mode = state.get('task_requirements', {}).get('full', {}).get('run_type', mode)
        if mode not in ('ORA_HRE_FULL_RUN', 'ORA_HRE_INCREMENTAL_RUN'):
            raise ValueError('Unsupported standalone run mode')
    if (not isinstance(payload, dict) or payload.get('jobDefinitionId') != JOB
            or payload.get('application') != 'EarHcmEss' or payload.get('product') != 'HRE'
            or type(payload.get('retries')) is not int or payload['retries'] != 0
            or set(payload) - {'jobDefinitionId', 'application', 'product', 'retries', 'description', 'requestParameters', 'schedule', 'executePast'}):
        raise ValueError('Fixed Touchpoints payload required')
    parameters = payload.get('requestParameters')
    if not isinstance(parameters, list) or len(parameters) != 2:
        raise ValueError('Exactly two ordered Touchpoints parameters required')
    workers = parameters[0].get('value') if isinstance(parameters[0], dict) else None
    if (not isinstance(workers, str) or not workers.isdecimal() or not 1 <= int(workers) <= 20
            or parameters != [{'name': 'submit.argument1', 'paramType': 'STRING', 'value': workers},
                              {'name': 'submit.argument2', 'paramType': 'STRING', 'value': mode}]):
        raise ValueError('Worker count and ordered run-mode parameters must match the operation')
    options = contract.get('execution_options', {})
    if (not isinstance(options, dict) or set(options) != {'wait_seconds', 'poll_interval_seconds'}
            or any(type(options[k]) is not int or not 1 <= options[k] <= 86400 for k in options)):
        raise ValueError('Positive bounded polling options required')
    if operation == 'daily':
        schedule = payload.get('schedule')
        if not isinstance(schedule, dict) or set(schedule) != {'recurrences'}:
            raise ValueError('Approved inline daily schedule required')
        row = schedule['recurrences'][0] if isinstance(schedule['recurrences'], list) and schedule['recurrences'] else {}
        if (not isinstance(row, dict) or set(row) - {'icalString', 'startDate', 'endDate'}
                or row.get('icalString') != 'FREQ=DAILY;INTERVAL=1;'
                or payload.get('executePast') is not False
                or options != {'wait_seconds': 1, 'poll_interval_seconds': 1}):
            raise ValueError('Daily recurrence, executePast and bounded readback must match review')
        start, _ = recurrence(schedule)
        if start <= datetime.now(timezone.utc):
            raise ValueError('New schedule start must be in the future')
    elif 'schedule' in payload or 'executePast' in payload:
        raise ValueError('Full is an on-demand submission without recurrence')
    core = load_core()
    core.validate_request_payload(payload)
    return {'operation': operation, 'request_payload': deepcopy(payload), 'execution_options': dict(options),
            'context': {k: state[k] for k in CONTEXT}, 'binding': dict(state['runbook']['bindings'][operation]),
            'approval_reference': audit['approval_reference'], 'payload_sha256': digest(payload),
            'full_request_id': state.get('full_run', {}).get('request_id'),
            'readback_fields': list(core.DEFAULT_STATUS_FIELDS) + list(EXTRA_FIELDS),
            'write_authorized': False}


def inspect_readback(handoff, request_id, status):
    """Project safe evidence; raw system parameters, messages and stacks stay in memory."""
    payload = handoff['request_payload']
    parameters = status.get('requestParameters', [])
    expected = payload['requestParameters']
    matches = isinstance(parameters, list) and all(
        sum(isinstance(p, dict) and all(p.get(k) == value for k, value in item.items()) for p in parameters) == 1
        and sum(isinstance(p, dict) and p.get('name') == item['name'] for p in parameters) == 1
        for item in expected)
    errors = any(status.get(k) for k in ('errorType', 'errorWarningMessage', 'errorWarningDetail'))
    exact = (str(status.get('requestId')) == str(request_id) and status.get('jobDefinitionId') == JOB
             and status.get('application') == 'EarHcmEss' and matches and not errors)
    core = load_core()
    terminal = core.is_terminal_status(status)
    if handoff['operation'] == 'daily':
        try:
            schedule_matches = recurrence(status.get('schedule')) == recurrence(payload['schedule'])
            schedule_matches &= not status['schedule'].get('timezone')
        except (ValueError, TypeError, KeyError):
            schedule_matches = False
        verified = bool(exact and status.get('requestType') == 'RECUR_PARENT' and schedule_matches
                        and status.get('cause') in ('NON_TERMINAL', 'PROCESS_SUCCESS')
                        and status.get('state') is not None and not status.get('completedTime')
                        and not core.terminal_by_text(status.get('state'))
                        and not core.terminal_by_text(status.get('processPhase')))
    else:
        verified = bool(exact and status.get('cause') == 'PROCESS_SUCCESS' and timestamp(status.get('completedTime')))
    safe_causes = {'NON_TERMINAL', 'PROCESS_SUCCESS', 'PROCESS_ERROR', 'PROCESS_WARNING',
                   'PROCESS_CANCEL', 'PROCESS_TIMED_OUT', 'PROCESS_UNKNOWN_STATUS',
                   'OPERATOR_CANCEL', 'VALIDATION_ERROR', 'SYSTEM_ERROR',
                   'REQUEST_LOGIN_ERROR', 'REQUEST_AUTHORIZATION_FAILED'}
    return {'verified': verified, 'errors_present': errors, 'terminal': terminal,
            'request_type': status.get('requestType') if status.get('requestType') in ('RECUR_PARENT', 'SINGLETON') else None,
            'completed_at': status.get('completedTime') if timestamp(status.get('completedTime')) else None,
            'cause': status.get('cause') if status.get('cause') in safe_causes else 'OTHER'}


def append_event(stream, event):
    try:
        stream.write(json.dumps({**event, 'recorded_at': datetime.now(timezone.utc).isoformat()}, allow_nan=False) + '\n')
        stream.flush()
        os.fsync(stream.fileno())
    except OSError as exc:
        raise AuditPersistenceError(event) from exc


def submit_and_monitor(project_root, contract, operation, access_token, *, run_id, timeout=60):
    """Delegate exactly one POST, checkpoint identity, then core-only monitoring.

    Entry requires current schema validation and agent-owned external preflight.
    OAuth is obtained through the already selected core authentication workflow.
    This function never calls core.main/run_with_token (which can replay a POST).
    Reuse of a run_id fails before dispatch. Any recovery is a separate read.
    """
    if not isinstance(run_id, str) or not run_id or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in run_id):
        raise ValueError('Path-safe unique run_id required')
    if type(timeout) is not int or not 1 <= timeout <= 60:
        raise ValueError('HTTP timeout must be 1..60 seconds')
    if not isinstance(access_token, str) or not access_token:
        raise ValueError('Token from the selected core authentication workflow required')
    project = Path(project_root).resolve(strict=True)
    state = json.loads((project / CURRENT / 'touchpoints-workflow-state.json').read_text())
    snapshot = json.loads((project / CURRENT / 'runbook-task-snapshot.json').read_text())
    control = json.loads((project / 'state/project-state.json').read_text()).get('runbook_control', {})
    if control.get('status') != 'active' or str(control.get('active_runbook_ref')) != state.get('runbook', {}).get('journey_id'):
        raise ValueError('Active project Run Book must match the Touchpoints binding')
    handoff = prepare_handoff(state, snapshot, deepcopy(contract), operation)
    core = load_core()
    props = core.read_properties(core.DEFAULT_PROPERTIES_PATH)
    core.require_props(props, ['environment', 'restBaseUrl'])
    if any(props.get(k) != contract['fusion_environment_context'].get(k) for k in ('environment', 'restBaseUrl')):
        raise ValueError('Configured target must match the approved environment and host')
    # A verified synchronized owner handoff is required, even for the manual daily row.
    owners = json.loads((project / CURRENT / 'owner-handoffs.json').read_text())
    if any(owners.get(k) != state[k] for k in CONTEXT) or not any(
        row.get('key') == operation and row.get('runbook_binding') == handoff['binding']
        and row.get('execution_route') == 'ess' for row in owners.get('tasks', [])):
        raise ValueError('Synchronized ESS owner handoff required')
    directory = project / CURRENT / 'ess-runs'
    if not directory.resolve().is_relative_to(project):
        raise ValueError('Audit destination must remain inside the project')
    directory.mkdir(parents=True, exist_ok=True)
    audit_path = directory / f'{run_id}.jsonl'
    if audit_path.exists():
        raise FileExistsError('ESS audit already exists; do not replay submission')
    # A new name cannot bypass an attempted/confirmed submission after a crash.
    # Keep a recurring schedule's barrier across configuration revisions.
    for previous in directory.glob('*.jsonl'):
        try:
            events = [json.loads(line) for line in previous.read_text().splitlines()]
        except (OSError, ValueError):
            raise ValueError('Cannot reconcile prior ESS audit; dispatch blocked') from None
        if any(event.get('operation') == operation and event.get('submission_attempted') is True
               and event.get('project_id') == state['project_id'] and event.get('environment') == state['environment']
               and (operation == 'daily' or event.get('configuration_revision') == state['configuration_revision'])
               for event in events):
            raise ValueError('Prior ESS attempt requires read-only reconciliation; a new run ID cannot authorize resubmission')
    result = {**handoff['context'], 'operation': operation, 'submitted': False,
              'submission_attempted': False, 'request_id': None, 'verified': False,
              'verification_reference': str(audit_path), 'approval_reference': handoff['approval_reference'],
              'payload_sha256': handoff['payload_sha256'], 'runbook_binding': handoff['binding'],
              'full_request_id': handoff['full_request_id'], 'job_definition_id': JOB,
              'run_type': handoff['request_payload']['requestParameters'][1]['value'],
              'number_of_workers': int(handoff['request_payload']['requestParameters'][0]['value']),
              'next_action': 'reconcile_existing_request_read_only', 'failure_class': None}
    if operation == 'daily':
        start, end = recurrence(handoff['request_payload']['schedule'])
        result['approved_schedule'] = {'icalString': 'FREQ=DAILY;INTERVAL=1;',
                                       'startDate': start.isoformat(), 'endDate': end.isoformat() if end else None}
    # Exclusive creation prevents accidental audit overwrite/replay.
    with audit_path.open('x', encoding='utf-8') as stream:
        stage = 'audit_preflight'
        started = None
        try:
            append_event(stream, {**result, 'stage': stage})
            stage = 'submission'
            result.update(submission_attempted=True, submitted=None)
            append_event(stream, {**result, 'stage': stage})
            response = core.submit_job_request(props, access_token, handoff['request_payload'], timeout=timeout)
            request_id = core.extract_request_id(response.body, response.headers)
            if type(request_id) is not int or request_id <= 0:
                raise ValueError('Missing valid request identity')
            result.update(submitted=True, request_id=request_id)
            # The request ID is durable BEFORE any GET or wait function can fail.
            stage = 'identity_checkpoint'
            append_event(stream, {**result, 'stage': stage})
            stage = 'readback'
            started = time.monotonic()
            options = handoff['execution_options']
            if operation == 'daily':
                status = core.get_job_request(props, access_token, request_id,
                    fields=handoff['readback_fields'], timeout=timeout).body
            else:
                status = core.wait_for_job_request(props, access_token, request_id,
                    fields=handoff['readback_fields'], wait_seconds=options['wait_seconds'],
                    poll_interval=options['poll_interval_seconds'], timeout=timeout)
            result.update(inspect_readback(handoff, request_id, status))
            result['elapsed_wait_seconds'] = round(time.monotonic() - started, 3)
            result['schedule_verified'] = operation == 'daily' and result['verified']
            result['verified_at'] = datetime.now(timezone.utc).isoformat() if result['verified'] else None
            result['next_action'] = 'propose_authorized_runbook_completion' if result['verified'] else 'reconcile_existing_request_read_only'
            if not result['verified']:
                result['failure_class'] = 'process_failed' if result['errors_present'] or result['terminal'] and result['cause'] != 'PROCESS_SUCCESS' else 'process_timeout' if operation == 'full' and not result['terminal'] else 'catalog_or_metadata_mismatch'
        except AuditPersistenceError:
            raise
        except Exception as exc:
            result['failure_class'] = (
                'authorization_or_privilege' if isinstance(exc, core.FusionHttpError) and exc.status_code in (401, 403)
                else 'fusion_api_error' if isinstance(exc, core.FusionHttpError)
                else 'transport_or_environment')
            result['http_status'] = exc.status_code if isinstance(exc, core.FusionHttpError) else None
            # Exception text/body can contain credentials or protected responses.
            result['message'] = 'ESS handoff stopped; reconcile retained identity and audit stage.'
        result['stage'] = stage
        if started is not None:
            result['elapsed_wait_seconds'] = round(time.monotonic() - started, 3)
        append_event(stream, result)
    return result
