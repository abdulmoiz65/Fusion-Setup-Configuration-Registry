# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Operation | AF.ROUTE_OPERATION selects exactly one supported branch after request, task/export and reference checks; no generic View/Change/Validate execution branch |
| 2 | Source-dependent resolution | Resolve one source flow/version or existing parent/type/all version names before dependent defaults. Template copy occurs only after new-target conflict validation |
| 3 | Candidate baseline | Draft statuses, deterministic name, uniqueness, Recruiting Type, options and translation plan precede baseline construction. Factory for DesignNew/CreateVersion; preserve copied source for template |
| 4 | Design validation | Validate fixed layout, every block's applicability/reuse, required placement, sequences, prohibited fields and final lengths before package branch |
| 5 | Package and handoff | Require all applicable Defaults and Design Gates Coverage evidence below. Owning workflow materializes every instruction in CSV, verifies final ZIP and checksum, then renders the Business-first Preview Contract. Preview-ready is not import approval; no resource-local processor or Fusion mutation |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| AF.ROUTE_OPERATION | Error | | Operation is not exactly one supported branch | Select Retrieve, DesignNew, CreateFromTemplate or CreateVersion; route malformed/unsupported input to issues | User correction only |
| AF.ROUTE_OPERATION; create-flow scope | Error | | A create-flow request is reduced to a root-only operation or waits for a separate request to add its initial version | By default DesignNew creates one new Draft flow plus one initial Draft version and its required hierarchy in the same preview/package. CreateFromTemplate also includes one initial Draft version. Use VersionName defaulting when omitted; do not ask whether to include a version. An explicit existing-parent version request stays CreateVersion; an explicit root-only/no-version request is outside the supported package contract and must be clarified, not silently expanded | Preserve explicit scope and all existing Data Loader validation/approval gates; no activation |
| AF.COPY_SUPPORTED_TEMPLATE_HIERARCHY | Error | resolve_apply_flow_availability | Source root/version is unresolved, target identity conflicts, copied hierarchy is ambiguous or unrelated data would be copied | Copy exactly one selected source root/version after conflict checks; preserve Description, applicable options, source section/page layout/counts/base names/sequences, block membership/title/instructions and existing supported translation values/SourceLang; exclude all property-child rows. Retain source block membership for applicability validation unless Explicit Block Selection replaces it; do not silently filter unsupported source blocks. Inherit type; never mutate source | Only supported explicit new-target overrides |
| AF.COPY_SUPPORTED_TEMPLATE_HIERARCHY; target identity | Error | | Source identity or parent keys survive as target keys | Freeze requested target AfCode/name. Copy with target root identity; rewrite every descendant parent key. Retain selected version content until final target VersionName is resolved, then replace every target version key before materialization. Defaults enforce Draft statuses; never let copying restore source status or identity | Mandatory consistent target-key rewrites |
| AF.RESOLVE_FACTORY_SKELETON | Error | | Factory section/page data is missing, a template layout would be rebuilt, or baseline blocks would be added despite explicit selection | Construct exact factory sections/pages for DesignNew/CreateVersion or preserve selected template sections/pages. Apply Explicit Block Selection below before materializing blocks; factory/copied membership is used only when block information is omitted | Supported new-target choices only; never add unrequested defaults |
| AF.VALIDATE_FIXED_LAYOUT | Error | | New design/version differs structurally from factory, or template differs structurally from selected source | Preserve applicable baseline section/page identities, counts, order, base names and sequences. A non-factory template layout is valid and must not be normalized. No added/removed/base-renamed/reordered sections or pages; explicit non-base SectionName/PageName translations are allowed | Non-base translations only; no structural fix inferred |
| AF.VALIDATE_BLOCK_APPLICABILITY | Error | resolve_apply_flow_block | Any retained explicit or copied block is unknown, unsupported or inapplicable to inherited/selected type | Validate each candidate instance through the supported canonical inventory. Report a rejected block's code and position with supported choices. Do not silently drop or replace an explicitly requested or retained template block. No source-release gate; no Timeline/Education/Experience condition. Work Preferences follows factory and inventory only | Explicit supported new-target selection or a template without the unsupported block |
| AF.VALIDATE_BLOCK_REUSE | Error | resolve_apply_flow_block | Nonreusable block appears more than once across the complete version | Y permits explicitly requested additional instances; N once per version. An implicit request for an already-present block is reported as already included and deduplicated, not materialized again | Explicit valid additional instances only |
| AF.VALIDATE_BLOCK_REUSE; ambiguous instance | Error | | Move/remove/reorder/title/instruction request could address several repeated instances | Show BlockCode, fixed page, current order and title for candidates and ask for the intended instance. Never alter one or all arbitrarily | User disambiguation only |
| AF.VALIDATE_REQUIRED_BLOCKS | Error | | Applicable mandatory Contact Information is missing or moved from baseline page; External Summary is absent/not globally final; retained Profile Import is not first | Validate required-block constraints without silently adding or restoring omitted blocks. If an explicit selection conflicts with a mandatory constraint, stop and explain it; request correction instead of changing the list. Contact retains its baseline section/page, not a fixed block position; it becomes position 1 when selected alone. Profile Import is first only when selected or included by omitted-input defaults. Preserve fixed section/page layout | User correction for a conflict; no automatic additions |
| All block construction | Error | resolve_apply_flow_block | Requested block changes are not materialized or leave invalid parent links/translations | Allow add/remove/move/reorder only while constructing a new target within fixed pages; preserve each valid block's text/translation identity through moves and remove orphan descendants. Final page-block sequences are checked by AF.VALIDATE_SEQUENCES | Explicit supported requests only |
| Bare property-capable Draft block | Error | | A restriction is invented solely because activation could need properties | Allow bare ORA_QUESTIONNAIRE for PADC when applicability/reuse passes; retain every property-child member header-only. Activation is never performed | No property capture |
| Translation materialization | Error | resolve_apply_flow_languages | Final entities do not implement the resolved language plan, duplicate/orphan TL rows exist, valid copied values are replaced without an explicit override, or unsupported fields change | Apply the language plan to final layout and every retained/new block instance before package validation. Preserve valid template rows/values/SourceLang; apply only the documented missing/blank-title fallback and language materialization from ora_reference_lookups.md. Supported explicit overrides affect exact language/field only. Keep CreateVersion root/root-TL/availability empty | Documented missing-title defaults and supported explicit translations only |
| AF.ROUTE_CREATION | Error | | Candidate has not passed all applicable preceding checks or operation is ambiguous | Select only its new-flow, template or new-version package branch; no path to a mutation | Correct failed node first |
| AF.BUILD_NEW_FLOW_GUIDANCE | Error | | Required new-root/version hierarchy or package facts are missing | Describe exactly one new Draft root and one initial Draft version using Operation Row Scope and Package Members for the owning workflow, including when no version was explicitly requested; consume VersionName and per-instance title defaults before translation materialization. Require immutable byte evidence at AF.VALIDATE_NEW_FLOW_PACKAGE | Owning workflow prepares artifact before validation |
| AF.BUILD_NEW_VERSION_GUIDANCE | Error | | Existing parent/type/all names were not resolved or root data would be imported | Describe one new Draft factory version under that parent; root/root-TL/availability members remain header-only; require byte evidence at AF.VALIDATE_VERSION_PACKAGE | Owning workflow prepares artifact before validation |

