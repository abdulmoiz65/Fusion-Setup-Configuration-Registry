# ResourceUser Import and Export Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve |
|---|---|---|---|
| Create resource identity | FirstName, LastName, BusinessUnit, LegalEntity, ResourceEmail | Block preview | Provide valid source values. |
| Update resource identity | ResourcePartyNumber | Block preview | Provide the existing resource party number. |
| Resource Users date fields | Every supplied ResourceEndDate, ResourceOrgMemRoleStartDate, or ResourceOrgMemRoleEndDate is a valid calendar date | Block preview | Trim and normalize valid YYYY/MM/DD or ISO 8601 timestamp input to YYYY-MM-DD before generating the Data Loader source. Preserve valid YYYY-MM-DD input. Reject malformed or impossible dates, ambiguous numeric dates, and locale-specific date text. Show the normalized value in the preview. |
| Organization role routing | Organization and Role | Block preview | Map Role to ResourceOrgRoleCode and complete its prerequisite setup. |
| Explicit individual role | Role explicitly designated individual | Block preview | Map Role to IndividualRoleCode and complete its prerequisite setup. |
| Ambiguous role routing | Organization or explicit individual-role designation with Role | Block preview | Provide Organization or explicitly identify the role as individual. |
| CX Import object code | Valid mapping CSV `IMPORT OBJECT`, or defaulted `ResourceUser` when this Manage Resources import has no mapping CSV | Block preview | Apply the Manage Resources default. Stop for clarification if the caller explicitly names a different object code. |
| CX UCM account | Nonblank `UcmAccount` returned by Data Loader object metadata for `ResourceUser` | Block preview | Correct object metadata access; do not hard-code or accept a caller UCM account. |
| Live BusinessUnit sample | Every distinct nonblank value from the source column mapped to `BusinessUnit` in the first 10 non-header CSV rows has exactly one exact `hcmBusinessUnitsLOV` match | Block preview | Correct the sampled BusinessUnit value. Do not use word search, a closest match, or later rows. |
| Live LegalEntity sample | Every distinct nonblank value from the source column mapped to `LegalEntity` in the first 10 non-header CSV rows has exactly one exact current-effective `legalEmployersLov` match | Block preview | Correct the sampled LegalEntity value. Do not use word search, a closest match, or later rows. |
| Live resource role code sample | Every distinct nonblank ResourceOrgRoleCode or IndividualRoleCode from the first 10 non-header CSV rows appears in the active Resource Roles lookup | Block preview | Correct unresolved sampled codes or activate the required Resource Role. |
| Reference lookup sample | BusinessUnit, LegalEntity, role codes, and manager emails are selected only from the first 10 non-header CSV rows in source order | Stop pending confirmation when more rows remain | Inform the user that only the first 10 rows were validated and require explicit confirmation to proceed for the remaining rows. Do not look up later rows. |
| Work, mobile, or fax phone | Matching country code when a raw phone number is provided | Block preview | Provide the corresponding country code. |
| Export identity and scope | Unique export activity name and a filter on the top-level ResourceUser object | Block preview | Provide the activity name and filter. |
| Reporting Hierarchy Generation | A single fndTreeVersions candidate with `Status=ACTIVE`, an effective start date on or before the target current date, and no earlier effective end date; successful import evidence; target environment context; and an exact tree triple | Block post-import submission | Resolve the candidate or correct the hierarchy selection, then send the complete structured handoff to Run Reporting Hierarchy Generation. |
| Send Pending LDAP Requests | Complete fixed verified ESS request contract | Block post-import submission | Use application `EarHcmEss`, job definition `JobDefinition://oracle/apps/ess/hcm/users/ProcessLdapRequests`, and all three required `STRING` arguments. |
| Single-resource GET identity | Exactly one ResourceEmail or ResourcePartyNumber for resource_user_get, with no CSV, UCM, bulk, or mutation intent | Stop lookup | Provide one exact identifier; stop on zero, multiple, incomplete, or unauthorized lookup results. |
| Unsupported one-resource write | A create, update, promotion, demotion, transfer, end-date, or delete request without a CSV or CX ZIP source | Stop before preview | Do not use Resource Users REST Data Loader or direct Resource Users POST/PATCH/DELETE. Request a supported ResourceUser CX Import source for create or update. |
| Direct reportees manager identity | Exactly one ResourceEmail or PartyName for the manager | Stop lookup | Provide one exact manager identifier and resolve one complete Resource User through read-only REST. |

## Dependency-Aware Validation

