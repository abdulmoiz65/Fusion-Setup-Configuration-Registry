"""Create an immutable Time Slots REST execution preview."""
from __future__ import annotations
import hashlib,json
from typing import Any
TASK_CODE='ORA_FFS_TS_TIME_SLOTS'; LIVE_DIRECTION='ora_rest_execution'
class ImmutablePreviewError(ValueError):pass
def build_execution_preview(payload_preview:dict[str,Any],execution_direction:str,environment:str,baselines:dict[str,dict[str,Any]])->dict[str,Any]:
 if execution_direction!=LIVE_DIRECTION:raise ImmutablePreviewError('immutable Time Slots REST preview requires ora_rest_execution.')
 if not environment.strip():raise ImmutablePreviewError('environment is required.')
 requests=payload_preview.get('requests')
 if not isinstance(requests,list) or not requests:raise ImmutablePreviewError('payload preview has no requests.')
 preview=[]
 for request in requests:
  identity=request.get('identity');body=request.get('body')
  if request.get('method') != 'PUT' or not isinstance(identity,str) or not isinstance(body,dict):raise ImmutablePreviewError('payload preview contains an invalid Time Slots PUT request.')
  baseline=baselines.get(identity)
  if not isinstance(baseline,dict):raise ImmutablePreviewError(f'{identity}: matching current-state baseline is required.')
  preview.append({'identity':identity,'operationId':request.get('operationId'),'method':request.get('method'),'path':request.get('path'),'headers':request.get('headers',{}),'body':body,'baseline':baseline})
 draft={'schemaVersion':'1.0','taskCode':TASK_CODE,'executionDirection':execution_direction,'environment':environment.strip(),'requests':preview}
 digest=hashlib.sha256(json.dumps(draft,ensure_ascii=False,separators=(',',':'),sort_keys=True).encode()).hexdigest()
 return {**draft,'sha256':digest,'approvalRequired':True,'retryPolicy':'never'}
