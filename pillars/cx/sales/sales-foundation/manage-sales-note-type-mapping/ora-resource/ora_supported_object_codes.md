# Sales Note Type Mapping Supported Objects and Source Codes

Use this catalog to translate the exact business-object choice in **Manage Sales Note Type Mapping** into `SourceObjectCode`. It is a controlled list, not a string-normalization rule.

## Evidence and Scope

Oracle documents the mapping behavior and the `NoteTypeFinder` input field, but does not publish a master list of values for the internal `NoteSourceTypeVA` lookup. The documented Object Metadata resource also exposes a distinct `ObjectCode`; it must not be converted or substituted for `SourceObjectCode`.

The selector list below was captured from the current Manage Sales Note Type Mapping page. Every listed code was then positively verified on 2026-08-12 against the documented read-only `GET /crmRestApi/resources/11.13.18.05/noteTypes` endpoint using `NoteTypeFinder;BindSourceObjectCode=<code>`. A nonempty result proves current effective availability; it does not prove that every returned type has an explicit mapping, because Default Note Types can supply a fallback.

Do not treat this catalog as a cross-release guarantee. Confirm the exact selector choice in the target environment before a mutation and preserve the code exactly. For an FSM import, use the exported `ORA_OBJECT_LOOKUP.csv` parent row when it exists. If it is absent, a catalogued selector entry authorizes a controlled parent row with `ObjectCode` set to the paired `SourceObjectCode`, `ObjectName` set to the exact selector label, blank `ObjectDesc`, `DeletedFlag=N`, blank `ModuleId`, and `LastUpdatedBy` set to the authorized setup owner evidenced by the fresh target export.

## Current Manage Sales Note Type Mapping Selector

| Setup-page business object | SourceObjectCode | Verification basis |
|---|---|---|
| Default note types | `NOTE` | Selector choice and positive runtime lookup |
| Competitor | `COMPETITOR` | Selector choice and positive runtime lookup |
| Contract | `CONTRACT` | Exact source-object code; verify target-environment availability before import |
| Deal | `DEAL` | Selector choice and positive runtime lookup |
| Group | `GROUP` | Selector choice and positive runtime lookup |
| Marketing Budget | `BUDGET` | Selector choice and positive runtime lookup |
| Marketing Claim | `CLAIM` | Selector choice and positive runtime lookup |
| Marketing Fund Request | `FUNDREQUEST` | Selector choice and positive runtime lookup |
| Opportunity | `OPPORTUNITY` | Selector choice and positive runtime lookup |
| Organization | `ORGANIZATION` | Selector choice and positive runtime lookup |
| Partner Profile | `PARTNER_PROFILE` | Selector choice and positive runtime lookup; Oracle partner-notes example returns this code |
| Dummy Object | `DUMMY` | Supplied `ORA_OBJECT_LOOKUP.csv` export |
| Project | `PROJECT` | Supplied `ORA_OBJECT_LOOKUP.csv` export |
| Project Budget Version | `PROJECT_BUDGET_VERSION` | Supplied `ORA_OBJECT_LOOKUP.csv` export |
| Receivables Transaction | `AR_TRANSACTION` | Supplied `ORA_OBJECT_LOOKUP.csv` export |
| Sales Account | `SALES_ACCOUNT` | Selector choice and positive runtime lookup |
| Sales Business Plan | `SALES_BUSINESS_PLAN` | Selector choice and positive runtime lookup; Oracle business-plan-notes example returns this code |
| Sales Objectives | `SALES_OBJECTIVES` | Selector choice and positive runtime lookup |
| Sales Reference Customer | `SALES_REFERENCE_CUSTOMER` | Selector choice and positive runtime lookup |
| Tasks | `TASK` | Selector choice and positive runtime lookup |

## Supplemental Runtime Codes

The following codes returned effective note types in the same validation but were not part of the current selector capture. They can be used only when the target environment exposes the exact object or current export/runtime evidence establishes the intended scope; do not claim that they are selector choices from this task.

| Object context | SourceObjectCode | Evidence |
|---|---|---|
| Contact | `CONTACT` | Current task export/import and positive runtime lookup |
| Customer | `CUSTOMER` | Current task export contains parent label `Lead`; positive runtime lookup |
| Lead | `LEAD` | Positive runtime lookup |
| Sales Party | `SALES_PARTY` | Positive runtime lookup |

## Validation Rules

1. Select the exact UI label first. Use its paired code exactly as listed; do not derive it from an Oracle REST `ObjectCode`, display name, or REST collection name.
2. For a runtime availability check, call `NoteTypeFinder` with the exact `SourceObjectCode`. A match verifies effective availability only. A zero-row result is not proof that the requested explicit mapping is absent, but it is insufficient evidence to construct a new mapping.
3. For a CSV/FSM import, include a matching parent object row in `ORA_OBJECT_LOOKUP.csv`. Reuse the exported parent when available. Otherwise, when this catalog contains the exact selector entry, add its controlled parent row: `ObjectCode=SourceObjectCode`, `ObjectName=selector label`, blank `ObjectDesc`, `DeletedFlag=N`, blank `ModuleId`, and `LastUpdatedBy` set to the authorized setup owner evidenced by the fresh target export. A mapping child without that parent is skipped by Fusion.
4. For a new object not listed here, obtain the exact UI label and code through the target environment's supported setup UI or a positive documented runtime lookup. Add it only with its evidence and release context; never guess from the display label.

## Oracle Public Documentation

| Source | What It Establishes |
|---|---|
| https://docs.oracle.com/en/cloud/saas/sales/oacts/define-notes.html | Mapping is object-specific; objects without a mapping use Default Note Types; Opportunity is a documented example. |
| https://docs.oracle.com/en/cloud/saas/sales/fasqa/how-can-i-add-new-note-types.html | The setup task sequence: select a business object, select a lookup code, and set Default. |
| https://docs.oracle.com/en/cloud/saas/sales/faaps/op-notetypes-get.html | `NoteTypeFinder` accepts `BindSourceObjectCode`; the response calls it the code defined in Object Metadata. |
| https://docs.oracle.com/en/cloud/saas/sales/faaps/api-object-metadata.html | Object Metadata is available read-only, but it is a different resource and schema from note-type mapping source codes. |
| https://docs.oracle.com/en/cloud/saas/sales/faaps/op-businessplans-businessplanid-child-note-noteid-get.html | Oracle's example returns `SALES_BUSINESS_PLAN` for a business-plan note. |
| https://docs.oracle.com/en/cloud/saas/sales/faaps/op-partners-companynumber-child-notes-get.html | Oracle's example returns `PARTNER_PROFILE` for a partner note. |
