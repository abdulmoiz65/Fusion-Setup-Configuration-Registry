# Configure Payroll Legislations Defaulting Rules

## Evidence Matrix

| Claim or Contract | Source | Source Type | Evidence Status | Release or Date | Limitation |
|---|---|---|---|---|---|
| Column names and data types | Configure Payroll Legislations FSM template metadata | Target-environment FSM template | Observed | Fusion release 11.13.26.10.0; exported 2026-08-12 | The template itself declares no defaults or override policy. |
| Parent-row defaults | Developer-provided functional decision | Authoring input | Confirmed | 2026-08-13 | Applies only when the user explicitly requests Add and omits the corresponding value. It does not establish another business operation or value transformation. |
| HCM-product defaults | User-supplied ORA_PAY_HCM_PRODUCT.csv baseline | Authoring input | Confirmed | 2026-08-13; source SHA-256 51B8F781D7896E1FA89E4F17DE3F9399D25969CE96AEB062669695815447B830 | The one-row default set is retained below. LegislationCode has no default and must be supplied by the user; SeededStatus and PayrollLicense remain explicitly blank in the baseline row. |
| Relationship-type mapping defaults | Developer-provided JSON mapping set | Authoring input | Confirmed | 2026-08-13 | Applies only when the user explicitly requests Add and supplies no relationship-type mapping rows. LegislationCode has no default and must be supplied by the user. |
| Payroll-relationship-rule defaults | User-supplied ORA_LEGISLATION_PAYROLL_RELATIONSHIP_RULE.csv baseline | Authoring input | Confirmed | 2026-08-13; source SHA-256 E4244CBC795451F4AF7BF800D1DF442ED400E936807CA4B9F1B36B1300B1E4DE | The eight-row default set is retained below. LegislationCode has no default and must be supplied by the user. |
| Balance-dimension defaults | User-supplied ORA_LEGISLATION_BALANCE_DIMENSION.csv baseline | Authoring input | Confirmed | 2026-08-13; source SHA-256 9E1574E8ACC2A1B45E66E6118A77032DFA6CCEA379B66F625ED559375FE24110 | The 365-row default set is retained below. It applies only for an explicitly requested Add with no user-supplied balance-dimension rows. LegislationCode remains a user input. |
| Balance-type defaults | User-supplied ORA_LEGISLATION_BALANCE_TYPE.csv baseline and developer clarification | Authoring input | Confirmed | 2026-08-13 | The 28-row default set is retained below. LegislationCode is a user input on every row; CurrencyCode is a user input on the 24 rows that contain a currency in the source. The four confirmed blank CurrencyCode rows remain blank. |
| Component-group defaults | User-supplied ORA_LEGISLATION_COMPONENT_GROUP.csv baseline | Authoring input | Confirmed | 2026-08-13 | The six-row default set is retained below. LegislationCode has no default and must be supplied by the user. |
| Element-classification defaults | User-supplied ORA_LEGISLATION_ELEMENT_CLASSIFICATION.csv baseline | Authoring input | Confirmed | 2026-08-13 | The 119-row default set is retained below. LegislationCode has no default and must be supplied by the user. |
| Payment-type defaults | User-supplied ORA_LEGISLATION_PAYMENT_TYPE.csv baseline | Authoring input | Confirmed | 2026-08-13; source SHA-256 EF9F4316987217D4182F9B9A3D99C951B194B011B617A0E674823567AD592F91 | The four-row default set is retained below. LegislationCode has no default and must be supplied by the user. |

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| ApplicationId | 801 | An explicitly requested new user-supplied ORA_PAY_HCM_PRODUCT row omits ApplicationId | Yes | |
| PayrollLicense | PAY | An explicitly requested new user-supplied ORA_PAY_HCM_PRODUCT row omits PayrollLicense; it does not replace the explicit blank in the complete HCM-product default row set | Yes | |
| AddressStyleCode | POSTAL_ADDR | An explicitly requested new user-supplied ORA_PAY_HCM_PRODUCT row omits AddressStyleCode | Yes | |
| ORA_PAY_HCM_PRODUCT default row set | The exact one durable row in the ORA_PAY_HCM_PRODUCT Durable Default Rows table, including ApplicationId=801, SeededFlag=N, blank SeededStatus, InstalledFlag=Y, blank PayrollLicense, AddressStyleCode=POSTAL_ADDR, and AddressValidationFlag=Y | Add is explicitly requested, the user supplies LegislationCode, and no ORA_PAY_HCM_PRODUCT rows are supplied | Yes | |
| ORA_PAY_HCM_PRODUCT LegislationCode | No default; use the user-supplied LegislationCode on the defaulted row | The HCM-product default row set applies | No | |
| ORA_LEGISLATION_PAYROLL_RELATIONSHIP_TYPE_MAPPING mappings | APL=Element Entries Only; CON=Standard; CWK=Element Entries Only; EMP=Standard; EX_APL=Element Entries Only; EX_EMP=Standard; NONW=Element Entries Only; ORA_CANDIDATE_CWK=Candidate Element Entries Only; ORA_CANDIDATE_EMP=Candidate Standard | Add is explicitly requested, the user supplies LegislationCode, and no mapping rows are supplied | Yes | |
| ORA_LEGISLATION_PAYROLL_RELATIONSHIP_TYPE_MAPPING ViewInstanceName | PayRelationshipTypeMapVO | The relationship-type mapping default set applies | No | |
| ORA_LEGISLATION_PAYROLL_RELATIONSHIP_TYPE_MAPPING GroupingKey | <SystemPersonType>,<LegislationCode>,<RelationshipTypeName> | The relationship-type mapping default set applies | No | |
| ORA_LEGISLATION_PAYROLL_RELATIONSHIP_RULE default row set | The exact eight durable rows in the ORA_LEGISLATION_PAYROLL_RELATIONSHIP_RULE Durable Default Rows table, including RuleMode and RuleType | Add is explicitly requested, the user supplies LegislationCode, and no ORA_LEGISLATION_PAYROLL_RELATIONSHIP_RULE rows are supplied | Yes | |
| ORA_LEGISLATION_PAYROLL_RELATIONSHIP_RULE LegislationCode | No default; use the user-supplied LegislationCode on every defaulted row | The payroll-relationship-rule default set applies | No | |
| ORA_LEGISLATION_BALANCE_DIMENSION default row set | The exact 365 durable rows in the ORA_LEGISLATION_BALANCE_DIMENSION Durable Default Rows table, including DimensionName, BaseDimensionName, ViewInstanceName, DatabaseItemSuffix, and blank LegislativeDataGroupId, DimensionUsageId, and BalanceDimensionId values | Add is explicitly requested, the user supplies LegislationCode, and no ORA_LEGISLATION_BALANCE_DIMENSION rows are supplied | Yes | |
| ORA_LEGISLATION_BALANCE_DIMENSION LegislationCode | No default; use the user-supplied LegislationCode on every defaulted row | The balance-dimension default set applies | No | |
| ORA_LEGISLATION_BALANCE_DIMENSION GroupingKey | Preserve the baseline key shape and replace its final legislation component with the user-supplied LegislationCode | The balance-dimension default set applies | No | |
| ORA_LEGISLATION_BALANCE_TYPE default row set | The exact 28 durable rows in the ORA_LEGISLATION_BALANCE_TYPE Durable Default Rows table, including BalanceName, ViewInstanceName, GroupingKey, BaseBalanceName, and blank LegislativeDataGroupId and BalanceTypeId values | Add is explicitly requested, the user supplies LegislationCode and CurrencyCode, and no ORA_LEGISLATION_BALANCE_TYPE rows are supplied | Yes | |
| ORA_LEGISLATION_BALANCE_TYPE LegislationCode | No default; use the user-supplied LegislationCode on every defaulted row | The balance-type default set applies | No | |
| ORA_LEGISLATION_BALANCE_TYPE CurrencyCode | No default; use the user-supplied CurrencyCode only on the 24 rows marked <CurrencyCode>; preserve the four explicitly blank rows | The balance-type default set applies | No | |
| ORA_LEGISLATION_BALANCE_TYPE GroupingKey | Preserve the baseline key shape and replace its legislation component with the user-supplied LegislationCode | The balance-type default set applies | No | |
| ORA_LEGISLATION_COMPONENT_GROUP default row set | The exact six durable rows in the ORA_LEGISLATION_COMPONENT_GROUP Durable Default Rows table, including BaseName, ViewInstanceName, GroupingKey, Name, and blank DeductionGroupId values | Add is explicitly requested, the user supplies LegislationCode, and no ORA_LEGISLATION_COMPONENT_GROUP rows are supplied | Yes | |
| ORA_LEGISLATION_COMPONENT_GROUP LegislationCode | No default; use the user-supplied LegislationCode on every defaulted row | The component-group default set applies | No | |
| ORA_LEGISLATION_COMPONENT_GROUP GroupingKey | Preserve the baseline key shape and replace its legislation component with the user-supplied LegislationCode | The component-group default set applies | No | |
| ORA_LEGISLATION_ELEMENT_CLASSIFICATION default row set | The exact 119 durable rows in the ORA_LEGISLATION_ELEMENT_CLASSIFICATION Durable Default Rows table, including BaseClassificationName, ViewInstanceName, GroupingKey, ClassificationName, and blank LegislativeDataGroupId and ClassificationId values | Add is explicitly requested, the user supplies LegislationCode, and no ORA_LEGISLATION_ELEMENT_CLASSIFICATION rows are supplied | Yes | |
| ORA_LEGISLATION_ELEMENT_CLASSIFICATION LegislationCode | No default; use the user-supplied LegislationCode on every defaulted row | The element-classification default set applies | No | |
| ORA_LEGISLATION_ELEMENT_CLASSIFICATION GroupingKey | Preserve the baseline key shape and replace its final legislation component with the user-supplied LegislationCode | The element-classification default set applies | No | |
| ORA_LEGISLATION_PAYMENT_TYPE default row set | The exact four durable rows in the ORA_LEGISLATION_PAYMENT_TYPE Durable Default Rows table, including BasePaymentTypeName, ViewInstanceName, GroupingKey, PaymentTypeName, and blank PaymentTypeId values | Add is explicitly requested, the user supplies LegislationCode, and no ORA_LEGISLATION_PAYMENT_TYPE rows are supplied | Yes | |
| ORA_LEGISLATION_PAYMENT_TYPE LegislationCode | No default; use the user-supplied LegislationCode on every defaulted row | The payment-type default set applies | No | |
| ORA_LEGISLATION_PAYMENT_TYPE GroupingKey | Preserve the baseline key shape and replace its legislation component with the user-supplied LegislationCode | The payment-type default set applies | No | |
| Any other attribute | No default confirmed | A value is omitted | No | |

## ORA_PAY_HCM_PRODUCT Durable Default Rows

The following row is the durable, version-controlled HCM-product default set. For an applicable Add, use the row exactly as shown. Replace only the LegislationCode placeholder with the user-supplied LegislationCode. Preserve the explicitly blank SeededStatus and PayrollLicense cells. User-supplied ORA_PAY_HCM_PRODUCT rows override this complete set; the separately documented parent-row defaults apply only when an explicitly supplied row omits their field.

| ApplicationId | LegislationCode | SeededFlag | SeededStatus | InstalledFlag | PayrollLicense | AddressStyleCode | AddressValidationFlag |
|---|---|---|---|---|---|---|---|
| 801 | <LegislationCode> | N |  | Y |  | POSTAL_ADDR | Y |

## ORA_LEGISLATION_PAYROLL_RELATIONSHIP_RULE Durable Default Rows

The following rows are the durable, version-controlled payroll-relationship-rule default set. For an applicable Add, use every row exactly as shown. Replace each LegislationCode placeholder with the user-supplied LegislationCode. User-supplied payroll-relationship-rule rows override this complete set.

| RuleMode | RuleType | LegislationCode |
|---|---|---|
| Y | RUN_RETRO_FORMULA | <LegislationCode> |
| Y | RETRO_RECOVERY | <LegislationCode> |
| AD_ABS_DONATION_POOL | DONATION_POOL_RD | <LegislationCode> |
| OPTIONAL | RETRO_ORG | <LegislationCode> |
| I | I | <LegislationCode> |
| NO_DEDUCTION_CARD | CALC_BREAK | <LegislationCode> |
| NO_DEDUCTION_CARD | GET_TU | <LegislationCode> |
| 1-Jun | L | <LegislationCode> |

## ORA_LEGISLATION_BALANCE_DIMENSION Durable Default Rows

The following rows are the durable, version-controlled balance-dimension default set. For an applicable Add, use every row exactly as shown. Replace each LegislationCode placeholder and only the final legislation component in each GroupingKey with the user-supplied LegislationCode. User-supplied balance-dimension rows override this complete set.

