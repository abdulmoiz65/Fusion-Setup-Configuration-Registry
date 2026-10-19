# ResourceUser Import and Export Intake

## Accepted Input Formats

| Input Format | What Must Be Provided | Applies To |
|---|---|---|
| CX ZIP or direct CSV group | Resource attributes mapped to Oracle Resource object attributes, with zero or one valid CX mapping CSV | Preview and initiate one ResourceUser CX data load |
| Export request | Unique activity name, top-level filter, optional selected fields, output settings, and optional download path | Export ResourceUser records |
| Direct reportees request | One exact manager ResourceEmail or exact manager PartyName | Read-only list of current Resource Users reporting directly to one manager |
| Single-resource GET request | One exact ResourceEmail or ResourcePartyNumber, with no CSV, UCM, bulk, or mutation intent | Read-only Resource Users identity lookup and requested authorized fields |

## Dependency Inputs

| Field | Mandatory | Purpose | Send in Request Body? | Lookup Rule |
|---|---|---|---|---|
| Operation | Yes | Choose ResourceUser CX Import, Export Management, direct reportees, or single-resource GET | Yes | Import requires a CSV or CX ZIP source; export requires a filter; read-only requests require one exact identity |
| CX import source | Conditional | Provide one CX ZIP or one or more direct CSV files | Yes | Use Data Loader CX Import; do not accept an existing UCM reference |
| CX object code | Conditional | Identify an unmapped CX source | Yes | Required only when a valid mapping CSV is absent; caller supplies `ResourceUser` |
| Export activity name | Conditional | Identify an export activity | Yes | Caller supplies a unique name |
| Export filter | Conditional | Restrict the top-level ResourceUser export object | Yes | Caller supplies a filter |
| Reporting Hierarchy Tree Version ID | Conditional | Identify the internal resource hierarchy version to generate | Yes | Resolve from fndTreeVersions when the import changes organizations or reporting managers; accept only the single current effective active version |
| Reporting Hierarchy job definition | Conditional | Prepare the documented scheduled process through the core ESS skill | Yes | Use `JobDefinition://oracle/apps/ess/cdm/foundation/resources/resourceRepMgrSync/ResourceHierarchyUpdateJob` in the fresh post-import approval preview when Reporting Hierarchy Generation is eligible |
| LDAP ESS request contract | Conditional | Prepare Send Pending LDAP Requests through the core ESS skill | Yes | Use application `EarHcmEss`, job definition `JobDefinition://oracle/apps/ess/hcm/users/ProcessLdapRequests`, and `STRING` parameters `submit.argument1=ALL` (Oracle User Type), `submit.argument2=ALL` (required verified runtime value), `submit.argument3=A` (Oracle automatic Batch Size) in the fresh post-import approval preview when LDAP processing is eligible |
| Post-import ESS execution approval | Conditional | Authorize eligible post-import ESS submission | Yes | After a successful import, approve the exact target environment and each job's application, job definition ID, and parameters; the import approval alone is insufficient |
| ResourcePartyNumber | Conditional | Identify an existing resource for update | Yes | Required for update import |
| ResourceEmail | Conditional | Identify a new resource and provide its email | Yes | Required for create import |
| Organization | Conditional | Select organization membership role routing | Yes | When supplied, map Role to ResourceOrgRoleCode unless the role is explicitly individual |
| Role and role designation | Conditional | Supply a ResourceUser role code and, when applicable, explicit individual-role designation | Yes | Explicit individual designation maps Role to IndividualRoleCode |
| Single-resource GET identity | Conditional | Identify exactly one Resource User for resource_user_get | No | Supply exactly one ResourceEmail or ResourcePartyNumber; resolve one complete exact result through read-only Resource Users REST. |
| Direct reportees manager identity | Conditional | Identify one manager whose current direct reportees are requested | No | Supply exactly one ResourceEmail or PartyName; resolve it through read-only Resource Users REST before querying reportees. |

## Body Field Rules

| Situation | What Happens |
|---|---|
| Importing a new resource | Collect FirstName, LastName, BusinessUnit, LegalEntity, and ResourceEmail before submission. |
| Updating a resource by import | Collect ResourcePartyNumber as the record key. |
| Source supplies Organization and Role | Map Role to ResourceOrgRoleCode and verify the related organization membership role setup. |
| Source explicitly identifies an individual role | Map Role to IndividualRoleCode and verify the related individual role setup. |
| Source supplies Role without Organization or explicit individual designation | Stop and collect the missing role-routing context. |
| Every imported row explicitly sets CreateUserAccountFlag to N | State that LDAP processing is suppressed because all rows set N. |
| Any imported row omits CreateUserAccountFlag or has a value other than N | Ignore the N suppression rule and submit the LDAP job after readiness checks; do not emit a flag-specific message. |
| Source contains parent and dependent resources | Keep them in one CSV when each parent row appears before every row that references it. |
| Source has a phone number | Collect the matching country code for the supplied phone type. |
| Exporting ResourceUser records | Collect a top-level-object filter; fields and output settings are caller-selected. |
| Import completed with successful hierarchy changes | Resolve the single current effective active Tree Version ID, present the Reporting Hierarchy Generation preview, and request fresh post-import approval. |
| Import completed and any row omits CreateUserAccountFlag or has a value other than N | Use the fixed LDAP ESS request contract, present the LDAP preview, and request fresh post-import approval. |
| Import completed and every row explicitly sets CreateUserAccountFlag to N | Do not submit the LDAP job; state that all imported rows suppress LDAP processing. |
| Both post-import processes are eligible | Present both exact job previews. Submit and poll only the jobs explicitly approved after the import result. |
| A one-resource create, update, promotion, demotion, transfer, end-date, or delete is requested without a CSV or CX ZIP source | Stop. This 26.10 skill does not use Resource Users REST Data Loader or direct Resource Users POST/PATCH/DELETE. Request a supported ResourceUser CX Import source for create or update. |
| resource_user_get is requested with one exact identity | Use only the read-only Resource Users identity lookup. Return requested authorized fields from one complete result, or stop on zero, multiple, incomplete, or unauthorized results. Do not enter Data Loader, preview, approval, or post-processing. |
| A standalone one-resource organization-membership change is requested | Stop. Do not reinterpret it as a generic Resource User update. A CSV source may use the separate ResourceUser CX Import route. |
| Direct reportees are requested | Use only the read-only direct-reportees branch. Resolve one exact manager identity, query ResourceOrgManagerEmail, paginate until complete, and return only current matches. Do not use Data Loader, preview, approval, POST, PATCH, hierarchy generation, or LDAP processing. |
| Caller supplies a CSV or CX ZIP source, including a single-row CSV | Route to ResourceUser CX Import through `core.data-loader`; do not convert the row into a REST Data Loader request. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MR.COLLECT | step | 1 | collect_input | complete->MR.OPERATION | none | stop | A ResourceUser CX Import, Export Management, direct reportees lookup, or single-resource GET is requested. |
| MR.OPERATION | decision | 2 | collect_input | import->MR.IMPORT_DEFAULT;export->MR.EXPORT_DEFAULT;reportees->MR.REPORTEES_VALIDATE;get->MR.GET_VALIDATE;unsupported_write->MR.STOP | MR.COLLECT | stop | Intake selects CX Import, Export Management, direct reportees, or single-resource GET. A one-resource write without a supported import source stops; it never enters Data Loader REST mode. |
