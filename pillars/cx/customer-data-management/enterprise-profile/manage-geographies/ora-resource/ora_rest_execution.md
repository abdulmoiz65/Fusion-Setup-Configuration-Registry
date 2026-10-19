# REST Execution

## Runtime Sources

| Source | Purpose |
|---|---|
| core.fusion-api.apps-common | Read configured site-level profile values without duplicating OAuth or REST transport |
| core.fusion-api.ess-job-submitter | Validate, submit, and poll the ESS request without duplicating scheduler logic |
| core.fusion-api.rest-api-client | Perform the read-only Scheduler collection query used only to recover an uncertain submission when the durable checkpoint is unavailable |
| core/fusion-api/apps-common/references/profile-options.md | Site-level profileOptions child-resource contract |
| https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-ess-rest-scheduler-v1-requests-post.html | Latest working published Scheduler REST submit contract verified for this skill |
| https://docs.oracle.com/en/cloud/saas/customer-data-management/fageo/import-geography-reference-data-licensed-by-oracle.html | Oracle geography import behavior and completion indicators |
| core.fusion-api.rest-api-client | Perform framework-version-9 CX object metadata, mapping_only import mapping REST operations without task-local transport |
| core/data-loader/scripts/upload_and_initiate.py | Native full_import preflight, immutable artifact verification, CRM document upload, and CX initiation |
| core.data-loader | Mandatory orchestration, task validation, immutable preview, approval, and authorization before any CX import adapter operation |
| core.data-loader.task-hook | Build, approve, and verify the immutable artifact envelope passed to ESS and CX mutation adapters |
| core/data-loader/SKILL.md | Authoritative native CX Import approval, reporting, and status boundary |
| references/import-mapping-definitions.json | Task-owned stable structure and hierarchy import mapping names, object codes, descriptions, and ordered column pairs |
| Data Loader-authorized REST core service | Required execution path for mapping_only importMappings and mapping-column operation; send REST-Framework-Version 9 |
| https://docs.oracle.com/en/cloud/saas/sales/faaps/op-importmappings-get.html | Current Fusion collection lookup contract used by the authorized REST core service for exact mapping resolution |
| https://docs.oracle.com/en/cloud/saas/sales/faaps/op-importmappings-post.html | Current Fusion nested import-mapping create contract used by the authorized REST core service |
| https://docs.oracle.com/en/cloud/saas/sales/faaps/op-importmappings-mappingnumber-child-importmappingcolumns-get.html | Current Fusion mapping-column read contract used by the authorized REST core service for drift comparison |
| https://docs.oracle.com/en/cloud/saas/customer-data-management/faicd/import-your-country-structure-data.html | Creation-only Country Structure file and existing-structure behavior |
| https://docs.oracle.com/en/cloud/saas/customer-data-management/faicd/import-your-geography-data.html | Creation-only Geography file requirements and restrictions |

## Delegated Execution Boundary

This resource defines only the Manage Geographies business operation, its
object-specific inputs, required evidence, and task-local outcome transitions.
It does not implement authentication, HTTP transport, UCM staging, ESS
submission or polling, retry mechanics, artifact storage, or cross-task
workflow coordination. Each such action is performed exclusively by the named
`core.*` service under that service's current contract. References to request
paths, headers, command modes, checkpoints, or adapters identify the
task-specific values supplied to the core service; they are not a task-local
transport or workflow implementation. The rule registry retains only local
Manage Geographies order and outcomes.

## Execution Contract