| DimensionName | BaseDimensionName | LegislationCode | ViewInstanceName | GroupingKey | DatabaseItemSuffix | LegislativeDataGroupId | DimensionUsageId | BalanceDimensionId |
|---|---|---|---|---|---|---|---|---|
| Assignment April to Date | Core Assignment April to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_APRTD,null,<LegislationCode> | _ASG_APRTD |  |  |  |
| Assignment August to Date | Core Assignment August to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_AUGTD,null,<LegislationCode> | _ASG_AUGTD |  |  |  |
| Assignment Deduction Type Run | Core Assignment Deduction Type Run | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_DT_RUN,null,<LegislationCode> | _ASG_DT_RUN |  |  |  |
| Assignment Element Entry Inception to Date | Core Assignment Element Entry Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_EE_ITD,null,<LegislationCode> | _ASG_EE_ITD |  |  |  |
| Assignment Element Entry Month to Date | Core Assignment Element Entry Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_EE_MTD,null,<LegislationCode> | _ASG_EE_MTD |  |  |  |
| Assignment Element Entry Period to Date | Core Assignment Element Entry Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_EE_PTD,null,<LegislationCode> | _ASG_EE_PTD |  |  |  |
| Assignment Element Entry Quarter Year to Date | Core Assignment Element Entry Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_EE_QTD,null,<LegislationCode> | _ASG_EE_QTD |  |  |  |
| Assignment Element Entry Year to Date | Core Assignment Element Entry Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_EE_YTD,null,<LegislationCode> | _ASG_EE_YTD |  |  |  |
| Assignment Element Entry, Reference Number Inception to Date | Core Assignment Element Entry,Ref Number Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_EE_RN_ITD,null,<LegislationCode> | _ASG_EE_RN_ITD |  |  |  |
| Assignment Fiscal Quarter Year to Date | Core Assignment Fiscal Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_FQTD,null,<LegislationCode> | _ASG_FQTD |  |  |  |
| Assignment Fiscal Year to Date | Core Assignment Fiscal Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_FYTD,null,<LegislationCode> | _ASG_FYTD |  |  |  |
| Assignment Hire Date Year to Date | Core Assignment Hire Date Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_HDYTD,null,<LegislationCode> | _ASG_HDYTD |  |  |  |
| Assignment Inception to Date | Core Assignment Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_ITD,null,<LegislationCode> | _ASG_ITD |  |  |  |
| Assignment July to Date | Core Assignment July to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_JULTD,null,<LegislationCode> | _ASG_JULTD |  |  |  |
| Assignment Last 12 Months | Core Assignment Last 12 Months | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_L12MTH,null,<LegislationCode> | _ASG_L12MTH |  |  |  |
| Assignment Last 3 Months | Core Assignment Last 3 Months | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_L3MTH,null,<LegislationCode> | _ASG_L3MTH |  |  |  |
| Assignment Month to Date | Core Assignment Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_MTD,null,<LegislationCode> | _ASG_MTD |  |  |  |
| Assignment No Calculation Breakdown Fiscal Quarter Year to Date | Core Assignment NoCB Fiscal Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_NOCB_FQTD,null,<LegislationCode> | _ASG_NOCB_FQTD |  |  |  |
| Assignment No Calculation Breakdown Fiscal Year to Date | Core Assignment NoCB Fiscal Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_NOCB_FYTD,null,<LegislationCode> | _ASG_NOCB_FYTD |  |  |  |
| Assignment No Calculation Breakdown Identification Number Run | Core Assignment NoCB Run | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_NOCB_RUN,null,<LegislationCode> | _ASG_NOCB_RUN |  |  |  |
| Assignment No Calculation Breakdown Inception to Date | Core Assignment NoCB Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_NOCB_ITD,null,<LegislationCode> | _ASG_NOCB_ITD |  |  |  |
| Assignment No Calculation Breakdown Period to Date | Core Assignment NoCB Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_NOCB_PTD,null,<LegislationCode> | _ASG_NOCB_PTD |  |  |  |
| Assignment No Calculation Breakdown Quarter Year to Date | Core Assignment NoCB Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_NOCB_QTD,null,<LegislationCode> | _ASG_NOCB_QTD |  |  |  |
| Assignment No Calculation Breakdown Tax 2 Months to Date | Core Assignment No Calculation Breakdown Tax 2 Months to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_NOCB_T2MTD,null,<LegislationCode> | _ASG_NOCB_T2MTD |  |  |  |
| Assignment No Calculation Breakdown Tax 2 Weeks to Date | Core Assignment No Calculation Breakdown Tax 2 Weeks to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_NOCB_T2WK,null,<LegislationCode> | _ASG_NOCB_T2WK |  |  |  |
| Assignment No Calculation Breakdown Tax 4 Weeks to Date | Core Assignment No Calculation Breakdown Tax 4 Weeks to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_NOCB_T4WK,null,<LegislationCode> | _ASG_NOCB_T4WK |  |  |  |
| Assignment No Calculation Breakdown Tax Half Year to Date | Core Assignment No Calculation Breakdown Tax Half Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_NOCB_THYTD,null,<LegislationCode> | _ASG_NOCB_THYTD |  |  |  |
| Assignment No Calculation Breakdown Tax Month to Date | Core Assignment No Calculation Breakdown Tax Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_NOCB_TMTD,null,<LegislationCode> | _ASG_NOCB_TMTD |  |  |  |
| Assignment No Calculation Breakdown Tax Quarter Year to Date | Core Assignment No Calculation Breakdown Tax Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_NOCB_TQTD,null,<LegislationCode> | _ASG_NOCB_TQTD |  |  |  |
| Assignment No Calculation Breakdown Tax Unit Fiscal Quarter Year to Date | Core Assignment NoCB Tax Unit Fiscal Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_NOCB_TU_FQTD,null,<LegislationCode> | _ASG_NOCB_TU_FQTD |  |  |  |
| Assignment No Calculation Breakdown Tax Unit Fiscal Year to Date | Core Assignment NoCB Tax Unit Fiscal Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_NOCB_TU_FYTD,null,<LegislationCode> | _ASG_NOCB_TU_FYTD |  |  |  |
| Assignment No Calculation Breakdown Tax Unit Inception to Date | Core Assignment NoCB Tax Unit Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_NOCB_TU_ITD,null,<LegislationCode> | _ASG_NOCB_TU_ITD |  |  |  |
| Assignment No Calculation Breakdown Tax Unit Period to Date | Core Assignment NoCB Tax Unit Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_NOCB_TU_PTD,null,<LegislationCode> | _ASG_NOCB_TU_PTD |  |  |  |
| Assignment No Calculation Breakdown Tax Unit Quarter Year to Date | Core Assignment NoCB Tax Unit Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_NOCB_TU_QTD,null,<LegislationCode> | _ASG_NOCB_TU_QTD |  |  |  |
| Assignment No Calculation Breakdown Tax Unit Run | Core Assignment NoCB Tax Unit Run | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_NOCB_TU_RUN,null,<LegislationCode> | _ASG_NOCB_TU_RUN |  |  |  |
| Assignment No Calculation Breakdown Tax Unit Year to Date | Core Assignment NoCB Tax Unit Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_NOCB_TU_YTD,null,<LegislationCode> | _ASG_NOCB_TU_YTD |  |  |  |
| Assignment No Calculation Breakdown Tax Unit, Balance Date,Time Definition Run | Core Assignment NoCB Tax Unit, Balance Date,Time Definition Run | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_NOCB_TU_BD_TD_RUN,null,<LegislationCode> | _ASG_NOCB_TU_BD_TD_RUN |  |  |  |
| Assignment No Calculation Breakdown Tax Week to Date | Core Assignment No Calculation Breakdown Tax Week to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_NOCB_TWK,null,<LegislationCode> | _ASG_NOCB_TWK |  |  |  |
| Assignment No Calculation Breakdown Tax Year to Date | Core Assignment NoCB Tax Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_NOCB_TYTD,null,<LegislationCode> | _ASG_NOCB_TYTD |  |  |  |
| Assignment Period to Date | Core Assignment Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_PTD,null,<LegislationCode> | _ASG_PTD |  |  |  |
| Assignment Quarter Year to Date | Core Assignment Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_QTD,null,<LegislationCode> | _ASG_QTD |  |  |  |
| Assignment Reference Code Inception to Date | Core Assignment Reference Code Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_RC_ITD,null,<LegislationCode> | _ASG_RC_ITD |  |  |  |
| Assignment Reference Code Period to Date | Core Assignment Reference Code Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_RC_PTD,null,<LegislationCode> | _ASG_RC_PTD |  |  |  |
| Assignment Reference Code Run | Core Assignment Reference Code Run | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_RC_RUN,null,<LegislationCode> | _ASG_RC_RUN |  |  |  |
| Assignment Reference Code Year to Date | Core Assignment Reference Code Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_RC_YTD,null,<LegislationCode> | _ASG_RC_YTD |  |  |  |
| Assignment Run | Core Assignment Run | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_RUN,null,<LegislationCode> | _ASG_RUN |  |  |  |
| Assignment Tax 2 Months to Date | Core Assignment Tax 2 Months to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_T2MTD,null,<LegislationCode> | _ASG_T2MTD |  |  |  |
| Assignment Tax 2 Weeks to Date | Core Assignment Tax 2 Weeks to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_T2WK,null,<LegislationCode> | _ASG_T2WK |  |  |  |
| Assignment Tax 4 Weeks to Date | Core Assignment Tax 4 Weeks to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_T4WK,null,<LegislationCode> | _ASG_T4WK |  |  |  |
| Assignment Tax Half Year to Date | Core Assignment Tax Half Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_THYTD,null,<LegislationCode> | _ASG_THYTD |  |  |  |
| Assignment Tax Month to Date | Core Assignment Tax Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_TMTD,null,<LegislationCode> | _ASG_TMTD |  |  |  |
| Assignment Tax Quarter Year to Date | Core Assignment Tax Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_TQTD,null,<LegislationCode> | _ASG_TQTD |  |  |  |
| Assignment Tax Unit Fiscal Quarter Year to Date | Core Assignment Tax Unit Fiscal Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_TU_FQTD,null,<LegislationCode> | _ASG_TU_FQTD |  |  |  |
| Assignment Tax Unit Fiscal Year to Date | Core Assignment Tax Unit Fiscal Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_TU_FYTD,null,<LegislationCode> | _ASG_TU_FYTD |  |  |  |
| Assignment Tax Unit Inception to Date | Core Assignment Tax Unit Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_TU_ITD,null,<LegislationCode> | _ASG_TU_ITD |  |  |  |
| Assignment Tax Unit Month to Date | Core Assignment Tax Unit Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_TU_MTD,null,<LegislationCode> | _ASG_TU_MTD |  |  |  |
| Assignment Tax Unit Period to Date | Core Assignment Tax Unit Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_TU_PTD,null,<LegislationCode> | _ASG_TU_PTD |  |  |  |
| Assignment Tax Unit Quarter Year to Date | Core Assignment Tax Unit Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_TU_QTD,null,<LegislationCode> | _ASG_TU_QTD |  |  |  |
| Assignment Tax Unit Run | Core Assignment Tax Unit Run | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_TU_RUN,null,<LegislationCode> | _ASG_TU_RUN |  |  |  |
| Assignment Tax Unit Tax Quarter Year to Date | Core Assignment Tax Unit Tax Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_TU_TQTD,null,<LegislationCode> | _ASG_TU_TQTD |  |  |  |
| Assignment Tax Unit Tax Year to Date | Core Assignment Tax Unit Tax Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_TU_TYTD,null,<LegislationCode> | _ASG_TU_TYTD |  |  |  |
| Assignment Tax Unit Year to Date | Core Assignment Tax Unit Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_TU_YTD,null,<LegislationCode> | _ASG_TU_YTD |  |  |  |
| Assignment Tax Unit, Reference Code Inception to Date | Core Assignment Tax Unit, Reference Code Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_TU_RC_ITD,null,<LegislationCode> | _ASG_TU_RC_ITD |  |  |  |
| Assignment Tax Unit, Reference Code Month to Date | Core Assignment Tax Unit, Reference Code Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_TU_RC_MTD,null,<LegislationCode> | _ASG_TU_RC_MTD |  |  |  |
| Assignment Tax Unit, Reference Code Period to Date | Core Assignment Tax Unit, Reference Code Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_TU_RC_PTD,null,<LegislationCode> | _ASG_TU_RC_PTD |  |  |  |
| Assignment Tax Unit, Reference Code Quarter to Date | Core Assignment Tax Unit, Reference Code Quarter to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_TU_RC_QTD,null,<LegislationCode> | _ASG_TU_RC_QTD |  |  |  |
| Assignment Tax Unit, Reference Code Run | Core Assignment Tax Unit, Reference Code Run | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_TU_RC_RUN,null,<LegislationCode> | _ASG_TU_RC_RUN |  |  |  |
| Assignment Tax Unit, Reference Code Year to Date | Core Assignment Tax Unit, Reference Code Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_TU_RC_YTD,null,<LegislationCode> | _ASG_TU_RC_YTD |  |  |  |
| Assignment Tax Unit, Reference Number Run | Core Assignment Tax Unit,Ref Number Run | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_TU_RN_RUN,null,<LegislationCode> | _ASG_TU_RN_RUN |  |  |  |
| Assignment Tax Unit,Balance Date,Time Definition Run | Core Assignment Tax Unit,Balance Date,Time Definition Run | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_TU_BD_TD_RUN,null,<LegislationCode> | _ASG_TU_BD_TD_RUN |  |  |  |
| Assignment Tax Week to Date | Core Assignment Tax Week to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_TWK,null,<LegislationCode> | _ASG_TWK |  |  |  |
| Assignment Tax Year to Date | Core Assignment Tax Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_TYTD,null,<LegislationCode> | _ASG_TYTD |  |  |  |
| Assignment Year to Date | Core Assignment Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _ASG_YTD,null,<LegislationCode> | _ASG_YTD |  |  |  |
| Group Deduction Type Inception to Date | Core Group Deduction Type Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_DT_ITD,null,<LegislationCode> | _GRP_DT_ITD |  |  |  |
| Group Deduction Type Run | Core Group Deduction Type Run | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_DT_RUN,null,<LegislationCode> | _GRP_DT_RUN |  |  |  |
| Group Deduction Type Year to Date | Core Group Deduction Type Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_DT_YTD,null,<LegislationCode> | _GRP_DT_YTD |  |  |  |
| Group Month to Date | Core Group Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_MTD,null,<LegislationCode> | _GRP_MTD |  |  |  |
| Group Period to Date | Core Group Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_PTD,null,<LegislationCode> | _GRP_PTD |  |  |  |
| Group Person Inception to Date | Core Group Person Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_PER_ITD,null,<LegislationCode> | _GRP_PER_ITD |  |  |  |
| Group Person Month to Date | Core Group Person Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_PER_MTD,null,<LegislationCode> | _GRP_PER_MTD |  |  |  |
| Group Person Period to Date | Core Group Person Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_PER_PTD,null,<LegislationCode> | _GRP_PER_PTD |  |  |  |
| Group Person Quarter to Date | Core Group Person Quarter to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_PER_QTD,null,<LegislationCode> | _GRP_PER_QTD |  |  |  |
| Group Person Year to Date | Core Group Person Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_PER_YTD,null,<LegislationCode> | _GRP_PER_YTD |  |  |  |
| Group Quarter to Date | Core Group Quarter to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_QTD,null,<LegislationCode> | _GRP_QTD |  |  |  |
| Group Run | Core Group Run | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_RUN,null,<LegislationCode> | _GRP_RUN |  |  |  |
| Group Tax Unit Dynamic Period | Core Group Tax Unit Dynamic Period | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_TU_DYNPRD,null,<LegislationCode> | _GRP_TU_DYNPRD |  |  |  |
| Group Tax Unit Fiscal Quarter Year to Date | Core Group Tax Unit Fiscal Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_TU_FQTD,null,<LegislationCode> | _GRP_TU_FQTD |  |  |  |
| Group Tax Unit Fiscal Year to Date | Core Group Tax Unit Fiscal Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_TU_FYTD,null,<LegislationCode> | _GRP_TU_FYTD |  |  |  |
| Group Tax Unit Inception to Date | Core Group Tax Unit Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_TU_ITD,null,<LegislationCode> | _GRP_TU_ITD |  |  |  |
| Group Tax Unit Last Month | Core Group Tax Unit Last Month | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_TU_LMTH,null,<LegislationCode> | _GRP_TU_LMTH |  |  |  |
| Group Tax Unit Month to Date | Core Group Tax Unit Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_TU_MTD,null,<LegislationCode> | _GRP_TU_MTD |  |  |  |
| Group Tax Unit Period to Date | Core Group Tax Unit Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_TU_PTD,null,<LegislationCode> | _GRP_TU_PTD |  |  |  |
| Group Tax Unit Quarter Year to Date | Core Group Tax Unit Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_TU_QTD,null,<LegislationCode> | _GRP_TU_QTD |  |  |  |
| Group Tax Unit Run | Core Group Tax Unit Run | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_TU_RUN,null,<LegislationCode> | _GRP_TU_RUN |  |  |  |
| Group Tax Unit Tax Year to Date | Core Group Tax Unit Tax Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_TU_TYTD,null,<LegislationCode> | _GRP_TU_TYTD |  |  |  |
| Group Tax Unit Year to Date | Core Group Tax Unit Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_TU_YTD,null,<LegislationCode> | _GRP_TU_YTD |  |  |  |
| Group Tax Unit, Area1, Payroll Dynamic Period | Core Group Tax Unit, Area1, Payroll Dynamic Period | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_TU_AR1_PY_DYNPRD,null,<LegislationCode> | _GRP_TU_AR1_PY_DYNPRD |  |  |  |
| Group Tax Unit, Area1,2, Payroll Dynamic Period | Core Group Tax Unit, Area1,2, Payroll Dynamic Period | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_TU_AR12_PY_DYNPRD,null,<LegislationCode> | _GRP_TU_AR12_PY_DYNPRD |  |  |  |
| Group Tax Unit, Area1,2,3, Payroll Dynamic Period | Core Group Tax Unit, Area1,2,3, Payroll Dynamic Period | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_TU_AR123_PY_DYNPRD,null,<LegislationCode> | _GRP_TU_AR123_PY_DYNPRD |  |  |  |
| Group Tax Unit, Area1,4, Payroll Dynamic Period | Core Group Tax Unit, Area1,4, Payroll Dynamic Period | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_TU_AR14_PY_DYNPRD,null,<LegislationCode> | _GRP_TU_AR14_PY_DYNPRD |  |  |  |
| Group Tax Unit, Deduction Type Inception to Date | Core Group Tax Unit, Deduction Type Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_TU_DT_ITD,null,<LegislationCode> | _GRP_TU_DT_ITD |  |  |  |
| Group Tax Unit, Deduction Type Run | Core Group Tax Unit, Deduction Type Run | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_TU_DT_RUN,null,<LegislationCode> | _GRP_TU_DT_RUN |  |  |  |
| Group Tax Unit, Deduction Type Year to Date | Core Group Tax Unit, Deduction Type Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_TU_DT_YTD,null,<LegislationCode> | _GRP_TU_DT_YTD |  |  |  |
| Group Tax Unit, Payroll Dynamic Period | Core Group Tax Unit, Payroll Dynamic Period | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_TU_PY_DYNPRD,null,<LegislationCode> | _GRP_TU_PY_DYNPRD |  |  |  |
| Group Tax Unit, Reference Number Month to Date | Core Group Tax Unit,Ref Number Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_TU_RN_MTD,null,<LegislationCode> | _GRP_TU_RN_MTD |  |  |  |
| Group Tax Unit, Reference Number Run | Core Group Tax Unit,Ref Number Run | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_TU_RN_RUN,null,<LegislationCode> | _GRP_TU_RN_RUN |  |  |  |
| Group Year to Date | Core Group Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _GRP_YTD,null,<LegislationCode> | _GRP_YTD |  |  |  |
| Relationship Balance Date Time Definition Period to Date | Core Relationship Balance Date Time Definition Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_BD_TDPTD,null,<LegislationCode> | _REL_BD_TDPTD |  |  |  |
| Relationship Balance Date, Payroll Time Definition Period to Date | Core Relationship Balance Date, Payroll Time Definition Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_BD_PY_TDPTD,null,<LegislationCode> | _REL_BD_PY_TDPTD |  |  |  |
| Relationship Balance Date, Reference Code Time Definition Period to Date | Core Relationship Balance Date, Reference Code Time Definition Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_BD_RC_TDPTD,null,<LegislationCode> | _REL_BD_RC_TDPTD |  |  |  |
| Relationship Deduction Type Inception to Date | Core Relationship Deduction Type Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_DT_ITD,null,<LegislationCode> | _REL_DT_ITD |  |  |  |
| Relationship Deduction Type Run | Core Relationship Deduction Type Run | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_DT_RUN,null,<LegislationCode> | _REL_DT_RUN |  |  |  |
| Relationship Deduction Type Year to Date | Core Relationship Deduction Type Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_DT_YTD,null,<LegislationCode> | _REL_DT_YTD |  |  |  |
| Relationship Fiscal Quarter Year to Date | Core Relationship Fiscal Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_FQTD,null,<LegislationCode> | _REL_FQTD |  |  |  |
| Relationship Fiscal Year to Date | Core Relationship Fiscal Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_FYTD,null,<LegislationCode> | _REL_FYTD |  |  |  |
| Relationship Inception to Date | Core Relationship Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_ITD,null,<LegislationCode> | _REL_ITD |  |  |  |
| Relationship Insurance Type Inception to Date | Core Relationship Insurance Type Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_IT_ITD,null,<LegislationCode> | _REL_IT_ITD |  |  |  |
| Relationship Insurance Type Month to Date | Core Relationship Insurance Type Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_IT_MTD,null,<LegislationCode> | _REL_IT_MTD |  |  |  |
| Relationship Insurance Type Period to Date | Core Relationship Insurance Type Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_IT_PTD,null,<LegislationCode> | _REL_IT_PTD |  |  |  |
| Relationship Insurance Type Run | Core Relationship Insurance Type Run | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_IT_RUN,null,<LegislationCode> | _REL_IT_RUN |  |  |  |
| Relationship January 2 Years Ago | Core Relationship January 2 Years Ago | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_JAN2YA,null,<LegislationCode> | _REL_JAN2YA |  |  |  |
| Relationship January 3 Years Ago | Core Relationship January 3 Years Ago | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_JAN3YA,null,<LegislationCode> | _REL_JAN3YA |  |  |  |
| Relationship January 4 Years Ago | Core Relationship January 4 Years Ago | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_JAN4YA,null,<LegislationCode> | _REL_JAN4YA |  |  |  |
| Relationship January 5 Years Ago | Core Relationship January 5 Years Ago | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_JAN5YA,null,<LegislationCode> | _REL_JAN5YA |  |  |  |
| Relationship January 6 Years Ago | Core Relationship January 6 Years Ago | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_JAN6YA,null,<LegislationCode> | _REL_JAN6YA |  |  |  |
| Relationship January 7 Years Ago | Core Relationship January 7 Years Ago | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_JAN7YA,null,<LegislationCode> | _REL_JAN7YA |  |  |  |
| Relationship January 8 Years Ago | Core Relationship January 8 Years Ago | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_JAN8YA,null,<LegislationCode> | _REL_JAN8YA |  |  |  |
| Relationship Last 12 Months | Core Relationship Last 12 Months | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_L12MTH,null,<LegislationCode> | _REL_L12MTH |  |  |  |
| Relationship Last 3 Months | Core Relationship Last 3 Months | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_L3MTH,null,<LegislationCode> | _REL_L3MTH |  |  |  |
| Relationship Last April 1 Month | Core Relationship Last April 1 Month | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_LAPR,null,<LegislationCode> | _REL_LAPR |  |  |  |
| Relationship Last August 1 Month | Core Relationship Last August 1 Month | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_LAUG,null,<LegislationCode> | _REL_LAUG |  |  |  |
| Relationship Last December 1 Month | Core Relationship Last December 1 Month | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_LDEC,null,<LegislationCode> | _REL_LDEC |  |  |  |
| Relationship Last February 1 Month | Core Relationship Last February 1 Month | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_LFEB,null,<LegislationCode> | _REL_LFEB |  |  |  |
| Relationship Last January 1 Month | Core Relationship Last January 1 Month | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_LJAN,null,<LegislationCode> | _REL_LJAN |  |  |  |
| Relationship Last July 1 Month | Core Relationship Last July 1 Month | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_LJUL,null,<LegislationCode> | _REL_LJUL |  |  |  |
| Relationship Last June 1 Month | Core Relationship Last June 1 Month | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_LJUN,null,<LegislationCode> | _REL_LJUN |  |  |  |
| Relationship Last March 1 Month | Core Relationship Last March 1 Month | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_LMAR,null,<LegislationCode> | _REL_LMAR |  |  |  |
| Relationship Last May 1 Month | Core Relationship Last May 1 Month | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_LMAY,null,<LegislationCode> | _REL_LMAY |  |  |  |
| Relationship Last Month | Core Relationship Last Month | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_LMTH,null,<LegislationCode> | _REL_LMTH |  |  |  |
| Relationship Last November 1 Month | Core Relationship Last November 1 Month | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_LNOV,null,<LegislationCode> | _REL_LNOV |  |  |  |
| Relationship Last October 1 Month | Core Relationship Last October 1 Month | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_LOCT,null,<LegislationCode> | _REL_LOCT |  |  |  |
| Relationship Last September 1 Month | Core Relationship Last September 1 Month | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_LSEP,null,<LegislationCode> | _REL_LSEP |  |  |  |
| Relationship Last Year | Core Relationship Last Year | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_LYEAR,null,<LegislationCode> | _REL_LYEAR |  |  |  |
| Relationship Month to Date | Core Relationship Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_MTD,null,<LegislationCode> | _REL_MTD |  |  |  |
| Relationship No Calculation Breakdown ,Statutory Report Type Date Earned Period to Date | Core Relationship No Calculation Breakdown ,Statutory Report Type Date Earned Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_SRT_DEPTD,null,<LegislationCode> | _REL_NOCB_SRT_DEPTD |  |  |  |
| Relationship No Calculation Breakdown Fiscal Quarter Year to Date | Core Relationship NoCB Fiscal Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_FQTD,null,<LegislationCode> | _REL_NOCB_FQTD |  |  |  |
| Relationship No Calculation Breakdown Fiscal Year to Date | Core Relationship NoCB Fiscal Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_FYTD,null,<LegislationCode> | _REL_NOCB_FYTD |  |  |  |
| Relationship No Calculation Breakdown Identification Number Inception to Date | Core Relationship No Calculation Breakdown Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_ITD,null,<LegislationCode> | _REL_NOCB_ITD |  |  |  |
| Relationship No Calculation Breakdown Identification Number Tax Unit Run | Core Relationship No Calculation Breakdown, Tax Unit Run | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_TU_RUN,null,<LegislationCode> | _REL_NOCB_TU_RUN |  |  |  |
| Relationship No Calculation Breakdown Month to Date | Core Relationship NoCB Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_MTD,null,<LegislationCode> | _REL_NOCB_MTD |  |  |  |
| Relationship No Calculation Breakdown Period to Date | Core Relationship NoCB Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_PTD,null,<LegislationCode> | _REL_NOCB_PTD |  |  |  |
| Relationship No Calculation Breakdown Quarter Year to Date | Core Relationship NoCB Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_QTD,null,<LegislationCode> | _REL_NOCB_QTD |  |  |  |
| Relationship No Calculation Breakdown Run | Core Relationship NoCB Run | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_RUN,null,<LegislationCode> | _REL_NOCB_RUN |  |  |  |
| Relationship No Calculation Breakdown Tax 2 Months to Date | Core Relationship No Calculation Breakdown Tax 2 Months to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_T2MTD,null,<LegislationCode> | _REL_NOCB_T2MTD |  |  |  |
| Relationship No Calculation Breakdown Tax 2 Weeks to Date | Core Relationship No Calculation Breakdown Tax 2 Weeks to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_T2WK,null,<LegislationCode> | _REL_NOCB_T2WK |  |  |  |
| Relationship No Calculation Breakdown Tax 4 Weeks to Date | Core Relationship No Calculation Breakdown Tax 4 Weeks to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_T4WK,null,<LegislationCode> | _REL_NOCB_T4WK |  |  |  |
| Relationship No Calculation Breakdown Tax Half Year to Date | Core Relationship No Calculation Breakdown Tax Half Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_THYTD,null,<LegislationCode> | _REL_NOCB_THYTD |  |  |  |
| Relationship No Calculation Breakdown Tax Month to Date | Core Relationship No Calculation Breakdown Tax Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_TMTD,null,<LegislationCode> | _REL_NOCB_TMTD |  |  |  |
| Relationship No Calculation Breakdown Tax Quarter Year to Date | Core Relationship NoCB Tax Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_TQTD,null,<LegislationCode> | _REL_NOCB_TQTD |  |  |  |
| Relationship No Calculation Breakdown Tax Week to Date | Core Relationship No Calculation Breakdown Tax Week to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_TWK,null,<LegislationCode> | _REL_NOCB_TWK |  |  |  |
| Relationship No Calculation Breakdown Tax Year to Date | Core Relationship NoCB Tax Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_TYTD,null,<LegislationCode> | _REL_NOCB_TYTD |  |  |  |
| Relationship No Calculation Breakdown Year to Date | Core Relationship NoCB Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_YTD,null,<LegislationCode> | _REL_NOCB_YTD |  |  |  |
| Relationship No Calculation Breakdown, Deduction Type Inception to Date | Core Relationship No Calculation Breakdown, Deduction Type Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_DT_ITD,null,<LegislationCode> | _REL_NOCB_DT_ITD |  |  |  |
| Relationship No Calculation Breakdown, Deduction Type Run | Core Relationship No Calculation Breakdown, Deduction Type Run | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_DT_RUN,null,<LegislationCode> | _REL_NOCB_DT_RUN |  |  |  |
| Relationship No Calculation Breakdown, Deduction Type Year to Date | Core Relationship No Calculation Breakdown, Deduction Type Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_DT_YTD,null,<LegislationCode> | _REL_NOCB_DT_YTD |  |  |  |
| Relationship No Calculation Breakdown, Insurance Type, Statutory Report Code Run | Core Relationship No Calculation Breakdown, Insurance Type, Statutory Report Code Run | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_IT_SRC_RUN,null,<LegislationCode> | _REL_NOCB_IT_SRC_RUN |  |  |  |
| Relationship No Calculation Breakdown, Reference Code Inception to Date | Core Relationship No Calculation Breakdown, Reference Code Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_RC_ITD,null,<LegislationCode> | _REL_NOCB_RC_ITD |  |  |  |
| Relationship No Calculation Breakdown, Reference Code Period to Date | Core Relationship No Calculation Breakdown, Reference Code Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_RC_PTD,null,<LegislationCode> | _REL_NOCB_RC_PTD |  |  |  |
| Relationship No Calculation Breakdown, Reference Code Run | Core Relationship No Calculation Breakdown, Reference Code Run | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_RC_RUN,null,<LegislationCode> | _REL_NOCB_RC_RUN |  |  |  |
| Relationship No Calculation Breakdown, Reference Code Tax 2 Months to Date | Core Relationship No Calculation Breakdown, Reference Code Tax 2 Months to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_RC_T2MTD,null,<LegislationCode> | _REL_NOCB_RC_T2MTD |  |  |  |
| Relationship No Calculation Breakdown, Reference Code Tax 2 Weeks to Date | Core Relationship No Calculation Breakdown, Reference Code Tax 2 Weeks to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_RC_T2WK,null,<LegislationCode> | _REL_NOCB_RC_T2WK |  |  |  |
| Relationship No Calculation Breakdown, Reference Code Tax 4 Weeks to Date | Core Relationship No Calculation Breakdown, Reference Code Tax 4 Weeks to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_RC_T4WK,null,<LegislationCode> | _REL_NOCB_RC_T4WK |  |  |  |
| Relationship No Calculation Breakdown, Reference Code Tax Half Year to Date | Core Relationship No Calculation Breakdown, Reference Code Tax Half Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_RC_THYTD,null,<LegislationCode> | _REL_NOCB_RC_THYTD |  |  |  |
| Relationship No Calculation Breakdown, Reference Code Tax Month to Date | Core Relationship No Calculation Breakdown, Reference Code Tax Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_RC_TMTD,null,<LegislationCode> | _REL_NOCB_RC_TMTD |  |  |  |
| Relationship No Calculation Breakdown, Reference Code Tax Quarter to Date | Core Relationship No Calculation Breakdown, Reference Code Tax Quarter to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_RC_TQTD,null,<LegislationCode> | _REL_NOCB_RC_TQTD |  |  |  |
| Relationship No Calculation Breakdown, Reference Code Tax Week to Date | Core Relationship No Calculation Breakdown, Reference Code Tax Week to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_RC_TWK,null,<LegislationCode> | _REL_NOCB_RC_TWK |  |  |  |
| Relationship No Calculation Breakdown, Reference Code Tax Year to Date | Core Relationship No Calculation Breakdown, Reference Code Tax Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_RC_TYTD,null,<LegislationCode> | _REL_NOCB_RC_TYTD |  |  |  |
| Relationship No Calculation Breakdown, Reference Number Inception to Date | Core Relationship No Calculation Breakdown, Reference Number Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_RN_ITD,null,<LegislationCode> | _REL_NOCB_RN_ITD |  |  |  |
| Relationship No Calculation Breakdown, Reference Number Month to Date | Core Relationship No Calculation Breakdown, Reference Number Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_RN_MTD,null,<LegislationCode> | _REL_NOCB_RN_MTD |  |  |  |
| Relationship No Calculation Breakdown, Reference Number Period to Date | Core Relationship No Calculation Breakdown, Reference Number Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_RN_PTD,null,<LegislationCode> | _REL_NOCB_RN_PTD |  |  |  |
| Relationship No Calculation Breakdown, Reference Number Run | Core Relationship No Calculation Breakdown, Reference Number Run | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_RN_RUN,null,<LegislationCode> | _REL_NOCB_RN_RUN |  |  |  |
| Relationship No Calculation Breakdown, Reference Number Year to Date | Core Relationship No Calculation Breakdown, Reference Number Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_RN_YTD,null,<LegislationCode> | _REL_NOCB_RN_YTD |  |  |  |
| Relationship No Calculation Breakdown, Statutory Report Type Period to Date | Core Relationship No Calculation Breakdown, Statutory Report Type Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_SRT_PTD,null,<LegislationCode> | _REL_NOCB_SRT_PTD |  |  |  |
| Relationship No Calculation Breakdown, Statutory Report Type Year to Date | Core Relationship No Calculation Breakdown, Statutory Report Type Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_SRT_YTD,null,<LegislationCode> | _REL_NOCB_SRT_YTD |  |  |  |
| Relationship No Calculation Breakdown, Tax Unit Inception to Date | Core Relationship No Calculation Breakdown, Tax Unit Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_TU_ITD,null,<LegislationCode> | _REL_NOCB_TU_ITD |  |  |  |
| Relationship No Calculation Breakdown, Tax Unit, Deduction Type Run | Core Relationship No Calculation Breakdown, Tax Unit, Deduction Type Run | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_TU_DT_RUN,null,<LegislationCode> | _REL_NOCB_TU_DT_RUN |  |  |  |
| Relationship No Calculation Breakdown, Tax Unit, Ref Number Run | Core Relationship No Calculation Breakdown, Tax Unit, Ref Number Run | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_TU_RN_RUN,null,<LegislationCode> | _REL_NOCB_TU_RN_RUN |  |  |  |
| Relationship No Calculation Breakdown, Tax Unit, Reference Code Inception to Date | Core Relationship No Calculation Breakdown, Tax Unit, Reference Code Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_TU_RC_ITD,null,<LegislationCode> | _REL_NOCB_TU_RC_ITD |  |  |  |
| Relationship No Calculation Breakdown, Tax Unit, Reference Code Period to Date | Core Relationship No Calculation Breakdown, Tax Unit, Reference Code Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_TU_RC_PTD,null,<LegislationCode> | _REL_NOCB_TU_RC_PTD |  |  |  |
| Relationship No Calculation Breakdown, Tax Unit, Reference Code Run | Core Relationship No Calculation Breakdown, Tax Unit, Reference Code Run | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_TU_RC_RUN,null,<LegislationCode> | _REL_NOCB_TU_RC_RUN |  |  |  |
| Relationship No Calculation Breakdown, Tax Unit, Reference Code Tax 2 Months to Date | Core Relationship No Calculation Breakdown, Tax Unit, Reference Code Tax 2 Months to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_TU_RC_T2MTD,null,<LegislationCode> | _REL_NOCB_TU_RC_T2MTD |  |  |  |
| Relationship No Calculation Breakdown, Tax Unit, Reference Code Tax 2 Weeks to Date | Core Relationship No Calculation Breakdown, Tax Unit, Reference Code Tax 2 Weeks to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_TU_RC_T2WK,null,<LegislationCode> | _REL_NOCB_TU_RC_T2WK |  |  |  |
| Relationship No Calculation Breakdown, Tax Unit, Reference Code Tax 4 Weeks to Date | Core Relationship No Calculation Breakdown, Tax Unit, Reference Code Tax 4 Weeks to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_TU_RC_T4WK,null,<LegislationCode> | _REL_NOCB_TU_RC_T4WK |  |  |  |
| Relationship No Calculation Breakdown, Tax Unit, Reference Code Tax Half Year to Date | Core Relationship No Calculation Breakdown, Tax Unit, Reference Code Tax Half Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_TU_RC_THYTD,null,<LegislationCode> | _REL_NOCB_TU_RC_THYTD |  |  |  |
| Relationship No Calculation Breakdown, Tax Unit, Reference Code Tax Month to Date | Core Relationship No Calculation Breakdown, Tax Unit, Reference Code Tax Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_TU_RC_TMTD,null,<LegislationCode> | _REL_NOCB_TU_RC_TMTD |  |  |  |
| Relationship No Calculation Breakdown, Tax Unit, Reference Code Tax Quarter to Date | Core Relationship No Calculation Breakdown, Tax Unit, Reference Code Tax Quarter to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_TU_RC_TQTD,null,<LegislationCode> | _REL_NOCB_TU_RC_TQTD |  |  |  |
| Relationship No Calculation Breakdown, Tax Unit, Reference Code Tax Week to Date | Core Relationship No Calculation Breakdown, Tax Unit, Reference Code Tax Week to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_TU_RC_TWK,null,<LegislationCode> | _REL_NOCB_TU_RC_TWK |  |  |  |
| Relationship No Calculation Breakdown, Tax Unit, Reference Code Tax Year to Date | Core Relationship No Calculation Breakdown, Tax Unit, Reference Code Tax Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_NOCB_TU_RC_TYTD,null,<LegislationCode> | _REL_NOCB_TU_RC_TYTD |  |  |  |
| Relationship Payments | Core Relationship Payments | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_PAYMENT,null,<LegislationCode> | _REL_PAYMENT |  |  |  |
| Relationship Payslip | Payroll Relationship Payslip | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_PAYSLIP,null,<LegislationCode> | _REL_PAYSLIP |  |  |  |
| Relationship Period to Date | Core Relationship Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_PTD,null,<LegislationCode> | _REL_PTD |  |  |  |
| Relationship Quarter Year to Date | Core Relationship Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_QTD,null,<LegislationCode> | _REL_QTD |  |  |  |
| Relationship Rate Type Period to Date | Core Relationship Rate Type Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_RT_PTD,null,<LegislationCode> | _REL_RT_PTD |  |  |  |
| Relationship Rate Type Run | Core Relationship Rate Type Run | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_RT_RUN,null,<LegislationCode> | _REL_RT_RUN |  |  |  |
| Relationship Rate Type Year to Date | Core Relationship Rate Type Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_RT_YTD,null,<LegislationCode> | _REL_RT_YTD |  |  |  |
| Relationship Reference Code Inception to Date | Core Relationship Reference Code Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_RC_ITD,null,<LegislationCode> | _REL_RC_ITD |  |  |  |
| Relationship Reference Code Month to Date | Core Relationship Reference Code Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_RC_MTD,null,<LegislationCode> | _REL_RC_MTD |  |  |  |
| Relationship Reference Code Payment | Core Relationship Reference Code Payment | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_RC_PAYMENT,null,<LegislationCode> | _REL_RC_PAYMENT |  |  |  |
| Relationship Reference Code Payslip | Core Relationship Reference Code Payslip | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_RC_PAYSLIP,null,<LegislationCode> | _REL_RC_PAYSLIP |  |  |  |
| Relationship Reference Code Period to Date | Core Relationship Reference Code Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_RC_PTD,null,<LegislationCode> | _REL_RC_PTD |  |  |  |
| Relationship Reference Code Quarter Year to Date | Core Relationship Reference Code Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_RC_QTD,null,<LegislationCode> | _REL_RC_QTD |  |  |  |
| Relationship Reference Code Run | Core Relationship Reference Code Run | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_RC_RUN,null,<LegislationCode> | _REL_RC_RUN |  |  |  |
| Relationship Reference Code Year to Date | Core Relationship Reference Code Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_RC_YTD,null,<LegislationCode> | _REL_RC_YTD |  |  |  |
| Relationship Reference Number Inception to Date | Core Relationship Reference Number Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_RN_ITD,null,<LegislationCode> | _REL_RN_ITD |  |  |  |
| Relationship Reference Number Month to Date | Core Relationship Reference Number Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_RN_MTD,null,<LegislationCode> | _REL_RN_MTD |  |  |  |
| Relationship Reference Number Period to Date | Core Relationship Reference Number Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_RN_PTD,null,<LegislationCode> | _REL_RN_PTD |  |  |  |
| Relationship Reference Number Run | Core Relationship Reference Number Run | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_RN_RUN,null,<LegislationCode> | _REL_RN_RUN |  |  |  |
| Relationship Reference Number Year to Date | Core Relationship Reference Number Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_RN_YTD,null,<LegislationCode> | _REL_RN_YTD |  |  |  |
| Relationship Run | Core Relationship Run | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_RUN,null,<LegislationCode> | _REL_RUN |  |  |  |
| Relationship Statutory Report Type Month to Date | Core Relationship Statutory Report Type Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_SRT_MTD,null,<LegislationCode> | _REL_SRT_MTD |  |  |  |
| Relationship Statutory Report Type Period to Date | Core Relationship Statutory Report Type Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_SRT_PTD,null,<LegislationCode> | _REL_SRT_PTD |  |  |  |
| Relationship Statutory Report Type Quarter Year to Date | Core Relationship Statutory Report Type Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_SRT_QTD,null,<LegislationCode> | _REL_SRT_QTD |  |  |  |
| Relationship Statutory Report Type Run | Core Relationship Statutory Report Type Run | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_SRT_RUN,null,<LegislationCode> | _REL_SRT_RUN |  |  |  |
| Relationship Statutory Report Type Year to Date | Core Relationship Statutory Report Type Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_SRT_YTD,null,<LegislationCode> | _REL_SRT_YTD |  |  |  |
| Relationship Tax 2 Months to Date | Core Relationship Tax 2 Months to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_T2MTD,null,<LegislationCode> | _REL_T2MTD |  |  |  |
| Relationship Tax 2 Weeks to Date | Core Relationship Tax 2 Weeks to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_T2WK,null,<LegislationCode> | _REL_T2WK |  |  |  |
| Relationship Tax 4 Weeks to Date | Core Relationship Tax 4 Weeks to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_T4WK,null,<LegislationCode> | _REL_T4WK |  |  |  |
| Relationship Tax Half Year to Date | Core Relationship Tax Half Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_THYTD,null,<LegislationCode> | _REL_THYTD |  |  |  |
| Relationship Tax Month to Date | Core Relationship Tax Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TMTD,null,<LegislationCode> | _REL_TMTD |  |  |  |
| Relationship Tax Quarter Year to Date | Core Relationship Tax Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TQTD,null,<LegislationCode> | _REL_TQTD |  |  |  |
| Relationship Tax Unit April to Date | Core Relationship Tax Unit April to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_APRTD,null,<LegislationCode> | _REL_TU_APRTD |  |  |  |
| Relationship Tax Unit August to Date | Core Relationship Tax Unit August to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_AUGTD,null,<LegislationCode> | _REL_TU_AUGTD |  |  |  |
| Relationship Tax Unit December to Date | Core Relationship Tax Unit December to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_DECTD,null,<LegislationCode> | _REL_TU_DECTD |  |  |  |
| Relationship Tax Unit February to Date | Core Relationship Tax Unit February to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_FEBTD,null,<LegislationCode> | _REL_TU_FEBTD |  |  |  |
| Relationship Tax Unit Fiscal Quarter Year to Date | Core Relationship Tax Unit Fiscal Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_FQTD,null,<LegislationCode> | _REL_TU_FQTD |  |  |  |
| Relationship Tax Unit Fiscal Year to Date | Core Relationship Tax Unit Fiscal Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_FYTD,null,<LegislationCode> | _REL_TU_FYTD |  |  |  |
| Relationship Tax Unit Inception to Date | Core Relationship Tax Unit Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_ITD,null,<LegislationCode> | _REL_TU_ITD |  |  |  |
| Relationship Tax Unit July to Date | Core Relationship Tax Unit July to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_JULTD,null,<LegislationCode> | _REL_TU_JULTD |  |  |  |
| Relationship Tax Unit June to Date | Core Relationship Tax Unit June to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_JUNTD,null,<LegislationCode> | _REL_TU_JUNTD |  |  |  |
| Relationship Tax Unit March to Date | Core Relationship Tax Unit March to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_MARTD,null,<LegislationCode> | _REL_TU_MARTD |  |  |  |
| Relationship Tax Unit May to Date | Core Relationship Tax Unit May to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_MAYTD,null,<LegislationCode> | _REL_TU_MAYTD |  |  |  |
| Relationship Tax Unit Month to Date | Core Relationship Tax Unit Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_MTD,null,<LegislationCode> | _REL_TU_MTD |  |  |  |
| Relationship Tax Unit November to Date | Core Relationship Tax Unit November to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_NOVTD,null,<LegislationCode> | _REL_TU_NOVTD |  |  |  |
| Relationship Tax Unit October to Date | Core Relationship Tax Unit October to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_OCTTD,null,<LegislationCode> | _REL_TU_OCTTD |  |  |  |
| Relationship Tax Unit Payment | Core Relationship Tax Unit Payment | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_PAYMENT,null,<LegislationCode> | _REL_TU_PAYMENT |  |  |  |
| Relationship Tax Unit Payslip | Core Relationship Tax Unit Payslip | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_PAYSLIP,null,<LegislationCode> | _REL_TU_PAYSLIP |  |  |  |
| Relationship Tax Unit Period to Date | Core Relationship Tax Unit Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_PTD,null,<LegislationCode> | _REL_TU_PTD |  |  |  |
| Relationship Tax Unit Quarter Year to Date | Core Relationship Tax Unit Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_QTD,null,<LegislationCode> | _REL_TU_QTD |  |  |  |
| Relationship Tax Unit Run | Core Relationship Tax Unit Run | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_RUN,null,<LegislationCode> | _REL_TU_RUN |  |  |  |
| Relationship Tax Unit September to Date | Core Relationship Tax Unit September to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_SEPTD,null,<LegislationCode> | _REL_TU_SEPTD |  |  |  |
| Relationship Tax Unit Tax Quarter Year to Date | Core Relationship Tax Unit Tax Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_TQTD,null,<LegislationCode> | _REL_TU_TQTD |  |  |  |
| Relationship Tax Unit Tax Year to Date | Core Relationship Tax Unit Tax Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_TYTD,null,<LegislationCode> | _REL_TU_TYTD |  |  |  |
| Relationship Tax Unit Year to Date | Core Relationship Tax Unit Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_YTD,null,<LegislationCode> | _REL_TU_YTD |  |  |  |
| Relationship Tax Unit, Balance Date Time Definition Period to Date | Core Relationship Tax Unit, Balance Date Time Definition Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_BD_TDPTD,null,<LegislationCode> | _REL_TU_BD_TDPTD |  |  |  |
| Relationship Tax Unit, Balance Date, Payroll Time Definition Period to Date | Core Relationship Tax Unit, Balance Date, Payroll Time Definition Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_BD_PY_TDPTD,null,<LegislationCode> | _REL_TU_BD_PY_TDPTD |  |  |  |
| Relationship Tax Unit, Deduction Card ID Inception to Date | Core Relationship Tax Unit,DedCard Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_DC_ITD,null,<LegislationCode> | _REL_TU_DC_ITD |  |  |  |
| Relationship Tax Unit, Deduction Card ID Period to Date | Core Relationship Tax Unit,DedCard Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_DC_PTD,null,<LegislationCode> | _REL_TU_DC_PTD |  |  |  |
| Relationship Tax Unit, Deduction Card ID Run | Core Relationship Tax Unit,DedCard Run | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_DC_RUN,null,<LegislationCode> | _REL_TU_DC_RUN |  |  |  |
| Relationship Tax Unit, Deduction Type Inception to Date | Core Relationship Tax Unit, Deduction Type Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_DT_ITD,null,<LegislationCode> | _REL_TU_DT_ITD |  |  |  |
| Relationship Tax Unit, Deduction Type Run | Core Relationship Tax Unit, Deduction Type Run | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_DT_RUN,null,<LegislationCode> | _REL_TU_DT_RUN |  |  |  |
| Relationship Tax Unit, Deduction Type Year to Date | Core Relationship Tax Unit, Deduction Type Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_DT_YTD,null,<LegislationCode> | _REL_TU_DT_YTD |  |  |  |
| Relationship Tax Unit, Reference Code Inception to Date | Core Relationship Tax Unit, Reference Code Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_RC_ITD,null,<LegislationCode> | _REL_TU_RC_ITD |  |  |  |
| Relationship Tax Unit, Reference Code Month to Date | Core Relationship Tax Unit, Reference Code Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_RC_MTD,null,<LegislationCode> | _REL_TU_RC_MTD |  |  |  |
| Relationship Tax Unit, Reference Code Payment | Core Relationship Tax Unit, Reference Code Payment | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_RC_PAYMENT,null,<LegislationCode> | _REL_TU_RC_PAYMENT |  |  |  |
| Relationship Tax Unit, Reference Code Payslip | Core Relationship Tax Unit, Reference Code Payslip | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_RC_PAYSLIP,null,<LegislationCode> | _REL_TU_RC_PAYSLIP |  |  |  |
| Relationship Tax Unit, Reference Code Period to Date | Core Relationship Tax Unit, Reference Code Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_RC_PTD,null,<LegislationCode> | _REL_TU_RC_PTD |  |  |  |
| Relationship Tax Unit, Reference Code Quarter Year to Date | Core Relationship Tax Unit, Reference Code Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_RC_QTD,null,<LegislationCode> | _REL_TU_RC_QTD |  |  |  |
| Relationship Tax Unit, Reference Code Run | Core Relationship Tax Unit, Reference Code Run | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_RC_RUN,null,<LegislationCode> | _REL_TU_RC_RUN |  |  |  |
| Relationship Tax Unit, Reference Code Tax 2 Months to Date | Core Relationship Tax Unit, Reference Code Tax 2 Months to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_RC_T2MTD,null,<LegislationCode> | _REL_TU_RC_T2MTD |  |  |  |
| Relationship Tax Unit, Reference Code Tax 2 Weeks to Date | Core Relationship Tax Unit, Reference Code Tax 2 Weeks to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_RC_T2WK,null,<LegislationCode> | _REL_TU_RC_T2WK |  |  |  |
| Relationship Tax Unit, Reference Code Tax 4 Weeks to Date | Core Relationship Tax Unit, Reference Code Tax 4 Weeks to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_RC_T4WK,null,<LegislationCode> | _REL_TU_RC_T4WK |  |  |  |
| Relationship Tax Unit, Reference Code Tax Half Year to Date | Core Relationship Tax Unit, Reference Code Tax Half Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_RC_THYTD,null,<LegislationCode> | _REL_TU_RC_THYTD |  |  |  |
| Relationship Tax Unit, Reference Code Tax Month to Date | Core Relationship Tax Unit, Reference Code Tax Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_RC_TMTD,null,<LegislationCode> | _REL_TU_RC_TMTD |  |  |  |
| Relationship Tax Unit, Reference Code Tax Quarter to Date | Core Relationship Tax Unit, Reference Code Tax Quarter to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_RC_TQTD,null,<LegislationCode> | _REL_TU_RC_TQTD |  |  |  |
| Relationship Tax Unit, Reference Code Tax Week to Date | Core Relationship Tax Unit, Reference Code Tax Week to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_RC_TWK,null,<LegislationCode> | _REL_TU_RC_TWK |  |  |  |
| Relationship Tax Unit, Reference Code Tax Year to Date | Core Relationship Tax Unit, Reference Code Tax Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_RC_TYTD,null,<LegislationCode> | _REL_TU_RC_TYTD |  |  |  |
| Relationship Tax Unit, Reference Code Year to Date | Core Relationship Tax Unit, Reference Code Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_RC_YTD,null,<LegislationCode> | _REL_TU_RC_YTD |  |  |  |
| Relationship Tax Unit, Reference Number Month to Date | Core Relationship Tax Unit, Reference Number Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_RN_MTD,null,<LegislationCode> | _REL_TU_RN_MTD |  |  |  |
| Relationship Tax Unit, Reference Number Period to Date | Core Relationship Tax Unit, Reference Number Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_RN_PTD,null,<LegislationCode> | _REL_TU_RN_PTD |  |  |  |
| Relationship Tax Unit, Reference Number Quarter Year to Date | Core Relationship Tax Unit, Reference Number Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_RN_QTD,null,<LegislationCode> | _REL_TU_RN_QTD |  |  |  |
| Relationship Tax Unit, Reference Number Run | Core Relationship Tax Unit, Reference Number Run | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_RN_RUN,null,<LegislationCode> | _REL_TU_RN_RUN |  |  |  |
| Relationship Tax Unit, Reference Number Year to Date | Core Relationship Tax Unit, Reference Number Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_RN_YTD,null,<LegislationCode> | _REL_TU_RN_YTD |  |  |  |
| Relationship Tax Unit, Third Party Payee Month to Date | Core Relationship Tax Unit, Third Party Payee Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_TPP_MTD,null,<LegislationCode> | _REL_TU_TPP_MTD |  |  |  |
| Relationship Tax Unit, Third Party Payee Payslip | Core Relationship Tax Unit, Third Party Payee Payslip | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_TPP_PAYSLIP,null,<LegislationCode> | _REL_TU_TPP_PAYSLIP |  |  |  |
| Relationship Tax Unit, Third Party Payee Period to Date | Core Relationship Tax Unit, Third Party Payee Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_TPP_PTD,null,<LegislationCode> | _REL_TU_TPP_PTD |  |  |  |
| Relationship Tax Unit, Third Party Payee Run | Core Relationship Tax Unit, Third Party Payee Run | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_TPP_RUN,null,<LegislationCode> | _REL_TU_TPP_RUN |  |  |  |
| Relationship Tax Unit, Third Party Payee Tax Year to Date | Core Relationship Tax Unit, Third Party Payee Tax Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_TPP_TYTD,null,<LegislationCode> | _REL_TU_TPP_TYTD |  |  |  |
| Relationship Tax Unit, Third Party Payee, Reference Code Inception to Date | Core Relationship Tax Unit, Third Party Payee, Reference Code Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_TPP_RC_ITD,null,<LegislationCode> | _REL_TU_TPP_RC_ITD |  |  |  |
| Relationship Tax Unit, Third Party Payee, Reference Code Month to Date | Core Relationship Tax Unit, Third Party Payee, Reference Code Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_TPP_RC_MTD,null,<LegislationCode> | _REL_TU_TPP_RC_MTD |  |  |  |
| Relationship Tax Unit, Third Party Payee, Reference Code Payment | Core Relationship Tax Unit, Third Party Payee, Reference Code Payment | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_TPP_RC_PAYMENT,null,<LegislationCode> | _REL_TU_TPP_RC_PAYMENT |  |  |  |
| Relationship Tax Unit, Third Party Payee, Reference Code Payslip | Core Relationship Tax Unit, Third Party Payee, Reference Code Payslip | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_TPP_RC_PAYSLIP,null,<LegislationCode> | _REL_TU_TPP_RC_PAYSLIP |  |  |  |
| Relationship Tax Unit, Third Party Payee, Reference Code Period to Date | Core Relationship Tax Unit, Third Party Payee, Reference Code Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_TPP_RC_PTD,null,<LegislationCode> | _REL_TU_TPP_RC_PTD |  |  |  |
| Relationship Tax Unit, Third Party Payee, Reference Code Quarter Year to Date | Core Relationship Tax Unit, Third Party Payee, Reference Code Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_TPP_RC_QTD,null,<LegislationCode> | _REL_TU_TPP_RC_QTD |  |  |  |
| Relationship Tax Unit, Third Party Payee, Reference Code Run | Core Relationship Tax Unit, Third Party Payee, Reference Code Run | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_TPP_RC_RUN,null,<LegislationCode> | _REL_TU_TPP_RC_RUN |  |  |  |
| Relationship Tax Unit, Third Party Payee, Reference Code Year to Date | Core Relationship Tax Unit, Third Party Payee, Reference Code Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TU_TPP_RC_YTD,null,<LegislationCode> | _REL_TU_TPP_RC_YTD |  |  |  |
| Relationship Tax Week to Date | Core Relationship Tax Week to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TWK,null,<LegislationCode> | _REL_TWK |  |  |  |
| Relationship Tax Year to Date | Core Relationship Tax Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TYTD,null,<LegislationCode> | _REL_TYTD |  |  |  |
| Relationship Third Party Payee, Reference Code Inception to Date | Core Relationship Third Party Payee, Reference Code Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TPP_RC_ITD,null,<LegislationCode> | _REL_TPP_RC_ITD |  |  |  |
| Relationship Third Party Payee, Reference Code Month to Date | Core Relationship Third Party Payee, Reference Code Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TPP_RC_MTD,null,<LegislationCode> | _REL_TPP_RC_MTD |  |  |  |
| Relationship Third Party Payee, Reference Code Payment | Core Relationship Third Party Payee, Reference Code Payment | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TPP_RC_PAYMENT,null,<LegislationCode> | _REL_TPP_RC_PAYMENT |  |  |  |
| Relationship Third Party Payee, Reference Code Payslip | Core Relationship Third Party Payee, Reference Code Payslip | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TPP_RC_PAYSLIP,null,<LegislationCode> | _REL_TPP_RC_PAYSLIP |  |  |  |
| Relationship Third Party Payee, Reference Code Quarter Year to Date | Core Relationship Third Party Payee, Reference Code Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TPP_RC_QTD,null,<LegislationCode> | _REL_TPP_RC_QTD |  |  |  |
| Relationship Third Party Payee, Reference Code Run | Core Relationship Third Party Payee, Reference Code Run | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TPP_RC_RUN,null,<LegislationCode> | _REL_TPP_RC_RUN |  |  |  |
| Relationship Third Party Payee, Reference Code Year to Date | Core Relationship Third Party Payee, Reference Code Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TPP_RC_YTD,null,<LegislationCode> | _REL_TPP_RC_YTD |  |  |  |
| Relationship Third Party Payment Payslip | Core Relationship Party Payslip | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TPP_PAYSLIP,null,<LegislationCode> | _REL_TPP_PAYSLIP |  |  |  |
| Relationship Third Party Payments | Core Relationship Party Payments | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_TPP_PAYMENT,null,<LegislationCode> | _REL_TPP_PAYMENT |  |  |  |
| Relationship Year to Date | Core Relationship Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _REL_YTD,null,<LegislationCode> | _REL_YTD |  |  |  |
| Term Inception to Date | Core Terms Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_ITD,null,<LegislationCode> | _TRM_ITD |  |  |  |
| Term Last 12 Months | Core Term Last 12 Months | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_L12MTH,null,<LegislationCode> | _TRM_L12MTH |  |  |  |
| Term Last 3 Months | Core Term Last 3 Months | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_L3MTH,null,<LegislationCode> | _TRM_L3MTH |  |  |  |
| Term Month to Date | Core Terms Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_MTD,null,<LegislationCode> | _TRM_MTD |  |  |  |
| Term No Calculation Breakdown Identification Number Inception to Date | Core Term No Calculation Breakdown Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_NOCB_ITD,null,<LegislationCode> | _TRM_NOCB_ITD |  |  |  |
| Term No Calculation Breakdown Identification Number Period to Date | Core Term No Calculation Breakdown Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_NOCB_PTD,null,<LegislationCode> | _TRM_NOCB_PTD |  |  |  |
| Term No Calculation Breakdown Identification Number Run | Core Term No Calculation Breakdown Run | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_NOCB_RUN,null,<LegislationCode> | _TRM_NOCB_RUN |  |  |  |
| Term No Calculation Breakdown Tax 2 Months to Date | Core Term No Calculation Breakdown Tax 2 Months to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_NOCB_T2MTD,null,<LegislationCode> | _TRM_NOCB_T2MTD |  |  |  |
| Term No Calculation Breakdown Tax 2 Weeks to Date | Core Term No Calculation Breakdown Tax 2 Weeks to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_NOCB_T2WK,null,<LegislationCode> | _TRM_NOCB_T2WK |  |  |  |
| Term No Calculation Breakdown Tax 4 Weeks to Date | Core Term No Calculation Breakdown Tax 4 Weeks to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_NOCB_T4WK,null,<LegislationCode> | _TRM_NOCB_T4WK |  |  |  |
| Term No Calculation Breakdown Tax Half Year to Date | Core Term No Calculation Breakdown Tax Half Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_NOCB_THYTD,null,<LegislationCode> | _TRM_NOCB_THYTD |  |  |  |
| Term No Calculation Breakdown Tax Month to Date | Core Term No Calculation Breakdown Tax Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_NOCB_TMTD,null,<LegislationCode> | _TRM_NOCB_TMTD |  |  |  |
| Term No Calculation Breakdown Tax Quarter Year to Date | Core Term No Calculation Breakdown Tax Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_NOCB_TQTD,null,<LegislationCode> | _TRM_NOCB_TQTD |  |  |  |
| Term No Calculation Breakdown Tax Week to Date | Core Term No Calculation Breakdown Tax Week to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_NOCB_TWK,null,<LegislationCode> | _TRM_NOCB_TWK |  |  |  |
| Term No Calculation Breakdown Tax Year to Date | Core Term No Calculation Breakdown Tax Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_NOCB_TYTD,null,<LegislationCode> | _TRM_NOCB_TYTD |  |  |  |
| Term No Calculation Breakdown, Tax Unit, Reference Code Inception to Date | Core Term No Calculation Breakdown, Tax Unit, Reference Code Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_NOCB_TU_RC_ITD,null,<LegislationCode> | _TRM_NOCB_TU_RC_ITD |  |  |  |
| Term No Calculation Breakdown, Tax Unit, Reference Code Period to Date | Core Term No Calculation Breakdown, Tax Unit, Reference Code Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_NOCB_TU_RC_PTD,null,<LegislationCode> | _TRM_NOCB_TU_RC_PTD |  |  |  |
| Term No Calculation Breakdown, Tax Unit, Reference Code Run | Core Term No Calculation Breakdown, Tax Unit, Reference Code Run | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_NOCB_TU_RC_RUN,null,<LegislationCode> | _TRM_NOCB_TU_RC_RUN |  |  |  |
| Term No Calculation Breakdown, Tax Unit, Reference Code Tax 2 Months to Date | Core Term No Calculation Breakdown, Tax Unit, Reference Code Tax 2 Months to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_NOCB_TU_RC_T2MTD,null,<LegislationCode> | _TRM_NOCB_TU_RC_T2MTD |  |  |  |
| Term No Calculation Breakdown, Tax Unit, Reference Code Tax 2 Weeks to Date | Core Term No Calculation Breakdown, Tax Unit, Reference Code Tax 2 Weeks to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_NOCB_TU_RC_T2WK,null,<LegislationCode> | _TRM_NOCB_TU_RC_T2WK |  |  |  |
| Term No Calculation Breakdown, Tax Unit, Reference Code Tax 4 Weeks to Date | Core Term No Calculation Breakdown, Tax Unit, Reference Code Tax 4 Weeks to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_NOCB_TU_RC_T4WK,null,<LegislationCode> | _TRM_NOCB_TU_RC_T4WK |  |  |  |
| Term No Calculation Breakdown, Tax Unit, Reference Code Tax Half Year to Date | Core Term No Calculation Breakdown, Tax Unit, Reference Code Tax Half Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_NOCB_TU_RC_THYTD,null,<LegislationCode> | _TRM_NOCB_TU_RC_THYTD |  |  |  |
| Term No Calculation Breakdown, Tax Unit, Reference Code Tax Month to Date | Core Term No Calculation Breakdown, Tax Unit, Reference Code Tax Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_NOCB_TU_RC_TMTD,null,<LegislationCode> | _TRM_NOCB_TU_RC_TMTD |  |  |  |
| Term No Calculation Breakdown, Tax Unit, Reference Code Tax Quarter to Date | Core Term No Calculation Breakdown, Tax Unit, Reference Code Tax Quarter to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_NOCB_TU_RC_TQTD,null,<LegislationCode> | _TRM_NOCB_TU_RC_TQTD |  |  |  |
| Term No Calculation Breakdown, Tax Unit, Reference Code Tax Week to Date | Core Term No Calculation Breakdown, Tax Unit, Reference Code Tax Week to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_NOCB_TU_RC_TWK,null,<LegislationCode> | _TRM_NOCB_TU_RC_TWK |  |  |  |
| Term No Calculation Breakdown, Tax Unit, Reference Code Tax Year to Date | Core Term No Calculation Breakdown, Tax Unit, Reference Code Tax Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_NOCB_TU_RC_TYTD,null,<LegislationCode> | _TRM_NOCB_TU_RC_TYTD |  |  |  |
| Term Payslip | Core Term Payslip | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_PAYSLIP,null,<LegislationCode> | _TRM_PAYSLIP |  |  |  |
| Term Period to Date | Core Terms Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_PTD,null,<LegislationCode> | _TRM_PTD |  |  |  |
| Term Quarter Year to Date | Core Terms Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_QTD,null,<LegislationCode> | _TRM_QTD |  |  |  |
| Term Reference Code Inception to Date | Core Term Reference Code Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_RC_ITD,null,<LegislationCode> | _TRM_RC_ITD |  |  |  |
| Term Reference Code Period to Date | Core Term Reference Code Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_RC_PTD,null,<LegislationCode> | _TRM_RC_PTD |  |  |  |
| Term Reference Code Run | Core Term Reference Code Run | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_RC_RUN,null,<LegislationCode> | _TRM_RC_RUN |  |  |  |
| Term Run | Core Terms Run | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_RUN,null,<LegislationCode> | _TRM_RUN |  |  |  |
| Term Tax Unit Month to Date | Core Terms Tax Unit Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_TU_MTD,null,<LegislationCode> | _TRM_TU_MTD |  |  |  |
| Term Tax Unit Payslip | Core Term Tax Unit Payslip | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_TU_PAYSLIP,null,<LegislationCode> | _TRM_TU_PAYSLIP |  |  |  |
| Term Tax Unit Quarter to Date | Core Terms Tax Unit Quarter Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_TU_QTD,null,<LegislationCode> | _TRM_TU_QTD |  |  |  |
| Term Tax Unit Run | Core Terms Tax Unit Run | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_TU_RUN,null,<LegislationCode> | _TRM_TU_RUN |  |  |  |
| Term Tax Unit Tax Year to Date | Core Term Tax Unit Tax Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_TU_TYTD,null,<LegislationCode> | _TRM_TU_TYTD |  |  |  |
| Term Tax Unit Year to Date | Core Terms Tax Unit Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_TU_YTD,null,<LegislationCode> | _TRM_TU_YTD |  |  |  |
| Term Tax Unit, Reference Code Inception to Date | Core Term Tax Unit, Reference Code Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_TU_RC_ITD,null,<LegislationCode> | _TRM_TU_RC_ITD |  |  |  |
| Term Tax Unit, Reference Code Month to Date | Core Term Tax Unit, Reference Code Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_TU_RC_MTD,null,<LegislationCode> | _TRM_TU_RC_MTD |  |  |  |
| Term Tax Unit, Reference Code Period to Date | Core Term Tax Unit, Reference Code Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_TU_RC_PTD,null,<LegislationCode> | _TRM_TU_RC_PTD |  |  |  |
| Term Tax Unit, Reference Code Quarter to Date | Core Term Tax Unit, Reference Code Quarter to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_TU_RC_QTD,null,<LegislationCode> | _TRM_TU_RC_QTD |  |  |  |
| Term Tax Unit, Reference Code Run | Core Term Tax Unit, Reference Code Run | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_TU_RC_RUN,null,<LegislationCode> | _TRM_TU_RC_RUN |  |  |  |
| Term Tax Unit, Reference Code Tax 2 Months to Date | Core Term Tax Unit, Reference Code Tax 2 Months to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_TU_RC_T2MTD,null,<LegislationCode> | _TRM_TU_RC_T2MTD |  |  |  |
| Term Tax Unit, Reference Code Tax 2 Weeks to Date | Core Term Tax Unit, Reference Code Tax 2 Weeks to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_TU_RC_T2WK,null,<LegislationCode> | _TRM_TU_RC_T2WK |  |  |  |
| Term Tax Unit, Reference Code Tax 4 Weeks to Date | Core Term Tax Unit, Reference Code Tax 4 Weeks to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_TU_RC_T4WK,null,<LegislationCode> | _TRM_TU_RC_T4WK |  |  |  |
| Term Tax Unit, Reference Code Tax Half Year to Date | Core Term Tax Unit, Reference Code Tax Half Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_TU_RC_THYTD,null,<LegislationCode> | _TRM_TU_RC_THYTD |  |  |  |
| Term Tax Unit, Reference Code Tax Month to Date | Core Term Tax Unit, Reference Code Tax Month to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_TU_RC_TMTD,null,<LegislationCode> | _TRM_TU_RC_TMTD |  |  |  |
| Term Tax Unit, Reference Code Tax Quarter to Date | Core Term Tax Unit, Reference Code Tax Quarter to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_TU_RC_TQTD,null,<LegislationCode> | _TRM_TU_RC_TQTD |  |  |  |
| Term Tax Unit, Reference Code Tax Week to Date | Core Term Tax Unit, Reference Code Tax Week to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_TU_RC_TWK,null,<LegislationCode> | _TRM_TU_RC_TWK |  |  |  |
| Term Tax Unit, Reference Code Tax Year to Date | Core Term Tax Unit, Reference Code Tax Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_TU_RC_TYTD,null,<LegislationCode> | _TRM_TU_RC_TYTD |  |  |  |
| Term Tax Unit, Reference Code Year to Date | Core Term Tax Unit, Reference Code Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_TU_RC_YTD,null,<LegislationCode> | _TRM_TU_RC_YTD |  |  |  |
| Term Year to Date | Core Terms Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_YTD,null,<LegislationCode> | _TRM_YTD |  |  |  |
| Terms Fiscal Year to Date | Core Terms Fiscal Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_FYTD,null,<LegislationCode> | _TRM_FYTD |  |  |  |
| Terms Tax Unit Inception to Date | Core Terms Tax Unit Inception to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_TU_ITD,null,<LegislationCode> | _TRM_TU_ITD |  |  |  |
| Terms Tax Unit Period to Date | Core Terms Tax Unit Period to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_TU_PTD,null,<LegislationCode> | _TRM_TU_PTD |  |  |  |
| Terms Tax Year to Date | Core Terms Tax Year to Date | <LegislationCode> | PayBalanceDimensionUsageVO | _TRM_TYTD,null,<LegislationCode> | _TRM_TYTD |  |  |  |

