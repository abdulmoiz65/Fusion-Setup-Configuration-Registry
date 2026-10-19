# Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_apply_flow_export | AF.LOAD_EXPORT_CACHE and AF.RESOLVE_REFERENCES | Immutable selected-environment task export from shared.setup-export.task-level-export for ORA_IRC_APPLY_FLOW_CONFIGURATION | Validate environment/release, complete carrier and archive evidence; retain all root/version rows for later branch selection, without deriving source-dependent defaults or applying Retrieve filters | Complete exported root/version data, carrier reference, checksum, timestamp, release | Missing/stale/wrong-environment evidence requires the declared export workflow at runtime; malformed archive is an artifact issue, not an empty result |
| resolve_apply_flow_identity | AF.RESOLVE_SOURCE_FLOW, AF.RESOLVE_PARENT_FLOW; new-identity validators consume exported evidence | Root rows from resolve_apply_flow_export; exact source/parent or new-target identity | Source/parent: exactly one exact AfCode; optional source name must match that same row exactly. New target: AfCode and ApplyFlowName must each be absent | Selected root and inherited type, or target conflict evidence | Missing source/parent is MISSING; many are AMBIGUOUS; existing new-target code/name is CONFLICT. Show exact value/candidates, never reuse or overwrite |
| resolve_apply_flow_version | AF.RESOLVE_SOURCE_VERSION or AF.RESOLVE_PARENT_FLOW | Complete ORA_IRC_JOB_AF_VERSION.csv rows and the exact selected source/parent AfCode | Template: exact requested VersionName requires one eligible Active/Draft match; otherwise unique Active, or only if no Active, unique Draft; exclude inactive. Parent: retain every existing name including inactive for later default/conflict checks | Exactly one selected template version and its hierarchy, or complete parent version-name set | Missing/inactive requested version: ask without fallback. Multiple exact/preferred candidates: show code/name/version/status and ask. Never infer latest from date, sequence, row order or name |
| resolve_apply_flow_version_conflict | AF.VALIDATE_VERSION_CONFLICT | Complete exported version rows; final target AfCode and VersionName | Exact target pair must be absent, including inactive versions | Unique new version identity or exact conflict | Any match is CONFLICT; request a new VersionName, never overwrite or auto-rename an explicit value |
| resolve_apply_flow_type | AF.RESOLVE_REFERENCES makes static authority available; AF.VALIDATE_FLOW_TYPE and AF.FILTER_RETRIEVE consume it | Developer-supplied local Application Flow Types table below | Creation: trim and case-insensitive exact code or whole Meaning, persist canonical supported code; no partial/fuzzy match. Retrieve filter: exact supported AfTypeCode equality | Canonical type, business label and support result | Show four supported meanings/codes for unsupported creation/filter input; no REST. Unfiltered retrieval may include internal root rows |
| resolve_apply_flow_block | AF.RESOLVE_REFERENCES makes inventory available; block construction, title defaulting and block design validators consume it | Developer-supplied local Canonical Block Inventory below and every candidate block instance | Require exactly one exact supported BlockCode row with a nonblank BlockName; split BLOCK_USAGE_CODE on commas, trim tokens and compare exact AfTypeCode; Y permits reuse, N one per complete version | Exact BlockName as the default PageBlockTitle source, canonical business names, support, applicability and reuse evidence | Missing/duplicate code or blank BlockName blocks title resolution; never derive a display name by splitting BlockCode. Unknown/unsupported/inapplicable code or nonreusable repeat: show value/positions and supported choices |
| resolve_apply_flow_languages | AF.RESOLVE_TRANSLATIONS | Distinct non-empty Language values across every exported translation CSV in the immutable target task export; cache and evidence keyed by environment/release | Use US base and the union of exported Language codes; refresh routed export evidence when missing or either cache key changes; require requested Language and corresponding required US base text | Available code set, US base, operation-specific translation plan and exact entity/field overrides | Unavailable Language: show codes and ask. Missing required US record/text after applicable title defaulting: name it and ask, never guess. Only optional Description and PageBlockInstructions may intentionally remain empty; PageBlockTitle must be nonblank |
| resolve_apply_flow_availability | AF.COPY_SUPPORTED_TEMPLATE_HIERARCHY and AF.RESOLVE_RECRUITING_TYPE for External template copies | Selected source root availability and Recruiting Type children from the same verified export | Exact selected AfCode and parent-child linkage; distinct RecruitingTypeCode associations; no source IDs carried to target | Distinct source External associations and available verified Meaning evidence | Empty associations is an empty set; ambiguous linkage is an artifact issue. No non-External copy; CreateVersion parent associations are unchanged evidence only |
| verify_apply_flow_route | AF.VERIFY_TASK_ROUTE | Existing nested metadata and routed task-catalog preflight evidence | Exact task code/name, Recruiting / Candidate Experience; CSVExportImportSupportedFlag=Y and declared shared.setup-export.task-level-export route | Task identity and export support | Missing/ambiguous identity or unsupported flag blocks; no substitute route |
| verify_apply_flow_environment | AF.VERIFY_TASK_ROUTE | Selected workflow environment, routed Auth/export privilege checks and safe destination evidence | One selected target, authorized access and safe durable paths verified by owning workflows | Environment identity and preflight results | Explain failed/missing gate and owning workflow correction; never expose secrets |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_external_recruiting_type | AF.RESOLVE_RECRUITING_TYPE only for explicit Meaning on External DesignNew/CreateFromTemplate, after type/input/environment validation | User-supplied business Meaning; ORA_IRC_RECRUITING_TYPE; target environment current calendar date formatted YYYY-MM-DD | GET /fscmRestApi/resources/latest/commonLookupsLOV; finder=LookupTypeFinder;LookupType=ORA_IRC_RECRUITING_TYPE,ActiveDate=target current YYYY-MM-DD; fields=LookupType,LookupCode,Meaning; onlyData=true; limit=500; offset advances while hasMore=true through all pages | LookupType,LookupCode,Meaning | Trim supplied Meaning and compare case-insensitively by exact whole-value equality against active/effective results for the target date and lookup type; require one result across complete pagination; never partial/fuzzy | LookupCode as RecruitingTypeCode; exact returned Meaning for preview | Zero: show supplied value and available meanings. Multiple: show meanings/codes and require selection. Incomplete/repeated pagination or Auth/transport/API error: stop with correction; never pick arbitrarily |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| All source-backed or static lookups | Only named Local Lookups may consume immutable exported evidence or the developer-supplied static tables; generic reference_lookup execution_route metadata does not authorize REST for these facts |
| AF.RESOLVE_REFERENCES | Make exported roots/versions and static type/block authorities available; no source-dependent defaults. AF.FILTER_RETRIEVE owns filtering after operation routing |
| AF.RESOLVE_SOURCE_FLOW then AF.RESOLVE_SOURCE_VERSION | Select one source root, inherit its type, then one eligible version before copied options, translations, layout or blocks are used; preserve source snapshots for comparison |
| AF.RESOLVE_PARENT_FLOW | Resolve one existing parent, inherit its type and collect all version names before any creation defaults; existing parent identity is required, not a conflict |
| AF.RESOLVE_RECRUITING_TYPE | Reject input for CreateVersion or non-External before any live call. No explicit Meaning means not_supplied with no live lookup; retain distinct copied External associations. Explicit additional type already present is reported, not duplicated |
| AF.RESOLVE_TRANSLATIONS | Resolve languages and exact override targets after source/parent selection. New designs/versions seed US text; templates preserve supported source rows/values/SourceLang, seed missing rows from corresponding US text, then apply explicit overrides only. Carry the plan through final layout/block construction so new/removed/moved instances have correct TL keys |
| Language materialization | Support ApplyFlowName, Description, SectionName, PageName, PageBlockTitle, PageBlockInstructions within operation scope. Seed missing rows with SourceLang=US; explicit language/field overrides set that row SourceLang to its Language and leave other values unchanged; no duplicate entity/language rows. CreateVersion imports no root translations |
| Block-title materialization | Resolve final base PageBlockTitle using ora_defaulting_rules.md before materializing block TL rows; the base block and its US row must agree. For newly constructed blocks, seed every required language from that final US title, then apply valid explicit non-US overrides. Preserve nonblank copied template titles/translations; fill only missing or blank copied titles from the resolved nonblank US title unless explicitly overridden. A fallback-seeded row uses SourceLang=US; explicit overrides use the existing language/field rule. Do not translate, blank, or replace other copied fields implicitly |
| Template target name | Required target ApplyFlowName replaces the root and US root-TL name. Preserve supported non-base source translations unless explicitly overridden; target-key rewrites are mandatory. Do not restore source identity when seeding rows |
| Recruiting Type display evidence | Use verified Meaning mappings from permitted lookup or source evidence; never invent a business Meaning from LookupCode. If required display evidence is unavailable, show the exact code/evidence gap and request correction; no additional undeclared lookup |
| Retrieval | No Recruiting Type lookup, translation generation, new-root restrictions on unfiltered rows, or package construction. Preserve existing exported evidence, including unsupported block codes; creation support restrictions do not filter retrieval results. Empty valid export/filter results are successful zero-row retrieval |
| Inventory freshness | Static Application Flow Types and Canonical Block Inventory are local authority. No source-release identifier or inventory refresh solely for a target release change. Package/language evidence still requires matching target release |
| Authoring | None of these runtime exports/lookups executes while authoring resources |

