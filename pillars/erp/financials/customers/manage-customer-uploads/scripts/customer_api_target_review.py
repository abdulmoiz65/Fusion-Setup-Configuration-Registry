"""Review existing-target intent from candidate-bound API observations, without SQL."""
import customers_package as package
import customer_api_effect_review as effects

PARENTS = {'account_identity', 'account_party', 'account_site_identity', 'account_site_account',
    'account_site_party_site', 'account_site_use_identity', 'account_site_use_parent',
    'account_site_use_purpose', 'account_site_use_set', 'party_site_identity', 'party_site_party',
    'party_site_location', 'party_site_use_identity', 'party_site_use_parent', 'party_site_use_purpose'}


def analyze(candidate, operation, environment, before, plan):
    digest = package.inspect_candidate(candidate, operation)['candidate_sha256']
    rows = package.inspect_zip(candidate)
    require = package.require
    require(isinstance(before, dict) and before.get('schema_version') == 'ar-customer-api-collection-v1'
        and before.get('candidate_sha256') == digest and before.get('operation_intent') == operation
        and before.get('environment_url') == environment and before.get('phase') == 'before'
        and before.get('read_only') is True and before.get('sql_input_used') is False
        and before.get('status') == 'API_OBSERVATIONS_CAPTURED_WITH_LIMITATIONS', 'API_TARGET_COLLECTION_BINDING')
    require(effects.timestamp(before['started_at']) <= effects.timestamp(before['finished_at']), 'API_TARGET_CAPTURE_ORDER')
    require(isinstance(before.get('rows'), list) and len(before['rows']) == len(rows)
        and [item.get('row') for item in before['rows']] == list(range(1, len(rows)+1)), 'API_TARGET_ROW_BINDING')
    require(isinstance(plan, dict) and set(plan) == {'schema_version', 'candidate_sha256', 'environment_url',
        'operation_intent', 'collection_sha256', 'review_reference', 'expectations'}
        and plan['schema_version'] == 'ar-customer-api-target-plan-v1'
        and plan['candidate_sha256'] == digest and plan['environment_url'] == environment
        and plan['operation_intent'] == operation and plan['collection_sha256'] == package.fingerprint(before)
        and isinstance(plan['review_reference'], str) and plan['review_reference'].strip(), 'API_TARGET_PLAN_BINDING')
    expected = {}
    require(isinstance(plan['expectations'], list), 'API_TARGET_EXPECTATIONS')
    for entry in plan['expectations']:
        require(isinstance(entry, dict) and set(entry) == {'row', 'entity', 'intent'}
            and type(entry['row']) is int and 1 <= entry['row'] <= len(rows)
            and entry['entity'] in effects.OWNERS and entry['intent'] in ('create', 'update', 'reuse'), 'API_TARGET_EXPECTATIONS')
        key = entry['row'], entry['entity']
        require(key not in expected, 'API_TARGET_DUPLICATE_INTENT')
        expected[key] = entry['intent']
    require(set(expected) == {(row, entity) for row in range(1, len(rows)+1) for entity in effects.OWNERS},
            'API_TARGET_INCOMPLETE_INTENT')
    findings, physical = [], {}
    for item in before['rows']:
        number, owners = item['row'], item.get('owners')
        require(isinstance(owners, dict) and set(owners) <= effects.OWNERS and
            all(effects.identifier(value) is not effects.MISSING for value in owners.values()), 'API_TARGET_OWNER_SCHEMA')
        for entity in sorted(effects.OWNERS):
            intent, owner = expected[number, entity], owners.get(entity)
            status = ('EXISTING_TARGET_OBSERVED' if owner and intent in ('reuse', 'update') else
                'CREATE_TARGET_ALREADY_REFERENCED' if owner else 'TARGET_EVIDENCE_REVIEW_REQUIRED')
            if owner:
                key = entity, str(owner)
                if key in physical and physical[key] != intent:
                    status = 'PHYSICAL_TARGET_INTENT_CONFLICT'
                physical[key] = intent
            findings.append({'row': number, 'entity': entity, 'intent': intent, 'status': status})
        for name, good in [('party_number', 'NUMBER_AND_SOURCE_OWNERS_MATCH'),
            ('site_number', 'NUMBER_AND_SOURCE_OWNERS_MATCH'), ('account_number', 'ACCOUNT_NUMBER_AND_SOURCE_OWNERS_MATCH')]:
            observed = item.get(name) or {}
            findings.append({'row': number, 'check': name, 'status': 'MATCH' if observed.get('status') == good
                             else 'NUMBER_TARGET_REVIEW_REQUIRED'})
        hierarchy = item.get('hierarchy') or {}
        observed = hierarchy.get('findings', [])
        for check in sorted(PARENTS):
            selected = [finding for finding in observed if finding.get('check') == check]
            status = 'MATCH' if len(selected) == 1 and selected[0].get('status') == 'MATCH' and hierarchy.get('collections_complete') is True else 'PARENT_TARGET_REVIEW_REQUIRED'
            findings.append({'row': number, 'check': check, 'status': status})
    consistent = all(f['status'] in ('MATCH', 'EXISTING_TARGET_OBSERVED') for f in findings)
    return {'schema_version': 'ar-customer-api-target-review-v1',
        'status': 'API_EXISTING_TARGET_INTENT_CONSISTENT' if consistent else 'API_TARGET_REVIEW_REQUIRED',
        'candidate_sha256': digest, 'environment_url': environment, 'operation_intent': operation,
        'collection_sha256': package.fingerprint(before), 'plan_sha256': package.fingerprint(plan),
        'findings': findings, 'target_intent_observations_consistent': consistent,
        'field_effects_reviewed': False, 'physical_creation_proven': False,
        'execution_authorized': False, 'live_ready': False,
        'limits': ['Existing API-visible targets only; absent/new or partial hierarchies require their separate target review, not a product prohibition.',
            'Recompute retained raw API captures and review completeness, provenance and freshness before use.',
            'Requested before-value differences do not invalidate matching identities; operation support and effects remain separate.']}
