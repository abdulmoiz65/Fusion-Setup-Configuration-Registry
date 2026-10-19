"""Compare scoped before/after evidence; never infer physical creation from a new reference."""
from datetime import datetime

import customers_package as package
import customer_identity_review as identity
import customer_ownership_review as ownership
import customer_value_review as values
import customer_receipt_review as receipts

require = package.require


def value_queries(snapshot, candidate_hash, environment, operation, identities, owners):
    require(isinstance(snapshot, dict) and set(snapshot) == {
        'schema_version', 'candidate_sha256', 'environment_url', 'operation_intent',
        'ownership_evidence_sha256', 'phase', 'captured_at', 'evidence_reference', 'queries'}, 'EFFECT_VALUES_SCHEMA')
    require(snapshot['schema_version'] == 'ar-customer-effect-values-v1', 'EFFECT_VALUES_VERSION')
    require(snapshot['candidate_sha256'] == candidate_hash and snapshot['environment_url'] == environment
            and snapshot['operation_intent'] == operation and snapshot['phase'] == owners['phase']
            and snapshot['ownership_evidence_sha256'] == package.fingerprint(owners), 'EFFECT_VALUES_BINDING')
    require(identity.text(snapshot['evidence_reference']), 'EFFECT_VALUES_PROVENANCE')
    try:
        captured = datetime.fromisoformat(snapshot['captured_at'].replace('Z', '+00:00'))
        owner_time = datetime.fromisoformat(owners['captured_at'].replace('Z', '+00:00'))
        require(captured.tzinfo is not None and captured >= owner_time, 'EFFECT_VALUES_CAPTURE_TIME')
    except (ValueError, TypeError, AttributeError) as exc:
        raise package.InvalidInput('EFFECT_VALUES_CAPTURE_TIME') from exc
    require(isinstance(snapshot['queries'], list), 'EFFECT_VALUES_QUERIES')
    allowed = {(q['entity'], q['owner_table_id']) for q in owners['queries']}
    queries = {}
    for query in snapshot['queries']:
        require(isinstance(query, dict) and set(query) == {'entity', 'owner_table_id', 'complete', 'records'}, 'EFFECT_VALUES_QUERY_SCHEMA')
        require(isinstance(query['entity'], str) and isinstance(query['owner_table_id'], str), 'EFFECT_VALUES_QUERY_ID')
        key = query['entity'], query['owner_table_id']
        require(key in allowed and key not in queries, 'EFFECT_VALUES_QUERY_SCOPE_OR_DUPLICATE')
        require(type(query['complete']) is bool and isinstance(query['records'], list), 'EFFECT_VALUES_QUERY_TYPE')
        fields = {column for entity, column in values.FIELDS.values() if entity == key[0]}
        for record in query['records']:
            require(isinstance(record, dict) and set(record) == fields, 'EFFECT_VALUES_COMPLETE_PROJECTION_REQUIRED')
            require(all(value is None or isinstance(value, str) for value in record.values()), 'EFFECT_VALUES_RECORD_TYPE')
        queries[key] = query
    return queries, captured


def resolved(identities, row, entity):
    sources = [q for q in identities['source_system_queries'] if q['source_name'] == row['ORIG_SOURCE_SYSTEM_NAME']]
    if len(sources) != 1 or not sources[0]['complete'] or len(sources[0]['records']) != 1:
        return 'unresolved', None
    key = identity.reference_candidates(row)[entity]
    source = sources[0]['records'][0]['orig_system']
    queries = [q for q in identities['reference_queries'] if
               (q['orig_system'], q['owner_table_name'], q['reference']) == (source, key['owner'], key['reference'])]
    if len(queries) != 1 or not queries[0]['complete'] or key['lexical_review_required']:
        return 'unresolved', None
    records = queries[0]['records']
    if not records:
        return 'absent_reference', None
    if len(records) != 1:
        return 'history_or_ambiguity', None
    record = records[0]
    midnight = datetime.fromisoformat(identities['as_of_date'] + 'T00:00:00')
    if record['status'] != 'A' or identity.oracle_date(record['start_date_active']) > midnight or (
            record['end_date_active'] is not None and identity.oracle_date(record['end_date_active']) < midnight):
        return 'inactive_or_out_of_date', None
    return 'one_active', record['owner_table_id']


