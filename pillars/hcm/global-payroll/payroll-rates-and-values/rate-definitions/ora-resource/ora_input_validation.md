# Rate Definitions HDL Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Import operation and object scope | RateDefinitionV2 and, when contributors are used, RateContributorV2; METADATA and MERGE records | Block preparation | Use the documented HDL object names and MERGE pattern; do not substitute REST or FSM | Every Rate Definition HDL request | |
| Target effective context | LegislativeDataGroupName, EffectiveStartDate, target environment | Block preparation | Supply the target LDG and an effective date that covers the intended setup | Every RateDefinitionV2 record | resolve_legislative_data_group_by_exact_name |
| Parent merge identity | RateDefinitionCode, LegislativeDataGroupName, EffectiveStartDate, and optional SourceSystemId and SourceSystemOwner | Block preparation | Validate the unique parent key and every child linkage in the prepared HDL artifact; preserve source-system identifiers when supplied | Every RateDefinitionV2 record | validate_rate_definition_hdl_identity |
| Rate identifiers | RateDefinitionCode, ShortName, RateDefinitionName, and the current target HDL template | Block preparation | Supply the target identifiers and validate their supported attributes against the target Data Loader template | Creating or updating a RateDefinitionV2 record | resolve_rate_definition_hdl_contract |
| Rate category design | Category and the category-specific source design | Block preparation | Specify Element, Derived Rate, or Value by Criteria and use only attributes present in the current target template | Every RateDefinitionV2 record | resolve_rate_definition_hdl_contract |
| Element-rate source | ElementCode, compatible StorageType, contributor input value, and periodicity/conversion choices | Block preparation | Supply the existing element and input-value codes and validate the selected HDL attributes against the current target template | Category is Element | resolve_rate_definition_hdl_contract |
| Derived-rate source | Contributor type and each balance, rate definition, base-rate, or overall-salary reference | Block preparation | Supply each contributor and validate the selected HDL attributes against the current target template | Category is Derived Rate | resolve_rate_definition_hdl_contract |
| Value-by-criteria source | Existing value-by-criteria definition and its target attribute mapping | Block preparation | Supply and validate the definition against the current target template | Category is Value by Criteria | resolve_rate_definition_hdl_contract |
| Contributor linkage and identity | RateDefinitionCode, LegislativeDataGroupName, EffectiveStartDate, contributor type, source value, and deterministic SequenceNumber; SourceSystemId and SourceSystemOwner are optional | Block preparation | Validate linkage to the one prepared parent record and unique sequence numbers; preserve child source identifiers when supplied | A RateContributorV2 record is included | validate_rate_definition_hdl_identity |
| Release-specific attribute contract | Current target RateDefinitionV2 Data Loader template and its RateContributorV2 section | Block preparation | Retrieve the template through core.data-loader before preparing production HDL | Every production HDL request | resolve_rate_definition_hdl_contract |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Required identifiers, effective context, source identity, and category design are supplied | Continue | Validate the local parent key and retrieve the target HDL template before assembling the file | validate_rate_definition_hdl_identity |
| A supplied parent or contributor source-system identifier is repurposed, or the parent link is not unambiguous | Blocked | Stop and correct the local identity or linkage; do not prepare a MERGE record | validate_rate_definition_hdl_identity |
| Any required group is missing or a selected HDL attribute is absent from the target template | Blocked | Identify the field and correct the source or template selection; do not prepare or import HDL | resolve_rate_definition_hdl_contract |
| Target template is unavailable or does not confirm the intended field contract | Blocked | Resolve the configured target environment or registered business object, then regenerate from the current template | resolve_rate_definition_hdl_contract |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| HDL record structure | Require METADATA to declare selected attributes and MERGE records for the intended create-or-update pattern; do not interpret a METADATA column as universally mandatory | Every supplied HDL data file | |
| Parent MERGE safety | Reject preparation when the local HDL artifact contains more than one parent for the same RateDefinitionCode, LDG, and effective date | A RateDefinitionV2 MERGE record is supplied | validate_rate_definition_hdl_identity |
| Contributor parent linkage | Reject a contributor whose RateDefinitionCode, LDG, effective date, or sequence does not correlate to the one prepared parent | A RateContributorV2 record is supplied | validate_rate_definition_hdl_identity |
| Effective-date format and coverage | Confirm the accepted date format and date-effective behavior from the current target Data Loader template | Every effective-dated record | resolve_rate_definition_hdl_contract |
| Sample-code handling | Validate ET, A, Y, D, IV, 1, and all other supplied coded values through the current template and HCM Data Loader validation | Every supplied coded value | resolve_rate_definition_hdl_contract |
| Contributor sequence | Require a deterministic order and a sequence unique within the definition and effective context | A RateContributorV2 record is supplied | validate_rate_definition_hdl_identity |
| Source-system lifecycle | Reject a local HDL artifact that reuses a supplied SourceSystemOwner and SourceSystemId pair for different parent or contributor identities | Create or update preparation | validate_rate_definition_hdl_identity |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RATE_DEFINITION.VALIDATE_INPUT | decision | 10 | validate_input | valid->RATE_DEFINITION.ASSESS_MERGE_IDENTITY;invalid->RATE_DEFINITION.HANDLE_INPUT_ERROR | none | stop | Validate RateDefinitionV2 and RateContributorV2 HDL inputs without inferring missing metadata or codes. |
