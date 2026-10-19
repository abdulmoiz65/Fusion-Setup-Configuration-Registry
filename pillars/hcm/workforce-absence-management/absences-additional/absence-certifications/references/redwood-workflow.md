# Absence Certifications: Redwood Conversation Contract

## Evidence and scope

Reviewed again on 2026-10-06 against [WFM-82961](https://jira.oraclecorp.com/jira/browse/WFM-82961)
and the live Redwood Absence Certifications page in HCM_FSCR_BRONZE_2701B.
Inspection covered both
Add classifications, Details, Rules, conditional controls, and unsaved-form
validation. No configuration was saved. Observed choices are evidence of that
session, not a reusable tenant-wide lookup cache.

Functional priority is the current target Redwood page, then the story's ACs.
Documentation and adapter metadata explain supported behavior and transport;
they cannot introduce additional operations, fields, classifications, or choices.

Use this skill for certification **setup definitions**. Worker evidence,
certificate completion, attachments, and payment actions belong to worker
absence administration; do not substitute the public worker
`absenceEntryCertifications` resource for the setup business object.

The observed target UI determines functional scope when a Jira criterion
conflicts with it. See the shared lifecycle source-priority table.

## Staged intake

1. Identify view/create/update/correct/end-date/delete intent. For maintenance,
   identify the exact existing certification and selected effective row first.
2. For create, collect Name, Classification (Documentation or Entitlement),
   Legislation, and Effective Start Date. Disclose the create-only current-date
   default and Active status candidate; retain supplied values. Management is
   displayed as User-defined and is not a user-selected field in the observed UI.
3. Complete Details: Absence Record Update Rule, Description, and requested
   Legislative or Descriptive Information. The observed update-rule choices
   were None, Update authorization status, and Update late notice waiver status.
   The UI blocks moving to Rules when required Details are missing.
   Status offers only Active and Inactive. Do not reuse Leave Agreement's
   Pending/Closed choices. Create has no Effective End Date control.
4. Resolve and collect an explicit Trigger before dependent Rules. Present
   business meanings from the live classification-specific lookup. Documentation
   showed On demand and On absence submit. Entitlement also showed Managed by
   entitlement formula. Never silently select a Trigger.
5. Gather applicable Creation, Passage of Due Date, Confirmation, Expiration,
   and Void choices using the matrix below. Ask only for missing applicable
   values; preserve values already supplied in the prompt or project context.
6. Validate the whole configuration, then prepare the existing Data Loader
   preview. Present Details and changed Rules together, including defaults,
   cleared values, target environment, operation, and effective context.
   A draft or valid local source is not a saved certification.

## Conditional rules

| Selection | Conversation and validation |
|---|---|
| On absence submit | Offer the observed Eligibility Profile control; resolve a supplied profile through its existing resolver. Do not require an omitted optional profile. |
| Managed by entitlement formula | Offer Allow creation on demand and Mark as confirmed when created on demand. In this branch the observed UI omitted Passage of Due Date and Expiration and the Creation reevaluation control. Do not populate hidden rules from the generic default profile. |
| Calculate date for Due Date or Expiration | Collect Reference Date, Duration, and Duration UOM as one group; resolve the corresponding date and UOM lookups separately for due date and expiration. Reject incomplete calculation intent before preview. |
| Capture date | Preserve the capture-date rule; do not invent calculated Reference Date, Duration, or Duration UOM. |
| Not applicable for a date rule | Omit calculation values; a supplied conflicting calculation must be clarified rather than silently discarded. |
| Entry required for Confirmation or Void Reason Rule | Require at least one reason from the corresponding lookup. These are separate lists; validate every selection and reject duplicates. The UI marks Reasons Required. |
| Entitlement classification | Offer applicable Absence Record Update and Entitlement Reevaluation Rule controls. Observed reevaluation choices were Not applicable, As of absence start date, and As of action date. |
| Absence Record Update at an event | Offer only when that event control is visible. Choices are None, Set value to true, and Set value to false. Selecting Update authorization status in Details exposed Confirmation and applicable Due Date event controls that were absent with None. A registered event field alone does not establish visibility. |
| Reevaluation applies | Collect Entitlement Update Rule. Observed choices were None, Override, Recalculate, and Retract. Override reveals Revised Payment Percentage; require the value and validate against current registered constraints. Do not guess numeric limits from the label. |
| Classification, Trigger, or rule changes in a draft | Invalidate affected lookup evidence and dependent values; explain incompatible supplied values and obtain the revised choice. Never carry stale hidden values into preparation. |
| Legislative or Descriptive Information requested | Refresh the exact registered flexfield context, segments, and constraints. Global segments may exist without a context. Do not copy the inspected pod's custom segment names or default a context from legislation. |

For entitlement event behavior, see current Oracle
[certification event actions](https://docs.oracle.com/en/cloud/saas/human-resources/faiam/options-to-manage-actions-for-certification-events.html).
The [FMLA example](https://docs.oracle.com/en/cloud/saas/human-resources/faufm/configure-fmla-absence-certification.html)
illustrates Calculate date with an absence-start reference, duration, and UOM;
its values are examples, not defaults for every certification.

## Maintenance and view

Read [the lifecycle and acceptance contract](../../references/absence-additional-lifecycle.md)
before any maintenance request. A view must include Name, Classification,
Legislation, Status, Effective Start Date, Effective End Date, and Description,
plus the requested rule details. Distinguish blank Description from a field not
retrieved. Never report a six-column identity lookup as the full detail view.

For **Update**, WFM-82961 forbids changing Name, Classification, Legislation,
Trigger, and the stored Effective Start Date. An operation date selects the new
context; it does not authorize changing the stored start-date attribute.
Use the resolved identifier and mutable changes only in the loader record.
The portable source validator rejects nonblank immutable fields for Update,
including unchanged values copied from a create template. Blank physical
columns in registered METADATA remain allowed. Correction is a distinct intent
and still needs exact-row, supported-field, impact, and approval checks.

### Observed maintenance restrictions

Both Update and Correct displayed Name, stored dates, Classification,
Legislation and Management without editable controls. Absence Record Update
Rule was disabled. Correct does not unlock identity or creation rules.
The reviewed Documentation On demand and Entitlement On absence submit
records with Absence Record Update Rule None exposed Status, Description,
current flexfields, Confirmation Reason Rule/Reasons, and Void Reason Rule/Reasons.
The On absence submit record also exposed Eligibility Profile. Creation Trigger,
checkboxes, due-date/expiration configuration and payment reevaluation were
absent from these maintenance forms. Resolve configuration-specific event
visibility from the current form; do not generalize a None-rule form to other
saved rules or permit a hidden control from template presence.

Update has a blank required operation date. Correct displays the selected
row's stored Start Date: derive correction context from that selected row;
do not ask for a new correction date or accept a replacement Start Date.
End Date is a separate dialog showing today's date as its candidate; preserve
a supplied date, disclose an omitted-date candidate and confirm the exact
chosen date in the existing core preview. It has no configuration-edit fields.
Delete Certification warns that **all date-effective records** will be deleted;
use one whole-certification operation, without synthetic child deletions.

History is displayed on the view page with effective date, Last Updated Date,
and Last Updated By. Its successful target read was captured and is declared
as `read_absence_certification_history` in ora_reference_lookups.md. Bind it to
the exact certification, validate the current service/finder and read all pages;
do not present extra backend change-detail fields absent from this panel.
The 2026-10-06 single-row review did not expose Delete Record. The fresh
2026-10-07 two-row User-defined Entitlement review exposed enabled **Delete
Record** for the selected July 1 row. Its confirmation states that the previous
record receives the deleted record's end date. No UI mutation was submitted.
AC4 therefore has a current UI action. Prepare one identity-only parent DELETE
with `RangeMode=DELETE_CHANGES;RangeStartDate=<selected stored Start Date>`.
The [Oracle Delete Changes protocol](https://docs.oracle.com/en/cloud/saas/human-resources/farws/Date_Effective_Delete_Changes.html)
defaults to the physical row end, matching the dialog semantics. This mapping
combines current item DELETE support, native loader controls, temporal History,
and empirically verified Create/Update date controls. It is an inference from
those sources, not a captured Redwood mutation request; live loader acceptance
remains a QA result. Runtime validation uses the exact selected configuration and
complete contiguous History with an earlier row to preserve. No browser read
or current enabled-action flag is required. Do not infer first-row or whole-object deletion.

Portable `uiContext.deleteRecordEvidence` is generated by the packaged
`resolve_certification_delete_record.py` from declared configuration and History
reads only. It binds the selected native ID/stored range, full before state,
resolved User-defined Management, complete History and current run/environment/
principal, with SHA-256 integrity checks and adapterContract
`DELETE_CHANGES_PHYSICAL_ROW`. The legacy `uiContext` container name does not
select a UI execution route. It does not authorize execution.

The inspected Pre-defined Entitlement record exposed only a disabled Update
button; Correct, End Date and Delete Certification were absent. Preserve this
protection using the full before state and resolved Management display meaning.
Viewing a predefined record does not authorize maintenance or bypassing disabled
UI controls through a backend capability. Refresh role/target-specific action
evidence rather than assuming a different user's privileges from this capture.

### Portable preparation evidence

For `absenceCertifications`, the existing preparation helper accepts a
technical `uiContext` alongside each resolved source record. It is populated
from the owning task's current read/LOV and UI evidence, never requested as
raw codes from the user. `meanings` maps each relevant attribute to its
resolved `{code, meaning}` pair. Conditional maintenance uses `beforeState`
bound to the exact Absence Certification ID, retaining relevant saved parent
fields as serialized string values and preserving unchanged rules
outside the mutation row. `visibleFields` records mapped event controls or
current active flexfield context/segments; it cannot add unknown root fields.
Registered native key fields remain technical linkage, not extra user fields.

The helper retains this context with a fingerprint and checks it again when
verifying the exact final DAT/ZIP. It rejects backend-only populated fields,
hidden defaults, stale meaning/code pairs, incomplete calculated dates,
required or duplicate reasons, and incomplete payment overrides. Blank native
template columns are allowed. The owning task still verifies evidence
provenance, all LOV selections, metadata constraints, access and operation
capability before core preview; local context is not live approval.

## Prompt trials

The inspected User-defined Documentation record exposed Delete Certification,
End Date, Correct, Update, and History. Entering Update opened an unsaved form
with an empty required Effective Start Date, and progression to Rules was
blocked until that operation date was supplied. Name was displayed as a
read-only textbox; the observed Absence Record Update Rule was disabled. This
date is the requested update's context, not permission to overwrite the stored
start date. The draft was discarded without submission. These observations
establish visible UI actions, not the Data Loader mapping or protection checks.

- "Create a UK documentation certification called Supporting evidence,
  effective 2026-10-01, when the employee submits an absence." Resolve the
  available Trigger, propose On absence submit for confirmation, and retain
  a draft until that choice and the final preview are confirmed.
- "Create an entitlement certificate on demand; calculate the due date 14
  calendar days after absence start; require a confirmation reason." Ask for
  Name, Legislation, and the exact confirmation reasons; preserve the supplied
  Trigger and date calculation. Do not ask for raw lookup codes.
- "Update the classification and name of Supporting evidence." Identify the
  target, reject these Update changes, explain the immutable fields, and do
  not automatically convert the request to a correction or replacement.
- "End-date Supporting evidence." Require the explicit end date and exact
  target. Do not borrow the search date or submit a guessed operation.
