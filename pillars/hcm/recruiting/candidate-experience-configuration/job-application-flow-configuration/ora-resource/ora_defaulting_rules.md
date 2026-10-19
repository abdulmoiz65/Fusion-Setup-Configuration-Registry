# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| AfStatusCode | Literal ORA_DRAFT in a new root CSV; no root row for CreateVersion | AF.DEFAULT_STATUSES after AF.VALIDATE_FLOW_TYPE and the selected successful identity/source/parent branch; all four supported creation types | Forced for DesignNew/CreateFromTemplate even if source differs; no supplied non-Draft override; CreateVersion parent unchanged | |
| VersionStatusCode | Literal ORA_DRAFT in the new version CSV | AF.DEFAULT_STATUSES after AF.VALIDATE_FLOW_TYPE; all three creation operations and four supported types | Forced even for an Active template source; no non-Draft override | |
| Description | Empty CSV cell for omitted DesignNew input; selected source Description for template; no root/root-TL row for CreateVersion | AF.DEFAULT_STATUSES after selected-branch identity/type readiness; copied source already resolved for template | Preserve valid DesignNew input and supported explicit translation overrides; no inferred text or CreateVersion parent change | |
| VersionName | Version 1 for a new root; for CreateVersion the lowest positive Version n absent from the resolved complete parent name set, including inactive names; serialize chosen text in every version key | AF.DEFAULT_VERSION_NAME after AF.DEFAULT_STATUSES; all four supported types; AF.RESOLVE_PARENT_FLOW must have supplied the exact parent and complete name set for CreateVersion | Valid supplied nonblank unique name wins; omission alone permits default. Freeze before preview and never regenerate after approval; never truncate, date-name or auto-rename a conflicting explicit value | |
| Version options | Per omitted field only: Factory Option Defaults below for DesignNew/CreateVersion; copied applicable source value for CreateFromTemplate; remaining applicable unassigned value N | AF.RESOLVE_VERSION_OPTIONS after AF.RESOLVE_RECRUITING_TYPE; resolve each supported checkbox independently using input presence, not truthiness | Preserve every explicit applicable uppercase Y or N exactly, including N when the default is Y. Never overwrite a supplied value with factory or copied data. Default only omitted fields; an invalid or blank supplied value is not omission. Inapplicable fields remain empty and supplied inapplicable values are rejected | |
| Option provenance | Retain whether each final applicable option was defaulted, copied or explicitly overridden and its source evidence | AF.RESOLVE_VERSION_OPTIONS for each applicable field after type and baseline resolution | Never infer provenance from equality with a default; hand evidence to preview, not an extra CSV column | |
| Section/page baseline | Exact Factory Skeleton below for DesignNew/CreateVersion; selected source layout for CreateFromTemplate; serialize applicable baseline names and sequences unchanged | AF.RESOLVE_FACTORY_SKELETON after AF.RESOLVE_TRANSLATIONS for all four supported types; template hierarchy must already be copied | Never replace copied layout with factory; no structural/base-name overrides; supported non-base translations and block changes only | |
| Block membership | Factory blocks only when block information is omitted for DesignNew/CreateVersion; selected template blocks when omitted for CreateFromTemplate | AF.RESOLVE_FACTORY_SKELETON; consume Explicit Block Selection in ora_design_enforcement.md before creating block rows | Any explicit block selection replaces the baseline block list, not appends to it. Populate only selected blocks and their translations; do not retain unrequested factory or copied blocks. Preserve the fixed section/page skeleton, including empty pages | |
| Page-block flags | Literal HideInMobileFlag=N and PageBlockRequiredFlag=N in each target page-block row, including template-derived instances | AF.RESOLVE_FACTORY_SKELETON and subsequent block construction on the creation branch after source/factory selection; final package gates verify every instance | Forced target values; no visibility/requiredness overrides | |
| PageBlockTitle | Exact resolved BlockName for every newly constructed block instance when its title is omitted; use the same fallback for missing/blank copied template base titles | Creation baseline and block construction after source/factory and language-plan resolution; applies to DesignNew, CreateVersion and newly added template blocks; final package gates verify base and TL titles | Valid explicit nonblank title wins; otherwise preserve a nonblank copied template title, then use the display-name default. Never overwrite valid custom text, default an explicitly blank title, or emit an empty title. Translation materialization is owned by ora_reference_lookups.md | resolve_apply_flow_block |
| PageBlockInstructions | Empty CSV cell when omitted on a newly constructed block; preserve selected source text for template-derived blocks | Creation baseline and block construction after source/factory and language-plan resolution; final package gates verify materialized values | Explicit supported text and exact language/field overrides win; omission does not clear copied text | |
| Availability identifiers | Frozen distinct uppercase hyphen-free 32-character hexadecimal ObjectCxtCode and ObjectCxtRecTypeCode; a different child identifier per Recruiting Type row; serialize literal identifiers | AF.COPY_SUPPORTED_TEMPLATE_HIERARCHY after selected source and target conflict checks, and AF.RESOLVE_RECRUITING_TYPE after version uniqueness; External new-root associations only | Allocate once before preview; no source-ID reuse, supplied override or regeneration after approval | |
| Availability parent and child values | Literal ObjectTypeCode=ORA_APPLY_FLOW, ObjectCode=target AfCode and DefaultFlag=N; child carries its target parent ObjectCxtCode | Same External association construction nodes after frozen target identity and resolved distinct associations | Forced target values even when source differs; no source identity or DefaultFlag override | |
| Availability associations | DesignNew: resolved selected type only, otherwise both files header-only. Template: distinct source External associations with fresh IDs plus explicit additional type only if absent. CreateVersion: both files header-only | AF.RESOLVE_RECRUITING_TYPE after type/version checks; AF.COPY_SUPPORTED_TEMPLATE_HIERARCHY supplies verified source set for External template | Report deduplication; non-External has no associations; no CreateVersion Recruiting Type input or parent mutation | |

