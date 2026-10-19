# Manage HCM Extract Definitions Defaulting Rules

These rules define task-local defaults for generated Data Loader source artifacts. Apply defaults after task identity, operation intent, and registered Data Loader metadata are resolved, and before dependency readiness and source generation.

## Defaulted Fields

| Field | Default | Applies When | Source Attribute | Override Rule | Validation |
|---|---|---|---|---|---|
| Changes Only | No | Scratch `Extract Definitions` creation and registered metadata exposes `ChangesOnlyFlg` | `ChangesOnlyFlg=N` | If the user explicitly requests changes-only extraction, generate `ChangesOnlyFlg=Y` | Value must be `Y` or `N` |
| Freeze Status | No | Scratch `Extract Definitions` creation and registered metadata exposes `FreezeStatus` | `FreezeStatus=N` | If the user explicitly requests the definition to be locked/frozen, generate `FreezeStatus=Y` | Value must be `Y` or `N` |
| Unfreeze Comments | Generated. | Scratch `Extract Definitions` creation and registered metadata exposes `UnfreezeComments` | `UnfreezeComments=Generated.` | Preserve user-supplied unfreeze comments after validation | Non-empty when generated |
| Main Block | Yes | Scratch `Extract Data Groups` creation includes exactly one block/data group | `MainBlockFlg=Y` | For multiple block/data groups, resolve which block is main before preview | Value must be `Y` or `N` |
| Filter Criteria Flag | Criteria expression | Extract data group filter criteria creation uses expression-based criteria | `CriteriaFlg=C` | Formula-based criteria requires explicit supported formula input | Value must be valid for the requested criteria mode |
| Filter Criteria Effective Start Date | Extract definition start date | Extract data group filter criteria creation | `EffectiveStartDate=<DateStart>` | User-supplied effective start date overrides the default after date validation | Value must use the accepted Data Loader date format |
| Filter Criteria Effective End Date | Open-ended date | Extract data group filter criteria creation | `EffectiveEndDate=4712-12-31` | User-supplied effective end date overrides the default after date validation | Value must use the accepted Data Loader date format |
| Filter Criteria Rest Action | Create | Extract data group filter criteria creation | `RestAction=POST` | Preserve supplied supported action | `POST` for create |
| Record Type | Detail record | Scratch `Extract Records` creation | `TypeCode=D` | User-supplied value overrides the default after lookup resolution through `PER_EXT_RECORD_TYPE_CODES` | Value must resolve to one lookup code |
| Process Code | Fast Formula | Scratch `Extract Records` creation | `ProcessCode=FF` | User-supplied value overrides the default after lookup resolution through `PER_EXT_RECORD_PROCESS_CODES` | Value must resolve to one lookup code |
| Record Effective Start Date | Extract definition start date | Scratch `Extract Records` creation | `EffectiveStartDate=<DateStart>` | User-supplied effective start date overrides the default after date validation | Value must use the accepted Data Loader date format |
| Record Effective End Date | Open-ended date | Scratch `Extract Records` creation | `EffectiveEndDate=4712-12-31` | User-supplied effective end date overrides the default after date validation | Value must use the accepted Data Loader date format |
| Record Sequence | Starts at 5 and increments by 5 | Scratch `Extract Records` creation | `Sequence=5,10,15...` | User-supplied sequence overrides the generated value after numeric validation | Value must be numeric and unique within the generated record set |
| Record XML Tag Name | Record-name tag | Scratch `Extract Records` creation | `XmlTagName=<RECORD_NAME_TAG>` | User-supplied XML tag overrides the default after XML tag validation | Value must be a valid XML tag |
| Record Flex Structure Code | Record-name tag | Scratch `Extract Records` creation | `FlexStructureCode=<RECORD_NAME_TAG>` | User-supplied value overrides the default after validation | Value must be non-empty |
| Record Hide Flag | No | Scratch `Extract Records` creation | `HideFlg=N` | User-supplied value overrides the default after yes/no validation | Value must be `Y` or `N` |
| Record Required Flag | No | Scratch `Extract Records` creation | `RequiredFlg=N` | User-supplied value overrides the default after yes/no validation | Value must be `Y` or `N` |
| Data Element Type Code | Database Item | Scratch DBI-backed `Extract Attributes` creation | `TypeCode=F` | User-supplied type overrides only after supported type-code resolution | Value must be a valid extract data element type code |
| Data Element Name | Resolved DBI group name | Scratch `Extract Attributes` creation | `DataElementName=<resolved DBI/group name>` | User-supplied `DataElementName` overrides after validation | Value must be non-empty |
| Data Element XML Tag Name | Data-element-name tag | Scratch `Extract Attributes` creation | `XmlTagName=<DATA_ELEMENT_NAME_TAG>` | User-supplied XML tag overrides after validation | Value must be a valid XML tag |
| Data Element Short Code | Data-element-name short code | Scratch `Extract Attributes` creation | `ShortCode=<derived short code>` | User-supplied short code overrides after validation | Value must be non-empty and fit metadata length |
| Data Element Information Column | Starts at 1 and increments by 1 | Scratch `Extract Attributes` creation | `InformationColumn=1,2,3...` | User-supplied value overrides after numeric validation | Value must be numeric and unique within the generated data element set |
| Data Element Information Label | Data element name | Scratch `Extract Attributes` creation | `InformationLabel=<DataElementName>` | User-supplied label overrides after validation | Value must be non-empty |
| Data Element Hide Flag | No | Scratch `Extract Attributes` creation | `HideFlg=N` | User-supplied value overrides after yes/no validation | Value must be `Y` or `N` |
| Data Element Required Flag | No | Scratch `Extract Attributes` creation | `RequiredFlg=N` | User-supplied value overrides after yes/no validation | Value must be `Y` or `N` |
| Data Element Context Flag | No | Scratch `Extract Attributes` creation | `ContextFlg=N` | User-supplied value overrides after yes/no validation | Value must be `Y` or `N` |
| Data Element UI Hide Flag | No | Scratch `Extract Attributes` creation | `UIHideFlg=N` | User-supplied value overrides after yes/no validation | Value must be `Y` or `N` |
| Data Element Attribute Twenty Five | No | Scratch `Extract Attributes` creation | `AttributeTwentyFive=N` | User-supplied value overrides after yes/no validation | Value must be `Y` or `N` |
| Data Element Start Date | Extract definition start date | Scratch `Extract Attributes` creation | `StartDate=<DateStart>` | User-supplied start date overrides after date validation | Value must use the accepted Data Loader date format |
| Delivery Option Base Name | Delivery option name | Scratch `Extract Delivery Options` creation | `BaseDeliveryOptionName=DeliveryOptionName` | Preserve supplied value after validation | Non-empty |
| Delivery Option Type | Explicit user input | Scratch `Extract Delivery Options` creation | No default | User must supply `NONE` | Only `NONE` is supported |
| Delivery Option Output Type | XML | Scratch `Extract Delivery Options` creation | `OutputType=XML` | User-supplied value overrides after validation | Value must be `DATA` or `XML` |
| Delivery Option Output Name | Delivery option name | Scratch `Extract Delivery Options` creation | `OutputName=DeliveryOptionName` | User-supplied value overrides after validation | Non-empty |
| Delivery Option Date From | Extract definition start date | Scratch `Extract Delivery Options` creation | `DateFrom=<DateStart>` | User-supplied date overrides after date validation | Valid Data Loader date |
| Delivery Option Rest Action | Create | Scratch `Extract Delivery Options` creation | `RestAction=POST` | Preserve supplied supported action | `POST` for create |
| Delivery Option Detail Types for `NONE` | Standard no-delivery detail rows | Scratch `Extract Delivery Options` creation with `DeliveryTypeNew=NONE` | Generate `ExtractDeliveryOptionDetail` rows for `BURSTING`, `FILE_NAME_DE`, `KEY`, `LOCALE`, `OBJECT_ID`, `OBJECT_TYPE`, `SYSTEM_DOCUMENT_TYPE`, `TIMEZONE`, `ZIP` | Preserve supported option-specific values when supplied | Each row uses `DefinitionName`, `DeliveryOptionName`, `OptionType`, and `RestAction=POST`; include `OptionValue` only when supplied as a supported option-specific value |
| Parameter Base Name | Parameter name | Custom parameter creation | BaseParameterName=ParameterName | Preserve supplied value after validation | Non-empty and within live metadata length |
| Parameter XML Tag | Trim parameter name, replace spaces with underscores, and prefix an underscore when the first character is a digit | Custom parameter creation | XmlTagName | Preserve supplied value after validation | Valid XML name within live metadata length |
| Parameter ESS Name | Trim parameter name, replace spaces with underscores, and uppercase | Custom parameter creation | ESSParameterName | Preserve supplied value after validation | Valid name within live metadata length; unique within the requested parent definition |
| Parameter Allowed In Expression | Y | Custom parameter creation | AllowedInExpression | Preserve valid supplied override | Y or N |
| Parameter Generated | N | Custom parameter creation | Generated | Preserve valid supplied override | Y or N |
| Parameter Display Flag | Y | Custom parameter creation | DisplayFlg | Preserve valid supplied override | Y or N |
| Parameter Usage Type | INPUT | Custom parameter creation | ParameterUsageType | Resolve coded overrides through the declared lookup contract | Valid registered usage type |

