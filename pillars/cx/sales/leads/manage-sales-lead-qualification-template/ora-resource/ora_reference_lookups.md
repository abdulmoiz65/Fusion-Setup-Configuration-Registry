# Reference Lookups

Source basis: Oracle Fusion Cloud Sales REST API, *Assessment Templates REST
Endpoints* and *Get all assessment templates*.

## Local Lookups

| Resolver | Runs When | Source Values | Local Authority | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|
| inventory_lead_templates_from_reference_export | After a current-data export is integrity- and metadata-validated | ReferenceZipPath, ReferenceZipSha256, ProcessEnv, ProcessRelease | MOW_ASSESSMENT_TEMPLATE.csv and ORA_CRM_ASSESSMENT_TEMPLATE_FOR_RATING.csv from the validated target-environment export | Retain only AssessedObjTypeCode exactly equal to LEAD; require both template CSVs to contain the same exact Name, AssessTemplateNumber, SetId, and StatusCode inventory; then compare TemplateName using exact case-sensitive equality | exported template inventory, exact match count, matching AssessTemplateNumber, SetId, StatusCode, inventory count | Return not_found for zero exact matches, found for one consistent match, many for more than one match, and failure when the two CSV inventories disagree or the archive evidence changes |
| reconcile_lead_template_name_evidence | After the exported inventory and live exact-name lookup are complete | TemplateName, exported exact match count, live exact match count, reference ZIP hash, export timestamp, live lookup timestamp | Output of inventory_lead_templates_from_reference_export plus output of find_assessment_template_by_exact_name | Require the two independently obtained exact-name counts to agree; retain the identifiers and timestamps from both evidence sources | reconciled result, exported exact match count, live exact match count, evidence timestamps, stale-evidence flag | Return not_found only for zero and zero, found only for one exact Lead name in each source, many for a count above one, and failure for every disagreement or changed evidence hash |

## Live Lookups

| Rule ID | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|
| LQT.LOOKUP_TEMPLATE | find_assessment_template_by_exact_name | After validation and dependency readiness for every supported operation | TemplateName | GET /crmRestApi/resources/11.13.18.05/assessmentTemplatesLOV?q=Name='{TemplateName}'&fields=AssessTemplateId,Name,AssessedObjTypeCode,ObjectVersionNumber&onlyData=true | AssessTemplateId, Name, AssessedObjTypeCode, ObjectVersionNumber, hasMore, offset, count | Escape the Fusion q string literal and URL-encode the query; follow pagination while hasMore is true; require exact case-sensitive Name equality; retain only AssessedObjTypeCode equal to LEAD; classify the final match count | AssessTemplateId, Name, AssessedObjTypeCode, ObjectVersionNumber, live exact match count, lookup timestamp | Return not_found for zero matches, found for one match, many for more than one match, and failure for transport, authentication, authorization, pagination, or response-shape errors |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Both export inventory and live lookup return zero exact matches for Create | Return not_found and continue to design enforcement |
| Either source returns exactly one exact match for Create | Return found and block the duplicate name |
| Export inventory and live lookup disagree | Return failure, treat evidence as stale, and require a fresh export before another lookup |
| Exactly one Lead template matches both sources for Copy, Review, or Deploy | Return found with the documented fields and continue to operation routing |
| No Lead template matches either source for Copy, Review, or Deploy | Return not_found and block routing |
| More than one Lead template matches | Return many and stop before review, package preparation, or deployment-readiness output |
| Authentication or authorization fails | Classify the failure and stop; refresh an approved cached token once only when the calling authentication workflow permits it |
| Transport or response-shape validation fails | Stop and disclose the safe request path, status, and corrective action; do not retry automatically |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LQT.LOOKUP_TEMPLATE | step | 3 | reference_lookup | found->LQT.ROUTE;not_found->LQT.ROUTE;many->LQT.RETURN_ISSUES;failure->LQT.RETURN_ISSUES | LQT.DEPENDENCIES | stop | Reconcile the environment-bound exported inventory with the live exact-name Lead lookup |
| LQT.ROUTE | decision | 4 | evaluate_result | proceed->LQT.DESIGN;blocked->LQT.RETURN_ISSUES | LQT.LOOKUP_TEMPLATE | stop | Proceed only when Create has zero matches in both sources, Copy has one consistent source plus a distinct target name, or Review/Deploy-readiness has one consistent target; block duplicates, disagreement, ambiguity, missing targets, and any actual Deploy mutation |
