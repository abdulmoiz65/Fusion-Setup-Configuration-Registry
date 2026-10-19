# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A functional-area assignment lacks user-provided `MultItemCatAssignFlag`; or it lacks `DefaultCategoryRequired` and no default Category Code or Category Name is supplied | Stop before treating the assignment as ready. Infer `DefaultCategoryRequired=Yes` when a default-category identity is supplied; otherwise obtain the missing required values. Prompt once for an applicable public Oracle Functional Area Catalog Rules document reference; when it is declined or absent, record `not_provided` and continue. When `HierarchyEnabled` is omitted, use the verified REST Describe default `Y`. |
| No catalog is assigned to a functional area and automatic-assignment impact is unresolved | Stop and assess the impact of skipping that functional area in automatic assignment. |
| The Catalogs functional area is shared by enabled offerings and cross-offering impact is unresolved | Stop and assess the effect on every enabled offering that uses the shared functional area. |
| An FSM import is requested without the validated same-task package, required metadata, or a verified target environment | Stop and request the missing package evidence or environment verification before preview or import. A same-environment baseline requires matching source and target environment identity; a cross-environment migration requires release compatibility. |
| The FSM package baseline is not a successful fresh export for EGP_MANAGE_DEFAULT_CATALOGS | Stop and obtain a new exact-task export with its process receipt; do not use a partial or unrelated archive. |
| Fusion returns an export ProcessId | Persist the TaskCode, ProcessId, submission time, source environment, and initial status in the project task run record before polling or ending the session. |
| Fusion accepts an FSM import | Persist the exact archive fingerprint, TaskCode, submission time, returned Data Loader Content ID, returned Request ID, and any returned FSM migration ProcessId before status polling or ending the session. |
| An FSM import response is missing, transport fails after dispatch, or the returned tracking identifier cannot be persisted | Treat the outcome as indeterminate. Do not resubmit the archive. Preserve a sanitized diagnostic and reconcile through the persisted Content ID, Request ID, or FSM migration ProcessId only; if no identifier exists, require a read-only reconciliation before a new import is considered. |
| Export polling times out or the session ends while the export is nonterminal | Preserve the ProcessId and last status, then resume that exact process later. Do not submit a replacement export automatically; if the process identity cannot be recovered after reconciliation, require fresh explicit user authorization for one replacement export. |
| An export process cannot be recorded safely | Stop before polling or resubmitting. Preserve a sanitized diagnostic and request recovery of the original process identity. |
| Candidate package members, metadata hierarchy, or CSV headers differ from the verified baseline | Stop before preview and correct the package. Only approved setup-data rows may differ from the verified baseline structure. |
| The package fingerprint is missing, the same-environment source/target identity does not match, or a cross-environment release is missing or incompatible | Stop before preview or import and obtain the missing identity evidence or a compatible package. |
| Catalog Code and Catalog Name are both blank for a catalog row | Present that only the catalog row will be omitted, retain the catalog CSV member and header, and request explicit omission approval. Do not omit dependent rows; they require an exact catalog reference validation. |
| Catalog Code or Category Code exceeds 30 characters | Stop before package preparation and ask the user for a distinct value of at most 30 characters. Do not truncate the value, copy an overlength value into its counterpart, or submit the package. |
| A non-omitted catalog row has a blank or mismatched EGP_CATALOG.csv.CategorySetName | Stop before preview or import. Map the resolved Catalog Name to CategorySetName, preserving the approved value; when Catalog Name was defaulted from Catalog Code, write that same value to CategorySetName. Rebuild and revalidate the package. |
| A non-omitted catalog row has an invalid ControlLevel | Stop before preview or import and ask the user to provide `1` (Master Level) or `2` (Organization Level), or the corresponding supported UI/REST value. A blank value defaults to `1`; normalize the accepted value, then rebuild and revalidate the package. |
| A REST or UI alias is unrecognized or conflicts with its supplied FSM counterpart | Classify as input validation and stop before package preparation. Preserve the supplied alias and normalized candidate in the diagnostic; require one unambiguous FSM value. |
| A supplied CategoryContentCode or its ItemsOnlyFlag/UI alias cannot normalize to `ITEM_ONLY` or `MIXED`, or conflicts with another supplied form | Classify as input validation and stop before package preparation. Require one unambiguous value: `ITEM_ONLY`/`MIXED`, or a supported Boolean alias. |
| Any catalog row's normalized `LEAF_ITEMS` or `ALL_ITEMS` code has zero, multiple, disabled, or ineffective matches in the one retrieved EGP_CATALOG_CONTENT_CODE collection | Stop before package preparation. Preserve the affected catalog-row identity, normalized code, sanitized row-to-lookup evidence, and the single complete lookup receipt; require an enabled, effective exact match rather than substituting another code or issuing a per-row lookup. |
| A catalog conflicts with user-provided HierarchyEnabled or MultItemCatAssignFlag values | Stop before preview or import. Correct the package to the exact user-provided documented values and rebuild it. Do not substitute values from another functional area. |
| User-provided DefaultCategoryRequired is Yes but neither Category Code nor Category Name is supplied | Stop before preview or import and ask the user to provide the default Category Code or Category Name. Do not choose, default, or omit the category. After the user provides it, resolve the category identity, retain the matching category and catalog-category rows, map the resolved code to EGP_CATALOG.csv.CategoryCode, and rebuild the package. |
| Exactly one of Category Code or Category Name is supplied | Inform the user that the missing counterpart will default to the supplied value; accept a different approved counterpart when the user provides one. |
| Any catalog or category row is absent without explicit row-omission approval | Stop before package preparation. Present each omitted row type, its retained CSV structure, and any remaining dependent-row verification requirement, then request explicit approval. |
| A dependent catalog reference is absent, ambiguous, or does not match the candidate catalog CSV or validated baseline ZIP | Stop before package preparation and request an exact approved Catalog Code or Catalog Name. |
| Functional Area ID or Functional Area Name cannot be resolved to one exact EGP_CATALOG_FUNCTIONAL_AREAS entry | Stop before package preparation and request a precise approved functional-area identity. Do not use the display name as the package ID. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| DESIGN_BLOCKER | Functional-area rule conformance, automatic-assignment impact, or shared-offering impact is unresolved | Correct or document the design decision before continuing. |
| MISSING | The validated same-task FSM package, its required metadata, or the target-environment verification is absent | Provide the missing package evidence or environment verification before continuing. |
| ARTIFACT_BLOCKER | The export receipt, package fingerprint, member inventory, metadata hierarchy, CSV headers, same-environment identity evidence, or cross-environment release-compatibility evidence is missing, invalid, or inconsistent | Refresh the exact-task export or correct the package; then rerun package verification before preview. |
| ROW_OMISSION_APPROVAL_BLOCKER | A catalog row, category rows, or both are absent without explicit row-omission approval | Approve the stated row omissions, or provide the missing row identity values. |
| CATALOG_REFERENCE_BLOCKER | A dependent catalog reference has zero, multiple, or conflicting exact matches in the candidate catalog CSV and validated baseline ZIP | Provide an exact approved Catalog Code or Catalog Name that resolves uniquely. |
| FSM_CATALOG_IDENTITY_MAPPING_BLOCKER | A non-omitted EGP_CATALOG.csv row has a blank CatalogCode or CategorySetName, or either field differs from its resolved catalog identity | Correct the FSM CSV mapping, rebuild the package, and revalidate before preview or import. |
| IDENTITY_LENGTH_BLOCKER | A Catalog Code or Category Code exceeds 30 characters | Obtain an approved value of at most 30 characters for the affected identity, then rebuild and revalidate. |
| FUNCTIONAL_AREA_RULE_BLOCKER | Required functional-area values are missing, invalid, or conflict with the package; or DefaultCategoryRequired is user-provided or inferred as Yes and the default category is missing | Obtain the missing required values. A public-document reference is optional: prompt once, then record `not_provided` and continue when it is declined or absent. Infer `DefaultCategoryRequired=Yes` from a supplied default Category Code or Category Name; otherwise, for a required default category, ask the user for Category Code or Category Name; then resolve it, rebuild, and revalidate. |
| CATEGORY_VALID_RELATIONSHIP_MISMATCH | An included category has no exactly matching row by unique `CategoryCode`, or duplicate/blank relationship rows exist | Stop before preview or import; create exactly one valid-category row for each unique `CategoryCode` and revalidate. Catalog context is not used for matching. |
| CATEGORY_PARENT_RELATIONSHIP_MISMATCH | Input supplies a parent category but `ParentCategoryCode` is missing, self-referencing, or cannot be resolved | Stop before preview or import; populate the matching valid-category row with the exact parent code and verify the parent category, then revalidate. |
| FUNCTIONAL_AREA_IDENTITY_BLOCKER | Functional Area ID and Functional Area Name have zero, multiple, or conflicting exact matches in EGP_CATALOG_FUNCTIONAL_AREAS | Provide an exact approved Functional Area ID or Functional Area Name that resolves uniquely. |
| PROCESS_TRACKING_BLOCKER | The export ProcessId, last status, or persisted task run record is absent or inconsistent | Stop and recover the original process identity. A replacement export is allowed only after reconciliation cannot recover it and the user gives fresh explicit authorization. |
| IMPORT_PROCESS_TRACKING_BLOCKER | The accepted FSM import has no persisted Content ID, Request ID, or available FSM migration ProcessId, or its result cannot be reconciled to exactly one status record | Do not resubmit. Recover and persist the original tracking identifier through a read-only reconciliation, then resume only that import. |
| APPROVAL_BLOCKER | An import is requested without the required preview and approval gate | Prepare a preview and obtain explicit approval immediately before a future import. |
| INPUT_CANONICALIZATION_BLOCKER | A REST/UI alias cannot be normalized exactly, conflicts with an FSM field, or needs an unverified FSM value | Provide one unambiguous canonical FSM value or verify the exact value against the same-task exported CSV contract. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Functional-area catalog design gate blocks | The unresolved prerequisite or design rule, affected functional area, and corrective action. |
| FSM import gate blocks | The missing package evidence or environment verification, the affected task code, and the safe next action. |
| FSM package verification blocks | Export-process outcome, package fingerprint, member and header difference, same-environment identity or cross-environment release evidence, and the corrective action. |
| Row omission approval blocks | The omitted catalog and/or category rows, the retained CSV members and headers, the effect on dependent rows, and the need for explicit approval. |
| Export process tracking blocks | TaskCode, ProcessId, submission time, last status, elapsed wait, run-record location, and the safe resume action. |
| FSM import tracking blocks | Archive fingerprint, TaskCode, Content ID, Request ID, FSM migration ProcessId when returned, submission time, last status, run-record location, and the safe read-only reconciliation action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| An export ProcessId is unavailable or unresolved | Do not submit another export, import a package, or claim that the baseline is complete, unless reconciliation cannot recover the process identity and the user gives fresh explicit authorization for one replacement export. |
| Export polling resumes | Do not poll a different process or use a manually inferred process identifier. |
| An FSM import response is uncertain | Do not resubmit the archive, create a replacement import, or claim completion. Reconcile the original submission through its persisted tracking identifier or a declared read-only status search. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CATALOGS.EXECUTION-CONTRACT-GATE | step | 40 | execution_gate | validated->RETURN_SUCCESS;incomplete->RETURN_ISSUES | CATALOGS.VERIFY-FSM-PACKAGE | stop | Manage Functional Area Catalogs input validation and FSM package verification are complete |
| CATALOGS.ROW-OMISSION-APPROVAL | step | 12 | execution_gate | approved->CATALOGS.CANONICALIZE-INPUT;missing->RETURN_ISSUES | CATALOGS.VALIDATE-INPUT | stop | A catalog row, category rows, or both would be omitted |
| RETURN_ISSUES | terminal | 50 | terminal | none | none | stop | Any task node identifies incomplete input, an unresolved design rule, or missing FSM import evidence |
| RETURN_SUCCESS | terminal | 60 | terminal | none | CATALOGS.EXECUTION-CONTRACT-GATE | stop | The FSM import gate passes |
