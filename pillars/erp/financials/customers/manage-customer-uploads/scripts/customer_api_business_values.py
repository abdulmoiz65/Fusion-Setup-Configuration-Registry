"""Project source-bound account and organization values; no hidden-field inference."""
from datetime import datetime
import re

import customers_package as package
from customer_api_hierarchy import ACCOUNT, TYPES, MISSING, NIL, identifier
from customer_api_profile_set_review import result, scalar

ORG = 'http://xmlns.oracle.com/apps/cdm/foundation/parties/organizationService/'
PARTY = 'http://xmlns.oracle.com/apps/cdm/foundation/parties/partyService/'
ORG_TYPES = ORG+'applicationModule/types/'
ACCOUNT_FIELDS = {'ACCOUNT_NUMBER':'AccountNumber', 'ACCOUNT_DESCRIPTION':'AccountName',
    'ACCOUNT_TYPE':'CustomerType', 'CUSTOMER_CLASS':'CustomerClassCode',
    'ACCOUNT_ESTABLISHED_DATE':'AccountEstablishedDate'}
ACCOUNT_SITE_FIELDS = {'ACCT_SITE_LANGUAGE':'Language', 'TRANSLATED_CUSTOMER_NAME':'TranslatedCustomerName'}
USE_FIELDS = {'SITE_USE_CODE':'SiteUseCode', 'SITE_USE_PRIMARY_FLAG':'PrimaryFlag', 'SITE_LOCATION':'Location'}
PARTY_FIELDS = {'PARTY_NUMBER':'PartyNumber', 'PARTY_NAME':'PartyName', 'DUNS_NUMBER':'DUNSNumberC',
    'TAXPAYER_ID_NUM':'JgzzFiscalCode', 'GSA_INDICATOR_FLAG':'GSAIndicatorFlag'}
SITE_FIELDS = {'PARTY_SITE_NUMBER':'PartySiteNumber', 'PARTY_SITE_NAME':'PartySiteName',
    'IDENTIFYING_ADDRESS_FLAG':'IdentifyingAddressFlag', 'MAIL_STOP':'Mailstop'}
BOOLEAN_FIELDS = {'SITE_USE_PRIMARY_FLAG', 'GSA_INDICATOR_FLAG', 'IDENTIFYING_ADDRESS_FLAG'}


def validate(row, owners, required):
    package.require(isinstance(row, dict) and all(isinstance(row.get(k), str) for k in
        set(ACCOUNT_FIELDS)|set(ACCOUNT_SITE_FIELDS)|set(USE_FIELDS)|set(PARTY_FIELDS)|set(SITE_FIELDS)),
        'API_BUSINESS_ROW_REQUIRED')
    package.require(isinstance(owners, dict) and all(k in owners for k in required) and
        all(identifier(v) is not MISSING for v in owners.values()), 'API_BUSINESS_OWNERS_REQUIRED')
    return {k:str(v) for k,v in owners.items()}


def select(parent, namespace, name, id_namespace, id_field, expected):
    if parent is None or expected is None:
        return None
    matches = [e for e in parent.findall('{'+namespace+'}'+name)
               if identifier(scalar(e,id_namespace,id_field)) == expected]
    package.require(len(matches) <= 1, 'API_BUSINESS_DUPLICATE_TARGET')
    if not matches:
        return None
    package.require(matches[0].get(NIL) not in ('true','1'), 'API_BUSINESS_NIL_TARGET')
    return matches[0]


def project(row, groups, metadata):
    observed, findings = {}, []
    for parent, namespace, fields in groups:
        for field, name in fields.items():
            value = scalar(parent, namespace, name)
            expected = row[field]
            if value is not MISSING and value is not None and field in BOOLEAN_FIELDS:
                package.require(value in ('true','false','1','0'), 'API_BUSINESS_BOOLEAN_FORMAT')
                value = 'Y' if value in ('true','1') else 'N'
            if field == 'ACCOUNT_ESTABLISHED_DATE':
                if expected:
                    package.require(re.fullmatch(r'\d{4}/\d{2}/\d{2}',expected) is not None,
                                    'API_BUSINESS_INPUT_DATE')
                    try: expected = datetime.strptime(expected,'%Y/%m/%d').date().isoformat()
                    except ValueError as exc: raise package.InvalidInput('API_BUSINESS_INPUT_DATE') from exc
                if value is not MISSING and value is not None:
                    # This deployed xsd:date projection cannot prove raw Oracle DATE seconds.
                    package.require(re.fullmatch(r'\d{4}-\d{2}-\d{2}',value) is not None,
                                    'API_BUSINESS_DATE_FORMAT')
                    try: datetime.strptime(value,'%Y-%m-%d')
                    except ValueError as exc: raise package.InvalidInput('API_BUSINESS_DATE_FORMAT') from exc
            if value is not MISSING:
                observed[field] = value
            findings.append({'field':field,'requested':bool(row[field]),'status':
                'VALUE_NOT_RETURNED' if value is MISSING else 'OMITTED_INPUT_OBSERVED_NOT_EFFECT_VERIFIED'
                if not row[field] else 'MATCH' if value == expected else 'MISMATCH'})
    requested = all(f['status']=='MATCH' for f in findings if f['requested'])
    return {'schema_version':'ar-customer-api-business-values-v1',
        'status':'SELECTED_REQUESTED_VALUES_MATCH' if requested else 'API_BUSINESS_VALUES_REVIEW_REQUIRED',
        'findings':findings,'observed_values':observed,'observed_metadata':metadata,
        'requested_fields_match':requested,'execution_authorized':False,'persisted_reconciliation_complete':False,
        'limits':['Missing values stay unknown; explicit null and omitted input are distinct.',
            'Boolean API values map to worksheet Y/N; account established date retains date-only precision.',
            'Returned children do not prove complete sibling inventories or profile history.',
            'Selected matches do not prove preservation, creation, update execution or attempt causality.']}


