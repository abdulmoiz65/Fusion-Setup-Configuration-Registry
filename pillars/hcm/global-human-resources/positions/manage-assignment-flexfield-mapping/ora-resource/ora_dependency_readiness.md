# Manage Assignment Flexfield Mapping Dependency Readiness

## Purpose

Defines the ordered runtime, current-state, template, reference, and approval
dependencies for Manage Assignment Flexfield Mapping.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Environment and runtime read contract | Confirm the connected target and discover current read resources |
| 2 | Current mapping state | Page the mapping collection before matching or preview, and retain the exact FlexSegmentMappingId for child update or delete grouping |
| 3 | Live CUD template | Fetch the registered raw UCM DAT template before assembling any create, edit, or delete source |
| 4 | Referenced setup | Resolve supplied source and destination contexts and segments |
| 5 | Data Loader route | Confirm AssignmentFlexfieldsMapping is the registered business object for CUD |
| 6 | Mutation approval | Confirm the current preview and explicit approval before Core Data Loader execution |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| afm_read_contract | Current mapping read contract | Yes | Every request | Lookup | Target Fusion runtime metadata and collections | read_assignment_flex_mappings | Prevents matching from a partial or stale snapshot and supplies the existing grouping ID when required | No user action unless the connected read is unavailable | Current mappings and the exact FlexSegmentMappingId for update or delete child rows |
| afm_cud_template | Raw registered CUD DAT template | Yes | create, edit, or delete | Lookup | Current Data Loader business-object metadata and UCM content | fetch_assignment_flex_mapping_loader_template | Prevents an inferred or compact sample from changing the current runtime action shape | Restore the registered template access or correct the registered template | Raw headers, action-section order, and allowed SourceRef omission set |
| afm_context_segment | Position and Assignment flexfield context and segment | Conditional | Create or edit supplies a source or destination value | Lookup | Current flexfield actions | resolve_assignment_flex_context_segment | Prevents unsupported segments and invalid scope pairings | Provide exact context and segment values | Current action-supported context and segment values; Fusion validates unavailable datatype, precision, and value-set compatibility during the submitted load |
| afm_loader | Registered Data Loader business object | Yes | Create, edit, or delete | Verify | Registered Data Loader metadata |  | Ensures CUD uses the approved mutation route | Register or restore AssignmentFlexfieldsMapping | Registered business object name |
| afm_approval | Exact mutation approval | Yes | Create, edit, or delete | Verify | Current preview and target context |  | Prevents unapproved or stale CUD | Approve the exact target, selector, delta, and impact | Approval, target, operation, and selector |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Every applicable dependency has exact authoritative evidence | No |
| Lookup | A documented read-only resolver can resolve an applicable dependency | Read-only lookup only |
| Verify | A registered business object or approval must be confirmed | No |
| Not Applicable | A dependency condition is false | No |
| Needs Input | A required selector, value, or approval is missing | No |
| Unresolved | A lookup has no match, multiple matches, unavailable evidence, or an invalid context-scope pairing | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AFM.DEPENDENCIES | decision | 5 | resolve_dependency | ready->AFM.DEFAULTS;not_required->AFM.DEFAULTS;needs_input->AFM.ERROR;unresolved->AFM.ERROR | AFM.CONTEXT_SEGMENT | stop | After applicable mapping, template, context, and segment reads |
