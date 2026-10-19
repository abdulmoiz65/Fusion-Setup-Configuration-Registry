"""Candidate-specific business-value obligations, separate from full physical audits.

This component cannot approve execution or complete an import. Identity, intent,
attempt lineage, relevant supporting effects and Journey have separate reviewers.
"""
import customers_package as package
import customer_api_effect_review as effects
import customer_api_dff_review as dff


def plan(candidate, operation, environment):
    inspection = package.inspect_candidate(candidate, operation)
    # Reuse origin validation without introducing a new external-operation route.
    from customer_api_snapshot import plan as reference_plan
    reference_plan(candidate, operation, environment, {})
    mapped = set().union(*effects.PROJECTIONS.values())
    rows = [dict(zip(package.columns(), row)) for row in package.inspect_zip(candidate)]
    return {
        'schema_version': 'ar-customer-business-outcome-scope-v1',
        'candidate_sha256': inspection['candidate_sha256'],
        'operation_intent': operation, 'environment_url': environment,
        'rows': [{
            'row': index,
            'requested_value_fields': [f for f in package.columns() if row[f]],
            'requested_api_projection_fields': [f for f in package.columns() if row[f] and f in mapped],
            'requested_separate_reviewer_fields': [f for f in package.columns() if row[f] and f not in mapped],
            'requested_dff_fields': [f for f in dff.FIELDS if row[f]],
            'omitted_fields': [f for f in package.columns() if not row[f]],
        } for index, row in enumerate(rows, 1)],
        'required_reviews': ['target_identity_and_entity_intent', 'parent_and_relationship_integrity',
            'all_requested_values', 'observed_omitted_value_changes', 'source_backed_relevant_effects',
            'attempt_and_partial_result_association'],
        'unobserved_internals_are_preserved': False,
        'unused_hidden_storage_is_unconditional_blocker': False,
        'requested_unreadable_values_are_verified': False,
        'sql_required': False, 'execution_authorized': False,
    }


