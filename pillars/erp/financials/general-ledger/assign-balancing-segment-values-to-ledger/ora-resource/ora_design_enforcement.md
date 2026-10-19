# Assign Balancing Segment Values to Ledger Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm direct-ledger scope | Treat the row as a nonlegal-entity transaction assignment, not a legal-entity assignment |
| 2 | Confirm specific-value configuration | Use the exact resolved ledger balancing-segment metadata and preserve the export contract |
| 3 | Confirm eligibility | Verify the proposed value is not assigned to a legal entity before preview |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every direct ledger assignment | Blocker | verify_balancing_segment_value_exists | The Company Value is absent, inactive, ineffective, assigned to a legal entity, or lacks authoritative assignment evidence | The UI's Legal Entity Company Value Assignments grid is reference context only. Use the legal-entity task for legal-entity values; add only eligible values in the Ledger Company Value Assignments grid for nonlegal-entity transactions such as adjustments | Yes, by changing scope or supplying authoritative evidence |
| A Company Value and LedgerName are supplied | Blocker |  | The request does not explicitly identify direct-ledger intent, or it explicitly names a Legal Entity | Ask the user to confirm direct-ledger versus Legal Entity assignment. This task may continue only for explicit direct-ledger intent; a Legal Entity request belongs to Assign Balancing Segment Values to Legal Entities. | Yes, by confirming direct-ledger intent or selecting the Legal Entity task |
| A Company Value is supplied for assignment | Blocker | list_current_ledger_assignments | The target ledger already has the same Company Value in an overlapping effective period | Return the existing assignment and do not generate a duplicate package. A value preview may flag current assignments but cannot authorize an import. | Yes, by selecting an unassigned value or changing dates so they do not overlap |
| The requested ledger resolves as SECONDARY | Blocker | resolve_primary_ledger_export_scope | Its exact owning primary ledger was not supplied and verified | Ask for the owning primary ledger and obtain the primary-scoped export. Do not guess the relationship, use an unscoped export, or submit the secondary ID as PRIMARY_LEDGER_ID. | Yes, by supplying and verifying the owning primary ledger |
| The resolved parent ledger has BalSegValueOptionCode A | Allowed | resolve_ledger_balancing_segment_context | None solely because the current source value is A | Keep the exact exported parent metadata. A specific direct assignment can cause Fusion to apply the required option transition as part of the task; do not manufacture a separate A-to-I parent change. | Not applicable |
| Every package that changes a parent ledger row | Blocker | resolve_ledger_balancing_segment_context | Parent BalSegValueOptionCode, BalSegColumnName, or BalSegValueSetCode is invented, stale, or differs from the exact resolved ledger evidence without an approved ledger-design change | Preserve current ledger metadata; do not use this task to redesign the ledger | Yes, by removing the unsupported parent-row delta |
| Every assignment row | Blocker | inspect_assignment_task_package | The row uses undocumented technical values, unsupported columns, or copied audit/service fields | Retain only the supported object fields and documented/defaulted values | Yes, by regenerating from the validated package contract |
| Every assignment row | Blocker | resolve_ledger_balancing_segment_context | `GL_LEDGER.Name` or `GL_SECONDARY_LEDGER.Name` is blank, differs from the one matching `GL_SECONDARY_LEDGER` parent row, or is copied from an unrelated ledger | Derive both technical parent keys from the selected ledger's matching parent row. Do not add every secondary ledger to the import package. | Yes, by regenerating the row with the resolved parent keys |
| Every rebuilt task ZIP | Blocker | inspect_assignment_task_package | A changed CSV member is moved, renamed, omitted, or reordered relative to the validated same-task baseline | Preserve the baseline ZIP member names and order; replace only the intended CSV content and retain all required package members | Yes, by rebuilding from the validated baseline |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_ledger_balancing_segment_context | Before any parent-ledger field is preserved or changed | Exact ledger balancing-segment option, column, and value-set metadata | ora_reference_lookups.md |
| verify_balancing_segment_value_exists | Before every direct ledger assignment | Exact value-set value and enabled/effective status, followed by legal-entity-assignment result | ora_reference_lookups.md |
| list_current_ledger_assignments | Before every direct ledger assignment and when previewing values | Exact target-ledger assignments and effective-date overlap result | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BSVL-050-ENFORCE-DESIGN | decision | 50 | design_enforcement | passed->BSVL-060-RETURN-SUCCESS;blocked->BSVL-070-RETURN-ISSUES | BSVL-040-APPLY-DEFAULTS | stop | Every package |
