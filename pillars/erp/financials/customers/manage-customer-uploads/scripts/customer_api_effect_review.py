"""Compare bound API before/after observations without fabricating missing values."""
from datetime import datetime
from pathlib import Path
import argparse
import hashlib
import json

import customers_package as package
import customer_api_business_values as business
import customer_api_location_review as locations
import customer_api_dff_review as dff
from customer_api_hierarchy import MISSING, identifier
from customer_value_review import FIELDS

PROJECTIONS = {
    'account_values': set(business.ACCOUNT_FIELDS)|set(business.ACCOUNT_SITE_FIELDS)|set(business.USE_FIELDS),
    'organization_values': set(business.PARTY_FIELDS)|set(business.SITE_FIELDS),
    'location': set(locations.FIELDS), 'dff':set(dff.FIELDS),
    'profile_set': {'ACCT_ADDRESS_SET_CODE','CUSTOMER_PROFILE_CLASS'},
}
ENTITY = {field: entity for field,(entity,_) in FIELDS.items()}
ENTITY.update(ACCT_ADDRESS_SET_CODE='account_site',CUSTOMER_PROFILE_CLASS='account')
OWNERS = {'party','account','location','party_site','party_site_use','account_site','account_site_use'}


def timestamp(value):
    try:
        result=datetime.fromisoformat(value.replace('Z','+00:00'))
        package.require(result.tzinfo is not None,'API_EFFECT_TIMEZONE_REQUIRED')
        return result
    except (ValueError,TypeError,AttributeError) as exc:
        raise package.InvalidInput('API_EFFECT_CAPTURE_TIME') from exc


def retained_collection(directory):
    """Read a private collector directory and verify retained capture bindings.

    Hash agreement establishes artifact consistency, not server signatures or
    authenticated authorship. Caller still reviews origin and freshness.
    """
    directory=Path(directory).resolve()
    load=lambda name: package.load_json(directory/name)
    binding=load('binding.json')
    report=load('collection-review.json')
    package.require(isinstance(binding,dict) and isinstance(report,dict) and
        all(report.get(k)==v for k,v in binding.items()),'API_EFFECT_BINDING_MISMATCH')
    captures=report.get('captures')
    package.require(isinstance(captures,list) and type(report.get('capture_count')) is int and
        report['capture_count']==len(captures),'API_EFFECT_CAPTURE_COUNT')
    seen=set()
    for capture in captures:
        package.require(isinstance(capture,dict) and isinstance(capture.get('response_file'),str),
                        'API_EFFECT_CAPTURE_SCHEMA')
        name=capture['response_file']
        path=(directory/name).resolve()
        package.require(path.parent==directory and name not in seen,'API_EFFECT_CAPTURE_PATH')
        seen.add(name)
        package.require(capture.get('binding_sha256')==package.fingerprint(binding) and
            hashlib.sha256(path.read_bytes()).hexdigest()==capture.get('response_sha256') and
            load(name+'.capture.json')==capture,'API_EFFECT_CAPTURE_INTEGRITY')
        package.require(timestamp(binding['started_at'])<=timestamp(capture['captured_at'])<=
            timestamp(report['finished_at']),'API_EFFECT_CAPTURE_ORDER')
    return report


def observations(item):
    values,metadata={},{}
    for name,fields in PROJECTIONS.items():
        projection=item.get(name)
        if projection is None:
            continue
        package.require(isinstance(projection,dict),'API_EFFECT_PROJECTION_SCHEMA')
        observed=projection.get('observed_values',{})
        package.require(isinstance(observed,dict) and set(observed)<=fields and
            all(v is None or isinstance(v,str) for v in observed.values()),'API_EFFECT_PROJECTED_VALUES')
        package.require(not set(values)&set(observed),'API_EFFECT_DUPLICATE_FIELD_PROJECTION')
        values.update(observed)
        extra=projection.get('observed_metadata',{})
        package.require(isinstance(extra,dict) and all(isinstance(k,str) and
            (v is None or isinstance(v,str)) for k,v in extra.items()),'API_EFFECT_METADATA_VALUES')
        metadata.update({name+'.'+k:v for k,v in extra.items()})
    return values,metadata


