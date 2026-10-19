# Sequential DAT Upload Orchestration

Read this reference only when the user explicitly requests live execution of
Question Library, Questionnaire Template, or Questionnaire DAT candidates.
Local generation and validation remain governed by
[HDL DAT Generation Contract](hdl-dat-generation.md).

## Boundary

The Questionnaire skill owns the domain order and dependency gates. It does
not implement upload or loader mechanics. For every ready artifact, invoke
`core.data-loader` with exactly one source path and follow its current
validation, Task Hook, preview, approval, upload, initiation, status, output,
and redaction contracts.

Approval is always obtained before a state-changing upload. Interpret a request
to approve after each upload as follows: after one accepted load is verified,
prepare the next file and obtain a new approval for that next upload. Never ask
for approval after bytes have already been uploaded, never request one bulk
approval, and never reuse an earlier approval.

## Request Contract

For more than one candidate, require `sequential_live_import_request` to state:

- the exact target environment identifier;
- `execute_all: true`;
- `monitor_status: true` when Data Loader status checks should occur after each
  accepted initiation; and
- one selected `post_load_readback_source`: a current approved target export
  supplied in task context, `shared.setup-export.task-level-export`, or another
  read-only route explicitly selected by the active workflow and documented by
  the applicable task skill.

If `monitor_status` is absent or false, process at most one approved file and
stop after initiation. If no post-load readback source is selected,
the queue may submit a standalone file but must stop before preparing any
dependent file. Never infer monitoring authorization or invent a product
readback endpoint.

Selecting `shared.setup-export.task-level-export` identifies the readback
route; it does not approve creation of an export process. Immediately before
each such export, present the exact target environment, owning TaskCode, and
operation `Create task-level setup export`, then obtain explicit approval for
that export. A DAT upload approval does not authorize an export, and an export
approval does not authorize a DAT upload. A current approved export already
supplied in task context requires no new live export action.

## Candidate Files

Build `ordered_data_load_queue` only from the current
`immutable_data_loader_handoff`. A candidate queue entry must have:

- one exact project-workspace path;
- one logical DAT filename and registered top-level discriminator;
- one SHA-256 bound to the current handoff;
- a supported create-only `MERGE` operation;
- a passed local generation result, or an explicit run-scoped `overridden`
  result whose handoff preserves every exception and requires Task Hook
  readiness override, with no other unresolved blocker;
- the same explicitly selected target environment as every other queue entry.

Record each candidate initially as `ready` or `pending_dependency`. Apply
predecessor and exact target-readback requirements when advancing that entry to
`ready`; do not require future readback evidence merely to list a later
candidate in the ordered queue.

Do not scan a directory or use every file returned by a glob. Exclude live UCM
header templates, attribute workbooks, sample DATs, FSM baselines, stale run
directories, superseded candidates, unsupported translations, blocked files,
and any DAT not named by the immutable handoff. If the handoff contains both a
DAT and its single-member validation ZIP, enqueue the logical load once and use
the exact source selected by the handoff; never submit both.

## Queue Order

Preserve this order when the corresponding candidate artifact exists:

1. `Question.dat`
2. `QuestionTranslation.dat`
3. `QuestionnaireTemplate.dat`
4. `QuestionnaireTemplateTranslation.dat`
5. `Questionnaire.dat`
6. `QuestionnaireTranslation.dat`

Bind every entry to its owning setup task:

| DAT | Task code |
|---|---|
| `Question.dat`, `QuestionTranslation.dat` | `HRT_MANAGE_QUESTIONS` |
| `QuestionnaireTemplate.dat`, `QuestionnaireTemplateTranslation.dat` | `HRT_MANAGE_QUESTIONNAIRE_TEMPLATES` |
| `Questionnaire.dat`, `QuestionnaireTranslation.dat` | `HRT_MANAGE_QUESTIONNAIRES` |

The current executable generation contract marks
`QuestionnaireTemplateTranslation.dat` unsupported. Its position is reserved,
but it must not enter the queue until the generation contract supports it and
the exact template-version readback is bound.

Every translation follows successful verification of its parent. A template
requires exact active readback of every referenced Question Library version in
the same subscriber. A questionnaire requires exact active readback of every
referenced question and every supplied or route-required template in the same
subscriber. An accepted initiation alone does not satisfy these gates.

Data Loader terminal status is process evidence, not object readback. Resolve
post-load object state only from a current approved target export/readback in
task context, a separately approved `shared.setup-export.task-level-export`
artifact, or another task-documented route explicitly selected by the active
workflow. If no such route is available or the evidence is ambiguous, stop and
classify the next entry as `blocked`; do not invent a REST, browser, SQL, or
first-match lookup.

