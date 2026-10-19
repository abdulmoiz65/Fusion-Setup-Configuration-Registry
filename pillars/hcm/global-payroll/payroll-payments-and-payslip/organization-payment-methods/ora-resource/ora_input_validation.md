# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Organization payment method identity | LegislativeDataGroupName, EffectiveStartDate, OrganizationPaymentMethodName, OrganizationPaymentMethodCode, CurrencyCode, PaymentTypeCode | Block preview | Provide all source fields in the OrganizationPaymentMethod DAT row | Create request | |
| Source tracking identity | SourceSystemOwner and SourceSystemId, or neither field | Block preview when only one source-key field is supplied | Supply both values for an established source system; otherwise omit both and let Fusion generate its default source key | Create or update request | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| EffectiveStartDate uses YYYY/MM/DD | Block preview when the date is invalid | Every request | |
| OrganizationPaymentMethodName and OrganizationPaymentMethodCode are each 80 characters or fewer | Block preview when either value is too long | Create or update request | |
| CurrencyCode is USD and PaymentTypeCode is EFT for a US Direct Deposit request | Block preview when the approved values change | US Direct Deposit request | |
| SourceSystemOwner and SourceSystemId are both omitted for this create-only request | Continue with Fusion-generated default source key | Create request | |
| PaymentSourceName and PaymentSourceCode are both supplied | Block preview when either value is missing | Request includes a payment source | |
| Default payment source has a PaymentMethodRule with DefaultFlag Y | Block preview when the default rule is absent or does not reference the payment source | Request includes a default payment source | |
| PaymentMethodRule supplies LegislativeDataGroupName, PaymentSourceCode, OrganizationPaymentMethodCode, and ThirdPartyPaymentFlag | Block preview when the composite user key is incomplete | Every PaymentMethodRule MERGE request | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Resolver |
|---|---|---|---|---|---|---|---|---|
| OPM.VALIDATE_INPUT | step | 1 | validate_input | passed->OPM.VALIDATE_RULE_CONDITIONS;failed->OPM.FAILED | none | stop | Every request | |
| OPM.VALIDATE_RULE_CONDITIONS | decision | 2 | validate_input | passed->OPM.VALIDATE_DEPENDENCIES;failed->OPM.FAILED | OPM.VALIDATE_INPUT | stop | Every create or update request; evaluate Payment Method Rule Conditional Field Validation and Payment Method Rule Pre-DAT Validation Gate for every proposed rule, including child-only requests | |
| OPM.VALIDATE_PRENOTIFICATION | decision | 8 | validate_input | passed->OPM.ENFORCE_HDL_DESIGN;failed->OPM.FAILED | OPM.APPLY_DEFAULTS | stop | Every create or update request; validate supplied prenotification values against their existing format and metadata contracts; preserve input intent | |

## HDL Source Analysis

| Source File | Source Role | SHA-256 | Observed Content |
|---|---|---|---|
| OrganizationPaymentMethodAll.dat | Supported-attribute catalog | 577173cb676078febedb72673406dbb0d1e1399f3497f3b80799889c9c66c854 | Contains METADATA rows for OrganizationPaymentMethod, PaymentSource, and PaymentMethodRule; contains no data-operation rows |
| OrganizationPaymentMethod2.dat | Developer-identified minimum-required example | 57e886b1adc988f3b28b069dcd1dc0670cfabeb803f14390828e2455e0db137e | Contains one METADATA row and one MERGE row for each of the three components |
| objectAttributes_export.csv | Exported HDL attribute metadata | 75da2a2048a4422221e1c3f7346ab7bc95935e2358e634d6a0df88d5e0ed57f3 | Contains 39 metadata rows for the OrganizationPaymentMethod root component; it contains no PaymentSource or PaymentMethodRule rows |

## Supported HDL Components and Operations

| Component | Supported Attributes in Full Source | Operation Evidenced by Supplied Sources | Source Interpretation |
|---|---|---|---|
| OrganizationPaymentMethod | 39 | MERGE | OrganizationPaymentMethodAll.dat supplies the attribute catalog; OrganizationPaymentMethod2.dat supplies the MERGE example |
| PaymentSource | 41 | MERGE | OrganizationPaymentMethodAll.dat supplies the attribute catalog; OrganizationPaymentMethod2.dat supplies the MERGE example |
| PaymentMethodRule | 30 | MERGE | OrganizationPaymentMethodAll.dat supplies the attribute catalog; OrganizationPaymentMethod2.dat supplies the MERGE example |

Only MERGE is evidenced as a data operation by the supplied files. OrganizationPaymentMethodAll.dat is metadata-only and is not a complete load file by itself because it contains no operation records.

## Supported Attribute Catalog

| Component | Supported Attributes |
|---|---|
| OrganizationPaymentMethod | OrganizationPaymentMethodId, EffectiveStartDate, EffectiveEndDate, LegislativeDataGroupId, OrganizationPaymentMethodCode, PaymentTypeId, PrenotificationRequiredFlag, PrenotificationDays, PrenotificationAmount, PaymentFreeText, TransactionLimit, PaymentLimit, CompanyReference, BankReference, BankNameEFT, AdditionalPaymentText, IncludeBalancingEntries, PaymentReference, CompanyReferenceType, CompanyName, BankReferenceType, GUID, SourceSystemId, SourceSystemOwner, LegislativeDataGroupName, PaymentTypeCode, CurrencyCode, OrganizationPaymentMethodName, SourceRefTableName, SourceRef001, SourceRef002, SourceRef003, SourceRef004, SourceRef005, SourceRef006, SourceRef007, SourceRef008, SourceRef009, SourceRef010 |
| PaymentSource | PaymentSourceId, PaymentSourceName, PaymentSourceCode, EffectiveStartDate, EffectiveEndDate, LegislativeDataGroupId, LegislativeDataGroupName, BankAccountId, BankAccountName, BankNameEFT, BankReferenceTypeEFT, BankReferenceEFT, CompanyNameEFT, CompanyReferenceTypeEFT, CompanyReferenceEFT, IncludeBalancingEntries, WorkerReportCategoryId, WorkerReportCategoryCode, ThirdPartyReportCategoryId, ThirdPartyReportCategoryCode, TransactionLimitEFT, PaymentLimitEFT, PaymentReferenceEFT, PaymentFreeTextEFT, AdditionalPaymentTextEFT, OrganizationPaymentMethodId, OrganizationPaymentMethodCode, GUID, SourceSystemOwner, SourceSystemId, SourceRefTableName, SourceRef001, SourceRef002, SourceRef003, SourceRef004, SourceRef005, SourceRef006, SourceRef007, SourceRef008, SourceRef009, SourceRef010 |
| PaymentMethodRule | PaymentMethodRuleId, EffectiveStartDate, EffectiveEndDate, PaymentSourceId, DefaultFlag, TaxReportingUnitId, PaymentCriteria, ThirdPartyId, ThirdPartyPaymentFlag, SourceSystemId, SourceSystemOwner, GUID, PaymentSourceCode, LegislativeDataGroupName, OrganizationPaymentMethodCode, TaxReportingUnitName, ThirdPartyCode, OrganizationPaymentMethodId, LegislativeDataGroupId, SourceRefTableName, SourceRef001, SourceRef002, SourceRef003, SourceRef004, SourceRef005, SourceRef006, SourceRef007, SourceRef008, SourceRef009, SourceRef010 |

