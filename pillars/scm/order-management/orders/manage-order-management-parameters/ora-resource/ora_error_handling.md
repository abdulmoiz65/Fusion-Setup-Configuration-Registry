# Manage Order Management Parameters Error Handling

## Oracle Guidance Source

Use Oracle's [Manage Order Management Parameters — 26c](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faiom/manage-order-management-parameters.html#Order-Management-Parameters) guide to resolve parameter behavior and value questions before retrying a failed or indeterminate save.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Requested parameter or intended value is absent, ambiguous, or not documented for the intended flow | Stop before saving. Obtain the approved parameter decision and verify it against the current Oracle documentation. |
| qpParameters lookup does not return exactly one canonical parameter record | Stop before preparing parameter values. Do not substitute qpParameterValues or attempt a mutating REST operation. Correct the requested parameter name and repeat the read-only lookup through the approved workflow. |
| qpParameters returns a parameter whose ParameterUsageCode is not FOM, CMN, or DOO | Stop. Do not use or prepare a value change for the out-of-scope parameter. |
| qpParameters does not return ParameterId or the qpParameterValues child lookup fails | Stop before preparing a value change. Do not construct a child URL with an inferred identifier and do not attempt a mutating REST operation. Resolve the parent record again through the approved read-only workflow. |
| A prepared `PATCH` row lacks `ParameterValueId` or `ParameterId`, or its `ParameterId` differs from the canonical parent identifier | Stop before creating the archive. Resolve the canonical parent again, populate both identifiers, and revalidate; do not infer the parent identifier from the child identifier. |
| inventoryOrganizationsLOV does not return exactly one inventory organization with OrganizationId for the supplied Item Validation Organization | Stop before preparing the parameter value. Do not infer an organization id or save the supplied organization text as the parameter value. Correct the organization input and repeat the approved read-only lookup. |
| ORA_DOO_COVERAGE_START_DATE lookupCodes does not return exactly one LookupCode for the supplied coverage-item start-date value | Stop before preparing the QP_COVERAGE_START_DATE parameter value. Do not infer a lookup code or save the supplied start-date text as the parameter value. Correct the coverage-item start-date input and repeat the approved read-only lookup. |
| ORA_FOM_SELL_PROFIT_CENTER_BU lookupCodes does not return exactly one LookupCode for the supplied selling-profit-center business-unit value | Stop before preparing the QP_SELLING_PROFIT_CENTER_BU parameter value. Do not infer a lookup code or save the supplied business-unit text as the parameter value. Correct the supplied value and repeat the approved read-only lookup. |
| YES_NO lookupCodes does not return exactly one LookupCode for a supplied value for a listed YES_NO parameter code | Stop before preparing the parameter value. Do not infer a lookup code or save the supplied value as the parameter value. Correct the supplied value and repeat the approved read-only lookup. |
| ORA_FOM_QTY_INVOICE_OVERSHIP lookupCodes does not return exactly one LookupCode for the supplied parameter value | Stop before preparing the QP_QTY_INVOICE_OVERSHIP parameter value. Do not infer a lookup code or save the supplied value as the parameter value. Correct the parameter value and repeat the approved read-only lookup. |
| ORA_FOM_SHIP_TOLERANCE_SOURCE lookupCodes does not return exactly one LookupCode for the supplied parameter value | Stop before preparing the QP_SHIP_TOLERANCE_SOURCE parameter value. Do not infer a lookup code or save the supplied value as the parameter value. Correct the parameter value and repeat the approved read-only lookup. |
| ORA_FOM_INV_TRX_DATE lookupCodes does not return exactly one LookupCode for the supplied parameter value | Stop before preparing the QP_INVENTORY_TRX_DATE parameter value. Do not infer a lookup code or save the supplied value as the parameter value. Correct the parameter value and repeat the approved read-only lookup. |
| ORA_DOO_CUST_REL_TYPE lookupCodes does not return exactly one LookupCode for the supplied parameter value | Stop before preparing the QP_CUSTOMER_REL_TYPE parameter value. Do not infer a lookup code or save the supplied value as the parameter value. Correct the parameter value and repeat the approved read-only lookup. |
| workersLov does not return exactly one worker with PersonId for the supplied preparer name | Stop before preparing the QP_PREPARER_FOR_PROC parameter value. Do not infer a person id or save the supplied preparer name as the parameter value. Correct the preparer name and repeat the approved read-only lookup. |
| ORA_DOO_DFLT_TAX_DETERMINANTS lookupCodes does not return exactly one LookupCode for the supplied parameter value | Stop before preparing the QP_DEFAULT_TAX_DETERMINANTS parameter value. Do not infer a lookup code or save the supplied value as the parameter value. Correct the parameter value and repeat the approved read-only lookup. |
| ORA_FOM_CASCAD_HDR_ATTR_TO_LNE lookupCodes does not return exactly one LookupCode for the supplied parameter value | Stop before preparing the QP_CASCAD_HDR_ATTR_TO_LNE parameter value. Do not infer a lookup code or save the supplied value as the parameter value. Correct the parameter value and repeat the approved read-only lookup. |
| ORA_CZ_PRICING_IN_CONFIGURATOR lookupCodes does not return exactly one LookupCode for the supplied parameter value | Stop before preparing the QP_PRICING_IN_CONFIGURATOR parameter value. Do not infer a lookup code or save the supplied value as the parameter value. Correct the parameter value and repeat the approved read-only lookup. |
| ORA_DOO_INCL_ITEM_EXP_DATE lookupCodes does not return exactly one LookupCode for the supplied parameter value | Stop before preparing the QP_INCL_ITEM_EXPLOSION_DATE parameter value. Do not infer a lookup code or save the supplied value as the parameter value. Correct the parameter value and repeat the approved read-only lookup. |
| ORA_FOM_CREDIT_CHK_FAIL_SUBMIT lookupCodes does not return exactly one LookupCode for the supplied parameter value | Stop before preparing the QP_CREDIT_CK_FAILURE_AT_SUBMIT parameter value. Do not infer a lookup code or save the supplied value as the parameter value. Correct the parameter value and repeat the approved read-only lookup. |
| ORA_DOO_DUOM_RETURN_QTY_TYPE lookupCodes does not return exactly one LookupCode for the supplied parameter value | Stop before preparing the QP_DUOM_RETURN_QTY_TYPE parameter value. Do not infer a lookup code or save the supplied value as the parameter value. Correct the parameter value and repeat the approved read-only lookup. |
| ORA_FOM_AUTH_CC_AMT lookupCodes does not return exactly one LookupCode for the supplied parameter value | Stop before preparing the QP_AUTH_CC_AMT parameter value. Do not infer a lookup code or save the supplied value as the parameter value. Correct the parameter value and repeat the approved read-only lookup. |
| ORA_DOO_CONFIG_EFFEC_DATE lookupCodes does not return exactly one LookupCode for the supplied parameter value | Stop before preparing the QP_CONFIG_EFFECTIVE_DATE parameter value. Do not infer a lookup code or save the supplied value as the parameter value. Correct the parameter value and repeat the approved read-only lookup. |
| ORA_DOO_REL_TYPE_SHIP_TO lookupCodes does not return exactly one LookupCode for the supplied parameter value | Stop before preparing the QP_RELATIONSHIP_SHIP_TO_CUST parameter value. Do not infer a lookup code or save the supplied value as the parameter value. Correct the parameter value and repeat the approved read-only lookup. |
| A documented constraint or conditional dependency is not satisfied | Stop before saving. Correct the design or remove the parameter change from scope. |
| Parameter save result is failed or indeterminate | Do not retry automatically. Preserve sanitized diagnostics, verify the current setting read-only through the approved workflow, and resolve the failure before another attempt. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Configuration approval | Target environment, each parameter name and proposed value, documented constraints, and validation evidence. |
| Live save | Explicit approval immediately before saving the unchanged parameter set. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ORDER_MANAGEMENT_PARAMETERS.APPROVAL_GATE | step | 90 | execution_gate | approved-for-separate-execution->RETURN_SUCCESS;approval-missing-or-changed->RETURN_ISSUES | ORDER_MANAGEMENT_PARAMETERS.ENFORCE_DOCUMENTED_CONSTRAINTS | stop | The proposed parameter set passed validation and design enforcement. |
| RETURN_SUCCESS | terminal | 100 | terminal | none | ORDER_MANAGEMENT_PARAMETERS.APPROVAL_GATE | continue | The parameter set is ready for its separate explicit save approval. |
| RETURN_ISSUES | terminal | 110 | terminal | none | none | continue | Input validation, a parameter lookup, a design constraint, or approval gate failed. |
