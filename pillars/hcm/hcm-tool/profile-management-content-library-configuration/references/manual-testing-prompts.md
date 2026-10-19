# Content Library manual testing prompts

These are fully filled **synthetic configuration examples**, not executed test
evidence, import archives, or approval records. They use business language plus
explicit field mappings; they do not ask the skill to invent business values or
discover business purpose. Optional values deliberately omitted below must stay
omitted. Technical provider columns, generated IDs, evidence hashes, target
identity and approval fingerprints must come from the actual workflow, not from
made-up example values.

Use the current repository checkout and Python 3.11. Authenticate privately on
the testing machine. Do not copy a token cache, credential properties, customer
exports or ignored project history through Git. Create/select a local test
project through the router; the original development project is not included in
a clone. These examples use no fixed tenant, host or project path.

## Start a manual-test session

Paste this once, then run one numbered example at a time:

```text
Use router/implementation-router/SKILL.md in this repository. Select or initialize
a durable local project for synthetic Content Library manual validation. Do not
edit implementation files. Use the target I configure privately on this machine;
resolve its authenticated identity and actual task privileges through the
selected workflow. Check profile mode and actual provider/schema compatibility where the
selected operation needs them; do not gate FSM exports on a quarterly label or
a Content Items REST probe. Never infer a quarterly label from a technical version.

Treat my following values as supplied configuration, not a request for workforce
design or downstream setup. Preserve each complete request and its provenance.
Show missing evidence or uncertain mappings without inventing values. Use exact
provider identifiers and applicable case rules; display every matched identifier
and stop creation on duplicates. Do not offer fuzzy matches, updates or reuse.

Start with review only. Before any export, show the exact target, task and export
payload and obtain its required approval. Before any full export, establish that
all contents are permitted synthetic or approved seed data. Do not substitute a
filtered export or move customer-bearing data elsewhere to bypass that gate.
Use the supported package workflow and Core Data Loader's actual immutable
preview/approval contract. Do not submit until its applicable approval passes.
Never use a unit-test ZIP as a live payload. Do not retry a create automatically
or delete test records as cleanup. Keep local, source-only and live results separate.
```

The `0911` suffix and date `2026-09-11` are intentional supplied sample values,
not instructions to default to today's date. If these keys already exist, record
the duplicate result. Choose a new explicitly supplied identity for a separate
test; never silently rename, increment a code, or replay a possibly submitted load.

## Template and export checks

The local requirements XLSX is not an FSM CSV template. First try:

```text
Give me the blank Profile Management Content Library requirements XLSX, with all
14 governed groups and repeating rows supported across worksheets. Keep it blank;
do not include these examples as default data and do not connect to Fusion.
```

For real FSM template-only checks, each request below is separate. Each must
still reach the declared export workflow and its exact-payload approval gate.

| Task | Copy-ready template-only request |
| --- | --- |
| Educational Establishments | Prepare a template-only FSM export request for Educational Establishments, HRT_MANAGE_EDUCATIONAL_ESTABLISHMENTS, on my authenticated test target. Show the exact export payload for approval; do not export business rows or import anything. After an approved successful export, validate the ZIP, metadata and HRT_SCHOOL.csv header. |
| Content Types | Prepare a template-only FSM export request for Content Types, HRT_MANAGE_PROFILE_CONTENT_TYPES, on my authenticated test target. Show the exact export payload for approval; do not export business rows or import anything. After approval and success, validate metadata and the HRT_CONTENT_TYPES_B.csv, ORA_HRT_CONTENT_PROPERTY.csv and ORA_HRT_CONTENT_TYPE_RLAT.csv headers. |
| Item Catalog | Prepare a template-only FSM export request for Item Catalog, ORA_MANAGE_PROFILE_ITEM_CATALOG, on my authenticated test target. Show the exact payload for approval. After approval and success, validate metadata and ORA_TALENT_PROFILE_ITEM_CATALOG.csv, ORA_TALENT_CATALOG_CONTENT_ITEM.csv and ORA_TALENT_CATALOG_CONTENT_ITEM_RDESC.csv headers. No business export or import. |
| Content Items, including GOAL | Prepare a template-only FSM export request for Content Items, HRT_MANAGE_PROFILE_CONTENT_ITEMS, on my authenticated test target. Show the exact payload for approval through the task export workflow. Inspect all returned members and observed provider coverage after approval and success. Do not require create-provider or profile-mode proof just to acquire the template, or interpret template/export success as enhanced GOAL FSM import support. |
| Nine catalog-backed contexts | Use the Item Catalog template request above. These share one task/provider; do not invent nine standalone enhanced Content Items import providers. |
| Instance Qualifiers | Explain the standalone Instance Qualifiers no-column limitation and show the local requirements input fields only. Do not request a standalone FSM template/export/import. Identify the Profile Types owner for any separately approved containing evidence. |

