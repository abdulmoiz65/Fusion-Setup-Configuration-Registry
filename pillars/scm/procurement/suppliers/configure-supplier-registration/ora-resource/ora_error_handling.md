# Configure Supplier Registration Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required scope or configuration decision is missing | Stop and request only the missing flow, component state, source default, identifier decision, attachment decision, or site-assignment decision |
| A component state is unsupported or an edit is requested for Organization Details or Contacts | Stop, identify the component-specific allowed states, and retain the read-only component value shown by the setup page |
| External-registration URL encryption-key regeneration is requested without explicit approval | Stop and request approval that identifies the target environment and acknowledges that existing registration URLs expire |
| Data Loader preview identifies an invalid or unsupported value | Stop, show the affected configuration item and validation result, correct the input, and preview again |
| A shared supplierOptions lookup is stale, missing, ambiguous, or conflicts with another task's proposed attribute value | Stop this task, retain the conflict evidence, re-read the singleton after the preceding task completes, and obtain one resolved final value before preparing a new Data Loader artifact |
| A shared supplierEntityConfigurations row is stale, missing, ambiguous, or includes another task's attributes | Stop this task, re-read the entity configuration after the preceding task completes, and prepare a new Data Loader artifact containing only RegistrationProspectiveCode and RegistrationSpendAuthorizedCode. |
| Data Loader processing fails or has an uncertain result | Preserve the redacted process evidence and reconcile through the supported setup-data workflow before any new submission |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A required configuration decision or accepted state is missing or invalid | Correct the identified input |
| Design policy | A flow, component, attachment scope, or mutation route violates an enforced rule | Correct the design or route through core.data-loader |
| Approval blocker | External-registration URL encryption-key regeneration lacks explicit approval | Obtain approval or exclude regeneration from the configuration change |
| Shared singleton conflict | A shared supplierOptions row is stale, unresolved, or has overlapping task values | Resolve ownership or the final value, then restart the affected task from its read-only lookup |
| Shared entity-configuration conflict | A shared supplierEntityConfigurations row is stale, unresolved, or includes attributes owned by Configure Supplier Profile Change Request | Re-read the row and restart the affected task with owned attributes only |
| Data Loader processing | Preview, import, or verification returns a failure or uncertain status | Stop before retry and inspect supported process evidence |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Mutation request | Do not invoke a supplier-registration REST write or custom REST action directly |
| Registration URL encryption-key regeneration | Do not invoke the custom action directly; use the approved setup-data workflow and obtain explicit approval before any action that expires registration URLs |
| Shared supplierOptions runbook | Do not run this task in parallel with Configure Supplier Profile Change Request or Configure Supplier Notifications, do not include another task's unapproved fields in its Data Loader artifact, and do not create, bootstrap, or delete the seeded singleton row |
| Shared supplierEntityConfigurations row | Do not run this task in parallel with Configure Supplier Profile Change Request, and do not include InternalChangeMgmtCode, SupplierInitiatedChangeMgmtProspectiveCode, or SupplierInitiatedChangeMgmtSpendAuthorizedCode in its Data Loader artifact. |
| Uncertain Data Loader outcome | Do not blindly resubmit the configuration |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POZ.SR.EXECUTION_GATE | decision | 40 | execution_gate | ready->POZ.SR.DONE;not_ready->POZ.SR.HANDLE_ERROR | POZ.SR.ENFORCE_DESIGN | stop | Before submitting through core.data-loader |
| POZ.SR.HANDLE_ERROR | step | 50 | error_handler | handled->POZ.SR.RETURN_ISSUES | none | stop | Any validation, design, preview, import, or verification failure |
| POZ.SR.RETURN_ISSUES | terminal | 60 | terminal | none | none | stop | A blocking issue was disclosed |
| POZ.SR.DONE | terminal | 70 | terminal | none | POZ.SR.EXECUTION_GATE | stop | All resource checks passed and the supported execution gate is ready |