| Situation | What Happens |
|---|---|
| Profile preflight requested | Invoke core.fusion-api.apps-common twice against the exact profileOptions siteProfileOptionValues child collections with `fields=ProfileOptionValue` and `onlyData=true` |
| ORA_HZ_ENABLE_DAAS_LOQATE is Y and ORA_HZ_DAAS_GEO_ENDPOINT is nonblank | Report each validation and continue immediately without a profile write or confirmation prompt |
| ORA_HZ_ENABLE_DAAS_LOQATE is missing or not Y | Build one eligible remediation plan and show `ORA_HZ_ENABLE_DAAS_LOQATE`, its safe current state, and proposed `Y` in the single geography execution preview; explicitly ask whether the user wants Loqate as the source for geography data and explain that doing so requires enabling the profile option |
| ORA_HZ_DAAS_GEO_ENDPOINT is missing or blank | Ask the user to configure its site-level value in Fusion; stop before profile writes or import and re-read it on resumption |
| Loqate enablement change is approved | Verify the profile definition has `SiteLevelEnabled=Y` and `SiteLevelUpdatable=Y`; POST a missing `ORA_HZ_ENABLE_DAAS_LOQATE` `SITE` item or PATCH its existing eligible item. Never write `ORA_HZ_DAAS_GEO_ENDPOINT`; never retry automatically |
| Approved profile writes complete | Re-read both values, continue only when exact expected values are verified, and report only that prerequisite setup completed unless technical details are requested |
| Single business preview is declined | Make no prerequisite changes, do not submit the ESS request, and explain the manual Manage Geographies alternative |
| Post-change verification fails | Make no further changes and do not submit the ESS request |
| Preconditions are satisfied | Construct and persist a deterministic immutable artifact containing the exact environment, country name/code, job identity, parameters, business effect, correlation description, submission window, checkpoint path, and no-retry policy; calculate its SHA-256 |
| Direct execution intent is present and Loqate enablement is already Y | Build the Task Hook preview, display it, and ask `Do you want to proceed with submitting the reviewed archive?`; make no POST |
| Direct execution intent is present and Loqate enablement is missing or not Y | Build the Task Hook preview, display the exact enablement profile option and proposed Y, and end with `Do you want to use Loqate as the source for geography data? If so, we need to enable ORA_HZ_ENABLE_DAAS_LOQATE by setting it to Y. Do you want to proceed with enabling it and submitting the reviewed archive?`; make no POST |
| Latest immutable preview receives standalone approval | Approve and verify the exact artifact, persist its taskValidationEnvelope receipt, reverify it immediately before execution, then invoke core.fusion-api.ess-job-submitter with its existing `--submit-only`, correlation-description, and durable-checkpoint inputs |
| ESS submission succeeds | Read `execution_result.requestId` from the checkpoint, persist it, and immediately report it as the job ID before starting a separate `--request-id` tracking invocation |
| Submission process returns a session handle | Retain and poll the same process handle until exit; an empty initial output chunk is not an empty Fusion response |
| Submission output is interrupted | Inspect the durable checkpoint first; if it contains a valid requestId, track that ID and do not resubmit |
| Submission checkpoint is missing or unreadable | Do not submit again; use core.fusion-api.rest-api-client for one read-only Scheduler collection query using the exact correlation description, application, job definition, submission window, and country parameter; require exactly one match |
| ESS request is still running when wait_seconds elapses | Say that setup is still running, include the job ID, and retain last status internally so tracking can resume without resubmission |
| ESS request completes successfully | Explain the job ID plus Define Geography Country Structure and Define Geography Hierarchy Master Data as completed, clarify the separate geocoding and address-cleansing boundary, and ask whether to set up another country |
| ESS reports that geography data already exists or was already imported | Report that the selected country's data is already present and no new import was performed, include the job ID, preserve the terminal diagnostic, do not retry that country, and ask whether to set up another country using the normal fresh-run continuation |
| ESS request fails | Include the job ID and completed profile-change summary, give a concise business-level failure and recovery action, and retain other technical details internally unless requested |
| Profile, submission, or polling call fails | Proactively report the failed stage, environment, safe Fusion response summary, job ID when assigned, and recommended action; never expose tokens or silently reduce the result to an internal error class |
| Mapping lookup returns duplicates or drift | Stop as catalog_or_metadata_mismatch without PATCH, DELETE, overwrite, arbitrary selection, or another create |
| Mapping create response is uncertain | Reconcile only with the same exact authorized REST-core GET; never repeat the POST automatically |

## Endpoint