## Default Evaluation Rules

| Situation | What Happens |
|---|---|
| Branch and prerequisites | Evaluate defaults only on the selected creation branch after its successful source/parent/identity checks. Retrieve reaches AF.RETRIEVE_READY without defaulting or creating candidate records. |
| Omitted versus invalid | Only omitted supported input is eligible for a default. Preserve explicit input state; blank VersionName, explicitly blank PageBlockTitle including language overrides, invalid option tokens, unsupported fields or unresolved source values are failures, not omissions to repair. The documented fallback for a missing/blank copied title is not permission to replace explicitly blank user input. Input checks remain owned by ora_input_validation.md. |
| Template precedence | Retain source section/page layout and supported omitted values, but explicit block selection replaces copied membership and explicit applicable Y/N replaces the corresponding copied option. Preserve text/translations only for retained instances; omit descendants of excluded blocks. Never run a global reset-to-factory step. |
| Independent input groups | Block omission and checkbox omission are independent. Specifying checkboxes alone still uses default blocks; specifying blocks alone still defaults omitted checkboxes. Within checkboxes, one supplied value does not suppress defaults for other omitted applicable values. This applies to supported version options, not unsupported block-property or lifecycle overrides. |
| All supported flow types | Apply the same explicit-input precedence to ORA_EXTERNAL, ORA_PADC, ORA_TALENT and ORA_EVENT. Select fallback blocks/options and option applicability using the resolved AfTypeCode; never limit this behavior to Event flows. |
| Consumed constants | Default-value tables are consumed by their named existing nodes and final operation-specific package checks. They do not add nodes, an executor, CSV columns or an external execution route. Translation mechanics remain in ora_reference_lookups.md. |
| Evidence before preview | For each applicable default retain operation/type, completed prerequisite, source value, omitted/copied/explicit input state, final value, override decision and exact CSV representation. Reconcile against final CSVs before preview; show the frozen VersionName and accurate option provenance in the business summary, with detailed evidence separately. |
| Default failure | Stop the affected branch through AF.HANDLE_ISSUES -> AF.RETURN_ISSUES using the field-specific Default Corrections in ora_error_handling.md. Name the field/value, missing prerequisite or valid choices and correction; state actual generation/import status. Never substitute an undocumented value or report ready with missing evidence. |

Translation source discovery, copy/seed rules and SourceLang mapping are owned
by ora_reference_lookups.md. Layout/copy policy is owned by
ora_design_enforcement.md; these tables supply literal defaults, not another
operation or execution route.

## Option Mapping

