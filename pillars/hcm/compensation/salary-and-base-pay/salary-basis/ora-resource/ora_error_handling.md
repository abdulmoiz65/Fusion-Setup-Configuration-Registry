# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A supplied ZIP contains ASM_SETUP_CSV_METADATA.xml | Classify it as an FSM setup-task CSV archive, preserve it unchanged, and route it to the approved Data Loader FSM preview and approval workflow. Do not perform SalaryBasis HDL registered-business-object, template, field, or child-row validation. |
| An FSM-marked ZIP reaches a SalaryBasis HDL lookup or child-row validation | Stop that HDL path as a source-routing error and restart from source-format classification; do not treat the missing HDL metadata or children as an FSM import blocker. |
| The registered-BO finder returns no or multiple SalaryBasis matches | Stop and report a registered-business-object validation gap. |
| SalaryBasis template download or attribute metadata retrieval fails | Stop before field validation, preview, import preparation, or mutation. Do not retry a non-authentication Fusion API failure automatically. |
| legislativeDataGroupsLOV returns no, multiple, ineffective, or schema-incompatible matches for the supplied LDG | Stop as a Legislative Data Group resolution or schema validation gap. Do not infer an LDG ID, loader field, or value shape. |
| Code is omitted and SalaryBasisName is missing or blank, or the derived Code fails schema validation or the selected-LDG duplicate check | Stop and request SalaryBasisName or an explicit Code. Do not infer a different transformation or bypass uniqueness validation. |
| A supplied status does not resolve to one enabled ACTIVE_INACTIVE code | Stop and request A or I, or the exact enabled meaning Active or Inactive. |
| A supplied Salary Basis Type does not resolve to one enabled ORA_CMP_SAL_BASIS_DET_METHOD code | Stop and request U, C, ORA_SIMPLE_COMPONENTS, or R, or its exact enabled meaning. |
| A supplied Frequency does not resolve to one enabled CMP_SALARY_BASIS code | Stop and request an enabled CMP_SALARY_BASIS code or its exact enabled meaning. |
| Frequency resolves to PERIOD and Annualization Factor is omitted | Stop and request Annualization Factor; no default is assumed for PERIOD. |
| Annualization Factor is omitted for an unmapped frequency code | Stop and request Annualization Factor; do not invent a default. |
| A supplied Annualization Factor fails the current SalaryBasis schema contract | Stop and request a valid value; do not replace it with a mapped default. |
| The default Amount or a supplied Input Value Name fails the current SalaryBasis field or dependency contract | Stop and request a valid Input Value Name; do not infer a replacement. |
| compensationElementsLOV does not declare the expected parent finder or payrollElementInputValues child, or returns parent or child records unrelated to the resolved element or Input Value Name | Stop as a query-contract failure. Do not report the input value as missing, infer a child path or parameter syntax, or fall back to the Data Loader BO. |
| compensationElementsLOV payrollElementInputValues returns no or multiple exact matches for the resolved Input Value Name | Stop as an Input Value resolution or ambiguity gap; request correction of the element or input value through the owning Elements task. |
| A current-schema field or dependency contract does not validate supplied input | Stop and identify the supplied field or dependency that needs correction. |
| payrollElementDefinitionsLOV returns no, many, or inactive salary basis elements | Stop and direct the user to correct the element through the owning Elements task; do not infer or create the prerequisite through this resource. |
| payrollElementDefinitionsLOV rejects separately serialized findByWord arguments, or returns records unrelated to the requested element or LDG | Stop as a query-contract failure. Do not report the element as missing and do not retry with generic q syntax or split finder arguments. |
| salaryRangeDifferentials does not declare the findByAdvancedSearchQuery custom action contract, rejects its documented headers or body, or returns a result with a Name or LDG unrelated to the supplied values | Stop as a query-contract failure. Do not report the differential as missing, infer a collection finder or filter, or fall back to the Data Loader BO. |
| salaryRangeDifferentials findByAdvancedSearchQuery returns no or multiple exact Differential Profile Name matches | Stop as a salary range differential resolution or ambiguity gap; request one valid, exact profile name. |
| A supplied Grade Rate has no exact active effective gradeRatesV2 match, or SalaryBasis metadata does not declare a compatible association field or child | Stop as a Grade Rate resolution or schema validation gap. Do not infer a loader attribute, identifier, or row shape. |
| SalaryBasisName or Code is blank or exceeds 80 characters, or a documented numeric bound fails current schema validation | Stop as an input validation gap and identify the failing field; do not truncate, round, or coerce the supplied value. |
| A component child collection has duplicates, invalid sequence values, missing type-specific fields, an unsupported child shape, or fails the required exactly-one overall rule | Stop as a collection validation gap. Do not flatten children into the parent row, synthesize a child key, or discard a child to make the request pass. |
| An assigned Salary Basis is requested to be deleted, recreated, or changed outside a current schema-supported minimal patch | Stop as an assignment-impact validation gap. Do not use delete/recreate as an update route. |
| A name or code collision is found in the selected LDG | Stop before loader-source preparation and request a unique name or code. |
| The user asks to change Fusion data | Route only through the task's separate approved Data Loader workflow after this resource has completed validation. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Source-routing error | An FSM-marked ZIP was sent to an HDL-specific SalaryBasis validation step | Restart from source-format classification and use the Data Loader FSM workflow; retain the original ZIP unchanged. |
| Registered-business-object validation gap | SalaryBasis is not uniquely resolved | Correct the registered BO condition, then rerun the read-only finder. |
| Schema validation gap | Template, component, or attribute metadata is unreadable, malformed, or mismatched | Restore the metadata contract; do not infer fields or dependencies. |
| Legislative Data Group resolution gap | The supplied LDG does not resolve to one exact effective legislativeDataGroupsLOV record, or its identity shape is unsupported by the current SalaryBasis schema | Provide one exact effective Legislative Data Group name or ID supported by the current schema. |
| Salary Basis code derivation gap | Code is omitted and SalaryBasisName cannot produce a schema-valid, unique derived Code | Provide SalaryBasisName or an explicit Code, then correct any schema or duplicate conflict. |
| Input validation gap | A supplied value does not meet the current schema contract | Correct the supplied field or dependent value, then validate again. |
| Status lookup validation gap | A supplied status is not an enabled ACTIVE_INACTIVE value | Provide A or I, or exact enabled meaning Active or Inactive. |
| Salary Basis Type lookup validation gap | A supplied type is not an enabled ORA_CMP_SAL_BASIS_DET_METHOD value | Provide U, C, ORA_SIMPLE_COMPONENTS, or R, or its exact enabled meaning. |
| Frequency lookup validation gap | A supplied frequency is not an enabled CMP_SALARY_BASIS value | Provide an enabled CMP_SALARY_BASIS code or its exact enabled meaning. |
| Annualization Factor input gap | A factor is required because the resolved frequency is PERIOD or has no documented mapping, or a supplied factor violates the schema | Provide a schema-valid Annualization Factor. |
| Input Value Name validation gap | The default Amount or supplied Input Value Name does not satisfy the current field or dependency contract | Provide a valid Input Value Name. |
| Input Value resolution gap | The resolved ElementTypeId does not return one exact payrollElementInputValues child with the resolved Input Value Name and InputValueId | Correct the element or input value through the owning Elements task, then validate again. |
| Fusion API failure | A non-authentication metadata request fails, including the observed UCM template HTTP 500 | Stop and report the failure; do not automatically retry. |
| Documented prerequisite gap | The referenced Oracle element fails declared read-only validation, or the rate-definition prerequisite is not ready | Correct or verify the prerequisite using its owning task. |
| Query-contract failure | Describe metadata does not support the selected finder or custom-action contract, the action headers or body are rejected, or returned records fail exact requested identity checks | Correct the endpoint contract before another lookup; do not treat it as a missing prerequisite. |
| Salary range differential resolution gap | The supplied Differential Profile Name does not resolve to one exact salaryRangeDifferentials custom-action result record | Provide one valid, exact Differential Profile Name. |
| Grade Rate resolution gap | The supplied Grade Rate does not resolve to one exact active effective gradeRatesV2 record | Provide one exact active effective Grade Rate name. |
| Duplicate configuration gap | An exact Salary Basis name or code collision exists in the selected LDG | Provide a unique name or code before preparing the approval artifact. |
| Collection validation gap | A documented incremental, simple, calculated-attribute, or rate-component child collection is duplicated, incomplete, unsupported, or violates its type-specific rule | Correct the collection using only current child metadata. |
| Assignment-impact validation gap | An assigned basis would be deleted, recreated, or edited outside a current schema-supported minimal patch | Use the assignment-aware owning workflow or restrict the request to supported patch fields. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Registered-BO blocker | Requested discriminator, resolver name, match result, and safe next action; never credentials. |
| Schema blocker | SalaryBasis, resolver name, failure class, and the fact that no field contract was inferred. |
| Legislative Data Group blocker | Supplied LDG name or ID, resolver name, effective-match result, and schema support result; never credentials. |
| Salary Basis code blocker | Supplied SalaryBasisName, supplied or derived Code, transformation result, and schema or duplicate result; never credentials. |
| Input blocker | Supplied field or dependency name and the current schema requirement that failed. |
| Collection blocker | Parent type, child collection name, child count, failing rule, and current-schema support result; never credentials or unrelated worker data. |
| Assignment-impact blocker | Requested operation, whether assignment impact was detected, allowed current-schema patch boundary, and safe next action; never worker-identifying data. |
| Documented prerequisite blocker | Supplied element name, LDG, or Grade Rate name; read-only validation result; relevant documented condition; and the owning task or process; do not disclose credentials. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| An FSM marker is present in the supplied ZIP | Do not query or require the SalaryBasis HDL business object, template, schema, or child collections for that archive. |
| Registered BO is not uniquely SalaryBasis | Do not use a similarly named BO. |
| Current schema is unavailable | Do not infer field names, request payloads, validation rules, dependencies, or defaults. |
| A Fusion metadata call fails outside 401 or 403 handling | Do not automatically retry the call. |
| A documented payroll prerequisite is missing, ambiguous, or fails read-only validation | Do not create, update, upload, import, or delete the element, group, rate definition, or process result through this resource. |
| A mutation is requested | Do not mutate through these resources; require the separate Data Loader workflow, exact preview, and explicit approval. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALB.FSM_LOADER_READY | terminal | 6 | terminal | none | SALB.CLASSIFY_SOURCE | continue | The supplied archive is FSM-marked and is ready for the Data Loader FSM preview and approval workflow |
| SALB.ROUTE | decision | 55 | execution_gate | validated_only->SALB.DONE_VALIDATED;hdl_mutation_ready->SALB.LOADER_READY;mutation_blocked->SALB.HANDLE_ISSUE | SALB.ENFORCE_SCHEMA_GATE | stop | Select validation completion or the Core Data Loader handoff for a create, update, delete, or import |
| SALB.HANDLE_ISSUE | step | 60 | error_handler | handled->SALB.RETURN_ISSUES | none | stop | Any registered-BO, schema, dependency, input, or Fusion API issue |
| SALB.RETURN_ISSUES | terminal | 70 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| SALB.DONE_VALIDATED | terminal | 80 | terminal | none | SALB.ROUTE | continue | SalaryBasis values are validated; no mutation was requested |
| SALB.LOADER_READY | terminal | 90 | terminal | none | SALB.ROUTE | continue | Create, update, delete, or import rules passed; invoke core.data-loader and follow it through immutable ZIP preview |