## Explicit Block Selection

These rules apply only when constructing a new target in DesignNew,
CreateVersion or CreateFromTemplate. They do not permit editing existing
versions, and they do not change fixed section/page structure.
The same input-precedence policy applies to every supported AfTypeCode:
ORA_EXTERNAL, ORA_PADC, ORA_TALENT and ORA_EVENT. Type controls block
applicability, fixed layout and fallback values, not whether explicit input
wins. Unsupported creation types remain unsupported.

| Situation | What Happens |
|---|---|
| User names blocks for a new target | Treat the named blocks as the complete requested selection, even when phrased add Contact Info without the word only. Start with no block rows and materialize only the selected valid instances. Do not union the list with factory or copied blocks. |
| User requests all blocks from the library | Expand to one instance of every supported Canonical Block Inventory entry applicable to the selected AfTypeCode. Apply the existing placement, required-block and ordering rules to the supported selection. Any additionally named block must pass AF.VALIDATE_BLOCK_APPLICABILITY. |
| No block information supplied | Use factory blocks for DesignNew/CreateVersion or the selected source blocks for CreateFromTemplate. Defaults are fallback data, not additions to an explicit list. |
| Explicitly asks to keep defaults or source blocks and add a block | Preserve that expressly requested baseline plus the requested additions. Do not infer this intent from add alone. |
| Placement and order | Keep the fixed section/page skeleton. For a selected block with an established baseline page, use that page when omitted, then renumber selected blocks contiguously from 1. Ask for placement or instance clarification when unresolved; never add another block to determine placement. |
| Empty, malformed or conflicting selection | Do not treat explicit empty/invalid input as omission and restore defaults. Apply existing validation; if requirements conflict, stop with the exact correction needed, without adding unrequested blocks. |
| Titles and translations | Populate canonical display-name titles for selected blocks when omitted. Materialize translations only for retained/new selected instances; remove excluded block descendants from the candidate, never from the existing source. |
| Final package gate | Reopened block rows must match the resolved requested selection exactly, including instance count, page and order, with no leftover factory/copied rows or translations. An extra Profile Import in a Contact Information-only Event request fails before preview or import approval. |