The full source writes SourceRefTableName and SourceRef001 through SourceRef010 using HDL header assignment syntax. The normalized attribute names above omit the example assignments while retaining the supported attribute identities.

## HDL Attribute Metadata Reconciliation

| Reconciliation Check | Result | Authoring Interpretation |
|---|---|---|
| Root attribute coverage | All 39 OrganizationPaymentMethod attributes in objectAttributes_export.csv match the 39 normalized attributes in OrganizationPaymentMethodAll.dat | Use the export for root-component data type, key type, requiredness, lookup, integration-object, and description metadata |
| Attribute order | The export and DAT contain the same root attribute set in different orders | Attribute identity is reconciled by exact METADATA Attribute name, not by column position across files |
| Child attribute metadata | No PaymentSource or PaymentMethodRule metadata rows are present in objectAttributes_export.csv | Retain their supported attribute names and minimum DAT shapes, but do not infer their data types, key types, requiredness, lookups, or descriptions from the root export |
| Data types | 31 String, 6 Number, and 2 Date attributes | Validate supplied root values using the exported type only where a value is present |
| Required metadata | 2 Yes, 5 For new records, and 32 No | Interpret requiredness with the attribute description and operation; OrganizationPaymentMethodId is application-generated and is available only for updates despite Required=Yes |
| Key metadata | 1 Surrogate ID, 3 User Key, 3 Foreign Object Reference, 2 Source Key, 1 Globally Unique ID, and 29 without a stated key type | Do not treat a blank key type as evidence that an attribute cannot participate in another documented business rule |
| Lookup metadata | IncludeBalancingEntries and PrenotificationRequiredFlag use PAY_TMPLT_YES_NO | Validate these two root fields against the exported lookup when supplied |
| Minimum create references | The minimum DAT uses LegislativeDataGroupName instead of LegislativeDataGroupId and PaymentTypeCode instead of PaymentTypeId | Accept the example's name/code user references for its MERGE create shape; do not require both the ID and alternate reference for the same object |

## OrganizationPaymentMethod Attribute Metadata

The table below captures every exported metadata field. Repeated SourceRef descriptions are normalized without changing their meaning. `In Minimum DAT` compares each exported root attribute with OrganizationPaymentMethod2.dat; it does not redefine the export's operation-specific requiredness.

