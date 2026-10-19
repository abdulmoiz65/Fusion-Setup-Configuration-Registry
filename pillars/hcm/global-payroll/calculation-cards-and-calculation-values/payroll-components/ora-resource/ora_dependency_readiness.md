# Payroll Components Dependency Readiness

## Native HDL Authority

The delivered mutation authority is the native **Deduction Type** Data Loader
business object:

- object type: `ADF_VO`;
- archive member: `PayrollDeductionType.dat`;
- hierarchy: root `PayrollDeductionType`, then optional child
  `DeductionContextUsage`;
- metadata actions for both sections: `MERGE_DELETE`;
- date effectivity for both sections: `None`.

The separate `PayrollDeductionTypeTranslation` business object is update-only
and therefore has no Create gap. Product REST, a registered `ADF_REST` object,
and an FSM setup-task CSV package do not replace this native-HDL authority.
Metadata availability alone never authorizes a write.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Operation and environment | Select read-only discovery or one supported Create profile, plus one configured environment alias without credentials in operation state. |
| 2 | Legislative scope | Resolve one exact LDG business name with its internal ID and legislation code. |
| 3 | Component target | Resolve one Component Group for Parent Create, or one exact existing parent for a component or reference review or Reference Child Create. |
| 4 | Create-specific references | Resolve the child journey and context when creating a reference. |
| 5 | Duplicate state | Complete pagination and prove zero exact duplicates under the operation-specific business key. Sequence is create data, not child identity. |
| 6 | Source owner | For a child Create, require one explicitly selected active Fusion source owner; the fresh operation source ID is allocated later by the defaults node. |

