# Leave Agreements: Redwood Conversation Contract

## Evidence and version boundary

Reviewed on 2026-10-01 against [WFM-82962](https://jira.oraclecorp.com/jira/browse/WFM-82962)
and the supplied Redwood Leave Agreements page. Inspection covered both Add
patterns, Details, Rules and Reasons, Entitlements, the target-plan drawer,
the certification drawer, and current Agreement Edit and entitlement Edit. Unsaved drafts were discarded.

The latest [26D Enhanced Leave Agreements documentation](https://docs.oracle.com/en/cloud/saas/readiness/hcm/26d/amg-26d/26D-absence-mgmt-wn-f50578.htm)
states that templates have one current version and support Edit, without
Update, Correct, or history actions. A displayed Start Date does not establish
a date-effective maintenance capability. The story's conflicting dated lifecycle criteria are not applicable to this
observed UI; Redwood defines functional scope. Use the lifecycle gate in
[the acceptance contract](../../references/absence-additional-lifecycle.md);
do not expose a dated Update or Correction action. The loader's current Edit
uses internal `RangeMode=CORRECTION` with the verified stored Start Date; it
does not accept a caller-selected date.

## Staged intake

1. Identify the requested operation and distinguish a setup template from a
   worker's entitlement agreement. Collect the exact template for maintenance.
2. For create, ask for the pattern: Childbirth or placement agreement, or
   Childbirth or placement conversion. Agreement supports received details;
   Conversion derives from a source absence. Do not infer a pattern from a
   country, name, or shared-parental-leave phrase alone.
3. Complete Details: Name and Legislation are explicitly required. Start Date
   defaults to the current date for create. The supplied 2026-10-05 New Leave
   Agreement Conversion screenshot shows the Status choices Active, Closed,
   Inactive, and Pending, with Pending selected in the unsaved form. Offer all
   four current choices and resolve the selected meaning through the live
   status lookup; Pending is the create candidate only when the requester omits
   Status. Management Type showed read-only User-defined. Offer Legislative Grouping Code and
   Description, then any requested Legislative or Descriptive Information.
   Resolve defaults in the selected environment and disclose them. Active is
   an explicit business choice, not the observed create default.
4. Gather applicable Rules and Reasons: Validation Formula, Denial Reason,
   Withdrawal Reason, Partner Rule, Event Type for Agreement, and Eligibility
   Rule. Formula reveals Eligibility Formula and Enable eligibility override;
   Profile requires the compatible Eligibility Profile. Do not retain both.
5. Gather Entitlements one row at a time. For Conversion, resolve Source Absence
   Type first; the observed UI marks it Required and disables Add until selected.
   Resolve each Source Plan only from that type's returned plan relationship.
   Both patterns require an explicitly selected Target Plan under current task
   rules; each row may have a Payment Percentage Display Formula and Override
   Allowed. Keep each formula and override attached to its own row.
6. Offer optional Certifications one row at a time. Only use active Documentation
   certifications valid for the selected legislation and agreement start date.
7. Show Details, Rules and Reasons, every Entitlement, and every Certification
   together in the final preview. The drawer's Add merely stages a child; it
   does not save the template or authorize the final submission.

## Drawer and lookup parity

| UI surface | Required and dependent behavior |
|---|---|
| Add entitlements, Agreement | Target Plan is Required. Payment Percentage Display Formula is optional. Override Allowed is disabled without that formula. Start Date is read-only and inherited from the parent in the observed draft. |
| Entitlements, Conversion | Source Absence Type is Required before Add. The collection displays Source Plan and Target Plan. The UK lookup returned no matches in the inspected session, so its Conversion drawer could not be reached; do not claim that drawer's full behavior was observed. |
| Add certification | Name is Required. Management, Legislation, and Start Date are read-only inherited/display values in the observed drawer. Add and Cancel affect the staged child only. |
| Collection rows | Preserve per-row identity and parent binding; multiple rows must not share values by list position. Use returned child links and registered loader keys for maintenance. |
| Pattern, legislation, start date, source type, or eligibility changes in a draft | Invalidate affected plans, formulas, grouping, certifications, context segments, and dependent selections. Resolve again in the revised context; explain changes before final confirmation. |
| Any empty or ambiguous lookup | Stop that stage with the missing prerequisite or ambiguous business choice. Never remove legislation/date/plan-type filters or select an item from another country to make the request pass. |
| Formula or profile selection | Resolve exact names and retain effective-period and legislation/LDG applicability evidence. A formula type or globally matching name alone does not prove country applicability; missing applicability evidence blocks preview. |
| Legislative or Descriptive Information | Load only the current registered contexts and active segments. Do not assume the setup template's start date proves that its flex children support dated operations. |

The current [UK create guide](https://docs.oracle.com/en/cloud/saas/human-resources/fabca/create-leave-agreements.html)
describes birth/adopter Conversion and partner Agreement examples, source and
target plans, payment formula, override, and certification selection. Its UK
formula names are examples to resolve, not values to invent or default. UK
conversion needs a compatible maternity/adoption source and linked plan;
country guidance is not authority to broaden an existing resolver's supported
pattern. If an adoption source cannot be verified by that resolver, report the
prerequisite/contract gap rather than silently treating it as maternity.

## View and review

The inspected existing template exposed Edit and Delete Agreement. Its view
organized the same four tabs. The reviewed internal REST attribute table maps
the Description label to `AbsenceAgreementDescription`; its sample PATCH using
`Description` is inconsistent and must not be copied. The declared full reader
refreshes current metadata and follows opaque parent/child response links.

On 2026-10-05, the observed `Delete Agreement` action on a current agreement
opened a confirmation warning that the agreement could not be recovered. It
offered Cancel and Delete, with no effective or end date. A separate requester
supplied Redwood network trace showed a bodyless `DELETE` to one
`absenceLeaveAgreementTemplates/<id>` item returning HTTP 204 for a different
agreement ID. The trace proves the UI's whole-agreement action shape; it does
not identify the selected target or change this task's declared Data Loader
mutation route. The Data Loader representation for this hard-delete intent is
one parent DELETE with date-free internal `effectiveOf=RangeMode=ZAP`.

Return Name, Management Type, Source Absence Type when applicable, Legislation,
Pattern, Status, Start Date, Description, eligibility,
rules/reasons, all entitlement mappings, and all associated certifications.
Retrieve parent detail and every requested child page through declared lookup
contracts. Distinguish not applicable, blank, and unavailable evidence. If the
environment exposes one current version, say so instead of inventing history.

Use draft, validating, unavailable, blocked, pending confirmation, submitted, and completed
states as defined in the lifecycle reference. Keep stored codes, identifiers,
endpoints, and loader column names in technical artifacts. Reviewers: HCM
Absence Management functional owners and the Data Loader technical owner.

## Prompt trials

- "Create a UK partner shared parental leave agreement called Partner leave,
  effective 2026-10-01." Confirm the Agreement pattern and collect the exact
  Target Plan. Disclose Pending, offer applicable rules/reasons and optional
  certifications, and keep the record in draft until the immutable preview.
- "Create a UK birth conversion using Maternity leave and Statutory maternity
  pay as source, and Shared parental pay as target." Resolve the named source
  and plans; empty lookup results are a prerequisite blocker, not permission
  to choose another legislation or pretend a plan exists.
- "Enable Override Allowed without choosing a payment formula." Require the
  formula for that entitlement row and block preview.
- "Correct the entitlement row as of 2026-10-01." Explain that dated Correct is unavailable in this
  single-current-version UI. Offer Edit of the current entitlement or View; do
  not perform Edit on its behalf or report the entire skill as blocked.

## Current template Edit

In the observed Agreement Edit, Start Date, Legislation, Management and Pattern
remain header displays. Name is editable (not read-only), as are Status,
Legislative Grouping Code and Description. The two information sections expose
Context Segment choices. Rules and Reasons expose Validation Formula, Denial
Reason, Withdrawal Reason, Partner Rule and Eligibility Rule. Event Type was
not exposed in this existing Edit, although it was seen on Create; require
fresh UI evidence before treating it as editable. Keep stored header values unchanged and resolve
only dependencies applicable to requested field changes. A Description-only
Edit does not require a new Start Date or new entitlement selection. A normal
request to "update the Description" expresses this current Edit; only explicit
dated Update/slice intent is unavailable.

Entitlements expose Add and per-row Edit/Delete. The observed Edit drawer is titled Update entitlements: Target Plan and
Payment Percentage Display Formula are editable; Override Allowed depends on
the formula; Start Date exposes aria-readonly=true. Its Update button stages a
current-row change, not date-effective Update. Review each current row's
identity and allowed fields through its drawer; current row deletion is distinct
from obsolete dated-row deletion. Stage child changes with the parent and
review one complete before/after preview. These observations establish UI
behavior, not a successful Data Loader save.

- "Edit the Description of Partner leave to Shared parental leave received."
  Resolve the exact current template and full before state; stage Description
  only, with no new operation date. Validate the current native Edit contract.
- "Show the history of Partner leave." Explain that this UI has one current
  version and no History action; offer the current configuration View.
