"""Review visible conflicts for explicit new logical targets; never prove absence."""
import customers_package as package
import customer_api_snapshot as snapshot
import customer_api_effect_review as effects


def analyze(candidate,operation,environment,before,reference_plan,reference_observations,intent_plan):
    require=package.require
    digest=package.inspect_candidate(candidate,operation)['candidate_sha256']
    rows=package.inspect_zip(candidate)
    require(isinstance(before,dict) and before.get('schema_version')=='ar-customer-api-collection-v1'
        and before.get('candidate_sha256')==digest and before.get('operation_intent')==operation
        and before.get('environment_url')==environment and before.get('phase')=='before'
        and before.get('read_only') is True and before.get('sql_input_used') is False
        and before.get('status')=='API_OBSERVATIONS_CAPTURED_WITH_LIMITATIONS','NEW_TARGET_COLLECTION_BINDING')
    require(effects.timestamp(before['started_at'])<=effects.timestamp(before['finished_at']),'NEW_TARGET_CAPTURE_ORDER')
    require(isinstance(before.get('rows'),list) and len(before['rows'])==len(rows)
        and [r.get('row') for r in before['rows']]==list(range(1,len(rows)+1)),'NEW_TARGET_ROW_BINDING')
    require(isinstance(reference_plan,dict) and reference_plan.get('candidate_sha256')==digest
        and reference_plan.get('environment_url')==environment and reference_plan.get('operation_intent')==operation,
        'NEW_TARGET_REFERENCE_BINDING')
    require(isinstance(reference_plan.get('row_scopes'),list) and len(reference_plan['row_scopes'])==len(rows)
        and isinstance(reference_plan.get('queries'),dict),'NEW_TARGET_REFERENCE_SCHEMA')
    source_codes={}
    for row,scope in zip(rows,reference_plan['row_scopes']):
        require(isinstance(scope,dict) and isinstance(scope.get('entities'),dict)
            and set(scope['entities'])==effects.OWNERS,'NEW_TARGET_LOGICAL_IDENTITIES_REQUIRED')
        source_name=dict(zip(package.columns(),row))['ORIG_SOURCE_SYSTEM_NAME']
        for query_id in scope['entities'].values():
            query=reference_plan['queries'].get(query_id)
            require(isinstance(query,dict) and isinstance(query.get('scope'),dict),'NEW_TARGET_REFERENCE_SCHEMA')
            code=query['scope'].get('SourceSystem')
            require(isinstance(code,str) and code.strip() and source_codes.get(source_name,code)==code,'NEW_TARGET_SOURCE_MAP')
            source_codes[source_name]=code
    require(package.fingerprint(snapshot.plan(candidate,operation,environment,source_codes))==package.fingerprint(reference_plan),
        'NEW_TARGET_PLAN_NOT_CANONICAL')
    resolved=snapshot.review(reference_plan,reference_observations)
    require(package.fingerprint(resolved)==before.get('reference_review_sha256'),'NEW_TARGET_REFERENCE_CHANGED')
    require(isinstance(intent_plan,dict) and set(intent_plan)=={'schema_version','candidate_sha256','environment_url',
        'operation_intent','collection_sha256','authority_reference','expectations'}
        and intent_plan['schema_version']=='ar-customer-api-new-target-plan-v1'
        and intent_plan['candidate_sha256']==digest and intent_plan['environment_url']==environment
        and intent_plan['operation_intent']==operation and intent_plan['collection_sha256']==package.fingerprint(before)
        and isinstance(intent_plan['authority_reference'],str) and intent_plan['authority_reference'].strip(),
        'NEW_TARGET_INTENT_BINDING')
    require(isinstance(intent_plan['expectations'],list) and len(intent_plan['expectations'])==len(rows), 'NEW_TARGET_EXPECTATIONS')
    require([r.get('row') for r in reference_plan['row_scopes']]==list(range(1,len(rows)+1)),'NEW_TARGET_SCOPE_ROWS')
    findings=[]
    if reference_plan['unresolved']:findings.append({'check':'reference_mapping','status':'MAPPING_UNRESOLVED'})
    logical_intents={}
    for number,(current,scope,resolution,expected) in enumerate(zip(before['rows'],reference_plan['row_scopes'],resolved['rows'],intent_plan['expectations']),1):
        require(isinstance(expected,dict) and set(expected)=={'row','entities'} and type(expected['row']) is int and expected['row']==number
            and isinstance(expected['entities'],dict) and set(expected['entities'])==effects.OWNERS
            and all(i in ('create','reuse','update') for i in expected['entities'].values()),'NEW_TARGET_ENTITY_INTENTS')
        require(current.get('owners')==resolution['owners'],'NEW_TARGET_OWNER_PROJECTION')
        intents=expected['entities']
        existing={e for e,i in intents.items() if i!='create'}
        supported=existing in (set(),{'party','account'})
        findings.append({'row':number,'check':'composition','status':'SUPPORTED_REVIEW_SHAPE' if supported else 'SEPARATE_COMPOSITION_REVIEW_REQUIRED'})
        require(set(scope['entities'])==effects.OWNERS,'NEW_TARGET_LOGICAL_IDENTITIES_REQUIRED')
        for entity,query_id in scope['entities'].items():
            observed=resolved['findings'][query_id]['status']
            logical=(entity,package.fingerprint(reference_plan['queries'][query_id]['scope']))
            status=('NO_VISIBLE_CONFLICT' if intents[entity]=='create' and observed=='NO_VISIBLE_REFERENCE_NOT_GLOBAL_ABSENCE'
                else 'EXISTING_OWNER_RESOLVED' if intents[entity]!='create' and observed=='API_VISIBLE_OWNER_RESOLVED'
                else 'TARGET_CONFLICT_OR_UNRESOLVED')
            if logical in logical_intents and logical_intents[logical]!=intents[entity]:status='SHARED_LOGICAL_INTENT_CONFLICT'
            logical_intents[logical]=intents[entity]
            findings.append({'row':number,'entity':entity,'intent':intents[entity],'status':status})
        for name,entity,missing,matched in (
            ('party_number','party','NO_VISIBLE_ORGANIZATION_NUMBER_NOT_GLOBAL_ABSENCE','NUMBER_AND_SOURCE_OWNERS_MATCH'),
            ('site_number','party_site','NO_VISIBLE_ORGANIZATION_NUMBER_NOT_GLOBAL_ABSENCE','NUMBER_AND_SOURCE_OWNERS_MATCH'),
            ('account_number','account','NO_VISIBLE_ACCOUNT_NUMBER_NOT_GLOBAL_ABSENCE','ACCOUNT_NUMBER_AND_SOURCE_OWNERS_MATCH')):
            value=current.get(name) or {}
            wanted=missing if intents[entity]=='create' else matched
            findings.append({'row':number,'check':name,'status':'NUMBER_PRECHECK_MATCH' if value.get('status')==wanted else 'NUMBER_REVIEW_REQUIRED'})
        if existing=={'party','account'}:
            # These components validate the exact account/party parent and number
            # from the retained raw SOAP response; caller must replay that raw data.
            input_row=dict(zip(package.columns(),rows[number-1]))
            parent_observed=True
            for component,field in (('account_values','ACCOUNT_NUMBER'),('organization_values','PARTY_NUMBER')):
                value=current.get(component)
                parent_observed=parent_observed and isinstance(value,dict) and value.get('schema_version')=='ar-customer-api-business-values-v1' and (
                    isinstance(value.get('observed_values'),dict) and value['observed_values'].get(field)==input_row[field])
            findings.append({'row':number,'check':'existing_parent_response','status':'PARENTS_OBSERVED' if parent_observed else 'PARENT_REVIEW_REQUIRED'})
    good={'SUPPORTED_REVIEW_SHAPE','NO_VISIBLE_CONFLICT','EXISTING_OWNER_RESOLVED','NUMBER_PRECHECK_MATCH','PARENTS_OBSERVED'}
    return {'schema_version':'ar-customer-api-new-target-review-v1','candidate_sha256':digest,
        'collection_sha256':package.fingerprint(before),'intent_plan_sha256':package.fingerprint(intent_plan),
        'findings':findings,'scoped_prechecks_satisfied':all(f['status'] in good for f in findings),
        'global_absence_proven':False,'business_ownership_authority_verified':False,
        'creation_proven':False,'execution_authorized':False,
        'limits':['No visible conflict is distinct from global absence and grants no permission to create.',
            'Review actual business authority over exact source keys and supplied numbers separately; an authority-reference string is not approval.',
            'Caller must replay authenticated raw captures and inspect visibility, freshness and concurrency risks.',
            'After execution require matching source/number/parent owners, audit creation times and requested values/effects.',
            'Other entity compositions need their separate review; this is not a product prohibition.']}