| Action | Method | Path |
|---|---|---|
| Read site-level profile value | GET | /fscmRestApi/resources/11.13.18.05/profileOptions/{ProfileOptionName}/child/siteProfileOptionValues |
| Create missing site-level profile value after confirmation | POST | /fscmRestApi/resources/11.13.18.05/profileOptions/{ProfileOptionName}/child/siteProfileOptionValues |
| Update existing site-level profile value after confirmation | PATCH | /fscmRestApi/resources/11.13.18.05/profileOptions/{ProfileOptionName}/child/siteProfileOptionValues/SITE |
| Submit Import Geography Data | POST | /ess/rest/scheduler/v1/requests |
| Track Import Geography Data | GET | /ess/rest/scheduler/v1/requests/{requestId} |
| Recover an uncertain submission | GET | /ess/rest/scheduler/v1/requests with an exact read-only filter |
| Resolve a stable import mapping for mapping_only through the authorized REST core service | GET | /crmRestApi/resources/11.13.18.05/importMappings with exact Name and ObjectCode filters |
| Read mapping columns for mapping_only through the authorized REST core service | GET | /crmRestApi/resources/11.13.18.05/importMappings/{MappingNumber}/child/ImportMappingColumns |
| Create a missing stable import mapping for mapping_only through the authorized REST core service | POST | /crmRestApi/resources/11.13.18.05/importMappings |

These paths describe underlying Fusion operations, not permission for task-local
calls. For mapping_only, complete `core.data-loader` orchestration first, then invoke mapping operations through
`core.fusion-api.rest-api-client` with `REST-Framework-Version: 9`; use
`core.data-loader`'s native helper for all full_import staging and initiation.

## ESS Request Fields

### Loqate ESS preflight and delegation

For this pillar's `oracle_loqate` branch, select this assisted ESS route before
execution. It is a narrow exception to the native file-import preflight
prerequisite in Data Loader and Task Hook: complete the checks below, then reuse
the existing Task Hook validation, preview, approval and artifact-verification
commands. Do not wait for a native loader preflight or treat its absence as a
missing ESS submission route. The shared skills remain unchanged; `full_import`
and `mapping_only` retain their existing Data Loader requirements.

Before Task Hook `data-load`, validate the exact task and active project Run
Book binding, configured target environment, required profile-read and ESS-submit
privileges, supported country and fixed job contract. Complete the selected
read-only profile checks, validate the payload and execution options, and verify
that artifact and checkpoint destinations are safe project workspace paths.
Persist this evidence as the Loqate preflight. Missing evidence, failed checks,
ambiguous identity or an unsupported country blocks approval and submission.
Do not invoke `upload_and_initiate.py`, fabricate a native file-import envelope,
or invent CSV mappings, UCM metadata or a loader business object for this route.

The JSON artifact must contain the exact target environment, task identity,
`job_contract`, `request_payload`, `execution_options`, country, business effect,
prerequisite change plan and durable checkpoint path. Its request payload uses
the fixed fields below and includes the unique correlation description. Persist
the request artifact and byte SHA-256 before evaluating Task Hook rules; include
the request in `finalData` and put that digest in `finalData.archiveSha256`.
Use the existing build, approve and verify Task Hook commands. They verify exact
bytes with `--archive <request.json>`; they do not require ZIP format. Never
mark unevaluated rules passed or manufacture an approval receipt.

Only after standalone business-preview approval and successful artifact
verification, build an `approved_submission` conforming to
`schemas/ess-delegation-contract.schema.json`:

- `contract_version`: `1.0`; `stage`: `approved_submission`.
- `task`: the validated `task_name` and `task_code`.
- `fusion_environment_context`, `job_contract`, `request_payload` and
  `execution_options`: copied from the verified immutable request.
- `approval.explicit_submission_approval`: `true`, derived from the verified
  Task Hook approval, never from the initial setup request.
- `approval.approved_payload_sha256`: SHA-256 of UTF-8 JSON serialization of
  the exact `request_payload` with sorted keys and compact separators
  (`sort_keys=True, separators=(",", ":"), ensure_ascii=False`). This payload
  digest is distinct from the digest of the whole request artifact.
- `audit_context`: the immutable artifact and verified Task Hook receipt
  references, artifact digest, Run Book binding and submission checkpoint.

Validate required fields, exact job/application/country/correlation values,
positive polling bounds, target/Run Book identity, payload hash and the schema
before handing off to `core.fusion-api.ess-job-submitter`. Map the verified
`request_payload` to its `--payload-file` input, use `--submit-only --output
<checkpoint>`, and retain the existing separate request-ID tracking invocation.
Do not reconstruct the payload from fresh defaults or independently supplied
CLI parameters after approval. The payload file must serialize the exact
approved object; verify its canonical digest again before submission.

