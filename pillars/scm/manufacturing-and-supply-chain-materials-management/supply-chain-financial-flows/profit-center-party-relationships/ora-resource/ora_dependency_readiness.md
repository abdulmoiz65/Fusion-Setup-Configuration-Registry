# PCBU parent dependency readiness

Operation scope: historical parent-only restrictions below apply to parent-create/header-update. For buyer-create/buyer-edit/buyer-delete or seller-create/seller-edit/seller-delete, evaluate the respective profile sections and their transport gate instead; shared identity, environment and artifact rules still apply.


For parent operations, this version creates one parent header or updates requested editable selections on one existing parent. Existing PCRelationshipId is required for update through resolve_existing_pcbu; it is not a prerequisite to create. Buyer operations follow the separate dependency rules below; no dependency is created implicitly. The header LOV definitions remain owned by ora_reference_lookups.md.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Parent BU context | Require the successful BU selection from PCBU.RESOLVE_REFERENCES |
| 2 | Supplied optional parent selections | Require successful applicable supplier, customer, trade-organization and ship-to selection within that BU/environment context |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| PCBU_HEADER_CONTEXT | Selected parent BU | Yes | Every supported header create | Verify | Prior PCBU.RESOLVE_REFERENCES result in this run | resolve_pcbu_by_exact_name | Parent IDs and optional references must belong to the selected environment and BU | Resolve missing or ambiguous selection before proceeding; reuse the completed result while context is unchanged | Verified parent BU and legal-entity context |
| PCBU_UPDATE_TARGET | Existing parent and requested selections | Yes | Header update only | Verify | Prior resolve_existing_pcbu and every applicable header resolver result from this run | resolve_existing_pcbu | Update must address the existing parent in the selected BU/legal entity | Stop on missing target or unresolved requested selections; never create dependencies | Verified PCRelationshipId and requested-field before/after context |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Prior reference node supplied all applicable parent selection evidence | No further lookup or dependency creation |
| Blocked | Parent selection evidence missing, ambiguous, conflicting or from another context | No; return the missing evidence and stop |
| Unsupported | Parent delete, unsupported header update fields or direct-ID-only request | No; do not create dependencies or invoke deferred child resolvers |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PCBU.CHECK_DEPENDENCIES | step | 30 | resolve_dependency | success->PCBU.CHECK_DEFAULTS;failure->PCBU.RETURN_ISSUES | PCBU.RESOLVE_REFERENCES | stop | After operation-specific reference resolution |

## Buyer Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| BUYER_PARENT | Existing parent context | Yes | All buyer operations | Verify | Current environment lookup | resolve_buyer_parent | Buyer must belong to one existing PCBU | Resolve name and profile presence first | PCRelationshipId and current PayablesId |
| BUYER_CUSTOMER | Parent customer, party and ledger | Yes | Buyer create/edit | Verify | Resolved parent | resolve_buyer_parent | Redwood requires a customer account; bill-to BU depends on ledger and procurement BU | Set up missing customer in a separate requested header operation | CustomerIdentificationId, PartyId, PrimaryLedgerId |
| BUYER_TRANSPORT | Deployed Data Loader child contract | Yes | Every buyer artifact preparation or mutation | Verify | Live generated schema and supported adapter evidence | | Parent-only registration is insufficient for composite buyer operations | Stop until PayablesBUAssignment and CustomerAssociation registration, linkage, operations, null encoding where requested and deletion behavior are verified | Environment-specific contract and validated artifact evidence |

The transport gate is evaluated before preparing or submitting a buyer artifact. Source-backed business planning may finish with a blocked execution outcome. Do not invent ParentId/ParentIdentifier mappings or reuse a parent-only XLSX as a child template. Do not require SupplierAssociation or ReceivablesBUAssignment for a buyer-only request.

## Seller Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| SELLER_PARENT | Existing PCBU and supplier | Yes | Seller create/edit | Verify | Selected environment | resolve_seller_parent | Redwood requires a header supplier; site lookup uses its VendorId | Request a separate header update if missing; do not add supplier implicitly | Parent, supplier and ledger context |
| SELLER_TARGET | Existing seller identity | Yes | Seller edit/delete | Verify | Parent-linked child lookup | resolve_seller_assignment | Operations must address current seller profile | Resolve current ReceivablesId; no guessed ID | ReceivablesBUAssignmentId |
| SELLER_TRANSPORT | Data Loader child operation contract | Yes | Seller artifact preparation or mutation | Verify | Live generated schema and adapter evidence | | Parent-only registration does not establish seller import behavior | Verify ReceivablesBUAssignment and SupplierAssociation registration, parent linkage, operations, derived set behavior and cascade before preparation | Environment-specific validated contract |

Planning can complete while APEX is unavailable. Stop execution at this gate until evidence exists. Seller-only work does not require creating buyer-profile children. Never substitute direct Redwood batch writes for core.data-loader.