## ORA_LEGISLATION_BALANCE_TYPE Durable Default Rows

The following rows are the durable, version-controlled balance-type default set. For an applicable Add, use every row exactly as shown. Replace each LegislationCode placeholder and the legislation component of each GroupingKey with the user-supplied LegislationCode. Replace each CurrencyCode placeholder with the user-supplied CurrencyCode; preserve empty CurrencyCode cells. User-supplied balance-type rows override this complete set.

| BalanceName | LegislationCode | CurrencyCode | ViewInstanceName | GroupingKey | BaseBalanceName | LegislativeDataGroupId | BalanceTypeId |
|---|---|---|---|---|---|---|---|
| Absences | <LegislationCode> | <CurrencyCode> | PayBalanceTypeVO | ABSENCES,<LegislationCode>,null | ABSENCES |  |  |
| Absences Donation Pool | <LegislationCode> | <CurrencyCode> | PayBalanceTypeVO | ABSENCES_DONATION_POOL,<LegislationCode>,null | ABSENCES_DONATION_POOL |  |  |
| Direct Payments | <LegislationCode> | <CurrencyCode> | PayBalanceTypeVO | Direct Payments,<LegislationCode>,null | Direct Payments |  |  |
| Employee Tax Credits | <LegislationCode> | <CurrencyCode> | PayBalanceTypeVO | Employee Tax Credits,<LegislationCode>,null | Employee Tax Credits |  |  |
| Employer Charges | <LegislationCode> | <CurrencyCode> | PayBalanceTypeVO | Employer Charges,<LegislationCode>,null | Employer Charges |  |  |
| Employer Taxes | <LegislationCode> | <CurrencyCode> | PayBalanceTypeVO | Employer Taxes,<LegislationCode>,null | Employer Taxes |  |  |
| Gross Earnings | <LegislationCode> | <CurrencyCode> | PayBalanceTypeVO | Gross Earnings,<LegislationCode>,null | Gross Earnings |  |  |
| Gross Pay | <LegislationCode> | <CurrencyCode> | PayBalanceTypeVO | Gross Pay,<LegislationCode>,null | Gross Pay |  |  |
| Information | <LegislationCode> | <CurrencyCode> | PayBalanceTypeVO | Information,<LegislationCode>,null | Information |  |  |
| Involuntary Deductions | <LegislationCode> | <CurrencyCode> | PayBalanceTypeVO | Involuntary Deductions,<LegislationCode>,null | Involuntary Deductions |  |  |
| Net | <LegislationCode> | <CurrencyCode> | PayBalanceTypeVO | Net,<LegislationCode>,null | Net |  |  |
| Net Pay | <LegislationCode> | <CurrencyCode> | PayBalanceTypeVO | Net Pay,<LegislationCode>,null | Net Pay |  |  |
| Pensionable Earnings | <LegislationCode> | <CurrencyCode> | PayBalanceTypeVO | Pensionable Earnings,<LegislationCode>,null | Pensionable Earnings |  |  |
| Prestatutory Deductions | <LegislationCode> | <CurrencyCode> | PayBalanceTypeVO | Pre-Statutory Deductions,<LegislationCode>,null | Pre-Statutory Deductions |  |  |
| Reduce Regular Absence Days | <LegislationCode> |  | PayBalanceTypeVO | REDUCE_REGULAR_ABSENCE_DAYS,<LegislationCode>,null | REDUCE_REGULAR_ABSENCE_DAYS |  |  |
| Reduce Regular Absence Earnings | <LegislationCode> | <CurrencyCode> | PayBalanceTypeVO | REDUCE_REGULAR_ABSENCE_EARNINGS,<LegislationCode>,null | REDUCE_REGULAR_ABSENCE_EARNINGS |  |  |
| Reduce Regular Absence Hours | <LegislationCode> |  | PayBalanceTypeVO | REDUCE_REGULAR_ABSENCE_HOURS,<LegislationCode>,null | REDUCE_REGULAR_ABSENCE_HOURS |  |  |
| Reduce Regular Days | <LegislationCode> |  | PayBalanceTypeVO | Reduce Regular Days,<LegislationCode>,null | Reduce Regular Days |  |  |
| Reduce Regular Earnings | <LegislationCode> | <CurrencyCode> | PayBalanceTypeVO | Reduce Regular Earnings,<LegislationCode>,null | Reduce Regular Earnings |  |  |
| Reduce Regular Hours | <LegislationCode> |  | PayBalanceTypeVO | Reduce Regular Hours,<LegislationCode>,null | Reduce Regular Hours |  |  |
| Social Insurance Deductions | <LegislationCode> | <CurrencyCode> | PayBalanceTypeVO | Social Insurance Deductions,<LegislationCode>,null | Social Insurance Deductions |  |  |
| Standard Earnings | <LegislationCode> | <CurrencyCode> | PayBalanceTypeVO | Standard Earnings,<LegislationCode>,null | Standard Earnings |  |  |
| Supplemental Earnings | <LegislationCode> | <CurrencyCode> | PayBalanceTypeVO | Supplemental Earnings,<LegislationCode>,null | Supplemental Earnings |  |  |
| TOTAL_THIRD_PARTY_PAYMENTS | <LegislationCode> | <CurrencyCode> | PayBalanceTypeVO | TOTAL_THIRD_PARTY_PAYMENTS,<LegislationCode>,null | TOTAL_THIRD_PARTY_PAYMENTS |  |  |
| Tax Deductions | <LegislationCode> | <CurrencyCode> | PayBalanceTypeVO | Tax Deductions,<LegislationCode>,null | Tax Deductions |  |  |
| Taxable Benefits | <LegislationCode> | <CurrencyCode> | PayBalanceTypeVO | Taxable Benefits,<LegislationCode>,null | Taxable Benefits |  |  |
| Total Deductions | <LegislationCode> | <CurrencyCode> | PayBalanceTypeVO | Total Deductions,<LegislationCode>,null | Total Deductions |  |  |
| Voluntary Deductions | <LegislationCode> | <CurrencyCode> | PayBalanceTypeVO | Voluntary Deductions,<LegislationCode>,null | Voluntary Deductions |  |  |