| Display Name | METADATA Attribute | Data Type | Key Type | Integration Object Name | Required | Lookup | In Minimum DAT | Description |
|---|---|---|---|---|---|---|---|---|
| Organization Payment Method ID | OrganizationPaymentMethodId | Number | Surrogate ID | OrganizationPaymentMethod | Yes | None stated | No | The application generated ID that uniquely identifies the organization payment method. Only available when updating existing records. |
| Legislative Data Group Name | LegislativeDataGroupName | String | User Key | None stated | No | None stated | Yes | The name of the legislative data group. |
| Organization Payment Method Code | OrganizationPaymentMethodCode | String | User Key | None stated | For new records | None stated | Yes | The code that uniquely identifies the organization payment method for the legislative data group. |
| Effective End Date | EffectiveEndDate | Date | None stated | None stated | No | None stated | No | The end date of the date-effective changes. If left blank, the effective end date is the end of time by default. |
| Effective Start Date | EffectiveStartDate | Date | None stated | None stated | Yes | None stated | Yes | The start date of the record or of date-effective changes to the record. |
| Additional Payment Text | AdditionalPaymentText | String | None stated | None stated | No | None stated | No | The text providing additional payment information from the user. |
| Bank Name | BankNameEFT | String | None stated | None stated | No | None stated | No | The name of the bank from which the payment will be made. |
| Bank Reference | BankReference | String | None stated | None stated | No | None stated | No | The reference information for the bank from which the payment will be made. |
| Bank Reference Type | BankReferenceType | String | None stated | None stated | No | None stated | No | The reference type for the bank from which the payment will be made. |
| Company Name | CompanyName | String | None stated | None stated | No | None stated | No | The name of the source company as it appears in the payment file. |
| Company Reference | CompanyReference | String | None stated | None stated | No | None stated | No | The reference of the source company, such as an employer identification number, as it appears in the payment file. |
| Company Reference Type | CompanyReferenceType | String | None stated | None stated | No | None stated | No | The type of the source company reference, such as reference number. |
| Currency Code | CurrencyCode | String | Foreign Object Reference | None stated | For new records | None stated | Yes | The code to identify the currency of the payment. |
| Include Balancing Entries | IncludeBalancingEntries | String | None stated | None stated | No | PAY_TMPLT_YES_NO | No | Indicates whether to include balance entries in an payments file to debit the bank account for the payer. |
| Legislative Data Group ID | LegislativeDataGroupId | Number | Foreign Object Reference | LegislativeDataGroups | For new records | None stated | No | A unique reference to the legislative data group. |
| Organization Payment Method Name | OrganizationPaymentMethodName | String | None stated | None stated | For new records | None stated | Yes | The name that identifies the organization method of payment. |
| Payment Free Text | PaymentFreeText | String | None stated | None stated | No | None stated | No | The text providing additional payment information, as it appears in the payment file. |
| Payment Limit | PaymentLimit | Number | None stated | None stated | No | None stated | No | The maximum amount of money that can be paid. |
| Payment Reference | PaymentReference | String | None stated | None stated | No | None stated | No | The reference information for the payment, as it appears in the payment file. |
| Payment Type Code | PaymentTypeCode | String | User Key | None stated | No | None stated | Yes | The code to identify the type of the payment. |
| Payment Type ID | PaymentTypeId | Number | Foreign Object Reference | None stated | For new records | None stated | No | The surrogate ID to identify the payment type. |
| Prenotification Amount | PrenotificationAmount | String | None stated | None stated | No | None stated | No | The amount of money to use in a prenotification for validation. |
| Prenotification Days | PrenotificationDays | Number | None stated | None stated | No | None stated | No | The number of days required to elapse after prenotification is sent before an actual funds transfer will be sent. |
| Prenotification Required | PrenotificationRequiredFlag | String | None stated | None stated | No | PAY_TMPLT_YES_NO | No | Indicates whether a validation record must be sent on an payments file to the receiving financial institution a specified number of days before a real financial transfer will be sent. |
| Transaction Limit | TransactionLimit | Number | None stated | None stated | No | None stated | No | The maximum amount of money allowed in a single payment. |
| Source System ID | SourceSystemId | String | Source Key | None stated | No | None stated | Yes | A value to uniquely identify this record. This must be unique for the source system owner and business object component. |
| Source System Owner | SourceSystemOwner | String | Source Key | None stated | No | None stated | Yes | The name of the source system used to generate the source system ID. |
| Globally Unique ID | GUID | String | Globally Unique ID | None stated | No | None stated | No | The globally unique ID. Only available to reference existing records, it cannot be supplied for new records. |
| Reference Context | SourceRefTableName | String | None stated | None stated | No | None stated | No | The context for the user-defined references provided for this component. Do not supply it as a data value; declare the context on the METADATA line as SourceRefTableName= context. |
| Reference 1 | SourceRef001 | String | None stated | None stated | No | None stated | No | A user-defined staging reference for reporting and reconciliation. It is not saved in the application and is named on the METADATA line. |
| Reference 2 | SourceRef002 | String | None stated | None stated | No | None stated | No | A user-defined staging reference for reporting and reconciliation. It is not saved in the application and is named on the METADATA line. |
| Reference 3 | SourceRef003 | String | None stated | None stated | No | None stated | No | A user-defined staging reference for reporting and reconciliation. It is not saved in the application and is named on the METADATA line. |
| Reference 4 | SourceRef004 | String | None stated | None stated | No | None stated | No | A user-defined staging reference for reporting and reconciliation. It is not saved in the application and is named on the METADATA line. |
| Reference 5 | SourceRef005 | String | None stated | None stated | No | None stated | No | A user-defined staging reference for reporting and reconciliation. It is not saved in the application and is named on the METADATA line. |
| Reference 6 | SourceRef006 | String | None stated | None stated | No | None stated | No | A user-defined staging reference for reporting and reconciliation. It is not saved in the application and is named on the METADATA line. |
| Reference 7 | SourceRef007 | String | None stated | None stated | No | None stated | No | A user-defined staging reference for reporting and reconciliation. It is not saved in the application and is named on the METADATA line. |
| Reference 8 | SourceRef008 | String | None stated | None stated | No | None stated | No | A user-defined staging reference for reporting and reconciliation. It is not saved in the application and is named on the METADATA line. |
| Reference 9 | SourceRef009 | String | None stated | None stated | No | None stated | No | A user-defined staging reference for reporting and reconciliation. It is not saved in the application and is named on the METADATA line. |
| Reference 10 | SourceRef010 | String | None stated | None stated | No | None stated | No | A user-defined staging reference for reporting and reconciliation. It is not saved in the application and is named on the METADATA line. |

## Export-Driven Root Attribute Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Supplied OrganizationPaymentMethod values conform to the exported String, Number, or Date data type | Block preview and identify the invalid attribute | Any root attribute is supplied | |
| CurrencyCode, OrganizationPaymentMethodName, and OrganizationPaymentMethodCode are supplied; LegislativeDataGroupId or LegislativeDataGroupName is supplied; and PaymentTypeId or PaymentTypeCode is supplied | Block preview when a required create value or both forms of an evidenced alternate reference are missing | New OrganizationPaymentMethod MERGE | |
| OrganizationPaymentMethodId is not supplied for a new record | Block preview when an application-generated surrogate ID is supplied during create | New OrganizationPaymentMethod MERGE | |
| GUID is used only to reference an existing record | Block preview when GUID is supplied for a new record | New OrganizationPaymentMethod MERGE | |
| IncludeBalancingEntries and PrenotificationRequiredFlag resolve to PAY_TMPLT_YES_NO values | Block preview when a supplied value is outside the exported lookup | Either lookup-backed root attribute is supplied | |
| SourceRefTableName is declared as METADATA header context rather than supplied as an operation-row value | Block preview when reference context is supplied as record data | SourceRefTableName is used | |

## Developer-Identified Minimum Attribute Sets

| Component | Attribute Count | Minimum Attributes Shown in OrganizationPaymentMethod2.dat | Parent Reference Shown |
|---|---|---|---|
| OrganizationPaymentMethod | 8 | SourceSystemOwner, SourceSystemId, LegislativeDataGroupName, EffectiveStartDate, OrganizationPaymentMethodName, OrganizationPaymentMethodCode, CurrencyCode, PaymentTypeCode | None |
| PaymentSource | 10 | SourceSystemOwner, SourceSystemId, LegislativeDataGroupName, EffectiveStartDate, OrganizationPaymentMethodId(SourceSystemId), PaymentSourceCode, PaymentSourceName, BankAccountName, BankReferenceEFT, CompanyReferenceEFT | OrganizationPaymentMethodId resolved from the parent SourceSystemId |
| PaymentMethodRule | 8 | SourceSystemOwner, SourceSystemId, LegislativeDataGroupName, EffectiveStartDate, PaymentSourceId(SourceSystemId), DefaultFlag, TaxReportingUnitName, ThirdPartyPaymentFlag | PaymentSourceId resolved from the parent SourceSystemId |

These sets are captured as the developer-provided minimum example. The source files do not establish that omitted attributes are unsupported or that every listed field is mandatory for every MERGE scenario.

