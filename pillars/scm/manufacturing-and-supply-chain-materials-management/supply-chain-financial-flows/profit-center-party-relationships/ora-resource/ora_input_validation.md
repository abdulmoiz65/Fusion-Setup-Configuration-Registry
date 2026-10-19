# PCBU input validation

Operation dispatch: parent-create/header-update use the parent rules below. buyer-create/buyer-edit/buyer-delete use the Buyer input contract; seller-create/seller-edit/seller-delete use the Seller input contract in this file and corresponding seller sections in the other resources. Global identity, environment and artifact rules apply to all operations.

Parent-operation scope: one parent header create by BU name or one existing parent header update by BU name and one or more requested editable header selections. Child records, fields outside the four editable header selections, clearing values, deletes, bulk operations and caller-supplied identity are unsupported. Task ORA_PROFIT_CENTER_PARTY_RELATIONSHIPS_NEW, business object financialOrchestrationProfitCenterPartyRelations. The intended workflow is executable through Data Loader after its contracts and approvals pass; these rules do not authorize imports.

## Source boundary

Source basis: APEX registration exports and the PCBU backend source under <fusion-source-root>/scm/financialOrchestration/fos/setup/profitCtrPartyRel. Relevant directories are model/src/oracle/apps/scm/fos/setup/profitCenterPartyRelations/model/entity and restModel/src/oracle/apps/scm/fos/setup/profitCenterPartyRelations/restModel/view. Resolve the source root in the current checkout. Source evidence must be checked against the selected deployed release and generated Data Loader metadata.

Primary inspected files: ProfitCenterBuHeaderEO.xml, CustomerAssociationEO.xml, PayablesBuAssignmentEO.xml, ReceivablesBuAssignmentEO.xml, SupplierAssociationEO.xml and their corresponding VO.xml files. EO not-null constraints are persistence constraints, not automatically caller-required REST attributes. Joined VO not-null flags likewise do not establish writable inputs.

## Identity metadata

| Resource | Table | Surrogate Column | Registered Surrogate Attribute | Registered Parent Attribute |
|---|---|---|---|---|
| financialOrchestrationProfitCenterPartyRelations | FOS_PROFIT_CENTER_BU_HEADER | PC_RELATIONSHIP_ID | PCRelationshipId | None |
| CustomerAssociation | FOS_CUSTOMER_ASSOCIATION | CUSTOMER_ASSOCIATION_ID | CustomerAssociationId | PCRelationshipId |
| PayablesBUAssignment | FOS_PAYABLES_BU_ASSIGNMENT | PAYABLES_BU_ASSIGNMENT_ID | PayablesBUAssignmentId | PCRelationshipId |
| ReceivablesBUAssignment | FOS_RECEIVABLES_BU_ASSIGNMENT | RECEIVABLES_BU_ASSIGNMENT_ID | ReceivablesBUAssignmentId | PCRelationshipId |
| SupplierAssociation | FOS_SUPPLIER_ASSOCIATION | SUPPLIER_ASSOCIATION_ID | SupplierAssociationId | PCRelationshipId |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Header business input | Profit Center BU name and explicit create or header-update intent; optional supplier, customer, trade organization and ship-to selections | Ask for the missing BU name or operation before continuing | Collect business names/codes first; identity resolution belongs to PCBU.RESOLVE_REFERENCES | One parent create or header update | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Supported request | Accept exactly one parent create by BU name, or one header update by BU name plus at least one nonblank supplier, customer, default trade organization or ship-to selection. Reject fields outside the four editable header selections, clearing/null-marker requests, deletes, multiple parent rows, caller-supplied surrogate IDs, direct-ID-only requests and every populated child row. Empty child sheets do not request child creation | Every request | |
| Initial input versus resolved values | Check supplied intent, BU name, optional selections and row scope only. Do not require lookup output before PCBU.RESOLVE_REFERENCES. IDs already present in a prepared artifact must have prior lookup evidence from this same task/environment; they are checked against fresh selected results at PCBU.CHECK_DESIGN | Initial input check | |
| Optional input intent | Keep explicitly omitted optional selections unset. Do not silently discard populated data or select a default when no selection was supplied | Every request | |
| Registration scope | Historical parent-only JSON does not establish current registration. Require the Data Loader workflow to verify deployed parent and requested child metadata before load approval | Parent create preparation | |