For a supported numbered import case, request current-state evidence separately:

```text
For the single case under review, prepare the workflow-approved complete,
unfiltered current-state export request for its actual owning task. First pass
the data-handling gate and show the exact target/task/payload for approval. Keep
the template baseline separate from duplicate evidence. After success, validate
all ZIP members and completeness, perform the provider's exact Name/code and
dependency checks, and show the resulting proposal. Do not package or submit yet.
```

Content Types and legacy Content Items require the integrity-validated seed
overlay in addition to fresh current evidence. Item Catalog requires a populated
full same-target export and exact owning Content Type evidence; do not invent a
generic Item Catalog seed-overlay requirement. A metadata-only export proves
neither absence nor a usable current-state baseline.

## 1. Educational Establishments

Expected route: Educational Establishments, create-only FSM. This is an
institution reference, not an employee's education record.

No quarterly-release label, seed overlay, Profile V2 proof or Talent Catalog
REST capability receipt is required for this task. Its own authenticated FSM
export and exact package validation are required. If release metadata is absent,
retain unknown rather than inventing 26C; report actual provider/schema conflicts.

```text
I want to add one synthetic educational establishment. Review these exact values:
SchoolCode = G8154_SCHOOL_0911
Name = FSCR Synthetic Technical Institute
Description = Synthetic institution reference for manual configuration validation.
Location = Example City

Country and state geography are intentionally omitted. Do not derive them from
Location. No PartyId or generated identifiers are supplied. Do not create a
degree, profile section or employee record. Show the complete review and exact
SchoolCode result before any package or import.
```

Verify all four supplied fields on independent readback. Description is required
by the current provider contract; Location/geography are not mandatory defaults.

## 2. Content Types

Expected route: Content Types, basic create-only FSM. This example intentionally
does not claim populated-property or relationship acceptance.

```text
I want one new synthetic controlled Content Type. Review these exact mappings:
ContextName = G8154_MANUAL_TYPE_0911
ContentTypeName = FSCR Synthetic Manual Type
ContentDescription = Synthetic controlled type for manual configuration validation.
FreeFormFlag = N

This request contains only the type definition. Properties, type relationships
and content items are empty; do not invent them. Do not configure a Profile Type
or Content Section. Check this exact ContextName against complete fresh target
evidence and the integrity-validated seed catalog. Show the proposal and blockers;
do not package or import yet.
```

Verify the type identity, description and free-form flag, with no unintended
properties or relationships. Do not treat this as a populated-graph test.

## 3. Item Catalog

Expected route: catalog-only create through Item Catalog FSM. The owning
COMPETENCY Content Type must already be evidenced; do not create it implicitly.

```text
I want one synthetic competency Item Catalog, with no child items:
ContextName = COMPETENCY
ContentValueSetCode = G8154_CMP_CAT_0911
ValueSetName = FSCR Synthetic Competencies
ValueSetDescription = Synthetic competency catalog for manual validation.

Review this as a catalog-only create. Both child member sets are empty, including
rating descriptions. Check the exact owning type and current catalog code/name
collisions. Do not supply ModuleId, SeedDataSource or generated IDs. Do not create
a competency, Rating Model, behavior relationship or Profile Section in this
request. Show the complete proposal before package or import.
```

After an approved successful import, independently verify this catalog before
using it as the existing parent in case 8. A failed/missing readback does not
establish that prerequisite.

## 4. Content Items — legacy-profile example

Expected route: standalone Content Items FSM **only if the target is verified
legacy mode**. This is not the enhanced catalog-backed competency example.

