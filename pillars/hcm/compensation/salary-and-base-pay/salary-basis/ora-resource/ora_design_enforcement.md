# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Resolve the registered BO | Require the exact discriminator SalaryBasis. |
| 2 | Read current schema | Use current template and attribute metadata as the authoritative field and dependency contract. |
| 3 | Resolve Legislative Data Group | Require one exact effective LDG and use only the identity field or child declared by the current SalaryBasis schema. |
| 4 | Derive missing code | When Code is omitted, derive it from SalaryBasisName by uppercasing letters and replacing spaces between words with underscores. Preserve a supplied nonblank Code. |
| 5 | Resolve status | When status is omitted, resolve the Active default against enabled ACTIVE_INACTIVE values. When supplied, validate the supplied value and use the resolved code. |
| 4 | Resolve supplied Salary Basis Type | Validate a supplied type against enabled ORA_CMP_SAL_BASIS_DET_METHOD values and use the resolved code. |
| 5 | Resolve supplied Frequency | Validate a supplied frequency against enabled CMP_SALARY_BASIS values and use the resolved code. |
| 6 | Resolve Annualization Factor | Keep a supplied value. Only when it is omitted, derive it from the explicit frequency mapping; require user input for PERIOD or an unmapped code. |
| 7 | Validate supplied values and dependencies | Stop on an unknown field, invalid shape, unreadable schema, unresolved status, unresolved type, unresolved frequency, missing required Annualization Factor, or unresolved schema-declared dependency. |
| 8 | Enforce documented setup prerequisites | Require the salary element to pass the declared read-only payrollElementDefinitionsLOV validation. Require the documented rate definition only when SalaryBasisType resolves to R. |
| 9 | Resolve Input Value Name and ID | Use Amount only when Input Value Name is omitted; otherwise retain the supplied value. Resolve InputValueId only through the describe-confirmed compensationElementsLOV payrollElementInputValues child. |
| 10 | Resolve Grade Rate association | When supplied, require one exact active effective Grade Rate and a current SalaryBasis schema-declared field or child association. |
| 11 | Check create uniqueness | Before source preparation, require no exact name-plus-LDG or code-plus-LDG collision. |
| 12 | Prepare Data Loader handoff | When a payroll element is supplied, require the separate Data Loader runbook to include the resolved InputValueName and InputValueId evidence values in the SalaryBasis payload. |
| 13 | Route eligible work | Hand off only validated setup data to the task's separate core Data Loader workflow. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every Salary Basis request | Blocker | resolve_salary_basis_business_object | The finder does not return exactly one SalaryBasis object | Correct the registered BO condition; do not substitute a name | No |
| Any configuration field is supplied | Blocker | read_salary_basis_schema | The current template or attribute metadata is unavailable, malformed, or does not validate the field | Restore metadata access or correct the field; do not infer a contract | Yes |
| A Legislative Data Group is supplied | Blocker | resolve_salary_basis_ldg | The LDG does not resolve to one effective record, or the current SalaryBasis schema does not declare a compatible field or child association | Correct the LDG or use the documented schema-supported association; do not infer an attribute, ID, or row shape | Yes |
| Code is omitted | Blocker | derive_salary_basis_code | SalaryBasisName is missing or blank, or the derived Code fails the current schema or selected-LDG duplicate check | Provide a Salary Basis name or explicit code; do not bypass schema validation or uniqueness verification | Yes |
| Status is omitted or supplied | Blocker | resolve_salary_basis_status | The default Active value or supplied value does not resolve to exactly one enabled ACTIVE_INACTIVE code | Omit status to use Active, or provide A, I, or the exact enabled meaning Active or Inactive | Yes |
| A Salary Basis Type is supplied | Blocker | resolve_salary_basis_type | The value does not resolve to exactly one enabled ORA_CMP_SAL_BASIS_DET_METHOD code | Provide U, C, ORA_SIMPLE_COMPONENTS, or R, or its exact enabled meaning | Yes |
| A Frequency is supplied | Blocker | resolve_salary_basis_frequency | The value does not resolve to exactly one enabled CMP_SALARY_BASIS code | Provide an enabled CMP_SALARY_BASIS code or its exact enabled meaning | Yes |
| Frequency is PERIOD or an unmapped valid code and Annualization Factor is omitted | Blocker | resolve_salary_basis_frequency | No documented default is available | Provide Annualization Factor | Yes |
| Annualization Factor is supplied | Blocker | read_salary_basis_schema | The supplied value violates the current SalaryBasis field contract | Correct the value; do not substitute a mapped default | Yes |
| A field has a live reference-object or lookup requirement | Blocker | read_salary_basis_schema | Its schema-declared dependent value is missing or invalid | Supply and validate the exact dependency required by current metadata | Yes |
| The referenced payroll-enabled Salary Basis flow is in scope | Blocker | resolve_salary_basis_element | payrollElementDefinitionsLOV does not return one effective exact element and LDG match | Correct the element in the Elements task, then rerun the read-only validation. Do not infer configuration that the endpoint does not return. | Yes |
| Input Value Name is omitted or supplied | Blocker | resolve_salary_basis_input_value_id | The parent element or its payrollElementInputValues child does not return exactly one record matching the resolved Input Value Name and InputValueId | Correct the element or input value in the owning Elements task, then revalidate | Yes |
| A Grade Rate association is supplied | Blocker | resolve_salary_basis_grade_rate | The Grade Rate does not resolve to one active effective record, or the current SalaryBasis schema does not declare a compatible field or child association | Correct the Grade Rate or use the documented schema-supported association; do not infer an attribute, ID, or row shape | Yes |
| A create is requested | Blocker | check_salary_basis_duplicates | An exact Salary Basis name-plus-LDG or code-plus-LDG collision exists, or the describe-confirmed query contract cannot establish uniqueness | Provide a unique name or code; do not prepare a preview artifact until uniqueness is proven | Yes |
| A payroll element is supplied for a Data Loader create or update | Blocker | resolve_salary_basis_input_value_id | The Data Loader handoff lacks the exact InputValueName and InputValueId from the successful resolver evidence | Rebuild the runbook payload from the successful resolver evidence; do not infer or hand-enter an ID | Yes |
| SalaryBasisType resolves to R, Salary amount is determined by rates | Blocker | resolve_salary_basis_rate_definition | The rate definition is missing or does not use Element, Amount, the salary basis element, Reporting Required selected, Calculate Live Rates selected, unchanged Returned Rate Details, and Input Value contributor type | Create or correct the rate definition in the Rate Definition task | Yes |
| SalaryBasisType resolves to C | Blocker | read_salary_basis_schema | ComponentUsage and its child collection are absent, unsupported, or invalid for the selected component-usage behavior | Correct the component usage and component child collection; do not send display-only derived child fields | Yes |
| SalaryBasisType resolves to ORA_SIMPLE_COMPONENTS | Blocker | read_salary_basis_schema | A simple-component child is missing, its sequences collide or fall outside 1 through 999, or component-type prerequisites are invalid | Correct the child collection and its type-specific fields; do not infer a child key or unsupported attribute | Yes |
| A simple component resolves to ORA_CALCULATED_AMOUNT | Blocker | read_salary_basis_schema | No supported calculated attribute child exists, or an attribute violates parent, sequence, impact, or nonnegative-factor requirements | Correct the calculated attribute child through its schema-supported fields | Yes |
| SalaryBasisType resolves to R | Blocker | read_salary_basis_schema | Rate components are absent, duplicate, have colliding or invalid display sequences, or do not identify exactly one overall rate | Correct the schema-supported rate-component child collection | Yes |
| An existing Salary Basis is assigned to a worker | Blocker | read_salary_basis_schema | A requested edit changes a field or child that current metadata does not identify as safe to patch, or requests delete/recreate | Use a minimal schema-supported patch or obtain the owning process's assignment-aware handling; do not delete and recreate the basis | Yes |
| Schema validation succeeds | Gate | read_salary_basis_schema | None | Use the separate approved Data Loader workflow for any import or change | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_salary_basis_business_object | Before every Salary Basis request | Exact registered BO identity | ora_reference_lookups.md |
| read_salary_basis_schema | Before processing any supplied configuration field | Current field and dependency contract | ora_reference_lookups.md |
| resolve_salary_basis_ldg | Before processing a supplied Legislative Data Group | Exact effective LDG identity and schema-declared target mapping | ora_reference_lookups.md |
| derive_salary_basis_code | Before validating a create, update, import, or preview request's code | Supplied Code or a deterministic Code derived from SalaryBasisName | ora_reference_lookups.md |
| resolve_salary_basis_status | Before every create, update, import, or validation request | Enabled ACTIVE_INACTIVE LookupCode for a supplied status or the Active default | ora_reference_lookups.md |
| resolve_salary_basis_type | When Salary Basis Type is supplied | Enabled ORA_CMP_SAL_BASIS_DET_METHOD LookupCode | ora_reference_lookups.md |
| resolve_salary_basis_frequency | When Frequency is supplied | Enabled CMP_SALARY_BASIS LookupCode | ora_reference_lookups.md |
| resolve_salary_basis_element | When the referenced payroll-enabled flow is in scope | Element identity, LDG, and effective dates | ora_reference_lookups.md |
| resolve_salary_basis_input_value_id | When the referenced payroll-enabled flow is in scope | Exact resolved Input Value Name child InputValueId for the resolved ElementTypeId | ora_reference_lookups.md |
| resolve_salary_basis_grade_rate | When a Grade Rate association is supplied | Exact active effective Grade Rate identity and schema-declared target mapping | ora_reference_lookups.md |
| check_salary_basis_duplicates | Before every create source or approval preview | No exact name-plus-LDG or code-plus-LDG collision | ora_reference_lookups.md |
| resolve_salary_basis_rate_definition | When SalaryBasisType resolves to R | Rate definition identity and documented setup result | ora_reference_lookups.md |

## HDL Collection Boundaries

- Keep parent `SalaryBasis` values separate from `SalaryBasisSimpleComponent`, `SalarySimpleComponentAttributes`, `SalaryBasisComponent`, and `SalaryBasisPayRate` child values. The current template and child metadata decide whether each documented field is supported and how it is keyed.
- Do not fabricate a direct REST payload, collection URL, child identifier, or mutable display field from the implementation page. The separate Data Loader workflow remains the only mutation route.
- For an assigned basis, query assignment impact through the workflow-approved read contract before update or delete. Preserve the existing object and use only the current schema-supported minimal patch; never use delete/recreate as a shortcut.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALB.ENFORCE_SCHEMA_GATE | decision | 50 | design_enforcement | eligible->SALB.ROUTE;blocked->SALB.HANDLE_ISSUE | SALB.CHECK_DUPLICATES | stop | After field, dependency, Grade Rate, and duplicate validation |
