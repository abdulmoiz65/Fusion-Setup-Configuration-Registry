# Self-Paced Learning Dependency Readiness

Evaluate dependencies per operation and per row. A conditional dependency that
does not apply is Not Required and must not block an unrelated operation.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Data Loader BC REST registration | Resolve learningSelfPacedItems through core.data-loader and validate the current template, components, and selected operation |
| 2 | Direct REST evidence | Use REST only for reads or an operation-specific exception named by the task skill |
| 3 | Exact current target | Resolve a duplicate check or existing item through an exact finder and returned opaque link |
| 4 | Requested references | Resolve only owner, language, lookup, profile, questionnaire, list, and DFF evidence used by this row |
| 5 | Fresh state | Re-read current state immediately before an approved mutation and compare its fingerprint |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| SPL-DEP-LOADER | learningSelfPacedItems Data Loader registration and operation | Yes | Any create or update mutation | Lookup | Current target Data Loader business-object metadata, template, components, and operation contract through core.data-loader | resolve_self_paced_loader_registration | Taxonomy metadata and raw REST Describe do not prove that the business object or selected operation is registered | Correct the registration or select only a documented operation-specific exception | Exact discriminator, template, components, selected operation, and evidence fingerprint |
| SPL-DEP-REST-CONTRACT | learningSelfPacedItems wire contract | Conditional | Read-only REST or a named Direct REST exception | Satisfied | Oracle public REST documentation and sanitized raw target Describe with 20 resource nodes, 410 attributes, 77 LOV-decorated attributes, and 300 queryable attributes | | Parent and child reads, activation PATCH, publish, reprocess, delete, exact finders, and content routes are operation-specific evidence | Select a supported read or listed exception and follow returned links | Route, method or action, request fields, response fields, and child links |
| SPL-DEP-IDENTITY | Exact item identity and state | Conditional | Create collision check or any operation on an existing item | Lookup | Current target learningSelfPacedItems collection and returned links | resolve_self_paced_identity | A unique target and fresh state are required for correct planning and readback | Supply an exact number or technical ID | Identity, returned item link, current state, usage, content, processing state, and fingerprint |
| SPL-DEP-OWNER | Worker or PublicWorker owner identity | Conditional | Owner is supplied or the approved request requires owner validation | Lookup | Read-only Worker and PublicWorker resources available on the target | resolve_self_paced_owner | A display label alone is not a safe writable identity | Supply person number, username, work email, or sufficiently exact identity | Exact person evidence and writable target identifier |
| SPL-DEP-LANGUAGE | Installed active language | Conditional | Language is supplied | Lookup | Current target languagesLOV | resolve_self_paced_language | A user-facing label is not necessarily the REST code or serialization | Supply an exact language label or code | Language code, label, installed state, active state, and serialization evidence |
| SPL-DEP-LOOKUP | Enabled target lookup values | Conditional | Status, visibility, content type, reason, or another lookup-backed field is used | Lookup | Exact commonLookupsLOV route declared by current target metadata | resolve_self_paced_lookup_value | Describe identifies lookup types but not the target's current enabled values | Supply the intended business meaning | Lookup type, code, meaning, enabled state, and validity |
| SPL-DEP-CATALOG-PROFILE | Catalog Administration Profile and audience | Conditional | Private visibility, publish readiness, or demo default profile is needed | Lookup | Current target learningCatalogProfiles read contract | resolve_self_paced_catalog_profile | Publishing and demo defaults must not guess a target profile | Supply an exact profile or request the single verified default | Profile number, ID, name, status, visibility, default flag, processing state, and audience evidence |
| SPL-DEP-QUESTIONNAIRE | Questionnaire reference | Conditional | Content uses a questionnaire | Lookup | Current target questionnaire read contract | resolve_self_paced_questionnaire | A referenced questionnaire must exist and be compatible | Supply subscriber, code, and applicable version | Exact questionnaire identity, status, subscriber, purpose, and version |
| SPL-DEP-HCM-LIST | HCM list identity and active state | Conditional | A filtered list is selected | Lookup | Current target hcmLists read contract | resolve_self_paced_hcm_list | List lookup proves identity, not Learning association semantics | Supply ListId or exact name plus Subscriber and ObjectName | ListId, Name, Subscriber, ObjectName, ListScope, and active-state evidence |
| SPL-DEP-DFF | WLF_LEARNING_ITEM DFF definition | Conditional | Extensible attributes are supplied | Lookup | Current target returned DFF link or Describe metadata | resolve_self_paced_dff | Environment-specific segments are not portable | Supply the intended context and segment values | Context, exact segments, types, value rules, and target timestamp |
| SPL-DEP-CONTENT-STATE | Content and asynchronous processing state | Conditional | Publish, replace, reprocess, content delete, or readback depends on content readiness | Lookup | Current item content links and changeRequests | resolve_self_paced_identity | An accepted request is not proof that required content finished processing | Wait for bounded reconciliation or correct the content state | Content identity, status, binary state, processingStatus, process identifiers, and timestamps |

## Dependency Classification

| Result Category | When Used | Can Continue? |
|---|---|---|
| Ready | Every applicable mandatory dependency has one exact current result | Yes, but a mutation still requires fresh approval |
| Blocked | An applicable contract, exact identity, current value, or reference is missing or ambiguous | No for the affected operation or row |
| Not Required | The conditional dependency does not apply to this operation or row | Yes without running that lookup |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SPL.CHECK_DEPENDENCIES | decision | 20 | resolve_dependency | ready->SPL.RESOLVE_REFERENCES;not_required->SPL.RESOLVE_REFERENCES;blocked->SPL.HANDLE_ERROR | SPL.VALIDATE_INPUT | stop | After input validation and before references, defaults, or preview |