```text
On a verified legacy-profile test target, I want one synthetic competency item:
ContextName = COMPETENCY
ContentItemCode = G8154_LEGACY_CMP_0911
Name = FSCR Synthetic Legacy Analysis
DateFrom = 2026-09-11
ContentSupplierCode = ORA_ADMIN
RatingModelCode = PROFICIENCY

The supplier and Rating Model codes are explicitly supplied references to check,
not claims that they exist. If either does not resolve exactly, stop; do not
create or substitute a dependency. DateTo, description, translations, dynamic
fields, item-specific proficiency descriptions and relationships are omitted.
Check the exact Name identity and separate code collision in fresh and seeded
evidence. Review only. If this target is enhanced, report the mode mismatch and
do not silently change this request into a catalog-backed or HDL load.
```

This sample cannot run on an enhanced-only target. A blocked mode/dependency
check is an honest result, not permission to weaken the request.

## 5. GOAL — strict FSM check and optional separate fallback

First test the strict FSM boundary:

```text
I want one synthetic reusable GOAL Content Item, not an assigned employee goal:
ContextName = GOAL
ContentItemCode = G8154_GOAL_FSM_0911
Name = FSCR Synthetic Process Improvement Goal
DateFrom = 2026-09-11

Use FSM only for this request. No description, end date, translations, Rating
Model, dynamic fields or relationships are supplied. Review the exact values and
the current provider eligibility. Do not use HDL or attempt an unsupported load.
```

Expected on the enhanced provider: preserve the GOAL companion-document FSM
import blocker. Export success does not remove it.

Only if you independently choose the registered fallback, use this distinct
request. Do not make the `not submitted` statement if it is not true:

```text
I explicitly select the verified GOAL HDL exception for one new synthetic item:
ContextName = GOAL
ContentItemCode = G8154_GOAL_HDL_0911
Name = FSCR Synthetic Goal Fallback
DateFrom = 2026-09-11

No load has been submitted for this specific request. Keep it separate from my
strict-FSM case. Verify enhanced mode, the verified
CONTENT_ITEM_V2_HDL provider and complete fresh Content Items FSM plus seed
evidence. Check literal ContextName+Name and ContextName+ContentItemCode locks.
Review these four fields only. Prepare the isolated local package only after its
required approvals; do not submit until Core Data Loader's actual gate passes.
No generic fallback, HSDL, updates, translations or additional rows are selected.
```

After an authorized fallback load, request terminal status and complete
independent FSM readback of all four fields. Label the result **HDL fallback
evidence**, never FSM-import acceptance.

## Existing-parent prerequisite for cases 6–14

Each following case is a separate one-item request against one exact **existing**
catalog. The named synthetic parents below are example prerequisites, not claims
that any target contains them. Resolve them first; if absent, stop that child
case. A tester may separately request an approved catalog-only creation and
verify it before starting a new child request. Never combine a new parent and
children, or split an existing complete-set request, to bypass the narrow route.

| Case | ContextName | ContentValueSetCode | ValueSetName | ValueSetDescription for a separately requested catalog-only setup |
| --- | --- | --- | --- | --- |
| 6 | BEHAVIOR | G8154_BEH_CAT_0911 | FSCR Synthetic Behaviors | Synthetic behavior catalog for manual validation. |
| 7 | CERTIFICATION | G8154_CERT_CAT_0911 | FSCR Synthetic Certifications | Synthetic certification catalog for manual validation. |
| 8 | COMPETENCY | G8154_CMP_CAT_0911 | FSCR Synthetic Competencies | Synthetic competency catalog for manual validation. |
| 9 | DEGREE | G8154_DEG_CAT_0911 | FSCR Synthetic Degrees | Synthetic degree catalog for manual validation. |
| 10 | EDUCATION_LEVEL | G8154_EDL_CAT_0911 | FSCR Synthetic Education Levels | Synthetic education level catalog for manual validation. |
| 11 | HONOR | G8154_HON_CAT_0911 | FSCR Synthetic Honors | Synthetic honor catalog for manual validation. |
| 12 | LANGUAGE | G8154_LNG_CAT_0911 | FSCR Synthetic Languages | Synthetic language catalog for manual validation. |
| 13 | MEMBERSHIP | G8154_MEM_CAT_0911 | FSCR Synthetic Memberships | Synthetic membership catalog for manual validation. |
| 14 | PROJECT | G8154_PRJ_CAT_0911 | FSCR Synthetic Projects | Synthetic project catalog for manual validation. |