| Applies When | Result | Next Action |
|---|---|---|
| BusinessUnit or LegalEntity is not an existing valid value | Blocked | Correct the CSV after the prerequisite setup is complete. |
| A sampled BusinessUnit value has zero or multiple exact `hcmBusinessUnitsLOV` matches | Blocked | Report the de-duplicated sampled value and affected source row numbers; correct the CSV before preview. |
| A sampled LegalEntity value has zero or multiple exact current-effective `legalEmployersLov` matches | Blocked | Report the de-duplicated sampled value and affected source row numbers; correct the CSV before preview. |
| ResourceEmail is duplicated for a new resource | Blocked | Provide a unique email address. |
| ResourcePartyNumber is duplicated for a new record | Blocked | Use a unique value or allow automatic generation. |
| Organization and Role are supplied without an explicit individual-role designation | Ready | Map Role to ResourceOrgRoleCode and verify it. |
| Role is explicitly identified as individual | Ready | Map Role to IndividualRoleCode and verify it. |
| Role is supplied without Organization or explicit individual-role designation | Blocked | Collect the missing role-routing context before preview. |
| A ResourceOrgRoleCode or IndividualRoleCode from the first 10 rows is absent from the active Resource Roles lookup | Blocked | Report only the distinct unresolved sampled code and its routing context; correct or activate the role before preview. |
| CSV has data rows after the first 10 | Blocked pending confirmation | Inform the user that only the first 10 rows were validated. Require explicit confirmation to proceed for the remaining rows; do not perform BusinessUnit, LegalEntity, role-code, or manager-email lookups for them. |
| A child row references a parent resource in the same CSV and the parent row appears earlier | Ready | Preserve the row order and continue to bulk preparation. |
| A child row references a parent resource that is absent or appears later in the same CSV | Blocked | Add the parent row or move it before the child row. |
| A matching import activity may already exist | Blocked | Stop and review the prior activity before resubmission. |
| Import source maps all required attributes and prerequisites are satisfied | Ready | Continue to import bulk preparation. |
| Manage Resources import has no valid CX mapping CSV and no explicit different object code | Ready | Default `cx_import_object_code` to `ResourceUser` and continue to Data Loader preview. |
| An explicit object code conflicts with a valid mapping CSV or requests an object other than ResourceUser | Blocked | Stop for clarification; do not override the mapping or substitute ResourceUser. |
| Export filter is on the top-level object and selected fields are caller-provided or intentionally omitted | Ready | Continue to export design review. |
| Completed import changed resource organizations or reporting-manager hierarchy | Ready | Validate the Reporting Hierarchy Generation request. |
| Completed import has at least one row whose CreateUserAccountFlag is absent or not N | Ready | Validate and submit Send Pending LDAP Requests without a flag-specific message. |
| A ResourceUser import completion check confirms a successful completed load | Ready | Validate both post-import processes, present every eligible job, and request fresh approval to submit them; do not submit an ESS job from the import approval. |
| Every imported row explicitly sets CreateUserAccountFlag to N | Ready | State that all imported rows suppress LDAP processing; do not submit Send Pending LDAP Requests. |
| Data Load initiation is accepted but no explicit successful completed status is available | Blocked | Do not route post-import ESS work or poll automatically. |
| Import is incomplete, failed, or loaded no successful rows | Blocked | Do not route post-import ESS work. |
| Reporting Hierarchy Generation lacks one current effective active Tree Version ID or a complete structured preview handoff | Blocked | Resolve one candidate using status and effective-date checks, then supply the successful import evidence, target environment context, exact tree triple, and submit intent to the receiving skill. Require fresh approval only after that skill returns the ESS preview. |
| Send Pending LDAP Requests is missing a required fixed request-contract value | Blocked | Restore application `EarHcmEss` and all three required `STRING` arguments before post-import preview. |
| Post-import preview is complete but an eligible ESS job lacks fresh post_import_ess_execution_approval | Blocked pending approval | Present the target environment, job definition, application, and exact parameters; do not treat the ResourceUser import approval as post-import approval. |
| A single-resource GET lookup returns zero, multiple, incomplete, or unauthorized results | Blocked | Do not infer a Resource User identity or claim the resource is globally absent. Resolve exact identity and visibility. |
| A one-resource write is requested without a CSV or CX ZIP source | Blocked | Do not use Resource Users REST Data Loader; request a supported ResourceUser CX Import source for create or update. |
| A direct reportees request has no exact manager identity, or the manager lookup returns zero, multiple, incomplete, or unauthorized results | Blocked | Do not query reportees or infer a manager email. Provide one exact visible manager ResourceEmail or PartyName. |
| A direct reportees query returns no current Resource Users | Ready | Return an explicit empty reportees list; do not substitute organization members, hierarchy descendants, or similarly named resources. |

## Field Validation

