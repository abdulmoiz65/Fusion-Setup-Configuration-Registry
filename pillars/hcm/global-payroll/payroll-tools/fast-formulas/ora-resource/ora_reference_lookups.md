# Fast Formulas Reference Lookups

The supplied FastFormula metadata defines `FormulaTypeId` and
`LegislativeDataGroupId` as foreign object references. Resolve a supplied name
or display value to the corresponding supported code or ID before preparing
HDL. A code or ID that is already supplied with valid evidence is reused
without another lookup.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_fast_formula_type_reference | A formula-type name or display value is supplied and FormulaTypeId must be resolved, or a supplied FormulaTypeId requires validation | FormulaTypeName or display value; FormulaTypeId | GET /hcmRestApi/resources/latest/fastFormulaTypesLOV | FormulaTypeId, FormulaTypeName | Compare FormulaTypeName exactly when a name is supplied, or FormulaTypeId exactly when an ID requires validation; require exactly one match | FormulaTypeId: FormulaTypeId; FormulaTypeName: FormulaTypeName | Return a field-level validation error for zero matches; return ambiguity for multiple matches; don't choose automatically |
| resolve_legislative_data_group_reference | LegislativeDataGroupName is supplied and LegislativeDataGroupId and LegislationCode must be resolved, or a supplied LegislativeDataGroupId requires validation | LegislativeDataGroupName; LegislativeDataGroupId; LegislativeDataGroupId(SourceSystemId) | GET /hcmRestApi/resources/latest/legislativeDataGroupsLOV | LegislativeDataGroupId, Name, LegislationCode | Compare Name exactly when a name is supplied, or LegislativeDataGroupId exactly when an ID requires validation; require exactly one match | LegislativeDataGroupId: LegislativeDataGroupId; LegislativeDataGroupName: Name; LegislationCode: LegislationCode | Return a field-level validation error for zero matches; return ambiguity for multiple matches; don't choose automatically |
| resolve_yes_no_lookup_code | A Fast Formula attribute is defined by metadata as the predefined Yes/No LOV and a name or display value is supplied | Supplied Meaning or already-valid LookupCode | GET /fscmRestApi/resources/latest/commonLookupsLOV with finder=LookupTypeFinder;LookupType=YES_NO | LookupCode, Meaning | If an already-valid LookupCode is supplied, return not_required; otherwise compare Meaning exactly and require exactly one match | Target attribute code: LookupCode; Display value: Meaning | Return a field-level validation error for zero matches; return ambiguity for multiple matches; don't choose automatically |
| resolve_formula_status_lookup_code | A Fast Formula status attribute is defined by metadata as ORA_FORMULA_STATUS_VB and a name or display value is supplied | Supplied Meaning or already-valid LookupCode | GET /fscmRestApi/resources/latest/commonLookupsLOV with finder=LookupTypeFinder;LookupType=ORA_FORMULA_STATUS_VB | LookupCode, Meaning | If an already-valid LookupCode is supplied, return not_required; otherwise compare Meaning exactly and require exactly one match | Status field code: LookupCode; Status display value: Meaning | Return a field-level validation error for zero matches; return ambiguity for multiple matches; don't choose automatically |
| describe_fast_formulas_resource | Fast Formula REST attribute metadata, validation, reference, LOV, or finder metadata must be discovered | Authorized target Fusion session | GET /hcmRestApi/resources/latest//fastFormulas/describe | FormulaId, EffectiveStartDate, EffectiveEndDate, FormulaTypeId, BaseFormulaName, FormulaName, FormulaText, FormulaTypeName, Description, EditStatus, LegislativeDataGroupId, LegislativeDataGroupName, LegislationCode, CompileFlag, CreatedBy, CreationDate, LastUpdateDate, LastUpdatedBy, Compiled, CompileStatus; PrimaryKey and findByFilterCriteria finder metadata | Require one successful describe response from the intended target environment; don't infer metadata omitted by the response | Fast Formula REST attribute names, types, optionality, precision or maximum length, queryability, update behavior, descriptions, attachment action, finder names, and finder attributes | Stop if the describe request is unavailable, unauthorized, unsuccessful, incomplete, or from an unconfirmed target environment |
| list_fast_formulas_by_filter_criteria | The list of Fast Formulas must be retrieved for a Legislative Data Group and effective-date context | LegislativeDataGroupId; SysEffectiveDate mapped to EffectiveAsOfDate; optional LegislationCode when supplied | GET /hcmRestApi/resources/latest//fastFormulas/ with finder=findByFilterCriteria;LegislativeDataGroupId={LegislativeDataGroupId},EffectiveAsOfDate={SysEffectiveDate}; supplied example adds LegislationCode=US | FormulaId, FormulaName, LegislationCode, LegislativeDataGroupId, FormulaTypeId, FormulaTypeName, LegislativeDataGroupName, BaseFormulaName | Pass LegislativeDataGroupId unchanged; pass SysEffectiveDate as EffectiveAsOfDate; include the optional LegislationCode when supplied; return all matching records and don't select one automatically | FormulaId: FormulaId; FormulaName: FormulaName; LegislationCode: LegislationCode; LegislativeDataGroupId: LegislativeDataGroupId; FormulaTypeId: FormulaTypeId; FormulaTypeName: FormulaTypeName; LegislativeDataGroupName: LegislativeDataGroupName; BaseFormulaName: BaseFormulaName | Return an empty-list result for no records; return every matching record for multiple records; stop if the required finder values are missing or invalid |
| resolve_existing_fast_formula_for_update | FormulaName or Formula Type immutability must be validated before an update | Existing FormulaId; LegislativeDataGroupId; SysEffectiveDate mapped to EffectiveAsOfDate | GET /hcmRestApi/resources/latest//fastFormulas/ with finder=findByFilterCriteria;LegislativeDataGroupId={LegislativeDataGroupId},EffectiveAsOfDate={SysEffectiveDate} | FormulaId, FormulaName, FormulaTypeId, FormulaTypeName | Retrieve the filtered collection, compare FormulaId exactly with the supplied existing FormulaId, and require exactly one matching record | ExistingFormulaName: FormulaName; ExistingFormulaTypeId: FormulaTypeId; ExistingFormulaTypeName: FormulaTypeName | Return a field-level validation error when FormulaId or required finder inputs are missing or no exact FormulaId match exists; return ambiguity and don't compare or update when multiple exact matches exist |
| resolve_fast_formula_action_target | Formula content or compilation is requested for a persisted formula identified by FormulaName or FormulaId | FormulaName or FormulaId; target effective-date context when supplied | GET /hcmRestApi/resources/latest//fastFormulas/ using the primary endpoint finder for FormulaName or the PrimaryKey finder for FormulaId | FormulaId, FormulaName, EffectiveStartDate, EffectiveEndDate, Compiled, CompileStatus | Match the supplied FormulaName or FormulaId exactly, require exactly one effective record, and use its EffectiveStartDate as effectiveDate for the custom action | formulaId: FormulaId; effectiveDate: EffectiveStartDate; FormulaName: FormulaName; Compiled: Compiled; CompileStatus: CompileStatus | Return not found for zero exact matches; return ambiguity for multiple effective matches; don't invent formulaId or effectiveDate |
| get_fast_formula_content | Formula text is requested for a persisted formula and resolve_fast_formula_action_target returned formulaId and effectiveDate | formulaId; effectiveDate | POST {BASE_URL}/fastFormulas/action/getFormulaContent; Content-Type: application/vnd.oracle.adf.action+json; body fields formulaId and effectiveDate | result | Send the resolved formulaId and effectiveDate once and require a successful response with a result value | FormulaText: result | Stop when target resolution fails, the action is unauthorized or unsuccessful, or result is missing; don't substitute cached or supplied formula text |
| get_fast_formula_compile_message | Compiled is Y and CompileStatus is I or E for the resolved persisted formula | formulaId; effectiveDate | POST {BASE_URL}/fastFormulas/action/getFormulaCompileMsg; Content-Type: application/vnd.oracle.adf.action+json; body fields formulaId and effectiveDate | result | Send the resolved formulaId and effectiveDate once and require a successful response with a result value | FormulaCompileMessage: result | Stop when target resolution fails, the action is unauthorized or unsuccessful, or result is missing; preserve and display the returned compiler message |