For separate parent setup, paste exactly one row with this instruction:

```text
This is a new independent catalog-only setup request for the one complete row I
am supplying. Review its ContextName, ContentValueSetCode, ValueSetName and
ValueSetDescription exactly as written. Both child members are empty. Do not
include any later child-item request. Check existing dependencies and duplicate
keys/names, and use the declared catalog-only FSM workflow and approval gates.
```

All nine child examples require `ContentSupplierCode=C`, no Rating Model,
translations, rating-description rows, item relationships or advanced/dynamic
fields. Blank generated/provider-only fields are not missing business inputs.
Use the actual export-derived unchanged parent anchor, including its portable
values; never reconstruct it from this table or overwrite a different description.
The provider must have lifecycle `verified` for general use.
Keep one unchanged parent plus one new child and the rating-description member
empty. These are not standalone enhanced Content Items FSM imports.

## 6. BEHAVIOR

```text
I want one synthetic behavior in an existing behavior catalog:
ContextName = BEHAVIOR
ContentValueSetCode = G8154_BEH_CAT_0911
Existing catalog name = FSCR Synthetic Behaviors
ContentItemCode = G8154_BEH_ITEM_0911
Name = FSCR Synthetic Shares Clear Updates
DateFrom = 2026-09-11
ContentSupplierCode = C

Review one create-only child through the eligible Item Catalog FSM route. Verify
the exact existing parent and preserve it unchanged. RatingModelCode and all
optional description, end-date, translation, relationship and advanced fields
are omitted. Do not associate this behavior with a competency or enable a Profile
Section. Show exact code and case-insensitive same-catalog Name checks before
any package or import.
```

## 7. CERTIFICATION

```text
I want one synthetic certification in an existing certification catalog:
ContextName = CERTIFICATION
ContentValueSetCode = G8154_CERT_CAT_0911
Existing catalog name = FSCR Synthetic Certifications
ContentItemCode = G8154_CERT_ITEM_0911
Name = FSCR Synthetic Safety Certification
DateFrom = 2026-09-11
ContentSupplierCode = C

Review one create-only Item Catalog FSM child after verifying this exact existing
parent. Keep its values unchanged. No Rating Model, description, end date,
translations, relationships, renewal/expiry rules, issuing-body fields or other
advanced fields are supplied. Do not award a certification to an employee.
Show exact code and same-catalog Name collision results; no package or import yet.
```

## 8. COMPETENCY — catalog-backed

```text
I want one synthetic competency in an existing competency catalog:
ContextName = COMPETENCY
ContentValueSetCode = G8154_CMP_CAT_0911
Existing catalog name = FSCR Synthetic Competencies
ContentItemCode = G8154_CMP_ITEM_0911
Name = FSCR Synthetic Structured Analysis
DateFrom = 2026-09-11
ContentSupplierCode = C

Review one create-only Item Catalog FSM child with the exact unchanged parent.
Unlike the legacy example, no RatingModelCode is supplied: leave it blank. No
descriptions, end date, translations, proficiency/rating descriptions, behavior
relationships or advanced fields are supplied. Do not create a Rating Model or
assign this competency to a profile. Show duplicate and provider checks before
any package or import.
```

## 9. DEGREE

```text
I want one synthetic degree reference in an existing degree catalog:
ContextName = DEGREE
ContentValueSetCode = G8154_DEG_CAT_0911
Existing catalog name = FSCR Synthetic Degrees
ContentItemCode = G8154_DEG_ITEM_0911
Name = FSCR Synthetic Applied Systems Degree
DateFrom = 2026-09-11
ContentSupplierCode = C

Review one create-only Item Catalog FSM child; verify and retain the existing
parent unchanged. Omit RatingModelCode, description, end date, translations,
relationships and advanced fields. Do not create a school, educational level,
employee degree record or inferred degree-to-level relationship. Show exact
duplicate results and provider eligibility; do not package or import yet.
```

## 10. EDUCATION_LEVEL

