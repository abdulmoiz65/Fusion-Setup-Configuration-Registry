# Reference Lookups

The maintained lookup catalogs remain the detailed source for individual
criteria. These resource entries expose the lookup and Plan Copy read paths to
the task-rule planner without moving REST writes out of the governed runbook.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_eligibility_profile_references | A populated workbook field is linked to a target-pod object or lookup resolver | Workbook value, Session Effective Date, criterion key, and the context fields linked by mapping-reference.json:criteria_resolver_links | Exact GET path selected by resolver_key from references/eligibility-profile-mapping-reference/mapping-reference.json:rest_api_resolvers or by the maintained criterion-lookup-mappings.json declaration | The selected catalog match_fields and result_id, plus fields required by its resolution_rule | Follow the selected catalog resolution_rule across all pages and require one exact active target-pod result; Department alone may select the first duplicate exact active name in Fusion response order and must emit a warning | Generated XML lookup values and the target identifiers used by BEN_PL_COPY_MAP.xml | Stop on zero or multiple exact matches, except the documented Department policy; stop on 403, 404, missing fields, inactive results, pagination failure, or schema drift. Never use a database or source-pod ID as fallback. |
| inspect_plan_copy_mappings | Combined mapping/import request completed for an existing PlCopyId | PlCopyId from the metadata-create response or approved resume context | /hcmRestApi/resources/latest/benefitPlanCopyParameters/{PlCopyId}/child/mappings?fields=PlCopyMapId,SrcId,SrcName,TrgId,TrgName,ComponentObjType,ComponentObjName,ObjectVersionNumber&limit=500&totalResults=true | PlCopyMapId, SrcId, SrcName, TrgId, TrgName, ComponentObjType, ComponentObjName, ObjectVersionNumber, hasMore | Follow every page; a populated SrcName is resolved only when TrgId is nonblank | Resolved mapping count, unresolved mapping rows, and post-import integrity status | Zero rows is valid only when the package requires no mappings. Any populated SrcName with null TrgId fails verification; preserve sanitized rows for correction and never call submitImport. |
| inspect_plan_copy_result | Combined mapping/import ESS completed or a previously submitted PlCopyId is resumed | PlCopyId and its mapping/import request ID | /hcmRestApi/resources/latest/benefitPlanCopyParameters/{PlCopyId}; /hcmRestApi/resources/latest/benefitPlanCopyParameters/{PlCopyId}/child/logs?limit=500&totalResults=true | ImportPlDesign, RequestStatus, Message, LogMessage, ProcessLog, items, hasMore | Poll the parent until ImportPlDesign is 12 or 10, or until the existing timeout; retrieve processing logs at a terminal application state | Final application status, request status, processing-log count, and sanitized error messages | ImportPlDesign 12 with no terminally unsuccessful RequestStatus is success. ImportPlDesign 10 or a failed RequestStatus is failure. A timeout preserves identifiers and never causes resubmission. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Target-pod pagination | Follow hasMore until false; an exact-match resolver may stop after two matches because ambiguity is already proved. |
| Authentication rejection on GET | Refresh one rejected cached OAuth token once, then repeat only that read. Stop if the read is still rejected. |
| Internal or unlisted resolver | Require the documented target-pod capability and privilege preflight before package generation. |
| Mapping or result inspection | Send REST-Framework-Version: 9, use GET only, and never convert the read into a mapping PATCH or a repeated action. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_PLAN_COPY.RESOLVE_REFERENCES | step | 3 | reference_lookup | resolved->BEN_PLAN_COPY.ENFORCE_DESIGN;blocked->BEN_PLAN_COPY.FAILED | BEN_PLAN_COPY.CONFIRM_DEPENDENCIES | stop | Resolve every lookup required by the current workbook on the selected target environment before package generation; apply the inspection resolvers only when an existing Plan Copy ID is being verified or resumed. |
