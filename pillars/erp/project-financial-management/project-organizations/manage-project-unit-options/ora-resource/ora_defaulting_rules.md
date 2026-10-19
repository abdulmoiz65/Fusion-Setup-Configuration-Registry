# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| UserDefinedProjectNumCode, ManualProjectNumType | MANUAL, ALPHANUMERIC | New PU implementation row only, enhanced-numbering feature enabled and NOT obsolete, and values omitted; hidden region alone is insufficient | No; existing/supplied values are preserved by FSCR |  |
| MethodCode, NumberType | MANUAL, ALPHANUMERIC | New PU save finds no automatic-numbering setup row; apply to a new working row only | No; never replace an existing determinant row |  |
| ManualProjectNumType | ALPHANUMERIC | Explicit requested transition to MANUAL in the legacy numbering branch; normalize before preview, not on unrelated updates or merely because method is already MANUAL | Yes, including a supplied conflicting type for that transition; disclose original and result |  |
| SourceCode | ORA_PJF_PROJ_UNIT | A missing project-unit automatic-number determinant row is created | Yes; fixed source discriminator |  |
| Related business units | Preserve current associations | The association list is omitted from an update | No | find_project_unit_options |
| Reporting options | Preserve current values | Reporting fields are omitted from an update and exactly one complete current `PJF_REPORTING_SETUP` row exists | No | find_project_unit_options |
| Optional Prefix | Blank | Automatic numbering is selected and Prefix is omitted | No |  |
| PJF_REPORTING_SETUP.csv.CommitmentStatusPo | R (Approved) | Fresh baseline proves the reporting row is absent and the user omitted this field | No | find_project_unit_options |
| PJF_REPORTING_SETUP.csv.CommitmentStatusReq | N (Not included) | Fresh baseline proves the reporting row is absent and the user omitted this field | No | find_project_unit_options |
| PJF_REPORTING_SETUP.csv.CommitmentStatusSupinv | A (All) | Fresh baseline proves the reporting row is absent and the user omitted this field | No | find_project_unit_options |
| PJF_REPORTING_SETUP.csv.CommitmentStatusExtr | A (All) | Fresh baseline proves the reporting row is absent and the user omitted this field | No | find_project_unit_options |
| PJF_REPORTING_SETUP.csv.PlanamtAllocMethod | S (Period start date) | Fresh baseline proves the reporting row is absent and the user omitted this field | No | find_project_unit_options |
| Seeded reporting parity proposal | No implicit default; display every proposed value | A seeded unit is used only as a parity reference | No; require explicit customer approval | find_project_unit_options |

## Reporting Default Precedence

Apply these UI new-row defaults per field only after the current project-unit baseline establishes that the reporting row is absent. Across prompts, Word, PDF, XLSX, and CSV inputs, distinguish omission from supplied but ambiguous, conflicting, or invalid input. A blank input cell without an explicit clear instruction counts as omission; a requested clear is supplied input and must be validated.

Resolve explicit codes, names, meanings, translations, or ordinary business wording first. Explicit valid intent overrides the default. Exclusion resolves to N; All to A; Approved to R. An explicit request to include Other Commitments resolves to A, matching its checkbox-only UI. An inclusion-only request for PO, requisitions, or supplier invoices does not choose between All and Approved: ask for clarification. Do not use defaulting to conceal ambiguous or invalid input.

For an existing complete reporting row, preserve each omitted field, including N. Do not reapply new-row defaults on update or silently fill an incomplete existing row. Unknown baseline or multiple rows blocks defaulting. Show all resolved, preserved, and defaulted values with their origin in the existing import preview. UI defaults do not bypass package approval or post-import readback; no seeded project's reporting values are copied.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PUOPT.APPLY_DEFAULTS | step | 3 | apply_default | applied->PUOPT.RESOLVE_SET;failure->PUOPT.RETURN_ISSUES | PUOPT.FIND_PROJECT_UNIT | stop | Resolved project-unit baseline, unambiguous input, and explicit target feature status; apply eligible defaults from this file |

## UI Behavior Boundaries

Enhanced numbering hides the legacy numbering region when enabled or obsolete; that visibility condition is broader than the new-row default condition above. Automatic numbering hides Type and shows the next number; other methods reverse that visibility. Hiding a field does not clear its value.

Changing to Manual resets Type to Alphanumeric at that moment. The user may subsequently choose another supported type. An unrelated update to an already-Manual row must preserve its type. For example, an explicit Automatic-to-Manual transition with Numeric becomes Alphanumeric in working input, with both values disclosed. These UI interactions do not establish import behavior.
## Related Business Unit Validation

An addition retains its exact supplied name and is validated by Fusion when the approved FSM package is imported. This task does not default or pre-validate Project Accounting enablement.
