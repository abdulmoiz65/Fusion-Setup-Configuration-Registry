# PCBU identity and design enforcement

Operation scope: historical parent-only restrictions below apply to parent-create/header-update. For buyer-create/buyer-edit/buyer-delete or seller-create/seller-edit/seller-delete, evaluate the respective profile sections and their transport gate instead; shared identity, environment and artifact rules still apply.


Source EO XML binds uniqueness validators to PcBusinessUnitAltKey (parent), CustomerAltKey (customer), PayablesBusinessUnitAltKey (payables) and SupplierAltKey (supplier). Their tuples are respectively ProfitCenterBuId; CustomerAddressSetId plus PcRelationshipId; PcRelationshipId plus InterCompanyPurchaseFlag; and ProcurementBuId plus PayablesInvoicingBuId plus PcRelationshipId. Payables also declares FosPayablesBuAssignmenUk1 including ProcurementBuId; supplier declares FosSupplierAssociationUk1 without PayablesInvoicingBuId. Receivables declares FosReceivablesBuAssignUk1 on PcRelationshipId and binds a uniqueness validator to RcvInvoicingBusinessUnitKey. These distinct declarations are not interchangeable Data Loader user-key contracts. Preserve the final ID-based registration: all user-key sets, including Customer Association, are deferred. Database uniqueness still applies.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Verify selected identities | Use completed parent lookup results; reject missing, conflicting or stale evidence |
| 2 | Validate the exact prepared artifact | Compare the immutable upload bytes with the requested parent scope and selected IDs |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every parent create | Blocker | resolve_pcbu_by_exact_name | BU selection is unresolved, candidate choice is pending or the selected create operation has changed | Use the selected BU. Do not require a duplicate pre-check; let Fusion enforce uniqueness and stop on a duplicate error without switching to update | No automatic update or retry |
| Final ID validation after PCBU.RESOLVE_REFERENCES | Blocker | | A populated ID differs from the selected lookup result, is not positive decimal text of at most 18 digits, or is fractional, rounded or scientific notation | Preserve exact IDs and verify all optional IDs against the applicable selected rows in the same environment/BU context | No identity substitution |
| Final field validation for create | Blocker | | Any populated field is outside ProfitCenterBUId, DefaultTradeOrganizationId, ShipToLocationId, SupplierIdentificationId, CustomerIdentificationId and RestAction; RestAction is not POST; or a mapping is unknown, duplicate or ambiguous | Use the Data Loader live header mapper and exact canonical attributes. Omit generated PCRelationshipId, audit, display, version and linkage values. Do not rely on ExcludeInPayload filtering | Correct source only through a fresh preparation and validation cycle |
| Final package validation for create | Blocker | | ZIP does not contain exactly one DAT member and one parent MERGE row with explicit RestAction=POST, or contains any child data row | Empty child metadata is allowed but populated child rows are unsupported. Verify mandatory ProfitCenterBUId and all populated optional values against the prior lookup evidence | No in-place artifact changes |
| Immutable Task Hook artifact | Blocker | | The prepared artifact or selected environment/BU changed, lookup results require replacement IDs, or live Data Loader schema validation did not pass | Stop. Reprepare through core.data-loader and rerun Task Hook for the new immutable artifact before approval; do not fill or alter approved bytes during rule execution | Fresh preparation only |

## Header update design rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Header update identity | Blocker | resolve_existing_pcbu | Existing parent is not uniquely resolved or PCRelationshipId differs from the selected row; BU/legal entity context changed | Stop and resolve again before preparing a new artifact | No identity substitution or create fallback |
| Supplier selection when requested | Blocker | resolve_pcbu_header_supplier | Supplier candidate unresolved, incompatible with legal entity, or payload VendorId differs from the selected supplier | Use the existing supplier LOV within the resolved legal entity; preserve all candidate-choice rules | No arbitrary supplier selection |
| Header update package | Blocker | | Anything other than one DAT member, one parent METADATA with PCRelationshipId, RestAction and exactly the requested subset of SupplierIdentificationId, CustomerIdentificationId, DefaultTradeOrganizationId, ShipToLocationId, and one MERGE PATCH row; any blank value, extra column, child section or POST/DELETE operation | Prepare a minimal update source with exact resolved IDs; validate through Data Loader and restart Task Hook for changed bytes | No in-place artifact edits |
| Update review and concurrency | Blocker | resolve_existing_pcbu | Missing before/after requested-field evidence, stale task/environment context or any conflict returned by Fusion | Present BU and the old/new values for every requested field before approval. Data Loader does not establish an atomic ETag precondition here; disclose this limitation. Stop on conflict, do not retry | Fresh preparation and approval after resolving a conflict |

