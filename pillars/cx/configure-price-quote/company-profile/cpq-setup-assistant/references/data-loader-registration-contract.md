# CPQ Setup Assistant Data Loader Registration Contract

Use this reference when building a CPQ Setup Assistant Data Loader source. It
captures the supported initialization and `setupAssistants` hierarchy contracts.
Revalidate it against the current registered metadata before each immutable
archive; a changed or incomplete live registration blocks the load.

## Initialization

- Resolve the exact `cpqSetupAssistantInitialize` business object through Core
  Data Loader, without aliases. It is a separate initialization action, not a
  parent `setupAssistants` create or a Company Profile create.
- Use one initialization row with `RestAction=POST`. Supply every value required
  by the current complete attribute metadata. Do not infer defaults or derive
  the action's payload from a generic parent-create example.
- `InitializationRequestId`, `Content-Type`, and `REST-Framework-Version` are
  conditional on the live registration: include them only when registered and
  needed. Their absence or optional designation is not itself an unsupported
  initialization action. The existing guard supports the action content type
  `application/vnd.oracle.adf.action+json` and framework version `9` when those
  transport values are supplied. It permits a `RestAction`-only row when the
  complete live metadata requires no other values.
- Use the current Core registration/template and prepared-archive validation
  as evidence, with the guard's live metadata recheck. A compact sample DAT or
  this reference alone does not prove live compatibility. If action routing or
  payload mapping needs confirmation, use only evidence exposed by the selected
  Core workflow; do not guess an endpoint or add a direct REST fallback.
- Distinguish a confirmed missing/incompatible action from unavailable evidence.
  A field omitted from Core's schema projection does not prove the underlying
  registration lacks it. If the selected workflow cannot establish compatibility,
  stop with the specific missing evidence and next action to confirm or correct
  the registration. Do not weaken validation to make the preview pass.

## Parent: Setup Assistants

- The parent is an ADF REST object whose patch route targets the one CPQ Setup
  Assistant record.
- Its patch payload excludes `Id`, `Name`, and `Data`. For final submission,
  send only the approved `Status` transition to `SUBMITTED`.
- Do not use the parent create route for company or administrator changes.

## Child: Company Profiles

- The child has a patch route parameterized by the discovered
  `CompanyProfileId`; use that current discovery value to bind the update.
- `IsDataExisting` is excluded from the payload and is discovery-only.
- There is no registered create route. Do not create a Company Profile through
  this object.
- For an existing company, include only the approved, branch-applicable
  business fields. Retain any identifier fields only when the current metadata
  requires them to resolve the registered patch route; they are not business
  configuration values.

## Child: CPQ Users

- The child create route is registered under the CPQ Setup Assistant parent.
- A new administrator requires `FirstName`, `LastName`, and `Email`.
- Treat both **Mandatory** (`ORA_Y`) and **Required for new records** (`ORA_W`)
  designations as required for the registered create action. A compact
  generated DAT sample is not authoritative evidence that a required create
  attribute is absent.
- Do not supply `CPQUserId`, `Id`, `PartyNumber`, or `UserName` for a new
  administrator. The CPQ-specific create contract treats those identity fields as
  server-generated even when the generic template marks them Mandatory or
  Required for new records. If separate route evidence establishes that one
  must be caller-supplied, stop with a catalog/metadata mismatch rather than
  inventing an identifier or weakening the `FirstName`, `LastName`, and `Email`
  create contract.
- Use the registered child patch route only for a separately approved change to
  an already discovered CPQ user. This skill does not modify existing users.

## Source and Approval Rules

Enforce these bindings with the [CPQ approval guard](cpq-approval-guard.md),
which derives the ordered operations from the prepared ZIP, records one
stage-specific approval, and delegates the approved artifact to Core Data
Loader. A generic task-code/route approval alone is insufficient for this skill.

Build one immutable pre-submission source containing the Company Profile update
and every approved CPQ administrator row, then a separate immutable final
parent-submission source. The combined child source uses the registered Company
Profile patch contract and CPQ-user create contract under the same parent. The
final parent source uses the registered patch contract. Revalidate both Company
Profile and CPQ-user state after an accepted or uncertain combined child import
before final submission.

The parent-link value and child identifier are routing evidence only. Do not
show them to the customer or persist them in a project artifact. The exact
source fingerprint, ordered operations, target environment, and redacted
change-summary approval must bind the combined child import and final submission
as one ordered sequence.
