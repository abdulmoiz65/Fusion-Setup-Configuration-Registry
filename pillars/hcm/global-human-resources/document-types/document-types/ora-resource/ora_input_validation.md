# Document Types Input Validation

## Purpose

Defines required inputs, conditional requirements, field checks, and validation routing for Document Types.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | get, create, edit, or delete | Block | Provide one supported operation | Every request |  |
| Environment | Configured target environment | Block | Select the target environment | Every request |  |
| Existing Document Type selector | Exact DocumentTypeId or DocumentType | Block | Provide one exact selector | get, edit, or delete | find_document_types |
| Create values | Name and category | Block | Provide both values | create |  |
| Edit changes | At least one explicit supported change | Block | Provide the intended change | edit |  |
| Create hierarchy | None | Do not request `HierarchyCode`; `GENERAL` and `PAYROLL` are not mandatory for an ordinary Document Type create | create without explicitly requested Delivery Preferences |  |
| Delete acknowledgement | Fresh exact target and explicit irreversible-delete acknowledgement | Block | Resolve the target and acknowledge deletion | delete | find_document_types |
| Delivery Preferences parent | Exact parent DocumentTypeId | Block | Resolve one Document Type parent | Delivery Preferences are requested | find_document_types |
| Delivery Preferences parent hierarchy | Nonblank current parent HierarchyCode | Block | Read the exact parent item and preserve its hierarchy | A Delivery Preferences mutation is requested | find_document_types |
| Delivery Preferences country | One current CountryName and TerritoryCode pair | Block | Resolve the supplied country through HCM Countries LOV | A Delivery Preferences mutation supplies a country | find_country |
| Delivery Preferences payroll statutory unit | One current PsuId and canonical name pair | Block | Resolve the supplied name through Payroll Statutory Units LOV | A PAYROLL Delivery Preferences mutation supplies a PSU | find_payroll_statutory_unit |
| Delivery Preferences legal employer | One current LempId and canonical name pair | Block | Resolve the supplied name through Legal Employers LOV | A GENERAL Delivery Preferences mutation supplies a Legal Employer | find_legal_employer |
| Delivery Preferences hierarchy rows | Applicable organization anchor plus every requested lower-level row | Block | Build the PAYROLL or GENERAL hierarchy set, then reconcile current rows | Department or Location preference is requested | reconcile_delivery_preference_hierarchy |
| Missing anchor route | Exact anchor count, same-organization lower-row count, current hierarchy, and route-specific live contract | Block | Reconcile all bounded children before artifact construction | A PSU or Legal Employer anchor is missing | reconcile_delivery_preference_hierarchy |
| Missing anchor Data Loader identity | Unique deterministic SourceSystemOwner and SourceSystemId | Block | Generate and collision-check a child source key without changing the existing parent identity or asking the user | A genuinely new hierarchy is routed to Data Loader | reconcile_delivery_preference_hierarchy |
| Delivery Preferences group | Default, non-person override, or person override | Block | Select one explicit preference group | Delivery Preferences are requested |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An existing target or Delivery Preferences parent does not resolve exactly once | Missing | Provide one exact Document Type selector | find_document_types |
| A create business key matches an existing Document Type | Invalid | Stop the duplicate create | find_document_types |
| A category or other lookup-backed value is missing, disabled, expired, or ambiguous | Invalid | Provide one enabled current stored value |  |
| A supplied subcategory is not valid for the resolved category | Invalid | Correct the category or subcategory |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Effective range | Reject an end date earlier than its start date | Both dates are supplied |  |
| Stored reference value | Reject an unverified lookup meaning when the stored code is required | A lookup-backed value is supplied |  |
| Subcategory scope | Validate the subcategory only after its category is resolved; never infer it from an example | A subcategory is supplied |  |
| Delivery Preferences headings | Reject fields absent from current Document Type Data Loader metadata, including LocationSetCode | Delivery Preferences are authored |  |
| Delivery Preferences location | Leave LocationCode blank when a resolved LocationId is used | A Delivery Preference supplies LocationId |  |
| Existing Location row identity | Resolve exactly one current child by returned LevelCode, organization ID, and LevelId equal to the resolved Location ID. Do not treat a null returned LocationId as absence when those values and LocationName match. | A Location preference is read, edited, deleted, retried, or reconciled | reconcile_delivery_preference_hierarchy |
| Delivery Preferences mode-only edit | Require one freshly read DocumentDeliveryPreferenceId; preserve each unrequested OnlineEnabledFlag or PaperEnabledFlag value; include only the changed child and omit an unchanged hierarchy anchor | An existing preference changes only Online or Paper mode | reconcile_delivery_preference_hierarchy |
| Parent hierarchy preservation | Require the freshly read parent HierarchyCode on the root DocumentType row. Reject blank, inferred, hard-coded, or stale evidence. | A Delivery Preferences mutation is authored | find_document_types |
| Ordinary create hierarchy omission | Do not require, prompt for, infer, or default `HierarchyCode`. Require the live REST parent-create contract to mark it nonmandatory and require the immutable parent payload to omit it. | A Document Type is created without explicitly requested Delivery Preferences |  |
| Existing-parent attachment add route | If HDL exposes only generated `AttachedDocumentId`, reject HDL MERGE and require the live REST child describe contract to advertise POST create, attachment-typed `FileContents`, and generated `AttachedDocumentId`. Require a safe nonempty file, MIME type, byte length, SHA-256, exact parent, no same-name current child, immutable preview, and standalone approval. Never solicit or invent the ID. | A new attachment is requested for an existing Document Type | find_document_types |
| Existing attachment edit identity | Require exactly one current attachment and its freshly read `AttachedDocumentId`; preserve the parent identity and change only requested attachment values. | An existing Document Type attachment is edited or replaced | find_document_types |
| Country attribute semantics | When the exact live heading is Country, require the resolved CountryName display value; when it is LegislationCode, require the resolved TerritoryCode | A Delivery Preferences country is authored | find_country |
| Payroll statutory unit identity | For a Data Loader `Payroll Statutory Unit`, require exact canonical `PayrollStatutoryUnitName` and blank PsuId; for Data Loader Department/Location, require current OrganizationId in `PsuId` and blank name. | A PAYROLL Delivery Preferences PSU is authored | find_payroll_statutory_unit |
| Legal employer identity | For `Legal Employer`, require exact canonical `LegalEmployerName` and blank LempId; for Department/Location, require current OrganizationId in `LempId` and blank name | A GENERAL Delivery Preferences Legal Employer is authored | find_legal_employer |
| Hierarchy pair | Require `Payroll Statutory Unit` plus Department/Location for PAYROLL, or `Legal Employer` plus Department/Location for GENERAL; use canonical name on the anchor and resolved numeric organization ID only on lower-level rows | A Department or Location Delivery Preference is authored | reconcile_delivery_preference_hierarchy |
| Reconciliation | Exclude a current exact row unless its delivery modes are explicitly changed; include every missing anchor or lower-level row | A prior load succeeded, partially succeeded, failed ambiguously, or the operation is retried | reconcile_delivery_preference_hierarchy |
| Anchor source key | Require nonblank generated source owner and collision-checked source ID only on a new Data Loader child; reject caller solicitation, partial keys, copied keys, parent-key changes, and user-key-only retry after a proven non-settable PsuId/LempId failure | A missing anchor is routed to Data Loader | reconcile_delivery_preference_hierarchy |
| Default preference controls | Omit PsuId and LevelCode only when current loader metadata marks them non-settable | A default preference row is authored |  |
| Complete row validation | Validate every populated Delivery Preferences cell together; reject partial correction of an otherwise invalid row | Delivery Preferences are authored |  |
| Supported shape | Reject unsupported fields or package shapes; never silently omit or invent them | A mutation source is prepared |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DOCT.VALIDATE | decision | 1 | validate_input | valid->DOCT.DEPENDENCY;missing->DOCT.ERROR;invalid->DOCT.ERROR;unsupported->DOCT.ERROR | none | stop | Every Document Type request |