def assess_values(candidate, operation, environment, before, after):
    """Recompute observations; never accept a caller's selected-fields PASS.

    Only the 77 direct/profile/set projection fields are adjudicated here. The
    other ten columns retain their identity/receipt/tax/Bill-to reviewers.
    A satisfied value component is deliberately not full reconciliation.
    """
    scoped = plan(candidate, operation, environment)
    comparison = effects.compare(candidate, operation, environment, before, after)
    results = []
    for requirement, observed, prior, current in zip(scoped['rows'], comparison['rows'], before['rows'], after['rows']):
        requested = set(requirement['requested_api_projection_fields'])
        blockers, disclosures = [], []
        for finding in observed['values']:
            field = finding['field']
            if field in requested and finding['after_value'] != 'MATCH':
                blockers.append({'field': field, 'reason': finding['after_value']})
            if finding['change'] == 'OMITTED_INPUT_VALUE_CHANGED_REVIEW_REQUIRED':
                blockers.append({'field': field, 'reason': finding['change']})
            elif field not in requested and finding['change'] in ('VALUE_NOT_RETURNED', 'OWNER_NOT_COMPARABLE', 'OWNER_NOT_RESOLVED'):
                disclosures.append({'field': field, 'reason': finding['change']})
        for identity in observed['identities']:
            if identity['status'] != 'SAME_REFERENCE_OWNER':
                # New targets need the separate creation/reuse review, not an
                # invented empty baseline or a blanket ban on creating entities.
                disclosures.append({'entity': identity['entity'], 'reason': identity['status']})
            if identity['status'] in ('REFERENCE_OWNER_CHANGED', 'REFERENCE_UNRESOLVED_AFTER', 'UNRESOLVED_BOTH_PHASES'):
                blockers.append({'entity': identity['entity'], 'reason': identity['status']})
        for finding in observed['metadata']:
            if finding['status'] == 'OBSERVED_METADATA_CHANGE_REVIEW_REQUIRED':
                blockers.append({'field': finding['field'], 'reason': finding['status']})
        old_dff, new_dff = prior.get('dff') or {}, current.get('dff') or {}
        old_values, new_values = old_dff.get('observed_values', {}), new_dff.get('observed_values', {})
        same_account = bool(prior['owners'].get('account') and
                            prior['owners'].get('account') == current['owners'].get('account'))
        if same_account:
            if 'ATTRIBUTE_CATEGORY' in old_values and 'ATTRIBUTE_CATEGORY' in new_values:
                if old_values['ATTRIBUTE_CATEGORY'] != new_values['ATTRIBUTE_CATEGORY']:
                    blockers.append({'field': 'ATTRIBUTE_CATEGORY', 'reason': 'DFF_CONTEXT_CHANGE_EFFECT_REVIEW_REQUIRED'})
            elif requirement['requested_dff_fields']:
                blockers.append({'field': 'ATTRIBUTE_CATEGORY', 'reason': 'DFF_CONTEXT_BASELINE_UNOBSERVED'})
            if requirement['requested_dff_fields']:
                # A changed deployment may reinterpret an unchanged physical value.
                # No guess based on a tenant API name or ATTR suffix is allowed.
                if not old_dff.get('metadata_revision') or not new_dff.get('metadata_revision'):
                    blockers.append({'field': 'ATTRIBUTE_CATEGORY', 'reason': 'DFF_METADATA_REVISION_UNOBSERVED'})
                elif old_dff['metadata_revision'] != new_dff['metadata_revision'] or old_dff.get('physical_to_api_mapping') != new_dff.get('physical_to_api_mapping'):
                    blockers.append({'field': 'ATTRIBUTE_CATEGORY', 'reason': 'DFF_DEPLOYMENT_CHANGED_REVIEW_REQUIRED'})
        results.append({'row': requirement['row'], 'projected_value_scope_satisfied': not blockers,
            'blockers': blockers, 'unobserved_or_incomparable': disclosures,
            'separate_reviewer_fields': requirement['requested_separate_reviewer_fields']})
    return {'schema_version': 'ar-customer-business-value-scope-review-v1',
        'candidate_sha256': scoped['candidate_sha256'], 'environment_url': environment,
        'operation_intent': operation, 'rows': results,
        'projected_value_scope_satisfied': all(row['projected_value_scope_satisfied'] for row in results),
        'comparison_sha256': package.fingerprint(comparison),
        'required_separate_reviews': scoped['required_reviews'],
        'sql_input_used': False, 'execution_authorized': False,
        'persisted_reconciliation_complete': False, 'journey_complete': False,
        'limits': ['Requested DFFs remain required; unobserved omitted storage is disclosed, not assumed preserved.',
            'Relevant sibling/history/default effects require a reviewed source-backed boundary.',
            'This value component does not replace identity, intent, relationships, separate requested-field reviewers or attempt evidence.',
            'Raw capture provenance, supported visibility and freshness must be reviewed before using supplied collections.']}


def main(argv=None):
    import argparse
    import json
    from pathlib import Path
    from customer_api_replay import recompute, core_inspector
    from customer_api_collect import save
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--operation', choices=['create', 'update', 'mixed'], required=True)
    parser.add_argument('--environment-url', required=True)
    parser.add_argument('--before', type=Path, required=True)
    parser.add_argument('--after', type=Path, required=True)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        package.require(not args.output.resolve().is_relative_to(args.repo.resolve()),
                        'API_PRIVATE_OUTPUT_OUTSIDE_REPOSITORY_REQUIRED')
        candidate = args.candidate.read_bytes()
        inspector = core_inspector(args.repo)
        before, after = (recompute(path, candidate, inspector) for path in (args.before, args.after))
        result = assess_values(candidate, args.operation, args.environment_url, before, after)
        result['raw_projections_recomputed'] = True
        result['fresh_collection_performed'] = False
        save(args.output, result)
        print(json.dumps({key: result[key] for key in ('projected_value_scope_satisfied',
            'persisted_reconciliation_complete', 'execution_authorized', 'raw_projections_recomputed')}))
        return 0 if result['projected_value_scope_satisfied'] else 2
    except Exception as exc:
        print(json.dumps({'status': 'BUSINESS_VALUE_SCOPE_REVIEW_INCOMPLETE',
            'error_type': type(exc).__name__,
            'error_code': str(exc) if isinstance(exc, package.InvalidInput) else 'REVIEW_OR_ARTIFACT_FAILURE',
            'execution_authorized': False}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