## Additional header update selections

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Customer update requested | Blocker | resolve_pcbu_header_customer | Missing/ambiguous candidate or prepared CustomerIdentificationId differs from selected CustomerAccountId | Resolve within legal entity, retaining Intercompany=All as a search-only preference | No inferred ID |
| Default trade organization update requested | Blocker | resolve_pcbu_header_trade_organization | Candidate missing/ambiguous, wrong BU or prepared ID differs from selected OrganizationId | Resolve organization within the fixed BU | No BU change |
| Ship-to update requested | Blocker | resolve_pcbu_header_ship_to | Reference set or location unresolved, context mismatch or prepared ID differs from selected LocationId | Resolve the BU reference set before the location; preserve candidate-selection rules | No arbitrary set/location choice |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_pcbu_by_exact_name | Parent create only; reuse the result from PCBU.RESOLVE_REFERENCES | Selected BU identity and completed candidate choice | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PCBU.CHECK_DESIGN | step | 50 | design_enforcement | success->PCBU.CHECK_HANDOFF;failure->PCBU.RETURN_ISSUES | PCBU.CHECK_DEFAULTS | stop | After reference resolution and before handing back validation of the exact operation-specific artifact |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Buyer create | Blocker | resolve_buyer_parent | Parent missing, buyer already present or customer missing | Resolve prerequisites without creating dependencies; never turn create into update silently | No automatic fallback |
| Buyer edit/delete identity | Blocker | resolve_buyer_assignment | Current PayablesId/item identity missing or not linked to selected parent | Retain current PayablesBUAssignmentId and PCRelationshipId | No inferred surrogate |
| Buyer address mutations | Blocker | resolve_buyer_customer_rows | Existing row ambiguous, duplicate address set proposed or a retained row silently dropped | Match updates/deletes by CustomerAssociationId; omit ID only for new rows; retain untouched rows | Fresh reviewed change set |
| Buyer transport gate | Blocker | | Missing verified child schema, operation mapping, parent linkage, cascade or requested null handling | Return blocked before preparation/submission; resolve via core.data-loader. Redwood REST batch is source evidence, not an alternative execution route | No direct REST fallback |
| Buyer delete impact | Blocker | resolve_buyer_customer_rows | Cascade impact not recorded or caller intent is only a row deletion | Review all related CustomerAssociation rows; target only PayablesBUAssignment, never the PCBU parent | No broader deletion |

### Redwood operation mapping

buildBuyerPayload emits payables child collection upsert with ProcurementBUId and PayablesInvoicingBUId; edit includes PayablesBUAssignmentId. It also emits a parent upsert of ShipToPartySiteId. Removed customer rows use DELETE on their child item path; additions/updates use parent upsert with CustomerAssociation array, including CustomerAssociationId only for updates. This is a behavioral reference, not a Data Loader wire contract. Preserve exact decimal IDs and operation intent; establish loader POST/PATCH/DELETE and ordering from live schema/adapter evidence before generating an import.

ProfileClickChain deletes /financialOrchestrationProfitCenterPartyRelations/{PCRelationshipId}/child/PayablesBUAssignment/{PayablesId}. PayablesBuAssignmentVORowImpl.remove rejects deletion when FtrVA returns a trade relationship for bindToBuId=parent ProfitCenterBuId, using FOS_FOSTP_NO_DEL_OF_ICBP_11. PayablesBuAssignmentEOToCustomerAssociationEO declares DeleteContainee=true linked on PcRelationshipId: expect related customer-association deletion and verify deployed behavior. Neither this action chain nor the inspected remove method explicitly clears header ShipToPartySiteId; do not promise that it clears or add a header-clear operation implicitly.

