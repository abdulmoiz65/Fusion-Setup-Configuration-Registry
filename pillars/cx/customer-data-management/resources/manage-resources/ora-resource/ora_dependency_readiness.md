# ResourceUser Import and Export Dependencies

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Business units | Complete Manage Business Unit setup for values used in the CSV. |
| 2 | Legal entities | Complete Manage Legal Entity setup for values used in the CSV. |
| 3 | Reference lookup sample | Select the first 10 non-header CSV rows in source order. Validate BusinessUnit, LegalEntity, role codes, and manager emails from those rows only; when later rows remain, inform the user and require explicit confirmation to proceed for them. |
| 4 | Business units | Use one exact `hcmBusinessUnitsLOV` `Name IN (...)` REST lookup for the distinct sampled source values mapped to `BusinessUnit`. |
| 5 | Legal entities | Use one exact current-effective `legalEmployersLov` `Name IN (...)` REST lookup for the distinct sampled source values mapped to `LegalEntity`. |
| 6 | Resource roles | Use the active Resource Roles REST lookup to verify every individual or organization membership role code used in the sample. |
| 7 | Parent records | In one CSV, list every parent row before each dependent child row; otherwise ensure the parent already exists. |
| 8 | Export visibility | Confirm ResourceUser is selectable and caller-visible fields can be exported under existing Fusion roles and data security. |
| 9 | Reporting Hierarchy Generation | Confirm internal hierarchy parameters, required privilege, and configured job definition before the post-import preview. |
| 10 | Send Pending LDAP Requests | Confirm the fixed ESS request contract, configured job definition, and required privilege before the post-import preview. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| MR.BUSINESS_UNIT | Business unit | Conditional | A source column is mapped to `BusinessUnit` for a ResourceUser CX import | Verify | Distinct nonblank values from first 10 source rows mapped to `BusinessUnit` | resolve_sampled_business_units | Resource BusinessUnit values must resolve exactly. | Use one `Name IN (...)` lookup and correct zero or multiple matches; do not search or auto-select a closest match. | Validated BusinessUnit values |
| MR.LEGAL_ENTITY | Legal entity | Conditional | A source column is mapped to `LegalEntity` for a ResourceUser CX import | Verify | Distinct nonblank values from first 10 source rows mapped to `LegalEntity` | resolve_sampled_legal_entities | Resource LegalEntity values must resolve exactly and be current-effective. | Use one current-effective `Name IN (...)` lookup and correct zero or multiple matches; do not search or auto-select a closest match. | Validated LegalEntity values |
| MR.RESOURCE_ROLE | Resource role | Conditional | Role, ResourceOrgRoleCode, or IndividualRoleCode is supplied in the first 10 rows | Verify | Distinct sampled role codes and routing context | GET /crmRestApi/resources/11.13.18.05/resourceRoles with `finder=AllActiveResourceRolesRowFinder`, `q=RoleCode='<code1>' OR RoleCode='<code2>' ...`, and header `Rest-Framework-Version: 9` | Organization selects an organization membership role unless the role is explicitly individual, and every sampled code must exist as an active Resource Role. | Join all distinct sampled role codes in one exact `q` predicate, validate returned RoleCode values, and block with a sanitized, de-duplicated unresolved sampled-code list. | ResourceOrgRoleCode or IndividualRoleCode |
| MR.REFERENCE_LOOKUP_SAMPLE | Reference lookup sample | Conditional | BusinessUnit, LegalEntity, resource role code, or manager email is supplied | Confirm when later rows remain | BusinessUnit, LegalEntity, role codes, and manager emails from the first 10 non-header rows | Local CSV analysis | The reference lookup scope is capped at the first 10 source rows. | Do not look up BusinessUnit, LegalEntity, role codes, or manager emails from later rows. Inform the user that only the first 10 rows were validated and require explicit confirmation to proceed for the remaining rows. | Remaining-rows validation confirmation |
| MR.PARENT_RECORD | Parent record | Conditional | First 10 CSV rows import child records | Verify | Source row order or exact sampled parent email | GET /crmRestApi/resources/11.13.18.05/resourceUsers?q=ResourceEmail='<email>' | A sampled child dependency can be resolved by an earlier sampled parent row or exactly one visible ResourceUser with the referenced manager email. | Place a sampled parent row before each sampled dependent child row, or validate the existing parent by exact email. Do not use an unfiltered or partial collection page; a zero-result response is not proof that the parent is absent and must be confirmed. | Parent email and source row order |
| MR.EXPORT_VISIBILITY | Export object and field visibility | Yes | ResourceUser export is requested | Verify | Current Fusion roles and data-security policy | Export Management object and field selection | Available objects and PII fields depend on the caller's access. | Use only visible, authorized fields; do not change security configuration from this task. | ResourceUser and selected fields |
| MR.RH_ESS | Reporting Hierarchy Generation readiness | Conditional | Completed import changes resource organization or reporting manager hierarchy | Verify | Successful import evidence, target environment context, Tree Structure Code, Tree Code, and fndTreeVersions response | Core REST API Client and Run Reporting Hierarchy Generation skill | The receiving skill owns the fixed CrmEss application, job definition, ordered arguments, final tree validation, submission, and tracking. | Resolve candidates for RESOURCE_ORG_TREE_STRUCTURE and GLOBAL_SALES_MARKETING. Hand off successful import evidence, target environment context, exact tree triple, and submit intent for its preview; after the preview, pass fresh approval as execution_approval. Do not construct a local Reporting Hierarchy ESS payload or perform a Scheduler active-instance lookup. | Validated Tree Version ID and complete receiving-skill preview handoff |
| MR.LDAP_ESS | Send Pending LDAP Requests readiness | Conditional | Completed import has at least one row whose CreateUserAccountFlag is absent or not N | Verify | Fixed ESS request contract and target environment | Core REST API Client and ESS Job Submitter | The job processes pending user-account and role requests and requires a complete verified request contract before its post-import preview. | Evaluate every imported row. Suppress LDAP only when all rows explicitly set N; otherwise present the exact job preview and require post_import_ess_execution_approval before submission. Use `submit.argument1=ALL`, `submit.argument2=ALL`, and `submit.argument3=A`, each as `STRING`. | Complete verified parameter set |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Verify | Existing prerequisite values must be confirmed | Yes |
| Blocked | A required prerequisite is absent or invalid | No |
| Verify | Existing roles and data-security policy must be confirmed | Yes |
| Verify | Eligible ESS parameters and privilege must be confirmed before post-import preview | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MR.IMPORT_DEPENDENCIES | decision | 7 | resolve_dependency | satisfied->MR.IMPORT_BULK;blocked->MR.STOP | MR.IMPORT_VALIDATE | stop | ResourceUser import source data passed field validation. For the first 10 non-header rows only, resolve values mapped to BusinessUnit and LegalEntity through their documented exact live lookups before bulk preparation. |
| MR.RH_READY | decision | 21 | resolve_dependency | ready->MR.LDAP_VALIDATE;blocked->MR.STOP | MR.RH_VALIDATE | stop | Reporting Hierarchy Generation handoff inputs are verified before the receiving skill prepares its post-import preview. |
| MR.LDAP_READY | decision | 23 | resolve_dependency | ready->MR.POST_IMPORT_PREVIEW;blocked->MR.STOP | MR.LDAP_VALIDATE | stop | Send Pending LDAP Requests inputs and privilege are verified for post-import preview. |