## HDL Record-Shape Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Every operation row uses the same component discriminator as its preceding METADATA row | Block validation when the component names differ | Every supplied HDL data row | |
| Every operation value remains in the exact positional order declared by its METADATA row | Block validation when a value is shifted into another attribute position | Every supplied HDL data row | |
| PaymentSource parent reference uses OrganizationPaymentMethodId(SourceSystemId) and matches the parent OrganizationPaymentMethod SourceSystemId | Block validation when the referenced parent source ID is missing or different | PaymentSource MERGE using the supplied minimum shape | |
| PaymentMethodRule parent reference uses PaymentSourceId(SourceSystemId) and matches the parent PaymentSource SourceSystemId | Block validation when the referenced payment-source source ID is missing or different | PaymentMethodRule MERGE using the supplied minimum shape | |
| SourceSystemOwner and SourceSystemId are supplied together for each component in the minimum example | Block validation when only one source-key field is populated | MERGE using the supplied minimum shape | |

## Author-Confirmed Minimum-Example Mapping

| Source Record | Confirmed Mapping | Required HDL Value Order |
|---|---|---|
| PaymentMethodRule MERGE in OrganizationPaymentMethod2.dat | DefaultFlag=Y; TaxReportingUnitName is blank; ThirdPartyPaymentFlag=N | Preserve an empty field between Y and N for the successive DefaultFlag, TaxReportingUnitName, and ThirdPartyPaymentFlag columns |

TaxReportingUnitName must remain blank and ThirdPartyPaymentFlag must be populated with N in the minimum PaymentMethodRule example.

## Oracle-Documented Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Organization payment method combination | LegislativeDataGroupName, PaymentTypeCode, CurrencyCode | Block preview | Provide one OPM for each LDG, payment type, and currency combination used to disburse payments | Every HDL create request | |
| Organization payment method basic details | OrganizationPaymentMethodName, PaymentTypeCode, CurrencyCode | Block preview | Provide the OPM name, payment type, and currency | Every HDL create request | |
| Payment source | PaymentSourceName and BankAccountName or BankAccountId | Block preview | Add at least one eligible payment source under the OPM | Oracle Fusion Global Payroll or Cloud Payroll processes the payments | |
| Payment rules for multiple sources | At least one PaymentMethodRule that selects each nondefault source and an explicit DefaultFlag choice | Block preview | Define rules that map payment sources to TRUs or documented payment criteria | More than one payment source is loaded | |

Oracle documents an exception to the payment-source requirement when a third-party payroll product is used. Do not apply that exception to Oracle Fusion Global Payroll or Cloud Payroll processing.

## Oracle-Documented Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| EffectiveStartDate is on or before the start date of payroll definitions or other objects that use the OPM or payment rule | Block preview when the dependent object begins earlier | Create request | |
| The first EffectiveStartDate and last EffectiveEndDate are unchanged | Block the update when either logical boundary is changed | Update of OrganizationPaymentMethod, PaymentSource, or PaymentMethodRule | |
| Payment-source EFT or payment information overrides the corresponding OPM-level information | Use the payment-source values and require the payment source when submitting the payment process | Both parent and child levels contain the same information | |
| PaymentSource parent uses OrganizationPaymentMethodId(SourceSystemId) | Block preview when it does not resolve to the parent OrganizationPaymentMethod SourceSystemId | PaymentSource MERGE | |
| PaymentMethodRule parent uses PaymentSourceId(SourceSystemId) | Block preview when it does not resolve to the selected PaymentSource SourceSystemId | PaymentMethodRule MERGE | |

## HCM Data Loader Implementation Map

| Load Order | HDL Component | Purpose | Minimum Oracle Example Mapping | Parent Relationship |
|---|---|---|---|---|
| 1 | OrganizationPaymentMethod | Defines the payment method for an LDG, payment type, and currency | SourceSystemOwner, SourceSystemId, LegislativeDataGroupName, EffectiveStartDate, OrganizationPaymentMethodName, OrganizationPaymentMethodCode, CurrencyCode, PaymentTypeCode | Root record |
| 2 | PaymentSource | Associates a bank account or other source of funds with the OPM | SourceSystemOwner, SourceSystemId, LegislativeDataGroupName, EffectiveStartDate, OrganizationPaymentMethodId(SourceSystemId), PaymentSourceCode, PaymentSourceName, BankAccountName, BankReferenceEFT, CompanyReferenceEFT | OrganizationPaymentMethodId(SourceSystemId) equals the parent OrganizationPaymentMethod SourceSystemId |
| 3 | PaymentMethodRule | Selects the payment source by default status, TRU, or documented payment criteria | SourceSystemOwner, SourceSystemId, LegislativeDataGroupName, EffectiveStartDate, PaymentSourceId(SourceSystemId), DefaultFlag, TaxReportingUnitName; retain the existing ThirdPartyPaymentFlag validation when that attribute is present | PaymentSourceId(SourceSystemId) equals the selected PaymentSource SourceSystemId |

Use MERGE for the documented create example. Build the DAT hierarchy in parent-before-child order and submit the resulting archive only through the HCM Data Loader route.

## Functional Summary

| Topic | HDL Functional Understanding |
|---|---|
| Purpose | OPMs control how payroll payments are disbursed to employees and third parties and connect personal payment methods to organization payment sources |
| Payment type and currency | Payment types vary by legislation; currency is normally aligned with the source bank account, and international payments require localization, bank, and file-format support |
| Payment sources | A payment source identifies the company bank account or other source of funds; the same bank account can be reused by different payment sources and OPMs |
| Payment rules | Rules select a payment source for a group of payees, commonly by TRU and optionally by payment criteria such as department, job, or location |
| Default source | The first source is initially default, but another source can be selected or no default can be retained; a valid default can provide fallback when a TRU rule becomes invalid |
| Prenotification | Direct-deposit OPMs can require zero-amount prenotification, an amount, and a waiting period before direct deposit begins |
| Source precedence | Payment information supplied on PaymentSource takes priority over corresponding OrganizationPaymentMethod information |

