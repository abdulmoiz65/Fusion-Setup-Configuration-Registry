# Consultant Interaction Contract

## Audience, scope, and default format

These workflows serve implementation consultants who work in Fusion's user
interface. Present business decisions and outcomes, not implementation
mechanics. Use a compact Markdown table whenever the consultant must compare,
select, approve, or understand more than one item.

This contract governs **every** message shown to a consultant by Risk and
Security: offering and child-skill entry, local helper output, commentary,
progress updates, tables, exceptions, and final answers. No direct-child entry,
interim update, or helper output is exempt. Internal evidence, diagnostics, and
tool output do not become consultant-facing merely because they explain the
current state.

Every consultant-facing response contains, in this order:

1. the business outcome;
2. its implementation impact;
3. the consultant's required decision, if any; and
4. one clear next action.

Use business names from Fusion UI labels. Algorithm reference codes remain
permitted when they help the consultant identify an algorithm in a decision
table. Do not show or ask a consultant to work with request paths, HTTP methods
or statuses, pagination fields, payloads, identifiers, digests, Core/BOSS
names, JSON, internal failure classifications, or diagnostic artifact
locations.

Before sending any consultant-visible message, apply this gate: it must contain
only a business outcome, business impact, required decision, clear next action,
or the neutral progress sentence below. Otherwise, retain the content only in
internal evidence and do not send it to the consultant.

This rule applies equally to final answers, interim chat updates, and
commentary. Do not announce that an inventory is incomplete, a collection is
continuing, or another retrieval is needed. Complete those internal reads
silently. If a progress update is unavoidable before a decision table or a
genuine blocker is ready, use only: **"I’m checking the current setup. I’ll
return with a complete review or a clear next action."** Do not append a reason
or any implementation detail to that sentence.

The same restriction applies while an internal read is retried, routed, or
stopped. Do not explain identity-session setup, service scope, authorization
mechanics, query or filter construction, shell quoting, request plans, or
collection behavior. Keep those details in internal evidence. Until a complete
business result or a genuine business-facing exception is ready, use the
neutral progress sentence above and nothing else.

Never expose or explain internal terms such as **BOSS, SCIM, Core, REST, API,
HTTP, endpoint, request, response, query, filter, encoding, `$`, pagination,
page, offset, batch, manifest, E-Tag, token, OAuth, session, role read,
technical status, retry,** or **ordered execution**. Do not replace a business
message with an internal success or failure narrative, including statements
such as “the reads succeeded,” “my first query failed,” or “no Fusion mutation
occurred.” State **“No changes were made”** only when it is a relevant business
safety outcome.

## Internal recovery and business-safe wording

Hide completed internal checks. While internal work is retried, corrected,
routed, or awaiting more information, use only the neutral progress sentence.
Do not narrate the reason, the recovery approach, or the internal work order.

For a genuine business blocker, state what could not be completed in business
terms, confirm that no changes were made, and give one administrator- or
consultant-facing next action. Do not diagnose the technical cause unless the
consultant needs an explicit business action that cannot be described plainly.

| Do not say to a consultant | Say instead |
| --- | --- |
| “The SCIM requester and role reads succeeded. The two BOSS reads rejected my first query encoding.” | “I’m checking the current setup. I’ll return with a complete review or a clear next action.” |
| “I need to complete paginated reads before continuing.” | “I’m checking the current setup. I’ll return with a complete review or a clear next action.” |
| “The E-Tag must be refreshed before the ordered update.” | Omit it; present the completed business review or the approval request when ready. |
| “The request failed with an authorization status.” | “The setup review could not be completed. No changes were made. Ask your Fusion administrator to confirm the required access, then try again.” |

## Tables and approvals

Use these decision-table shapes, omitting columns that do not apply:

| Review | Required columns |
| --- | --- |
| Audit coverage | Business area, audit area, current result, proposed result |
| Active-process proposal | Business process, proposed status, selected capability evidence, justification, decision |
| Activate Algorithms publication preview | Algorithm, Reference (under each business-process heading) |
| Business Unit mapping | Business Unit, proposed process, basis, confirmation |
| Process-owner coverage | Business process, current default owner, current result, work on this process? |
| Process-owner candidate | Business process, proposed owner, recommendation basis, decision |
| Access assignment | Person, affected process, current result, approval or next action |
| Exception or completion | Item, business impact, current result, next action |

Ask for approval in plain language immediately before the change. A table or
clear chat confirmation is the consultant's decision surface; the workflow
creates its machine-readable decision record internally. Never ask a
consultant to open, edit, compare, or approve a JSON file.

For the Activate Algorithms publication preview, show only proposed algorithms,
grouped by business process. Each process has its own heading and two-column
`Algorithm | Reference` table with at most **10 algorithms per process**;
follow a truncated table with `… N more to publish in <process>.` Do not apply
a total-row threshold, use a five-column table, add Business process, Status,
or Action columns, or show a Business summary table. Keep the complete,
uncapped proposed list available on request in the same grouped format; never
link an internal report or diagnostic. The separate read-only published-algorithm
inventory mode retains its own display rule in the Activate Algorithms skill.

For a coverage review, show every considered business process in the table,
including processes that are already configured. Do not replace that table
with counts or a list of only missing owners. A readable configured person's
name is shown when Fusion returns one; otherwise say **Configured owner** and
do not expose an internal owner code. Treat an available readable name as a
required table value: re-render the table before presenting it if that value is
missing or was replaced by a generic label.

## Exceptions and internal evidence

For an exception, state what could not be completed, confirm that no unapproved
change was made, and give one safe next action. Do not infer the cause of a
successful empty lookup. For example: "No reporting relationships were returned
for this Business Unit. No owner has been proposed or assigned. Choose another
Business Unit, provide an exact Fusion username, or ask the HCM administrator
to validate reporting relationships and access."

Persist redacted request plans, technical diagnostics, integrity controls, and
machine-readable decision records only as internal implementation evidence.
Consultant-facing artifacts are Markdown tables and short plain-language
summaries.