```text
I want one synthetic education-level reference in an existing catalog:
ContextName = EDUCATION_LEVEL
ContentValueSetCode = G8154_EDL_CAT_0911
Existing catalog name = FSCR Synthetic Education Levels
ContentItemCode = G8154_EDL_ITEM_0911
Name = FSCR Synthetic Advanced Education Level
DateFrom = 2026-09-11
ContentSupplierCode = C

Review one create-only Item Catalog FSM child with the verified unchanged parent.
Omit RatingModelCode, description, end date, translations, relationships and
advanced fields. Do not infer an education hierarchy, degree mapping, ordering
or employee education record. Show exact code/name checks and provider eligibility
before any package or import.
```

## 11. HONOR

```text
I want one synthetic honor reference in an existing honor catalog:
ContextName = HONOR
ContentValueSetCode = G8154_HON_CAT_0911
Existing catalog name = FSCR Synthetic Honors
ContentItemCode = G8154_HON_ITEM_0911
Name = FSCR Synthetic Service Excellence Honor
DateFrom = 2026-09-11
ContentSupplierCode = C

Review one create-only Item Catalog FSM child after exact parent verification;
preserve the parent unchanged. Omit RatingModelCode, description, end date,
translations, relationships, award dates and advanced fields. This does not award
an honor to an employee. Show exact duplicates and current provider readiness;
historical successful tests do not approve this package. Do not import yet.
```

## 12. LANGUAGE

```text
I want one synthetic profile language item in an existing language catalog:
ContextName = LANGUAGE
ContentValueSetCode = G8154_LNG_CAT_0911
Existing catalog name = FSCR Synthetic Languages
ContentItemCode = G8154_LNG_ITEM_0911
Name = FSCR Synthetic Demonstration Language
DateFrom = 2026-09-11
ContentSupplierCode = C

Review one create-only Item Catalog FSM child with the exact unchanged parent.
Omit RatingModelCode, description, end date, translations, proficiency values,
relationships and advanced fields. This is not a request to install or enable
an application language, translate UI text, or change an employee profile.
Show exact duplicate checks and route eligibility; do not package or import yet.
```

## 13. MEMBERSHIP

```text
I want one synthetic membership reference in an existing membership catalog:
ContextName = MEMBERSHIP
ContentValueSetCode = G8154_MEM_CAT_0911
Existing catalog name = FSCR Synthetic Memberships
ContentItemCode = G8154_MEM_ITEM_0911
Name = FSCR Synthetic Systems Association Membership
DateFrom = 2026-09-11
ContentSupplierCode = C

Review one create-only Item Catalog FSM child after exact parent verification;
preserve its values unchanged. Omit RatingModelCode, description, end date,
translations, relationships, renewal rules and other advanced fields. Do not
create a party, association foundation or employee membership transaction.
Show exact code/name and eligibility checks before any package or import.
```

## 14. PROJECT

```text
I want one synthetic controlled project reference in an existing project catalog:
ContextName = PROJECT
ContentValueSetCode = G8154_PRJ_CAT_0911
Existing catalog name = FSCR Synthetic Projects
ContentItemCode = G8154_PRJ_ITEM_0911
Name = FSCR Synthetic Process Mapping Project
DateFrom = 2026-09-11
ContentSupplierCode = C

Review one create-only Item Catalog FSM child with the exact unchanged parent.
Keep PROJECT exactly; do not change it to SPECIAL_PROJECT or select the free-form
Special Project route. Omit RatingModelCode, description, end date, translations,
relationships and advanced fields. Do not create a project-management project,
staffing assignment or employee profile item. Show exact duplicates and provider
eligibility before any package or import.
```

For every case 6–14, success requires terminal import success plus independent
same-target readback of the exact child, all supplied child values and unchanged
parent portable values. It does not establish multi-child, richer-field,
competency-to-behavior or new-parent-and-child support.

## 15. Instance Qualifiers — review only

The following is a complete synthetic selected-row proposal. Parent references
are supplied for review, not evidence that the Profile Type/Section exists.
No standalone import or non-invasive containing-task executor is approved.

