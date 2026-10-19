# Manage Organization Hierarchies and Classifications Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_current_org_hierarchy_setup | Before an update, removal, replacement, import, or post-change verification | Authorized target task state and fresh target current-data export | Require one target environment and reconcile the visible hierarchy type, selected classifications, and applicable default hierarchy; supplied historical reports are guidance only | Current hierarchy type, classifications, default tree, tree version, starting organization, verification result | Stop; do not infer or merge states from another environment |
| resolve_allowed_hierarchy_type | Before accepting PJF_PROJECT_ORG_HIERARCHY.csv OrgHierarchyTypeCode | Static immutable organization hierarchy type list below, established from Fusion tree-structure and lookup data; no supported add, delete, or maintenance path is identified | Resolve a code, meaning, translation, description, or ordinary natural-language value to exactly one listed member; write its canonical code | OrgHierarchyTypeCode and hierarchy-type meaning | Stop when no listed member or more than one plausible member resolves |
| resolve_available_org_classifications | Before accepting or verifying ORA_PROJECT_ORGANIZATION_CLASSIFICATION.csv ClassificationCode | Static immutable organization classification list below, established from enabled Fusion organization-classification data; no supported add, delete, or maintenance path is identified | Resolve a code, meaning, translation, description, or ordinary natural-language value to exactly one listed member; write its canonical code; separately reconcile requested additions, removals, and preserved values with the target task selection | ClassificationCode and classification meaning; validated additions, removals, and preserved values | Stop when no listed member or more than one plausible member resolves, or when the selected result is empty |
| resolve_default_org_hierarchy | When organization or department hierarchy is selected | Target task tree, active-version, and starting-organization choices | Require one compatible tree, one active version, and one valid starting organization as a single combination | Tree identity, version identity, starting organization | Stop on a missing, inactive, invalid, or ambiguous combination |
| verify_org_hierarchy_fsm_package | Before an FSM package is prepared, previewed, submitted, or verified | Customer-provided or freshly exported target template, current export, metadata, and process log | Require exact task identity, target and release, preserved template metadata, documented members and headers, supported additive operation, and unchanged preview checksum | Validated package contract, operation, member inventory, row counts, checksum, process result | Stop on missing evidence, mismatch, unsupported operation, or more than one candidate contract |

## Organization Hierarchy Types

CSV columns: PJF_PROJECT_ORG_HIERARCHY.csv.OrgHierarchyTypeCode

| Lookup Code | Meaning |
|---|---|
| PER_DEPT_TREE_STRUCTURE | HCM Department Hierarchy Tree Structure |
| PER_ORG_TREE_STRUCTURE | HCM Organization Hierarchy Tree Structure |
| ORA_PJF_NO_TREE_STRUCTURE | None |

## Organization Classifications

CSV columns: ORA_PROJECT_ORGANIZATION_CLASSIFICATION.csv.ClassificationCode