| Business option | Technical field | Applicable types |
|---|---|---|
| Legal Disclaimer | LegalEnabledFlag | ORA_EXTERNAL,ORA_TALENT,ORA_EVENT |
| E-Signature | EsignEnabledFlag | ORA_EXTERNAL,ORA_PADC |
| Campaign Opt In | OptinEnabledFlag | ORA_EXTERNAL,ORA_PADC |
| Campaign Opt In | TcOptinEnabledFlag | ORA_TALENT |
| One Page Application Flow | SingleClickApplyFlag | ORA_EXTERNAL,ORA_PADC,ORA_EVENT |
| Express Apply | QuickApplyEnabledFlag | ORA_EXTERNAL |

## Factory Option Defaults

| AfTypeCode | EsignEnabledFlag | LegalEnabledFlag | OptinEnabledFlag | QuickApplyEnabledFlag | SingleClickApplyFlag | TcOptinEnabledFlag |
|---|---|---|---|---|---|---|
| ORA_EXTERNAL | Y | Y | Y | N | N | |
| ORA_PADC | Y | | Y | | N | |
| ORA_TALENT | | Y | | | | Y |
| ORA_EVENT | | Y | | | N | |

Empty table cells denote inapplicable fields serialized as empty CSV cells.

## Factory Skeleton

ApplyFlowDefaultVersionFactory is the developer-supplied local authority for
this exact skeleton. Factory section/page identity, counts and sequences stay
fixed; supported translated display text is handled in language rows. The
Factory blocks in order column is a fallback only when block information is
omitted; it is not an instruction to add blocks to an explicit selection.

| AfTypeCode | SectionSeqNum | SectionName | PageName | PageSeqNum | Factory blocks in order |
|---|---|---|---|---|---|
| ORA_EXTERNAL | 1 | Personal Information | Page 1 | 1 | ORA_PROFILE_IMPORT,ORA_NAME_CONTACT_INFO,ORA_ADDRESS |
| ORA_EXTERNAL | 2 | Job Application Questions | Page 1 | 1 | ORA_DQ_QUESTIONS |
| ORA_EXTERNAL | 3 | Experience | Page 1 | 1 | ORA_TIMELINE |
| ORA_EXTERNAL | 4 | More About You | Page 1 | 1 | ORA_DOCUMENTS,ORA_LICENSE_CERTIFICATES,ORA_WORK_PREFERENCE,ORA_LANGUAGE |
| ORA_EXTERNAL | 5 | Summary | Page 1 | 1 | ORA_SUMMARY |
| ORA_PADC | 1 | Personal Information | Page 1 | 1 | none |
| ORA_PADC | 2 | Job Application Questions | Page 1 | 1 | none |
| ORA_PADC | 3 | Experience | Page 1 | 1 | none |
| ORA_PADC | 4 | More About You | Page 1 | 1 | none |
| ORA_TALENT | 1 | Personal Information | Page 1 | 1 | ORA_PROFILE_IMPORT,ORA_NAME_CONTACT_INFO |
| ORA_EVENT | 1 | Personal Information | Page 1 | 1 | ORA_PROFILE_IMPORT,ORA_NAME_CONTACT_INFO |
| ORA_EVENT | 2 | Event Registration Questions | Page 1 | 1 | none |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AF.DEFAULT_STATUSES | step | 150 | apply_default | success->AF.DEFAULT_VERSION_NAME;failure->AF.HANDLE_ISSUES | AF.VALIDATE_FLOW_TYPE | stop | Creation only after selected-branch and type readiness. Apply the Standard Defaults status/Description contract and Default Evaluation Rules; forced new-root/version Draft, copied template Description, unchanged CreateVersion parent. |
| AF.DEFAULT_VERSION_NAME | step | 160 | apply_default | success->AF.VALIDATE_VERSION_CONFLICT;failure->AF.HANDLE_ISSUES | AF.DEFAULT_STATUSES | stop | Creation. Apply the VersionName default only on omission after resolved parent/source; preserve valid supplied text for conflict validation, freeze the chosen name before preview and never regenerate after approval. |
| AF.RESOLVE_VERSION_OPTIONS | step | 190 | apply_default | success->AF.RESOLVE_TRANSLATIONS;failure->AF.HANDLE_ISSUES | AF.RESOLVE_RECRUITING_TYPE | stop | Creation. Preserve each explicit applicable Y/N by field presence; default only omitted options from factory or selected template. Reject invalid input, serialize inapplicable fields empty and retain supplied/defaulted/copied provenance for preview. |
