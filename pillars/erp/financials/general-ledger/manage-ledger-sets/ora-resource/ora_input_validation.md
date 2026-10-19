# Manage Ledger Sets Input Validation

Input shape belongs here; policy belongs in ora_design_enforcement.md and resolver mechanics in ora_reference_lookups.md.

## User Business Fields

| Field | Required | User Options and Handling |
|---|---|---|
| Operation | Yes | Create, review, or update. Reject deletion of an existing ledger set, including delete-and-recreate, purge, reset, rollback-by-deletion and test cleanup, before preparing any action. Membership changes are explicit add/remove deltas; omission preserves existing assignments and member removal must preserve the set. |
| Name | Yes | Nonblank, unique across ledgers and ledger sets for create; maximum 30 characters. For update/review also provide the stable resolved LedgerSetId when available. |
| Description | No | Maximum 240 characters. Omission on update preserves the existing value; an explicit clear is distinct from omission. |
| Classification | No on create | Offer None for processing, Currency-specific for same-currency reporting, or GAAP view for one primary and its eligible secondary ledgers. FSM codes are blank, ORA_GL_CURRENCY_SPECIFIC, ORA_GL_GAAP_VIEW. Omission defaults to None; show that choice in the preview. |
| Chart of Accounts | Resolved value required on create; user selection optional | Accept an exact display selection or use the declared resolver with the common member ChartOfAccountsId. Resolve the same-release StructureInstanceCode; do not treat a display label as an import code. |
| Accounting Calendar | Exact display selection required under the current resolver contract | Resolve PeriodSetName and AccountedPeriodType separately. If the display selection is omitted, request it; the member's internal period-set name is not an automatic display-name mapping. |
| Currency | Yes for either nonblank classification | Offer enabled monetary currencies compatible with all effective members. A single shared member currency may be proposed for approval; never choose one for mixed-currency members. Use LedgerSetCurrencyCode, not the legacy CurrencyCode placeholder. |
| Default Ledger | No | Exact eligible member ledger. Blank initially is valid; omission preserves the existing default on update. |
| Descriptive flexfields | Conditional | Enabled context and segment requirements are tenant-specific. Preserve omitted values, validate explicitly supplied values using deployed DFF metadata, and distinguish clear from preserve. |
| Ledger Set Assignments | Yes for submission | At least one resolved ledger or ledger set. Resolve members through the declared endpoints/current task data and prepare explicit assignment rows before Data Loader handoff. |
| Source package and candidate package | Yes for FSM writes | Framework obtains the current template and applies packaged MLS_FSM_CREATE_V1 for create; acquire a selected-object baseline for update when required. User does not supply a profile, test receipt or full ledger-set export. |

## Additional FSM Creation Input

| Field | Required | User Options and Handling |
|---|---|---|
| ShortName | Resolved value required unless a supported importer allocation is established | Advanced FSM input. Accept an explicit unique value of at most 20 characters. If omitted, use the packaged Name-based derivation only after a separate short-name duplicate check. For a longer Name or collision, request or propose a distinct short name; do not silently truncate. |
| Technical create profile | Built-in framework rule | Use packaged MLS_FSM_CREATE_V1 and validate the current template's field/type contract. New projects do not need an external profile or previous controlled-create evidence. |

Collect Name and at least one member as the main creation choices. Accept a supplied COA or resolve it from member evidence; request an omitted calendar display selection under the current calendar contract. Offer Description, Classification, Default Ledger and deployed DFF values as optional or conditional choices. Structure codes, period type, segment metadata and L/S member type are resolved from the chosen objects rather than asked as unrelated options. When a lookup produces multiple eligible structures or calendars, let the user choose instead of selecting an arbitrary match. Do not advertise a fully automatic Name/member-only flow until the missing calendar-resolution behavior is declared and qualified.