## APEX mandatory-field review

Historical review: the following read-only fields were removed from MandatoryOnCreate in the final APEX export. Do not repeat these corrections or claim they remain selected. They are not a payload allowlist or an instruction to change ExcludeInPayload. ObjectVersionNumber is also no longer marked mandatory; generated-ID and version handling still require operation-specific verification.

| Resource | Read-only fields removed from mandatory selection | Evidence |
|---|---|---|
| Parent | AccountNumber, LocationCode, SupplierNumber, VendorName, LegalEntityName, PartyId, PartyName, PartyNumber, PartySiteNumber, CreatedBy, CreationDate, LastUpdatedBy | ProfitCenterBuHeaderVO.xml ViewAttribute and EntityUsage |
| CustomerAssociation | CustomerAddressSetName, ProfitCenterBUId, BillToLocation, SiteUseCode | CustomerAssociationVO.xml ViewAttribute and EntityUsage |
| PayablesBUAssignment | ProfitCenterBUId | PayablesBuAssignmentVO.xml read-only parent EntityUsage |
| ReceivablesBUAssignment | CreatedBy, CreationDate, LastUpdateDate, LastUpdatedBy, ICAddressSetName, ProfitCenterBUId | ReceivablesBuAssignmentVO.xml ViewAttribute and EntityUsage |
| SupplierAssociation | CreatedBy, CreationDate, LastUpdateDate, LastUpdatedBy, ProfitCenterBUId, SupplierSiteCode | SupplierAssociationVO.xml ViewAttribute and EntityUsage |

## Final registration contract

The initial parent-only export is historical evidence: its parent surrogate was PCRelationshipId and its create requirement was ProfitCenterBUId. It is not the current runtime schema. For each operation, generate the selected environment’s template and verify the parent and requested child collections, keys, writable attributes and operation encoding. Use the buyer and seller contracts below together with the dependency gate. An exported header-only workbook is a template, not a validated upload artifact.

| Resource | MandatoryOnCreate |
|---|---|
| financialOrchestrationProfitCenterPartyRelations | ProfitCenterBUId |

## Client validation evidence

The regenerated APEX JSON reviewed after the developer's header correction has MandatoryOnCreate=ProfitCenterBUId. LegalEntityId is no longer caller-mandatory in that registration. Keep it available as BU-derived lookup context; its database not-null constraint does not require the caller to send it. This records the supplied registration contract, not proof that the metadata is deployed or that a minimal-payload live create has succeeded. Data Loader filtering remains pending; ExcludeInPayload is unchanged.

Inspected core/data-loader/scripts/data_loader_metadata.py validate_source_sections: it rejects unknown sections, unknown/duplicate attributes and inconsistencies between mandatory metadata and the live template. It deliberately does not require all mandatory attributes in each input row; operation-specific required-value enforcement belongs to Fusion. Therefore MandatoryOnCreate selections alone do not establish a valid create/update contract.

Inspected core/data-loader/scripts/xlsx_sample_workbook.py read_xlsx_source: it maps headers, retains selected column indexes, converts supplied values to DAT records and rejects an entirely header-only workbook. It does not itself assign PCBU IDs or resolve customer/supplier references. A header-only APEX XLSX is a template, not loadable test data.

Live validation requires registered business-object detail, UCM template and child attribute metadata (data_loader_metadata.py fetch path). The APEX export is not a substitute for that generated schema. No live metadata request was made during this authoring pass.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PCBU.CHECK_INPUT | step | 10 | validate_input | success->PCBU.RESOLVE_REFERENCES;failure->PCBU.RETURN_ISSUES | none | stop | Before any PCBU task validation or import preparation |

