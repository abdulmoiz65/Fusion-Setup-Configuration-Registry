# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Project unit cannot be resolved exactly once | Stop and show supplied identity plus match cardinality |
| Required default set is missing or ambiguous, or its required lookup is incomplete | Stop and show requested set intent, resolver match count, and sanitized current-target REST lookup diagnostics; do not require a separate reference-data-set export |
| Numbering method and conditional fields conflict | Reject the numbering change and show required Method/Type/NextNumber combination |
| Automatic NextNumber conflicts with another determinant | Stop before package generation and show the conflicting determinant evidence |
| Fusion rejects a requested business-unit relationship | Persist the Fusion error with the package checksum and row identity; do not retry automatically |
| Relationship removal is nondeletable or used | Preserve it and disclose the project/template usage gate |
| Reporting inclusion and status conflict | Reject the affected commitment row |
| Project unit exists but `PJF_REPORTING_SETUP` has no row | Mark Task 2 incomplete, resolve explicit reporting intent and default omitted fields using ora_defaulting_rules.md; ask only about ambiguous, conflicting, or invalid supplied input, prepare only the missing same-task row from a fresh target template, and require post-import export/readback before downstream use |
| Package validation or Data Loader import fails | Report target, checksum, stage, task member, row identity, and Oracle message; do not retry automatically |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required, conditional, method/type, status, or basis rule fails | Correct the named field |
| Dependency readiness | Project unit, complete reporting row, required set resolution, removal usage evidence, feature status, current export, or package is missing | Collect or correct the named target prerequisite; use the set resolver for membership |
| Fusion validation | Fusion rejects determinant uniqueness, relationship usage, reference set, or reporting semantics | Preserve message and correct setup data |
| Unsupported operation | Set-assignment mutation, project-unit delete, or direct REST option write is requested | Stop and provide the separately supported route |
| Approval blocker | Immutable preview is missing, changed, or declined | Stop without importing |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Numbering normalization and warning | Original versus resulting working values, feature enabled/obsolete state, and whether a method transition or missing row triggered the rule. The UI manual-numbering warning is informational, not an approval gate or evidence that Cancel will undo a completed save. |
| Validation result | Operation, project-unit identity, current/create resolution, set, numbering feature/method/type/next number, BU additions/removals, reporting values, dependencies, and rejected fields |
| Immutable import preview | Target, package checksum, operation, project-unit identity, every changed option, relationship, reporting flag/status, numbering determinant, member row counts, and warnings |
| Import result | Target, checksum, Data Loader stage/status, task members, row identities/counts, and Oracle errors |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Related-BU list is omitted | Do not interpret omission as remove all |
| Relationship is used or nondeletable | Do not remove it or bypass the source gate |
| Numbering feature status is unknown | Do not guess the owning setup surface or apply hidden-region defaults |
| Set-assignment fields are supplied | Do not place them in this task package |
| A direct REST write is requested | Do not infer write support from read-only project-unit fields or adjacent resources |
| Preview approval is absent or package changed | Do not invoke core.data-loader |
| Import fails | Do not retry automatically or mutate the approved package |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PUOPT.EXECUTION_GATE | decision | 9 | execution_gate | ready->PUOPT.RETURN_SUCCESS;not_ready->PUOPT.RETURN_ISSUES;declined->PUOPT.RETURN_REFUSAL | PUOPT.ENFORCE_DESIGN | stop | Return validation output, or require immutable preview and approval before import |
| PUOPT.RETURN_SUCCESS | terminal | 10 | terminal | none | PUOPT.EXECUTION_GATE | continue | Validation is complete or an approved package is ready for core.data-loader |
| PUOPT.RETURN_ISSUES | terminal | 11 | terminal | none | none | continue | A correctable validation or dependency issue blocks progress |
| PUOPT.RETURN_REFUSAL | terminal | 12 | terminal | none | none | continue | Unsupported operation or declined approval |
## Related Business Unit Validation

Fusion is the source of truth for addition eligibility. A Fusion rejection is a load failure, not a reason to alter or retry the approved package automatically.