| Field | Value Source | Required Behavior |
|---|---|---|
| jobDefinitionId | Fixed task contract | Use JobDefinition://oracle/apps/ess/fod/simplifiedsetup/geographies/SimplifiedGeoSetupJob |
| application | Fixed task contract | Use CrmEss |
| requestParameters.name | Fixed task contract | Use submit.argument1 |
| requestParameters.paramType | Fixed task contract | Use STRING |
| requestParameters.value | country_code from country_code_resolver | Use the normalized two-letter code |
| retries | Fixed safety policy | Use zero or omit so no automatic retry is introduced |
| description | Task-local correlation rule | Use `FDOS:manage-geographies:{project_id}:{country_code}:{run_id}` and persist it before POST |

## Internal Validation and User Disclosure

| Step | Requirement |
|---|---|
| Internal environment validation | Bind the execution plan to the exact Fusion environment identity |
| Internal dependency validation | Verify ORA_HZ_ENABLE_DAAS_LOQATE against Y and require ORA_HZ_DAAS_GEO_ENDPOINT to contain any non-null, non-empty value after trimming |
| Required user updates | Explain prerequisite readiness in business language, the country and environment, approved scope, job ID, structure and hierarchy status, and the next-country option after success |
| Normal user update | Explain what is being checked or configured for the resolved country in the selected Fusion environment, why it matters, what remains outside this task, and include the required status details above |
| Technical disclosure | Show UCM, object metadata, accounts, mappings, adapters, REST paths, payloads, hashes, job definitions, parameters, polling settings, or no-retry mechanics only when the user explicitly asks for technical details, troubleshooting, or audit evidence |

## Live Pattern

| Step | Requirement |
|---|---|
| Authentication | Start or refresh the configured Fusion authentication flow automatically without asking the user for permission; never request credentials or tokens in chat |
| Profile authorization | A direct request authorizes preflight only; when Loqate enablement is missing or not Y, display `ORA_HZ_ENABLE_DAAS_LOQATE`, proposed Y, and the combined Loqate-and-submission question; after its standalone approval apply and verify eligible changes without another prompt |
| ESS authorization | Treat a direct imperative as authorization to validate and build the immutable preview only; require a standalone affirmative reply to the standard Data Loader prompt before one submission |
| Profile mutation | POST a missing `ORA_HZ_ENABLE_DAAS_LOQATE` `SITE` record or PATCH its existing eligible record once, then re-read both profiles. Never create or update `ORA_HZ_DAAS_GEO_ENDPOINT`; do not retry a mutation automatically |
| Submission checkpoint | Require `project_id`; persist the execution plan, UTC window, verified Task Hook receipt, and artifact first, reverify the artifact immediately before invocation, then invoke core.fusion-api.ess-job-submitter with `--submit-only`, `--description`, and the checkpoint `--output` |
| Request-ID gate | Read the checkpoint after the submission process exits; require one positive integer `execution_result.requestId`, persist it, and report it before polling |
| Polling | Invoke core.fusion-api.ess-job-submitter again with `--request-id <captured-id>`, bounded wait_seconds and poll_interval values, and `--output` pointing to `.../current/ess-execution-result.json` |
| Polling authentication retry | Refresh a cache-managed token once and retry only request-ID tracking; never invoke submission again |
| Lost-output recovery | Inspect the checkpoint first. If absent, query the Scheduler collection read-only using the exact correlation description, `CrmEss`, fixed job definition, recorded UTC submission window, and country parameter. Accept exactly one match; zero or multiple matches block execution |
| Timeout | Stop polling, report the requestId as job ID, retain last status, and resume tracking instead of resubmitting |
| Success | Confirm the country and completion of both geography structure and hierarchy outcomes, include the requestId as job ID, explain the separate-feature boundary, and invite one next country |
| Already present | When the terminal error unambiguously states that data already exists or was already imported, say no new import was performed, include the requestId, preserve diagnostics, and invite one next country without retrying the same country |
| Failure | Retrieve the full status or process diagnostics available through the core skill and stop before retry |
| User-visible failure | Always summarize the failed stage and Fusion message safely, include the job ID when available, and recommend the next action even when technical details were not requested |
| Persistence | When project_id is supplied, write redacted validation, execution, and diagnostic outputs to the declared project paths |

## Read-Only Recovery Contract

