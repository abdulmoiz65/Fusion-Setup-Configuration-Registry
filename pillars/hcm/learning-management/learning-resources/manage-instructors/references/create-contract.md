# Standalone creation and shared handoff

## Evidence and readiness

FDD: [OLC-116674, page 21981495973](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21981495973),
version 6 inspected 2026-09-23; sections Common scope, 3.0 Manage Instructors,
dependencies, validation and IN-AT-01 through IN-AT-07. Jira OLC-120237 provides
traceability, not an additional detailed contract. Examples are illustrative.

The supplied authoring payload declares learningInstructors, ADF_REST,
ORA_HCM_REST, MERGE_DELETE, MandatoryOnCreate=personId, surrogate instructorNumber,
WLF_RESOURCES_B.RESOURCE_NUMBER, empty user/foreign keys, null PostUrl/PatchUrl and
no EffectiveDated override. It does not prove current deployment, writable fields,
generated identity/defaults or child support. Never write tables from this metadata.
The last project metadata check returned HTTP 502 twice after authentication;
neither registration absence nor readiness was established.

Later metadata-only inspection (2026-09-23) succeeded for the instructor describe
endpoint. Its resourcesDFF custom attributes learnDffResChrac, learnDffResNum,
learnDffResDate and fawqaWlfResourceDff, and __FLEX_Context, reported mandatory=false.
ResourceId reported mandatory=true as parent identity, not custom user input.
This is point-in-time project evidence, not a universal tenant default or proof of
Data Loader child omission. The separate inspection route cannot grant create readiness.
The later validate-configuration route combines live global/context/default metadata
with the source-confirmed parent-entity DFF mapping for narrow root-only preflight;
it does not claim a successful write or verified runtime defaults.

Mandatory checks before a create preview:

1. Ready, current shared task graph, exact CUSTOM_MANAGE_INSTRUCTORS context.
2. Intended target and current account; active project Run Book with the instructor
   task. Do not reuse CAP task identity/approval or create a Run Book implicitly.
3. One uniquely resolved nominated ACTIVE person per row; explicit partial-name
   selection, fresh identity and complete accessible duplicate check. No inferred
   identities, intra-batch duplicates or existing-instructor updates.
4. Functional/data privileges WLF_MANAGE_TRAINING_RESOURCES and
   WLF_MANAGE_TRAINING_RESOURCES_DATA, PublicPerson scope and applicable loader/UCM
   privileges assessed using shared policy. Successful GET alone is not write proof.
5. Assess ORA_WLF_LEARN_ADMIN_RESOURCES_VBCS_ENABLED; conditional
   ORA_WLF_LEARN_FILTER_BY_SET_MAPPING and deployed WLF_RESOURCE_DFF mandatory
   fields/value sets. For explicitly deferred Set scope, execute the root-only
   validate-configuration contract in prerequisite-inspection.md. Require its
   current configuration_validated result; it does not assert Set is disabled.
   Required or supplied DFF inputs and Set-enabled creation remain unsupported.
   Booking search
   profile/index/ESS prerequisites do not gate basic instructor creation.
6. Exact deployed BO/template, explicit create mapping, personId input, generated
   instructor number/ID, omitted supplier, status and availability defaults verified.
   MERGE_DELETE is not sufficient proof. Missing target evidence is not approval.

The first increment accepts the minimal root only. Additional required Set/DFF
fields block it until their verified mapping is added; this limitation is not a
waiver of FDD requirements. Supplier association, children and all other writes
remain unavailable.

## Preparation, validation and one approval

Read current `core/data-loader/SKILL.md`, `references/user-friendly-output.md`,
`core/data-loader/task-hook/SKILL.md` and the returned execution guide in full.
Use the unchanged public interfaces; do not import another pillar's helpers.

1. Resolve the live template and attributes through the shared Data Loader.
   Default editable XLSX uses the supported spreadsheet runtime. When the user
   explicitly selects DAT/ZIP, prepare a UTF-8 root-only DAT from verified inputs:
   METADATA columns personId and RestAction; one MERGE row per selected person
   with RestAction=POST. Omit generated identities, supplier and optional DFF
   fields only after the current configuration check passes. This is source
   preparation, not schema validation. Pass the DAT through unchanged shared
   validate_data_load_file.py and the same task-routed preflight/Task Hook below.
   Do not use generate_sample_dat.py --format dat for this route: it also creates
   an attribute-details XLSX and therefore requires the spreadsheet runtime.
   Do not replace that runtime, bypass validation, or treat a supplied template
   as current without the shared live-schema check. Keep personnel DAT/ZIP files
   in protected private runtime storage, outside project/.
