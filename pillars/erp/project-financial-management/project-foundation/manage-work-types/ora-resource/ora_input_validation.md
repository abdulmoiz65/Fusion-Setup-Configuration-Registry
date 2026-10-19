# Input Validation

## CSV Column Intent Resolution

| CSV Column | User Intent |
|---|---|
| PJF_PROJECT_WORK_TYPE.csv.Name | Work Type |
| PJF_PROJECT_WORK_TYPE.csv.Attribute1 | Additional Information — descriptive flexfield segment 1; deployed label requires target metadata |
| PJF_PROJECT_WORK_TYPE.csv.Attribute10 | Additional Information — descriptive flexfield segment 10; deployed label requires target metadata |
| PJF_PROJECT_WORK_TYPE.csv.Attribute11 | Additional Information — descriptive flexfield segment 11; deployed label requires target metadata |
| PJF_PROJECT_WORK_TYPE.csv.Attribute12 | Additional Information — descriptive flexfield segment 12; deployed label requires target metadata |
| PJF_PROJECT_WORK_TYPE.csv.Attribute13 | Additional Information — descriptive flexfield segment 13; deployed label requires target metadata |
| PJF_PROJECT_WORK_TYPE.csv.Attribute14 | Additional Information — descriptive flexfield segment 14; deployed label requires target metadata |
| PJF_PROJECT_WORK_TYPE.csv.Attribute15 | Additional Information — descriptive flexfield segment 15; deployed label requires target metadata |
| PJF_PROJECT_WORK_TYPE.csv.Attribute2 | Additional Information — descriptive flexfield segment 2; deployed label requires target metadata |
| PJF_PROJECT_WORK_TYPE.csv.Attribute3 | Additional Information — descriptive flexfield segment 3; deployed label requires target metadata |
| PJF_PROJECT_WORK_TYPE.csv.Attribute4 | Additional Information — descriptive flexfield segment 4; deployed label requires target metadata |
| PJF_PROJECT_WORK_TYPE.csv.Attribute5 | Additional Information — descriptive flexfield segment 5; deployed label requires target metadata |
| PJF_PROJECT_WORK_TYPE.csv.Attribute6 | Additional Information — descriptive flexfield segment 6; deployed label requires target metadata |
| PJF_PROJECT_WORK_TYPE.csv.Attribute7 | Additional Information — descriptive flexfield segment 7; deployed label requires target metadata |
| PJF_PROJECT_WORK_TYPE.csv.Attribute8 | Additional Information — descriptive flexfield segment 8; deployed label requires target metadata |
| PJF_PROJECT_WORK_TYPE.csv.Attribute9 | Additional Information — descriptive flexfield segment 9; deployed label requires target metadata |
| PJF_PROJECT_WORK_TYPE.csv.AttributeCategory | Additional Information — descriptive flexfield context |
| PJF_PROJECT_WORK_TYPE.csv.BillableCapitalizableFlag | Billable |
| PJF_PROJECT_WORK_TYPE.csv.Description | Description |
| PJF_PROJECT_WORK_TYPE.csv.EndDateActive | To Date |
| PJF_PROJECT_WORK_TYPE.csv.StartDateActive | From Date |
| PJF_PROJECT_WORK_TYPE.csv.TpAmtTypeCode | Transfer Price Amount Type |
| PJF_PROJECT_WORK_TYPE.csv.UtilizableFlag | Utilizable |
| PJF_PROJECT_WORK_TYPE_ST.csv.PJF_PROJECT_WORK_TYPE.Name | Parent work type name |
| PJF_PROJECT_WORK_TYPE_ST.csv.SetCode | Resolved assigned-set code; derive from SetName unless the user explicitly supplies a code |
| PJF_PROJECT_WORK_TYPE_TRANSLATION.csv.PJF_PROJECT_WORK_TYPE.Name | Parent work type name |
| PJF_PROJECT_WORK_TYPE_TRANSLATION.csv.Description | Translated description |
| PJF_PROJECT_WORK_TYPE_TRANSLATION.csv.Language | Translation language |
| PJF_PROJECT_WORK_TYPE_TRANSLATION.csv.Name | Translated work type name |
| PJF_PROJECT_WORK_TYPE_TRANSLATION.csv.SourceLang | Source language for translation |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | create, update, validate, export, import, end_date | Block | Ask for supported intent; delete unproven | Every request |  |
| Identity | Work Type name, optional stable ID or evidenced alternate wording | Block | Resolve one existing identity or preserve the requested new name | Every write | find_work_type |
| Base | StartDateActive (From Date), optional EndDateActive (To Date), BillableCapitalizableFlag (Billable), UtilizableFlag (Utilizable), TpAmtTypeCode (Transfer Price Amount Type); accept prior business aliases | On create, allow omitted StartDateActive, Billable and Utilizable to reach WTYPE.APPLY_DEFAULTS; block other missing required values without a confirmed default | Resolve the intended CSV column first; preserve explicit values and apply ora_defaulting_rules.md at WTYPE.APPLY_DEFAULTS; preserve omitted fields on update | Create/update |  |
| Set assignments | Optional set names; codes only when explicitly labeled as set codes by the user | Omitted on create: continue without a set question or invented assignment; omitted on update: preserve baseline | Resolve only supplied or explicitly changed assignments through resolve_work_type_sets; derive canonical SetCode for a unique name. Check target CSV child-member requirements separately through verify_work_type_package | Set supplied or explicitly changed | resolve_work_type_sets |
| Translations/DFF | Explicit language rows and supplied DFF CSV fields in their proven representation | Preserve omitted | Resolve supported fields; disclose unavailable DFF membership/requiredness checks without requiring manual metadata or a waiver | Child/DFF change | resolve_work_type_children |
| Target/artifacts | TargetEnvironment, current_export, package_template | Block | Obtain current target evidence | Every write | verify_work_type_package |
| Consumer-impact handoff | work_type_use_evidence supplied through captured caller context | Block affected import preparation when absent | Validate through the owning resolver; input presence alone does not establish authority or completeness | Existing identity with an actual flag/transfer, availability-date or set-assignment diff | resolve_work_type_use |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Unique resolved name with valid dates | Satisfied | Create/update | find_work_type |
| Set assignment supplied/removed | Conditional | Resolve unique sets; apply assignment preservation in design enforcement | resolve_work_type_sets |
| Existing identity with an actual flag/transfer, availability-date or set-assignment diff | Required dependency | Require the owning resolver's satisfied result; missing/invalid evidence is blocking and cannot use REFERENCE_UNRESOLVED | resolve_work_type_use |
| Translation rows supplied | Conditional | Acquire the language catalog through the declared REST read and resolve each field | resolve_work_type_languages |
| Delete requested | Refused | End-date if safe | resolve_work_type_use |
| Create or DFF change requested; supported deployed metadata authority unavailable | REFERENCE_UNRESOLVED; Warning; blocking=false | Preserve supplied proven CSV representation, disclose skipped membership/requiredness checks, and continue all supported checks and preview; ask only if actual ambiguity or missing representation prevents construction | resolve_work_type_dff_context |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Nonblank work-type name resolving to the intended identity | Preserve authored text; do not impose English or exact-label input | Create/update | find_work_type |
| StartDateActive <= EndDateActive when end date is supplied | Accept; else reject; use the target FSM date representation. If the create start date is omitted, defer the comparison until WTYPE.APPLY_DEFAULTS materializes it; reject a resulting invalid range before preview | Dates supplied/defaulted |  |
| Billable and Utilizable each resolve to their checkbox domain | Accept codes, booleans, translated meanings or unambiguous ordinary wording; write each resolved CSV flag | Supplied/defaulted | resolve_work_type_boolean |
| Transfer Price Amount Type resolves to one valid member | Accept code, meaning, translation or unambiguous ordinary wording; write canonical TpAmtTypeCode | Supplied/defaulted | resolve_work_type_transfer_type |
| Set resolves uniquely to canonical SetCode | Unqualified values and SetName fields are names; only explicit code wording or user-authored SetCode/assigned_set_code fields are code inputs. Do not infer code intent from spelling or an agent-generated CSV column. Duplicate resolved assignments are invalid | Set change | resolve_work_type_sets |
| DFF validation evidence | Missing supported metadata is REFERENCE_UNRESOLVED, Warning, blocking=false; preserve proven CSV fields and continue supported validation/preview with skipped checks disclosed. Never invent a context code, segment label, column mapping or required value from unresolved prose | Create or AttributeCategory or Attribute1 through Attribute15 changed | resolve_work_type_dff_context |
| Translation Language and SourceLang resolve to Fusion language identities | Both required; published VARCHAR2 length 4 each; duplicate parent plus Language rows invalid; preserve translated text and source-language intent. Installation/activation state alone does not prove import eligibility; unresolved parity is a nonblocking warning | Translation rows supplied | resolve_work_type_languages |
| Translated Name plus Language is unique across work types | Require the owning child resolver's collision-free result before preview; a collision or incomplete required check is blocking, distinct from optional DFF/eligibility warnings | Translation rows supplied | resolve_work_type_children |
| Name and translated Name required; published VARCHAR2 length 240; Description length 2000 | Preserve supplied text and its language; validate against the documented storage limits and confirmed target serialization semantics; see Source Evidence below | Base/translation fields supplied |  |
| AttributeCategory published VARCHAR2 length 30; each Attribute1 through Attribute15 length 150 | Enforce evidenced storage/deployed constraints; these outer lengths do not prove deployed DFF membership or requiredness; unknown encoding/length semantics remain disclosed, never a claim of full validation | DFF fields supplied | resolve_work_type_dff_context |
| Child parent reference identifies the intended work type | PJF_PROJECT_WORK_TYPE.Name in each child CSV must reference the resolved base Name; do not replace it with translated Name | Set/translation rows supplied | find_work_type |
| Exact package members/headers | Accept; else reject | Import | verify_work_type_package |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WTYPE.VALIDATE_INPUT | step | 1 | validate_input | valid->WTYPE.APPLY_DEFAULTS;warning->WTYPE.APPLY_DEFAULTS;invalid->WTYPE.RETURN_ISSUES | none | stop | Every Manage Work Types request; retain nonblocking warnings while completing supported checks |
| WTYPE.ROUTE_OPERATION | decision | 5 | evaluate_result | supported->WTYPE.RESOLVE_DEPENDENCIES;unsupported->WTYPE.RETURN_REFUSAL;invalid->WTYPE.RETURN_ISSUES | WTYPE.RESOLVE_CHILDREN | stop | After identity/set/child/use resolution |