Use recovery only when the submission process may have reached Fusion and the
durable checkpoint is missing or unreadable. Invoke
`core.fusion-api.rest-api-client` against the Scheduler requests collection;
do not implement task-local OAuth or HTTP transport.

1. Filter by the exact persisted correlation description, application
   `CrmEss`, fixed geography job definition, and recorded UTC submission window.
2. Request only the identifiers and safe status fields needed to reconcile the
   submission, ordered by submission time descending.
3. For each candidate, read its request details and require exactly one
   `submit.argument1` STRING parameter equal to the resolved country code.
4. Accept recovery only when exactly one candidate satisfies every condition.
5. Persist the recovered requestId and status before tracking it through the
   core ESS skill's `--request-id` path.
6. For zero or multiple matches, stop as `approval_blocker`; never infer a
   candidate and never issue another POST.

## User-Provided Import Contract

### Mapping-only REST contract

This subsection applies only to `mapping_only`. Full imports render these
definitions as CSVs and use the native Data Loader route below, without a
separate importMappings lookup/create or persisted MappingNumber prerequisite.

Load the selected definition or definitions from
`references/import-mapping-definitions.json`. For each mapping, canonicalize
`ObjectCode` plus the ordered `ColumnHeader`/`AttributeCode` pairs and calculate
a SHA-256 fingerprint. The structure create payload is:

```json
{
  "Name": "FDOS_MANAGE_GEOGRAPHIES_STRUCTURE_V1",
  "Description": "FSCR Manage Geographies country structure mapping version 1",
  "ObjectCode": "GeoStructureInterface",
  "ImportMappingColumns": [
    {"ColumnHeader": "CountryCode", "AttributeCode": "CountryCode"},
    {"ColumnHeader": "LevelNumber", "AttributeCode": "LevelNumber"},
    {"ColumnHeader": "GeographyType", "AttributeCode": "GeographyType"}
  ]
}
```

The hierarchy mapping is
`FDOS_MANAGE_GEOGRAPHIES_HIERARCHY_V1` for `GeographyInterface` and contains
the exact nineteen identity pairs in the task-owned JSON definition. Do not
derive either persistent mapping from runtime CSV contents.

Complete Data Loader validation and authorization before the REST core service invokes
the underlying Fusion collection GET, mapping-column GET, or collection POST.
Query by exact stable `Name` and `ObjectCode`. Reuse only one result with
the complete one-to-one column-pair set, canonicalized into the task-defined
order so REST return order alone is not drift. Create the complete nested
mapping only when no match exists. Persist `MappingNumber`, fingerprint,
environment, and `created` or
`reused` before any UCM upload. Duplicate or drifted results block execution;
never PATCH or DELETE. An uncertain create is reconciled only by the exact
authorized REST-core read and is never posted again automatically.

### Native Data Loader CX Import

For `full_import`, use the existing `core/data-loader/scripts/upload_and_initiate.py`
workflow. Do not use standalone CX prepare/approve/execute commands,
`upload-ucm --execute`, ERP Integration upload, or direct importActivities POST.
Data Loader owns transport and initiation; the pillar owns geography validation.

1. Validate the one-country structure and parent-first hierarchy locally using
   the task rules. Reject all update/delete/replacement intents. The helper
   exposes no ImportMode option; do not invent CREATE_ONLY payload controls.
   Fail closed if target support cannot establish the required additive behavior.
2. Select one stage's reviewed definition from `references/import-mapping-definitions.json`.
   With a UTF-8 CSV writer, emit exactly these two four-column tables, separated
   by an optional blank row:

   ```csv
   MAP NAME,MAP DESCRIPTION,IMPORT OBJECT,OBJECT DISPLAY NAME
   FDOS_MANAGE_GEOGRAPHIES_STRUCTURE_V1,FSCR Manage Geographies country structure mapping version 1,GeoStructureInterface,Country Structure

   COLUMN HEADER,TARGET ATTRIBUTE CODE,TARGET ATTRIBUTE DISPLAY NAME,SOURCE ATTRIBUTE CODE
   CountryCode,CountryCode,CountryCode,CountryCode
   LevelNumber,LevelNumber,LevelNumber,LevelNumber
   GeographyType,GeographyType,GeographyType,GeographyType
   ```

   For hierarchy use its reviewed Name, Description, `GeographyInterface`,
   display name `Geography`, and all nineteen ordered column pairs. Set each
   target/source attribute code to the reviewed AttributeCode/ColumnHeader and
   use AttributeCode as the deterministic target display label. Do not infer
   pairs from a partial data file or accept caller overrides.