Core archive preparation occurs after task data normalization. Task Hook
contract validation then consumes the exact immutable artifact, and the core
approval, dispatch, and later status lifecycle follows only after that task
validation succeeds. None is resolved by `PCOMP.RESOLVE_DEPENDENCIES`.

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| PCOMP-DEP-001 | Environment alias and classification | Yes | Every request | Verify | Configured project environment and explicit production/nonproduction classification | verify_environment_alias | Prevents cross-environment state reuse and proves the controlled C QA boundary without hostname inference | Select the intended configured environment by alias | environmentAlias, environmentFingerprint, environmentClassification, nonProductionVerified |
| PCOMP-DEP-002 | Legislative Data Group | Yes | Parent or child Create, or scoped component/reference read | Lookup | Current Fusion LDG LOV | find_legislative_data_group | Establishes legislative scope and internal foreign keys | Select an LDG by business name | LegislativeDataGroupId, LegislativeDataGroupName, LegislationCode |
| PCOMP-DEP-003 | Component Group | Yes | Parent Create | Lookup | Current Fusion DeductionGroupRestVO rows | find_component_group | Supplies the required parent foreign key | Select a Component Group by name | ComponentGroupName, DeductionGroupId |
| PCOMP-DEP-004 | Parent duplicate state | Yes | Parent Create | Verify | Fully paginated component discovery in the selected LDG | find_payroll_component | Create requires an unused Deduction Code in the LDG | Use a code with zero exact matches | parentDuplicateCount, duplicateCheckedAt |
| PCOMP-DEP-005 | Existing Payroll Component | Yes | Read-only component/reference review or Reference Child Create | Lookup | Current component discovery plus exact item; a requested reference review or child Create additionally uses the registered expanded or direct child-collection GET | find_payroll_component | Binds every read or child Create to one exact current parent; a requested reference review or child Create additionally requires one registered reference-read route | Select a component by code or name | DeductionTypeId, DeductionCode, parentItemUrl, optional parentSelfLink, referenceCollectionLink, and referenceReadRoute, LegislativeDataGroupId |
| PCOMP-DEP-006 | Reference journey | Yes | Reference Child Create | Lookup | Task-supported business journeys | map_reference_journey | Derives the native usage code without exposing it | Select Wage Basis Rule Reference or Calculation Factor Reference | ReferenceJourney, UsageType, qaEvidenceClass |
| PCOMP-DEP-007 | Reference context | Yes | Reference Child Create | Lookup | Current scoped ContextUsageRestVO rows | find_reference_context | Supplies the required child context foreign key | Select a context by display name | DisplayContextName, ContextId |
| PCOMP-DEP-008 | Child duplicate state | Yes | Reference Child Create | Verify | Fully paginated current child collection joined to context labels | find_reference_children | Prevents duplicate parent, LDG, context, and journey business keys; Sequence is not part of the documented child user key | Choose a business-key combination with zero exact matches | childDuplicateCount, duplicateCheckedAt |
| PCOMP-DEP-009 | Active source owner | Yes | Reference Child Create | Lookup | Current HRC_SOURCE_SYSTEM_OWNER common-lookup codes through core Apps Common Lookups | resolve_active_source_owner | Supplies the proved child source-key owner without hardcoding a tenant value | Select one active owner by business meaning or code | SourceOwnerName, SourceSystemOwner |
| PCOMP-DEP-010 | Deferred lifecycle operation | Yes | Correct, Update, Delete, or another unlisted mutation | Blocked | Current create-only delivery allowlist | | The lifecycle contract is deferred future work | Record the requested operation for future development | routeBlocker |
| PCOMP-DEP-011 | Missing native capability | Yes | End Date, translation Create, Calculation Card reference, or specific tax reporting units | Blocked | Delivered native hierarchy and field set | | The delivered native contract lacks the required action, discriminator, or field | Report UNSUPPORTED and do not substitute a REST write | routeBlocker |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| READY | All mandatory dependencies are exact, current, and source-backed | Yes for reads or preparation of one supported Create plan; no write yet |
| NEEDS_INPUT | A user-owned business choice or free-form value is missing | Read-only lookup or collection only |
| NOT_FOUND | A required exact scoped target lookup returns zero rows | No, except zero exact rows is READY for the explicit Parent Create duplicate check |
| AMBIGUOUS | More than one exact scoped target remains | No; show business-facing distinctions and require selection |
| CONFLICT | A Create duplicate check finds one or more exact matches | No |
| STALE_PLAN | A selected row, link, template, duplicate proof, archive, or internal Task Hook preview is no longer current | Read-only refresh only; invalidate approval |
| CATALOG_MISMATCH | Current metadata conflicts with the declared contract | No; retain sanitized evidence and stop |
| QA_EVIDENCE_REQUIRED | A same-shape Create case is valid but lacks direct native-HDL proof for the requested environment class | No; run the case only in a verified nonproduction QA environment |
| UNSUPPORTED | The request needs an action, field, discriminator, or date behavior absent from the native contract | No |
| PCOMP_HDL_ROUTE_FROZEN | The mutation is outside the current create-only delivery | No |
| READY_FOR_CONFIRMATION | Task Hook checks pass for the exact immutable archive | No write here; return the result to the core/data-loader approval lifecycle |

## Create Command Isolation

- A new `create_parent` or `create_reference` command is never a resume, retry,
  clone, or continuation of an earlier Create.
- Do not reuse LDGs, component groups, parent IDs, context IDs, links, source
  keys, payloads, fingerprints, approvals, or receipts from another operation.
- Prior receipts may be consulted only for duplicate detection or read-only
  reconciliation of that identified operation.
- Parent and child writes are separate dependency graphs and approval units.

## Invalidation Rules

| Changed Value | Invalidate |
|---|---|
| Environment alias | All session-bound reads, IDs, links, metadata, internal preview, approval, and receipts from the other environment |
| LDG | Legislation, groups, components, contexts, duplicate evidence, and internal preview |
| Component Group or parent | Target IDs, registered reference-read routes, child links, duplicate evidence, internal preview, and approval |
| Reference journey or context | Child packet, duplicate evidence, fingerprint, and approval |
| Sequence or Display in Overview | Child packet, fingerprint, and approval; the documented child business key is unchanged |
| Template, archive bytes, or resolved reference | Fingerprint and approval |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PCOMP.RESOLVE_DEPENDENCIES | decision | 2 | resolve_dependency | ready->PCOMP.RESOLVE_REFERENCES;blocked->PCOMP.HANDLE_ERROR | PCOMP.VALIDATE_INPUT | stop | Input validation succeeds |
