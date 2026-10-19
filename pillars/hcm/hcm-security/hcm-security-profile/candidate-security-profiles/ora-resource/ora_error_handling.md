# Candidate Security Profiles Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A Name has no matching existing profile | Classify as create. When wording implies an existing-profile update, explain that this Name would create a new profile and obtain clarification before proceeding. Never silently turn a replacement or rename into a create |
| More than one exported header matches the existing profile name | Report ambiguous duplicate header records and stop; do not select a row. Multiple associated detail rows alone are valid |
| An existing criterion value, unsupported setting, or name change is requested | Say: Replacing existing criterion values, changing unsupported settings, or renaming profiles is not supported through this task. Existing profiles support EnabledFlag and supported SecureBy flag updates plus new criterion additions; non-existing names create new profiles. Explain the proposed alternative and obtain clarification before proceeding; do not silently convert or partially execute the request |
| CSP.CHECK_VIEW_ALL rejects an eligible create or update | Say: Creating or updating profiles with View All enabled is not supported through this task. Do not prompt for ViewAllFlag or silently change existing access |
| No active configured and authenticated Fusion environment is available | Stop at the first export gate, generate no configuration rows, and return an environment-configuration error; do not request an environment URL |
| Current-run Candidate Security Profiles export is missing, stale, failed, belongs to another environment or task, or cannot be associated with the active configured environment | Stop at the first export gate, generate no configuration rows, and return an export error after running shared.setup-export.task-level-export against the active configured environment |
| Multiple exported detail rows share the same exact profile Name | Group all associated detail rows under that profile and continue; do not classify the rows as ambiguous |
| Every supplied requested profile and detail value already matches the exported baseline | Return no-op only for allowed intent with unchanged effective flags, identical supplied settings, and no new canonical criteria. Explicit replacement or rename intent must be handled by the change-intent gate, not silently converted to no-op |
| A profile deletion or criterion-entry removal is requested | Return exactly: Deletion of Candidate Security Profile rows is not supported. |
| Conflicting requests or criterion operations | Report the exact conflicting fields, destinations, or source/target entries; request resolution without choosing a winner or silently dropping an operation |
| Security dimension activation lacks a corresponding value | Report the exact profile Name, security dimension flag, and missing corresponding value. Stop before approval/upload and request a value that can pass the existing lookup and validation rules. A value from another profile or dimension is insufficient; do not invent values, resend baseline criteria for flag-only updates, or treat profile EnabledFlag as a security dimension flag |
| Contradictory dimension flag and criteria | Explain the explicit N flag conflicts with the requested criteria; do not silently override it or delete entries |
| No LOV result | After applying the owning resolver's complete sources and eligibility rules, tell the user no eligible value was found and request a corrected term |
| Name is supplied but other configuration fields are omitted | Export and classify first; create defaults apply only to eligible creates. Existing-profile updates preserve omitted settings and all existing criteria. Ask only about invalid input or intent requiring clarification |
| Recruiting Type or Person Type selection is rejected | Explain the specific owning resolver failure; do not impose a shared enabled-only filter or modify lookup definitions |
| Multiple LOV results | Return candidate values and require the user to choose |
| Country lookup has no match or ambiguous matches | Report no exact match or present returned candidates and request selection for ambiguity through resolve_country; do not guess a country code |
| ORA_IRC_CANDIDATE_SECURITY_ENABLED is not Y | Continue FSM package creation, preview, and import; report the setting only when validating post-configuration behavior |
| Candidate Search or Oracle Search is not configured | Continue FSM package creation, preview, and import; report search readiness only when validating post-configuration restrictive-search behavior |
| An activation batch would exceed the enabled-profile limit | Report current total, requested activations, projected total, and limit 20 including the default; block the entire activation batch before approval/upload. Request fewer activations or confirmation of completed disables through a fresh baseline; never silently select a subset |
| The environment is already over capacity and the request does not increase capacity | Disclose the excess and allow disables and other non-capacity-increasing updates through all remaining checks |
| A request is excluded by CSP.PROTECT_SEEDED_PROFILE | Explain: View All Candidates is an Oracle-delivered profile and cannot be modified through this task. Continue unrelated user-configured profiles; if none remain, return the protection result with no package or approval prompt |
| A LOV request returns 401 or 403 | Stop and route to the integration or security owner |
| Unsupported security dimension is requested | Stop that field and do not generate hidden migration fields |
| Import outcome is uncertain | Do not retry automatically; reconcile with a current export and manual UI review |
| Required FSM import behavior, privilege, or idempotency evidence remains unresolved after assessment | Explain the specific missing or conflicting contract evidence and stop before generating affected rows; do not invent execution behavior |
| Malformed outgoing Grade or Business Unit ID | Report exact profile, field, offending representation, and correction required through resolve_grade or resolve_business_unit. Stop before approval/upload; never expand, round, trim, or guess IDs. Existing criterion replacement remains unsupported |
| Malformed baseline-only ID in a flag-only update | Disclose the stored issue separately; do not resend or silently repair it, and do not claim the flag-only update corrected it |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| View All policy | An eligible create or update is rejected by CSP.CHECK_VIEW_ALL | Return the exact View All policy message and stop before package or approval; do not ask for ViewAllFlag |
| Input | Required input is missing, invalid, or cannot be normalized | Request the corrected value |
| Environment configuration | No active configured and authenticated Fusion environment is available | Return the environment-configuration error; do not request an environment URL |
| Baseline | The required current-environment export is missing, stale, failed, mismatched, incomplete, or unassociated | Run the declared task-level export route for the active configured environment and task, then revalidate |
| No-op | No allowed flag change or missing additive detail tuple remains for any supplied profile | Report unchanged comparisons by profile and stop without generating duplicate rows |
| Unsupported deletion | Profile deletion or criterion removal is requested | Return the documented deletion refusal and stop |
| Ambiguity | A value-resolution LOV returns multiple candidate values; multiple detail rows associated with one profile are not ambiguous | Require a user selection for the LOV value |
| Dependency | A required export, applicable data-role validation, or scope-alignment dependency is unresolved | Route to the stated owner and stop |
| Capacity | An enabled create or N-to-Y update produces requested activations greater than zero and a projected total above 20 including the default | Block the activation batch; report current and projected totals; do not exempt existing-profile activations |
| Authorization | A LOV request returns 401 or 403 | Route to the integration or security owner and stop |
| Scope | An unsupported dimension or mismatched source hierarchy is requested | Exclude it or resolve the authoritative contract |
| Transaction | An import outcome is uncertain | Reconcile by current export and manual UI review; do not retry |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Read-details output | Show exact Name, stored Description (explicitly empty when blank), EnabledFlag, ViewAllFlag, and each dimension flag independently of its stored criterion rows. Show every associated criterion as display name (original code/ID); preserve raw values and annotate label unresolved with its reason. Retain disabled/inactive values and flag/detail discrepancies without correcting them |
| Read-details partial result | Distinguish no match, conflicting matches, unavailable lookup, auth/transport failure, and unverified contract. Return verified profile facts and unresolved raw identities; never imply complete resolution. Do not use an authoring gap as permission to bypass registry readiness |
| Read-details execution gap | Clearly mark the request incomplete when a required lookup was not executed or its evidence is missing. Show each affected original code/ID with label unresolved: lookup not executed or evidence missing, the actual blocker, and resume at CSP.READ_RESOLVE_LABELS for permitted outstanding lookups. Do not describe skipped work as no match, unavailable lookup, or complete success |
| Read-details missing or ambiguous profile | Report not found for zero exact header matches; report ambiguity for multiple exact header matches. Never enter configuration, select one duplicate, prepare a package, or request import approval |
| Package readiness | The source hierarchy conflict and every unresolved contract that blocks a package |
| Create preview | Each eligible create, proposed header fields, one proposed detail row per requested value, and current, activation, and projected totals against limit 20 including the default |
| Protected request disclosure | List excluded protected-profile requests and explain the protection separately from eligible create, update, or no-op results; never describe excluded requests as processed or approved |
| Unsupported change disclosure | Show the requested criterion replacement, unsupported setting change, or rename and explain it is unsupported; explain any additive or new-profile alternative and obtain clarification before packaging |
| Update preview | Show current, activation, and projected totals against limit 20 including the default. Show before/after flag changes separately from criterion additions and unchanged values. Show all preserved omitted settings and existing entries. Do not imply an existing criterion value or name will change |
| Mixed preview | Every supplied profile Name, its create, update, or no-op classification, and its grouped setting rows |
| No-op result | Every matched profile and value that already exists, with confirmation that no duplicate rows were generated |
| Deletion refusal | Deletion of Candidate Security Profile rows is not supported. |
| Value resolution | The no-match or many-match outcome without guessing tenant identifiers |
| Import boundary | That this resource does not authorize FSM import execution or a REST write |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A current-run verified export baseline is unavailable | Do not classify the request as create or update, request an environment URL, or use the authoring reference files as the active-environment baseline |
| A requested detail tuple already exists | Do not generate a duplicate detail row |
| Profile deletion or criterion-entry removal is requested | Do not generate deletion rows, replacement data, an import, a disable operation, a blanking operation, or profile recreation |
| An explicit replacement or rename is requested | Do not generate replacement or rename rows, silently convert to addition or create, or claim that CSV row order identifies an existing entry. Explain the limitation and obtain clarification for a different supported operation |
| Required values are unresolved | Do not guess IDs or create a profile |
| An FSM import is requested from this workflow | Do not submit or retry an import |
| A target-pod identifier is absent | Do not copy or infer GradeId or BusinessUnitId from another pod |
| An existing profile is being updated | Do not bypass counting or capacity enforcement for N-to-Y activation updates; never request user confirmation as a substitute for validation |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CSP.READ_INVALID_NAME | terminal | 210 | terminal | none | CSP.READ_VALIDATE_NAME | stop | Ask for one nonblank exact profile Name; no defaults, package, approval, or profile mutation |
| CSP.READ_NOT_FOUND | terminal | 220 | terminal | none | CSP.READ_FIND_PROFILE | stop | Return profile not found in the fresh current-environment export; never reinterpret as create |
| CSP.READ_AMBIGUOUS | terminal | 230 | terminal | none | CSP.READ_FIND_PROFILE | stop | Report multiple exact header matches and stop without choosing or changing a profile |
| CSP.DONE_READ | terminal | 240 | terminal | none | CSP.READ_RESULT | stop | Return complete read-details output only after the evidence gate verifies a current-request label for every populated supported criterion, or verifies no supported criteria exist. Show display name (original code/ID), exact Name, stored Description, EnabledFlag, ViewAllFlag, every dimension flag, and all source criteria. No create/update defaults, design rejection, capacity check, package, import approval, or profile write |
| CSP.DONE_READ_PARTIAL | terminal | 250 | terminal | none | CSP.READ_RESULT | stop | Return verified stored profile details and every original criterion with available labels and explicit unresolved reasons; no configuration or profile write |
| CSP.READ_EXECUTION_GAP | terminal | 260 | terminal | none | CSP.READ_RESULT | stop | Return incomplete read-details output under Read-details execution gap disclosure, preserving verified facts and all raw criteria. Identify outstanding resolver evidence and the safe resume step; never mark the request completed. No configuration, package, import, or profile write |
| CSP.PACKAGE_GATE | decision | 80 | execution_gate | create_only_ready->CSP.DONE_CREATE;update_only_ready->CSP.DONE_UPDATE;mixed_ready->CSP.DONE_MIXED;blocked->CSP.HANDLE_ISSUES | CSP.VALIDATE_OUTGOING_IDS | stop | Return packages only after capacity enforcement and outgoing-ID validation passed for the exact artifact, for eligible creates or existing-profile flag updates and criterion additions. Retain update_only_ready for updates, including flag-only changes. Normal preview and explicit import approval remain mandatory; this resource executes no import |
| CSP.HANDLE_ISSUES | step | 90 | error_handler | classified->CSP.ISSUES | none | continue | Any declared failure or blocker other than deletion |
| CSP.HANDLE_DELETION | step | 100 | error_handler | refused->CSP.DELETION_REFUSED | none | continue | Profile deletion or criterion removal is requested |
| CSP.DONE_CREATE | terminal | 110 | terminal | none | CSP.PACKAGE_GATE | stop | All changed profiles are creates; the package is valid and no import is executed |
| CSP.DONE_UPDATE | terminal | 120 | terminal | none | CSP.PACKAGE_GATE | stop | Existing-profile allowed flag updates and criterion additions; omitted settings and existing criterion values preserved. Package valid; no import executed |
| CSP.DONE_MIXED | terminal | 130 | terminal | none | CSP.PACKAGE_GATE | stop | The valid package contains both create and update profiles; no import is executed |
| CSP.NO_CHANGE | terminal | 140 | terminal | none | CSP.CLASSIFY_DELTA | stop | Every supplied profile already contains all requested header and detail values; no rows are generated |
| CSP.DELETION_REFUSED | terminal | 150 | terminal | none | CSP.HANDLE_DELETION | stop | Return exactly: Deletion of Candidate Security Profile rows is not supported. |
| CSP.ISSUES | terminal | 160 | terminal | none | CSP.HANDLE_ISSUES | stop | A declared issue or unresolved TBD is present |
| CSP.PROTECTED_ONLY | terminal | 165 | terminal | none | CSP.PROTECT_SEEDED_PROFILE | stop | All supplied requests target the protected profile; explain protection and return without a package, missing configuration questions, approval prompt, or import |
