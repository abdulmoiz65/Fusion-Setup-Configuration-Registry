# Picking Rules Input Validation

## Source Evidence

| Source | Used For |
|---|---|
| Developer-provided Data Loader business-object record | RuleName is mandatory on create and is owned by Data Loader and Fusion validation |
| Redwood Picking Rules page | Priority fields can be supplied through display-value LOV controls |
| Redwood rules-page.js payload builder | Selected checkbox values for EnabledFlag, PartialAllowedFlag, SingleLotFlag, AllocateLPNFlag, and LPNLocationOnlyFlag map to true; empty selections map to false when the field is included by the UI |
| User approval | Normalize every supplied boolean flag locally and do not verify LPN flags through REST |
| Verified Picking Rules FSM template | FSM columns use native `Y` or `N` flag values; the `PartialAllowedFlagBoolean` and `SingleLotBoolean` companion columns use `true` or `false` |

## Scope Boundary

| Boundary | What Happens |
|---|---|
| Backend-owned validation | Data Loader and Fusion own required fields, uniqueness, lengths, server-side domains, and final field enforcement |
| Local validation ownership | For REST, normalize approved Redwood checkbox representations and trimmed case-insensitive `Y` or `N` literals for every supplied boolean flag. For FSM, preserve native `Y` or `N` values and validate supplied companion booleans for consistency. Do not perform REST verification for AllocateLPNFlag or LPNLocationOnlyFlag |
| Priority display values | REST may resolve a supplied display Meaning to LookupCode. FSM preserves supplied priority values unchanged. |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Picking Rule name | RuleName | Leave required-field enforcement to Data Loader and Fusion | Supply RuleName according to Data Loader metadata | Create | |
| REST boolean checkbox representation | EnabledFlag, PartialAllowedFlag, SingleLotFlag, AllocateLPNFlag, or LPNLocationOnlyFlag as true or false, selected checkbox token, empty checkbox selection, or trimmed case-insensitive `Y` or `N` | Stop when a supplied representation is neither a canonical boolean string, an observed checkbox representation, nor `Y` or `N` | Supply true or false, a selected checkbox token, an empty checkbox selection, or `Y` or `N` | REST route and one or more supported boolean fields are supplied | |
| FSM boolean representation | EnabledFlag, PartialAllowedFlag, SingleLot, AllocateLPNFlag, or LPNLocationOnlyFlag as Y or N; PartialAllowedFlagBoolean or SingleLotBoolean as true or false when supplied | Stop when a native FSM flag is not Y or N, or a supplied companion Boolean conflicts with its corresponding FSM flag | Supply Y or N and use the matching true or false companion Boolean | FSM route and one or more supported boolean fields are supplied | |
| FSM priority sort | Priority1Sort, Priority2Sort, Priority3Sort, or Priority4Sort | No task-local priority requirement | Preserve the supplied native value unchanged | FSM route and one or more priority fields are supplied | |
| FSM template contract | A discoverable project-local template and task-local receipt, with `ASM_SETUP_CSV_METADATA.xml`, `ORA_INV_RULE.csv`, `INV_RULE_SELECTION_CRITERION.csv`, and `ORA_INV_RULE_TRANSLATION.csv` | Stop before package authoring | Reuse a verified empty template and receipt or obtain one through the approved task-level template/spec export workflow | FSM route | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A REST Priority1Sort, Priority2Sort, Priority3Sort, or Priority4Sort display Meaning is supplied | Continue after the display value resolves exactly once to LookupCode | Pass the canonical LookupCode to Data Loader | resolve_picking_rule_priority |
| A REST priority field is supplied as a canonical LookupCode only | Continue without display-value conversion | Pass the supplied canonical code to Data Loader | |
| An FSM priority field is supplied | Preserve it without local lookup, normalization, or display-value validation | Pass the supplied value unchanged to Data Loader | |
| A supported boolean field is supplied as a selected checkbox token | Continue after filling the corresponding field with true | Pass the canonical boolean string to Data Loader | |
| A supported boolean field is supplied as an empty checkbox selection | Continue after filling the corresponding field with false | Pass the canonical boolean string to Data Loader | |
| A supported boolean field is supplied as canonical true or false | Continue without changing the supplied canonical value | Pass the canonical boolean string to Data Loader | |
| A supported REST boolean field is supplied as `Y` or `N` | Normalize trimmed, case-insensitive `Y` to true and `N` to false | Pass the canonical boolean string to Data Loader | |
| Native FSM boolean fields are supplied | Preserve the supplied Y or N values; do not apply REST checkbox normalization | Pass the native FSM values to Data Loader | |
| FSM Boolean companion fields are supplied | Continue when PartialAllowedFlagBoolean and SingleLotBoolean correspond to their Y or N FSM flag values | Pass the supplied companion Boolean to Data Loader | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| REST priority display-value conversion | Resolve a supplied Meaning through the approved read-only lookup and fill the matching LookupCode | REST priority display Meaning is supplied | resolve_picking_rule_priority |
| FSM priority preservation | Preserve the supplied value; do not resolve, normalize, or validate it locally | FSM priority field is supplied | |
| REST boolean normalization | Convert a selected checkbox token or trimmed case-insensitive `Y` to true; convert an empty checkbox selection or trimmed case-insensitive `N` to false; preserve canonical true or false | Before Data Loader handoff on the REST route when EnabledFlag, PartialAllowedFlag, SingleLotFlag, AllocateLPNFlag, or LPNLocationOnlyFlag is supplied | |
| FSM boolean preservation | Preserve native Y or N for EnabledFlag, PartialAllowedFlag, SingleLot, AllocateLPNFlag, and LPNLocationOnlyFlag; do not convert them to REST boolean strings | Before Data Loader handoff on the FSM route | |
| FSM companion consistency | Reject a supplied PartialAllowedFlagBoolean or SingleLotBoolean that does not correspond to its native Y or N FSM flag | Before Data Loader handoff on the FSM route when a companion Boolean is supplied | |
| FSM template eligibility | Require one discoverable template and receipt; exactly one metadata marker; task code `ORA_PICKING_RULES`; compatible target environment and release; matching ZIP fingerprint; the three native CSV members with exported headers; and no data rows before authoring | Before FSM package authoring | |
| FSM package preservation | Preserve metadata XML, CSV headers, encoding, member names, and empty child CSVs; add only the approved `ORA_INV_RULE.csv` row | Before Data Loader handoff on the FSM route | |
| Unsupported boolean representation | Reject a REST value other than a selected checkbox token, an empty checkbox selection, true, false, `Y`, or `N`; reject an FSM flag other than Y or N | A supported boolean field is supplied on its selected route | |
| Conflicting boolean representation | Reject values that express more than one state for the same supported boolean field | More than one representation is supplied for one supported boolean field | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PICKRULES.CLASSIFY_IMPORT_ROUTE | step | 5 | validate_input | rest->PICKRULES.NORMALIZE_BOOLEAN_FLAGS;fsm->PICKRULES.VALIDATE_FSM_ARCHIVE;blocked->PICKRULES.RETURN_ISSUES | none | stop | Every request. REST is the task default; FSM applies only to an explicitly selected package or an archive containing `ASM_SETUP_CSV_METADATA.xml`. |
| PICKRULES.NORMALIZE_BOOLEAN_FLAGS | decision | 10 | validate_input | valid->PICKRULES.CHECK_DEPENDENCIES;invalid->PICKRULES.RETURN_ISSUES | PICKRULES.CLASSIFY_IMPORT_ROUTE | stop | Classified REST requests with one or more supported boolean fields. |
| PICKRULES.VALIDATE_FSM_ARCHIVE | step | 11 | validate_input | validated->PICKRULES.CHECK_FSM_READINESS;blocked->PICKRULES.RETURN_ISSUES | PICKRULES.CLASSIFY_IMPORT_ROUTE | stop | Classified FSM package. Validate the native member/header and boolean contract; do not apply REST priority or boolean transformations. |