## Reference Input Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| LegislativeDataGroupName resolves to exactly one LDG before legislation-dependent values are resolved | Block preview and report the LDG value when zero or multiple matches are returned | LegislativeDataGroupName is supplied | resolve_ldg_by_exact_name |
| A currency display value resolves to exactly one CurrencyCode | Block preview and report the currency value when zero or multiple matches are returned | CurrencyCode isn't supplied and a currency name or display value is supplied | resolve_currency_by_exact_display |
| A payment-type display value resolves within the LegislationCode returned for the LDG | Block preview and report the payment type and legislation when zero or multiple matches are returned | PaymentTypeCode or PaymentTypeId isn't supplied and a payment-type display value is supplied | resolve_payment_type_by_legislation |
| BankAccountName resolves to exactly one bank account associated with a legal employer returned for the LDG | Block preview and report the bank-account value when zero or multiple matches are returned | PaymentSource supplies BankAccountName instead of a validated BankAccountId | resolve_bank_account_by_legal_employer |
| Worker and third-party-payee report-category names are resolved independently within the LDG | Block preview and identify the applicable report-category field when zero or multiple matches are returned | A PaymentSource report-category display value is supplied | resolve_payment_source_report_category_by_ldg |
| TaxReportingUnitName resolves to exactly one returned key-value pair for the LDG | Block preview and report the TRU value when zero or multiple matches are returned | PaymentMethodRule supplies TaxReportingUnitName instead of a validated TaxReportingUnitId | resolve_tax_reporting_unit_by_ldg |
| Third-party name resolves to exactly one third-party payment method under the resolved OrganizationPaymentMethodId | Block preview and report the third-party value when zero or multiple matches are returned | PaymentMethodRule supplies a third-party display name | resolve_third_party_payment_method_by_opm |
| Unresolved display values are excluded from code-or-ID HDL attributes | Block DAT generation when a name would be placed in an attribute that requires a code or ID | Every create, update, or import request | |

## Validated Direct Reference Values

| Input Condition | Validation Result | Payload or DAT Behavior |
|---|---|---|
| A valid code or ID is supplied | Accepted without an additional name-resolution lookup | Use the validated code or ID directly |
| Both a display value and its validated code or ID are supplied | The values must identify the same reference | Use the validated code or ID; block when the pair conflicts |
| A code or ID is supplied but its validity isn't established | Not ready for import preparation | Validate it through the applicable authoritative reference contract before use |
| The same resolver inputs recur within one operation | Reuse the cached exact-match result | Don't issue a duplicate lookup for the same normalized resolver inputs |

## Payment Type Category Prerequisite

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Category is derived from the selected Payment Type LOV result | Use the Category returned for the currently selected payment type; don't accept an independently supplied Category as authoritative | Category-dependent validation is evaluated | derive_payment_category_by_payment_type |
| A Payment Type selection changes | Invalidate the prior derived Category and derive Category again for the new payment type | Payment Type changes during create, update, or import preparation | derive_payment_category_by_payment_type |
| Category can't be derived from exactly one payment type | Block preview and don't evaluate Category-dependent field requirements with a stale or assumed value | Payment Type lookup returns zero or multiple matches | derive_payment_category_by_payment_type |

## Developer-Supplied Mandatory Fields

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Organization Payment Method mandatory values | OrganizationPaymentMethodName, CurrencyCode, PaymentTypeCode or PaymentTypeId | Block preview and identify each missing field independently | Supply Name, Currency, and Payment Type; resolve display values through their existing reference resolvers when needed | Every OrganizationPaymentMethod create or update input | |
| PaymentSource source bank account | BankAccountId or BankAccountName | Block preview and identify Source Bank Account as mandatory | Supply a validated bank-account ID or a name that can be resolved through the existing bank-account resolver | A PaymentSource is present and derived Category isn't CA | resolve_bank_account_by_legal_employer |

## Shared OrganizationPaymentMethod and PaymentSource Field Map

| Validation Family | OrganizationPaymentMethod HDL Attribute | PaymentSource HDL Attribute |
|---|---|---|
| Bank name | BankNameEFT | BankNameEFT |
| Bank reference | BankReference | BankReferenceEFT |
| Bank reference type | BankReferenceType | BankReferenceTypeEFT |
| Company name | CompanyName | CompanyNameEFT |
| Company reference | CompanyReference | CompanyReferenceEFT |
| Company reference type | CompanyReferenceType | CompanyReferenceTypeEFT |
| Payment reference | PaymentReference | PaymentReferenceEFT |
| Payment free text | PaymentFreeText | PaymentFreeTextEFT |
| Additional payment text | AdditionalPaymentText | AdditionalPaymentTextEFT |
| Payment limit | PaymentLimit | PaymentLimitEFT |
| Transaction limit | TransactionLimit | TransactionLimitEFT |

## Thirty-Character Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| BankNameEFT is 30 characters or fewer | When invalid, display Enter 30 or fewer characters for BankNameEFT | OrganizationPaymentMethod or PaymentSource supplies BankNameEFT | |
| BankReference or BankReferenceEFT is 30 characters or fewer | Validate the populated level independently; when invalid, display Enter 30 or fewer characters for <FieldName> | OrganizationPaymentMethod or PaymentSource supplies the applicable bank-reference attribute | |
| BankReferenceType or BankReferenceTypeEFT is 30 characters or fewer | Validate the populated level independently; when invalid, display Enter 30 or fewer characters for <FieldName> | OrganizationPaymentMethod or PaymentSource supplies the applicable bank-reference-type attribute | |
| CompanyName or CompanyNameEFT is 30 characters or fewer | Validate the populated level independently; when invalid, display Enter 30 or fewer characters for <FieldName> | OrganizationPaymentMethod or PaymentSource supplies the applicable company-name attribute | |
| CompanyReference or CompanyReferenceEFT is 30 characters or fewer | Validate the populated level independently; when invalid, display Enter 30 or fewer characters for <FieldName> | OrganizationPaymentMethod or PaymentSource supplies the applicable company-reference attribute | |
| CompanyReferenceType or CompanyReferenceTypeEFT is 30 characters or fewer | Validate the populated level independently; when invalid, display Enter 30 or fewer characters for <FieldName> | OrganizationPaymentMethod or PaymentSource supplies the applicable company-reference-type attribute | |
| PaymentReference or PaymentReferenceEFT is 30 characters or fewer | Validate the populated level independently; when invalid, display Enter 30 or fewer characters for <FieldName> | OrganizationPaymentMethod or PaymentSource supplies the applicable payment-reference attribute | |
| EFTBureauReference and EFTUserReference are each 30 characters or fewer | Validate each field independently; when invalid, display Enter 30 or fewer characters for <FieldName> | Legislation isn't US and either named field is supplied | |

