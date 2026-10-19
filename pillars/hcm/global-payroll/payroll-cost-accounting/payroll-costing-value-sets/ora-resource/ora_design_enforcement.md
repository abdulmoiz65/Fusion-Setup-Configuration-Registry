# Payroll Costing Value Sets Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Enforce task boundary | Confirm the request is limited to ORA_PAY_PAYROLL_COSTING_VALUE_SETS task-level FSM CSV behavior |
| 2 | Enforce package identity | Require the exact task metadata, Payroll Costing scope, root object, six CSV nodes, headers, and compatible release |
| 3 | Enforce target ownership | Require a target-evidence-backed ModuleId and preserve the distinction between ModuleId and moduleKey |
| 4 | Enforce Value Set design | Apply only confirmed validation-code mappings, typed values, parents, security, and table source evidence |
| 5 | Enforce relationship integrity | Require two Independent Value Sets, complete mappings, confirmed orientation, and disabled state until a new relationship is complete |
| 6 | Enforce dependent effect verification | Require post-import verification and Cost Allocation KFF redeployment verification when the change affects a used Value Set or relationship |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every request | Error | inspect_task_csv_package_metadata | The request targets another task, module, functional area, root business object, or package contract | Use only the confirmed task-level FSM CSV route and package | Yes |
| A root Value Set is created or changed | Error | verify_target_module_evidence | ModuleId is absent, unvalidated for the target, or copied from incompatible release evidence | Obtain one target-specific evidence result; keep moduleKey = HcmPayCostTop separate from ModuleId | Yes |
| A new Value Set definition is authored | Error | | ValueSetIdentifier, audit data, stored code, data type, subtype, flag, range, or required attribute is invented from an example | Preserve confirmed source data and block unconfirmed field behavior | Yes |
| A Value Set uses Independent, Dependent, Subset, Format Only, or Table semantics | Error | resolve_parent_value_set_reference | The functional model is conflated with another model or its stored CSV representation is unconfirmed | Use only the documented functional meaning; author only a confirmed stored task CSV representation | Yes |
| Table validation is requested | Error | verify_table_validation_source_evidence | Source table, columns, filtering, ordering, aliases, or target contract has not been validated | Validate the actual source through the declared shared workflow; do not generate SQL | Yes |
| A Validation View Object row is proposed | Error | | The task-level authoring contract is unconfirmed | Preserve the known schema and stop until task evidence confirms authoring semantics | No |
| Security-related or protected data is affected | Error | verify_value_set_security_evidence | The request would modify a protected Value Set or values, or security evidence is missing | Stop the protected mutation; use only target-validated security references | No |
| A Value Set value is supplied | Error | resolve_parent_value_set_reference | The parent cannot resolve, typed value storage conflicts with the parent, dates are invalid, or a row is moved by an unconfirmed foreign-key change | Keep one exact parent and use a datatype-compatible value field | Yes |
| A related relationship is created, modified, enabled, or disabled | Error | resolve_related_value_pair | Either member is not an Independent Value Set, a mapped value is unresolved, or the pair orientation is unconfirmed | Keep related Value Sets distinct from Dependent and Subset relationships; complete mappings before enabling a new relationship | Yes |
| An import affects Value Sets used by a Cost Allocation KFF or related values used by its segments | Error | | There is no successful post-import redeployment verification when applicable | Record the affected flexfield and verify successful redeployment before completion | Yes |
| A delete is requested through omitted rows, missing CSV files, REST, alternate import, XML, HDL, or another unlisted route | Error | | The request attempts to bypass the confirmed task-level CSV contract | Stop and report the task boundary; use only a separately authorized, confirmed workflow if one exists | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| inspect_task_csv_package_metadata | Every task-level package or operation | Task identity; root object; scope; release; all file names and headers | ora_reference_lookups.md |
| verify_target_module_evidence | New or modified root Value Set | Target environment; applicable release; validated ModuleId | ora_reference_lookups.md |
| resolve_parent_value_set_reference | Value authoring or Independent-parent-based model | Parent codes; child association; parent readiness | ora_reference_lookups.md |
| verify_table_validation_source_evidence | Table validation | Validated source metadata and parent association | ora_reference_lookups.md |
| resolve_related_value_pair | Related Value Set or mapping behavior | Independent pair; mapping readiness; orientation; enable readiness | ora_reference_lookups.md |
| verify_value_set_security_evidence | Protected or security-related behavior | Protection status; security readiness | ora_reference_lookups.md |

## Evidence Matrix

