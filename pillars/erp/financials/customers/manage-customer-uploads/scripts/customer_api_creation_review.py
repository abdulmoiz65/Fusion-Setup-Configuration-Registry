"""Project scoped entity creation times from supported SOAP responses, no I/O."""
from datetime import datetime
import re

import customers_package as package
import customer_api_business_values as values
from customer_api_profile_set_review import result,scalar
from customer_api_hierarchy import ACCOUNT,TYPES,MISSING,identifier

LOCATION='http://xmlns.oracle.com/apps/cdm/foundation/parties/locationService/'
OWNERS={'party','account','location','party_site','party_site_use','account_site','account_site_use'}


def timestamp(value):
    if not isinstance(value,str) or not re.fullmatch(
            r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,9})?(?:Z|[+-]\d{2}:\d{2})',value):
        return None
    try:return datetime.fromisoformat(value.replace('Z','+00:00'))
    except ValueError:return None


def project(row,owners,organization_xml,account_xml,location_xml):
    """Retain each exact physical owner's timestamp; child/profile dates differ."""
    require=package.require
    require(isinstance(owners,dict) and set(owners)==OWNERS and all(
        identifier(v) is not MISSING for v in owners.values()),'API_CREATION_OWNERS_REQUIRED')
    owners={k:str(v) for k,v in owners.items()}
    # Reuse strict operation/result/number/parent validation before extracting dates.
    values.organization_values(row,owners,organization_xml)
    values.account_values(row,owners,account_xml)
    org=result(organization_xml,values.ORG_TYPES,'findOrganizationResponse')
    party=org.find('{'+values.ORG+'}Value')
    party_site=values.select(party,values.ORG,'PartySite',values.PARTY,'PartySiteId',owners['party_site'])
    party_use=values.select(party_site,values.PARTY,'PartySiteUse',values.PARTY,'PartySiteUseId',owners['party_site_use'])
    account=result(account_xml,TYPES,'getCustomerAccountResponse')
    account_site=values.select(account,ACCOUNT,'CustomerAccountSite',ACCOUNT,'CustomerAccountSiteId',owners['account_site'])
    account_use=values.select(account_site,ACCOUNT,'CustomerAccountSiteUse',ACCOUNT,'SiteUseId',owners['account_site_use'])
    location=result(location_xml,LOCATION+'applicationModule/types/','getLocationResponse')
    require(identifier(scalar(location,LOCATION,'LocationId'))==owners['location'],'API_CREATION_LOCATION_SCOPE')
    require(all(n is not None for n in (party_site,party_use,account_site,account_use)), 'API_CREATION_CHILD_NOT_RETURNED')
    require(scalar(account,ACCOUNT,'AccountNumber')==row['ACCOUNT_NUMBER']
        and scalar(party_site,values.PARTY,'PartySiteNumber')==row['PARTY_SITE_NUMBER'],'API_CREATION_NUMBER_SCOPE')
    require(scalar(party_use,values.PARTY,'SiteUseType')==row['SITE_USE_CODE']
        and scalar(account_use,ACCOUNT,'SiteUseCode')==row['SITE_USE_CODE'],'API_CREATION_PURPOSE_SCOPE')
    groups={'party':(party,values.ORG),'party_site':(party_site,values.PARTY),
        'party_site_use':(party_use,values.PARTY),'account':(account,ACCOUNT),
        'account_site':(account_site,ACCOUNT),'account_site_use':(account_use,ACCOUNT),'location':(location,LOCATION)}
    observations={}
    for entity,(node,namespace) in groups.items():
        raw=scalar(node,namespace,'CreationDate')
        observations[entity]={'owner_id':owners[entity],
            'status':'TIMESTAMP_OBSERVED' if timestamp(raw) else 'TIMESTAMP_UNAVAILABLE_OR_INVALID',
            'creation_date':raw if timestamp(raw) else None}
    return {'schema_version':'ar-customer-api-creation-observation-v1','owners':owners,
        'observations':observations,'all_creation_times_observed':all(
            v['status']=='TIMESTAMP_OBSERVED' for v in observations.values()),
        'global_absence_proven':False,'attempt_causality_proven':False,'execution_authorized':False}


def review_window(projection,intents,window_start,window_end):
    """Compare audit timestamps with a caller-reviewed attempt interval.

    This cannot prove which actor/request created an entity, global prior absence,
    or ownership. Those require separate source/number/parent and attempt checks.
    """
    require=package.require
    require(isinstance(projection,dict) and projection.get('schema_version')=='ar-customer-api-creation-observation-v1'
        and isinstance(projection.get('owners'),dict) and set(projection['owners'])==OWNERS
        and isinstance(projection.get('observations'),dict) and set(projection['observations'])==OWNERS,'API_CREATION_PROJECTION')
    require(isinstance(intents,dict) and set(intents)==OWNERS and all(
        v in ('create','update','reuse') for v in intents.values()),'API_CREATION_INTENTS')
    start,end=timestamp(window_start),timestamp(window_end)
    require(start is not None and end is not None and start<end,'API_CREATION_WINDOW')
    findings=[]
    for entity in sorted(OWNERS):
        observation=projection['observations'][entity]
        require(isinstance(observation,dict) and observation.get('owner_id')==projection['owners'][entity]
            and identifier(observation.get('owner_id')) is not MISSING,'API_CREATION_OWNER_BINDING')
        date=timestamp(observation.get('creation_date'))
        if observation.get('status')!='TIMESTAMP_OBSERVED' or date is None:status='CREATION_TIME_UNRESOLVED'
        elif date>end:status='CREATION_TIME_AFTER_OBSERVATION'
        elif intents[entity]=='create':status='CREATED_WITHIN_WINDOW' if start<=date else 'TARGET_PREDATES_CREATE_WINDOW'
        else:status='TARGET_PREDATES_WINDOW' if date<start else 'REUSED_TARGET_APPEARS_NEW'
        findings.append({'entity':entity,'intent':intents[entity],'status':status})
    return {'schema_version':'ar-customer-api-creation-window-review-v1','projection_sha256':package.fingerprint(projection),
        'intents':intents,'window_start':window_start,'window_end':window_end,'findings':findings,
        'creation_time_expectations_match':all(f['status'] in ('CREATED_WITHIN_WINDOW','TARGET_PREDATES_WINDOW') for f in findings),
        'attempt_causality_proven':False,'persisted_value_outcome_verified':False,'execution_authorized':False,
        'limits':['Audit time corroborates create/reuse intent only after exact owner and attempt association.',
            'Missing audit values and timestamp/clock contradictions remain unresolved.',
            'No global absence, concurrency exclusion, field-value or import-permission inference.']}
