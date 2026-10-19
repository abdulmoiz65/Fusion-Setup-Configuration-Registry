# Reference Lookups

All discovery is delegated. This task does not construct REST URLs, use curl, manage OAuth, invoke browser automation, mutate Fast Formulas, or export Fast Formula setup data.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_computed_field_eff_scope | Contexts, segments, or mappings are requested | FlexfieldCode PER_PERSON_EIT_EFF; Category PER_EIT; Usage PER_PERSON_EIT_EFF | Delegated to `hcm.recruiting.recruiting-common.manage-extensible-flexfields` using a fresh EFF task export | Context code and name, enabled state, row behavior, SegmentCode, Name, Prompt, enabled state, data type | Keep enabled single-row contexts and enabled non-date, non-number segments; ORA_FND_APP_DESCRIPTIVE_FLEXFIELD_SEGMENT.csv is authoritative for segment presence | Selected FlexContextCode and eligible FlexSegmentCode values | Return a business-language no-match or ambiguity; do not infer absence from summary exports |
| resolve_fast_formula_details | Formula list, proposal, validation, artifact preparation, or stale-evidence revalidation | Exact comma-separated FormulaName values plus an optional Legislative Data Group filter; when omitted, use `Global` | Delegated request to `hcm.global-payroll.payroll-tools.fast-formulas`: Give me all the details of the formulas: names; Legislative Data Group: Global; run resource description, then perform the exact all-details lookup | Formula name, Formula ID, Base formula name, Formula type, Formula type ID, Effective start, Effective end, Legislative Data Group, Description, Edit status, Compiled, Compile status | Require exactly one effective result per exact name, type Recruiting Job Application Computed Field, BaseFormulaName, FormulaId, FormulaTypeId, Compiled Y, CompileStatus V; a blank LDG returned on a formula is valid global scope; impose no as-of-date filter because the delegated skill owns effective-date handling | Eligible formula evidence and CSV identity values; discard Formula Text | Block unavailable, ambiguous, ineffective, uncompiled, wrong-type, or incomplete results |
| export_current_computed_field_mappings | Mapping creation, replacement, import preparation, or verification | Exact setup task ORA_IRC_COMPUTED_FIELDS_CONFIGURATION | Delegated to shared.setup-export.task-level-export | ASM_SETUP_CSV_METADATA.xml and ORA_IRC_JA_COMPOUND_FIELD_DATA.csv | Require both members; count current mapping rows; after import compare every exported row to the approved complete mapping set | Fresh baseline identity, row count, and verification result | Block missing members, nonzero clean-target rows, or post-import mismatch |
| validate_computed_field_import_artifact | Exact final ZIP is assembled | Immutable ZIP filename, bytes, SHA-256, task identity, and task context | Delegated to Core Data Loader Task Hook data-load preview | Task-rule results, approval fingerprint, archive integrity, envelope readiness | All applicable task rules must pass against the exact archive bytes | Immutable artifact identity, approval fingerprint, task-validation envelope readiness | Block approval when validation fails; any byte change requires a new preview |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Context list is requested | Show only Context and Eligible segments count. |
| One context is selected | Show only Segment code, Segment name, and Prompt for that context. |
| Formula list is requested | Show only Formula name, Effective start, Effective end, Legislative Data Group, and Formula type. |
| Technical traceability is not requested | Retain formula IDs and technical type evidence internally; omit them from normal displays. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| JACF.RESOLVE_EFF | decision | 2 | reference_lookup | review->JACF.FORMAT_REVIEW;mapping->JACF.RESOLVE_FORMULAS;issues->JACF.DEPENDENCY_ISSUES | JACF.VALIDATE_INTAKE | stop | Context, segment, or mapping work is requested |
| JACF.RESOLVE_FORMULAS | decision | 3 | reference_lookup | review->JACF.FORMAT_REVIEW;mapping->JACF.VALIDATE_MAPPING;issues->JACF.DEPENDENCY_ISSUES | JACF.VALIDATE_INTAKE | stop | Formula list or mapping work is requested |
| JACF.EXPORT_BASELINE | decision | 6 | reference_lookup | clean->JACF.BUILD_ARTIFACT;existing_rows->JACF.MANUAL_CLEANUP;issues->JACF.DEPENDENCY_ISSUES | JACF.VALIDATE_MAPPING | stop | Mapping creation, replacement, or import is requested |