| Lookup Code | Meaning |
|---|---|
| ACCIDENT | Accident Insurance Provider |
| AMW_AUDIT_UNIT | Auditable Unit |
| BEN | Benefit Provider |
| BEN TPA | Third Party Administrator |
| BOM_ECOD | ECO Department |
| CA_PMED | Provincial Medical Carrier |
| CA_TAX_GROUP | Tax Group |
| COLLECTIONS_GROUP | Collections Group |
| CONSTITUENCY | Constituency |
| CONTRACTS_RESOURCE_ORGANIZATION | Contracts Organization |
| CRP | CRP Organization |
| CST | Cost Organization |
| CTB_HEALTHCARE | Healthcare Classification |
| CTB_INT_BUS | Healthcare Business Unit |
| CTB_INT_DATA_CONTROL | Healthcare Data Controller |
| CTB_INT_ENT | Healthcare Enterprise |
| CTB_INT_FAC | Healthcare Facility |
| CTB_INT_MRI | Healthcare Medical Record Issuer |
| CTB_INT_ORDER_FILLER | Healthcare Order Filler |
| CTB_INT_PS | Healthcare Practice Setting |
| DEPARTMENT | Department |
| DE_ADD_SEC_PEN_PROV | German Additional Second Pension Insurance |
| DE_BUD_PLAN | Budget Plan Unit |
| DE_CAP_LIFE_PROV | German Capitalized Life Insurance Provider |
| DE_LIABILITY_INS_PROVIDER | German Workers Liability Insurance Provider |
| DE_MAN_HEALTH_PROV | German Mandatory Health/Special Care Insurance Provider |
| DE_MAN_PENSION_PROV | German Mandatory Pension Insurance Provider |
| DE_PRV_HEALTH_PROV | German Private Health/Special Care Insurance Provider |
| DE_PUB_SEC | German Public Sector |
| DE_SUPERVISING_OFF_ORG | German Work Incident Supervising office |
| DE_TAX_OFFICE | German Tax Office |
| DE_UNEMP_PROV | German Unemployment Insurance Provider |
| DE_VOL_PENSION_PROV | German Voluntary Pension Provider |
| DK_PENSION_PROVIDER | Denmark Pension Provider |
| DK_SERVICE_PROVIDER | Denmark Service Provider |
| EMPLOYER | Employer |
| ENTERPRISE | Enterprise |
| ES_HEALTHCARE_ORG | Healthcare Organization |
| ES_LEGAL_EMPLOYER | Legal Employer (Obsolete) |
| ES_SECTION | Section |
| ES_SS_OFFICE_INFO | Social Security Office |
| ES_SS_PROVINCE_INFO | Social Security Province Office |
| ES_TAX_ADMIN | Tax Administration |
| ES_TAX_OFFICE | Tax Office |
| ES_WORK_CENTER | Work Center |
| FA_ORG | Asset Organization |
| FI_EXTERNAL_COMPANY | External Company |
| FI_LOCAL_UNIT | Finnish Local Unit |
| FI_MAGISTRATE_OFFICE | Finnish Magistrate Office |
| FI_TRADE_UNION | Finnish Trade Union |
| FPT_BANK | Bank Organization |
| FPT_BRANCH | Bank Branch Organization |
| FR_ASSURANCE | Insurance Provider |
| FR_CENTRE_ASSEDIC | ASSEDIC Center |
| FR_CENTRE_URSSAF | URSSAF Center |
| FR_CPAM | CPAM |
| FR_DADS_CRE_ESTAB | DADS-U CRE Establishment |
| FR_DADS_ISSUE_ESTAB | DADS-U Issuing Establishment |
| FR_EMPS_GROUP | Grouping of Employers |
| FR_ETABLISSEMENT | Establishment |
| FR_OPAC | OPCA |
| FR_OPACIF | OPACIF |
| FR_PENSION | Pension Provider |
| FR_PENSION_GROUP | Pension Group |
| FR_PQH_EXT_ORG | Public Sector Other External Organization |
| FR_SOCIETE | Company |
| FUN_BUSINESS_UNIT | Business Unit |
| HCM_BARGAINING_ASSOCIATION | Bargaining Association |
| HCM_DISABILITY_ORGANIZATION | Disability Organization |
| HCM_DIVISION | Division |
| HCM_LEMP | Legal Employer |
| HCM_LRU | Legal Reporting Unit |
| HCM_PAYEE_ORGANIZATION | Payee Organization |
| HCM_PROFESSIONAL_BODY | Professional Body |
| HCM_PSU | Payroll Statutory Unit |
| HCM_REPORTING_ESTABLISHMENT | Reporting Establishment |
| HCM_TRU | Tax Reporting Unit |
| HK_MPF | MPF Trustee |
| HR_AAP | AAP Organization |
| HR_BEN | Beneficiary Organization |
| HR_CA_PROV_REM_INFO | Prov Reporting Establishment |
| HU_COMPANY_INFORMATION | Company Information |
| HU_DRAFT_AGENCY | Draft Agency |
| IE_PENSION | Ireland Pension Provider |
| INV | Inventory Organization |
| IN_COMPANY | Registered Company |
| IN_CONTRACTOR | Contractor |
| IN_ESI_ORG | ESI Organization |
| IN_ESTABLISHMENT | Shops / Establishment |
| IN_FACTORY | Factory |
| IN_PF_ORG | Provident Fund Organization |
| IN_PTAX_ORG | Professional Tax Organization |
| JP_EXTRA_NAME | Extra Names |
| JP_KENKO | Health Insurance Location |
| JP_KIKIN | Welfare Pension Fund Location |
| JP_KOUSEI | Welfare Pension Location |
| JP_ORG_HIST | Organization Name Change History |
| JP_ROUDOU | Labor Insurance Employer |
| JP_TAX_SWOT | Swot |
| KR_BUSINESS_PLACE | Business Place |
| MARKETING_RESOURCE_ORGANIZATION | Marketing Organization |
| MEDICAL_ASSESSMENT_ORG | Medical Service Provider |
| MRP | MRP Organization |
| NL_ORG | Dutch Organization |
| NL_PAYEE_OVERRIDE | Dutch Payee Override |
| NL_PHI_ORG | Dutch Private Health Insurance Organization |
| NL_TAX_OFFICE | Dutch Tax Office |
| NL_UWV | Dutch UWV Organization |
| NO_LOCAL_UNIT | Norwegian Local Unit |
| NO_NI_EXEMPTION_LIMIT | Norwegian Employer Contribution Exemption Limit |
| NO_SOC_SEC_OFFICE | Norwegian Social Security Office |
| ORA_PER_UNION | Worker Union |
| OTA_TC | Training Center |
| PARTNER_RESOURCE_ORG | Partner Organization |
| PAR_ENT | Parent Entity |
| PA_EXPENDITURE_ORG | Project Expenditure Organization |
| PA_INVOICE_ORG | Project Invoice Collection Organization |
| PA_PROJECT_ORG | Project Task Owning Organization |
| PJM | Project Manufacturing Organization |
| PL_INS | Insurance Company |
| PL_SII | PL SII Branch |
| PL_SO | PL Statistic Office |
| PL_TO | PL Tax Office |
| PQP_GB_EDU_AUTH | Education Authority |
| PRJ_PROJECT_UNIT | Project Unit Classification |
| PRNT_ENT | Parent Organization |
| PROV_TAX_OFFICE | Provincial Tax Office |
| REGBOD | Regulatory Body |
| RESOURCE_ORGANIZATION | Resource Organization |
| SALES_RESOURCE_ORG | Sales Organization |
| SA_EMPLOYMENT_OFFICE | Saudi Employment Office |
| SA_GOSI_OFFICE | Saudi GOSI Office |
| SERVICE_RESOURCE_ORGANIZATION | Service Organization |
| SE_ENFORCEMENT_OFFICE | Swedish Enforcement Office |
| SE_LOCAL_UNIT | Swedish Local Unit |
| SE_SOC_SEC_OFFICE | Swedish Social Security Office |
| US_CARRIER | Benefits Carrier |
| US_CRP | Corporate Headquarters |
| US_WC_CARRIER | Workers Compensation Carrier |
| WC_BOARD | Workers Compensation Board |
| WIP | WIP Organization |
| ZA_TP | Training Provider |