## Defaults and Design Gates Coverage

This is the authoring coverage map, not runtime test evidence. Each row is
Documented by the existing reachable nodes or the explicit owning-workflow
handoff. AF.ROUTE_CREATION requires all applicable preceding checks; the three
package-validation nodes require materialized evidence before their distinct
preview terminals. A missing check, invalid default or unresolved evidence
blocks readiness through AF.HANDLE_ISSUES -> AF.RETURN_ISSUES; it must not be
silently defaulted or waived.

| Area | Owning resource and reachable rule or handoff | Required evidence before preview | Status |
|---|---|---|---|
| Operation precedence | ora_reference_lookups.md: AF.RESOLVE_SOURCE_FLOW, AF.RESOLVE_SOURCE_VERSION, AF.RESOLVE_PARENT_FLOW; this file: AF.ROUTE_OPERATION, AF.COPY_SUPPORTED_TEMPLATE_HIERARCHY, AF.RESOLVE_FACTORY_SKELETON | Selected branch resolves source/parent before dependent defaults; factory versus copied baseline identified; Retrieve has no creation defaults | Documented |
| Identity and versions | ora_input_validation.md: AF.VALIDATE_TARGET_IDENTITY, AF.VALIDATE_TEMPLATE_CONFLICTS, AF.VALIDATE_VERSION_CONFLICT; ora_defaulting_rules.md: AF.DEFAULT_STATUSES, AF.DEFAULT_VERSION_NAME | New-root identity absent; new-flow request includes one initial Draft version without a separate version request; existing parent resolved for CreateVersion; name unique including inactive names, chosen deterministically and frozen; target Draft and CreateVersion parent unchanged | Documented |
| Field limits and omitted text | ora_input_validation.md: AF.VALIDATE_REQUEST, AF.VALIDATE_FIELD_LENGTHS and package title checks; ora_defaulting_rules.md: Standard Defaults consumed by AF.DEFAULT_STATUSES and construction/package nodes | Lengths pass without truncation; each title's exact resolved BlockName, preserved custom/source or explicit override provenance recorded; all base/TL titles nonblank with base/US agreement; optional Description/instructions may remain empty | Documented |
| Options | ora_defaulting_rules.md: AF.RESOLVE_VERSION_OPTIONS; ora_input_validation.md: AF.VALIDATE_REQUEST | Exact four-type/six-field matrix and business labels; copied/default/explicit precedence; invalid supplied tokens rejected; applicable unassigned N and inapplicable empty | Documented |
| Layout | This file: AF.RESOLVE_FACTORY_SKELETON, AF.VALIDATE_FIXED_LAYOUT | Exact factory sections with Page 1 or unchanged copied source layout/sequences; no structural/base-name changes; only supported non-base translations | Documented |
| Blocks | This file: AF.RESOLVE_FACTORY_SKELETON, AF.VALIDATE_BLOCK_APPLICABILITY, AF.VALIDATE_BLOCK_REUSE, AF.VALIDATE_REQUIRED_BLOCKS; ora_input_validation.md: AF.VALIDATE_SEQUENCES | Explicit selection versus omitted fallback recorded; no unrequested baseline blocks; exact usage tokens, reuse, instance counts, placement and order; conflicts block without auto-additions; empty fixed pages retained | Documented |
| Properties | ora_input_validation.md: AF.VALIDATE_PROHIBITED_FIELDS, AF.REFUSE_PROPERTIES; this file: operation/package gates; ora_defaulting_rules.md: Page-block flags/text consumed during construction | Only supported block inputs; forced flags and omitted/copied text correct; all seven property children header-only; bare Draft blocks not rejected for activation-time needs | Documented |
| Recruiting Type and availability | ora_reference_lookups.md: AF.RESOLVE_RECRUITING_TYPE; this file: AF.COPY_SUPPORTED_TEMPLATE_HIERARCHY and package gates; ora_defaulting_rules.md: availability constants | External-only optional Meaning lookup when supplied; CreateVersion input rejected; distinct source/additional associations, frozen fresh IDs and forced parent/child values; conditional header-only files | Documented |
| Translations | ora_reference_lookups.md: AF.RESOLVE_TRANSLATIONS; this file: translation materialization and package gates | US plus exported non-empty language union keyed by environment/release; copy/seed/override and SourceLang evidence; no duplicates/orphans; unavailable language or required base text blocks | Documented |
| Package | This file: Operation Row Scope, Package Members, Verified Headers, Package Invariants; ora_input_validation.md: AF.VALIDATE_NEW_FLOW_PACKAGE, AF.VALIDATE_TEMPLATE_PACKAGE, AF.VALIDATE_VERSION_PACKAGE | Exact 18 CSVs plus XML/order/headers/keys; one scoped target hierarchy, required empty members, valid relationships, unchanged metadata, reopened verified bytes and frozen SHA-256 | Documented |
| Preview and submission | ora_error_handling.md: AF.NEW_FLOW_PREVIEW_READY, AF.TEMPLATE_PREVIEW_READY, AF.VERSION_PREVIEW_READY and owning core.data-loader FSM handoff | Complete actual-CSV business summary/layout/options/text/translations, separate technical evidence; later exact environment/package approval and revalidation; preview does not authorize import | Documented |
| Lifecycle and errors | ora_input_validation.md: eleven AF.REFUSE_* nodes; ora_error_handling.md: AF.HANDLE_ISSUES, AF.RETURN_ISSUES and status handoff | Unsupported dates/properties/lifecycle/edits/direct mutation refused; friendly correction and actual execution evidence; one accepted initiation distinguished from completion, no automatic polling/retry/resubmission/activation | Documented |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_apply_flow_availability | Copying External template associations | Distinct selected-source associations | ora_reference_lookups.md |
| resolve_apply_flow_block | Block construction/title defaulting and applicability/reuse validation | Exact nonblank BlockName, exact usage tokens, reusable flag | ora_reference_lookups.md |
| resolve_apply_flow_languages | Final language-plan materialization | US base, distinct available codes, source values and explicit overrides | ora_reference_lookups.md |

