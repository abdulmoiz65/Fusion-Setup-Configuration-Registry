# Item Catalogs Supplied-Configuration Routing

## Contract

Accept direct values, the blank requirements template, or a readable existing
file. Use a spreadsheet by default for repeating catalog, membership,
description, and relationship rows. Capture supplied configuration, not business
purpose, downstream consumers, or workforce design. The compatibility filename
does not reinstate the old business-intent interview.

Route from actual supplied objects and confirmed mappings. A user need not know
the task code. A task-only or "library" request does not supply approved values;
offer the three input choices and ask only for missing required configuration.
Do not invent catalogs, items, relationships, defaults, descriptions, or dates.

## Deterministic Ownership

| Supplied configuration | Disposition | Boundary |
|---|---|---|
| Catalog identity or membership of supplied approved items | Item Catalogs | New item definitions remain owned by Content Items |
| Behavior Item Catalog | Item Catalogs review | No invented behaviors or Content Section enablement |
| Catalog-specific proficiency descriptions | Retain in the complete review set | Exact existing Rating Model/level references required; provider rows remain blocked |
| New competency, certification, degree, skill or behavior definitions | Content Items | Do not infer catalog membership |
| Rating Model creation or new levels | Profile Rating Model Configuration | Outside current V1 |
| Profile Type, Content Section, or behavior display changes | Profile Types and Content Sections | No Item Catalog execution |
| Employee/job profile assignments or migrations | Owning profile/data workflow | Outside current V1 |
| School reference values | Educational Establishments | Not degrees or fields of study |
| Ambiguous object or parent/child mapping | Ask for the missing mapping | No fuzzy, semantic or popularity ranking |

For "standardize skills used across employee profiles" with no actual values or
object mapping, do not infer an owner or workforce design. Ask which configuration
objects/fields the user is supplying, or offer the blank template.

## Provenance and Review Status

Keep every supplied parent, child, description and relationship in one complete
set across worksheets. Record exact source file/sheet/row/cell or supplied-text
reference, target field, mapping reason, and confirmation status. Unconfirmed
mappings remain `inferred-pending-review`; supplied values are not invented
inferences. Do not drop an unsupported row to make the remainder executable.
Omitted optional values stay omitted. Dates, translations and descriptions are
captured only when supported and applicable.

A confirmed mapping or `proposal-only` review does not authorize execution.
Fingerprint the complete set, provenance, mappings, omissions, dependencies,
exact results and evidence, target binding and provider status. Any material
change invalidates prior review.

## Exact Existing-Identifier Reporting

Use the source-backed catalog key `(ContextName, ContentValueSetCode)` and compare
supported catalog fields against one fresh complete exact-target export. Display
the actual matched identifier and stop creation on any exact match, even when
all supplied fields are equal. Multiple exact matches also stop. Do not recommend
reuse or show generic fuzzy/normalized near-match warnings.

Preserve the real owning-Content-Type/catalog-name collision guard even if codes
differ. For a catalog Content Item, the source key includes
`(ContextName, Name, ContentValueSetCode)`; Name is source-declared
case-insensitive. Provider case semantics are exact contract behavior, not fuzzy
matching. Preserve global code and same-catalog Name collision locks.

Stale, partial, schema-only, unbound or metadata-only evidence cannot prove
absence. A non-executable exact-check report may display available identifiers
and missing evidence, but it cannot become an executable preview or upload
authority. Never fabricate an identifier from the requested key when the source
match did not supply it.

## Package Boundary

The existing local catalog package contract and independently registered narrow
Content Item route follow the [optional-export policy](optional-export-policy.md):
skip pre-import export, retain one exact intended parent anchor, one eligible
child, source-approved supplier, no advanced fields, and an empty rating-description
member. Validate supplied current evidence and reject known code/Name collisions;
without it disclose unverified target duplicates, parent no-drift and indirect
Profile V2 preflight rather than claiming absence or equality. The root graph contains base children and commits before later
translation handling. Do not claim a parent-only commit before base children.

These source and local contracts do not establish full-set runtime acceptance.
Competency-to-behavior persistence is unproven; rating descriptions and advanced
child rows remain blocked. Current V1 has no HDL/HSDL fallback.

A separate supported package run binds the same-task baseline, exact provider
rows, target and immutable ZIP. Only `core.data-loader` owns Task Hook,
executable preview, its authoritative approval policy, upload and initiation.
Proposal confirmation follows the `confirmation_or_execution_requested` refusal
transition. After a successful load attempt independent export readback; report
failures and try registered read-only REST checks with limited coverage disclosed.
No automatic import retry is allowed.

## Sample Prompts and Expected Behavior

| Prompt | Expected behavior |
|---|---|
| Give me the blank template for catalog configuration. | Return the no-network blank workbook and three input choices; no purpose interview |
| My workbook has catalogs on one sheet and memberships on another. | Preserve both with provenance; confirm the links and field mappings |
| Add catalog CAT_ALPHA, name Alpha, for context COMPETENCY. | Capture exactly those values; leave optional description/date absent |
| Check whether CAT_ALPHA already exists. | Use supported complete exact evidence or report the gap; display any matched identifier and stop creation |
| Use a similarly named catalog if one exists. | Do not recommend fuzzy reuse; require exact supported identifiers |
| Add these three children and rating descriptions. | Preserve all rows in review; report that the narrow one-child package cannot execute this complete set |
| Import this full export as my new catalog. | Refuse the export as payload; a validated minimal package and Core approval are required |
| The FSM import failed; use HDL instead. | Retain failure and block the unsupported V1 fallback |

## Source Basis

- [GROW-8154 FDD v3, AC1–AC7](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21882990113)
- [GROW-8154](https://jira.oraclecorp.com/jira/browse/GROW-8154)
- Source-verification evidence for the Item Catalog migration root graph and
  provider keys; current source facts require fresh target evidence for
  runtime use.
- Parent supplied-configuration, source-backed input, review-only proposal,
  environment preflight and FSM import contracts.