2. Create a draft with `build_proposal` after current person resolution. Its
   fingerprint binds version, request, target and people; it is not a readiness
   attestation or approval. Changing a person, input, row, target or version
   invalidates the old proposal/preview. Resolve duplicates before preview.
3. Shared preparation CLI (paths are private runtime paths; never secrets):

   ```text
   python3.11 core/data-loader/scripts/upload_and_initiate.py <source>
     --task-routed
     --properties <selected-properties> --run-config <project-run-config>
     --preflight-envelope-output <private-preflight.json>
   ```

   This invocation has no approve-upload flag. Shared code owns actual schema
   validation, conversion, immutable ZIP and authoritative preflight output.
   Do not reconstruct envelopes, refresh jobs, publish registration or replace
   missing metadata. Handle the shared preparation result as documented, not
   merely by assuming exit zero means approval readiness.
   For DAT, the filename must be learningInstructors.dat; do not pass
   --business-object, which the shared CLI allows only for CSV/XLSX.
4. On the final ZIP, `instructor_workflow.py check-archive --input <proposal.json>
   --archive <final.zip>` cross-checks exactly one root component, personId values,
   order and explicit POST rows. It does not validate target schema or privileges.
   The parser is a defensive cross-check, not a sample/template generation claim.
5. Require valid shared preflight taskRouted=true, mappingComplete=true and the
   same archive hash. Use Task Hook `data-load --task-context <context>
   --task-name "Manage Instructors" --sequence <selected-sequence>`. Ready means
   rules can run, not that they passed. Execute the returned graph and record
   honest ordered ruleResults. No readiness overrides for this approved scope.
6. Use `build-data-load-preview --input-stdin` with taskContextPath, taskName,
   sequence, ruleResults and finalData containing the archiveSha256, proposal
   fingerprint/version, target, operation and exact inputs. Include the source
   proposal in finalData so its revision is bound by the shared preview hash.
   Ensure only approved private runtime storage receives real identities.
7. Present current people, supplier=None, known omissions/defaults, warnings,
   target, operation, row count and exact artifact for the one shared approval.
   A previous general "go ahead" or candidate selection is not that approval.
8. After explicit approval, Task Hook approve-data-load-preview, then
   verify-approved-data-load-archive produces the authoritative validation envelope.
   Persist it unchanged. Any modified bytes/context/proposal require fresh preview
   and approval; no hand-authored approved flags, waiver or readiness override.

## Submission and separately requested verification

Only after the above exact approval, invoke the unchanged shared uploader with
`--approved-preflight-envelope`, `--task-validation-envelope`,
`--approve-upload`, the same properties and run-config. Do not pass `--task-routed`
on this submission: task routing is retained in the approved preflight, and the
shared CLI rejects routing overrides with that envelope. No source revalidation,
repackaging or refreshing lookups after approval. No private POST alternative.
Shared upload_approved_preflight validates target, Run Book, artifact and Task Hook
binding before transport. Preserve its documented response and retry semantics;
add no instructor retry loop. Stop uncertain outcomes and reconcile before retry.

Return initiation output immediately, preserving shared Markdown. On a separate
user request for status/results, use shared get_data_load_info.py for terminal
status, loaded/failed counts and row-level errors, then declared shared GET readback
by each personId. Do not equate submission, completed job and verified business
state. Require exactly one accessible instructor, linked person, generated number,
instructorStatus and absent supplier; missing response fields stay unknown.
Readback names instructorStatus (UI layout.json:83), not CAP's status attribute.
Scheduling availability and child state remain separately unverified.

For a partial batch, correlate every approved row and retain successes; never
replay the whole batch. A concurrent WLF_LEARNTOP_DUP_INSTRUCTOR rejection needs
read-only reconciliation. No cleanup deletion, configuration repair or extra load.
