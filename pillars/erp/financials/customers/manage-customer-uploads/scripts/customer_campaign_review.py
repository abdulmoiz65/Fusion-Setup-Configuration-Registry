"""Review one FBDI campaign evidence bundle; no network, approval or submission."""
import argparse
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

import customers_package as package
import customer_identity_review as identity
import customer_ownership_review as ownership
import customer_value_review as values
import customer_profile_set_review as profiles
import customer_receipt_review as receipts
import customer_bill_to_review as bill_to
import customer_tax_review as tax
import customer_effect_review as effects
import customer_supporting_effect_review as supporting
import customer_attempt_review as attempts
import customer_request_review as requests
import customer_target_review as targets
import customer_reconciliation_scope as outcome_scope

require = package.require
EVIDENCE_KEYS = frozenset(('identity', 'ownership', 'values', 'profile_set',
    'receipt', 'bill_to', 'tax', 'before_identity', 'before_ownership',
    'before_values', 'after_values', 'effect_plan', 'before_supporting',
    'after_supporting', 'runtime_binding', 'core_status', 'staging', 'target_plan'))
FIELD_GROUPS = {
    'identity': frozenset(values.IDENTITY_FIELDS),
    'values': frozenset(values.FIELDS),
    'profile_set': frozenset(('CUSTOMER_PROFILE_CLASS', 'ACCT_ADDRESS_SET_CODE')),
    'receipt': frozenset(('PAYMENT_METHOD_NAME', 'PAYMENT_METHOD_PRIMARY_FLAG')),
    'bill_to': frozenset(('BILL_TO_CUST_SITE_REF',)),
    'tax': frozenset(('TAXPAYER_REGISTRATION_NUM',))}


def field_routes():
    """One authoritative reviewer per input, in the exact CSV column order."""
    fields = package.columns()
    flat = [field for group in FIELD_GROUPS.values() for field in group]
    require(len(flat) == len(set(flat)) and set(flat) == set(fields), 'CAMPAIGN_FIELD_ROUTING_INCOMPLETE')
    return {field: next(group for group, names in FIELD_GROUPS.items() if field in names) for field in fields}


def context(candidate, operation, environment):
    checked = package.inspect_candidate(candidate, operation)
    require(isinstance(environment, str), 'CAMPAIGN_ENVIRONMENT_ORIGIN')
    url = urlsplit(environment)
    require(url.scheme == 'https' and url.hostname and not url.username and not url.password
            and not url.query and not url.fragment and url.path in ('', '/'), 'CAMPAIGN_ENVIRONMENT_ORIGIN')
    return checked


def plan(candidate, operation, environment):
    checked = context(candidate, operation, environment)
    routes = field_routes()
    rows = [dict(zip(package.columns(), row)) for row in package.inspect_zip(candidate)]
    requested = [{'row': number, 'field': field, 'reviewer': routes[field]}
        for number, row in enumerate(rows, 1) for field, value in row.items() if value]
    omitted = [{'row': number, 'field': field, 'reviewer': routes[field]}
        for number, row in enumerate(rows, 1) for field, value in row.items() if not value]
    return {'schema_version': 'ar-customer-campaign-readback-plan-v1',
        'candidate_sha256': checked['candidate_sha256'], 'environment_url': environment,
        'operation_intent': operation, 'row_count': len(rows), 'field_routes': routes,
        'runtime_business_outcome_scope': outcome_scope.plan(candidate, operation, environment),
        'detailed_supplied_evidence_contract_is_runtime_prerequisite': False,
        'requested_checks': requested,
        'omitted_field_effect_checks': omitted,
        'mandatory_evidence': ['identity', 'ownership', 'values', 'profile_set',
            'before_identity', 'before_ownership', 'before_values', 'after_values',
            'effect_plan', 'target_plan', 'before_supporting', 'after_supporting', 'runtime_binding', 'core_status', 'staging'],
        'additional_requested_evidence': sorted({r['reviewer'] for r in requested} & {'tax','receipt','bill_to'}),
        'collection_contract': {
            'route': 'assisted_supplied_read_only_evidence',
            'reference': 'references/verification-plan.md',
            'before_preview': ['before_identity', 'before_ownership', 'target_plan',
                'before_values', 'before_supporting', 'effect_plan',
                'reviewed_supporting_baselines_and_expected_effects'],
            'after_submission': ['identity', 'ownership', 'values', 'profile_set',
                'receipt', 'bill_to', 'tax', 'after_values', 'after_supporting',
                'runtime_binding', 'core_status', 'staging'],
            'separate_review': ['physical_entity_creation_or_reuse_evidence',
                'profile_defaults_before_after', 'receipt_inventory_before_after',
                'bill_to_blank_effects_before_after', 'tax_inventory_and_callback_outcome',
                'candidate_to_staging_lineage', 'journey_synchronization'],
            'blank_input_is_no_effect_evidence': False,
            'after_evidence_required_before_preview': False,
            'automatic_collection_implemented': False},
        'separate_effect_obligations': ['physical_creation_or_reuse', 'profile_defaults',
            'receipt_assignment_deltas', 'tax_profile_deltas_and_async_completion',
            'bill_to_blank_update_effects', 'request_to_candidate_lineage', 'journey_sync'],
        'execution_authorized': False, 'live_ready': False}