The framework also needs the selected project/environment and the executor's approval of the final immutable package. It obtains current template shape, fresh reference results and the primary-ledger-scoped export through the declared workflow. The packaged profile is already part of the skill. Do not ask for a full Manage Ledger Sets export or inspect another project's runs. A COA populated export is conditional on a named required structural gap and requires separate disclosure/approval; it is not an ordinary creation input or prerequisite.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Task and environment | Operation, selected environment, GL_MANAGE_LEDGER_SETS, current source package | Block task validation | Select the exact environment and obtain a current same-release task package through the routed exporter | All FSM writes | inspect_ledger_set_package |
| Ledger set identity | Name and optional stable LedgerSetId | Block | Supply exact identity; create and update have different match requirements | All operations | find_ledger_set_by_exact_name |
| FSM short identity | Explicit or packaged derived ShortName | Block unresolved allocation, overlength or collision | Resolve a distinct short name independently of the set Name | FSM create with an explicit or derived short name | find_ledger_set_by_exact_short_name |
| Shared accounting structure | ChartOfAccountsId, StructureInstanceCode, PeriodSetName, AccountedPeriodType | Block | Resolve labels to exact structure and calendar keys using member lookup and designated source evidence | Create or requested structural change | find_ledger_by_exact_name |
| COA import identity | Selected COA Name, StructureInstanceCode, StructureInstanceNumber | Block unresolved or mismatched instance | Resolve through the declared COA endpoint; do not require another ledger set's exported row | Create or requested structural change | resolve_ledger_set_chart_of_accounts |
| Calendar import identity | UserPeriodSetName, PeriodSetName, PeriodType | Block unresolved or mismatched calendar | Resolve through the declared calendar endpoint and match member period types | Create or requested calendar change | resolve_ledger_set_accounting_calendar |
| Structural metadata | Allowlisted structural values from the resolved primary's scoped export and packaged field dispositions | Acquire through the primary-scoped route; conditional COA export only for a named required gap | Match exact primary row and cross-check selected references; no existing ledger-set profile is required | FSM create | resolve_ledger_set_structural_profile |
| Intended membership | At least one final member, with explicit additions/removals for update | Block | Supply final membership or an unambiguous delta against current membership | Create and membership update | inspect_ledger_set_evidence |
| Classified currency | Currency code | Block | Select an enabled monetary currency when Classification is Currency-specific or GAAP view | Classified create or update | resolve_ledger_set_currency |
| DFF context contract | Deployed context, segment mapping, types and value-set evidence | Block only supplied or required DFF fields | Obtain current enabled DFF metadata; do not guess labels-to-Attribute mappings | DFF changes | inspect_ledger_set_evidence |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Name shape | Require a nonblank Name | Supplied fields |  |
| Operation and classification enum | Reject unknown operations or classification labels/codes; normalize blank to None only on create | All |  |
| Framework execution route | Only declared FSCR endpoint clients, exporters, Data Loader and explicitly configured metadata/report adapters may perform checks or task operations. Reject a requested UI execution route as input_validation with reason ui_execution_prohibited; UI screenshots/grid extracts do not supply required runtime evidence | All requests and delegated execution |  |
| Existing-set deletion intent | Reject an explicit or deletion-equivalent request to remove an already-created set; return input_validation with reason ledger_set_deletion_prohibited before deletion-related lookup/export, package preparation or execution. General test/import approval does not permit it | All requests, including cleanup, reset, rollback and delete-and-recreate |  |
| Delta shape | Require unique member identities, disjoint add/remove lists, and a final nonempty list; do not interpret an omitted list as remove-all | Create or membership update |  |
| Package syntax | Require exact member names, ordered headers, row widths, UTF-8 CSV quoting, matching metadata XML and valid parent-child keys. Commas, double quotes and embedded newlines must survive CSV encoding/decoding as one logical field; physical line counts are not record counts | FSM candidate preparation | inspect_ledger_set_package |
| Independent length boundaries | Accept values exactly at the documented 30-character Name, 20-character ShortName and 240-character Description limits; reject overlength values before upload. Validate the logical string, including embedded newline characters, without silent truncation | Supplied or derived fields |  |
| FSM create profile | Apply the packaged field partition and validate every current template column/type. Reject unclassified columns, incompatible types, unresolved required values and primary-ledger settings used as set defaults. No external qualification receipt is required. If supplied or derived, ShortName must be nonblank and at most 20 characters with its own negative precheck | FSM create | resolve_ledger_set_create_profile |
| Update preservation | Require presence/clear/omit distinctions and preserve all nonrequested exported fields | Update | inspect_ledger_set_package |
| Dates and DFF types | Follow the same-release XML type contract for supplied dates, numbers, context and segments; no invented status/date/default codes | Supplied values | inspect_ledger_set_evidence |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Input shape is valid | Continue | Run fresh identity/member lookups, validate current template shape and acquire primary-ledger-scoped structural evidence; a new project is not a failure |  |
| Input shape or package is invalid | Blocked | Correct the identified field or file before any upload |  |

Business input requiredness and FSM create requiredness are separate contracts. Review ShortName, legacy CurrencyCode, LedgerCategoryCode, AlcLedgerTypeCode, LeLedgerTypeCode, FirstLedgerPeriodName, ledger-set flags and other technical columns against current framework create evidence. Database not-null declarations identify investigation candidates; they do not prove that every corresponding CSV cell must be populated, because supported importer defaults and derivations may exist. Do not equate ZIP/header validation with a complete server-side create contract.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MLS.VALIDATE_INPUT | step | 10 | validate_input | valid->MLS.RESOLVE_REFERENCES;invalid->MLS.HANDLE_ERROR | none | stop | All requested operations; reject UI execution and existing-set deletion intent locally before action preparation. Data Loader Task Hook validates the exact prepared candidate before upload. |