For every row above, replace `<FieldName>` with the exact field that failed. A failure in one field must not be reported as a failure in another field.

## US EFT Reference Validation

| Field | Required Format | Length | Validation Message | Applies When |
|---|---|---|---|---|
| EFTBureauReference | Exactly nine numeric digits | Exactly 9 characters | The value must match this pattern: ^[0-9]{9}$. Enter exactly 9 characters. | LegislationCode is US |
| EFTUserReference | Either exactly nine numeric digits or one printable ASCII character followed by exactly nine numeric digits | 9 to 10 characters | The number of characters is out of range. Enter 9 or more characters, up to a maximum of 10. The value is not in the correct format. Enter a value that matches this pattern: "NNNNNNNNN" Or "ANNNNNNNNN". Enter between 9 and 10 characters. | LegislationCode is US |

EFTBureauReference pattern:

```regex
^\d{9}$
```

EFTUserReference pattern:

```regex
^(?:[ -`{-~]?\d{9})$
```

The US patterns override the general 30-character rule for EFTBureauReference and EFTUserReference. The direct OrganizationPaymentMethod HDL mappings are EFTBureauReference to BankReference and EFTUserReference to CompanyReference. Apply each pattern to its mapped HDL attribute; don't substitute another attribute.

## One-Hundred-Twenty-Character Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| PaymentFreeText or PaymentFreeTextEFT is 120 characters or fewer | Validate the populated level independently; when invalid, display Enter 120 or fewer characters for <FieldName> | OrganizationPaymentMethod or PaymentSource supplies the applicable payment-free-text attribute | |
| AdditionalPaymentText or AdditionalPaymentTextEFT is 120 characters or fewer | Validate the populated level independently; when invalid, display Enter 120 or fewer characters for <FieldName> | OrganizationPaymentMethod or PaymentSource supplies the applicable additional-payment-text attribute | |

For each failure, replace `<FieldName>` with the exact attribute that exceeded 120 characters.

## Payment and Transaction Limit Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| PaymentLimit and PaymentLimitEFT accept integers only | Block a non-integer value; the developer source doesn't supply a separate non-integer error message | The applicable OrganizationPaymentMethod or PaymentSource field is supplied | |
| TransactionLimit and TransactionLimitEFT accept integers only | Block a non-integer value; the developer source doesn't supply a separate non-integer error message | The applicable OrganizationPaymentMethod or PaymentSource field is supplied | |
| PaymentLimit or PaymentLimitEFT exceeds the supplied numeric capacity of up to 20 numbers and 12 places to the right of the decimal | Display Enter a value with up to 20 numbers and 12 places to the right of the decimal. for <FieldName> | The applicable OrganizationPaymentMethod or PaymentSource field exceeds the capacity | |
| TransactionLimit or TransactionLimitEFT exceeds the supplied numeric capacity of up to 20 numbers and 12 places to the right of the decimal | Display Enter a value with up to 20 numbers and 12 places to the right of the decimal. for <FieldName> | The applicable OrganizationPaymentMethod or PaymentSource field exceeds the capacity | |

The integer-only rule permits zero decimal places. The supplied capacity message mentions up to 12 decimal places; retain that exact message for a capacity failure, but don't use it to permit decimal input.

## Prenotification Amount Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| PrenotificationAmount is a valid number with no more than two decimal places | When invalid, display Enter a valid number with up to 2 decimal places. | PrenotificationAmount is supplied | |

## FSCR Conditional Prenotification Validation

These developer-provided FSCR contracts preserve the exported Required=No metadata for Prenotification Amount and Prenotification Days. OPM.VALIDATE_INPUT normalizes aliases and preserves original input intent; it does not infer enablement from an affirmative value. OPM.RESOLVE_PRENOTIFICATION_ENABLEMENT and OPM.VALIDATE_PRENOTIFICATION_SELECTION in ora_design_enforcement.md determine legislation and Category enablement and selection eligibility before OPM.APPLY_DEFAULTS. OPM.VALIDATE_PRENOTIFICATION then validates the final requested state before populated DAT or ZIP generation and preview.

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| PrenotificationRequiredFlag and Prenotification Required identify the same flag | Normalize case-insensitive True, Enabled, Selected, Yes, or Y to HDL Y; normalize False, Disabled, Unselected, No, or N to HDL N; reject conflicting aliases or unsupported values; selected value and field enablement are separate states | Either flag name is supplied | |
| Original supplied state is preserved independently for each detail field | Distinguish omission, explicit value including 0, and explicit clearing, removal, blank, or null; an empty source cell counts as omission only when no explicit removal instruction exists; do not lose that instruction during workbook conversion | Every create or update request that includes prenotification intent | |
| Supplied prenotification detail values conform to existing contracts | Validate supplied PrenotificationAmount using the existing up-to-two-decimal-places rule and supplied PrenotificationDays against existing Number metadata; accept numeric 0; do not infer flag selection from detail values | Prenotification Amount or Prenotification Days is supplied | |

OPM.VALIDATE_PRENOTIFICATION owns validation of supplied detail values. Preserve explicit removal intent and report each invalid supplied field independently. Record original supplied state, enablement evidence, selected value, final value, and value origin. User values never override enablement or supplied-value validation.

## Resubmitted US Bank and Company Reference Clarification

This resubmission supplies the previously missing direct HDL mapping for the US-specific reference patterns. For this updated requirement, the business names BankReference and CompanyReference map to their component-specific HDL attributes shown below.

| Business Field | OrganizationPaymentMethod HDL Attribute | PaymentSource HDL Attribute | Mandatory at OrganizationPaymentMethod | Mandatory at PaymentSource | Applies When |
|---|---|---|---|---|---|
| BankReference | BankReference | BankReferenceEFT | No requirement supplied | Yes | LegislationCode is US |
| CompanyReference | CompanyReference | CompanyReferenceEFT | No requirement supplied | Yes | LegislationCode is US |

## Resubmitted US Reference Format Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| BankReference contains exactly nine numeric digits | When invalid, display The value must match this pattern: ^[0-9]{9}$. Enter exactly 9 characters. | OrganizationPaymentMethod supplies BankReference and LegislationCode is US | |
| BankReferenceEFT is present and contains exactly nine numeric digits | When missing, block preview and identify BankReference as mandatory; when invalid, display The value must match this pattern: ^[0-9]{9}$. Enter exactly 9 characters. | PaymentSource is present and LegislationCode is US | |
| CompanyReference contains exactly nine numeric digits or one printable ASCII character followed by exactly nine numeric digits | When invalid, display The number of characters is out of range. Enter 9 or more characters, up to a maximum of 10. The value is not in the correct format. Enter a value that matches this pattern: "NNNNNNNNN" Or "ANNNNNNNNN". Enter between 9 and 10 characters. | OrganizationPaymentMethod supplies CompanyReference and LegislationCode is US | |
| CompanyReferenceEFT is present and contains exactly nine numeric digits or one printable ASCII character followed by exactly nine numeric digits | When missing, block preview and identify CompanyReference as mandatory; when invalid, display The number of characters is out of range. Enter 9 or more characters, up to a maximum of 10. The value is not in the correct format. Enter a value that matches this pattern: "NNNNNNNNN" Or "ANNNNNNNNN". Enter between 9 and 10 characters. | PaymentSource is present and LegislationCode is US | |

BankReference and BankReferenceEFT pattern:

```regex
^\d{9}$
```

CompanyReference and CompanyReferenceEFT pattern:

```regex
^(?:[ -`{-~]?\d{9})$
```

## Resubmitted Validation Precedence

| Situation | What Happens |
|---|---|
| US OrganizationPaymentMethod BankReference or PaymentSource BankReferenceEFT is validated | Apply the exact-nine-digit US rule instead of the general 30-character rule |
| US OrganizationPaymentMethod CompanyReference or PaymentSource CompanyReferenceEFT is validated | Apply the 9-to-10-character US rule instead of the general 30-character rule |
| US PaymentSource is present | Require both BankReferenceEFT and CompanyReferenceEFT and validate each independently |
| A listed 30-character field other than the two US-special reference fields is supplied | Continue to apply the existing independent 30-character validation |
| LegislationCode isn't US | Apply the existing 30-character validation to BankReference or BankReferenceEFT and CompanyReference or CompanyReferenceEFT |
| Earlier EFTBureauReference or EFTUserReference validation aliases are encountered | Don't use those aliases for this resubmitted rule; the explicit HDL attributes are BankReference or BankReferenceEFT and CompanyReference or CompanyReferenceEFT according to component level |

## FSCR Project DAT Code and Source-System Validation

The following project-supplied rules apply when preparing an Organization Payment Methods DAT file. They supplement the existing source contracts; they do not replace any existing instruction.

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| OrganizationPaymentMethodCode is absent from the user input | Populate OrganizationPaymentMethodCode by copying OrganizationPaymentMethodName exactly; do not invent, abbreviate, generate, or resolve a code from Fusion | Every OrganizationPaymentMethod DAT record | |
| PaymentSourceCode is absent from the user input | Populate PaymentSourceCode by copying PaymentSourceName exactly; do not invent, abbreviate, generate, or resolve a code from Fusion | Every PaymentSource DAT record | |
| An OrganizationPaymentMethodCode or PaymentSourceCode is populated in the DAT | Block final DAT production when the populated Code does not exactly match its corresponding Name | Every OrganizationPaymentMethod or PaymentSource DAT record | |
| SourceSystemOwner or SourceSystemId is populated | Block final DAT production; omit both Source System fields from every generated DAT record | Every OrganizationPaymentMethod, PaymentSource, or PaymentMethodRule DAT record | |
| A proposed DAT value is not present in the source data or an explicit transformation rule | Block final DAT production and identify the fabricated value; preserve supplied source values exactly | Every DAT record | |

## Physical Payment Method Rule Deletion Validation

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| OPM delete target | LegislativeDataGroupId, OrganizationPaymentMethodName, SysEffectiveDate; or a validated OrgPaymentMethodId and SysEffectiveDate | Block archive preparation | Resolve the OPM by its exact name within the LDG and system-effective date, or provide the previously validated OPM ID | A permanent PaymentMethodRule deletion is requested | resolve_opm_by_exact_name_for_physical_delete |
| Payment Method Rule delete identity | One resolved active PaymentMethodRuleId and its PaymentSourceId | Block archive preparation | Retrieve the OPM rule hierarchy and require exactly one active rule selected for physical deletion | A permanent PaymentMethodRule deletion is requested | resolve_payment_method_rule_for_physical_delete |

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| The requested operation is explicitly permanent physical deletion | Use a DELETE record; don't substitute an end-date operation | A PaymentMethodRule deletion is requested | |
| The OPM exact-name lookup returns exactly one record within the selected LDG and SysEffectiveDate | Block on zero or multiple exact matches; don't choose a similarly named OPM | A permanent PaymentMethodRule deletion is requested | resolve_opm_by_exact_name_for_physical_delete |
| The selected OPM returns exactly one active Payment Method Rule | Block when zero or multiple active rules are returned; don't delete an arbitrary rule | A permanent PaymentMethodRule deletion is requested | resolve_payment_method_rule_for_physical_delete |
| The DELETE record contains the resolved PaymentMethodRuleId, PaymentSourceId, EffectiveStartDate, and EffectiveEndDate | Block archive preparation when any resolved identity or effective-date value is omitted, altered, or replaced by a fabricated value | A permanent PaymentMethodRule deletion is requested | resolve_payment_method_rule_for_physical_delete |
| The final delete archive is immutable after validation | Invalidate preview and require new validation when its SHA-256 changes | After archive preparation and before approval | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Resolver |
|---|---|---|---|---|---|---|---|---|
| OPM.VALIDATE_PHYSICAL_DELETE | step | 120 | validate_input | passed->OPM.DELETE_RESOLVE_OPM;failed->OPM.DELETE_FAILED | none | stop | A permanent PaymentMethodRule deletion is requested | |

## REST Hierarchy Finder Input Validation

These checks apply only to the read-only `/hcmRestApi/resources/latest/organizationPaymentMethods` hierarchy finders. They do not change the existing HDL date format or DAT validation rules.

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| LegislativeDataGroupId is present and is a valid resolved identifier | Stop before the request and identify LegislativeDataGroupId when absent or unresolved | `findByFilterCriteria` is invoked | retrieve_opms_by_ldg_and_effective_date |
| OrgPaymentMethodId is present and is a valid returned or resolved identifier for OPM detail retrieval | Stop before the request and identify OrgPaymentMethodId when absent or unresolved | `findByOrgPayMethodId` is invoked for OPM details | retrieve_opm_details_by_id_and_effective_date |
| OrgPaymentMethodId is present and is a valid returned or resolved identifier for rule retrieval | Stop before the request and identify OrgPaymentMethodId when absent or unresolved | `findByOrgPayMethodId` is invoked for Payment Method Rules | retrieve_payment_rules_by_opm_and_effective_date |
| ParentOrgPayMethodId is present and is a valid returned or resolved identifier | Stop before the request and identify ParentOrgPayMethodId when absent or unresolved | `paymentSourceFinder` is invoked | retrieve_payment_sources_by_parent_opm_and_effective_date |
| SysEffectiveDate matches `YYYY-MM-DD` and represents a real calendar date | Stop before the request and report the invalid SysEffectiveDate; don't convert it silently from the HDL `YYYY/MM/DD` representation | Every hierarchy finder invocation | |
| Finder parameters use the exact names documented for that finder | Stop before the request when an ID is supplied under a different finder parameter name | Every hierarchy finder invocation | |
| The required `expand` value is present without dropping any requested child expansion | Stop before metadata preparation and repeat only the read-only request with the documented expansion | OPM details, Payment Source, or Payment Method Rule retrieval | |

## REST Hierarchy Response Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Every response page is consumed before the collection is treated as complete | Continue through the documented pagination links or indicators; report an incomplete-response error if paging can't continue | Any finder returns a paged collection | |
| Every returned attribute has a runtime metadata entry | Block a claim of complete metadata until attribute name, object path, and all required metadata properties are present; mark undocumented characteristics through the runtime metadata profile | Every hierarchy finder response | |
| Logical dates are taken from the expanded `additionalDetails` at the correct hierarchy level | Retain the record but report missing logical-date metadata when the required expansion lacks documented logical dates | OPM details, Payment Sources, or Payment Method Rules are retrieved | |
| A child retains its returned parent or source identifier | Block hierarchy completion if the identifier is discarded; retain the child and identifier with a mapping error if it can't be resolved | Payment Source or Payment Method Rule is returned | |
| An ID and denormalized name refer to the same exact object | Preserve both on agreement; retain both conflicting values and report a mapping error on disagreement | A response or fallback lookup provides both values | |

## Payment Method Rule Conditional Field Validation

These developer-supplied rules describe the fields that are valid for each payment-method-rule type.

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| A default payment method rule supplies a Payment Source and does not supply Tax Reporting Unit, Third-Party Name, or Payment Criteria | Continue; Payment Source is the only editable selection for the default rule | DefaultFlag is Yes | |
| Tax Reporting Unit is supplied | Continue | DefaultFlag is No and ThirdPartyPaymentFlag is No | |
| Tax Reporting Unit is missing | Block the rule and require Tax Reporting Unit | DefaultFlag is No and ThirdPartyPaymentFlag is No | |
| Tax Reporting Unit or Third-Party Name is supplied | Continue | DefaultFlag is No and ThirdPartyPaymentFlag is Yes | |
| Both Tax Reporting Unit and Third-Party Name are missing | Block the rule and require at least one of those values | DefaultFlag is No and ThirdPartyPaymentFlag is Yes | |
| Third-Party Name is supplied while the third-party flag isn't selected | Block the rule; Third-Party Name is enabled only for a third-party payment rule | ThirdPartyPaymentFlag is No | |
| Tax Reporting Unit, Third-Party Name, or Payment Criteria is supplied on a default rule | Block the conflicting values; retain only the Payment Source selection for the default rule | DefaultFlag is Yes | |

## Payment Method Rule Pre-DAT Validation Gate

OPM.VALIDATE_RULE_CONDITIONS owns the conditional input checks above. This is a mandatory assisted preflight step before generating or converting any populated HDL DAT or upload ZIP, not merely an approval-preview check. This resource defines the task-runner validation contract; it does not add a standalone Data Loader Python validator.

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Every proposed PaymentMethodRule is evaluated against every applicable row in Payment Method Rule Conditional Field Validation | Record a separate result for each rule and applicable condition; pass only when every applicable condition passes | Before DAT generation for create or update, including a rule-only request using an existing OPM and Payment Source | |
| DefaultFlag and ThirdPartyPaymentFlag have known Yes or No values | Interpret Yes and Y as Yes, and No and N as No; stop for missing or unrecognized values unless a documented default establishes the value; do not infer a flag to avoid a required-field check | A PaymentMethodRule is proposed | |
| Required conditional selections contain a nonblank value | Treat absent, null, empty, and whitespace-only selections as missing; accept documented HDL ID or name/code alternatives for the same selection, subject to the existing dependency resolvers; a header or optional metadata declaration is not a supplied value | A conditional rule requires Tax Reporting Unit or Third-Party Name | |
| Validation evidence includes the evaluated flags, presence of Payment Source, TRU, third party and Payment Criteria, applicable conditions, results, and exact missing or conflicting fields | Block progression when condition-level evidence is missing or when any condition fails; a generic schema-valid or metadata-optional assertion cannot mark this node passed | Every proposed PaymentMethodRule | |
| Individual HDL metadata requiredness differs from conditional input requiredness | Enforce both contracts; optional live metadata never waives a conditional requirement in this resource | Before DAT generation and before Task Hook preview | |
| No PaymentMethodRule is proposed | Record not applicable with the reason and pass this conditional node; do not invent a rule or require TRU or third party for a source-only request | The create or update request contains no rule rows | |
| A rule fails conditional validation | Follow failed to OPM.FAILED, classify as input validation, identify the rule and exact missing or conflicting fields, and request correction; do not generate a populated DAT, upload ZIP, successful preview, or approval envelope | Any conditional check fails | |
| Defaulting, identity resolution, mapping, or later input changes alter the evaluated rule | Invalidate earlier conditional evidence and re-evaluate this gate before generating or regenerating the DAT; preserve supplied conflicts and do not silently remove them | The normalized rule differs from the evaluated input | |

A non-default third-party rule with neither TRU nor third party must stop with: You must specify a tax reporting unit or a third-party name for any payment rules used for third-party payments. A non-default employee-payment rule without TRU must stop and require a tax reporting unit. Default-rule selections and third-party selections with the third-party flag No remain subject to the existing blocking rows above.