## Operation Row Scope

| Operation | Materialized rows | Rows forbidden |
|---|---|---|
| DesignNew | Exactly one new Draft root and initial Draft version; factory hierarchy plus valid requested changes, in-scope TL rows and optional External availability | Existing roots/versions, unrelated source data and every property-child data row |
| CreateFromTemplate | Exactly one new Draft root/version seeded from one exact eligible source hierarchy; copied Description, supported translations/options/blocks/title/instructions; all target parent keys rewritten; distinct External associations with fresh IDs | Source mutation, unrelated roots/versions, non-External Recruiting Types and every property-child data row |
| CreateVersion | Exactly one new Draft factory version under exact existing parent AfCode with inherited supported type; version descendants and their TL rows | Any root/root-TL/Description/root-status/availability/Recruiting Type data row; existing-version edits; keep root, root-TL and both availability files header-only |
| All construction | HideInMobileFlag=N and PageBlockRequiredFlag=N; defaults then explicit supported user inputs materialized; no properties required merely for future activation | Unsupported hidden/requiredness/property overrides and prohibited dates |

## Package Members

| Order | Exact member name | Content rule |
|---|---|---|
| 1 | ORA_IRC_JA_APPLY_FLOW.csv | Root; header-only for CreateVersion |
| 2 | ORA_IRC_ORA_IRC_JA_APPLY_FLOW_TL.csv | Root translations; header-only for CreateVersion |
| 3 | ORA_IRC_JA_AF_AVAIL_CXT.csv | External availability; header-only when no target associations or CreateVersion |
| 4 | ORA_IRC_JA_AF_AVAIL_CXT_REC_TYPE.csv | External Recruiting Type children; header-only when no target associations or CreateVersion |
| 5 | ORA_IRC_JOB_AF_VERSION.csv | Exactly one new version |
| 6 | ORA_IRC_JOB_AF_SECTION.csv | New version's sections |
| 7 | ORA_IRC_JOB_AF_PAGE.csv | New version's pages |
| 8 | ORA_IRC_JOB_AF_SECTION_TL.csv | Section translations |
| 9 | ORA_IRC_JOB_AF_PAGE_BLOCK.csv | New version's supported blocks |
| 10 | ORA_IRC_JOB_AF_PAGE_TL.csv | Page translations |
| 11 | ORA_IRC_AF_PAGE_BLK_DOCTYPES.csv | Header-only |
| 12 | ORA_IRC_AF_PAGE_BLK_JA_EFF.csv | Header-only |
| 13 | ORA_IRC_AF_PAGE_BLK_MISCDOCS.csv | Header-only |
| 14 | ORA_IRC_AF_PAGE_BLK_PRF_SCS.csv | Header-only |
| 15 | ORA_IRC_AF_PAGE_BLK_QSTNRS.csv | Header-only |
| 16 | ORA_IRC_AF_PAGE_BLK_SENSINFO.csv | Header-only |
| 17 | ORA_IRC_AF_PAGE_BLK_SUPDOCS.csv | Header-only |
| 18 | ORA_IRC_JOB_AF_PAGE_BLOCK_TL.csv | Block title/instruction translations |
| 19 | ASM_SETUP_CSV_METADATA.xml | Preserve exact current target-release metadata graph |

