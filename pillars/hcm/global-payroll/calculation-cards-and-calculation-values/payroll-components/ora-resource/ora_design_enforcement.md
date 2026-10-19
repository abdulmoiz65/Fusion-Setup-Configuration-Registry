# Payroll Components Design Enforcement

## Current Authority

Product REST is GET-only. Native HCM Data Loader is the only mutation route,
and only the Parent Create and Reference Child Create field shapes declared in
`ora_input_validation.md` may proceed. Registered ADF REST objects, product
REST mutations, FSM CSV imports, date-effective operations, and unlisted native
packets do not authorize a write.

## Capability Matrix

| Capability | QA Status | Boundary |
|---|---|---|
| Search and read | Ready | Product REST GET using business labels, operation-local verified internal IDs, and the registered expanded or direct reference-read routes |
| Parent Payroll Component Create | Ready | One PayrollDeductionType MERGE, zero child rows, all tax reporting units |
| Wage Basis Rule Reference Create | Ready | One child-only DeductionContextUsage MERGE with UsageType T and a Fusion-selected source owner; load and exact read-back directly proved |
| Calculation Factor Reference Create | Ready for nonproduction QA | Identical child field shape with Fusion-valid UsageType C; capture direct loader/read-back evidence during QA |
| Translation Create | Not applicable | The separate translation object is update-only |
| Calculation Card Reference Create | Unsupported | The native child template has no calculation-component reference field |
| Specific tax reporting unit assignment | Unsupported | No delivered native discriminator for DeductionReportUseRest |
| Correct, Update, or Delete | Deferred | Future development; the current delivery is create-only |
| End Date | Unsupported | Both delivered sections are non-date-effective |

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Classify route | Continue only for read, Parent Create, Wage Basis Rule Reference Create, or the controlled nonproduction Calculation Factor QA case. |
| 2 | Resolve business references | Resolve the environment, LDG, group or parent, context, duplicate state, and Source System Owner through declared resolvers. |
| 3 | Apply defaults | Derive only the declared flags, sequence, journey code, internal IDs, and fresh operation SourceSystemId. |
| 4 | Core preparation boundary | Core Data Loader prepares and normally validates one deterministic immutable DAT/ZIP before Task Hook; this task does not build, upload, or initiate it. |
| 5 | Task contract validation | Validate the same supplied bytes against current Deduction Type metadata, template, exact headers, field allowlist, values, and row counts through PCOMP.VALIDATE_NATIVE_CONTRACT. |
| 6 | Design gate | Evaluate every task-specific blocker using the current resolver and contract-validation evidence. |
| 7 | Approval handoff | Return the Task Hook result to core/data-loader; core owns its internal preview, immutable envelope, authoritative report, and either same-request explicit auto-approval or later contextual approval. |
| 8 | Governed dispatch | Core verifies the persisted artifact, environment and Run Book context, and approved Task Hook envelope, then applies its current upload and initiation policy. |
| 9 | Later verification | After accepted initiation, use the core status workflow only when status or verification is explicitly requested; bind the later task read-back to that same request. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any requested write | Blocker | verify_environment_alias | The target environment is missing, mismatched, or cannot be verified | Select and authenticate the intended configured environment | Yes |
| Parent Create | Blocker | find_payroll_component | Fully paginated duplicate proof is missing or finds an exact Deduction Code plus LDG match | Refresh discovery or use a new business code | Yes |
| Reference Child Create | Blocker | find_payroll_component | The parent is absent, ambiguous, stale, disagrees with the selected code or LDG, or neither registered reference-read route can be established | Select one exact current parent by business code or name and refresh the registered route | Yes |
| Reference Child Create | Blocker | find_reference_children | Duplicate pagination is incomplete or an exact parent plus LDG plus context plus journey business-key row exists | Refresh the collection or select a different business combination | Yes |
| Reference Child Create | Blocker | resolve_active_source_owner | An active effective nonreserved owner was not explicitly selected, became inactive, or no longer resolves exactly | Select one current Source System Owner by Fusion meaning or code and rebuild validation | Yes |
| Calculation Factor Reference Create | Blocker | map_reference_journey | The target is not explicitly selected and verified as nonproduction while direct C native-HDL QA evidence is pending | Use the designated nonproduction QA environment | Yes |
| Parent or child Create | Blocker | verify_native_hdl_contract | The core-supplied immutable archive, current metadata, template, headers, rows, fields, or normal validation evidence differs from the task contract | Rebuild through core/data-loader and rerun Task Hook validation; never broaden the allowlist automatically | Yes |
| Correct, Update, Delete, or another unlisted lifecycle mutation | Blocker | | The request is outside the create-only delivery | Return PCOMP_HDL_ROUTE_FROZEN and record it as future work | No |
| Calculation Card reference, specific tax units, translation Create, or End Date | Blocker | | The delivered native contract lacks the required action, discriminator, field, or date behavior | Return UNSUPPORTED and use no mutation fallback | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| verify_environment_alias | Every operation; explicit nonproduction proof is additionally required for Calculation Factor Reference Create | environmentAlias, environmentFingerprint, environmentClassification, nonProductionVerified | ora_reference_lookups.md |
| map_reference_journey | Reference Child Create | ReferenceJourney, UsageType, qaEvidenceClass | ora_reference_lookups.md |
| find_payroll_component | Parent duplicate check, child parent selection, freshness, and reconciliation | duplicate count or exact parent, registered reference-read route when references are required, and any current links returned | ora_reference_lookups.md |
| find_reference_children | Child duplicate check, freshness, and reconciliation | childDuplicateCount, matching business state, registered collection route, and any current child link returned | ora_reference_lookups.md |
| resolve_active_source_owner | Reference Child Create | SourceOwnerName, SourceSystemOwner; SourceSystemId is derived after selection | ora_reference_lookups.md |
| verify_native_hdl_contract | Every Create | current hierarchy, fields, schema fingerprint, validation results | ora_reference_lookups.md |