def finding_status(result, row, key, value):
    findings = [f for f in result.get('findings', [])
                if isinstance(f, dict) and f.get('row') == row and f.get(key) == value]
    return findings[0]['status'] if len(findings) == 1 else 'FINDING_MISSING_OR_AMBIGUOUS'


def review(candidate, bundle):
    require(isinstance(bundle, dict) and set(bundle) == {
        'schema_version', 'environment_url', 'operation_intent', 'evidence'}, 'CAMPAIGN_BUNDLE_SCHEMA')
    require(bundle['schema_version'] == 'ar-customer-campaign-evidence-v1', 'CAMPAIGN_BUNDLE_VERSION')
    operation, environment, supplied = bundle['operation_intent'], bundle['environment_url'], bundle['evidence']
    readback = plan(candidate, operation, environment)
    require(isinstance(supplied, dict) and set(supplied) <= EVIDENCE_KEYS, 'CAMPAIGN_EVIDENCE_KEYS')
    results = {}

    def run(name, keys, fn):
        missing = [key for key in keys if key not in supplied]
        if missing:
            results[name] = {'status': 'EVIDENCE_MISSING', 'missing': missing}
            return
        try:
            results[name] = fn(*[supplied[key] for key in keys])
        except (ValueError, TypeError, KeyError, AttributeError, IndexError) as exc:
            # Unexpected data shape stays visible; raw exceptions can contain values.
            code = str(exc) if isinstance(exc, package.InvalidInput) and re.fullmatch(r'[A-Z0-9_]+', str(exc)) else 'MALFORMED_EVIDENCE'
            results[name] = {'status': 'EVIDENCE_INVALID', 'error': code}

    args = candidate, operation, environment
    run('targets', ['before_identity','before_ownership','target_plan'], lambda *docs: targets.analyze(*args, *docs))
    run('identity', ['identity'], lambda doc: identity.analyze(*args, doc))
    def after_ownership(identities, owners):
        require(isinstance(owners, dict) and owners.get('phase') == 'after', 'CAMPAIGN_AFTER_PHASE_REQUIRED')
        return ownership.analyze(*args, identities, owners)
    run('ownership', ['identity', 'ownership'], after_ownership)
    for name, module in [('values', values), ('profile_set', profiles), ('receipt', receipts), ('bill_to', bill_to), ('tax', tax)]:
        run(name, ['identity', 'ownership', name], lambda *docs, module=module: module.analyze(*args, *docs))
    run('effects', ['before_identity', 'before_ownership', 'identity', 'ownership',
        'before_values', 'after_values', 'effect_plan'], lambda *docs: effects.analyze(*args, *docs))
    run('supporting', ['before_identity', 'before_ownership', 'identity', 'ownership',
        'before_supporting', 'after_supporting'], lambda *docs: supporting.analyze(*args, *docs))
    run('attempt', ['runtime_binding', 'core_status'], lambda *docs: attempts.analyze(*args, *docs))

    def staging(binding, observation, evidence):
        attempt = attempts.staging_attempt(*args, binding, observation)
        return requests.analyze(*args, attempt, evidence)
    run('staging', ['runtime_binding', 'core_status', 'staging'], staging)

    findings = []
    for check in readback['requested_checks']:
        row, field, group = check['row'], check['field'], check['reviewer']
        result = results[group]
        if result['status'] in ('EVIDENCE_MISSING', 'EVIDENCE_INVALID'):
            status = result['status']
        elif group == 'identity':
            # Resolve all seven entities and parents, including derived keys.
            owned = [f for f in results['ownership'].get('findings', []) if f['row'] == row]
            status = ('MATCH' if owned and all(f['status'] in ('MATCH','TARGET_ROW_OBSERVED') for f in owned)
                      else 'OWNERSHIP_NOT_VERIFIED')
        elif group == 'values':
            status = finding_status(result, row, 'field', field)
        elif group == 'profile_set':
            status = finding_status(result, row, 'check', 'account_profile_class'
                if field == 'CUSTOMER_PROFILE_CLASS' else 'requested_reference_set')
        else:
            observed = [f for f in result['findings'] if f['row'] == row]
            status = observed[0]['status'] if len(observed) == 1 else 'FINDING_MISSING_OR_AMBIGUOUS'
            if status in ('SELECTED_TAX_VALUE_MATCH', 'SELECTED_RECEIPT_VALUES_MATCH', 'SELECTED_BILL_TO_LINK_MATCH'):
                status = 'MATCH'
        findings.append({**check, 'status': status})
    matched = bool(findings) and all(f['status'] == 'MATCH' for f in findings)
    # Do not expose identifiers or raw evidence through the combined result.
    safe_results = {}
    for name, result in results.items():
        safe_results[name] = {key: value for key, value in result.items()
            if key in ('schema_version','status','findings','missing','error','staging_counts',
                'organization_profile_findings','effects','limits')}
    return {'schema_version': 'ar-customer-campaign-review-v1',
        'status': 'REQUESTED_FIELD_OBSERVATIONS_MATCH' if matched else 'CAMPAIGN_EVIDENCE_REVIEW_REQUIRED',
        'candidate_sha256': readback['candidate_sha256'], 'environment_url': environment,
        'operation_intent': operation, 'bundle_sha256': package.fingerprint(bundle),
        'field_findings': findings, 'requested_fields_match': matched, 'components': safe_results,
        'open_obligations': readback['separate_effect_obligations'],
        'persisted_reconciliation_complete': False, 'execution_authorized': False,
        'retry_authorized': False, 'journey_complete': False,
        'limits': ['Only raw evidence is accepted; supplied pass/fail claims are not evidence.',
            'Each reviewer recomputes its bindings; partial observations remain visible.',
            'Blank/default and supporting effects, provenance/freshness, attempt causality and Journey synchronization require separate review.',
            'This is the offline reconciliation stage, not the live FBDI submission adapter.']}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--zip', required=True, type=Path)
    commands = parser.add_subparsers(dest='command', required=True)
    planning = commands.add_parser('plan')
    planning.add_argument('--operation', required=True, choices=('create','update','mixed'))
    planning.add_argument('--environment-url', required=True)
    checking = commands.add_parser('review')
    checking.add_argument('--bundle', required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        require(args.zip.stat().st_size <= package.LIMIT, 'LOCAL_INSPECTION_LIMIT_REQUIRES_STREAMING_REVIEW')
        candidate = args.zip.read_bytes()
        result = (plan(candidate, args.operation, args.environment_url) if args.command == 'plan'
                  else review(candidate, package.load_json(args.bundle)))
        print(json.dumps(result, indent=2))
        # Zero means plan generated; reviewed observations never complete the campaign.
        return 0 if args.command == 'plan' else 2
    except (OSError, ValueError, TypeError) as exc:
        code = str(exc) if isinstance(exc, package.InvalidInput) and re.fullmatch(r'[A-Z0-9_]+', str(exc)) else type(exc).__name__
        print(json.dumps({'status':'BLOCKED','error':code,'execution_authorized':False}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