3. Pass the mapping CSV and its canonical data CSV as one stage-specific group.
   Never group GeoStructureInterface and GeographyInterface together. Do not
   add JSON, manifests, or mapping-definition JSON to a CX ZIP. The mapping's
   IMPORT OBJECT supplies the object code; do not pass --cx-import-object-code.
   Let the helper resolve and normalize UcmAccount from exact-object metadata.
4. Run preflight without --approve-upload from the repository root:

   ```bash
   python3 core/data-loader/scripts/upload_and_initiate.py \
     --ide-file <stage-mapping.csv> --ide-file <stage-data.csv> \
     --cx-import --task-routed \
     --preflight-envelope-output <stage-preflight.json>
   ```

   Apply only the same explicitly selected --properties/--run-config overrides
   when needed. Add --cx-import-high-volume-load only for an explicit high-volume
   load request; there is no default HighVolume=YES. Resolve the Task Hook using
   task_context, HZ_MANAGE_GEOGRAPHIES, and task_sequence; validate its rules
   against the exact immutable ZIP retained by preflight. Complete Task Hook
   preview and approval, then persist its envelope for approved submission.
   Return the helper's approval-required report with the geography scope and
   additive/no-rollback boundary; include its required UCM Account disclosure.
   Follow core.data-loader's same-request auto-approval policy when applicable.
5. After approval, submit only the retained artifact and envelopes:

   ```bash
   python3 core/data-loader/scripts/upload_and_initiate.py \
     --approved-preflight-envelope <stage-preflight.json> --approve-upload \
     --task-validation-envelope <approved-stage-task-envelope.json>
   ```

   Pass no source files, --cx-import, mapping, object-code, high-volume, or
   routing arguments. Retain only identical explicitly selected environment and
   Run Book options. Do not rebuild sources, refresh live metadata, or rerun
   task validation after approval. Drift or missing artifacts require fresh
   validation and approval.
6. The helper uploads the mapping first and data CSVs in approved order through
   CRM Documents. It retains raw dDocName values, prefixes only the mapping ID
   with M_ in the semicolon-joined initiation contentId, and sends sourceType
   ORA_CX_IMPORT and cxImportObjectName to initiateDataLoad. Do not reproduce this
   transport in the pillar or manually supply document IDs.
7. Return the helper's Data Load In Progress table including Data Set Name,
   Load Type, Business Object Name, UCM Account, Content ID, and Request ID.
   Submission is not completion. Do not poll dataLoaderDataSets/dataSetErrors
   unless the user explicitly requests status, progress, results, counts, or errors.
8. For structure_and_hierarchy, initiate structure only and leave hierarchy
   pending. Resume at GEO.USER.STRUCTURE.STATUS or GEO.USER.HIERARCHY.STATUS only
   on an explicit status request; follow core.data-loader status
   guidance for the same returned data set; only confirmed completion without
   errors unlocks a fresh hierarchy preflight and stage approval. A failed,
   nonterminal, or uncertain structure blocks hierarchy. Do not resubmit from
   status or roll back successful structure if hierarchy fails.
9. On a partial upload or uncertain initiation retain approved artifacts and
   envelopes for reconciliation. Do not upload again or initiate a partial CSV
   group. Only the helper's documented HTTP 400/action 27503 retry without Run
   Book fields is allowed, preserving IDs and all CX fields. After accepted
   initiation let the helper remove internal envelopes; do not write an extra
   local initiation report, log, or run record.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GEO.PROFILE.APPROVE | decision | 9 | approval_gate | retired->GEO.DESIGN | GEO.READINESS | continue | Retired unreachable legacy node retained for registry compatibility; never route to it and never prompt the user |