## Application Flow Types

| AfTypeCode | Meaning | Description | Creation support |
|---|---|---|---|
| ORA_EXTERNAL | Apply | External Flow | Supported |
| ORA_PADC | Request Information - External | External Post Apply Data Capture Flow | Supported |
| ORA_TALENT | Talent Community | Talent Community Flow | Supported |
| ORA_EVENT | Event | Event Flow | Supported |
| ORA_INTERNAL | Internal Apply | Internal flow | Unsupported |
| ORA_PADC_INTERNAL | Internal Request Information | Internal post-apply flow | Unsupported |

## Canonical Block Inventory

This inventory contains blocks supported for new target construction through
this skill.

| BlockCode | BlockName | BLOCK_USAGE_CODE | REUSABLE_FLAG |
|---|---|---|---|
| ORA_ADDRESS | Address | ORA_EXTERNAL,ORA_TALENT,ORA_PADC,ORA_EVENT | N |
| ORA_ASSESSMENT | Assessment | ORA_EXTERNAL | N |
| ORA_CITIZENSHIP_INFO | Citizenship | ORA_EXTERNAL,ORA_INTERNAL,ORA_TALENT,ORA_PADC,ORA_EVENT | N |
| ORA_DISABILITY | Disability | ORA_EXTERNAL,ORA_INTERNAL,ORA_PADC | N |
| ORA_DIVERSITY | Diversity | ORA_EXTERNAL,ORA_INTERNAL,ORA_PADC | N |
| ORA_DOCUMENT_TYPES | Document Types | ORA_EXTERNAL,ORA_INTERNAL,ORA_TALENT,ORA_PADC,ORA_EVENT | Y |
| ORA_DOCUMENTS | Supporting Documents | ORA_EXTERNAL,ORA_INTERNAL,ORA_TALENT,ORA_PADC,ORA_EVENT,ORA_PADC_INTERNAL | N |
| ORA_DQ_QUESTIONS | Job Application Questions | ORA_EXTERNAL,ORA_INTERNAL | N |
| ORA_EDUCATION | Education | ORA_EXTERNAL,ORA_TALENT,ORA_PADC,ORA_EVENT | Y |
| ORA_EVENT_REG_QUESTIONS | Event Registration Questions | ORA_EVENT | N |
| ORA_EXPERIENCE | Experience | ORA_EXTERNAL,ORA_TALENT,ORA_PADC,ORA_EVENT | Y |
| ORA_JA_EXTRA_INFO | Extra Information | ORA_EXTERNAL,ORA_INTERNAL,ORA_PADC,ORA_TALENT | Y |
| ORA_LANGUAGE | Languages | ORA_EXTERNAL,ORA_INTERNAL,ORA_TALENT,ORA_PADC,ORA_EVENT | Y |
| ORA_LICENSE_CERTIFICATES | Licenses and Certificates | ORA_EXTERNAL,ORA_INTERNAL,ORA_TALENT,ORA_PADC,ORA_EVENT | Y |
| ORA_LOCATION_PREFERENCE | Preferred Locations | ORA_EXTERNAL | N |
| ORA_MISC_DOCUMENTS | Miscellaneous Documents | ORA_EXTERNAL,ORA_PADC,ORA_PADC_INTERNAL | Y |
| ORA_NAME_CONTACT_INFO | Contact Information | ORA_EXTERNAL,ORA_TALENT,ORA_PADC,ORA_EVENT | N |
| ORA_PROFILE_IMPORT | Profile Import | ORA_EXTERNAL,ORA_TALENT,ORA_PADC,ORA_EVENT | N |
| ORA_QUESTIONNAIRE | Questionnaire | ORA_PADC,ORA_PADC_INTERNAL | Y |
| ORA_SENSITIVE_PERSONAL_INFO | Sensitive Personal Information | ORA_EXTERNAL,ORA_PADC,ORA_TALENT | N |
| ORA_SKILL | Skills | ORA_EXTERNAL,ORA_INTERNAL,ORA_TALENT,ORA_PADC,ORA_EVENT | Y |
| ORA_SUMMARY | Review | ORA_EXTERNAL,ORA_INTERNAL | N |
| ORA_TAXCREDITS | Tax Credits | ORA_EXTERNAL | N |
| ORA_TIMELINE | Timeline | ORA_EXTERNAL,ORA_INTERNAL,ORA_TALENT,ORA_PADC,ORA_EVENT | N |
| ORA_VETERAN | Veteran | ORA_EXTERNAL,ORA_INTERNAL,ORA_PADC | N |
| ORA_WORK_PREFERENCE | Work Preferences | ORA_INTERNAL,ORA_EXTERNAL,ORA_PADC,ORA_TALENT | N |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AF.RESOLVE_REFERENCES | decision | 40 | reference_lookup | success->AF.ROUTE_OPERATION;failure->AF.HANDLE_ISSUES | AF.LOAD_EXPORT_CACHE | stop | All. Make exported roots, versions and local inventories available. Do not derive source-dependent creation defaults yet. |
| AF.RESOLVE_SOURCE_FLOW | decision | 90 | reference_lookup | success->AF.RESOLVE_SOURCE_VERSION;failure->AF.HANDLE_ISSUES | AF.ROUTE_OPERATION | stop | CreateFromTemplate. Select one exact source AfCode; optional name cross-check; inherit its type. |
| AF.RESOLVE_SOURCE_VERSION | decision | 100 | reference_lookup | success->AF.VALIDATE_TEMPLATE_CONFLICTS;failure->AF.HANDLE_ISSUES | AF.RESOLVE_SOURCE_FLOW | stop | CreateFromTemplate. Resolve one eligible source version before copying options, layout, translations or blocks. Ask on ambiguity; never infer latest. |
| AF.RESOLVE_PARENT_FLOW | decision | 130 | reference_lookup | success->AF.VALIDATE_FLOW_TYPE;failure->AF.HANDLE_ISSUES | AF.ROUTE_OPERATION | stop | CreateVersion. Require one existing parent AfCode; inherit its type and collect all existing version names before defaults. Existing parent code/name is required, not a conflict. |
| AF.RESOLVE_RECRUITING_TYPE | decision | 180 | reference_lookup | resolved->AF.RESOLVE_VERSION_OPTIONS;not_supplied->AF.RESOLVE_VERSION_OPTIONS;blocked->AF.HANDLE_ISSUES | AF.VALIDATE_VERSION_CONFLICT | stop | Creation; live lookup only for explicit External input. Resolve supplied External meaning, otherwise no lookup. Preserve distinct template associations; reject input for CreateVersion/non-External types. |
| AF.RESOLVE_TRANSLATIONS | decision | 200 | reference_lookup | success->AF.RESOLVE_FACTORY_SKELETON;failure->AF.HANDLE_ISSUES | AF.RESOLVE_VERSION_OPTIONS | stop | Creation. Use US base and distinct exported Language values. New designs seed US text; templates preserve existing supported translations and seed missing rows; explicit overrides affect only selected language/field. Resolve the language plan and explicit per-entity overrides now; materialize against the selected layout and final block instances before package validation. |
