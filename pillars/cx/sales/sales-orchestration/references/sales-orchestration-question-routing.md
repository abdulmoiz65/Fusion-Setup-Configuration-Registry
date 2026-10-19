# Sales Orchestration Question Routing

## Contents

- [Purpose](#purpose)
- [Question Classes](#question-classes)
- [Task Selection](#task-selection)
- [Answer Mode Before Execution](#answer-mode-before-execution)
- [Source Selection](#source-selection)
- [Response Status](#response-status)
- [Write and Import Boundary](#write-and-import-boundary)
- [Response Contract](#response-contract)

## Purpose

Use this reference to handle any question about the Sales Orchestration
functional area or its nested tasks without treating every question as a live
API request. Classify the question, select the task-specific source, and return
a sourced answer, a clarification, a route, a source gap, or an unsupported
operation result.

Generic coverage does not authorize invented product behavior, direct external
calls, or mutations outside the active implementation workflow.

## Question Classes

Classify the complete user request into one or more of these classes:

| Class | Examples of intent | Required handling |
|---|---|---|
| `CONCEPT` | What is it, why is it used, how do the task objects differ? | Answer only from loaded task sources; otherwise return `SOURCE_GAP`. |
| `MODEL` | Fields, status values, translations, objectives, activities, artifacts, attributes, accessors, relationships | Load the task's BOSS contract and return only documented metadata. |
| `LIFECYCLE` | Draft, active, archive, activation, publication, state transitions | Return documented states and behavior; mark undocumented transitions or validations as `SOURCE_GAP`. |
| `SETUP` | Configuration, sequencing, dependencies, UI access, prerequisites | Load the task skill and its dependency/security sources. Distinguish setup-screen access from API access. |
| `SECURITY` | Profile-option readiness, Security Console role provisioning, roles, duties, privileges, permission groups, security views, data policies, ESS synchronization | Load the task security reference and both shared security procedure references in full, then return the complete applicable contract. |
| `API` | Endpoint, method, fields, filters, query body, sorting, pagination, effective date | Load the task BOSS or Knowledge Management reference. Explain the contract without calling Fusion unless execution is requested. |
| `LIVE_READ` | List, find, retrieve, count, filter, inspect, test search | Use the task's controlled read workflow only when the active project workflow selects the external-operation step. |
| `TROUBLESHOOT` | 400, 401, 403, 404, empty results, invalid filter, OAuth, transport, result interpretation | Load task error handling and the relevant API/security source; classify the observed evidence without guessing. |
| `WRITE` | Create, update, patch, delete, activate, archive, publish, copy, bulk mutation | Explain current support and documented provisioning prerequisites, then return `UNSUPPORTED` for execution. |
| `IMPORT_EXPORT` | CSV, Data Loader, FSM export/import, migration, bulk intake | Apply catalog flags and the Data Loader blocker. Do not invent a fallback route. |
| `HELP_SOURCE` | Where is this documented, where can I get more help? | Return the task's help sources and release-freshness caveat. |
| `CROSS_TASK` | A comparison, sequence, dependency, or question spanning two or more tasks | Route to the parent functional-area skill and combine only source-backed task results. |

A request may have multiple classes. For example, "Why does my active Sales
Play return no content?" is `LIFECYCLE`, `TROUBLESHOOT`, and possibly `API` or
`LIVE_READ`; do not discard any supported part.

## Task Selection

| Request subject | Route |
|---|---|
| Sales Motion, objective, or high-value activity | `cx.sales.sales-orchestration.sales-motions` |
| Sales Play, content bundle, content packet, Sales Play artifact, or Sales Play Content Intelligence | `cx.sales.sales-orchestration.sales-plays-and-content` |
| Data Capture Rule or Data Capture Rule attribute | `cx.sales.sales-orchestration.data-capture-rules` |
| Functional-area overview, comparison, sequence, or multiple task subjects | `cx.sales.sales-orchestration` |
| Explicit Sales Orchestration Pre-requisites setup task | `cx.sales.sales-orchestration.pre-requisites` |

Do not infer a task from the word "content" or "data" alone. Ask one short
clarification when more than one task is plausible and the answer would differ.

## Answer Mode Before Execution

Determine the answer mode before authentication or any external call:

1. Use `EXPLAIN` for definitions, metadata, lifecycle, setup, security, API
   contract, troubleshooting guidance, support boundaries, and help sources.
2. Use `READ` only when the user asks to retrieve or validate live environment
   data and the routed project workflow reaches its declared external-read step.
3. Use `CLARIFY` when a missing task, environment, ID, filter, field, sort, or
   acting-user choice would materially change the answer or call.
4. Use `ROUTE` for functional-area or cross-task questions that belong to the
   parent skill.
5. Use `GAP` when the available approved sources do not establish the answer.
6. Use `REFUSE` for an unsupported mutation or an external shortcut that would
   bypass the routed workflow.

Never authenticate, refresh a token, call Fusion, submit an ESS job, or persist
a project artifact merely to answer an `EXPLAIN` question.

## Source Selection

Use sources in this order:

1. The selected task `SKILL.md` for scope, workflow, and routing.
2. The task's `references/` files for security, BOSS, Knowledge Management, and
   Content Intelligence contracts.
3. The task's `ora-resource/` files for validated input, dependency, lookup,
   and error rules.
4. The current target-release Oracle source explicitly linked by the task.
5. New user-provided source material, after validating its task and release.

Do not use chat memory as the sole product source. If the answer is absent,
contradictory, release-specific, or requires a newer contract, return
`SOURCE_GAP`, state what is missing, and identify the exact source or SME review
needed. Do not use browser navigation, direct REST, OAuth, or another external
integration as a discovery shortcut when the active workflow has not selected
it.

## Response Status

Return one primary status:

| Status | Meaning |
|---|---|
| `ANSWERED_FROM_SOURCE` | The approved loaded sources establish the answer. |
| `LIVE_READ_REQUIRED` | The question requests environment data and the required read inputs or workflow step are not yet ready. |
| `CLARIFICATION_REQUIRED` | One material choice is ambiguous. |
| `ROUTED` | Another nested task or the parent skill owns the question. |
| `SOURCE_GAP` | The current sources do not establish the requested fact or behavior. |
| `UNSUPPORTED` | The requested execution crosses the current mutation, import/export, or workflow boundary. |

For a multi-part question, answer the supported parts and give a separate status
for each unresolved or unsupported part. Never broaden, weaken, or silently
drop a constraint to manufacture a complete answer.

## Write and Import Boundary

The Sales Motion, Sales Play and Content, and Data Capture Rule skills remain
read-only. Their documented `$query` POST operations and Sales Play Content
Intelligence POST have read semantics and are not mutations.

Data Loader does not currently support the applicable BOSS REST endpoints.
Create, Update, and Delete support may be added only after Data Loader supports
those endpoints and the repository has reviewed payload, child-object,
translation, identity, concurrency, idempotency, approval, retry, diagnostic,
and recovery contracts.

Until then:

- explain documented Create, Update, and Delete roles and permission groups when
  asked;
- do not generate executable mutation payloads, blueprints, previews, or
  approval requests;
- do not route to direct BOSS REST, a browser, or another loader as a fallback;
  and
- return `UNSUPPORTED` for mutation execution.

## Response Contract

Structure a task answer as follows when applicable:

1. Give the direct answer first.
2. Identify the selected task and question class.
3. Cite or name the loaded task source that supports the answer.
4. State whether the result is guidance, documented API capability, or observed
   live-environment evidence.
5. Include security prerequisites only when the user asks for them or they are
   required to interpret or execute the request.
6. State the operation-support boundary when the request involves writes,
   import/export, activation, publication, or another possible side effect.
7. End with the primary response status and any precise clarification or source
   gap.

Do not dump every endpoint, permission group, or prerequisite into an unrelated
answer. Completeness means answering every material part of the question, not
returning all available task documentation each time.
