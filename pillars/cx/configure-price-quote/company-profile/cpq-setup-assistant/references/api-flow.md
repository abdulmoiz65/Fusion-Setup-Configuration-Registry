# CPQ Setup Assistant Data Loader Flow

Use direct REST only for read-only CPQ deployment, assistant status, discovery,
reconciliation, and LOV retrieval. Do not use a direct REST POST or PATCH for a
CPQ Setup Assistant mutation.

## Read-Only Preparation

1. Verify CPQ deployment without OAuth. A `404` stops the workflow.
2. Read Setup Assistant status once. Only `SETUP_NOT_DONE` can proceed to the
   separately approved initialization.
3. After each accepted or uncertain Data Loader operation, rediscover the
   assistant and its Company Profile and CPQ Users.
4. Treat `Status` and `IsDataExisting` as read-only discovery fields except for
   the final approved `setupAssistants` parent row that transitions `Status` to
   `SUBMITTED`.
5. Before requesting a company-profile selection, retrieve
   `/crmRestApi/resources/latest/setupAssistantsLOV` through the standard
   authenticated read-only Fusion client with `onlyData=true` and `limit=5000`.
   Retain the complete response internally.
   For `EXISTS` and `EXISTS_WITH_BU`, show eligible Legal Entity display values
   upfront before requesting a selection. For all other choices, show display
   values only when the user asks and only for the requested category—Country,
   Corporate Currency, Legal Entity, or Business Unit.

## Data Loader Mutation Route

All three mutation stages must pass through the pillar-local
[CPQ approval guard](cpq-approval-guard.md). Use Core for preapproval preparation,
then record the existing stage approval and execute through the guard; never
hand the generic Core approval directly to its upload command. The guard calls
Core's prepared-artifact upload without adding a second user confirmation.

Use `core.data-loader` for every mutation. Before preparing each source, resolve
the exact registered object and its live metadata. Do not assume REST fields,
keys, parent linkage, `RestAction`, or template layout.

| Sequence | Data Loader object | Scope |
|---:|---|---|
| 1 | `cpqSetupAssistantInitialize` | One-time CPQ initialization after its separate approval. |
| 2 | `setupAssistants` | One immutable pre-submission source containing changed Company Profile values in `CompanyProfiles` and approved administrators in `CPQUsers`. |
| 3 | `setupAssistants` | Final parent row that sets `Status` to `SUBMITTED`, only after prior operations are verified and the approval covers submission. |

For each object, generate or validate a metadata-backed XLSX or DAT source and
preserve its immutable archive through Data Loader validation and approval. Use
the exact operation-specific `RestAction` and parent-child references from the
current metadata. The supplied registration establishes a Company Profile patch
using the discovered Company Profile identity, CPQ-user creation with first
name, last name, and email, and parent patch submission with only `Status`.
Build Company Profile and CPQ-user changes together in one immutable
pre-submission source, then use a separate final parent-submission source. Read
[data-loader-registration-contract.md](data-loader-registration-contract.md)
before building any such source. Do not add `IsDataExisting`, create a Company
Profile, manually supply a new CPQ-user identifier, submit an unrelated status
transition, or combine initialization or final submission with the combined
child source.

For each new `CPQUsers` child row, resolve the full current child template and
include `FirstName`, `LastName`, and `Email`, because they are required for the
registered create action. Treat both Mandatory (`ORA_Y`) and Required for new
records (`ORA_W`) fields as create-required, and do not let a compact DAT sample
omit them. Keep generated identity fields caller-empty under the CPQ-specific
contract even when the generic template marks them required. If separate route
evidence requires a caller-supplied generated identity, stop with a
catalog/metadata mismatch before approval or upload.

For `REST-Framework-Version` and `Content-Type`, treat `SAMPLE_VALUE` in a
generated sample as a non-uploadable placeholder. Use the current registered
business-object metadata/template to determine whether each optional field is
omitted or requires a value. Do not infer a loader-row value from the Data
Loader HTTP client's own request headers; a missing registration rule is a
catalog/metadata blocker.

## Approval, Reconciliation, and Failure

Each stage—initialization, combined company/administrator import, and final
submission—requires one separate approval of its exact preview. First prepare
and validate the immutable artifact through Core and Task Hook with current-stage
approval pending, then build and present the guard manifest. Only then record
approval binding the target environment, redacted change summary, exact source
fingerprint and ordered operation set. Prior-stage completion and reconciliation
remain prerequisites for later-stage readiness; never reuse approval across stages.

If a Data Loader upload or initiation is rejected, fails, or is indeterminate,
stop. Do not retry automatically. Rediscover the assistant, Company Profile,
and CPQ Users through `inspect-child-outcome`; observations do not grant retry
authority. Retain pending markers for partial or uncertain writes. Only a proven
zero-write attempt may use `recover-prewrite`, followed by fresh evidence and
approval. Automated remaining-work resume requires a separately verified
original-job finality/idempotency contract.
After a final submission is accepted or uncertain, perform exactly one
read-only status retrieval; never resubmit automatically.

## Customer Response Boundary

Do not expose loader source contents, template fields, endpoints, request IDs,
IDs, or raw responses in customer-facing messages. State the business action,
its result, and the next safe action. Preserve only sanitized diagnostics under
the project workspace when that workflow is active.