## Parent header update contract

Update intake requires an explicit update intent, a BU name and at least one nonblank supplier, customer, default trade organization or ship-to selection. A supplier string such as 1099-Supplier is matched literally; never split it into an inferred number/name pair. Resolver outputs are not intake requirements.

The prepared update must contain PCRelationshipId, RestAction=PATCH and exactly the requested subset of SupplierIdentificationId, CustomerIdentificationId, DefaultTradeOrganizationId and ShipToLocationId as its METADATA attributes, with one parent MERGE row. PCRelationshipId identifies the target; it is not a requested change. All IDs must be resolved positive decimal strings of at most 18 digits. Do not include ProfitCenterBUId, blank optional columns, generated/read-only attributes or child sections in an update source. MandatoryOnCreate=ProfitCenterBUId is create-only metadata and must not cause that field to be added to PATCH.

## Buyer input contract

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Buyer operation and target | Require an explicit buyer-create, buyer-edit or buyer-delete intent and existing PCBU name. Do not create or change the PCBU as a dependency | Every buyer request | |
| Buyer create | Require procurement BU and bill-to BU names. Optional ship-to party site and zero or more address-set/bill-to-location pairs. Resolve the existing parent and verify no buyer profile before creation | buyer-create | |
| Buyer edit | Require at least one requested change to procurement BU, bill-to BU, ship-to party site or an explicit add/update/delete of a customer bill-to row. Identify an existing row by its address set and location, then retain its resolved surrogate. Preserve omitted data | buyer-edit | |
| Buyer delete | Resolve exactly the current buyer profile. Review its related customer-association rows as deletion impact. Parent and seller deletion are not part of this operation | buyer-delete | |
| Display versus writable fields | Ship-to Site Name is derived. Do not write BU names, site names, set names, generated/audit/version fields or infer InterCompanyPurchaseFlag from the screen title | Every buyer request | |
| Explicit clearing | Distinguish omitted from explicitly cleared ShipToPartySiteId. Redwood sends null for a cleared site; Data Loader null encoding must be verified before accepting a clear artifact. Required procurement and bill-to BUs cannot be cleared | buyer-edit | |

The screenshot is UI evidence, not selected input or authority to mutate CST Business Unit. New parent plus buyer in one import is outside this extension.

## Seller input contract

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Seller target and intent | Require existing PCBU name and seller-create, seller-edit or seller-delete. No parent creation, parent deletion or buyer-profile mutation is implied | Every seller request | |
| Seller create inputs | Require customer address set for LOV context, receivables BU and at least one buyer-detail row with procurement BU, bill-to BU and supplier site. Redwood CreateIntercompanySellerProfile requires at least one row; do not treat this UI rule as proof of a database minimum | seller-create | |
| Seller edit inputs | Require requested receivables BU change or explicit add/edit/delete of supplier rows. Identify existing rows by BU pair and site, resolving exact SupplierAssociationId. Preserve omitted rows and values | seller-edit | |
| Insert-only fields | SupplierAssociation.PayablesInvoicingBUId cannot be changed in place in inspected EO/REST VO metadata. Plan explicit delete-and-add replacement for a requested change, showing both operations and impacts; never silently replace. Existing CustomerAssociation.CustomerAddressSetId has the same insert-only restriction for buyer edits | Profile row edit | |
| Seller address set | Editable selection on create; display-only on edit. It filters receivables BU candidates. Do not serialize ICAddressSetName or turn an edit-time set change into an unsupported direct update | Seller create/edit | |
| Seller delete | Resolve current ReceivablesBUAssignment and all SupplierAssociation rows; review cascading impact. Deleting one supplier row is distinct from deleting the profile | seller-delete | |

Supplier/site/BU clears are outside this extension. Screenshots provide UI evidence, not live record selections.