| Claim or Contract | Source | Source Type | Evidence Status | Release or Date | Limitation |
|---|---|---|---|---|---|
| Payroll Costing Value Sets precede Cost Allocation KFF definition | OHC-PAY-SETUP | Public documentation | Confirmed | Accessed 2026-08-19 | Functional sequencing only |
| Value Sets can be reused or created for Payroll Costing segments | OHC-PAY-REL | Public documentation | Confirmed | Accessed 2026-08-19 | Does not define FSM schema |
| Related Value Sets enforce full cost-combination relationships during payroll validation | OHC-PAY-REL | Public documentation | Confirmed | Accessed 2026-08-19 | Runtime payroll semantics, not CSV row behavior |
| Payroll related members must be Independent | OHC-PAY-REL | Public documentation | Confirmed | Accessed 2026-08-19 | Pair orientation remains task-contract evidence |
| New Payroll relationship remains disabled until mappings exist | OHC-PAY-REL | Public documentation | Confirmed | Accessed 2026-08-19 | Applies to a new relationship |
| Related-value changes require successful Cost Allocation KFF redeployment | OHC-PAY-REL | Public documentation | Confirmed | Accessed 2026-08-19 | Verify only when affected |
| Functional validation models include Format Only, Independent, Dependent, Subset, and Table | OHC-VS-OVERVIEW and OHC-VS-TYPES | Public documentation | Confirmed | 25c; accessed 2026-08-19 | Stored FSM codes are not all documented |
| Dependent and Subset models rely on an Independent Value Set | OHC-VS-TYPES | Public documentation | Confirmed | 25c; accessed 2026-08-19 | Exact task CSV row shape is incomplete |
| Table validation has source, value column, and optional ID, description, WHERE, and ORDER BY semantics | OHC-VS-TYPES | Public documentation | Confirmed | 25c; accessed 2026-08-19 | Task-specific SQL and VO authoring require evidence |
| Value data types and subtypes have functional semantics | OHC-VS-PLAN | Public documentation | Confirmed | 25c; accessed 2026-08-19 | Stored FSM codes other than observed mappings are not confirmed |
| Protected Value Sets and their maintained values cannot be edited | OHC-VS-OVERVIEW and OHC-VS-PROTECTED | Public documentation | Confirmed | Accessed 2026-08-19 | References to protected Value Sets remain allowed |
| Application Flexfield Value Set is the FSM business object and supports moduleType/moduleKey or valueSetCode scope | OHC-FSM-BO | Public documentation | Confirmed | 25d; accessed 2026-08-19 | Generic business-object scope, not task schema |
| Value Set import can require flexfield redeployment | OHC-FSM-BO | Public documentation | Confirmed | 25d; accessed 2026-08-19 | Verify affected flexfields |
| CSV template and task data packages are supported generic FSM concepts | OHC-FSM-CSV, OHC-FSM-EXPORT, OHC-FSM-IMPORT, and OHC-FSM-TEMPLATE | Public documentation | Confirmed | 25c through 26c; accessed 2026-08-19 | Shared workflows own API operations |
| Do not delete a CSV file; retain a header-only file | OHC-FSM-CSV | Public documentation | Confirmed | 25c; accessed 2026-08-19 | Does not establish record-deletion behavior |
| Import does not delete a target record omitted from the configuration package | OHC-FSM-PROCESS | Public documentation | Confirmed | 26a; accessed 2026-08-19 | Deletion needs a separately confirmed workflow |
| Task metadata flow is TASK_CSV_SERVICE for the current target export | TARGET-EXPORT-300103767070301 | Target-environment task CSV evidence | Observed | 2026-08-19 | Revalidate package metadata for a future target release or environment |
| Root business object is FND_APP_FLEX_VALUE_SET | SUP-REQ supplied metadata excerpt | Task CSV evidence | Observed | 11.13.26.10.0 | Revalidate future schema changes |
| Task scope is LBA and HcmPayCostTop | SUP-REQ supplied metadata excerpt | Task CSV evidence | Observed | 11.13.26.10.0 | Scope identity is not ModuleId |
| Service metadata is ValueSetWS and BatchSize is 500 | SUP-REQ supplied metadata excerpt | Task CSV evidence | Observed | 11.13.26.10.0 | Package-specific metadata |
| The template contains six CSV nodes with identical headers in template and normal exports | SUP-TEMPLATE and SUP-EMPTY-EXPORT | Task CSV evidence | Observed | 11.13.26.10.0 | Revalidate future releases |
| Payroll Costing ModuleId 61ECAF4AAAEAE990E040449821C61C97 was observed in one test export | SUP-TEST-EXPORT | Task CSV evidence | Observed | 11.13.26.10.0 | Not a portable constant |
| Independent is stored as INDEP | SUP-TEST-EXPORT | Task CSV evidence | Observed | 11.13.26.10.0 | Other stored validation codes are unconfirmed |
| Character and Text are stored as VARCHAR2 and TEXT | SUP-TEST-EXPORT | Task CSV evidence | Observed | 11.13.26.10.0 | Other datatype and subtype codes are unconfirmed |
| Test Value Set and value 001 are customer-created test evidence | SUP-TEST-EXPORT | Task CSV evidence | Observed | 11.13.26.10.0 | Not seeded configuration or defaults |
| Exact Validation View Object authoring behavior | SUP-REQ | Evidence gap | TBD | 2026-08-19 | Preserve schema only and block authoring |
| Exact stored CSV enums beyond INDEP, VARCHAR2, and TEXT | SUP-REQ | Evidence gap | TBD | 2026-08-19 | Do not guess |
| Related pair orientation and task CSV delete behavior | SUP-REQ | Evidence gap | TBD | 2026-08-19 | Do not infer a write or delete contract |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Resolver |
|---|---|---|---|---|---|---|---|---|
| PCVS.ENFORCE_TASK_BOUNDARY | decision | 3 | design_enforcement | passed->PCVS.HANDOFF_GATE;failed->PCVS.FAILED | PCVS.CHECK_DEPENDENCIES | stop | Every task-level CSV package, authoring, import, or verification request | |