def account_values(row, owners, content):
    owners = validate(row,owners,('account','party'))
    account = result(content,TYPES,'getCustomerAccountResponse')
    package.require(identifier(scalar(account,ACCOUNT,'CustomerAccountId'))==owners['account'] and
        identifier(scalar(account,ACCOUNT,'PartyId'))==owners['party'], 'API_BUSINESS_ACCOUNT_SCOPE')
    site = (select(account,ACCOUNT,'CustomerAccountSite',ACCOUNT,'CustomerAccountSiteId',owners.get('account_site'))
            if 'party_site' in owners else None)
    if site is not None:
        package.require(identifier(scalar(site,ACCOUNT,'CustomerAccountId'))==owners['account'] and
            identifier(scalar(site,ACCOUNT,'PartySiteId'))==owners['party_site'], 'API_BUSINESS_ACCOUNT_SITE_SCOPE')
    use = select(site,ACCOUNT,'CustomerAccountSiteUse',ACCOUNT,'SiteUseId',owners.get('account_site_use'))
    if use is not None:
        package.require(identifier(scalar(use,ACCOUNT,'CustomerAccountSiteId'))==owners['account_site'],
                        'API_BUSINESS_USE_PARENT')
    meta = {}
    for parent,prefix,names in ((account,'account',('Status',)),(site,'account_site',
            ('Status','BillToIndicator','ShipToIndicator','MarketIndicator')),
            (use,'account_site_use',('Status','BillToSiteUseId'))):
        for name in names:
            value=scalar(parent,ACCOUNT,name)
            if value is not MISSING: meta[prefix+'.'+name]=value
    return project(row,[(account,ACCOUNT,ACCOUNT_FIELDS),(site,ACCOUNT,ACCOUNT_SITE_FIELDS),
                        (use,ACCOUNT,USE_FIELDS)],meta)


def organization_values(row, owners, content):
    owners=validate(row,owners,('party',))
    container=result(content,ORG_TYPES,'findOrganizationResponse')
    values=container.findall('{'+ORG+'}Value')
    package.require(len(values)==1 and len(container)==1 and values[0].get(NIL) not in ('true','1'),
                    'API_BUSINESS_ORGANIZATION_AMBIGUOUS')
    party=values[0]
    package.require(identifier(scalar(party,ORG,'PartyId'))==owners['party'] and
        scalar(party,ORG,'PartyNumber')==row['PARTY_NUMBER'] and
        scalar(party,ORG,'PartyType')=='ORGANIZATION', 'API_BUSINESS_PARTY_SCOPE')
    site=(select(party,ORG,'PartySite',PARTY,'PartySiteId',owners.get('party_site'))
          if 'location' in owners else None)
    if site is not None:
        package.require(identifier(scalar(site,PARTY,'PartyId'))==owners['party'] and
            identifier(scalar(site,PARTY,'LocationId'))==owners['location'], 'API_BUSINESS_PARTY_SITE_SCOPE')
    use=select(site,PARTY,'PartySiteUse',PARTY,'PartySiteUseId',owners.get('party_site_use'))
    if use is not None:
        package.require(identifier(scalar(use,PARTY,'PartySiteId'))==owners['party_site'],
                        'API_BUSINESS_PARTY_USE_PARENT')
    meta={}
    for parent,namespace,prefix,names in ((party,ORG,'party',('Status',)),(site,PARTY,'party_site',('Status',)),
        (use,PARTY,'party_site_use',('Status','SiteUseType','PrimaryPerType','BeginDate','EndDate'))):
        for name in names:
            value=scalar(parent,namespace,name)
            if value is not MISSING:meta[prefix+'.'+name]=value
    return project(row,[(party,ORG,PARTY_FIELDS),(site,PARTY,SITE_FIELDS)],meta)
