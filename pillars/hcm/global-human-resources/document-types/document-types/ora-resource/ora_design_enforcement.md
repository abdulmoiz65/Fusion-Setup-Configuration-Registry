# Document Types Design Enforcement

## Purpose

Defines the mandatory Document Type and Delivery Preferences design gates
evaluated before preview or routing. It does not perform lookups, apply
defaults, or create missing setup.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm target scope | Resolve the selected Document Type and restrict work to its approved data |
| 2 | Confirm parent and references | Resolve the exact parent and each supplied reference before child work |
| 3 | Enforce country behavior | Keep LegislationCode blank for an explicit All Countries create |
| 4 | Confirm mutation control | Select Data Loader or the qualified PAYROLL anchor create route from fresh hierarchy state, then require an approved immutable preview for that route |
| 5 | Decide readiness | Continue only when no applicable blocking rule remains |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| SCOPE | Create, edit, or delete | Blocking |  | The request contains data outside the selected Document Type or Delivery Preferences scope | Rebuild the XLSX source with only the approved scope | Source rebuild |
| REFERENCE | A reference is supplied | Blocking | find_document_types | The required target or parent reference is missing, inactive, ambiguous, or incompatible | Resolve one exact current reference before preview | Lookup fix |
| ALL_COUNTRIES | A create is scoped to All Countries | Blocking |  | LegislationCode contains the All Countries display value or another inferred country code | Leave LegislationCode blank or null and rebuild the preview | Source rebuild |
| PARENT | Delivery Preferences are requested | Blocking | find_document_types | The parent is missing, ambiguous, or lacks one resolved DocumentTypeId | Refine the selector and re-read one exact parent | Lookup fix |
| PARENT_HIERARCHY | A Delivery Preferences mutation is requested | Blocking | find_document_types | Data Loader omits the freshly read nonblank parent HierarchyCode on its root DocumentType row, or uses stale, inferred, or hard-coded evidence | Re-read the exact parent and rebuild the Data Loader artifact | Source rebuild |
| CREATE_HIERARCHY_OMISSION | A Document Type create has no explicitly requested Delivery Preferences | Blocking | find_document_types | Intake requires or defaults `HierarchyCode`, the payload invents `GENERAL` or `PAYROLL`, the REST contract marks the field mandatory, or the exact name already exists | Use the declared REST parent-create adapter with the attribute omitted, or stop | Route correction |
| COUNTRY_REPRESENTATION | A Delivery Preferences mutation supplies a country | Blocking | find_country | `Country` contains a territory code, `LegislationCode` contains a display name, or the country does not resolve uniquely and currently | Resolve the country and rebuild using CountryName for `Country` or TerritoryCode for `LegislationCode` | Source rebuild |
| PSU_IDENTITY | A PAYROLL Delivery Preferences mutation supplies a PSU | Blocking | find_payroll_statutory_unit | Data Loader violates name-only anchor or ID-only lower-row mapping, or trims significant canonical whitespace | Resolve the PSU and rebuild the Data Loader identity mapping | Source rebuild |
| HIERARCHY_PAIR | A Department or Location preference is requested | Blocking | reconcile_delivery_preference_hierarchy | The reconciled final state omits the applicable anchor; a Data Loader anchor contains its numeric organization ID; or a Data Loader lower row lacks the resolved organization ID | Build the applicable Data Loader hierarchy, then omit only current exact rows from a reconciliation package | Source rebuild |
| LOWER_ROW_IDENTITY | A Department or Location preference is read, edited, deleted, retried, or reconciled | Blocking | reconcile_delivery_preference_hierarchy | A lower row is classified from a nullable convenience field alone, or its returned level code, organization identity, and LevelId do not match the independently resolved lower-level identity | Reconcile by the current returned LevelCode plus organization ID and LevelId; for Location, do not infer absence solely from null LocationId | Lookup fix |
| MODE_ONLY_EDIT | An existing Delivery Preference changes only Online or Paper | Blocking | reconcile_delivery_preference_hierarchy | The source lacks the one fresh DocumentDeliveryPreferenceId, changes or omits an unrequested mode, includes a different child, or resubmits an unchanged hierarchy anchor | Re-read the exact child and rebuild a one-child edit that preserves unrequested modes | Source rebuild |
| ANCHOR_CREATE_KEY | A missing organization anchor is routed to Data Loader | Blocking | reconcile_delivery_preference_hierarchy | The new child lacks a generated unique SourceSystemOwner/SourceSystemId, reuses a current key, changes the parent key, asks the user for technical key values, or relies only on the child user key after a proven non-settable organization-ID failure | Generate and collision-check the child key internally, or stop with a catalog mismatch | Source rebuild |
| CHILD | Delivery Preferences are requested | Blocking | find_document_types | The wrong child resource or an unresolved preference group is proposed | Use hrDocumentTypes/{id}/child/documentDeliveryPreference and one explicit group | Input fix |
| ATTACHMENT_CREATE_KEY | A new attachment is requested for an existing Document Type | Blocking | find_document_types | The source proposes an HDL child MERGE with generated `AttachedDocumentId`, or the REST child describe contract lacks POST create, attachment-typed `FileContents`, or generated ID behavior | Reject HDL for this add; use only the declared approval-gated REST child-create adapter when its live contract passes | Route correction |
| MUTATION_ROUTE | Create, edit, or delete | Blocking |  | A browser workflow, FSM import, CSV import, undeclared REST call, or another undeclared route is proposed | Use Core Data Loader except for the declared hierarchy-free parent-create and existing-parent attachment adapters | No |
| APPROVAL | Create, edit, or delete | Blocking |  | The immutable preview for the selected declared route is absent, stale, or unapproved | Revalidate the Data Loader ZIP or REST attachment preview and approve the exact environment, business effect, artifact, and fingerprint | Re-preview |
| READ_OUTPUT | A user-facing read is returned | Blocking |  | WHO or transport metadata is included in the functional result | Return only functional configuration values | Input fix |
| DOCUMENT_GOVERNANCE | Create or edit | Warning |  | Name, retention, approvals, security, or delivery method is not aligned with business and confidentiality needs | Use concise business names and configure retention, access, approvals, and delivery deliberately | Input fix |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_document_types | Target, reference, parent, child, or create-uniqueness evaluation | Exact Document Type identity, DocumentTypeId, current HierarchyCode, current values, and delivery preference values when requested | ora_reference_lookups.md |
| find_country | A Delivery Preferences country is supplied | Exact current CountryName and TerritoryCode | ora_reference_lookups.md |
| find_payroll_statutory_unit | A PAYROLL Delivery Preferences PSU is supplied | Exact current OrganizationId, canonical name, legislation, and effective dates | ora_reference_lookups.md |
| find_legal_employer | A GENERAL Delivery Preferences Legal Employer is supplied | Exact current OrganizationId, canonical name, legislation, and effective dates | ora_reference_lookups.md |
| reconcile_delivery_preference_hierarchy | A PAYROLL or GENERAL Department or Location preference is supplied or retried | Current rows, expected anchor and lower-level row keys, and requested modes | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every applicable blocking rule is satisfied | Continue to the declared routing node |
| not_required | No design rule applies to the requested operation | Continue without changing the request |
| blocked | An applicable blocker remains or required evidence is unavailable | Stop and require the declared correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DOCT.ENFORCE | decision | 5 | design_enforcement | passed->DOCT.ROUTE;not_required->DOCT.ROUTE;blocked->DOCT.ERROR | DOCT.DEFAULTS | stop | After validation, dependencies, lookups, and defaulting are complete |
