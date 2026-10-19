# Manage Training Suppliers Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_contact_person | Contact is supplied | Full name, person number, person ID, or work email | /hcmRestApi/resources/latest/workersLov?finder=findByWord;SearchTerms={url_encoded_search_terms}&onlyData=true&limit=100&fields=PersonId,PersonNumber,DisplayName,WorkEmailAddress | PersonId, PersonNumber, DisplayName, WorkEmailAddress | Prefer exact PersonId or PersonNumber; otherwise require explicit selection of one accessible worker | contactPersonId, contactPersonDisplayName, verified person number and email | Zero permits correction or Skip; many requires selection; never select automatically |
| inspect_existing_training_suppliers | Before proposing creation and after every REST upload or Data Loader create attempt | Exact requested supplier name; mutation-returned resource ID or resource number when available | GET /hcmRestApi/resources/latest/learningTrainingSuppliers?onlyData=true&limit=100; follow collection paging links or offset until `hasMore=false` | TrainingSupplierResourceId, TrainingSupplierResourceNumber, supplier title, status | Before create, retain every exact case-insensitive title match after complete paging. After create, prefer one exact resource ID or resource number match and require its title to equal the approved name; use an exact-name-only result only when it is unique | Existing or created supplier ID, number, title, and status plus the sanitized REST receipt | Pre-create zero matches continues; one or many matches requires use-existing or create-another intent. Post-create zero, many, incomplete, or identity-mismatched results are `unknown` and must not be retried automatically |
| validate_required_supplier_configuration | Set filtering or configured flexfields are enabled | Supplied Set and configured flexfield values | GET /hcmRestApi/resources/latest/hcmSetsLOV?finder=findByWord;SearchTerms={url_encoded_search_terms}&onlyData=true&limit=100&fields=SetId,SetCode,SetName,Description and GET /hcmRestApi/resources/latest/learningTrainingSuppliers/describe | SetId, SetCode, SetName, Description; resourcesDFF contexts, segments, writable attributes, and requiredness exposed by live metadata | Prefer exact SetCode or SetId; otherwise require explicit selection. Require every configured required DFF segment and validate optional retained values against live metadata | SetCode plus SetId/SetName evidence; validated context and segment values | Zero or many Set matches, inaccessible metadata, missing required segments, or invalid values block; never default COMMON or invent a context |
| validate_training_supplier_rest_contract | REST upload is selected, before payload construction and again if the environment changes | learningTrainingSuppliers REST resource | /hcmRestApi/resources/latest/learningTrainingSuppliers/describe | Collection create action; writable trainingSupplierTitle, trainingSupplierDescription, contact fields, retained configuration and related-material children; item or canonical readback link | Require collection POST support and validate every proposed JSON property as writable in the current environment | Exact endpoint, writable field catalog, approved JSON payload, and readback identity contract | Missing create support, inaccessible describe metadata, or an unsupported proposed property blocks REST upload |
| validate_training_supplier_dataloader_contract | Data Loader is selected, before source preparation and again before approval | learningTrainingSuppliers | /hcmRestApi/resources/latest/dataLoaderBusinessObjects?finder=findDataLoaderBos plus the returned business-object, child-component, attribute, and template links | BusinessObjectId, BusObjTopDiscriminator, component discriminator, attribute names, keys, data types, requiredness, flexfield contexts/segments, and template columns | Require exact BusObjTopDiscriminator learningTrainingSuppliers and validate every proposed Excel or DAT column against current metadata | Supported field catalog, accepted loader columns, template, and validation evidence | No exact match, inaccessible metadata/template, or an unsupported source column blocks Data Loader preparation |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A lookup path is `TBD` | Stop before presenting the task as executable; do not invent a service path |
| A lookup returns 401 or 403 | Classify as authentication or authorization failure, not no-match |
| A result is ambiguous | Show distinguishing values and require user selection |
| Duplicate or verification lookup | Use REST GET only; do not use the browser UI |
| Collection paging is incomplete | Stop; do not claim zero duplicates or successful verification |
| REST upload is selected | Run validate_training_supplier_rest_contract; do not preflight Data Loader unless the user selects a new route and approves a new proposal |
| Data Loader is selected | Run validate_training_supplier_dataloader_contract; do not issue direct REST POSTs unless the user selects a new route and approves a new proposal |
| Selected route is unavailable | Stop and request a new route choice; never substitute the other route silently |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TS.RESOLVE_REFERENCES | decision | 2 | reference_lookup | resolved->TS.CHECK_DEPENDENCIES;selection_required->TS.BLOCKED;blocked->TS.BLOCKED;failure->TS.FAILED | TS.VALIDATE_INPUT | stop | Resolve the selected REST or Data Loader contract, applicable contacts, existing suppliers, Set, and configured flexfields before proposal |
