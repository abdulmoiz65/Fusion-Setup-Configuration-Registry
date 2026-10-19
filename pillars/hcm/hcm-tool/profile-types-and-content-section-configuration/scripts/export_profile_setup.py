#!/usr/bin/env python3
"""Skill-local approval gate; delegates once to the unchanged shared exporter."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
ADAPTER = ROOT / 'shared/setup-export/task-level-export/scripts/export_setup_task_csv.py'
TASKS = {'HRT_MANAGE_PROFILE_TYPES': 'profile-types', 'HRT_MANAGE_CONTENT_SUBSCRIBERS': 'content-subscribers'}


def plan(request, props):
    required = {'environment', 'restBaseUrl', 'task_code', 'mode', 'criteria', 'project_id', 'output_dir'}
    if set(request) != required:
        raise ValueError('Export request fields must match the documented contract exactly.')
    if request['task_code'] not in TASKS or request['mode'] not in ('template', 'data'):
        raise ValueError('Only explicit Profile Types/Content Subscribers template or data exports are supported.')
    if any(request[k] != props.get(k) or not request[k] for k in ('environment', 'restBaseUrl')):
        raise ValueError('Export environment does not match the selected core configuration.')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', request['project_id']):
        raise ValueError('Invalid project ID.')
    allowed = (ROOT / 'project' / request['project_id'] / 'exports/hcm-tool/profile-types-and-content-section-configuration' / TASKS[request['task_code']]).resolve()
    output = Path(request['output_dir']).resolve()
    if output != allowed and allowed not in output.parents:
        raise ValueError('Export destination is outside this task project directory.')
    if not (ROOT / 'project' / request['project_id'] / 'state/project-state.json').is_file():
        raise ValueError('An initialized project is required.')
    if not isinstance(request['criteria'], list) or (request['mode'] == 'template' and request['criteria']):
        raise ValueError('Invalid export criteria or template/data mode conflict.')
    sys.path.insert(0, str(ADAPTER.parent))
    sys.path.insert(0, str(ROOT / 'shared/setup-export/fsm-csv-export/scripts'))
    from fsm_csv_export_engine import normalize_task_export_criteria
    criteria = normalize_task_export_criteria(request['criteria'], request['task_code'])
    if criteria != request['criteria']:
        raise ValueError('Review normalized criteria including the exact TaskCode before approval.')
    command = [sys.executable, str(ADAPTER), '--task-code', request['task_code'],
               '--project-id', request['project_id'], '--output-dir', str(output),
               '--wait-seconds', '300', '--poll-interval', '10',
               '--export-criteria', json.dumps(criteria)]
    # The shared adapter defaults to template-only; omission is not data mode.
    command.append('--template-only' if request['mode'] == 'template' else '--data')
    fingerprint = hashlib.sha256(json.dumps(request, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    return command, fingerprint


def execute(request, props, approval, journal_dir, extra_args=(), runner=subprocess.run):
    command, fingerprint = plan(request, props)
    if (approval.get('approved') is not True or approval.get('request') != request or
            not isinstance(approval.get('approval_ref'), str) or not approval['approval_ref'].strip()):
        raise ValueError('Explicit approval bound to this exact export is required.')
    # One durable reservation per actual user approval, even if the command fails.
    journal_dir = Path(journal_dir).resolve()
    expected = (ROOT / 'project' / request['project_id'] / 'state/runs').resolve()
    if journal_dir != expected:
        raise ValueError('Export attempt journal must use the selected project state/runs directory.')
    key = hashlib.sha256(approval['approval_ref'].encode()).hexdigest()
    journal = journal_dir / ('profile-export-' + key + '.json')
    journal_dir.mkdir(parents=True, exist_ok=True)
    with journal.open('x', encoding='utf-8') as stream:
        json.dump({'status': 'attempt_reserved', 'request_sha256': fingerprint,
                   'next_action': 'Do not resubmit; reconcile existing process or obtain fresh explicit retry approval.'}, stream)
    # This shared orchestration entry point does not catch/replay create errors.
    # Never use create_setup_task_csv_export.py or fsm_csv_export.py creation routes.
    result = runner(command + list(extra_args), cwd=ROOT, text=True, capture_output=True)
    process_ids = re.findall(r'(?:process:|ProcessId:)\s*`?(\d+)', result.stdout)
    with journal.open('w', encoding='utf-8') as stream:
        json.dump({'status': 'adapter_finished', 'returncode': result.returncode,
                   'request_sha256': fingerprint, 'process_ids': sorted(set(process_ids)),
                   'next_action': 'Resume GET-only polling by ProcessId; never replay creation.'}, stream)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--request', required=True, type=Path)
    parser.add_argument('--approval', type=Path)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--token-cache', default='auto')
    args = parser.parse_args()
    try:
        sys.path.insert(0, str(ROOT / 'core/auth/fusion-oauth-authentication/scripts'))
        from fusion_auth import read_properties
        props = read_properties(ROOT / 'core/auth/fusionEnv.properties')
        request = json.loads(args.request.read_text())
        command, fingerprint = plan(request, props)
        if not args.execute:
            print(json.dumps({'status': 'planned', 'request': request, 'request_sha256': fingerprint, 'fusion_calls': 0}))
            return 0
        if not args.approval:
            raise ValueError('Approval is required for execution.')
        result = execute(request, props, json.loads(args.approval.read_text()),
                         ROOT / 'project' / request['project_id'] / 'state/runs',
                         ['--token-cache', args.token_cache])
        print(result.stdout, end='')
        if result.returncode:
            print('Export adapter stopped. Inspect the retained ProcessId; do not rerun creation.', file=sys.stderr)
        return result.returncode
    except (ValueError, OSError, TypeError, KeyError) as error:
        print(json.dumps({'status': 'blocked', 'message': str(error)}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
