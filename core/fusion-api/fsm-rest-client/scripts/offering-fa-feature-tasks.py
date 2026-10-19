#!/usr/bin/env python3
"""Retrieve an offering's functional areas and related feature hierarchy."""
from __future__ import annotations
import argparse, csv, json, sys, urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[4]; sys.path.insert(0,str(ROOT/'core/auth/fusion-oauth-authentication/scripts'))
from fusion_auth import FusionHttpError,get_access_token,http_json,read_properties,require_props # noqa:E402
BASE='/api/boss/extraction/queries/ora/commonSetup/features/v1'
OFFERINGS='/api/boss/data/objects/ora/commonSetup/features/v1/features/$views/availableOfferings'
def rows(value:Any)->list[dict[str,Any]]:
    if isinstance(value,list): return [x for x in value if isinstance(x,dict)]
    if isinstance(value,dict):
        for key in ('items','results','rows','data','value'):
            if isinstance(value.get(key),list): return [x for x in value[key] if isinstance(x,dict)]
    return []
def fetch_rows(base:str,token:str,endpoint:str,params:dict[str,Any],limit:int=500)->list[dict[str,Any]]:
    output=[]
    offset=0
    while True:
        query=urllib.parse.urlencode({**params,'$limit':limit,'$offset':offset})
        page=rows(http_json(base.rstrip('/')+endpoint+'?'+query,access_token=token, headers={'Authorization':'Bearer '+token}))
        output.extend(page)
        if len(page)<limit: return output
        offset+=limit
def get(base:str,token:str,name:str,params:dict[str,str])->list[dict[str,Any]]:
    return fetch_rows(base,token,BASE+'/'+name,params)
def get_offerings(base:str,token:str)->list[dict[str,Any]]:
    return fetch_rows(base,token,OFFERINGS,{})
def text(row:dict[str,Any],*keys:str)->str:
    lower={str(k).lower():v for k,v in row.items()}
    for key in keys:
        if lower.get(key.lower()) not in (None,''): return str(lower[key.lower()])
    return ''
def build(offering:str,fas:list[dict[str,Any]],features:list[dict[str,Any]])->list[dict[str,str]]:
    fa_names={text(fa,'featureShortName'):text(fa,'featureName') for fa in fas if text(fa,'featureShortName')}
    output=[{'OFFERING':offering,'FA':name,'FEATURE':''} for name in sorted(set(fa_names.values()))]
    for feature in features:
        feature_name=text(feature,'childFeatureName','featureName')
        if not feature_name: continue
        parent=text(feature,'parentFeatureShortName','immediateParentShortName')
        path_parts=[part for part in text(feature,'path').strip('/').split('/') if part]
        fa_code=parent if parent in fa_names else next((part for part in path_parts if part in fa_names),'')
        output.append({'OFFERING':offering,'FA':fa_names.get(fa_code,''),'FEATURE':feature_name})
    return output
def main()->int:
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--offering-short-name'); p.add_argument('--offering-offset',type=int,default=0); p.add_argument('--offering-limit',type=int); p.add_argument('--project-id',default='fdos-initial-setup'); p.add_argument('--properties',default=str(ROOT/'core/auth/fusionEnv.properties')); p.add_argument('--token-cache',default='auto'); p.add_argument('--dry-run',action='store_true'); p.add_argument('--verbose',action='store_true'); a=p.parse_args()
    if a.offering_offset<0 or a.offering_limit is not None and a.offering_limit<1: p.error('Offering offset must be nonnegative and limit must be positive.')
    if a.dry_run: print('Would call availableOfferings, availableSetupFunctionalAreasByOffering, and availableFeaturesByOffering.'); return 0
    props=read_properties(Path(a.properties)); require_props(props,['restBaseUrl','boss_scope']); scoped=dict(props); scoped['scope']=props['boss_scope']; token=get_access_token(scoped,token_cache=a.token_cache)
    if a.verbose: print('Subtask 1: retrieving available offerings...',file=sys.stderr,flush=True)
    try: available=get_offerings(props['restBaseUrl'],token)
    except FusionHttpError as exc:
        if exc.status_code not in {401,403}: raise
        token=get_access_token(scoped,token_cache=a.token_cache,force_login=True); available=get_offerings(props['restBaseUrl'],token)
    if a.verbose: print(f'Subtask 1 complete: retrieved {len(available)} offerings.',file=sys.stderr,flush=True)
    offerings=[{'code':text(row,'featureShortName','offeringShortName'),'name':text(row,'featureName','offeringName','featureShortName','offeringShortName')} for row in available]
    offerings=[row for row in offerings if row['code']]
    if a.offering_short_name:
        offerings=[row for row in offerings if row['code']==a.offering_short_name]
        if not offerings: raise ValueError(f'Offering not found: {a.offering_short_name}')
    else:
        offerings=offerings[a.offering_offset:]
        if a.offering_limit is not None: offerings=offerings[:a.offering_limit]
    project=ROOT/'project'/a.project_id
    if not project.is_dir(): raise ValueError(f'Project workspace does not exist: {project}')
    folder=project/'artifacts/core/fusion-api/fsm-rest-client/offering-fa-features'; folder.mkdir(parents=True,exist_ok=True); label=a.offering_short_name.lower() if a.offering_short_name else 'all-offerings'; path=folder/f"{label}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.csv"
    fields=['OFFERING','FA','FEATURE']
    rows_out=[]; errors=[]
    with path.open('w',newline='',encoding='utf-8') as h:
        w=csv.DictWriter(h,fieldnames=fields); w.writeheader()
        for index,offering in enumerate(offerings,start=1):
            code=offering['code']; name=offering['name'] or code
            if a.verbose: print(f'Subtask 2.{index}/{len(offerings)}: processing offering {code}...',file=sys.stderr,flush=True)
            fa=[]; feature=[]
            try:
                fa=get(props['restBaseUrl'],token,'availableSetupFunctionalAreasByOffering',{'parentShortName':code})
            except Exception as exc:
                errors.append({'offering':code,'endpoint':'functional_areas','message':str(exc)})
            try:
                feature=get(props['restBaseUrl'],token,'availableFeaturesByOffering',{'parentShortName':code})
            except Exception as exc:
                errors.append({'offering':code,'endpoint':'features','message':str(exc)})
            built=build(name,fa,feature)
            rows_out.extend(built); w.writerows(built); h.flush()
            if a.verbose: print(f'Subtask 2.{index} complete: collected {len(rows_out)} rows so far.',file=sys.stderr,flush=True)
    print(json.dumps({'offering_count':len(offerings),'row_count':len(rows_out),'errors':errors,'relationship_csv':str(path.relative_to(ROOT))},indent=2,ensure_ascii=False)); return 1 if errors else 0
if __name__=='__main__':
    try: raise SystemExit(main())
    except Exception as exc: print(f'Error: {exc}',file=sys.stderr); raise SystemExit(1)
