# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Preserve seeded parent structure type | Keep the seeded parent structure type active. Do not delete, repurpose, or retire it through this task. For an FSM child addition, carry forward the exact exported parent row; leave it unchanged unless the request changes a parent control. |
| 2 | Add or maintain a child structure name | Retain the seeded parent and add or maintain the child structure name. Use the display name as the internal name when no internal name is supplied, and allow an empty description. In FSM, include the matching parent EGP_STRUCTURE_TYPE row with the child row. |
| 3 | Protect assigned structure names and parent identity | Do not delete or repurpose structure names assigned to items. Preserve the supplied parent StructureTypeId, ensure the archive parent and child use that same identifier, and do not generate a new StructureTypeId when adding a child structure name. |
| 4 | Default optional controls | In FSM CSV, normalize a supplied `LifecycleValidationFlag` to `1` to enable or `2` to disable; when omitted, default it to `2` (false; unchecked). When Use Primary for Expansion is omitted, default it to false (unchecked). |
| 5 | Validate reference designators, attachment categories, and effective-date handling | Keep None unless range behavior is needed. When a range indicator is used, resolve the supplied code or meaning to one enabled, effective lookup value; comma-separated values remain individual reference designators. Validate attachment categories only when one is supplied or the target requires one; use the exact canonical spelling and do not duplicate an existing category. When neither condition applies, preserve the empty attachment list and do not block the design. Require an effective start date for UI execution only. When the FSM template cannot represent it, continue the FSM import without an archive date value and record that handling. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every request affecting the seeded parent structure type | Blocker | | The request would deactivate, delete, or repurpose the parent | Keep the parent active and add or maintain a child structure name for the business need | Yes |
| A structure name is assigned to items | Blocker | | The request would delete or repurpose the assigned name | Keep the assigned structure name unchanged; add a different child name when needed | Yes |
| A child structure name is added through FSM | Blocker | | The archive lacks the matching exported EGP_STRUCTURE_TYPE parent row, or the parent and child do not use the same StructureTypeId | Rebuild the archive with the exact parent row from the same fresh export. Preserve parent values unless requested parent controls also change. | Yes |
| A child structure name is added | Blocker | | The proposed import generates, requires, or changes a StructureTypeId | Preserve the seeded parent identifier and add the child structure name without generating a primary key | Yes |
| Quantity Related is enabled | Mandatory | | The request lacks the business need for reference-designator quantity to match component quantity | Enable only for that stated business need | Yes |
| A Reference Designator Range Indicator other than None is selected | Mandatory | resolve_rd_range_indicator_lookup_value | The supplied code or meaning does not resolve uniquely to an enabled, effective value of lookup type ORA_EGP_COMP_REF_DES_RANGE_IND | Supply an enabled, effective value of ORA_EGP_COMP_REF_DES_RANGE_IND; use it between range endpoints, for example RX01-RX05 | Yes |
| A comma-separated list is supplied | Mandatory | | A comma is treated as the selected range indicator | Treat the list as individual values; use the selected special character only for a range | Yes |
| A structure header attachment category is supplied or required by the target | Mandatory | | A supplied category cannot be resolved to an exact target CategoryName, or a target-required category is missing | Use the exact target CategoryName and add a row only when it is absent from the exported parent configuration | Yes |
| An attachment category is already present in the populated export | Mandatory | | The proposed FSM archive adds a duplicate category row | Preserve the existing canonical category row and omit it from the additive archive | Yes |
| A structure name is added through the UI | Mandatory | | No effective start date is supplied | Obtain the date and include it in the UI runbook before execution | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_rd_range_indicator_lookup_value | A Reference Designator Range Indicator value or range is requested | Enabled, effective lookup code and meaning from ORA_EGP_COMP_REF_DES_RANGE_IND | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| STRUCTURE_DETAILS.ENFORCE_DESIGN | decision | 30 | design_enforcement | compliant->STRUCTURE_DETAILS.DONE;blocked->STRUCTURE_DETAILS.DESIGN_BLOCKED | STRUCTURE_DETAILS.RESOLVE_RD_RANGE_INDICATOR | stop | A validated request to create, retire, or change an item structure type |