| Check | What Happens |
|---|---|
| Map source attributes to Resource object attributes | Review mappings before submission. |
| Validate CSV data and unmapped columns | Correct issues before live submission. |
| Verify parent dependency order | Allow one CSV when each parent row appears before its dependent child rows; otherwise block preview. |
| Verify sampled active resource role codes | Retrieve all active Resource Roles and verify distinct ResourceOrgRoleCode and IndividualRoleCode values from the first 10 non-header CSV rows only. Block the import when a sampled code is unresolved. |
| Verify sampled BusinessUnit values | After mapping, collect distinct nonblank values from the source column mapped to `BusinessUnit` in the first 10 non-header CSV rows and use one exact `hcmBusinessUnitsLOV` `Name IN (...)` lookup. Require exactly one match per value. |
| Verify sampled LegalEntity values | After mapping, collect distinct nonblank values from the source column mapped to `LegalEntity` in the first 10 non-header CSV rows and use one exact current-effective `legalEmployersLov` `Name IN (...)` lookup. Require exactly one match per value. |
| Verify sampled manager emails | From the first 10 non-header rows only, validate manager emails not satisfied by an earlier sampled parent row through the exact ResourceUser lookup. Inform the user of the sample limit and require confirmation before proceeding when later rows remain. |
| Verify the export activity name is unique | Correct the activity name before preview. |
| Verify the export filter targets the top-level ResourceUser object | Correct the filter before preview. |
| Verify Reporting Hierarchy Generation parameters | Require RESOURCE_ORG_TREE_STRUCTURE, GLOBAL_SALES_MARKETING, one Tree Version ID selected by status and effective-date checks, and job definition `JobDefinition://oracle/apps/ess/cdm/foundation/resources/resourceRepMgrSync/ResourceHierarchyUpdateJob`. |
| Verify Send Pending LDAP Requests parameters | Require application `EarHcmEss`, job definition `JobDefinition://oracle/apps/ess/hcm/users/ProcessLdapRequests`, and `STRING` arguments `submit.argument1=ALL` (Oracle User Type), `submit.argument2=ALL` (required verified runtime value), and `submit.argument3=A` (Oracle automatic Batch Size). |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MR.IMPORT_VALIDATE | decision | 5 | validate_input | valid->MR.IMPORT_DEPENDENCIES;invalid->MR.STOP | MR.IMPORT_DEFAULT | stop | ResourceUser import inputs and source data are collected. BusinessUnit, LegalEntity, role-code, and manager-email reference validation applies only to the first 10 non-header CSV rows; if later rows remain, valid requires explicit confirmation to proceed for them. |
| MR.EXPORT_VALIDATE | decision | 6 | validate_input | valid->MR.EXPORT_DESIGN;invalid->MR.STOP | MR.EXPORT_DEFAULT | stop | ResourceUser export inputs are collected. |
| MR.REPORTEES_VALIDATE | decision | 31 | validate_input | valid->MR.REPORTEES_MANAGER_RESOLVE;invalid->MR.STOP | MR.OPERATION | stop | A direct reportees request provides exactly one manager ResourceEmail or PartyName and contains no CSV, UCM, bulk, import, or mutation intent. |
| MR.GET_VALIDATE | decision | 51 | validate_input | valid->MR.GET_LOOKUP;invalid->MR.STOP | MR.OPERATION | stop | resource_user_get supplies exactly one ResourceEmail or ResourcePartyNumber and has no CSV, UCM, bulk, export, or mutation intent. |
| MR.IMPORT_RESULT | decision | 17 | evaluate_result | complete->MR.POST_IMPORT_ROUTE;incomplete->MR.STOP | MR.IMPORT_SUBMIT | stop | A Data Loader completion check, not initiation alone, confirms a completed ResourceUser import. On success, validate post-import ESS eligibility and readiness, present every eligible job, and request fresh approval to submit them before ending the result flow. |
| MR.EXPORT_RESULT | decision | 18 | evaluate_result | complete->MR.DONE_EXPORT;incomplete->MR.STOP | MR.EXPORT_SUBMIT | stop | The core export workflow returns job status and a ZIP download result. |
| MR.POST_IMPORT_ROUTE | decision | 19 | validate_input | none->MR.DONE_IMPORT_NO_ESS;eligible->MR.RH_VALIDATE;ineligible->MR.STOP | MR.IMPORT_RESULT | stop | A completed import is classified for the two independent post-import processes. |
| MR.RH_VALIDATE | decision | 20 | validate_input | eligible->MR.RH_READY;not_eligible->MR.LDAP_VALIDATE;invalid->MR.STOP | MR.POST_IMPORT_ROUTE | stop | Reporting Hierarchy Generation eligibility, exact tree triple, successful import evidence, and receiving-skill handoff inputs are evaluated before a fresh post-import approval. |
| MR.LDAP_VALIDATE | decision | 22 | validate_input | eligible->MR.LDAP_READY;not_eligible->MR.POST_IMPORT_PREVIEW;invalid->MR.STOP | MR.RH_VALIDATE | stop | Send Pending LDAP Requests eligibility and runtime inputs are evaluated before a fresh post-import approval. |
| MR.POST_IMPORT_RESULT | decision | 27 | evaluate_result | complete->MR.DONE_IMPORT_ESS;incomplete->MR.STOP | MR.POST_IMPORT_SUBMIT | continue | Every eligible ESS request reached a terminal status after independent polling. |
