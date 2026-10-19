# Error Handling

This resource owns direct QSC Site-value failure disclosure and the approval
gate. It does not authorize an Apps Common write or a Data Loader import.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Direct QSC input is missing or invalid | Stop before preview and request the exact missing profile code, Site level, or, when a value is being provided, organization code or name. |
| A reported QSC value code cannot resolve to exactly one Inventory Organizations name | Stop the report as unresolved; do not return the profile value as a code-only sales organization. |
| Required code-or-name validation returns zero active master-organization matches | Report the configured value as unverified when applicable. Prompt the user to identify or create the item master through Manage Item Organizations; do not create it as a side effect. |
| A value supplied without identifying whether it is an organization code or name returns multiple matches | Ask the user whether the supplied value is an organization code or organization name, then rerun only that field match. |
| Field-specific validation returns multiple matches, code and name resolve to different records, or a REST access/data-security failure | Stop as a validation blocker; do not substitute an FSM list, browser LOV, or raw SQL result. |
| A direct Site-value change lacks a current approved route and approval | Stop as an approval blocker and present the missing execution-route or approval requirement. |
| A removal request finds no QSC Site child | Report that the profile value is already unset; do not issue a DELETE. |
| Approval for the Manage Item Organizations export is missing or declined | Do not run the export. Explain that the complete valid-organization list cannot be provided without an approved export. |
| The Site value or its absence changes after preview | Invalidate the preview and approval, re-read the value, and require a new immutable preview. |
| Apps Common reports an authentication, authorization, transport, Fusion API, or indeterminate write failure | Preserve redacted status and ECID/request ID when returned, perform one configured-value verification read, and do not retry the mutation. |
| Post-mutation verification differs from the approved result | Report a verification failure and do not issue a compensating write. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Item-master identity is unresolved | Do not select an arbitrary organization or substitute a value. |
| A prerequisite is unavailable | Do not create a location, item organization, unit of measure, or spoke-system setting as a side effect. |
| A direct write is failed or indeterminate | Do not retry, replay, or submit a compensating write without a new exact approval and idempotency review. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| QSC.PROFILE.REPORTED | terminal | 3 | terminal | none | QSC.PROFILE.VALUE_NAME | continue | Report the QSC profile value as the resolved OrganizationCode and OrganizationName pair |
| QSC.PROFILE.MASTER_ORG_MISSING | decision | 5 | error_handler | prompted->QSC.PROFILE.BLOCKED | QSC.PROFILE.ITEM_ORGANIZATION | stop | Run only when a direct QSC request provides an organization for QSC_SALES_PRODUCTS_INVENTORY_ORG_ID; disclose the missing item-master prerequisite before retrying validation |
| QSC.PROFILE.EXECUTION_GATE | decision | 8 | execution_gate | ready->QSC.PROFILE.READY;blocked->QSC.PROFILE.BLOCKED | QSC.PROFILE.DESIGN | stop | Run only for a direct QSC_SALES_PRODUCTS_INVENTORY_ORG_ID Site-value mutation; require an approved execution route and current approval |
| QSC.PROFILE.READY | terminal | 9 | terminal | none | QSC.PROFILE.EXECUTION_GATE | continue | All documented direct QSC planning and approval gates are satisfied; hand off the unchanged approved request to Apps Common |
| QSC.PROFILE.UNSET_EXECUTION_GATE | decision | 10 | execution_gate | ready->QSC.PROFILE.UNSET_READY;already_unset->QSC.PROFILE.ALREADY_UNSET;blocked->QSC.PROFILE.BLOCKED | QSC.PROFILE.INPUT | stop | Run only when a direct QSC request asks to remove QSC_SALES_PRODUCTS_INVENTORY_ORG_ID; read the Site child, require an approved DELETE preview when it exists, and require current approval |
| QSC.PROFILE.UNSET_READY | terminal | 11 | terminal | none | QSC.PROFILE.UNSET_EXECUTION_GATE | continue | The existing Site child has an unchanged approved DELETE preview; hand off the deletion to Apps Common and verify its absence afterward |
| QSC.PROFILE.ALREADY_UNSET | terminal | 12 | terminal | none | QSC.PROFILE.UNSET_EXECUTION_GATE | continue | The QSC Site child is absent; report the profile value as already unset without issuing a DELETE |
| QSC.PROFILE.BLOCKED | terminal | 13 | terminal | none | none | continue | An input, lookup, dependency, design, execution-route, or approval requirement blocks the direct request |
| QSC.PROFILE.FAILED | terminal | 14 | terminal | none | none | continue | A documented validation or lookup operation fails |
