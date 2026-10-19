# Cost Allocation Key Flexfield Error Handling

Classify failures without exposing credentials, cookies, bearer tokens, package-sensitive data, or direct KFF mutation details. Stop before retrying an import or any other external operation.

## Error Situations

| Situation | What Should Happen | Evidence |
|---|---|---|
| Package task, flow, root, metadata, filename, or header mismatch | Return package mismatch with the expected task identity and seven-file contract; do not import | E1 |
| Missing parent, duplicate business key, conflicting column, or invalid instance segment | Return hierarchy integrity error with the affected business key and parent relationship | E1; E2 |
| Unresolved value set, tree, or segment label reference | Return dependency blocker; do not create, guess, or copy the reference | E1; E3 |
| Unsupported flag, enum, mandatory field, mutability, or custom-label behavior | Return an unconfirmed-contract blocker with the specific behavior that requires authoritative evidence | E1 |
| Delete-by-omission request | Return unsupported mutation; target rows absent from a package remain unchanged | E4 |
| Translation migration, direct KFF REST mutation, HDL, value-set creation, LDG association, SLA mapping, or transactional costing request | Return out-of-scope routing result; do not manufacture CSV rows or fallback routes | E1; E5 |
| Import process fails | Persist sanitized process result and ProcessLog/status evidence when available; stop before retry | E4 |
| Post-import verification or flexfield redeployment fails | Report failed completion; retain import and deployment evidence; do not claim success | E3; E5 |

## Error Classifications

| Result Category | When Used | Next Action | Evidence |
|---|---|---|---|
| input_validation | Package metadata, CSV schema, root identity, hierarchy, or field validation fails | Correct the package and repeat package validation | E1 |
| catalog_mismatch | Task code, offering, functional area, root, release, or package flow is wrong | Re-export or select the exact task package | E1 |
| dependency_blocker | Required value set, tree, label, deployment state, operation record, preview, or approval is unavailable | Resolve the owning prerequisite and revalidate | E2; E3 |
| unsupported_mutation | Requested operation exceeds the task-level CSV KFF contract | Route to the owning task; do not choose a fallback route | E4; E5 |
| process_failed | Shared FSM import or verification reports failure | Preserve sanitized diagnostic result and stop before retry | E4 |
| deployment_failure | Post-import KFF redeployment is unsuccessful or unavailable | Resolve deployment and verify again before declaring completion | E3 |

## Disclosure Rules

| Gate | What Must Be Shown | Evidence |
|---|---|---|
| Before import | Target environment; selected task; package identity and release; COST/801 root; applicable CSV files and Rule IDs; requested effect; dependency result; preview fingerprint; approval state | E1 |
| After import | Import process result; sanitized external IDs when available; post-import verification; flexfield deployment result; remaining blockers | E1; E3 |
| On failure | Failure class; stage; redacted message; recommended action; environment; artifact references; external IDs when available | E1 |

## Refusal Rules

| Situation | What Must Not Happen | Evidence |
|---|---|---|
| Direct task execution is not selected by a shared FSM workflow | Do not call a browser, OAuth path, loader, REST mutation, or alternate import route as a substitute | E1 |
| A package has a missing CSV file or mismatched header | Do not repair by deleting another file, changing schema, or silently substituting a package | E4 |
| A delete behavior is requested | Do not implement deletion by omitting rows | E4 |
| An evidence gap remains | Do not present unconfirmed enum, requiredness, mutability, custom-label, or target lookup behavior as executable | E1 |

## TBD Items

The exact create-field mandatory matrix, field mutability after deployment or costing use, task CSV enum domains for DefaultType, QueryRequiredType, and RangeType, custom-label creation constraints, and the target-tree compatibility contract remain `TBD`. The affected request must stop for authoritative or target-environment evidence; these limits do not authorize a fallback route.

## Evidence Register

| Evidence | Source | Source Type | Evidence Status | Release or Date | Limitation |
|---|---|---|---|---|---|
| E1 | Supplied task CSV template, data export, and ASM_SETUP_CSV_METADATA.xml described in the request | Task CSV evidence | Observed | 11.13.26.10.0 | No target environment result was supplied |
| E2 | [Key Information About Setup Data Export and Import Processes](https://docs.oracle.com/en/cloud/saas/applications-common/26b/oafsm/key-information-about-setup-data-export-and-import-processes.html) | Public Oracle documentation | Confirmed | 26b, reviewed 2026-08-18 | Generic FSM import behavior |
| E3 | [Business Objects for Moving Common Reference Objects](https://docs.oracle.com/en/cloud/saas/applications-common/26b/facia/business-objects-for-moving-common-reference-objects.html) | Public Oracle documentation | Confirmed | 26b, reviewed 2026-08-18 | Deployment evidence is run-specific |
| E4 | [Export and Import CSV File Packages](https://docs.oracle.com/en/cloud/saas/applications-common/25d/oafsm/export-and-import-csv-file-packages.html) | Public Oracle documentation | Confirmed | 25d, reviewed 2026-08-18 | Generic FSM package behavior |
| E5 | [Payroll Cost Allocation Key Flexfield Setup](https://docs.oracle.com/en/cloud/saas/human-resources/faipc/payroll-cost-allocation-key-flexfield-setup.html) | Public Oracle documentation | Confirmed | Current, reviewed 2026-08-18 | Separate tasks own LDG and SLA setup |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| KFFCSV_GATE_OPERATION | decision | 60 | execution_gate | ready->KFFCSV_COMPLETE;blocked->KFFCSV_HANDLE_GATE_ERROR | KFFCSV_ENFORCE_PACKAGE_DESIGN | stop | Validation and design enforcement succeeded; the selected shared workflow is determining whether the requested export, authoring, validation, or import can proceed |
| KFFCSV_HANDLE_INPUT_ERROR | step | 70 | error_handler | handled->KFFCSV_INPUT_STOP | KFFCSV_VALIDATE_PACKAGE | stop | Package input validation returned invalid |
| KFFCSV_HANDLE_DEPENDENCY_ERROR | step | 71 | error_handler | handled->KFFCSV_DEPENDENCY_STOP | KFFCSV_CHECK_DEPENDENCY_READINESS | stop | Hierarchy, external reference, or readiness validation returned unresolved |
| KFFCSV_HANDLE_DESIGN_ERROR | step | 72 | error_handler | handled->KFFCSV_DESIGN_STOP | KFFCSV_ENFORCE_PACKAGE_DESIGN | stop | Design enforcement returned blocked |
| KFFCSV_HANDLE_GATE_ERROR | step | 73 | error_handler | handled->KFFCSV_GATE_STOP | KFFCSV_GATE_OPERATION | stop | Execution gate returned blocked |
| KFFCSV_COMPLETE | terminal | 80 | terminal | none | KFFCSV_GATE_OPERATION | stop | The shared workflow has recorded the required validated outcome; an import also requires post-import and deployment verification |
| KFFCSV_INPUT_STOP | terminal | 81 | terminal | none | KFFCSV_HANDLE_INPUT_ERROR | stop | Input validation failed |
| KFFCSV_DEPENDENCY_STOP | terminal | 82 | terminal | none | KFFCSV_HANDLE_DEPENDENCY_ERROR | stop | Dependency validation failed |
| KFFCSV_DESIGN_STOP | terminal | 83 | terminal | none | KFFCSV_HANDLE_DESIGN_ERROR | stop | Design enforcement failed |
| KFFCSV_GATE_STOP | terminal | 84 | terminal | none | KFFCSV_HANDLE_GATE_ERROR | stop | The operation gate failed |