| GEO.PREVIEW | step | 11 | preview_gate | ok->GEO.APPROVE;failure->GEO.FAILED | GEO.DESIGN | stop | Build the deterministic artifact, complete every read-only preflight, display one business-only preview, and ask the standard reviewed-archive question once |
| GEO.APPROVE | decision | 12 | approval_gate | approved_ready->GEO.EXECUTE;approved_with_remediation->GEO.PROFILE.UPDATE;declined->GEO.REFUSED | GEO.PREVIEW | stop | Require one standalone affirmative response to the latest unchanged business preview, verify the artifact, and persist taskValidationEnvelope |
| GEO.PROFILE.UPDATE | step | 13 | execution_gate | success->GEO.PROFILE.VERIFY;failure->GEO.FAILED | GEO.APPROVE | stop | Apply only eligible prerequisite changes included in the approved business preview; do not ask another question |
| GEO.EXECUTE | step | 15 | execution_gate | success->GEO.DONE;timeout->GEO.TIMEOUT;failure->GEO.FAILED | GEO.APPROVE | stop | Reverify the receipt/artifact, invoke the ESS submit-only contract, capture requestId, and track separately; never resubmit when output is uncertain |
| GEO.DONE | terminal | 16 | terminal | none | GEO.EXECUTE | continue | ESS reaches a terminal successful status; report the country, job ID, structure, and hierarchy outcomes, then offer another country |
| GEO.TIMEOUT | terminal | 17 | terminal | none | GEO.EXECUTE | continue | Loqate polling window expires while the request remains nonterminal; report the job ID and last business status |
| GEO.USER.PREVIEW | step | 20 | preview_gate | ok->GEO.USER.APPROVE;failure->GEO.FAILED | GEO.USER.VALIDATE | stop | Complete native stage preflight and exact-byte Task Hook validation before presenting the loader approval report; mapping_only retains its REST mapping preview |
| GEO.USER.APPROVE | decision | 21 | approval_gate | approved->GEO.USER.MAPPING;declined->GEO.REFUSED | GEO.USER.PREVIEW | stop | Approve the unchanged stage artifact and Task Hook preview under core.data-loader policy; persist its envelope |
| GEO.USER.MAPPING | step | 22 | execution_gate | full_import->GEO.USER.STRUCTURE;mapping_only->GEO.USER.MAPPING.DONE;blocked->GEO.BLOCKED;failure->GEO.FAILED | GEO.USER.APPROVE | stop | For full_import verify the reviewed stage mapping CSV already retained by preflight; only mapping_only reuses or creates REST mappings |
| GEO.USER.MAPPING.DONE | terminal | 23 | terminal | none | GEO.USER.MAPPING | continue | Every selected stable mapping was reused or created and persisted internally; report business completion and perform no file upload or import activity |
| GEO.USER.STRUCTURE | step | 24 | execution_gate | success->GEO.USER.PENDING;skipped->GEO.USER.HIERARCHY;failure->GEO.FAILED | GEO.USER.MAPPING | stop | When requested, submit only the approved structure preflight envelope through native Data Loader and stop after accepted initiation; otherwise skip |
| GEO.USER.STRUCTURE.STATUS | step | 25 | execution_gate | success->GEO.USER.HIERARCHY;pending->GEO.USER.PENDING;failure->GEO.FAILED | GEO.USER.STRUCTURE | stop | Only on an explicit status request, check the same structure data set through core.data-loader; require confirmed completion without errors before hierarchy preflight |
| GEO.USER.HIERARCHY | step | 26 | execution_gate | success->GEO.USER.PENDING;skipped->GEO.USER.DONE;failure->GEO.FAILED | GEO.USER.MAPPING | stop | Require compatible structure; validate and obtain approval for a fresh hierarchy artifact, then submit its native approved envelope and stop after initiation |
| GEO.USER.HIERARCHY.STATUS | step | 27 | execution_gate | success->GEO.USER.DONE;pending->GEO.USER.PENDING;failure->GEO.FAILED | GEO.USER.HIERARCHY | stop | Only on explicit status request, check the same hierarchy data set through core.data-loader and preserve any successful structure |
| GEO.USER.DONE | terminal | 28 | terminal | none | GEO.USER.HIERARCHY | continue | Requested status results confirm all requested stages completed without errors; report business outcomes and UI verification guidance |
| GEO.USER.TIMEOUT | terminal | 29 | terminal | none | none | continue | An explicitly requested bounded status check times out; retain the same data set identity and never resubmit |
| GEO.USER.PENDING | terminal | 30 | terminal | none | none | continue | A native CX load was initiated or remains nonterminal; return Data Load In Progress, stop without polling, and retain the hierarchy dependency |
