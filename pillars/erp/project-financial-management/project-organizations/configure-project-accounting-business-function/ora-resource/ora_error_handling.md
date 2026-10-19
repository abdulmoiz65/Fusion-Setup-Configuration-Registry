# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Business-unit name does not resolve uniquely in the fresh PJF_INSTALLATION export | Stop and request one exact exported Name |
| Independent start-organization membership proof is missing and the available PABF export does not expose hierarchy membership | Disclose the design warning without blocking preview or import; keep all other gates and let Fusion FSM import validate membership. Proven membership mismatches still block |
| Project or Expenditure Tree Name has no exact fndTrees match | Stop and identify the supplied hierarchy role and Tree Name; request a valid display tree name; never manufacture a technical code |
| Project or Expenditure Tree Name has more than one exact fndTrees match | Stop and report the hierarchy role, supplied Tree Name and ambiguity; do not select the first row |
| Project Tree Version Name has count = 0 under the resolved project tree | Stop and say: Project Tree Version Name <given name> does not exist under Project Tree <given tree name>. Provide a valid tree version name. |
| Expenditure Tree Version Name has count = 0 under the resolved expenditure tree | Stop and say: Expenditure Tree Version Name <given name> does not exist under Expenditure Tree <given tree name>. Provide a valid tree version name. |
| Project or Expenditure Tree Version Name has count > 1 under its resolved tree | Stop and report the hierarchy role, supplied Tree Version Name, selected Tree Name and ambiguity; do not obtain any code from the version name |
| Hierarchy REST response is incomplete, lacks TreeCode or TreeStructureCode, or fails | Stop before preview with input validation for missing fields, transport/environment or Fusion API failure as applicable; preserve existing auth/authz handling and retry policy; never substitute normalized names, export codes or the other hierarchy response |
| A retained documented lookup value is invalid or ambiguous | Stop and name the exact field/value |
| Package/import fails | Report target, checksum, member/row, and Oracle message; no auto-retry |
| ProjStartOrgName has no exact active effective identity or no active effective PROJECTS row | Stop before ZIP generation: {organization name} is not an active Project Organization for the Project and Task Owning Organization Hierarchy. |
| ExpStartOrgName has no exact active effective identity or no active effective EXPENDITURES row | Stop before ZIP generation: {organization name} is not an active Expenditure Organization for the Expenditure Organization Hierarchy. |
| A start-organization lookup has multiple distinct active effective OrganizationId values | Stop before ZIP generation and identify the hierarchy role, supplied name and ambiguity; duplicate same-ID rows are not multiple identities |
| A start-organization lookup fails or pagination/evidence/fields are incomplete | Stop via BUFUNC.RETURN_ISSUES before ZIP generation; disclose role, target, resolver, failure class and sanitized evidence. Retain core auth/authz policy; do not substitute partial data, task exports or another role |
| An exact tree version exists but Status is DRAFT, INACTIVE, blank/missing or any value other than ACTIVE | Stop before ZIP generation, preview or submission: Tree Version Name {version name} exists under Tree {tree name} but is {returned status or blank/missing Status}. Select or activate an active tree version before generating the PABF import ZIP. Do not send it to import to discover this error |
| An exact ACTIVE tree version is expired or future-effective | Stop before ZIP generation, preview or submission; report tree/version, current configuration date and EffectiveStartDate/EffectiveEndDate. Select an active tree version effective on that date |
| Tree-version status, effective dates, configuration date, provenance or pagination is incomplete or REST fails | Stop via BUFUNC.RETURN_ISSUES before ZIP generation; disclose role, target, version and sanitized failure class. Never infer ACTIVE, default missing date bounds, consume partial data or retry a mutation |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required/conditional field fails | Correct field |
| Dependency readiness | Applicable BU, hierarchy, financial-context, calendar, feature, changed-group reference, or package evidence missing | Complete only the dependency applicable to the requested change |
| Protected mutation | Locked calendar or used relationship | Preserve current value |
| Unsupported operation | Enterprise BU/function or direct REST setup write | Route separately/use FSM |
| Approval blocker | Preview absent/changed/declined | Stop without import |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation | Target, matched export row, BU, function/feature state, applicable financial context, each changed group, reference results, warnings |
| Preview | Target, BU, exact before/after fields, relationships, cross-charge rows, member counts, checksum, and any start-organization membership warning |
| Result | Accepted initiation returns In Progress with a retained receipt and no status/export calls. A later explicit status request returns core status/count/error results; requested setup verification requires terminal success before a fresh same-task PABF export comparison of the requested owning/expenditure tree, version and start organization, other requested fields and preserved groups against the approved preview |
| Start-organization validation | Hierarchy role, exact supplied/returned name, OrganizationId, FromDate, ToDate, ActiveStatusFlag, required PROJECTS/EXPENDITURES, target effective date and complete REST evidence reference; preserve the independent membership warning separately |
| Tree-version validation | Hierarchy role, resolved tree, exact version name, Status, EffectiveStartDate, EffectiveEndDate, current configuration date, complete source receipt and any verified same-tree/version reuse |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| BU/function unavailable | Do not silently create or enable it |
| Direct REST requested | Do not infer setup write from unrelated project children or GETs |
| Template/approval absent | Do not import |
| Failure occurs | Do not retry automatically or claim target-state success |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BUFUNC.EXECUTION_GATE | decision | 17 | execution_gate | ready->BUFUNC.RETURN_SUCCESS;not_ready->BUFUNC.RETURN_ISSUES;declined->BUFUNC.RETURN_REFUSAL | BUFUNC.NORMALIZE_EXPORT_ONLY_EFFECTIVE_DATES | stop | Return completed task validation/preparation to the loader's own approval workflow; no submission or status call is authorized by this gate |
| BUFUNC.RETURN_SUCCESS | terminal | 18 | terminal | none | BUFUNC.EXECUTION_GATE | continue | Validation/preparation complete; not evidence of submission or verified import completion |
| BUFUNC.RETURN_ISSUES | terminal | 19 | terminal | none | none | continue | Correctable issue blocks progress |
| BUFUNC.RETURN_REFUSAL | terminal | 20 | terminal | none | none | continue | Unsupported/protected action or declined approval |