## Verified Headers

| Exact member name | Exact header |
|---|---|
| ORA_IRC_JA_APPLY_FLOW.csv | AfCode,AfStatusCode,AfTypeCode,ApplyFlowName |
| ORA_IRC_ORA_IRC_JA_APPLY_FLOW_TL.csv | ORA_IRC_JA_APPLY_FLOW.AfCode,Language,ApplyFlowName,Description,SourceLang |
| ORA_IRC_JOB_AF_VERSION.csv | AfCode,VersionName,EsignEnabledFlag,LegalEnabledFlag,OptinEnabledFlag,QuickApplyEnabledFlag,SingleClickApplyFlag,TcOptinEnabledFlag,VersionStatusCode |
| ORA_IRC_JOB_AF_PAGE_BLOCK.csv | ORA_IRC_JOB_AF_VERSION.AfCode,ORA_IRC_JOB_AF_VERSION.VersionName,ORA_IRC_JOB_AF_SECTION.SectionSeqNum,ORA_IRC_JOB_AF_PAGE.PageSeqNum,PageBlockSeqNum,HideInMobileFlag,PageBlockInstructions,PageBlockTitle,PageBlockRequiredFlag,BlockCode |
| ORA_IRC_JOB_AF_PAGE_BLOCK_TL.csv | ORA_IRC_JOB_AF_VERSION.AfCode,ORA_IRC_JOB_AF_VERSION.VersionName,ORA_IRC_JOB_AF_SECTION.SectionSeqNum,ORA_IRC_JOB_AF_PAGE.PageSeqNum,ORA_IRC_JOB_AF_PAGE_BLOCK.PageBlockSeqNum,Language,PageBlockInstructions,PageBlockTitle,SourceLang |

