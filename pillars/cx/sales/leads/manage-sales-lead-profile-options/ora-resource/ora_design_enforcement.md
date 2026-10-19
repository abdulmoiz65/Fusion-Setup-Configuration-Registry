# Design Enforcement

## Mandatory Gates

| Gate | Pass Condition | Block Condition |
|---|---|---|
| Live identity | Exact live definition exists and the code is documented, exported, or explicitly reviewed as environment-only | Missing definition, guessed code, or unreviewed unknown code |
| Scope | Site, Product, or User is enabled and updatable; its exact scope key resolves | Disabled/read-only level, guessed application short name, or unresolved user |
| Current-state lock | Latest exact child state equals ExpectedCurrentValue, including explicit not configured for Create | Row changed, appeared, or disappeared after preview |
| CRUD selection | Absent row routes POST; existing row routes PATCH; existing row plus Remove routes DELETE | Upsert hides state, POST targets an existing row, PATCH/DELETE targets an absent row, or parent definition is targeted |
| Stored-value identity | Proposed lookup code, rule code, Copy Map, approver identifier, UserGuid, or AssessTemplateId is exact | Display label is sent where Fusion stores a code or ID |
| Request minimization | Create body contains only required key/value fields; Update contains only ProfileOptionValue; Delete has no body | Audit, parent, definition, validation, level, description, or unrelated fields are sent |
| Approval binding | Approval matches the full canonical preview digest, environment, method, endpoint, target, expected state, and body/delete effect | Vague approval, changed preview, stale state, or different route |
| Delete impact | Preview shows the lower-precedence configured value or delivered behavior that can apply | Delete is described as setting a default or its fallback is undisclosed |
| Bulk uniqueness | Each code/level/level-value tuple appears once and ordered calls stop on first failure | Duplicate target, parallel writes, rollback promise, or continue-after-failure |
| Mutation route | Every Create/Update/Delete uses core.fusion-api.apps-common | FSM ZIP, Data Loader, setup import, browser write, direct curl, or task-local HTTP implementation |
| Verification | Exact child read confirms the approved value or deletion immediately after the response | HTTP acceptance alone, inferred effective value, or skipped verification |
| Current-value authority | Configured values come from exact live children or explicit absence | Documentation default, export-only row, Site fallback, or profileValues is presented as configured state |
| Inventory completeness | Candidate reconciliation, per-code status, paginated definition/level/Site/User/Product reads, timestamps, and conversion-option canary are present | Inventory silently drops candidates or returns documentation/export rows only |
| Review completeness | Exact code, export attempt, live definition, level flags, complete child reads, and timestamps are present | Review returns a default, parent only, or inferred configured value |

## Additional Rules

- Treat export omission as reconciliation evidence only. It never selects or
  blocks the Apps Common mutation route.
- Do not update option definitions, SQL validation, level metadata,
  descriptions, application/module identifiers, or audit fields.
- Do not use `Upsert-Mode=true` for normal CRUD; choose POST or PATCH from the
  exact pre-read so approval describes one deterministic operation.
- For BulkSet, re-read each row immediately before its call. Stop on the first
  stale row, write failure, or verification mismatch and report earlier
  verified successes as partial completion.
- Do not automatically sequence qualification-template deployment,
  assignment-rule publication, Copy Map creation, or security changes.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SPO.DESIGN | decision | 5 | design_enforcement | pass->SPO.EXECUTION_GATE;fail->SPO.RETURN_ISSUES | SPO.ROUTE | stop | After complete Inventory/Review reconciliation or after an exact mutation target, method, endpoint, body/delete effect, dependencies, current-state lock, verification plan, and approval boundary are established |