def analyze(candidate, operation, environment, before_identity, before_owners,
            after_identity, after_owners, before_values, after_values, plan):
    before_result = ownership.analyze(candidate, operation, environment, before_identity, before_owners)
    after_result = ownership.analyze(candidate, operation, environment, after_identity, after_owners)
    require(before_owners['phase'] == 'before' and after_owners['phase'] == 'after', 'EFFECT_PHASES')
    digest = before_result['candidate_sha256']
    before, before_time = value_queries(before_values, digest, environment, operation, before_identity, before_owners)
    after, after_time = value_queries(after_values, digest, environment, operation, after_identity, after_owners)
    require(after_time > before_time and datetime.fromisoformat(after_identity['captured_at'].replace('Z', '+00:00')) > before_time,
            'EFFECT_CAPTURE_ORDER')
    require(identity.oracle_date(after_identity['as_of_date'] + 'T00:00:00') >=
            identity.oracle_date(before_identity['as_of_date'] + 'T00:00:00'), 'EFFECT_DATABASE_DATE_ORDER')
    require(isinstance(plan, dict) and set(plan) == {'schema_version', 'candidate_sha256', 'environment_url',
            'operation_intent', 'review_reference', 'expectations'}, 'EFFECT_PLAN_SCHEMA')
    require(plan['schema_version'] == 'ar-customer-effect-plan-v1' and plan['candidate_sha256'] == digest
            and plan['environment_url'] == environment and plan['operation_intent'] == operation, 'EFFECT_PLAN_BINDING')
    require(identity.text(plan['review_reference']) and isinstance(plan['expectations'], list), 'EFFECT_PLAN_REVIEW_REQUIRED')
    rows = [dict(zip(package.columns(), raw)) for raw in package.inspect_zip(candidate)]
    expected = {}
    shared = {}
    for entry in plan['expectations']:
        require(isinstance(entry, dict) and set(entry) == {'row', 'entity', 'intent'}, 'EFFECT_EXPECTATION_SCHEMA')
        require(type(entry['row']) is int and 1 <= entry['row'] <= len(rows)
                and isinstance(entry['entity'], str) and entry['entity'] in identity.ENTITIES
                and entry['intent'] in ('create', 'update', 'reuse'), 'EFFECT_EXPECTATION_VALUES')
        key = entry['row'], entry['entity']
        require(key not in expected, 'EFFECT_DUPLICATE_EXPECTATION')
        row = rows[entry['row'] - 1]
        ref = identity.reference_candidates(row)[entry['entity']]
        shared_key = row['ORIG_SOURCE_SYSTEM_NAME'], ref['owner'], ref['reference']
        require(shared_key not in shared or shared[shared_key] == entry['intent'], 'EFFECT_SHARED_TARGET_INTENT_CONFLICT')
        shared[shared_key] = entry['intent']
        expected[key] = entry['intent']
    require(set(expected) == {(i, entity) for i in range(1, len(rows) + 1) for entity in identity.ENTITIES}, 'EFFECT_PLAN_INCOMPLETE')
    owner_before = {(q['entity'], q['owner_table_id']): q for q in before_owners['queries']}
    owner_after = {(q['entity'], q['owner_table_id']): q for q in after_owners['queries']}
    findings = []
    for number, row in enumerate(rows, 1):
        for entity in identity.ENTITIES:
            intent = expected[number, entity]
            bs, bid = resolved(before_identity, row, entity)
            ats, aid = resolved(after_identity, row, entity)
            detail = {'row': number, 'entity': entity, 'intent': intent, 'before_reference': bs, 'after_reference': ats}
            source_records = [[q['records'] for q in evidence['source_system_queries']
                               if q['source_name'] == row['ORIG_SOURCE_SYSTEM_NAME']]
                              for evidence in (before_identity, after_identity)]
            if source_records[0] != source_records[1]:
                status = 'SOURCE_RESOLUTION_CHANGED_REVIEW_REQUIRED'
            elif bs == 'absent_reference' and ats == 'one_active':
                status = 'NEW_REFERENCE_OBSERVED_CREATION_UNPROVEN' if intent == 'create' else 'UNEXPECTED_REFERENCE_APPEARANCE'
            elif bs == 'one_active' and ats == 'absent_reference':
                status = 'REFERENCE_MISSING_AFTER_ENTITY_DELETION_UNPROVEN'
            elif bs != 'one_active' or ats != 'one_active':
                status = 'REFERENCE_EVIDENCE_INCOMPLETE_OR_AMBIGUOUS'
            elif bid != aid:
                status = 'REFERENCE_TARGET_REPLACED'
            elif intent == 'create':
                status = 'CREATE_INTENT_FOUND_EXISTING_REFERENCE'
            else:
                ob, oa = owner_before.get((entity, bid)), owner_after.get((entity, aid))
                qb, qa = before.get((entity, bid)), after.get((entity, aid))
                fields = {column for mapped_entity, column in values.FIELDS.values() if mapped_entity == entity}
                if any(not q or not q['complete'] or len(q['records']) != 1 for q in (ob, oa)):
                    status = 'OWNERSHIP_TARGET_EVIDENCE_INCOMPLETE'
                elif ob['records'][0] != oa['records'][0]:
                    status = 'RELATIONSHIP_CHANGED_REVIEW_REQUIRED'
                elif fields and any(not q or not q['complete'] or len(q['records']) != 1 for q in (qb, qa)):
                    status = 'VALUE_SNAPSHOT_MISSING_OR_AMBIGUOUS'
                else:
                    old = qb['records'][0] if fields else {}
                    new = qa['records'][0] if fields else {}
                    desired = {column: values.expected_value(field, row[field]) for field, (mapped_entity, column) in values.FIELDS.items()
                               if mapped_entity == entity and row[field]}
                    changed = sorted(field for field in fields if old[field] != new[field])
                    detail['changed_columns'] = changed
                    if any(new[field] != value for field, value in desired.items()):
                        status = 'REQUESTED_VALUE_NOT_OBSERVED'
                    elif intent == 'reuse' and changed:
                        status = 'UNEXPECTED_VALUE_CHANGE'
                    elif any(field not in desired for field in changed):
                        status = 'UNREQUESTED_VALUE_CHANGE_REVIEW_REQUIRED'
                    else:
                        status = 'REQUESTED_UPDATE_OBSERVED' if changed else 'UNCHANGED_WITH_REQUESTED_VALUES'
            findings.append({**detail, 'status': status})
    return {'schema_version': 'ar-customer-effect-review-v1', 'status': 'SCOPED_EFFECT_OBSERVATIONS',
        'candidate_sha256': digest, 'environment_url': environment, 'operation_intent': operation,
        'plan_sha256': package.fingerprint(plan),
        'before_values_sha256': package.fingerprint(before_values), 'after_values_sha256': package.fingerprint(after_values),
        'before_ownership_status': before_result['status'], 'after_ownership_status': after_result['status'],
        'compared_value_projection_fields': len(values.FIELDS),
        'findings': findings, 'creation_causality_verified': False, 'persisted_reconciliation_complete': False,
        'execution_authorized': False, 'journey_complete': False,
        'limits': ['New/missing references do not prove physical entity creation/deletion or attempt causality.',
                   'Only the complete selected-value projection and supplied ownership are compared; other fields, profile/receipt effects and concurrent changes remain separate.',
                   'Observed changes are compared to declared reviewed intent; this record is not approval or a claim of supported mutability.']}