## Source Evidence

Reviewed on 2026-10-08. Sources below are Oracle's latest published release 26D table references, reached through the 26D Tables and Views documentation contents. Table documentation establishes storage facts; it does not independently establish FSM column mapping, blank-cell semantics or task-specific import eligibility. Validate those against the selected workflow's current target package/template.

| Validation fact | Source and locator | Evidence boundary |
|---|---|---|
| Required StartDateActive and independent billable/utilizable fields; optional EndDateActive | [PJF_WORK_TYPES_B, 26D](https://docs.oracle.com/en/cloud/saas/project-management/26d/oedpp/pjfworktypesb-25294.html), START_DATE_ACTIVE, BILLABLE_CAPITALIZABLE_FLAG, UTILIZABLE_FLAG, END_DATE_ACTIVE | Required storage does not prove a UI/import default. Start <= End is this task's availability design gate |
| AttributeCategory length 30; Attribute1 through Attribute15 length 150 | PJF_WORK_TYPES_B, ATTRIBUTE_CATEGORY and ATTRIBUTE1 through ATTRIBUTE15 | Outer storage only; deployed DFF rules remain subject to the existing unresolved-authority warning |
| Name length 240 and required; Description length 2000 | [PJF_WORK_TYPES_TL, 26D](https://docs.oracle.com/en/cloud/saas/project-management/26d/oedpp/pjfworktypestl-25298.html), NAME and DESCRIPTION | Base/translated serialized names must follow the current target FSM contract; do not derive a label or translation from the table |
| Language and SourceLang length 4 and required; distinct semantics | PJF_WORK_TYPES_TL, LANGUAGE and SOURCE_LANG | Catalog identity comes from the declared language read; table storage does not prove import eligibility or permit inferring SourceLang |
| Unique work type plus translation language | PJF_WORK_TYPES_TL, primary key WORK_TYPE_ID + LANGUAGE | Resolve the serialized parent Name to its base identity before checking child uniqueness |
| Unique translated name plus language across work types | PJF_WORK_TYPES_TL, unique index PJF_WORK_TYPES_TL_U2 on NAME + LANGUAGE; reviewed 2026-10-12 | Independent of parent/language uniqueness. Collision-check mechanics belong to resolve_work_type_children; target comparison and FSM execution semantics require their own evidence |
| Unique work type plus reference set | [PJF_WORK_TYPES_B_ST, 26D](https://docs.oracle.com/en/cloud/saas/project-management/26d/oedpp/pjfworktypesbst-25297.html), unique index WORK_TYPE_ID + SET_ID | Supports duplicate-assignment rejection. The index does not require assignments on create or prohibit final-assignment removal; validate explicit changes and consumer impact separately |

The table pages report VARCHAR2 lengths without establishing the target's byte-versus-character serialization behavior. Do not reject multilingual text merely by counting bytes under an assumed encoding. Apply confirmed target length semantics; disclose any remaining unperformed check. The static transfer/flag mappings have the separate evidence boundary in ora_reference_lookups.md.
