# Manage Channel Claim Sources Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Operation safety | Create duplicate evidence or exact existing update targets are established |
| 2 | Settlement restrictions | Verify any proposed accounting change against current predefined state |
| 3 | Change boundary | Preserve unrelated records, explicit intent and approved-artifact integrity |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Parent create only | Error | find_claim_source_duplicate | An existing mapping has the same class/source/set tuple | Stop duplicate parent create; this check does not apply to create_child | No automatic upsert |
| create_child | Error | find_settlement_method_duplicate | Any existing child matches the resolved method code or name, or parent identity is unresolved | Stop duplicate child create; classify separately only with explicit user intent. Never create or mutate the parent to add the child | No automatic upsert |
| Update | Error | resolve_existing_claim_source | Parent does not exist or identity is ambiguous or conflicting | Resolve exact existing identity; never fall through to create | No |
| Existing child update | Error | resolve_existing_settlement_method | Child does not exist under selected parent or ownership conflicts | Correct identity; do not add, move or delete child records | No |
| Existing-child update changes AccountingFor, including clear | Error | resolve_existing_settlement_method | Current child is predefined, or predefined status is unknown | Accounting is not editable for predefined methods; resolve unknown state before changing accounting. Do not treat null SeededFlag as false. New-child creation uses the accounting lookup instead | No |
| SettlementMethod changes | Error | resolve_settlement_method | Proposed method does not resolve to exactly one valid name | Resolve exact valid name; do not alter other rows to make room or bypass a Fusion constraint | No |
| Update | Error | | Implicit child replacement, deletion, create fallback, or unrelated changes appear in the intended effect | Preserve other mappings; prepare only explicit permitted existing-record edits | No |
| Any operation | Error | | Live loader does not support exact operation, writable fields, keys or child linkage; or approved evidence/artifact has changed | Report contract gap or restart preparation and approval; no alternate writer | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_claim_source_duplicate | Create | Exact duplicate count | ora_reference_lookups.md |
| resolve_existing_claim_source | Update | Verified existing parent identity | ora_reference_lookups.md |
| resolve_existing_settlement_method | Child update | Verified child identity, ownership and predefined state | ora_reference_lookups.md |
| resolve_settlement_method | SettlementMethod changes | Exact proposed method match | ora_reference_lookups.md |
| find_settlement_method_duplicate | create_child | Verified existing parent and zero child collisions | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CJMCS.VALIDATE_DESIGN | step | 5 | design_enforcement | compliant->CJMCS.APPLY_DEFAULTS;not_compliant->RETURN_ISSUES | CJMCS.RESOLVE_REFERENCES | stop | Enforce operation-specific design rules before readiness preview |
