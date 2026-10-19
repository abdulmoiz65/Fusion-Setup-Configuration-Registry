# Assign Balancing Segment Values to Ledger Defaulting Rules

Derive technical values before package generation from the current task export and authoritative read-only evidence. Do not treat an import error as a default-discovery mechanism.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| LedgerName | Exact name from the one resolved target ledger | Every assignment row | No | resolve_ledger_balancing_segment_context |
| GL_LEDGER.Name | `AssignmentPrimaryLedgerName` from the one matching `GL_SECONDARY_LEDGER` parent row | Every assignment row | No | resolve_ledger_balancing_segment_context |
| GL_SECONDARY_LEDGER.Name | `AssignmentSecondaryLedgerName` from the one matching `GL_SECONDARY_LEDGER` parent row | Every assignment row | No; never preserve a blank exported assignment value | resolve_ledger_balancing_segment_context |
| BalSegValueOptionCode, BalSegColumnName, BalSegValueSetCode in the parent ledger row | Exact current values from the resolved ledger export | A package includes the parent ledger row | No; `A` is a valid source value for a direct specific-value assignment. Preserve it and do not add a manual `A`-to-`I` delta solely for assignment eligibility; Fusion performs any required transition as part of the task | resolve_ledger_balancing_segment_context |
| SegmentTypeCode | `B` from a same-scope UI export row | Every direct balancing-segment assignment row | No | inspect_assignment_task_package |
| SegmentValue (UI label: Company Value) | No default; exact enabled/effective business value selected in the active request and resolved in the balancing value set | Every assignment row | No | verify_balancing_segment_value_exists |
| SegmentValueTypeCode | `S` from a same-scope UI export row | Every direct single-value assignment row | No | inspect_assignment_task_package |
| StartDate | Intentional blank | The active request does not supply a business effective start date | Yes; use the explicitly requested date |  |
| EndDate | Intentional blank | The active request does not supply a business end date | Yes; use the explicitly requested date after StartDate validation |  |
| Prior-request Company Value and dates | Never default from prior conversation, project state, export rows, or another ledger | The active request omits Company Value or either date | No |  |
| LegalEntityIdentifier | Intentional blank | Direct ledger assignment | No; legal-entity values belong to the separate legal-entity task |  |
| SlaSequencingFlag | `N` from a same-scope UI export row | Every direct assignment row unless an explicit supported sequencing design says otherwise | No | inspect_assignment_task_package |
| AttributeCategory and Attribute1 through Attribute15 | Intentional blank | No deployed DFF context and explicit business request exists | No |  |
| Audit, request, record, and object-version fields | Intentional blank | New FSM-import row | No; Fusion owns generated values |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BSVL-040-APPLY-DEFAULTS | step | 40 | apply_default | applied->BSVL-050-ENFORCE-DESIGN;failed->BSVL-070-RETURN-ISSUES | BSVL-030-RESOLVE-DEPENDENCIES | stop | Every package |
