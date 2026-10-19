# Self-Paced Learning Input Validation

Sources: OLC-116681 FDD version 5 section OLC-120241, Oracle public
Self-Paced Learning REST documentation, sanitized raw target Describe evidence
reviewed 2026-09-22, and the supplied draft-create-then-activate HAR trace.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Request identity | target environment; requested operation; row identifier for multi-row input | Stop the affected request or row before preview | Supply one exact target and a supported operation | All requests | |
| Ordinary item definition | title; subtype or content type; content intent; learning item number and visibility before execution | Return the missing values without creating a payload | Supply business values; resolve target codes where the user supplied labels | Ordinary create | resolve_self_paced_lookup_value |
| Demonstration request | optional industry, domain, or topic; optional count from 1 through 10 | Apply only documented demo defaults | Generate reviewable candidates; omitted count defaults to 10 | Demonstration generation | |
| Content source | one absolute supported URL or one staged binary reference; declared media type; status and autoCommit only for a standalone child create when current child Describe requires them | Stop content processing for the affected row | Supply one supported source; omit status and autoCommit from a parent deep insert and verify server-derived values | Create item with content, add content, replace content, or reprocess | |
| Existing item identity | exact learningItemNumber or technical learningItemId; current fingerprint | Stop the affected operation | Resolve exactly one current item and follow its returned link | Read, update, activate, delete, publish content, reprocess, or content CRUD on an existing item | resolve_self_paced_identity |
| Data Loader route | exact learningSelfPacedItems registration; current template and components; selected supported operation | Stop mutation preparation for the affected row | Resolve through core.data-loader; a raw REST Describe or taxonomy mapping is not registration evidence | Any create or update mutation | resolve_self_paced_loader_registration |
| Owner | person number, username, work email, or sufficiently exact display identity | Stop only when an owner was requested or required by the approved request | Resolve one authorized readable Worker or PublicWorker without using a fuzzy first match | Owner is supplied | resolve_self_paced_owner |
| Language | exact language code or label | Stop only when language is supplied or required | Resolve one active installed target language and its canonical code | Language is supplied | resolve_self_paced_language |
| Catalog profile and audience | exact profile number or exact name; audience evidence when private | Keep the item in draft | Resolve one active usable profile and applicable audience evidence | Private visibility, publish, or demo default profile is requested | resolve_self_paced_catalog_profile |
| Questionnaire | exact subscriber, questionnaire code, and applicable version | Stop only the content row that requires it | Resolve one active compatible questionnaire | Assessment or observation content requires a questionnaire | resolve_self_paced_questionnaire |
| Filtered list | ListId; or exact Name with Subscriber and ObjectName; compatible ListScope | Stop filtered-list validation | Resolve identity and active state; do not infer association write support | A filtered list is selected | resolve_self_paced_hcm_list |
| Extensible attributes | WLF_LEARNING_ITEM context and exact target-returned segment definitions | Stop extensibility processing | Refresh current target metadata and validate every segment and value | DFF values are supplied | resolve_self_paced_dff |
| Approval evidence | immutable preview fingerprint; explicit approval; Objective and Ideal Learner omission acceptance when shown | Do not mutate | Rebuild a fresh preview and obtain approval for its exact contents | Any live mutation | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A demo count is omitted | Default required | Generate 10 candidates | |
| A demo count exceeds 10 or is less than 1 | Invalid | Correct or split the request before preview | |
| A create number already exists | Duplicate | Stop the affected row and return exact collision evidence | resolve_self_paced_identity |
| An exact title exists but the number differs | Collision evidence | Show the exact-title matches for user resolution; do not treat title as identity | resolve_self_paced_identity |
| A lifecycle status, visibility, content type, or reason is supplied as a label | Lookup required | Resolve one exact enabled code from the lookup type declared by current target metadata | resolve_self_paced_lookup_value |
| Item or content state differs from the approved fingerprint | Stale | Refresh, revalidate, rebuild the preview, and obtain new approval | resolve_self_paced_identity |
| An invalid row occurs in multi-row input | Row blocked | Exclude only that row and show its correction; preserve other independently valid rows | |
| A write outcome for any row is uncertain | Batch paused | Stop further writes and reconcile the uncertain row before a new attempt | resolve_self_paced_identity |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Operation is documented | Accept read, create, update, activate, delete, publish content, reprocess, and documented content CRUD; reject user-facing upsert | Every request | |
| Number and visibility are resolved | Require learningItemNumber and one exact enabled visibility code before parent POST | Create | resolve_self_paced_lookup_value |
| Content type and source agree | Reject unsupported or mismatched URL, binary, media, provider, questionnaire, or processing values before staging | Create content or replace content | |
| URL is usable | Require an absolute allowed-protocol URL and perform only an authorized safe reachability check | URL content | |
| Binary reference is usable | Require an accessible staged reference, declared supported MIME type, permitted size, and no binary body in project artifacts | Binary content | |
| Parent deep-insert content contract | Omit status and autoCommit; after creation require content status ORA_ACTIVE and autoCommit Y from readback | Parent create includes content | |
| Standalone child-create minimums | Require status and autoCommit only when a listed Direct REST child exception is selected and current child Describe requires them | Standalone content child create exception | resolve_self_paced_lookup_value |
| Activation contract | Set learningItemStatus to ORA_ACTIVE through a supported Data Loader update; when unavailable, allow only the returned-item PATCH exception with Effective-Of RangeMode=UPDATE | Activate | resolve_self_paced_identity |
| Activation readback | Require Active status, learningItemDraftExists N, learningItemPublishedExists Y, and unchanged approved content source | After activation | resolve_self_paced_identity |
| Dates are coherent | Reject an end date before the start date and values outside target-supported formats | Dates are supplied | |
| Owner is exact | Require one active accessible person and preserve only the exact identifier that the current writable field accepts | Owner is supplied | resolve_self_paced_owner |
| Language is exact | Convert a user-facing label to one installed active target code and verify target serialization before payload construction | Language is supplied | resolve_self_paced_language |
| Objective and Ideal Learner are preview-only | Show generated text and explicitly state that it will not persist; require omission acceptance and never map it to another REST field | Demo output includes either value | |
| Draft, activation, and content publish are separate | A parent create or update does not imply activation; the collection publish action is not UI Activate | Create, update, activate, or publish content | |
| Current identity is exact | Zero or multiple number or ID matches block the row; title results are collision evidence only | Existing-item operation or create collision check | resolve_self_paced_identity |
| DFF context is target-confirmed | Reject a context other than WLF_LEARNING_ITEM or a segment absent from current target metadata | DFF values are supplied | resolve_self_paced_dff |
| Filtered-list association is not inferred | Reject a requested association write that is absent from the Self-Paced Learning schema | Filtered-list association write is requested | resolve_self_paced_hcm_list |

## Multi-Row Validation

| Rule | What Happens |
|---|---|
| Independent rows | Each row gets its own operation, identity, dependencies, validation result, preview fingerprint, approval state, submission result, and readback result |
| Mixed validity | Invalid rows are corrected or explicitly excluded; valid rows are never used to hide invalid-row failures |
| Aggregate approval | The aggregate manifest fingerprint covers every included row fingerprint and exclusion; changing one row invalidates aggregate approval |
| Write uncertainty | Stop subsequent submissions after an uncertain mutation so replay cannot duplicate a row |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SPL.VALIDATE_INPUT | decision | 10 | validate_input | valid->SPL.CHECK_DEPENDENCIES;invalid->SPL.HANDLE_ERROR | none | stop | A Self-Paced Learning request or row is normalized |
| SPL.EVALUATE_RESULT | decision | 70 | evaluate_result | verified->SPL.RETURN_SUCCESS;partial->SPL.HANDLE_ERROR;failed->SPL.HANDLE_ERROR;indeterminate->SPL.HANDLE_ERROR | SPL.AUTHORIZE_EXECUTION | stop | Validation-only evidence or a submitted mutation is reconciled with the approved preview |
