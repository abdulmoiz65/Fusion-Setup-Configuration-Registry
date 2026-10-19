# Features by Country or Territory Dependency Readiness

Evaluate dependency evidence for the invoking runbook's selected phase after
the applicable resolvers in ora_reference_lookups.md have run. This file owns
prerequisite readiness, not lookup requests, defaults, business-policy decisions,
or an independent execution route.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Active workflow and environment | The router/runbook selects the task and its read or core.data-loader operation. Complete identity, privilege, catalog, source, destination, and approval-requirement preflight through that workflow; submission approval follows final validation |
| 2 | Legislation resolution | Resolve requested names/codes and retain candidate groups, canonical names, and codes before existence decisions or territory-specific option resolution |
| 3 | Complete current-state evidence | Use the applicable main resolver to retrieve the requested result set, exact existing identities, all required business fields, and completeness evidence |
| 4 | Applicable editable-value evidence | Resolve requested or default-display options through their authoritative LOVs; supply the resolved territory for write-style validation |
| 5 | Task business rules | Evaluate defaults in ora_defaulting_rules.md and scope, branch, eligibility, preservation, no-op, and open-decision gates in ora_design_enforcement.md |
| 6 | Deployed registration and template | Before a write, core.data-loader must establish that the exact registered BO, current template, item identifiers, and required internal surrogate derivation support the intended operation |
| 7 | Final immutable artifact | The runbook/core.data-loader produces the artifact using the established profile, completes Task Hook validation, then follows the authoritative approval and submission boundary |
| 8 | Later verification evidence | When the workflow selects verification, use submitted identities, approved desired values, preserved baseline, actual loader results, and complete post-read evidence |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| legislation_identity | Resolved Legislation candidates | Conditional | Names/codes are requested for Search, details, Create, Update, Delete, UPSERT, or available-to-Create selection | Lookup | Current Fusion Legislation LOV | resolve_legislation_by_exact_value | A display alias is not the target identity | Supply the intended name/code context; unresolved candidate decisions belong to design enforcement | Canonical TerritoryCode and TerritoryShortName with candidate/completeness evidence |
| configured_records | Current configuration set | Conditional | Main Search, details, existence classification, available-to-Create listing, final pre-approval reread, or post-operation verification is selected | Lookup | Current Fusion primary collection | find_features_by_criteria | Existence and exact existing identity require complete successful reads | Retain unknown outcomes as unknown and obtain missing evidence before dependent decisions | ApplicationId, LegislationCode, territory identity, current business attributes, and read completeness |
| selected_extension | Selected Extension code and Meaning | Conditional | A requested extension or a displayed current/default extension requires resolution | Lookup | Current Fusion Selected Extension LOV | resolve_selected_extension | Display labels and stored codes must remain distinct, including the null default label | Use the returned option evidence; D01 still governs unresolved null/PER semantics | PayrollLicense candidate code and current Meaning |
| address_style_search | Observed Search style context | Conditional | An Address Style Search criterion or label needs resolution under the documented Search context | Lookup | Current Fusion Address Style LOV in the source's observed US context | resolve_address_style_search | The observed context is not global style authority | Disclose limited scope and return D02 for unsupported global discovery | Style code/name candidates with their scope |
| address_style_target | Target-specific Address Style | Conditional | A Create, Update, or UPSERT style/default is validated or a target-specific label is required | Lookup | Current Fusion territory-specific Address Style LOV | resolve_address_style_by_territory | A generic style label does not establish validity for a target territory | Retain the resolved territory and use its returned choices | Valid target style codes and names |
| address_validation | Address Validation code and Meaning | Conditional | A supplied, current, or default Yes/No value requires validation/presentation | Lookup | Current Fusion PQH_YES_NO LOV | resolve_address_validation_value | The user-facing value must resolve through authoritative lookup evidence | Supply the intended option; preserve its internal code separately | AddressValidation code and Meaning |
| null_extension_search | Null/PER search contract | Conditional | A request needs the still-open combined/default extension Search semantics | Blocked | Source decision D01 and its required query evidence remain unresolved | resolve_selected_extension_null_search | A successful null reset does not prove a search predicate or equivalence policy | Resolve D01 and T06 in a later authoring update | Confirmed search semantics and expression |
| deployed_bo | Current registered BO and template | Yes for writes | Create, Update, Delete, or UPSERT reaches core.data-loader preflight | Blocked | The governing core.data-loader live metadata/template validation result; not a historical ZIP or HAR | | The source requires the deployed registration and current template before loading | Have the selected core.data-loader step validate registration. Block only while required proof is absent or mismatched; never repair metadata automatically | Exact registered BO identity, compatible current profile metadata, validation outcome |
| surrogate_derivation | Internal LegislationApplicationKey derivation | Yes for PATCH | Update or an existing UPSERT branch reaches loader preflight | Blocked | Deployed surrogate user-key registration checked by the governing core.data-loader workflow | | The task supplies ApplicationId and LegislationCode while the deployed BO resolves its surrogate | Require the recorded derivation to be deployed and compatible. A historical successful fixture is not current deployment proof | Matching registered user keys, internal item-key derivation readiness, or diagnostic blocker |
| verification_context | Submitted plan and baseline | Yes for verification | Later business verification is explicitly selected by the active workflow | Blocked | The invoking workflow's approved submitted plan, retained baseline, actual processing results, and current resolver evidence | find_features_by_criteria | Verification cannot infer requested values or prior success from a record count | Obtain missing plan/baseline/result evidence; do not replace unavailable values with defaults | Per-target action, desired/preserved values, processing outcome, and post-read comparison evidence |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Applicable dependency evidence exists, is complete, and matches the current phase/environment | Continue through declared task rules; no mutation is implied |
| Lookup | An applicable live value or current state must be resolved | Only the named read-only resolver selected by the active workflow |
| Blocked | Required evidence, contract, deployed registration, or current identity is absent, ambiguous, incomplete, or mismatched | Stop the dependent action and return the exact missing evidence or decision |
| Not applicable | The dependency is unnecessary for this operation/phase | Skip without synthesizing values or invoking unrelated APIs |

