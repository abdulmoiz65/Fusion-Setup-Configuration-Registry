# Legal Entity HCM Information Dependency Readiness

## Purpose

Require current identity, synchronization, branch, EFF, history, and Core Data Loader evidence before a read completes or a mutation is handed off.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Environment and identity | Confirm the safe environment alias, authenticated identity, and required read/synchronization privileges |
| 2 | Exact Legal Entity | Resolve one current Legal Entity from a business identifier |
| 3 | Organization synchronization | Reuse only a successful terminal ManageLegalEntity outcome from the same interaction session, same normalized Legal Entity identity, and same environment when it is no more than 24 hours old; otherwise use the registered object once for the fresh match and retain its verified outcome in resume context |
| 4 | Applicable branches | Resolve every branch whose current routing flag is Y |
| 5 | Exact metadata and contexts | Resolve current CategoryCode-based describes, link-bearing EFF envelopes, requested/default contexts, and selected rows |
| 6 | Values and history | Resolve declared value sets and complete history when applicable |
| 7 | Loader route | Select legalEmployersEFF, payrollStatutoryUnitsEFF, or both from affected applicable branches for EFF work, with each selected EFF object's embedded ModifyOrganizationUnitForChildCorrect correction action or SplitOrganizationUnitForEFFUpdate dated-update action; select only DeleteOrganizationUnitForDTDelete for date-effective parent deletion |
| 8 | Live loader contract | Confirm the registered object, template, keys, operation fields, and required action sections for each selected object |
| 9 | Effective operation contract | For every EFF edit, including a new child row, compare the requested operation EffectiveStartDate only with the affected top-level organization's current EffectiveStartDate: equal requires ModifyOrganizationUnitForChildCorrect, later requires SplitOrganizationUnitForEFFUpdate, and earlier is invalid. For a parent delete, require one eligible history start and the current DeleteOrganizationUnitForDTDelete template with RestAction=POST and its required transport headers |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| LE.ENV | Environment, authentication, and privileges | Yes | Every request | Verify | Active project/environment context |  | Prevents cross-environment reads or unauthorized work | Supply or correct the intended environment and access | Safe environment alias and privilege readiness |
| LE.IDENTITY | Exact Legal Entity | Yes | Every request | Lookup | Fresh advanced-search result | find_legal_entity_exact | Prevents mutation or disclosure against the wrong Legal Entity | Provide one exact Name or identifier | Current identity and routing flags |
| LE.SYNC | Current Legal Entity synchronization | Yes | Every Get or mutation | Verify | Approved ManageLegalEntity Core Data Loader workflow and resume context |  | Establishes current HCM state before branch-root resolution | Reuse only a successful terminal same-session, same-identity, same-environment outcome no more than 24 hours old; otherwise complete the synchronization-only loader handoff once. Resolve branch OrganizationId only from the subsequent exact LegalEntityId root query. Do not treat synchronization as approval for another mutation | Synchronization status and current OrganizationId fingerprint |
| LE.ROOTS | Applicable Legal Employer and PSU roots | Yes | After synchronization | Lookup | Fresh branch-root reads | resolve_legal_entity_hcm_roots | Supplies current effective boundaries, CategoryCode, and EFF links | Resolve every applicable requested branch | Root and boundary evidence |
| LE.METADATA | Exact EFF metadata | Conditional | Explicit category, mutation, or verification | Lookup | Current polymorphic describe | resolve_legal_entity_eff_metadata | Prevents guessed fields, contexts, cardinality, and value-set contracts | Refresh the exact branch metadata | Category, context, attributes, labels, cardinality, and value sets |
| LE.CONTEXT | Current context and row | Conditional | Context view, mutation, or verification | Lookup | Fresh canonical child reads | resolve_legal_entity_eff_context | Supplies current values and an unambiguous row selection | Select one row when the context is multirow | Current values and selected-row evidence |
| LE.VALUESET | Enabled canonical EFF value | Conditional | A changed segment declares a value set | Lookup | Current declared value-set lookup | resolve_legal_entity_eff_value_set | Prevents invalid stored values | Choose one enabled exact value | Stored and display value |
| LE.HISTORY | Latest eligible HCM Information change | Conditional | Date-effective deletion | Lookup | Complete current history | resolve_legal_entity_hcm_history | Prevents historical, first-row, future, or complete deletion | Confirm only the eligible range shown by the runtime | Selected range and before-history fingerprint |
| LE.LOADER.ROUTE | Core Data Loader mutation route | Conditional | Every supported mutation or import | Satisfied | Current task manifest |  | Makes Core Data Loader the only mutation executor and approval owner | Do not use direct REST writes | dataloader_import_mode=REST |
| LE.LOADER.OBJECTS | Registered mutation objects | Conditional | Every supported mutation or import | Lookup | Current loader business-object metadata | resolve_legal_entity_loader_contract | Restricts the handoff to applicable configured objects | Use the Legal Employer object, PSU object, or both in manifest order for EFF work; use each object's embedded ModifyOrganizationUnitForChildCorrect correction action or SplitOrganizationUnitForEFFUpdate dated-update action; use only DeleteOrganizationUnitForDTDelete for parent deletion | Selected registered discriminators and action sections |
| LE.LOADER.CONTRACT | Operation-specific DAT contract | Conditional | Every supported mutation or import | Verify | Current UCM templates, loader metadata, affected top-level organization rows, selected EFF context rows, complete delete history, and synchronized OrganizationId | resolve_legal_entity_loader_contract | Prevents copied or stale action structures, wrong correction/update semantics, changed existing-child keys, child keys on a new POST row, and EFF/root locator identifiers in a parent delete | For every EFF edit compare the operation date with the top-level organization start and use ModifyOrganizationUnitForChildCorrect when equal or SplitOrganizationUnitForEFFUpdate when later, including for a new child row. An existing PATCH child retains its fresh OrgInformationId, EffectiveStartDate, and EffectiveEndDate; a new POST child leaves all three blank. For a parent delete require one DeleteOrganizationUnitForDTDelete row with the synchronized organizationId, selected history effectiveStartDate, POST action, content type, and framework version | Exact template sections, keys, operation fields, effective comparison, actions, and immutable-source rules |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | Every applicable dependency is current and unambiguous | Yes, read-only lookups or loader handoff only |
| Needs Input | Required business identity, branch, effective date, row selection, or value is missing | No mutation handoff |
| Blocked | Synchronization, metadata, history, loader object, operation contract, privilege, or environment is unavailable or ambiguous | No |
| Unsupported | Requested parent/classification/physical deletion or another excluded operation is requested | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LE.DEPENDENCIES | decision | 10 | resolve_dependency | ready->LE.DEFAULTS;missing->LE.ERROR;blocked->LE.BLOCKED | LE.ROOTS | stop | Applicable lookup evidence has been collected and readiness must be resolved |