ShipToPartySiteId (customer party site), parent ShipToLocationId (header location), and child location fields are different identities. BillToLocationId in CustomerAssociation maps to customer account site ID, not the payables assignment's similarly named BillToLocationId.

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_buyer_parent | All buyer operations | Existing parent, buyer presence and customer context | ora_reference_lookups.md |
| resolve_buyer_assignment | Buyer edit/delete | Current parent-linked assignment | ora_reference_lookups.md |
| resolve_buyer_customer_rows | Buyer address edits and profile delete | Existing row identities and cascade impact | ora_reference_lookups.md |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Seller identity | Blocker | resolve_seller_assignment | Create finds an existing assignment, or edit/delete has no unique current assignment | Resolve operation-specific presence and current parent link | No create/update fallback |
| Seller row edits | Blocker | resolve_seller_supplier_rows | Row identity unresolved, retained rows dropped, or existing PayablesInvoicingBUId changed in place | Keep existing IDs; review explicit replacement for insert-only changes | No silent replacement |
| Seller site validity | Blocker | resolve_seller_supplier_site | Site not resolved under supplier and both row BUs | Revalidate all dependent selections before artifact preparation | No ID substitution |
| Seller Data Loader contract | Blocker | | Child registration, linkage, operation encoding, derived set behavior or delete cascade unverified | Stop before preparation and report missing evidence | No direct REST fallback |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_seller_assignment | Seller create/edit/delete | Assignment presence and current identity | ora_reference_lookups.md |
| resolve_seller_supplier_rows | Seller row edits or delete impact | Current row identities and before values | ora_reference_lookups.md |
| resolve_seller_supplier_site | Supplier row add/edit | Context-qualified site ID | ora_reference_lookups.md |

### Seller Redwood payload reference

Paths below are relative to /financialOrchestrationProfitCenterPartyRelations/{PCRelationshipId}. They describe the inspected REST batch, not a verified Data Loader DAT contract.

| Operation | Path | Payload |
|---|---|---|
| Create assignment | /child/ReceivablesBUAssignment | IntercompanyReceivablesBUId; batch operation create |
| Create each supplier row | /child/SupplierAssociation | ProcurementBUId, PayablesInvoicingBUId, SupplierSiteId; batch operation create |
| Edit assignment | /child/ReceivablesBUAssignment/{ReceivablesBUAssignmentId} | IntercompanyReceivablesBUId; batch operation upsert |
| Delete individual row | /child/SupplierAssociation/{SupplierAssociationId} | No body; batch operation delete |
| Add/update rows during edit | Parent path | SupplierAssociation array of the three business IDs; include SupplierAssociationId only for existing rows; batch operation upsert |
| Delete seller profile | /child/ReceivablesBUAssignment/{ReceivablesId} | Child DELETE; no parent deletion |

Redwood emits removed rows before row upserts. Do not infer Data Loader atomicity or retry safety from that sequence. The UI can send PayablesInvoicingBUId in an edit payload, but EO/VO insert-only metadata takes precedence when planning an actual change.

ReceivablesBuAssignmentVORowImpl.remove queries trade relationships by selling BU, buying-BU payables assignments and matching supplier associations. It can raise FOS_FOSTP_NO_DEL_OF_ICSP_11. Do not simplify this to the buyer profile's any-trade-relationship rule or bypass it. The inspected loop can reset its proceed flag on subsequent rows; rely on the deployed server outcome, not a client-side simulation. Association metadata declares supplier-row cascade deletion; verify in the target environment and show all rows in the impact review.

### Buyer insert-only correction

CustomerAssociationVO.xml and CustomerAssociationEO.xml mark CustomerAddressSetId insert-only. Earlier Redwood payload evidence must not be read as proof it can change in place. For a changed set, stop ordinary PATCH preparation and propose explicit row replacement with new set/location resolution and separate review of removal impact. Updating BillToLocationId within the same set remains a distinct operation.