def compare(candidate, operation, environment, before, after):
    """Return visible changes and gaps, never permission or complete reconciliation."""
    digest=package.inspect_candidate(candidate,operation)['candidate_sha256']
    rows=[dict(zip(package.columns(),r)) for r in package.inspect_zip(candidate)]
    for phase,report in (('before',before),('after',after)):
        package.require(isinstance(report,dict) and report.get('schema_version')=='ar-customer-api-collection-v1',
                        'API_EFFECT_COLLECTION_VERSION')
        package.require(report.get('candidate_sha256')==digest and report.get('operation_intent')==operation and
            report.get('environment_url')==environment and report.get('phase')==phase,'API_EFFECT_COLLECTION_BINDING')
        package.require(report.get('read_only') is True and report.get('sql_input_used') is False and
            report.get('status')=='API_OBSERVATIONS_CAPTURED_WITH_LIMITATIONS','API_EFFECT_COLLECTION_STATUS')
        package.require(timestamp(report['started_at'])<=timestamp(report['finished_at']),'API_EFFECT_CAPTURE_ORDER')
        package.require(isinstance(report.get('rows'),list) and len(report['rows'])==len(rows) and
            all(isinstance(r,dict) for r in report['rows']) and
            [r.get('row') for r in report['rows']]==list(range(1,len(rows)+1)),'API_EFFECT_ROW_BINDING')
        for item in report['rows']:
            package.require(isinstance(item.get('owners'),dict) and set(item['owners'])<=OWNERS and
                all(identifier(v) is not MISSING for v in item['owners'].values()),'API_EFFECT_OWNERS')
    package.require(timestamp(before['finished_at'])<timestamp(after['started_at']),'API_EFFECT_PHASE_ORDER')
    results=[]
    all_fields=set().union(*PROJECTIONS.values())
    for row,b,a in zip(rows,before['rows'],after['rows']):
        old,old_meta=observations(b)
        new,new_meta=observations(a)
        findings=[]
        identities=[]
        for entity in sorted(OWNERS):
            prior=b['owners'].get(entity);current=a['owners'].get(entity)
            status=('UNRESOLVED_BOTH_PHASES' if not prior and not current else
                'NEW_VISIBLE_REFERENCE_CREATION_UNPROVEN' if not prior else
                'REFERENCE_UNRESOLVED_AFTER' if not current else
                'SAME_REFERENCE_OWNER' if str(prior)==str(current) else 'REFERENCE_OWNER_CHANGED')
            identities.append({'entity':entity,'status':status})
        for field in sorted(all_fields):
            entity=ENTITY[field]
            prior=b['owners'].get(entity);current=a['owners'].get(entity)
            same=bool(prior and current and str(prior)==str(current))
            expected=row[field]
            if expected and field=='ACCOUNT_ESTABLISHED_DATE':
                expected=datetime.strptime(expected,'%Y/%m/%d').date().isoformat()
            after_check=('OWNER_NOT_RESOLVED' if not current else 'VALUE_NOT_RETURNED' if field not in new else 'OMITTED_INPUT_OBSERVATION_ONLY'
                if not row[field] else 'MATCH' if new[field]==expected else 'MISMATCH')
            change=('OWNER_NOT_RESOLVED' if not current else 'OWNER_NOT_COMPARABLE' if not same else
                'VALUE_NOT_RETURNED' if field not in old or field not in new else
                'UNCHANGED' if old[field]==new[field] else 'REQUESTED_VALUE_CHANGE'
                if row[field] else 'OMITTED_INPUT_VALUE_CHANGED_REVIEW_REQUIRED')
            findings.append({'field':field,'entity':entity,'after_value':after_check,'change':change})
        metadata=[]
        owners_same=b['owners']==a['owners'] and set(b['owners'])==OWNERS
        for key in sorted(set(old_meta)|set(new_meta)):
            status=('OWNERS_NOT_COMPARABLE' if not owners_same else 'METADATA_NOT_RETURNED'
                if key not in old_meta or key not in new_meta else 'UNCHANGED'
                if old_meta[key]==new_meta[key] else 'OBSERVED_METADATA_CHANGE_REVIEW_REQUIRED')
            metadata.append({'field':key,'status':status})
        results.append({'row':a['row'],'identities':identities,'values':findings,'metadata':metadata,
            'requested_fields_outside_projection':sorted(k for k,v in row.items() if v and k not in all_fields),
            'requested_after_mismatches':sum(f['after_value']=='MISMATCH' for f in findings),
            'omitted_value_changes':sum(f['change']=='OMITTED_INPUT_VALUE_CHANGED_REVIEW_REQUIRED' for f in findings)})
    return {'schema_version':'ar-customer-api-effect-review-v1','status':'SCOPED_API_BEFORE_AFTER_OBSERVATIONS',
        'candidate_sha256':digest,'environment_url':environment,'operation_intent':operation,
        'before_collection_sha256':package.fingerprint(before),'after_collection_sha256':package.fingerprint(after),
        'projected_field_count':len(all_fields),'rows':results,'sql_input_used':False,
        'execution_authorized':False,'persisted_reconciliation_complete':False,
        'attempt_causality_verified':False,'journey_complete':False,
        'limits':['API-visible observations only; missing fields are not nulls or preservation evidence.',
            'Same owner IDs allow value comparison, not proof this import caused a change.',
            'New references do not prove physical creation; changed/unresolved owners are not compared as one entity.',
            'Full profile history, unexposed DFFs, complete sibling inventories, receipt/tax effects and attempt lineage remain separate.',
            'Artifact hashes and ordering do not prove authentic server origin, current freshness or a transactionally consistent snapshot.']}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate',type=Path,required=True)
    parser.add_argument('--operation',choices=['create','update','mixed'],required=True)
    parser.add_argument('--environment-url',required=True)
    parser.add_argument('--before',type=Path,required=True)
    parser.add_argument('--after',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args(argv)
    try:
        report=compare(args.candidate.read_bytes(),args.operation,args.environment_url,
                       retained_collection(args.before),retained_collection(args.after))
        with args.output.open('x',encoding='utf-8') as stream:
            json.dump(report,stream,indent=2);stream.write('\n')
        print(json.dumps({'status':report['status'],'rows':len(report['rows']),
            'projected_field_count':report['projected_field_count'],'persisted_reconciliation_complete':False}))
        return 0
    except Exception as exc:
        print(json.dumps({'status':'API_EFFECT_REVIEW_INCOMPLETE','error_type':type(exc).__name__,
                          'execution_authorized':False}))
        return 2


if __name__=='__main__':
    raise SystemExit(main())