## Primary Resource Attribute Metadata

The live describe response identifies the resource as fastFormulas but returns
the plural title User Column Instances and several user-column-oriented field
descriptions. Preserve those values as endpoint metadata; don't reinterpret
them as Fast Formula business semantics.

| Attribute | Data Type | Required? | Length or Precision | Queryable? | Updatable? | Allow Changes | Accepted Values or Format | Reference or LOV Dependency | Describe Description |
|---|---|---|---|---|---|---|---|---|---|
| FormulaId | integer | Optional | Not returned | Yes | No | never | Integer; no range or enumeration returned | None declared by describe metadata | Unique identifier of the user row. |
| EffectiveStartDate | date | Optional | Not returned | Yes | No | never | Date; no explicit wire format returned | None declared by describe metadata | Unique identifier of the user column instance. |
| EffectiveEndDate | date | Optional | Not returned | Yes | No | never | Date; no explicit wire format returned | None declared by describe metadata | Unique identifier of the user column. |
| FormulaTypeId | integer | Optional | Precision 18 | Yes | No | never | Integer; no range or enumeration returned | fastFormulaTypesLOV from existing task instructions | The userColumnInstances resource returns a list of user column instances. |
| BaseFormulaName | string | Optional | Precision 80 | Yes | No | never | String; no enumeration or pattern returned | None declared by describe metadata | Finds all the user column instances that match the specified primary key criteria. |
| FormulaName | string | Optional | Precision 120 | Yes | No | never | String; no enumeration or pattern returned | None declared by describe metadata | Value for the user column instance. |
| FormulaText | attachment | Optional | Not returned | No | No | never | GET attachment action with application/octet-stream response | None declared by describe metadata | Get user column instances. |
| FormulaTypeName | string | Optional | Precision 80 | Yes | No | never | String; no enumeration or pattern returned | fastFormulaTypesLOV from existing task instructions | Get a user column instance. |
| Description | string | Optional | Precision 240 | Yes | No | never | String; no enumeration or pattern returned | None declared by describe metadata | Unique identifier for the legislative data group. |
| EditStatus | string | Optional | Precision 30 | Yes | No | never | String; no enumeration or pattern returned | None declared by describe metadata | Finds the column instance from the effective end date. |
| LegislativeDataGroupId | integer | Optional | Precision 18 | Yes | No | never | Integer; no range or enumeration returned | legislativeDataGroupsLOV from existing task instructions | Update user column instance. |
| LegislativeDataGroupName | string | Optional | Precision 240 | Yes | No | never | String; no enumeration or pattern returned | legislativeDataGroupsLOV from existing task instructions | Finds all the user column instances that match the specified primary key criteria. |
| LegislationCode | string | Optional | Precision 30 | Yes | No | never | String; no enumeration or pattern returned | Legislative Data Group lookup returns LegislationCode under existing task instructions | Delete a user column instance. |
| CompileFlag | boolean | Optional | Precision 1; maximum length 1 | Yes | No | never | Boolean; no explicit accepted literals returned | None declared by describe metadata | Find a list of user column instances. |
| CreatedBy | string | Optional | Precision 64 | Yes | No | never | String; no enumeration or pattern returned | None declared by describe metadata | Effective end date of the user column instance. |
| CreationDate | datetime | Optional | Not returned | Yes | No | never | Datetime; no explicit wire format returned | None declared by describe metadata | Effective start date of the user column instance. |
| LastUpdateDate | datetime | Optional | Not returned | Yes | No | never | Datetime; no explicit wire format returned | None declared by describe metadata | Get user column instances. |
| LastUpdatedBy | string | Optional | Precision 64 | Yes | No | never | String; no enumeration or pattern returned | None declared by describe metadata | Create a user column instance. |
| Compiled | string | Optional | Precision 4000 | Yes | No | never | String; no enumeration or pattern returned | None declared by describe metadata | Finds the column instance from the effective end date. |
| CompileStatus | string | Optional | Precision 1 | Yes | No | never | String; no enumeration or pattern returned | None declared by describe metadata | Finds the column instance from the effective start date. |