```text
Review this synthetic Instance Qualifier Set and its two selected qualifier rows.
Do not export, package or import anything in this request.

QualifierSetCode = G8154_QUAL_SET_0911
ProfileTypeCode = PERSON
ContextName = COMPETENCY
SectionContext = G8154_COMP_SECTION_0911
Description = Synthetic assessment sources for manual proposal validation.
QualifierTypeCode = Q
KeyTableName is intentionally omitted because this uses selected rows, not a
prompt/key-table source.

Row 1:
QualifierCode = G8154_SELF_0911
Description = Synthetic self assessment
QualifierSeqNumber = 1
EmpViewFlag = Y
EmpDefFlag = Y
MgrViewFlag = Y
MgrDefFlag = N
SearchFlag = Y

Row 2:
QualifierCode = G8154_MANAGER_0911
Description = Synthetic manager assessment
QualifierSeqNumber = 2
EmpViewFlag = Y
EmpDefFlag = N
MgrViewFlag = Y
MgrDefFlag = Y
SearchFlag = Y

Keep the complete set and both rows. Confirm mappings against the supported
source-backed contract. Treat the supplied Profile Type and Section as unverified
references; do not create or modify them. Explain the standalone no-column
limitation. Identify the Profile Types owner for any separately requested complete
containing evidence. Do not claim absence or a working import route.
```

Expected: source-backed review or an explicit mapping/reference blocker. A good
review is not live Instance Qualifier execution proof.

## Continue a supported case through its actual gates

These follow-ups deliberately bind to the artifacts actually returned in the
same case. A pre-filled fake SHA or job ID would be unsafe, not a complete example.

### Review to local package

```text
For this single reviewed case, show the complete proposal fingerprint, all exact
provider rows and their fingerprint, task context, target, dependency
evidence and export-baseline binding. Identify all omissions and blockers.
Request the actual package-preparation confirmation required by this route.
Do not treat this request or my field confirmation as upload/import approval.
```

If the route requires `PREPARE PACKAGE` followed by a fingerprint, use the exact
fingerprint displayed by that live workflow, not an identifier copied from this
guide. Approve the exact provider rows separately where the contract requires it.

### Package to Core Data Loader preview

```text
For the one validated immutable archive just prepared for this case, show its
actual path, SHA-256, task, target and complete contents through the required
Core Data Loader Task Hook preview. Revalidate its bindings. Ask for the required
submission approval; do not upload or initiate while that approval is missing.
```

Give a contextual approval only after reviewing that exact preview. The guide,
old session-wide testing intent, a successful login and a previous case's approval
do not approve the next load. No bypass or automatic batch approval is requested.

### Accepted initiation to status and readback

After the loader has returned actual accepted IDs, paste:

```text
For the accepted load in this case, use its recorded process/request IDs and the
declared Core status workflow to obtain terminal status and ProcessLog within
the bounded polling policy. Do not initiate another load. Then prepare the
separately gated fresh same-target export/readback request and obtain its actual
approval where required. Compare every approved value, generated identity where
applicable, and protected parent/reference. Report any differences without
automatic correction. If status is unknown or timed out, retain the IDs and give
the status-only next check; do not retry the import.
```

## Record results without overstating them

For each case record the prompt/input, commit SHA, authenticated safe target
alias, verified profile mode, task/provider, exact matches and dependency
results, baseline/evidence fingerprints, immutable package hash, retained
approval, accepted IDs, terminal result/ProcessLog and independent readback.
Record `not run`, `blocked`, `failed`, `partial` or `verified` honestly; export,
template, local-unit and response-only passes are separate result categories.

Do not use these author-written examples as independent forward-test proof.
They are guided manual scenarios and have not themselves been live-executed.

## Authoritative local contracts

- [Parent workflow](../SKILL.md)
- [Supplied-configuration intake](../business-intent-contract.md)
- [Source-backed input fields](source-backed-input-contract.md)
- [FSM package and approval contract](fsm-import-contract.md)
- [FSM evidence contract](fsm-evidence-contract.md)
- [Nine-context provider registry](../item-catalogs/references/catalog-content-item-fsm-provider.json)
- [Verified GOAL exception](verified-fallback-contract.md)
- [Instance Qualifier field/read ownership](../instance-qualifiers/ora-resource/ora_reference_lookups.md)
