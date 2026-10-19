# Manage Change Order Types Dependency Readiness

Source: user requirements to retain all selected-type dependencies and identify types through exported content. Lookup mechanics are owned by ora_reference_lookups.md.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Selected change type | Resolve its exported identity and base/child relationship |
| 2 | Related rows | Resolve all rows needed by the selected type across dependent files |
| 3 | Header-attribute ownership | Identify header rows before applying the design rule for base or child targets |
| 4 | Default lookup assignment | Resolve every requested priority/reason code before preparing the type package; create a missing code through its mapped task first |
| 5 | Default lookup removal | For an explicit clear request, confirm the requested field currently has a value and validate the blank-field archive; no lookup mutation applies |
| 6 | Attachment category and Change Policy association | When requested for creation, reuse an exact category for `EGO_ENGINEERING_CHANGES_B` or create it through Manage Attachment Categories for Product Management, then verify the exact category is associated with the target Change Policy with its supplied or current-date-defaulted effective Start Date in the final package |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| selected_type | Source for creation or target for update | Yes | Every package | Verify | Supplied export package | resolve_change_type_relationship | Establish package scope and relationship | Resolve exactly the requested change type | selected_type; base_type; relationship |
| related_rows | All related dependent rows | Yes | Every package | Verify | Supplied export package | resolve_change_type_dependencies | Avoid missing-entity errors during import | Retain the complete selected-type dependency set subject to the header-attribute exception | selected_type_rows; dependent_rows |
| header_rows | Header-attribute rows and owner | Yes | Every package | Verify | Supplied export package | resolve_change_type_header_attributes | Apply the target-specific header rule without deleting other dependencies | Resolve header rows before package preparation | header_attribute_rows; header_attribute_owner |
| default_lookup | Enabled mapped lookup code | Conditional | `PriorityCode` or `ReasonCode` is supplied or changed | Verify | Mapped Standard Lookup | resolve_default_lookup | Prevent a type from referencing an unavailable default | Create missing codes through the mapped task, then re-read all requested lookups before type association | field_name; lookup_type; lookup_code; lookup_status |
| default_lookup_removal | Explicit clear request and nonblank current field | Conditional | `PriorityCode` or `ReasonCode` is explicitly cleared | Verify | Selected target header and final ZIP validation | resolve_default_lookup_removal | Prevent accidental clearing or an unsupported blank import | Retain the lookup code and stop if Fusion validation rejects blank | field_name; value_before; clear_validated |
| attachment_category | Exact category and target Change Policy association with an effective Start Date | Conditional | Creating a change order type with `attachment_category` supplied | Resolve and verify | Manage Attachment Categories for Product Management and supplied Change Order Types export | resolve_attachment_category | Prevent creation without the requested attachment-category association | Reuse an existing exact category for entity `EGO_ENGINEERING_CHANGES_B`; otherwise create it with Category Name, User Name, Description, and that entity, then require its exact Change Policy association with a nonblank supplied or current-date-defaulted `StartDate` | category_name; category_identity; entity_name; category_status; association_start_date; association_start_date_source; change_policy_association |


## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COT.RESOLVE_ATTACHMENT_CATEGORY | decision | 25 | resolve_dependency | not_requested->COT.CHECK_DEPENDENCIES;resolved->COT.CHECK_DEPENDENCIES;invalid->COT.REPORT_ISSUES | COT.RESOLVE_EXPORT | stop | A creation request supplies an attachment category, or the category check is skipped because none was supplied |
| COT.CHECK_DEPENDENCIES | step | 30 | resolve_dependency | satisfied->COT.PRESERVE_VALUES;invalid->COT.REPORT_ISSUES | COT.RESOLVE_ATTACHMENT_CATEGORY | stop | A selected-type package is being prepared |