## Archive and Approval Boundary

Parent and child creates use separate archives and separate approvals. The
selected Source System Owner meaning and code may be shown only while making
the Fusion LOV choice. Keep surrogate IDs, the generated `SourceSystemId`, the
combined source-key identity, ID-bearing paths, transport payloads,
credentials, token-cache contents, and artifact digests internal. The task
binds them to the immutable envelope but does not prescribe or augment the
user-facing approval report owned by `core/data-loader`. This task performs no
proactive lookup, duplicate, source-owner, or metadata refresh at later
approval time. A known or user-declared target, reference, duplicate, template,
or byte change invalidates the plan as `STALE_PLAN` and requires fresh
validation. Otherwise, later submission performs only the artifact-integrity,
environment and Run Book context, and Task Hook envelope checks owned by core.

Only upload and loader initiation are mutation stages. This task adds no
transport retries, optional initiation fallback, polling, or status calls; it
delegates those mechanics to the current `core/data-loader` contract. An
uncertain write is never replayed. A later explicit status request remains
bound to the original request and returns the core helper report verbatim. A
separate business-verification request after authoritative loader success may
use the task-specific product REST GET reconciliation below.

## Governed Lifecycle Handoff

`PCOMP.READY_FOR_CONFIRMATION` means that Task Hook validation accepted the
immutable artifact; it is not mutation success and it does not itself supply
approval. The shared governed Data Loader lifecycle consumes that result only
after approval accepted under the current core contract, whether that approval
was unambiguously included in the same load request or arrives later as a clear
contextual affirmative. Approval remains bound to the persisted artifact,
environment context, and Task Hook envelope.
The core lifecycle owns upload, initiation, and status reporting. A separate
explicit business-verification request after authoritative loader success may
invoke the reconciliation contract in `ora_error_handling.md`; its result is
never appended to a core helper report. The task registry intentionally stops
at the ready-for-confirmation boundary.

## Execution Ownership

These task-owned `ora-resource` files own Payroll Components validation,
business-label selection, exact create allowlists, Task Hook rule results, and
reconciliation expectations. Shared core capabilities own authentication,
REST transport, deterministic archive preparation, Data Loader validation,
Task Hook invocation, approval rendering, upload, initiation, later status
queries, and generic diagnostics.
This task does not depend on task-local scripts or tests.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PCOMP.ENFORCE_DESIGN | decision | 6 | design_enforcement | compliant->PCOMP.EXECUTION_GATE;noncompliant->PCOMP.HANDLE_ERROR | PCOMP.VALIDATE_NATIVE_CONTRACT | stop | Post-default native-contract validation succeeded and task-specific design rules must be enforced |
