# Candidate Security Profiles Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 0 | Protected request scope | After fresh export validation, apply CSP.PROTECT_SEEDED_PROFILE before configuration intake; retain excluded requests for disclosure and process only the remaining profiles |
| 1 | Optional criteria | Permit no criteria; validate resolved values only for selected dimensions and preserve existing update criteria |
| 2 | View All policy | Apply CSP.CHECK_VIEW_ALL after defaulting and before delta/no-op classification; require effective ViewAllFlag=N for every eligible create or update |
| 3 | Supported-dimension boundary | Reject Job Family, Job Function, and Legal Employer without an approved verified contract |
| 4 | Tenant identity boundary | Confirm Grade and Business Unit values are resolved in the target pod and were not copied or inferred from another pod |
| 5 | Ambiguity boundary | Auto-select only one unambiguous exact result |
| 6 | Profile grouping | Group all requested and exported detail rows by their exact profile Name; allow multiple setting rows per profile |
| 7 | Detail-row atomicity | Generate exactly one detail row for each requested value in one security dimension |
| 8 | Flag and criterion delta | Allow EnabledFlag and supported SecureBy flag updates; preserve omitted settings and existing criterion rows. Insert only missing canonical criteria; no criterion replacement, deletion, rename, or other setting change |
| 9 | Enabled-profile capacity | Require count_active_candidate_security_profiles for changed batches. If requested activations are positive and projected total exceeds 20 including the default, block the batch. Disables and updates that do not increase capacity remain allowed, with excess disclosed |
| 10 | Deletion boundary | Refuse profile deletion and criterion-entry removal; do not reinterpret replacements as additions |
| 11 | Branch preview | Show creates, flag updates, criterion additions, and no-ops; identify flag changes separately from new criteria and preserved entries |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any request targeting exact Name View All Candidates | Error | | A create, update, rename, disable, delete, or detail change targets this protected profile as Name, old name, or new name | Treat this exact case-sensitive Name as count-only and read-only. After fresh export validation, at CSP.PROTECT_SEEDED_PROFILE exclude its requests from configuration processing before create/update classification, missing-field questions, defaults, or deletion handling. Retain the excluded requests for the protection explanation; continue unrelated profiles through all normal gates. If only protected requests remain, return CSP.PROTECTED_ONLY without a package. Do not identify other profiles as protected solely because ViewAllFlag=Y | No |
| Final package validation | Error | | Any header or associated detail output row targets exact Name View All Candidates | Stop package handoff until the protected row is excluded; leave the fresh exported baseline unchanged and retain all other safeguards | No |
| Any eligible create or update at CSP.CHECK_VIEW_ALL | Error | | ViewAllFlag=Y was explicitly requested or remains Y on an existing profile | Reject with the View All policy message; never silently replace Y with N or prompt for ViewAllFlag. Changing an existing Y to N is also unsupported under the unchanged View All policy | No |
| Any create or update package | Error | | Any output profile has effective ViewAllFlag other than N | Block package handoff; do not rewrite the value to pass validation | No |
| Supplied criteria and dimension flags | Error | | Explicit N conflicts with supplied criteria | Set the corresponding supported dimension flag Y when criteria are supplied on creates or updates, including exported N. Preserve omitted flags when no criteria are supplied. Explicit flag changes do not delete existing criterion entries | No |
| A security dimension is selected | Error | find_candidate_security_profile_by_name | The selected dimension has neither an existing nonblank value for the same exact profile and dimension in the fresh verified export nor a newly supplied value that passed the existing lookup and validation rules | For creates with a supported SecureBy flag Y and existing N-to-Y dimension updates, including activation derived from supplied criteria, require corresponding value evidence. Use the fresh verified export as the authoritative local baseline; values for another profile or dimension never qualify. Block before approval/upload and identify the profile and missing dimension value. Do not invent values or resend existing criteria for flag-only updates. For creates with no selected dimensions, all SecureBy flags N and zero detail rows are valid, even when EnabledFlag=Y. Preserve omitted existing-profile settings and all existing criteria | Yes |
| Grade Level is selected | Error | resolve_grade | A target-pod GradeId is missing, ambiguous, copied, or inferred | Resolve the value in the target pod | Yes |
| Business Unit is selected | Error | resolve_business_unit | A target-pod BusinessUnitId is missing, ambiguous, copied, or inferred | Resolve the value in the target pod | Yes |
| Job Family, Job Function, or Legal Employer is requested | Error | | No approved verified product contract exists | Exclude the unsupported dimension | No |
| Country is selected | Error | resolve_country | The match is not one unambiguous exact result | Request correction or selection | Yes |
| Person Type is selected | Error | resolve_person_type | The value fails the resolver's exact-match or current-row eligibility rule | Request an eligible selection; preserve unchanged stored values | Yes |
| Recruiting Type is selected | Error | resolve_recruiting_type | The match is not one unambiguous exact result | Request correction or selection | Yes |
| Any generated detail row | Error | | The row represents zero values or more than one security dimension value | Generate one row containing exactly one security dimension value | Yes |
| Multiple detail rows share the same exact profile Name | Error | find_candidate_security_profile_by_name | The rows are treated as ambiguous or are not grouped under that profile | Group every associated row under the profile and evaluate each row as one setting value | Yes |
| Enabled creates or existing N-to-Y activations | Error | count_active_candidate_security_profiles | Requested activations are positive and the projected total exceeds 20 enabled profiles including the always-enabled default | Block the complete activation batch before approval/upload; report current total, requested activations, projected total, and limit 20. At most 19 non-default profiles may be enabled. Do not silently select a subset or credit unconfirmed disables. Allow disables and non-capacity-increasing updates even when already over capacity; disclose the excess | Yes |
| Deleting an existing profile or security-value row | Error | classify_candidate_security_profile_delta | The request deletes a profile or removes an existing security-value row | Refuse deletion | No |
| Previewing one or more profiles | Error | find_candidate_security_profile_by_name | The preview does not identify create or update independently for each exact profile Name | Show the per-profile classification and all grouped setting rows | Yes |
| Previewing an update | Error | classify_candidate_security_profile_delta | The preview does not separate flag changes, criterion additions, and unchanged values | Show before/after flag changes separately from new criteria and unchanged values; preserve omitted settings and existing entries | Yes |
| Existing profile settings | Error | find_candidate_security_profile_by_name | Any supplied setting other than EnabledFlag or supported SecureBy flags differs from the baseline | Allow EnabledFlag and supported SecureBy flag updates; identical supplied settings are no-ops. Reject changes to Name, Description, ViewAllFlag, or other settings; retain supported-dimension restrictions | No |
| Replacement or rename intent | Error | | A replacement or differing new name is requested, including when the source Name is absent | Explain unsupported changes and obtain clarification for an additive request or separate new profile. Do not silently reinterpret or process partial changes | No |
| Missing-name update wording | Error | find_candidate_security_profile_by_name | Zero matches classifies as create but the user expected an existing-profile update | Explain the proposed new profile and obtain clarification before proceeding | Yes |
| Existing-profile additions | Error | classify_candidate_security_profile_delta | Output changes an unsupported setting or replaces, removes, or duplicates an existing criterion | Preserve omitted settings and existing entries; apply allowed flag changes and insert only absent canonical tuples | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_grade | Grade Level is selected | GradeId | ora_reference_lookups.md |
| resolve_business_unit | Business Unit is selected | BusinessUnitId | ora_reference_lookups.md |
| resolve_country | Country is selected | TerritoryCode | ora_reference_lookups.md |
| resolve_person_type | Person Type is selected | LookupCode | ora_reference_lookups.md |
| resolve_recruiting_type | Recruiting Type is selected | LookupCode | ora_reference_lookups.md |
| find_candidate_security_profile_by_name | Before create-or-update classification | Per-profile classification, matching header row, and all associated detail rows | ora_reference_lookups.md |
| classify_candidate_security_profile_delta | At least one supplied profile matched | Per-profile flag changes, unchanged settings, unchanged detail tuples, canonical additions, duplicate suppression, and conflicts | ora_reference_lookups.md |
| count_active_candidate_security_profiles | Every changed configuration batch, including activation updates | Current total, requested activations, projected total | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CSP.PROTECT_SEEDED_PROFILE | decision | 5 | design_enforcement | eligible_remaining->CSP.VALIDATE_IDENTITY;protected_only->CSP.PROTECTED_ONLY | CSP.CHECK_READINESS | stop | After fresh export validation, partition protected-name requests using supplied Name, old name, and new name. No modification is performed. An empty or missing-name request follows eligible_remaining for input validation |
| CSP.CHECK_CHANGE_INTENT | decision | 25 | design_enforcement | allowed->CSP.VALIDATE_INPUTS;unsupported->CSP.HANDLE_ISSUES;clarification_required->CSP.HANDLE_ISSUES | CSP.CLASSIFY_PROFILE | stop | Reject requested replacements, differing new names, and any supplied setting different from an existing header except EnabledFlag and supported SecureBy flags. Identical supplied settings are unchanged. Missing-name update wording requires clarification that a new profile would be created. Never reinterpret unsupported intent; only a clarified create, allowed flag update, or additive request may resume |
| CSP.CHECK_VIEW_ALL | decision | 40 | design_enforcement | allowed->CSP.CHECK_CRITERIA_FLAGS;blocked->CSP.HANDLE_ISSUES | CSP.APPLY_DEFAULTS | stop | After create defaults or update baseline preservation, require effective ViewAllFlag=N before delta classification, including otherwise unchanged updates |
| CSP.CHECK_CRITERIA_FLAGS | decision | 42 | design_enforcement | consistent->CSP.RESOLVE_VALUES;conflict->CSP.HANDLE_ISSUES | CSP.CHECK_VIEW_ALL | stop | Reject explicit N with supplied criteria. On creates and updates, derive omitted selected supported flags Y even when exported N. Preserve omitted flags without supplied criteria and retain all existing criterion rows |
| CSP.CHECK_DIMENSION_VALUES | decision | 48 | design_enforcement | satisfied->CSP.CLASSIFY_DELTA;not_applicable->CSP.CLASSIFY_DELTA;missing->CSP.HANDLE_ISSUES | CSP.RESOLVE_VALUES | stop | Apply the selected-security-dimension value rule to every create with a supported SecureBy flag Y and every existing N-to-Y security dimension update, whether explicit or derived from supplied criteria. Match baseline entries from find_candidate_security_profile_by_name to the exact profile and corresponding dimension; alternatively require newly supplied values with successful existing lookup and validation evidence. An empty or absent corresponding value fails. If no such activation is requested, return not_applicable. Do not infer this requirement from profile EnabledFlag alone; preserve existing supported-dimension restrictions and other design rules |
| CSP.ENFORCE_DESIGN | step | 70 | design_enforcement | compliant->CSP.VALIDATE_OUTGOING_IDS;deletion_requested->CSP.HANDLE_DELETION;blocked->CSP.HANDLE_ISSUES | CSP.COUNT_CAPACITY | stop | Apply all Design Rules, including the enabled-profile capacity rule using count_active_candidate_security_profiles results for the entire batch. Validate creates, EnabledFlag and supported SecureBy flag updates, and criterion insertions; no identity, other setting, or existing criterion value may change |
