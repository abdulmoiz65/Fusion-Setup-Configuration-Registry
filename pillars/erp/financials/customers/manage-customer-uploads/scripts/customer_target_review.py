"""Classify supplied before-state targets against explicit create/update/reuse intent."""
from datetime import datetime

import customers_package as package
import customer_identity_review as identity
import customer_ownership_review as ownership

require = package.require
NUMBER_FIELDS = {'PARTY_NUMBER': 'party', 'ACCOUNT_NUMBER': 'account', 'PARTY_SITE_NUMBER': 'party_site'}


def analyze(candidate, operation, environment, identities, owners, plan):
    identity_result = identity.analyze(candidate, operation, environment, identities)
    owner_result = ownership.analyze(candidate, operation, environment, identities, owners)
    require(owners['phase'] == 'before', 'TARGET_BEFORE_PHASE_REQUIRED')
    require(isinstance(plan, dict) and set(plan) == {
        'schema_version','candidate_sha256','environment_url','operation_intent',
        'identity_evidence_sha256','ownership_evidence_sha256','captured_at',
        'review_reference','expectations','number_queries'}, 'TARGET_PLAN_SCHEMA')
    require(plan['schema_version'] == 'ar-customer-target-plan-v1', 'TARGET_PLAN_VERSION')
    require(plan['candidate_sha256'] == identity_result['candidate_sha256']
            and plan['environment_url'] == environment and plan['operation_intent'] == operation
            and plan['identity_evidence_sha256'] == package.fingerprint(identities)
            and plan['ownership_evidence_sha256'] == package.fingerprint(owners), 'TARGET_PLAN_BINDING')
    require(identity.text(plan['review_reference']), 'TARGET_REVIEW_REFERENCE')
    try:
        capture = datetime.fromisoformat(plan['captured_at'].replace('Z','+00:00'))
        owner_time = datetime.fromisoformat(owners['captured_at'].replace('Z','+00:00'))
        require(capture.tzinfo is not None and capture >= owner_time, 'TARGET_CAPTURE_ORDER')
    except (AttributeError, TypeError, ValueError) as exc:
        raise package.InvalidInput('TARGET_CAPTURE_ORDER') from exc
    rows = [dict(zip(package.columns(), row)) for row in package.inspect_zip(candidate)]
    require(isinstance(plan['expectations'], list), 'TARGET_EXPECTATIONS_REQUIRED')
    expected, shared = {}, {}
    for entry in plan['expectations']:
        require(isinstance(entry, dict) and set(entry) == {'row','entity','intent'}, 'TARGET_EXPECTATION_SCHEMA')
        row, entity, intent = entry['row'], entry['entity'], entry['intent']
        require(type(row) is int and 1 <= row <= len(rows) and isinstance(entity, str)
                and entity in identity.ENTITIES and intent in ('create','update','reuse'), 'TARGET_EXPECTATION_VALUES')
        require((row,entity) not in expected, 'TARGET_DUPLICATE_EXPECTATION')
        expected[row,entity] = intent
        key = identity.reference_candidates(rows[row-1])[entity]
        shared_key = rows[row-1]['ORIG_SOURCE_SYSTEM_NAME'], key['owner'], key['reference']
        require(shared_key not in shared or shared[shared_key] == intent, 'TARGET_SHARED_INTENT_CONFLICT')
        shared[shared_key] = intent
    require(set(expected) == {(n, entity) for n in range(1,len(rows)+1) for entity in identity.ENTITIES},
            'TARGET_EXPECTATIONS_INCOMPLETE')
    require(isinstance(plan['number_queries'], list), 'TARGET_NUMBER_QUERIES_REQUIRED')
    scope = {(field, row[field]) for row in rows for field in NUMBER_FIELDS if row[field]}
    numbers = {}
    for query in plan['number_queries']:
        require(isinstance(query, dict) and set(query) == {'field','value','complete','records'}, 'TARGET_NUMBER_QUERY_SCHEMA')
        require(isinstance(query['field'], str) and isinstance(query['value'], str), 'TARGET_NUMBER_QUERY_KEY')
        key = query['field'], query['value']
        require(key in scope and key not in numbers, 'TARGET_NUMBER_QUERY_SCOPE')
        require(type(query['complete']) is bool and isinstance(query['records'], list), 'TARGET_NUMBER_QUERY_VALUES')
        for record in query['records']:
            require(isinstance(record, dict) and set(record) == {'owner_table_id'}
                    and ownership.identifier(record['owner_table_id']), 'TARGET_NUMBER_RECORD')
        numbers[key] = query

    refs = {(q['orig_system'],q['owner_table_name'],q['reference']):q for q in identities['reference_queries']}
    sources = {q['source_name']:q for q in identities['source_system_queries']}
    identity_findings = {(f['row'],f['entity']):f for f in identity_result['findings']}
    owner_findings = {(f['row'],f['check']):f for f in owner_result['findings']}
    findings, actual_intents = [], {}
    for n, row in enumerate(rows,1):
        for entity in identity.ENTITIES:
            intent = expected[n,entity]
            observed = identity_findings[n,entity]['status']
            record_id = None
            if observed == 'ONE_ACTIVE_REFERENCE_OBSERVED':
                key = identity.reference_candidates(row)[entity]
                source = sources[row['ORIG_SOURCE_SYSTEM_NAME']]['records'][0]['orig_system']
                records = refs[source,key['owner'],key['reference']]['records']
                if len(records) == 1:
                    record_id = records[0]['owner_table_id']
            if intent == 'create':
                status = ('NEW_REFERENCE_TARGET_PROPOSED' if observed == 'NO_REFERENCE_OBSERVED_NOT_CREATE_AUTHORITY'
                          else 'CREATE_TARGET_ALREADY_REFERENCED' if record_id else 'TARGET_IDENTITY_UNRESOLVED')
            elif record_id and owner_findings[n,entity]['status'] == 'TARGET_ROW_OBSERVED':
                status = 'EXISTING_TARGET_OBSERVED'
            else:
                status = 'UPDATE_OR_REUSE_TARGET_UNRESOLVED'
            if record_id:
                physical_key = entity, record_id
                if physical_key in actual_intents and actual_intents[physical_key] != intent:
                    status = 'PHYSICAL_TARGET_INTENT_CONFLICT'
                actual_intents[physical_key] = intent
            findings.append({'row':n,'entity':entity,'intent':intent,'status':status})
            for field, mapped in NUMBER_FIELDS.items():
                if mapped != entity or not row[field]:
                    continue
                query = numbers.get((field,row[field]))
                if not query or not query['complete']:
                    ns = 'NUMBER_QUERY_MISSING_OR_INCOMPLETE'
                elif intent == 'create':
                    ns = 'NUMBER_ABSENT_OBSERVED' if not query['records'] else 'NUMBER_COLLISION'
                else:
                    ns = ('NUMBER_TARGET_MATCH' if record_id and len(query['records']) == 1
                          and query['records'][0]['owner_table_id'] == record_id else 'NUMBER_TARGET_REVIEW_REQUIRED')
                findings.append({'row':n,'entity':entity,'field':field,'status':ns})
        for name, child, _, parent, _ in ownership.LINKS:
            child_new, parent_new = expected[n,child] == 'create', expected[n,parent] == 'create'
            if not child_new:
                status = ('EXISTING_CHILD_NEW_PARENT_REVIEW_REQUIRED' if parent_new else owner_findings[n,name]['status'])
                findings.append({'row':n,'check':name,'status':status})
        for entity, purpose in (('account_site_use','site_use_purpose'),('party_site_use','party_site_use_purpose')):
            if expected[n,entity] != 'create':
                findings.append({'row':n,'check':purpose,'status':owner_findings[n,purpose]['status']})
    good = {'NEW_REFERENCE_TARGET_PROPOSED','EXISTING_TARGET_OBSERVED','NUMBER_ABSENT_OBSERVED','NUMBER_TARGET_MATCH','MATCH'}
    consistent = bool(findings) and all(f['status'] in good for f in findings)
    return {'schema_version':'ar-customer-target-review-v1',
        'status':'TARGET_INTENT_OBSERVATIONS_CONSISTENT' if consistent else 'TARGET_REVIEW_REQUIRED',
        'candidate_sha256':identity_result['candidate_sha256'],'environment_url':environment,
        'operation_intent':operation,'plan_sha256':package.fingerprint(plan),
        'findings':findings,'target_intent_observations_consistent':consistent,
        'field_effects_reviewed':False,'physical_creation_proven':False,
        'execution_authorized':False,'live_ready':False,
        'limits':['Absent references and numbers are point-in-time observations, not proof of global absence or reservation.',
            'Existing-target values, specialized defaults and full requested effects need separate before-state review.',
            'Publisher evidence needs reviewed scope, provenance, completeness and freshness; the helper does not authenticate it.',
            'No source reference or number is changed, no parent is silently reassigned, and no import is authorized.']}