## Per-File Cycle

Run this complete cycle for queue entry `n` before preparing entry `n + 1`:

1. Confirm the target environment, task, discriminator, operation, source path,
   source SHA-256, and predecessor readback evidence. Fail closed on a mismatch.
2. Invoke `core.data-loader` with only this entry's source path and without its
   upload-approval flag. Do not pass another DAT, XLSX, or ZIP in the same call.
3. Let `core.data-loader` perform live source and schema validation, build the
   immutable one-file upload artifact, run Ora Resource Task Validation, and
   present its standard approval preview.
4. Stop for the exact standalone approval requested by `core.data-loader`.
   Approval is bound to this target and immutable artifact only. A conditional,
   embedded, declined, stale, or changed-artifact response is not approval.
5. After approval, invoke `core.data-loader` for the same source and approved
   bytes using its approval path. Let core revalidate immediately before the
   first POST, upload the content, and initiate exactly one data load.
6. Do not add a second pillar approval for that same upload. Preserve the exact
   core success or failure result and do not submit another queue entry in the
   same approval cycle.
7. Only when the request explicitly sets `monitor_status: true`, make one core
   status request for the accepted load. Do not poll repeatedly. If the result
   is nonterminal, stop with the existing request ID and next-check action until
   the user explicitly requests another status check. If monitoring was not
   selected, stop after initiation until the user requests status.
8. After terminal success, obtain exact post-load object evidence from the
   request's selected `post_load_readback_source`. A task-level export is a
   separate routed external operation. Present the exact selected target
   environment, the exact owning TaskCode, and `Create task-level setup export`,
   then obtain explicit approval
   immediately before invoking `shared.setup-export.task-level-export`. Use its
   own bounded polling and failure rules. If exact readback cannot be obtained,
   stop; Data Loader success alone does not unlock a dependent entry.
9. Only after terminal success and exact required readback may the skill
   prepare entry `n + 1`. Present that entry's new immutable preview and stop
   for its independent Data Loader approval.

The user's initial request to process all files establishes the desired queue;
it does not approve any upload. Each approval authorizes at most one unchanged
`core.data-loader` submission.

## Failure and Stop Rules

Stop the queue and leave all later entries unsubmitted when any of these occurs:

- input, path, handoff, hash, environment, schema, or Task Hook validation fails;
- a reference, predecessor, duplicate check, or exact readback is missing or
  ambiguous;
- approval is declined, absent, stale, conditional, or bound to different
  bytes;
- a required task-level export approval is missing, declined, stale, or scoped
  to another environment, TaskCode, or operation;
- authentication or authorization remains invalid after the single
  core-managed cached-token refresh allowed by `core.data-loader`;
- upload or initiation fails, times out, or has an uncertain outcome;
- the explicitly requested status check remains nonterminal, or the load fails,
  partially succeeds, or does not match readback; or
- any queued source, target, operation, or handoff evidence changes.

Do not skip a failed dependency, combine later files, roll back a successful
load, or retry a live upload or initiation automatically. Restart only from a
fresh immutable preview and approval after the blocker is resolved. Retain the
safe core result and one next action; redact tokens, credentials, token-cache
contents, private keys, and sensitive payloads.

## Durable Checkpoint

The parent project workflow, not `core.data-loader`, writes one sanitized
`sequential_data_load_checkpoint` before every approval pause and after each
state transition. Use append-only checkpoint versions under the parent skill's
declared project workspace location. Record only:

- target environment identifier without credentials;
- logical filename, exact source path, SHA-256, task code, and discriminator;
- queue state: `pending_dependency`, `ready`, `previewed`, `approved`,
  `submitted`, `verified`, `declined`, or `blocked`;
- current and next pending entries;
- the Data Loader request ID when available; and
- sanitized blocker class, message, timestamp, and next action.

Do not store raw core responses, OAuth material, token-cache contents, upload
payloads, full DAT content, hidden Fusion identifiers, or the user's approval
message. On resume, revalidate the source hash, target, operation, and live
gates; a checkpoint never substitutes for a fresh core preview or approval.

## Completion

The queue is complete only when every in-scope candidate has its own accepted data
load and all dependency-required terminal-status and exact-readback checks have
passed. Report files in queue order with their completed or stopped stage. Do
not claim that later objects were loaded merely because their DAT files were
available locally.
