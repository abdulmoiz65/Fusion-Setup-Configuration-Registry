# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Assess existing balances | Review predefined and element-generated balances before creating a custom balance. |
| 2 | Validate LDG-specific design | Confirm category, UOM, currency condition, dimensions, contexts, and localization applicability in the target LDG. |
| 3 | Validate feed design | Confirm compatible UOMs and applicable classification or element/input-value feeds. |
| 4 | Validate HDL structure | Use BalanceId or BalanceCode with the same LDG for child linkage and separate seeded-feed changes from custom-feed changes. |
| 5 | Gate import | Require target metadata, an immutable HDL artifact, and immediate explicit approval before any import. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A new custom balance is proposed | Blocker | find_balance_by_exact_name | The existing-balance assessment has not shown that a predefined or generated balance is unsuitable | Reuse or adapt a valid existing balance where it meets the requirement; create a custom balance only when needed | Yes |
| A parent balance or defined balance is prepared | Blocker | resolve_balance_reference_values | A supplied category, dimension, context, UOM, currency condition, or localization applicability is unverified for the target LDG | Use only values validated for the target LDG and legislation | Yes |
| A classification or element feed is prepared | Blocker | resolve_balance_reference_values | The feed source is absent, LDG-incompatible, or UOM-incompatible | Correct the feed source or balance UOM before HDL preparation | Yes |
| A child record is prepared | Blocker | | Neither BalanceId nor BalanceCode with the same LDG is provided | Use BalanceId (Balance Type ID) or BalanceCode with the same LDG; source-system identifiers are optional | Yes |
| Feed changes are prepared | Blocker | | Seeded and custom balance-feed updates are mixed in one HDL file | Split the updates into separate HDL files | Yes |
| Import is requested | Blocker | resolve_balance_metadata | Target metadata, immutable artifact, target environment, or immediate approval is missing | Complete validation and obtain approval bound to the exact artifact and environment | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_balance_by_exact_name | A custom balance is proposed or an existing balance is selected | Existing balance identity and BalanceId | ora_reference_lookups.md |
| resolve_balance_reference_values | LDG-scoped values or feed sources require validation | LDG, category, UOM, currency condition, dimensions, contexts, classification, element, input value | ora_reference_lookups.md |
| resolve_balance_metadata | Before final HDL preparation or import | Exact business-object discriminator and successful live schema validation | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BAL.ENFORCE_DESIGN | decision | 40 | design_enforcement | compliant->BAL.GATE_HDL_IMPORT;blocked->BAL.HANDLE_DESIGN_BLOCKER | BAL.RESOLVE_DEPENDENCIES | stop | A Balance Definitions HDL request has resolved dependencies |
