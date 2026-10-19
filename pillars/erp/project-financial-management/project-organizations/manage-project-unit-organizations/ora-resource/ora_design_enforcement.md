# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Derived routing | Use complete organization-search evidence to derive CREATE_NEW or USE_EXISTING_ORGANIZATION; stop when already defined or selection is required |
| 2 | Effective identity | For an existing organization, preserve the exact selected ID as evidence, exact returned name and code, returned start date, and exact organizationClassificationsLOV display name as HDL anchor and parent keys |
| 3 | Package contract | Generate exactly one action-specific Organization.dat, validate its fields and order, and bind the immutable archive to the preview |
| 3a | Bulk contract | Finish all row checks before packaging; group valid rows by derived action, with one metadata layout per component and one MERGE per row; block every archive if any row fails |
| 4 | Terminal load outcome | Return In Progress after accepted initiation; only a later explicit status request may obtain Core Data Loader terminal success before business verification |
| 5 | Verified outcome | After terminal loading succeeds, confirm both the active classification and sequence-1 Project Unit attributes row before reporting task success |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Routing | Blocker | find_active_organization | Action was user-selected, inferred without complete search evidence, or does not match the active-organization result | Remove the user-selected action and use DerivedAction from the exact-name search | Yes |
| CREATE_NEW | Blocker | find_active_organization | An eligible active organization exists with the requested name | Route to USE_EXISTING_ORGANIZATION; if it is already active as PRJ_PROJECT_UNIT, stop and report it instead | Yes |
| USE_EXISTING_ORGANIZATION | Blocker | find_active_organization | Organization inactive, date outside effective range, missing exact ID/name/classification, or active PRJ_PROJECT_UNIT classification on date | Select an eligible organization using full classification evidence; already-active PRJ_PROJECT_UNIT is a stop outcome, not a load request | Yes |
| Existing classification label | Blocker | resolve_organization_classification | No exact organizationClassificationsLOV match for the selected returned ClassificationCode, ambiguous match, blank label, or returned label disagreement | Bind the exact code and LOV display label before defaults or generation | Yes |
| Existing end date supplied | Blocker | find_active_organization | End exceeds organization range or precedes start | Correct effective range | Yes |
| Existing parent reference | Blocker | resolve_project_unit_member_linkage | Name whitespace changed, Project Unit Classification substituted for existing display label, or raw/composite ID used in DAT | Use exact returned name plus existing classification display name | Yes |
| CREATE_NEW package | Blocker | verify_project_unit_package_contract | Not exactly Organization then OrgInformation then OrgUnitClassification | Regenerate one DAT | Yes |
| Existing package | Blocker | verify_project_unit_package_contract | Not exactly Organization anchor then OrgUnitClassification then OrgInformation; anchor missing, end-dated, mismatched to selected REST/LOV evidence, or using PRJ_PROJECT_UNIT or Project Unit Classification | Regenerate the anchor from the selected existing identity, then add only the Project Unit classification and EFF; never create or rename the base organization | Yes |
| Any package | Blocker | verify_project_unit_package_contract | Source-system fields, SetCode, reference-data-set, wrong fixed values, unsupported fields, or child dates differ | Regenerate from validated request | Yes |
| Bulk package | Blocker | verify_project_unit_package_contract | Any invalid or duplicate row, mixed action headers in one DAT, missing row mapping, or missing per-row verification plan | Report all issues, correct the entire batch, and regenerate action-specific archives | Yes |
| Load completion | Blocker | | Accepted initiation, a nonterminal status, polling timeout, or unknown status is treated as completed, or status is queried without a later explicit request | Return In Progress immediately after initiation; on a later explicit status request check the same request ID through core.data-loader; only terminal success may proceed to post-load verification | Yes |
| Acceptance persistence and resume | Blocker | | Project services or safe receipt/run/token destinations are unavailable, acceptance binding is not persisted/registered, or resumed identity/approved archive binding differs | Block submission during preflight; after acceptance preserve the known ID and stop on local persistence failure. Repair only local evidence, then resume matching registered evidence on explicit request | No automatic write retry |
| Post-load state | Blocker | verify_project_unit_after_load | Terminal loader success is proven but either active PRJ_PROJECT_UNIT or sequence-1 PRJ_PU_ATTRIBUTES with the exact requested code is not verified | Preserve the receipt, report the mismatch, and investigate without resubmitting | No |
| Write route | Blocker | | Direct REST, FSM CSV, update, delete, declassification, end-date mutation of existing Project Unit, or organization-tree write requested | Use the two declared HDL actions; route other work separately | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_active_organization | Both actions | Name conflict or exact eligible selection | ora_reference_lookups.md |
| resolve_organization_classification | Existing action before generation | Exact selected ClassificationCode and LOV ClassificationName | ora_reference_lookups.md |
| resolve_project_unit_member_linkage | Generation | Exact parent references and dates | ora_reference_lookups.md |
| verify_project_unit_package_contract | Preview | Action-specific package and checksum | ora_reference_lookups.md |
| verify_project_unit_after_load | After terminal load success | Active Project Unit classification and sequence-1 exact code attributes | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PUORG.ENFORCE_DESIGN | decision | 7 | design_enforcement | pass->PUORG.EXECUTION_GATE;blocked->PUORG.RETURN_REFUSAL;failure->PUORG.RETURN_ISSUES | PUORG.RESOLVE_DEPENDENCIES | stop | Check eligibility before generation; for bulk, hold execution until every row passes and each action archive validates before preview |
