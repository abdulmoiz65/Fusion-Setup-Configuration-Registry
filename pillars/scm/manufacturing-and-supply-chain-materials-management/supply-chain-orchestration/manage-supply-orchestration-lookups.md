---
task_code: "ORA_DOS_MANAGE_SUPPLY_ORCHESTRATION_LOOKUPS"
task_name: "Manage Supply Orchestration Lookups"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.supply-chain-orchestration"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Supply Chain Orchestration"
functional_area_code: "ORA_DOS_SUPPLY_CHAIN_ORCH"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Supply Orchestration Lookups

## Purpose

Route this pillar's lookup work to the shared Application Common Features
capability. This task owns its scope and filtering conditions; it does not own
Fusion authentication, REST transport, endpoint selection, or mutation logic.

## Task Context

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area: `Supply Chain Orchestration` (`ORA_DOS_SUPPLY_CHAIN_ORCH`)
- Setup task: `Manage Supply Orchestration Lookups`
  (`ORA_DOS_MANAGE_SUPPLY_ORCHESTRATION_LOOKUPS`)

## Lookup API Routing

Route every Manage Supply Orchestration Lookups request to
`core.fusion-api.apps-common` (`skill_id: "core.fusion-api.apps-common"`).
The Apps Common router selects its `lookups` nested skill and the appropriate
common, standard, generic, or set-enabled workflow. Do not select a direct REST
endpoint here or assume that all lookup types use the same view.

Pass the following task-specific context in the core request:

- `lookup_types`: the explicitly requested subset of the allowlist below; for
  an approved lookup listing without a subset, pass all 23 types.
- `lookup_view`: only when already validated for the requested type; otherwise
  let Apps Common perform its declared lookup-view discovery.
- expected customization category: the category assigned below for each type.
- requested fields: `LookupType`, `Meaning`, and `Description`

### Approved Lookup Types

These categories reflect the pillar developer's supplied scope. `Extension`
and `Extensible` in that input are grouped as **User Extensible Lookups**.
Blank rows and `NIL` are placeholders, not lookup types. Preserve the exact
identifiers below, including `SUPLY`, `REQST`, and `RQST` spellings.

#### User Extensible Lookups

- `ORA_DOS_TARGET_SYSTEM_TYPE`
- `ORA_DOS_DOCUMENT_TYPE`
- `ORA_DOS_RDD_INTRVL`
- `ORA_CTO_CATALOG_COPY_REQUEST`
- `ORA_CTO_CONFIG_TYPE`
- `ORA_CTO_COPY_ENTITY_TYPE`

#### System Lookups

- `ORA_DOS_INTERACTION_TYPE`
- `ORA_DOS_SUPPLY_REQUEST_STATUS`
- `ORA_DOS_SUPPLY_LINE_STATUS`
- `ORA_DOS_SUPPLY_ORDER_SOURCE`
- `ORA_DOS_SUPPLY_ORDER_STATUS`
- `ORA_DOS_COMP_REPORT_VIEW_BY`
- `ORA_DOS_COMP_REPT_STATUS_OPT`
- `ORA_DOS_LINES_VIEW_BY`
- `ORA_DOS_ORCH_PROCESS_VIEW`
- `ORA_DOS_REPORT_DISP_QTY`
- `ORA_DOS_SUPLY_REQST_FLOW_TYPES`
- `ORA_DOS_SUPLY_REQST_STATUSES`
- `ORA_DOS_SUPLY_RQST_SUBFL_TYPES`
- `ORA_DOS_SUPPLY_DEVIATION_TYPE`
- `ORA_DOS_SUPPLY_ORDER_TYPE`
- `ORA_DOS_SUPPLY_REQ_PRC_STATUS`
- `ORA_CTO_CONFIG_INTERVAL_UNIT`

The union of these two lists is the complete allowlist for this task. Do not
add or infer another type. Validate the entire requested set before dispatch;
if any type is outside the allowlist, stop and report the out-of-scope types
without partially dispatching the request.

### Read Results

For reads, preserve the exact `Meaning` and `Description` returned by Fusion;
report an absent description as `Not provided`. Do not expand lookup codes
unless the request explicitly asks for code-level details or maintenance.
For a multi-type listing, report each exact match and identify missing,
ambiguous, or failed types separately. Do not invent meanings or descriptions,
or present partial results as a complete successful listing.

### Category Enforcement

Follow the category-enforcement pattern in
[Manage Order Lookups](../../order-management/orders/manage-order-lookups/SKILL.md).
Only types under **User Extensible Lookups** may be extended through this task.
Membership in that list is not approval for a write or permission to alter
Oracle-seeded code identities.

Treat types under **System Lookups** as system-managed. Do not add, delete, or
change the identity of their lookup codes through this task. Allow code
updates only to `Meaning`, `Description`, and `DisplaySequence`, subject to the
selected core workflow's live validation and approval requirements.

Before any otherwise allowed change, have Apps Common read the current lookup,
verify its exact identity and customization level, and validate the operation
and payload. If live metadata conflicts with the expected category or does not
establish that the change is supported, stop the write and report the gap;
the supplied categories do not override Fusion restrictions.

The core skill owns target validation, identity validation, authentication,
REST transport, and explicit approval immediately before the mutation. Do not
duplicate that implementation here or retry a mutation automatically.

## Implementation Notes

This flat task metadata file is part of the [parent functional-area skill](SKILL.md),
not a standalone skill. Use the parent for sequencing and scope decisions;
inherit its execution mode, inputs and outputs, ownership, applicability,
workspace persistence, and token-usage policy. The parent declares the Apps
Common dependency; this file supplies the task-specific routing filters.
