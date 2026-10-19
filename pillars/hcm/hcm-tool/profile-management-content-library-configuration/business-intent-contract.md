# Supplied-Configuration Intake and Routing Contract

## Purpose

Capture configuration supplied in ordinary language or a readable file. Offer direct entry, a blank requirements template, or an existing-file upload. Use a spreadsheet by default for repeating data. The filename is retained for existing references; current V1 behavior follows GROW-8154 FDD v3 AC1-AC7 and GROW-8688-GROW-8712.

For user-requested manual examples, use the [filled synthetic task prompts](references/manual-testing-prompts.md). They are guided scenarios, not executed evidence or standing approval.

Do not ask for business purpose, workforce design, downstream consumers, or intended use to select a task. A request without values may receive the blank template immediately. A request with values enters normalization and review without a business-language restatement.

## Input and Complete-Set Rules

1. Accept directly supplied values, the [blank XLSX](templates/profile-management-content-library-configuration-intake.xlsx), or a readable existing file. The optional flat CSV is another intake representation.
2. Capture one object or one complete related set across all five task families. Preserve every supplied parent, child, reference, relationship and source row across worksheets. Use one complete_set_id.
3. Retain safe filename, source fingerprint, page/sheet/row references, extracted values and confirmed source-to-field mappings. Preserve the source file unchanged. Show an uncertain mapping and obtain confirmation before creation.
4. Leave omitted optional values omitted. Capture descriptions, translations and dates only when supplied, supported and applicable. Item-specific proficiency descriptions require verified existing applicable Rating Model and level references; never create those dependencies.
5. Ask for a missing required value or object distinction only when it affects validation or ownership. Do not invent values from comparable setups, documented defaults or business objectives. Provider-generated technical values require a documented approved execution/readback contract.
6. Unreadable or unsupported input stops with the affected file/row and a correction or resubmission action. Host extraction of Word/PDF requires a readable source and confirmed mapping; the CSV/XLSX helpers do not parse arbitrary documents.

## Normalized Value Contract

| Field | Required behavior |
|---|---|
| Value | Preserve the supplied value without silent rewriting |
| Owning task | Resolve from supplied objects and fields |
| Source type | User statement, supplied file, confirmed mapping, approved decision or exact provider lookup |
| Exact source reference | Sentence, filename and sheet/row, documentation anchor or lookup evidence |
| Sanitized evidence | Non-sensitive supplied value, source rule or resolver result |
| Confidence | Mapping confidence does not confirm a mapping |
| Materiality | Material when it changes values, identity, scope, relationships, dates or execution |
| Review status | supplied, inferred-pending-review, confirmed, blocked or not-applicable |
| Inference reason | Explain a proposed technical mapping; never invent missing values |
| Proposal/execution status | proposal-only during review; Core Data Loader owns execution approval |
| Last-confirmed fingerprint | Fingerprint of the complete request in which the mapping was confirmed |

Do not promote `inferred-pending-review` to `confirmed` without user review. This status records unresolved mapping, not authority to infer optional configuration. Keep unknown required fields visible as blockers.

## Supplied-Object Routing

Use the source-backed ownership mappings below. An explicit task/code or unambiguous object structure selects its owner. Ordinary language is supported; Fusion terminology is not required. Never silently select a pattern when the supplied object remains ambiguous.

| Supplied object or fields | Owning task | Boundary |
|---|---|---|
| Type definitions, properties or type relationships | Content Types | No item values or dependent foundations inferred |
| Named items under a supplied existing type, translations, item-specific descriptions or item relationships | Content Items | No catalog membership or profile assignment inferred |
| Catalog definitions, supplied catalog items or behavior catalogs | Item Catalogs; Content Items when their definitions are supplied | Keep the complete set; no section enablement |
| Qualifier sets and qualifier rows | Instance Qualifiers | Unsupported containing-task execution remains blocked |
| Approved schools, colleges or universities as establishment references | Educational Establishments | No employee education records |
| Exact task name or code | The named task | No task inferred from intended use |

Ask one concise question about an ambiguous supplied configuration, for example: "Which records are you supplying: content items, an Item Catalog with its items, or profile assignments?" Do not ask why or for downstream consumers. "Standardize skills across employee profiles" supplies insufficient object/value detail; offer the three input choices and clarify the object. Do not select Content Items from the word "skills" alone.

### Explicit Current-Item Content Type Is Authoritative

Resolve the explicit Content Type supplied for the current item to exactly one current task-local context and lifecycle; stop if unknown or ambiguous. Never inherit the preceding item's type, evidence or package builder. Apply this to Goal, Behavior, Certification, Competency, Degree, Education Level, Educational Establishment, Honor, Language, Membership, Skill, Special Project and Projects.

Explicit Skill catalog/item creation uses SKILL and the [controlled Item Catalog
new-set route](item-catalogs/references/skill-catalog-creation.md). Do not mistake
it for Skills Center enablement or subscription configuration; those remain
separate consuming-product work. Historical HDL blockers do not govern this
independent non-production FSM capability.