## ORA_LEGISLATION_COMPONENT_GROUP Durable Default Rows

The following rows are the durable, version-controlled component-group default set. For an applicable Add, use every row exactly as shown. Replace each LegislationCode placeholder and the legislation component of each GroupingKey with the user-supplied LegislationCode. User-supplied component-group rows override this complete set.

| BaseName | LegislationCode | ViewInstanceName | GroupingKey | Name | DeductionGroupId |
|---|---|---|---|---|---|
| Benefits | <LegislationCode> | PayDeductionGroupVO | Benefits,<LegislationCode> | Benefits |  |
| Federal | <LegislationCode> | PayDeductionGroupVO | Federal,<LegislationCode> | Federal |  |
| GLB_ABSENCES | <LegislationCode> | PayDeductionGroupVO | GLB_ABSENCES,<LegislationCode> | Absences |  |
| GLB_TIME_CARDS | <LegislationCode> | PayDeductionGroupVO | GLB_TIME_CARDS,<LegislationCode> | Time Cards |  |
| ORA_RECOVERY | <LegislationCode> | PayDeductionGroupVO | ORA_RECOVERY,<LegislationCode> | Recoveries |  |
| Social insurance | <LegislationCode> | PayDeductionGroupVO | Social insurance,<LegislationCode> | Social Insurance |  |