## Defaulting Rules

| Situation | What Happens |
|---|---|
| Custom parameters are requested | Apply parameter naming rules and defaults before dependency readiness; preserve validated explicit overrides |
| ParameterDisplayType, ParameterSequence, lookup, value-set, or default-value fields are supplied or conditionally required | Validate the applicable metadata and declared lookup contract; include resolved values only, with no automatic defaults for these fields |
| A parameter coded override needs an undeclared lookup contract | Stop before preview and report the unresolved contract |
| User does not supply Changes Only for scratch creation and metadata exposes `ChangesOnlyFlg` | Generate `ChangesOnlyFlg=N` |
| User explicitly requests Changes Only | Generate `ChangesOnlyFlg=Y` |
| Metadata does not expose `ChangesOnlyFlg` | Do not invent the field; continue without it and record that the default was not applicable |
| ChangesOnlyFlg is generated with any value other than `Y` or `N` | Stop before preview |
| User does not supply Freeze Status for scratch creation and metadata exposes `FreezeStatus` | Generate `FreezeStatus=N` |
| User explicitly requests the definition to be locked/frozen | Generate `FreezeStatus=Y` |
| Metadata does not expose `FreezeStatus` | Do not invent the field; continue without it and record that the default was not applicable |
| FreezeStatus is generated with any value other than `Y` or `N` | Stop before preview |
| User does not supply Unfreeze Comments for scratch creation and metadata exposes `UnfreezeComments` | Generate `UnfreezeComments=Generated.` |
| Metadata does not expose `UnfreezeComments` | Do not invent the field; continue without it and record that the default was not applicable |
| UnfreezeComments is generated as empty | Stop before preview |
| Scratch `Extract Data Groups` creation includes exactly one block/data group | Generate `MainBlockFlg=Y` |
| Multiple block/data groups are created in one source | Resolve main-vs-child intent before preview |
| MainBlockFlg is generated with any value other than `Y` or `N` | Stop before preview |
| Extract data group filter criteria is generated from an expression | Default `CriteriaFlg=C`, `EffectiveStartDate=<DateStart>`, `EffectiveEndDate=4712-12-31`, and `RestAction=POST` |
| User supplies filter criteria effective dates | Preserve after date validation |
| Formula-based filter criteria is requested | Require explicit supported formula input before source generation |
| Scratch `Extract Records` creation | Default `TypeCode=D`, `ProcessCode=FF`, `EffectiveStartDate=<DateStart>`, `EffectiveEndDate=4712-12-31`, `XmlTagName=<RECORD_NAME_TAG>`, `FlexStructureCode=<RECORD_NAME_TAG>`, `HideFlg=N`, `RequiredFlg=N`, and assign `Sequence` values starting at `5` with increments of `5` |
| User supplies Record Type | Resolve through `PER_EXT_RECORD_TYPE_CODES` and generate the resolved LookupCode into `TypeCode` |
| User supplies Process Code | Resolve through `PER_EXT_RECORD_PROCESS_CODES` and generate the resolved LookupCode into `ProcessCode` |
| User supplies record effective dates | Preserve after date validation |
| User supplies Sequence | Preserve after numeric and uniqueness validation |
| A task-standard defaulted field is exposed by metadata | Generate the applicable default unless the user supplied a valid override |
| Scratch `Extract Attributes` creation | Default `DataElementName` from the resolved DBI/group name unless supplied; generate `TypeCode=F`, `XmlTagName`, `ShortCode`, `InformationColumn`, `InformationLabel`, `HideFlg=N`, `RequiredFlg=N`, `ContextFlg=N`, `UIHideFlg=N`, `AttributeTwentyFive=N`, and `StartDate=<DateStart>` |
| Scratch `Extract Delivery Options` creation | Default `BaseDeliveryOptionName=DeliveryOptionName`, `OutputType=XML`, `OutputName=DeliveryOptionName`, `DateFrom=<DateStart>`, `RestAction=POST`; require explicit `DeliveryTypeNew=NONE`; and for `NONE` generate the standard `ExtractDeliveryOptionDetail` option-type rows |
| DBI-backed extract data element is generated | Require `DataType` as user input and validate it as `N`, `D`, or `T` |
| Data element `ShortCode` is generated | First generate the data-element-name tag by replacing spaces with underscores. If that value is 30 characters or less, use it as the short code. If it is longer than 30 characters, split it by underscores, take the first character of each non-empty word, then append the generated `InformationColumn` |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HCM_EXT_DEF.APPLY_DEFAULTS | step | 75 | apply_defaults | applied->HCM_EXT_DEF.RESOLVE_DEPENDENCIES;not_applicable->HCM_EXT_DEF.RESOLVE_DEPENDENCIES;blocked->HCM_EXT_DEF.RETURN_ISSUES | HCM_EXT_DEF.LOOKUP_PARAMETER_DATA_TYPE | stop | Operation intent is extract definition creation, extract block/data group creation, extract data group filter criteria creation, extract record creation, extract data element creation, extract delivery option creation, or custom parameter creation; unchanged imported sources use not_applicable |