`Certification` selects `CERTIFICATION`, never `GOAL`. The provider lifecycle label `certification-only` describes controlled-use readiness and is not a Content Type mapping. Preserve registered contexts and Name/code collision guards. `PROJECT` and free-form `SPECIAL_PROJECT` are different contexts; the specialProjectContentItems relation does not make them interchangeable. A blocked context routes to its declared owner. Historical verified read or HDL evidence does not establish current V1 FSM creation support.

## Ownership Boundaries

| Request | Owner disposition |
|---|---|
| Rating Model design, levels, categories or distributions | Route to hcm.hcm-tool.profile-rating-model-configuration |
| Profile Types, Content Sections, or behavior enablement on a section | Route to the Profile Types and Content Section owner |
| Employee, contingent worker, job, position, or other profile-instance values | Route to the owning profile/data skill |
| Update, delete, merge, migration or downstream configuration | Reject as outside current V1; migration belongs to Profile Management Data Load, Migration, and Maintenance |
| Goals, performance templates, talent review, succession, compensation, Skills Center, plans, meetings or notifications | Route to the consuming product skill |

Do not partially process an out-of-boundary request. A split requires confirmed scope. Existing rating models, levels, lookups, value sets, profile options and foundations are verified dependencies only.

## Exact-Match Contract

Use only supported identifiers and the declared provider's exact case/normalization semantics against complete fresh target evidence. Provider-defined equality is not a similarity search. Do not perform or display fuzzy, partial, semantic, near-match or intelligent reuse analysis.

| Classification | Meaning | Required disposition |
|---|---|---|
| exact | One record matches the supported exact key | Stop creation; display the actual matched identifier and evidence reference |
| not-found | No exact record in complete supported evidence | Continue remaining validation; the check is not creation approval |
| multiple-exact | More than one exact candidate | Stop creation; retain all actual matching identifiers and resolve evidence ambiguity |
| evidence-unavailable | Source incomplete, stale, unsupported or unbound | Stop duplicate disposition; absence is unproven |

An exact duplicate blocks create even when all values are identical. Do not offer reuse, a second create, update or merge. Preserve provider-specific Name/code collision guards and fresh-customer/validated-seed evidence rules. Check each independently identifiable child, not only its parent.

## Review-Only Proposal Shape

Present the complete supplied set, source and confirmed mappings, values and provenance, supplied/omitted groups, validations, existing dependencies, exact results and matched identifiers, exclusions and provider gaps. Distinguish item-specific proficiency descriptions from Rating Model/level definitions.

For a canonical request with literal keys:

```text
python3.11 pillars/hcm/hcm-tool/profile-management-content-library-configuration/scripts/build_profile_content_library_preview.py exact-report <contract.json> --target-environment-alias <alias>
```

The diagnostic report retains all 14 groups, target, source/mapping provenance and a report fingerprint. Missing matching identifiers remain an evidence gap; never manufacture them from the proposed key. This helper validates literal-key bindings, not provider-specific normalization or fresh live evidence. Use the declared provider adapter for its exact semantics. The report has no executable preview fingerprint, approval action or submission authority.

`Prepare configuration` means refine the local review-only proposal. Proposal confirmation, `Prepare configuration` and assumption/mapping confirmation cannot approve a Fusion create, FSM import, HDL, HSDL, REST call or provider operation.

Prepare configuration | Review assumptions

## Proposal Fingerprint and Execution Separation

Fingerprint the complete supplied set, target, source, confirmed mappings, validations, dependency and exact-check evidence, omissions, exclusions and provider readiness. Any material change creates a new fingerprint and invalidates prior confirmation.

Only a separately requested supported create-only FSM package may proceed through the [FSM import contract](references/fsm-import-contract.md) and Core Data Loader's authoritative Task Hook, immutable preview and approval gate. Preserve its actual approval/auto-approval rules. Strict V1 acceptance excludes HDL/HSDL/DAT and direct REST/browser creation. A separately selected [verified GOAL fallback exception](references/verified-fallback-contract.md) may proceed only under its exact provider and Core Data Loader gates. It does not supply FSM-only acceptance; other historical HDL artifacts remain regression history.

Retain single-parent/single-child catalog and rating-description guards. Complete new-catalog/multiple-child relationships and non-invasive qualifiers require their reviewed provider contracts. After a supported approved import, retain accepted IDs, terminal state and ProcessLog, independently read back all saved values and protected references, report discrepancies and never auto-correct or retry.

## Traceability and Data Safety

Persist only sanitized synthetic/local inputs and evidence references, fingerprints, mappings, validations, exact results, lifecycle state, omissions, provider gaps and safe next actions. Preserve historical evidence. Never retain credentials, tokens, source documents, employee/customer data or full current-state rows in project artifacts.