## ORA_LEGISLATION_ELEMENT_CLASSIFICATION Durable Default Rows

The following rows are the durable, version-controlled element-classification default set. For an applicable Add, use every row exactly as shown. Replace each LegislationCode placeholder and only the final legislation component in each GroupingKey with the user-supplied LegislationCode. User-supplied element-classification rows override this complete set.

| BaseClassificationName | LegislationCode | ViewInstanceName | GroupingKey | ClassificationName | LegislativeDataGroupId | ClassificationId |
|---|---|---|---|---|---|---|
| GLB_DONATION_POOL | <LegislationCode> | ElementClassificationVO | GLB_DONATION_POOL,null,<LegislationCode> | Donation Pool |  |  |
| Absences | <LegislationCode> | ElementClassificationVO | Absences,null,<LegislationCode> | Absences |  |  |
| GLB_ABSENCES_MATERNITY | <LegislationCode> | ElementClassificationVO | GLB_ABSENCES_MATERNITY,null,<LegislationCode> | Maternity |  |  |
| GLB_ABSENCES_OTHER | <LegislationCode> | ElementClassificationVO | GLB_ABSENCES_OTHER,null,<LegislationCode> | Other |  |  |
| GLB_ABSENCES_SICKNESS | <LegislationCode> | ElementClassificationVO | GLB_ABSENCES_SICKNESS,null,<LegislationCode> | Sickness |  |  |
| GLB_ABSENCES_VACATION | <LegislationCode> | ElementClassificationVO | GLB_ABSENCES_VACATION,null,<LegislationCode> | Vacation |  |  |
| Absences Subject to Social Insurance | <LegislationCode> | ElementClassificationVO | Absences Subject to Social Insurance,null,<LegislationCode> | Subject to Social Insurance |  |  |
| Balance Initialization | <LegislationCode> | ElementClassificationVO | Balance Initialization,null,<LegislationCode> | Balance Initialization |  |  |
| Direct Payments | <LegislationCode> | ElementClassificationVO | Direct Payments,null,<LegislationCode> | Direct Payments |  |  |
| Direct Payments Expense Reimbursement | <LegislationCode> | ElementClassificationVO | Direct Payments Expense Reimbursement,null,<LegislationCode> | Expense Reimbursement |  |  |
| Employee Tax Credits | <LegislationCode> | ElementClassificationVO | Employee Tax Credits,null,<LegislationCode> | Employee Tax Credits |  |  |
| Employer Charges | <LegislationCode> | ElementClassificationVO | Employer Charges,null,<LegislationCode> | Employer Charges |  |  |
| Employer Charges Benefits Employer Paid | <LegislationCode> | ElementClassificationVO | Employer Charges Benefits Employer Paid,null,<LegislationCode> | Benefits Employer Paid |  |  |
| EMPLOYER_PRETAX_CHARGES | <LegislationCode> | ElementClassificationVO | EMPLOYER_PRETAX_CHARGES,null,<LegislationCode> | Employer Pretax Charges |  |  |
| Employer Taxes | <LegislationCode> | ElementClassificationVO | Employer Taxes,null,<LegislationCode> | Employer Taxes |  |  |
| Sanjay_Secondary EmployerTax Classification_Generic | <LegislationCode> | ElementClassificationVO | Sanjay_Secondary EmployerTax Classification_Generic,null,<LegislationCode> | Sanjay_Secondary EmployerTax Classification_Generic |  |  |
| Sanjay_Sub Classification_Empployer Tax_Generic | <LegislationCode> | ElementClassificationVO | Sanjay_Sub Classification_Empployer Tax_Generic,null,<LegislationCode> | Sanjay_Sub Classification_Empployer Tax_Generic |  |  |
| Information | <LegislationCode> | ElementClassificationVO | Information,null,<LegislationCode> | Information |  |  |
| Information Subject to Social Insurance | <LegislationCode> | ElementClassificationVO | Information Subject to Social Insurance,null,<LegislationCode> | Subject to Social Insurance |  |  |
| Pre-Statutory Deductions | <LegislationCode> | ElementClassificationVO | Pre-Statutory Deductions,null,<LegislationCode> | Prestatutory Deductions |  |  |
| Pre-Statutory Deductions Pension Plan Pre-Statutory | <LegislationCode> | ElementClassificationVO | Pre-Statutory Deductions Pension Plan Pre-Statutory,null,<LegislationCode> | Pension Plan Prestatutory |  |  |
| Pre-Statutory Deductions Dependent Care | <LegislationCode> | ElementClassificationVO | Pre-Statutory Deductions Dependent Care,null,<LegislationCode> | Dependent Care |  |  |
| Pre-Statutory Deductions Health Care | <LegislationCode> | ElementClassificationVO | Pre-Statutory Deductions Health Care,null,<LegislationCode> | Health Care |  |  |
| Pre-Statutory Deductions Benefits Pre-Statutory | <LegislationCode> | ElementClassificationVO | Pre-Statutory Deductions Benefits Pre-Statutory,null,<LegislationCode> | Benefits Prestatutory |  |  |
| Pre-Statutory Deductions Deferred Compensation Plan | <LegislationCode> | ElementClassificationVO | Pre-Statutory Deductions Deferred Compensation Plan,null,<LegislationCode> | Deferred Compensation Plan |  |  |
| Pre-Statutory Deductions Union Dues | <LegislationCode> | ElementClassificationVO | Pre-Statutory Deductions Union Dues,null,<LegislationCode> | Union Dues |  |  |
| Social Insurance Deductions | <LegislationCode> | ElementClassificationVO | Social Insurance Deductions,null,<LegislationCode> | Social Insurance Deductions |  |  |
| Standard Earnings | <LegislationCode> | ElementClassificationVO | Standard Earnings,null,<LegislationCode> | Standard Earnings |  |  |
| Sanjay_Secondary Earning Classification_Generic | <LegislationCode> | ElementClassificationVO | Sanjay_Secondary Earning Classification_Generic,null,<LegislationCode> | Sanjay_Secondary Earning Classification_Generic |  |  |
| Sanjay_Sub Classification_Std Earning_Generic | <LegislationCode> | ElementClassificationVO | Sanjay_Sub Classification_Std Earning_Generic,null,<LegislationCode> | Sanjay_Sub Classification_Std Earning_Generic |  |  |
| Standard Earnings Tips Regular | <LegislationCode> | ElementClassificationVO | Standard Earnings Tips Regular,null,<LegislationCode> | Tips Regular |  |  |
| Standard Earnings Regular Not Worked | <LegislationCode> | ElementClassificationVO | Standard Earnings Regular Not Worked,null,<LegislationCode> | Regular Not Worked |  |  |
| Standard Earnings Subject to Social Insurance | <LegislationCode> | ElementClassificationVO | Standard Earnings Subject to Social Insurance,null,<LegislationCode> | Subject to Social Insurance |  |  |
| Standard Earnings Overtime | <LegislationCode> | ElementClassificationVO | Standard Earnings Overtime,null,<LegislationCode> | Overtime |  |  |
| Standard Earnings Subject to Pension | <LegislationCode> | ElementClassificationVO | Standard Earnings Subject to Pension,null,<LegislationCode> | Subject to Pension |  |  |
| Standard Earnings Premium | <LegislationCode> | ElementClassificationVO | Standard Earnings Premium,null,<LegislationCode> | Premium |  |  |
| Standard Earnings Shift | <LegislationCode> | ElementClassificationVO | Standard Earnings Shift,null,<LegislationCode> | Shift |  |  |
| Standard Earnings Bonus Earnings | <LegislationCode> | ElementClassificationVO | Standard Earnings Bonus Earnings,null,<LegislationCode> | Bonus Earnings |  |  |
| Standard Earnings Commission Earnings | <LegislationCode> | ElementClassificationVO | Standard Earnings Commission Earnings,null,<LegislationCode> | Commission Earnings |  |  |
| Standard Earnings Sick | <LegislationCode> | ElementClassificationVO | Standard Earnings Sick,null,<LegislationCode> | Sick |  |  |
| Standard Earnings Vacation | <LegislationCode> | ElementClassificationVO | Standard Earnings Vacation,null,<LegislationCode> | Vacation |  |  |
| Standard Earnings Disposable Income Spousal Support | <LegislationCode> | ElementClassificationVO | Standard Earnings Disposable Income Spousal Support,null,<LegislationCode> | Disposable Income Spousal Support |  |  |
| Standard Earnings Disposable Income Alimony | <LegislationCode> | ElementClassificationVO | Standard Earnings Disposable Income Alimony,null,<LegislationCode> | Disposable Income Alimony |  |  |
| Standard Earnings Disposable Income Bankruptcy Order | <LegislationCode> | ElementClassificationVO | Standard Earnings Disposable Income Bankruptcy Order,null,<LegislationCode> | Disposable Income Bankruptcy Order |  |  |
| Standard Earnings Disposable Income Court Order | <LegislationCode> | ElementClassificationVO | Standard Earnings Disposable Income Court Order,null,<LegislationCode> | Disposable Income Court Order |  |  |
| Standard Earnings Disposable Income Debt Collection | <LegislationCode> | ElementClassificationVO | Standard Earnings Disposable Income Debt Collection,null,<LegislationCode> | Disposable Income Debt Collection |  |  |
| Standard Earnings Disposable Income Education Loan | <LegislationCode> | ElementClassificationVO | Standard Earnings Disposable Income Education Loan,null,<LegislationCode> | Disposable Income Education Loan |  |  |
| Standard Earnings Regular | <LegislationCode> | ElementClassificationVO | Standard Earnings Regular,null,<LegislationCode> | Regular |  |  |
| Standard Earnings Disposable Income Employee Requested | <LegislationCode> | ElementClassificationVO | Standard Earnings Disposable Income Employee Requested,null,<LegislationCode> | Disposable Income Employee Requested |  |  |
| Standard Earnings Disposable Income Support Child | <LegislationCode> | ElementClassificationVO | Standard Earnings Disposable Income Support Child,null,<LegislationCode> | Disposable Income Support Child |  |  |
| Standard Earnings Disposable Income Tax Levy | <LegislationCode> | ElementClassificationVO | Standard Earnings Disposable Income Tax Levy,null,<LegislationCode> | Disposable Income Tax Levy |  |  |
| Standard Earnings Disposable Income Wage Attachment | <LegislationCode> | ElementClassificationVO | Standard Earnings Disposable Income Wage Attachment,null,<LegislationCode> | Disposable Income Wage Attachment |  |  |
| Standard Earnings Bonus | <LegislationCode> | ElementClassificationVO | Standard Earnings Bonus,null,<LegislationCode> | Bonus |  |  |
| Standard Earnings Commission | <LegislationCode> | ElementClassificationVO | Standard Earnings Commission,null,<LegislationCode> | Commission |  |  |
| Standard Earnings Taxable | <LegislationCode> | ElementClassificationVO | Standard Earnings Taxable,null,<LegislationCode> | Taxable |  |  |
| Supplemental Earnings | <LegislationCode> | ElementClassificationVO | Supplemental Earnings,null,<LegislationCode> | Supplemental Earnings |  |  |
| Supplemental Earnings Disposable Income Spousal Support | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Disposable Income Spousal Support,null,<LegislationCode> | Disposable Income Spousal Support |  |  |
| Supplemental Earnings Disposable Income Support Child | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Disposable Income Support Child,null,<LegislationCode> | Disposable Income Support Child |  |  |
| Supplemental Earnings Disposable Income Tax Levy | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Disposable Income Tax Levy,null,<LegislationCode> | Disposable Income Tax Levy |  |  |
| Supplemental Earnings Disposable Income Wage Attachment | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Disposable Income Wage Attachment,null,<LegislationCode> | Disposable Income Wage Attachment |  |  |
| Supplemental Earnings Subject to Social Insurance | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Subject to Social Insurance,null,<LegislationCode> | Subject to Social Insurance |  |  |
| Supplemental Earnings Severance Pay Taxable | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Severance Pay Taxable,null,<LegislationCode> | Severance Pay Taxable |  |  |
| Supplemental Earnings Taxable | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Taxable,null,<LegislationCode> | Taxable |  |  |
| Supplemental Earnings Disposable Income Alimony | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Disposable Income Alimony,null,<LegislationCode> | Disposable Income Alimony |  |  |
| Supplemental Earnings Disposable Income Bankruptcy Order | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Disposable Income Bankruptcy Order,null,<LegislationCode> | Disposable Income Bankruptcy Order |  |  |
| Supplemental Earnings Disposable Income Court Order | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Disposable Income Court Order,null,<LegislationCode> | Disposable Income Court Order |  |  |
| Supplemental Earnings Disposable Income Debt Collection | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Disposable Income Debt Collection,null,<LegislationCode> | Disposable Income Debt Collection |  |  |
| Supplemental Earnings Disposable Income Education Loan | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Disposable Income Education Loan,null,<LegislationCode> | Disposable Income Education Loan |  |  |
| Supplemental Earnings Disposable Income Employee Requested | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Disposable Income Employee Requested,null,<LegislationCode> | Disposable Income Employee Requested |  |  |
| Supplemental Earnings Pensions and Annuities | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Pensions and Annuities,null,<LegislationCode> | Pensions and Annuities |  |  |
| Supplemental Earnings Travel Taxable Reimbursement | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Travel Taxable Reimbursement,null,<LegislationCode> | Travel Taxable Reimbursement |  |  |
| Supplemental Earnings Awards and Prizes | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Awards and Prizes,null,<LegislationCode> | Awards and Prizes |  |  |
| Supplemental Earnings Bonus | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Bonus,null,<LegislationCode> | Bonus |  |  |
| Supplemental Earnings Benefit Plan Credits | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Benefit Plan Credits,null,<LegislationCode> | Benefit Plan Credits |  |  |
| Supplemental Earnings Deceased Employee Wages | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Deceased Employee Wages,null,<LegislationCode> | Deceased Employee Wages |  |  |
| Supplemental Earnings Deferred Compensation Distribution | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Deferred Compensation Distribution,null,<LegislationCode> | Deferred Compensation Distribution |  |  |
| Supplemental Earnings Moving Expense Nonqualified and Taxable | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Moving Expense Nonqualified and Taxable,null,<LegislationCode> | Moving Expense Nonqualified and Taxable |  |  |
| Supplemental Earnings Moving Expense Nontaxable | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Moving Expense Nontaxable,null,<LegislationCode> | Moving Expense Nontaxable |  |  |
| Supplemental Earnings Moving Expense Taxable Reimbursement | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Moving Expense Taxable Reimbursement,null,<LegislationCode> | Moving Expense Taxable Reimbursement |  |  |
| Supplemental Earnings Tips Supplemental | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Tips Supplemental,null,<LegislationCode> | Tips Supplemental |  |  |
| Supplemental Earnings Commission | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Commission,null,<LegislationCode> | Commission |  |  |
| Supplemental Earnings Vacation Pay | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Vacation Pay,null,<LegislationCode> | Vacation Pay |  |  |
| Supplemental Earnings Sick Pay | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Sick Pay,null,<LegislationCode> | Sick Pay |  |  |
| Supplemental Earnings Dismissal Payments | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Dismissal Payments,null,<LegislationCode> | Dismissal Payments |  |  |
| Supplemental Earnings Jury Duty Pay | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Jury Duty Pay,null,<LegislationCode> | Jury Duty Pay |  |  |
| Supplemental Earnings Moving Expense Qualified and Nontaxable | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Moving Expense Qualified and Nontaxable,null,<LegislationCode> | Moving Expense Qualified and Nontaxable |  |  |
| Supplemental Earnings Educational Assistance | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Educational Assistance,null,<LegislationCode> | Educational Assistance |  |  |
| Supplemental Earnings Severance Pay Nontaxable | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Severance Pay Nontaxable,null,<LegislationCode> | Severance Pay Nontaxable |  |  |
| Supplemental Earnings Subject to Pension | <LegislationCode> | ElementClassificationVO | Supplemental Earnings Subject to Pension,null,<LegislationCode> | Subject to Pension |  |  |
| Tax Deductions | <LegislationCode> | ElementClassificationVO | Tax Deductions,null,<LegislationCode> | Tax Deductions |  |  |
| Taxable Benefits | <LegislationCode> | ElementClassificationVO | Taxable Benefits,null,<LegislationCode> | Taxable Benefits |  |  |
| Taxable Benefits Disposable Income Alimony | <LegislationCode> | ElementClassificationVO | Taxable Benefits Disposable Income Alimony,null,<LegislationCode> | Disposable Income Alimony |  |  |
| Taxable Benefits Disposable Income Bankruptcy Order | <LegislationCode> | ElementClassificationVO | Taxable Benefits Disposable Income Bankruptcy Order,null,<LegislationCode> | Disposable Income Bankruptcy Order |  |  |
| Taxable Benefits Disposable Income Court Order | <LegislationCode> | ElementClassificationVO | Taxable Benefits Disposable Income Court Order,null,<LegislationCode> | Disposable Income Court Order |  |  |
| Taxable Benefits Board and Lodging | <LegislationCode> | ElementClassificationVO | Taxable Benefits Board and Lodging,null,<LegislationCode> | Board and Lodging |  |  |
| Taxable Benefits Disposable Income Debt Collection | <LegislationCode> | ElementClassificationVO | Taxable Benefits Disposable Income Debt Collection,null,<LegislationCode> | Disposable Income Debt Collection |  |  |
| Taxable Benefits Disposable Income Education Loan | <LegislationCode> | ElementClassificationVO | Taxable Benefits Disposable Income Education Loan,null,<LegislationCode> | Disposable Income Education Loan |  |  |
| Taxable Benefits Disposable Income Employee Requested | <LegislationCode> | ElementClassificationVO | Taxable Benefits Disposable Income Employee Requested,null,<LegislationCode> | Disposable Income Employee Requested |  |  |
| Taxable Benefits Disposable Income Spousal Support | <LegislationCode> | ElementClassificationVO | Taxable Benefits Disposable Income Spousal Support,null,<LegislationCode> | Disposable Income Spousal Support |  |  |
| Taxable Benefits Disposable Income Support Child | <LegislationCode> | ElementClassificationVO | Taxable Benefits Disposable Income Support Child,null,<LegislationCode> | Disposable Income Support Child |  |  |
| Taxable Benefits Disposable Income Tax Levy | <LegislationCode> | ElementClassificationVO | Taxable Benefits Disposable Income Tax Levy,null,<LegislationCode> | Disposable Income Tax Levy |  |  |
| Taxable Benefits Disposable Income Wage Attachment | <LegislationCode> | ElementClassificationVO | Taxable Benefits Disposable Income Wage Attachment,null,<LegislationCode> | Disposable Income Wage Attachment |  |  |
| Taxable Benefits Moving Expense Qualified and Nontaxable | <LegislationCode> | ElementClassificationVO | Taxable Benefits Moving Expense Qualified and Nontaxable,null,<LegislationCode> | Moving Expense Qualified and Nontaxable |  |  |
| Taxable Benefits Moving Expense Nonqualified and Taxable | <LegislationCode> | ElementClassificationVO | Taxable Benefits Moving Expense Nonqualified and Taxable,null,<LegislationCode> | Moving Expense Nonqualified and Taxable |  |  |
| Taxable Benefits Taxable | <LegislationCode> | ElementClassificationVO | Taxable Benefits Taxable,null,<LegislationCode> | Taxable |  |  |
| Taxable Benefits Subject to Social Insurance | <LegislationCode> | ElementClassificationVO | Taxable Benefits Subject to Social Insurance,null,<LegislationCode> | Subject to Social Insurance |  |  |
| Taxable Benefits Moving Expense - Nonqualified | <LegislationCode> | ElementClassificationVO | Taxable Benefits Moving Expense - Nonqualified,null,<LegislationCode> | Moving Expense - Nonqualified |  |  |
| Taxable Benefits Moving Expense - Qualified | <LegislationCode> | ElementClassificationVO | Taxable Benefits Moving Expense - Qualified,null,<LegislationCode> | Moving Expense - Qualified |  |  |
| Taxable Benefits Noncash Award | <LegislationCode> | ElementClassificationVO | Taxable Benefits Noncash Award,null,<LegislationCode> | Noncash Award |  |  |
| Taxable Benefits Personal Use of Company Car | <LegislationCode> | ElementClassificationVO | Taxable Benefits Personal Use of Company Car,null,<LegislationCode> | Personal Use of Company Car |  |  |
| Taxable Benefits Group Term Life Insurance | <LegislationCode> | ElementClassificationVO | Taxable Benefits Group Term Life Insurance,null,<LegislationCode> | Group Term Life Insurance |  |  |
| Taxable Benefits Cash Tips Reported | <LegislationCode> | ElementClassificationVO | Taxable Benefits Cash Tips Reported,null,<LegislationCode> | Cash Tips Reported |  |  |
| Voluntary Deductions | <LegislationCode> | ElementClassificationVO | Voluntary Deductions,null,<LegislationCode> | Voluntary Deductions |  |  |
| Voluntary Deductions Loans | <LegislationCode> | ElementClassificationVO | Voluntary Deductions Loans,null,<LegislationCode> | Loans |  |  |
| Voluntary Deductions Pension Plan After Tax | <LegislationCode> | ElementClassificationVO | Voluntary Deductions Pension Plan After Tax,null,<LegislationCode> | Pension Plan After Tax |  |  |
| Voluntary Deductions Professional Fees | <LegislationCode> | ElementClassificationVO | Voluntary Deductions Professional Fees,null,<LegislationCode> | Professional Fees |  |  |
| Voluntary Deductions Benefits After Tax | <LegislationCode> | ElementClassificationVO | Voluntary Deductions Benefits After Tax,null,<LegislationCode> | Benefits After Tax |  |  |
| Voluntary Deductions Employer Reimbursements | <LegislationCode> | ElementClassificationVO | Voluntary Deductions Employer Reimbursements,null,<LegislationCode> | Employer Reimbursements |  |  |
| Voluntary Deductions Union Deductions | <LegislationCode> | ElementClassificationVO | Voluntary Deductions Union Deductions,null,<LegislationCode> | Union Deductions |  |  |

## ORA_LEGISLATION_PAYMENT_TYPE Durable Default Rows

The following rows are the durable, version-controlled payment-type default set. For an applicable Add, use every row exactly as shown. Replace each LegislationCode placeholder and the legislation component of each GroupingKey with the user-supplied LegislationCode. User-supplied payment-type rows override this complete set.

| BasePaymentTypeName | LegislationCode | ViewInstanceName | GroupingKey | PaymentTypeName | PaymentTypeId |
|---|---|---|---|---|---|
| Cash | <LegislationCode> | PaymentTypeVO | Cash,<LegislationCode> | Cash |  |
| Check | <LegislationCode> | PaymentTypeVO | Check,<LegislationCode> | Check |  |
| EFT | <LegislationCode> | PaymentTypeVO | EFT,<LegislationCode> | EFT |  |
| International Transfer | <LegislationCode> | PaymentTypeVO | International Transfer,<LegislationCode> | International Transfer |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CPL.APPLY_DEFAULTS | step | 3 | apply_default | not_applicable->CPL.ENFORCE_FSM_CONTRACT;unresolved->RETURN_ISSUES | CPL.RESOLVE_FSM_READINESS | stop | An explicitly requested Add omits a documented default value or mapping set |
