# Design Enforcement

Before mutation, verify protection, security, and required properties against
current REST evidence. Unknown required properties block mutation. Only
confirmed missing rows may be proposed; verified no-ops are excluded. A blocked
set stops the batch before mutation.

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| FAVS.001 | A shared value-set **definition** changes | Error | resolve_value_set_metadata | A material definition field changes and other flexfield usage was not assessed, or a redeployment plan for every affected flexfield is absent | Confirm compatibility for every usage and redeploy every affected flexfield after the definition change. A value-only addition that preserves the definition does not trigger this rule. | Yes |
| FAVS.002 | Existing value set is protected | Critical | find_value_set | Target metadata identifies the value set as protected, or its protection status cannot be established before a mutation | Do not create, update, delete, or add values through the protected value set; select an unprotected approved alternative or escalate to the owning application team | No |
| FAVS.003 | Security is enabled | Error | resolve_value_set_metadata | Security impact across every flexfield usage is not assessed, DataSecurityObjectName is not fixed before save, or a table-security rule relies on a WHERE-clause bind variable | Assess all usages, use table aliases in security conditions, and treat table-security rules as independent of WHERE-clause bind variables | Yes |
| FAVS.004 | Table validation uses bind variables | Error | verify_table_validated_value_set_metadata | Bind syntax, source-segment ordering/context, or uniqueness assumptions are undocumented; a context-segment table value set uses SEGMENT or VALUESET bind variables | Use only Oracle-documented bind forms and verify the owning flexfield configuration; for a context segment, remove SEGMENT and VALUESET bind variables | Yes |
| FAVS.005 | Table value set is used by a key flexfield | Error | verify_table_validated_value_set_metadata | The approved design requires data security, OTBI, Essbase, or tree/hierarchy integration | Use an Independent value set for that key-flexfield usage, or obtain an approved design without those integrations | Yes |
| FAVS.006 | Flex Value Attribute or User-defined Value Attribute is supplied | Error |  | FND_VS_VALUES_B configuration, a context code equal to ValueSetCode, deployment, and sign-out/sign-in are not evidenced | Configure the required FND_VS_VALUES_B context-sensitive segments in the owning Descriptive Flexfields workflow, deploy, sign out/in, then return to this task | No |
| FAVS.007 | Existing value-set ValidationType update | Critical | find_value_set | Requested `ValidationType` differs from an existing target definition | Do not submit a package. State that ValidationType cannot be changed for an existing value set and request the new dependent value-set code and definition | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_value_set_metadata | Shared changes, security-enabled changes, or export-backed compatibility checks | Existing definition, values, parent context, and approved delta | ora_reference_lookups.md |
| find_value_set | Before evaluating an existing definition, protection, or ValidationType | Exact ValueSetCode and target definition | ora_reference_lookups.md |
| verify_table_validated_value_set_metadata | When a table-validated value set is in scope | Exported value-set key and approved table-validation attributes | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| VSET.ENFORCE_DESIGN | decision | 50 | design_enforcement | pass->VSET.IMPORT_GATE;blocked->VSET.HANDLE_DESIGN | VSET.SELECT_PACKAGE_SOURCE | stop | Package source selected |