## Package Invariants

| Situation | What Happens |
|---|---|
| Carrier | Use current target-release immutable task export; preserve exact filenames/case, all 18 CSV members plus XML, member order, all remaining headers and metadata relationships. |
| CSV generation | Always generate every CSV member, including header-only files, as UTF-8 without a byte-order mark (BOM). In Python use encoding='utf-8', never encoding='utf-8-sig'; do not rely on the platform-default encoding. Preserve the exported column names and order. |
| Target keys | Replace every target identity/parent key consistently; retain exact existing parent AfCode for CreateVersion; exclude unrelated export/source rows. |
| Descendant relationships | Version key is AfCode plus VersionName; section adds SectionSeqNum; page adds PageSeqNum; page block adds PageBlockSeqNum. TL rows retain their corresponding parent keys plus Language. Preserve carrier-declared remaining keys and column order; every descendant must reference the one selected target hierarchy. |
| Internal identifiers | Do not add an ApplyFlowId column or populate an internal ApplyFlowId in any generated CSV. Let the import operation resolve it internally from the carrier-declared keys. An ApplyFlowId import error does not authorize a schema change; preserve the XML metadata unchanged. |
| Availability relationships | Each child uses its frozen target ObjectCxtCode; ObjectCode is the exact target AfCode and ObjectTypeCode is ORA_APPLY_FLOW. Validate both identifier fields against uppercase [0-9A-F]{32}, distinctness and DefaultFlag=N; no duplicate RecruitingTypeCode association for the target. |
| Carrier mismatch | If the current carrier differs from the required members or five verified headers, or a remaining header/relationship cannot be preserved unambiguously, show the mismatch and stop. Never synthesize unknown headers, metadata or rows. |
| Before preview | Owning runtime materializes every instruction into CSV, verifies ZIP bytes/shape/relationships and calculates SHA-256 over final immutable ZIP. A verbal design alone is not preview-ready. |
| Creation contract evidence | Apply ora_input_validation.md Package branch and Required block titles checks to reopened final CSVs: actual version-row count and parent linkage, required descendants, and each base/TL title with default/copy/override provenance must pass. A flow-header-only package or blank block title cannot reach a preview-ready terminal. |
| Supplied values versus fallback evidence | Compare reopened block rows with Explicit Block Selection and each applicable checkbox with the supplied value or omitted-field fallback in ora_defaulting_rules.md. Record input presence and provenance. Extra blocks, changed explicit Y/N or orphan translations block every creation package branch before preview. |
| Byte verification | Reopen the finished ZIP, check exact ordered member names without duplicates, and apply the CSV encoding and headers check in ora_input_validation.md to each member before comparing headers or parsing rows. Verify unchanged XML metadata and all keys, counts and header-only requirements. Compute SHA-256 on those same final bytes and freeze the artifact; no mutation of bytes after verification. |
| After preview | Any byte, environment, identity or material instruction change invalidates preview/approval and requires new verified bytes, preview and approval. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AF.ROUTE_OPERATION | decision | 50 | design_enforcement | retrieve->AF.FILTER_RETRIEVE;design_new->AF.VALIDATE_TARGET_IDENTITY;create_from_template->AF.RESOLVE_SOURCE_FLOW;create_version->AF.RESOLVE_PARENT_FLOW;invalid->AF.HANDLE_ISSUES | AF.RESOLVE_REFERENCES | stop | All. Select exactly one operation branch; ordinary create-flow intent includes a new Draft root and initial Draft version, not a root-only operation. Preserve explicit template or existing-parent version intent. |
| AF.COPY_SUPPORTED_TEMPLATE_HIERARCHY | decision | 120 | design_enforcement | success->AF.VALIDATE_FLOW_TYPE;failure->AF.HANDLE_ISSUES | AF.VALIDATE_TEMPLATE_CONFLICTS | stop | CreateFromTemplate. Copy exactly one source flow/version, its section/page layout, supported options, blocks and translations; rewrite target keys, generate new availability IDs and omit property-child rows. Retain source block membership until Explicit Block Selection and applicability validation; do not silently filter unsupported blocks. |
| AF.RESOLVE_FACTORY_SKELETON | decision | 210 | design_enforcement | success->AF.VALIDATE_FIXED_LAYOUT;failure->AF.HANDLE_ISSUES | AF.RESOLVE_TRANSLATIONS | stop | Creation. Preserve factory or copied sections/pages; apply Explicit Block Selection before block rows. Named blocks replace baseline membership; only omitted block input uses factory/copied blocks. |
| AF.VALIDATE_FIXED_LAYOUT | decision | 220 | design_enforcement | success->AF.VALIDATE_BLOCK_APPLICABILITY;failure->AF.HANDLE_ISSUES | AF.RESOLVE_FACTORY_SKELETON | stop | Creation. Validate against factory baseline for new designs/versions and selected source baseline for template copies. Preserve section/page identity, order and base names; apply only explicit translation overrides. |
| AF.VALIDATE_BLOCK_APPLICABILITY | decision | 230 | design_enforcement | success->AF.VALIDATE_BLOCK_REUSE;failure->AF.HANDLE_ISSUES | AF.VALIDATE_FIXED_LAYOUT | stop | Creation. Validate every candidate block for support and exact usage tokens through resolve_apply_flow_block. Reject explicit or retained copied instances absent from the supported inventory; no silent removal or replacement and no inventory release gate. |
| AF.VALIDATE_BLOCK_REUSE | decision | 240 | design_enforcement | success->AF.VALIDATE_REQUIRED_BLOCKS;failure->AF.HANDLE_ISSUES | AF.VALIDATE_BLOCK_APPLICABILITY | stop | Creation. Y permits explicit repeated instances; N once per version; deduplicate implicit repeated requests. |
| AF.VALIDATE_REQUIRED_BLOCKS | decision | 250 | design_enforcement | success->AF.VALIDATE_SEQUENCES;failure->AF.HANDLE_ISSUES | AF.VALIDATE_BLOCK_REUSE | stop | Creation. Check required blocks and ordering without auto-adding omitted blocks. A conflicting explicit selection stops for correction. Contact stays on its baseline page and selected sequences are renumbered; External Summary final; Profile Import first only when retained. |
| AF.ROUTE_CREATION | decision | 290 | design_enforcement | design_new->AF.BUILD_NEW_FLOW_GUIDANCE;create_from_template->AF.VALIDATE_TEMPLATE_PACKAGE;create_version->AF.BUILD_NEW_VERSION_GUIDANCE;invalid->AF.HANDLE_ISSUES | AF.VALIDATE_FIELD_LENGTHS | stop | Creation. Route the fully resolved candidate to its package validation. |
| AF.BUILD_NEW_FLOW_GUIDANCE | decision | 300 | design_enforcement | success->AF.VALIDATE_NEW_FLOW_PACKAGE;failure->AF.HANDLE_ISSUES | AF.ROUTE_CREATION | stop | DesignNew. Describe one new Draft root plus initial Draft version and required hierarchy, even when only flow creation was requested; materialize per-instance title defaults and translations for the owning package workflow. |
| AF.BUILD_NEW_VERSION_GUIDANCE | decision | 350 | design_enforcement | success->AF.VALIDATE_VERSION_PACKAGE;failure->AF.HANDLE_ISSUES | AF.ROUTE_CREATION | stop | CreateVersion. Describe one new version under existing parent; root/root-TL/availability members header-only. |