def assignment_delta(before, after):
    """Inventory differences only; caller must bind snapshots to the campaign.

    Intentionally no candidate/attempt-success claim. Used for existing-account
    before/after queries; a new account needs a separately proven baseline.
    """
    fields = {'cust_receipt_method_id', 'customer_id', 'receipt_method_id', 'site_use_id',
              'primary_flag', 'start_date', 'end_date', 'request_id'}
    for query in (before, after):
        require(isinstance(query, dict) and set(query) == {'customer_id', 'complete', 'records'}
                and ownership.identifier(query['customer_id']) and type(query['complete']) is bool
                and isinstance(query['records'], list), 'RECEIPT_DELTA_QUERY_SCHEMA')
        for record in query['records']:
            require(isinstance(record, dict) and set(record) == fields, 'RECEIPT_DELTA_RECORD_SCHEMA')
            receipts.validate_assignment(query['customer_id'], record)
    require(before['customer_id'] == after['customer_id'], 'RECEIPT_DELTA_ACCOUNT_MISMATCH')
    ambiguous = any(len({r['cust_receipt_method_id'] for r in q['records']}) != len(q['records']) for q in (before, after))
    result = {'schema_version': 'ar-receipt-inventory-delta-v1', 'status': 'INCOMPLETE_OR_DUPLICATE_INVENTORY',
              'before_sha256': package.fingerprint(before), 'after_sha256': package.fingerprint(after),
              'attempt_causality_verified': False, 'expected_effects_verified': False}
    if not before['complete'] or not after['complete'] or ambiguous:
        return result
    old = {r['cust_receipt_method_id']: r for r in before['records']}
    new = {r['cust_receipt_method_id']: r for r in after['records']}
    changed = [sorted(field for field in fields if old[key][field] != new[key][field])
               for key in sorted(old.keys() & new.keys()) if old[key] != new[key]]
    return {**result, 'status': 'SCOPED_INVENTORY_DELTA', 'added_count': len(new.keys() - old.keys()),
            'removed_count': len(old.keys() - new.keys()), 'changed_count': len(changed),
            'unchanged_count': len(old.keys() & new.keys()) - len(changed), 'changed_columns': changed}