## Finder Metadata

| Finder | Finder Description | Finder Attribute | Data Type | Required? | Queryable? | Updatable? | Allow Changes | Accepted Values or Format | Attribute Description |
|---|---|---|---|---|---|---|---|---|---|
| PrimaryKey | Get a user column instance. | FormulaId | integer | Optional | Yes | Yes | never | Integer; no range or enumeration returned | Get user column instances. |
| findByFilterCriteria | Effective end date of the user column instance. | CompileStatus | string | Optional | No | Yes | always | String; no enumeration or pattern returned | Unique identifier of the user column instance. |
| findByFilterCriteria | Effective end date of the user column instance. | CreatedBy | string | Optional | No | Yes | always | String; no enumeration or pattern returned | No description returned. |
| findByFilterCriteria | Effective end date of the user column instance. | EffectiveAsOfDate | date | Optional | No | Yes | always | Date; no explicit wire format returned | Unique identifier for the legislative data group. |
| findByFilterCriteria | Effective end date of the user column instance. | FormulaName | string | Optional | No | Yes | always | String; no enumeration or pattern returned | Unique identifier of the user column. |
| findByFilterCriteria | Effective end date of the user column instance. | FormulaTypeId | integer | Optional | No | Yes | always | Integer; no range or enumeration returned | The userColumnInstances resource returns a list of user column instances. |
| findByFilterCriteria | Effective end date of the user column instance. | LegislationCode | string | Optional | No | Yes | always | String; no enumeration or pattern returned | Effective start date of the user column instance. |
| findByFilterCriteria | Effective end date of the user column instance. | LegislativeDataGroupId | integer | Optional | No | Yes | always | Integer; no range or enumeration returned | Value for the user column instance. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A reference name or display value is supplied | Run the applicable resolver and use its resolved code or ID in the HDL record. |
| A code or ID is supplied with valid evidence | Use it directly and don't perform another lookup. |
| A supplied code or ID isn't yet validated | Use the applicable resolver once its endpoint contract is complete; don't treat presence alone as validity. |
| A name or display value returns exactly one match | Use only the corresponding returned code or ID supported by the selected HDL attribute form. |
| A name or display value returns no match | Return a validation error identifying the field and invalid supplied value. |
| A name or display value returns multiple matches | Return an ambiguity error and don't select a result automatically. |
| A name remains unresolved | Don't place the unresolved name in an HDL field that requires a code or ID. |
| The same reference value is used again within one operation | Reuse the resolved value from the operation-local cache and don't repeat the lookup. |
| Lookup authentication, authorization, paging, transport, or endpoint contract is incomplete | Stop reference resolution and don't prepare a production-ready import record. |
| No authenticated Fusion session is active | Establish or refresh the configured authorized session, then call only the captured read-only reference endpoint; don't request or persist credentials in resource files. |
| A lookup session expires during the read | Refresh the configured session once and repeat only the read-only lookup; don't retry an HDL mutation. |
| A Yes/No LOV field receives a display value | Resolve it through YES_NO and place the returned LookupCode in the code field. |
| A formula status field receives a display value | Resolve it through ORA_FORMULA_STATUS_VB and place the returned LookupCode in the status code field. |
| Fast Formula REST metadata is needed | Invoke describe_fast_formulas_resource through an authorized target Fusion session and capture every returned attribute, data type, requiredness rule, validation, accepted value, format, length, reference or LOV dependency, finder, and finder attribute before treating the catalog as complete. |
| The Fast Formula list finder is invoked | Map SysEffectiveDate to EffectiveAsOfDate, preserve LegislativeDataGroupId, include LegislationCode only when supported, and preserve all returned matches. |
| FormulaName or Formula Type immutability is validated for update | Run resolve_existing_fast_formula_for_update, require exactly one FormulaId match, and compare the proposed values with the returned existing FormulaName and FormulaTypeId or FormulaTypeName. |
| The supplied section title says Retrieve Organization Payment Methods | Use the supplied fastFormulas endpoint, finder, and response mapping as the resource identity; don't route this lookup to an Organization Payment Methods resource. |
| Formula content or compilation is requested by FormulaName or FormulaId | Run resolve_fast_formula_action_target first and carry its FormulaId and EffectiveStartDate forward as formulaId and effectiveDate; don't ask the user to invent either value. |
| Persisted formula text is requested | After exact target resolution, call get_fast_formula_content with the required action content type and return the response result as FormulaText. |
| Compiled is Y and CompileStatus is I or E | Call get_fast_formula_compile_message with the resolved action target and display the returned result without rewriting the compiler message. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| FF.RESOLVE_REFERENCES | decision | 3 | reference_lookup | resolved->FF.APPLY_DEFAULTS;not_required->FF.APPLY_DEFAULTS;blocked->FF.HANDLE_ERROR | FF.RESOLVE_DEPENDENCIES | stop | A Fast Formula Type or Legislative Data Group reference or LOV-style value requires validation or resolution |

## Sources

- Developer-provided standard reference and LOV instructions, received 2026-08-17.
- Developer-provided Fast Formula reference endpoint and session instructions, received 2026-08-17.
- Developer-provided /scratch/share/FastFormulasExport.xls, accessed 2026-08-17.
- Developer-provided Fast Formula primary REST describe endpoint, corrected finder invocation, example, and response mappings, received 2026-08-18.
- Live GET /hcmRestApi/resources/latest//fastFormulas/describe response from the configured Fusion environment, accessed 2026-08-18.
- Developer-provided persisted formula-content and formula-compilation custom-action contracts, received 2026-08-18.
