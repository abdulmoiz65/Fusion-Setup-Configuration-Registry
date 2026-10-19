# External Purchase Prices Requisitioning BU Mapping Dependency Readiness

## Required Dependency Order

This resource gates mutation preparation only. Pure record GET completes at
`EPPBU.RETURN_READ_RESULT` after reference resolution and does not enter this
node. Read privileges and scope are still checked before GET under the lookup
contract; write privileges and Procurement/BPA readiness are not read prerequisites.

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Procurement foundation | Procurement is implemented and blanket purchase agreements can be created successfully |
| 2 | Access | The implementation user has the privileges of the predefined Purchase Pricing Manager role |
| 3 | Mapping identities | Resolve the exact parent using supplied natural keys or consistent optional IDs; name-only child inputs are supported |
| 4 | Existing mappings | Obtain the applicable complete membership evidence for names as well as IDs; design enforcement owns conflict decisions and operation applicability |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| procurement_foundation | Procurement implementation and BPA readiness | Yes | Before mapping maintenance or REST import, not pure record GET | Verify | Implementation evidence |  | External purchase prices ultimately create BPAs | Confirm the target can create BPAs manually or through FBDI before enabling External Purchase Prices | Readiness confirmation |
| purchase_pricing_access | Purchase Pricing Manager-equivalent access | Yes | Before mapping maintenance or REST import | Verify | Security assignment evidence |  | The documented setup prerequisite requires the role's privileges | Confirm access before attempting the task | Access confirmation |
| mapping_identity | Existing parent and current child membership | Conditional | Duplicate-create checks and existing-target mutations; pure reads use reference resolution directly | Lookup | Fusion mapping state, with requested keys from reviewed task input | resolve_existing_bu_mapping | Existing-target actions require an exact mapping; optional IDs must agree with names | Supply a precise name or ID; do not require numeric IDs when names suffice | Exact identity and complete current membership, or explicit not-found |
| active_mapping_evidence | Active source-organization memberships | Conditional | Proposed active membership, including name-only inputs and reactivation | Lookup | Fusion mapping state | find_active_requisitioning_bu_mapping | Design enforcement requires complete evidence, not an assumption based on omitted IDs | Resolve incomplete visibility, ambiguity or pagination before preview | Complete membership evidence or an explicit inconclusive/not-applicable outcome |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Evidence is complete and the prerequisite is met | Continue |
| Lookup | A documented read-only Fusion lookup is required | Read-only only |
| Verify | Readiness or access evidence must be reviewed | No write |
| Blocked | Required identity, access, readiness, or exclusivity is missing | No |
| Not applicable | The design rule excludes a pure read, removed membership, parent deletion or explicit deactivation from mutation exclusivity | No mutation; retain exact-target and other applicable checks |

The existing readiness/access confirmations are evidence prerequisites, not a
new BU lookup or proof of unrestricted visibility. Lookup coverage must be
established separately before claiming no active conflicts. This resource does
not verify a BU's existence or eligibility merely because an ID was supplied.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EPPBU.CHECK_DEPENDENCIES | decision | 30 | resolve_dependency | ready->EPPBU.APPLY_DEFAULTS;blocked->EPPBU.HANDLE_ERROR | EPPBU.RESOLVE_REFERENCES | stop | Mutation validation only, after reference resolution selects resolved; never for pure record GET |
