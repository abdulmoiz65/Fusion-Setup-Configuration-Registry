#!/usr/bin/env python3
"""Return task-to-business-object relations or export them to CSV."""
from __future__ import annotations
import argparse, csv, json, sys, urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'core/auth/fusion-oauth-authentication/scripts'))
from fusion_auth import FusionHttpError,get_access_token,http_bytes,read_properties,require_props # noqa:E402
ENDPOINT='/api/boss/data/objects/ora/commonSetup/tasks/v1/taskBusinessObjects'
FIELDS=['PRODUCT','TASK_NAME','TASK_SHORT_NAME','BUSINESS_OBJECT_SHORT_NAME','BUSINESS_OBJECT_NAME']
def rows(body:Any)->list[dict[str,Any]]:
    if isinstance(body,list): return [x for x in body if isinstance(x,dict)]
    if isinstance(body,dict):
        for key in ('items','results','rows','data','value'):
            if isinstance(body.get(key),list): return [x for x in body[key] if isinstance(x,dict)]
    return []
def val(row:Any,*keys:str)->str:
    if not isinstance(row,dict): return ''
    values={str(k).casefold():v for k,v in row.items()}
    for key in keys:
        candidate=values.get(key.casefold())
        if candidate not in (None,'') and not isinstance(candidate,(dict,list)): return str(candidate)
    return ''
def get(base:str,token:str,params:dict[str,Any],stats:dict[str,int])->Any:
    stats['api_call_count']+=1; query=urllib.parse.urlencode(params,safe="$'=")
    body=http_bytes(base.rstrip('/')+ENDPOINT+'?'+query,access_token=token, headers={'Authorization':f'Bearer {token}'})
    return json.loads(body) if body.strip() else {'items':[]}
def main()->int:
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--properties',default=str(ROOT/'core/auth/fusionEnv.properties')); p.add_argument('--token-cache',default='auto'); p.add_argument('--preview-limit',type=int,default=25); p.add_argument('--all',action='store_true'); p.add_argument('--project-id'); p.add_argument('--output'); p.add_argument('--verbose',action='store_true'); a=p.parse_args()
    if a.preview_limit<1: raise ValueError('--preview-limit must be at least 1')
    if a.all and not(a.project_id or a.output): raise ValueError('Full export requires --project-id or --output')
    props=read_properties(Path(a.properties)); require_props(props,['restBaseUrl','boss_scope']); scoped=dict(props); scoped['scope']=props['boss_scope']; token=get_access_token(scoped,token_cache=a.token_cache); stats={'api_call_count':0}; raw=[]; offset=0; limit=1000
    while True:
        if a.verbose: print(f'Subtask 1: retrieving relationship page at offset {offset}...',file=sys.stderr,flush=True)
        try: page=rows(get(props['restBaseUrl'],token,{'$limit':limit if a.all else a.preview_limit,'$offset':offset},stats))
        except FusionHttpError as exc:
            if exc.status_code not in {401,403}: raise
            token=get_access_token(scoped,token_cache=a.token_cache,force_login=True); page=rows(get(props['restBaseUrl'],token,{'$limit':limit if a.all else a.preview_limit,'$offset':offset},stats))
        raw.extend(page)
        if a.verbose: print(f'Subtask 1 complete: retrieved {len(raw)} relations so far.',file=sys.stderr,flush=True)
        if not a.all or len(page)<limit: break
        offset+=len(page)
    output=[]
    for relation in raw:
        task=relation.get('task',{}); bo=relation.get('businessObject',{}); family=task.get('family',{}) if isinstance(task,dict) else {}
        output.append({'PRODUCT':val(family,'userModuleName') or val(task,'product','productName'),'TASK_NAME':val(task,'taskName'),'TASK_SHORT_NAME':val(task,'taskShortName'),'BUSINESS_OBJECT_SHORT_NAME':val(bo,'businessObjectShortName'),'BUSINESS_OBJECT_NAME':val(bo,'businessObjectName')})
    output.sort(key=lambda row:(row['PRODUCT'],row['TASK_NAME'],row['BUSINESS_OBJECT_NAME']))
    if not a.all: print(json.dumps({'row_count':len(output),'api_call_count':stats['api_call_count'],'rows':output[:a.preview_limit]},indent=2,ensure_ascii=False)); return 0
    target=Path(a.output) if a.output else ROOT/'project'/a.project_id/'artifacts/core/fusion-api/fsm-rest-client/tasks-bo'/f"tasks-bo-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.csv"; target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('w',newline='',encoding='utf-8') as h: w=csv.DictWriter(h,fieldnames=FIELDS); w.writeheader(); w.writerows(output)
    if a.verbose: print(f'Subtask 2 complete: wrote {len(output)} rows to {target}.',file=sys.stderr,flush=True)
    print(json.dumps({'row_count':len(output),'api_call_count':stats['api_call_count'],'csv':str(target)},indent=2,ensure_ascii=False)); return 0
if __name__=='__main__':
    try: raise SystemExit(main())
    except Exception as exc: print(f'Error: {exc}',file=sys.stderr); raise SystemExit(1)