The Blocked registration and verification rows are runtime prerequisite gates.
They are satisfied only by the corresponding successful evidence; they do not
assert that any particular deployment is currently broken or grant permission
to discover it outside the selected workflow. The unresolved D01 contract is a
separate authoring blocker.

## Registered BO Contract

| Property | Source Contract | Boundary |
|---|---|---|
| Business Object | payrollFeaturesByTerritoryOrCountry | Resolve the exact deployed registration through core.data-loader |
| Create row action | POST | The DAT data-row operation is MERGE; explicit RestAction selects the intended action |
| Update row action | PATCH | Existing identity is retained; no automatic backend UPSERT is inferred |
| Delete row action | DELETE | The task uses the minimal key profile after eligibility checks |
| Item identifier order | ApplicationId, LegislationCode | Use the exact existing record's values, not the Create ApplicationId constant for all existing rows |
| Configured item path | /payrollFeaturesByTerritoryOrCountry/<ApplicationId>,<LegislationCode> | Registration documentation only; not a direct REST write route |
| Internal surrogate | LegislationApplicationKey | Preserve BO metadata and derivation; omit from task DAT input |
| Surrogate user keys | ApplicationId and LegislationCode | Registered bind names must match the attributes exactly |
| DAT profiles | DELETE-KEYS, UPDATE-OPTIONS, FULL-CREATE-MIXED | Exact column/shape contracts are owned by ora_input_validation.md |
| Write executor | core.data-loader through the task's routed workflow | No direct REST mutation, database query, alternate loader, or automatic registration change |

## Internal Derivation Evidence

The supplied source records this working registration query. It is metadata
evidence for the BO owner, never SQL to execute during task runtime.

```sql
SELECT TO_CHAR(APPLICATION_ID) || ',' || LEGISLATION_CODE
FROM PAY_INSTALLED_LEGISLATIONS
WHERE APPLICATION_ID = :ApplicationId
  AND LEGISLATION_CODE = :LegislationCode
```

| Evidence | Established Fact | Remaining Limit |
|---|---|---|
| Source E09 | Recorded PATCH succeeded after configuring the surrogate user-key derivation | Current deployment and any template-exclusion change still require their own evidence |
| Source E04 and supplied Delete ZIPs | The tested Delete profile omits the derived surrogate input | Does not establish other BOs' Delete behavior |
| Supplied seven operation ZIPs | Packaged profiles match source E02-E07 | Does not establish current metadata, privilege, atomicity, or post-load state |
| Proposed template cleanup D03/T05 | Display/template omission is distinct from BO metadata and payload exclusion | No registration flag or physical template is changed by resource authoring |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FBCT.RESOLVE_DEPENDENCIES | step | 30 | resolve_dependency | ready->FBCT.APPLY_DEFAULTS;blocked->FBCT.HANDLE_ISSUES | FBCT.RESOLVE_REFERENCES | stop | Evaluate only the dependencies required for the selected phase from declared resolver and workflow evidence |