## Live Lookups

Before executing any REST lookup below, apply the
[REST version and query compatibility preflight](../../../references/rest-query-compatibility.md)
and the REST request compatibility rule in Lookup Execution Rules. Existing
matching, classification precedence and workflow gates continue to apply.

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| list_organization_classifications_rest_reference | A current read-only reference or audit of the Organization Classifications static table is explicitly requested, including an explicit audit request after repeated input failures | Verified target environment and explicit audit request | GET /hcmRestApi/resources/latest/organizationClassificationsLOV?onlyData=true&limit=500&orderBy=ClassificationCode | ClassificationCode, ClassificationName | Collect all pages through the governed client; require a complete, nonempty collection with both requested fields populated and unique ClassificationCode values. Retain returned codes and names in ClassificationCode order and compare with the static table without changing its validation set | ClassificationCode and ClassificationName -> ClassificationReferenceRows; resolver name, verified target, request path, collection time, row count, completeness, and sanitized evidence reference -> ClassificationReferenceReceipt; differences from the static table -> ClassificationReferenceComparison | Missing preflight evidence, authorization, service or transport failure, zero rows, partial results, malformed rows, or ambiguous duplicate codes produce failure->OHCL.HANDLE_ERROR; do not infer that the static table is invalid |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| REST request compatibility | Before a workflow-selected request, determine framework applicability and the effective REST framework version from the selected core client or workflow. Use compatible query syntax and verify that the outgoing header agrees; never pin an independent pillar version. Apply the linked offering preflight, preserve finder separators and literal values, and stop the affected request on an unresolved version or header/query conflict. |
| A current-data report is supplied | Use it as baseline guidance and reconcile it to the current target; do not treat observed values as defaults or a universal allowed set |
| PJF_PROJECT_ORG_HIERARCHY.csv is validated | Resolve any unambiguous supported input to one code in the static Organization Hierarchy Types table and write the canonical code; the table is the runtime validation source |
| ORA_PROJECT_ORGANIZATION_CLASSIFICATION.csv is validated | Resolve any unambiguous supported input to one code in the static Organization Classifications table and write the canonical code; the table is the runtime validation source |
| A current organization-classification reference is explicitly requested | OHCL.CHECK_CLASSIFICATION_REFERENCE runs list_organization_classifications_rest_reference only after its prerequisites succeed; a complete result and recorded receipt produce resolved->OHCL.RESOLVE_ALLOWED_VALUES |
| No current organization-classification reference is explicitly requested | OHCL.CHECK_CLASSIFICATION_REFERENCE performs no GET and records not_required->OHCL.RESOLVE_ALLOWED_VALUES; an input failure or user confidence alone does not authorize a lookup or bypass static validation |
| The optional reference lookup is selected | Use core.fusion-api.rest-api-client through the active workflow after target identity, read privilege, supported read-only contract, client availability, and safe evidence destination checks; missing checks produce failure before any GET |
| The collection has additional pages | Retrieve all pages of this same target collection through core.fusion-api.rest-api-client; an unavailable page or incomplete collection is failure, not resolved |
| The reference lookup returns data | Preserve the exact returned codes and names and record ClassificationReferenceReceipt in the sanitized runtime record; never persist credentials or protected response material in tracked files |
| The reference differs from the static table | Report ClassificationReferenceComparison for review; never replace the static validation set automatically, accept an otherwise invalid input, generate an import from audit rows, or authorize an import |
| A target template or package fact is required | Resolve it only from the customer's exact target-pod export or template |
| A REST or internal-service lookup is proposed | Do not call it unless a supported read-only customer contract is separately evidenced |
| Target state is inaccessible, ambiguous, or differs from approved scope | Stop and return the missing or conflicting fact |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OHCL.RESOLVE_CURRENT_STATE | decision | 2 | evaluate_result | resolved->OHCL.CHECK_CLASSIFICATION_REFERENCE;missing->OHCL.HANDLE_ERROR | OHCL.VALIDATE_INPUT | stop | Current-state reconciliation is required, or an unchanged create baseline is confirmed |
| OHCL.CHECK_CLASSIFICATION_REFERENCE | step | 3 | reference_lookup | resolved->OHCL.RESOLVE_ALLOWED_VALUES;not_required->OHCL.RESOLVE_ALLOWED_VALUES;failure->OHCL.HANDLE_ERROR | OHCL.RESOLVE_CURRENT_STATE | stop | Evaluate the explicit current-reference request guard for list_organization_classifications_rest_reference; run the governed read only when requested, otherwise return not_required without a GET |
| OHCL.RESOLVE_ALLOWED_VALUES | decision | 4 | evaluate_result | resolved->OHCL.RESOLVE_DEFAULT_HIERARCHY;invalid->OHCL.HANDLE_ERROR | OHCL.CHECK_CLASSIFICATION_REFERENCE | stop | Validate the hierarchy type and classifications |
| OHCL.RESOLVE_DEFAULT_HIERARCHY | decision | 5 | evaluate_result | resolved->OHCL.CHECK_DEPENDENCIES;not_required->OHCL.CHECK_DEPENDENCIES;missing->OHCL.HANDLE_ERROR | OHCL.RESOLVE_ALLOWED_VALUES | stop | Resolve the conditional default hierarchy combination |
| OHCL.VERIFY_TARGET_STATE | decision | 12 | evaluate_result | verified->OHCL.READY;mismatch->OHCL.HANDLE_ERROR | OHCL.LOAD_COMPLETION_GATE | stop | Only on requested setup verification after terminal load success, use the core result/error evidence and a fresh same-task export to compare approved changes and preservation; no verification immediately after submission |

## Refined Target-State Checks

- **BP-014 — Blocking control:** An owning organization must be classified for ownership, belong to the business unit's selected active hierarchy/version, and be active on the effective date.
- **BP-015 — Blocking control:** An expenditure organization must be classified for expenditure, belong to the business unit's selected active hierarchy/version, and be active on the effective date.
