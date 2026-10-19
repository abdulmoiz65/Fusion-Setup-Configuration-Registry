# RMCS Data Model and Output Routing

This file owns record-level output selection, existing mapped-value updates and RMCSInterface.insert fields. It is not an AR interface contract. Read [input preflight](ora_algorithm_xml_guidance.md#input-preflight) and use the selected action's bindings before applying it.

## Physical objects and runtime bindings

| Record level | Subscription staging object | Revenue Management physical object | Algorithm output alias |
|---|---|---|---|
| Header | OSS_RMCS_DOC_T | VRM_SOURCE_DOCUMENTS | RmcsDoc |
| Line | OSS_RMCS_DOC_LINES_T | VRM_SOURCE_DOC_LINES | RmcsDocLines |
| Subline / satisfaction event | OSS_RMCS_DOC_SUB_LINES_T | VRM_SOURCE_DOC_SUB_LINES | RmcsDocSublines |

These are object-level relationships, not proof of column-to-column mapping. Use the existing [physical identities](../../manage-service-mappings-for-subscriptions-to-revenue-recognition/ora-resource/ora_reference_lookups.md#physical-object-identities), [source column evidence](../../manage-service-mappings-for-subscriptions-to-revenue-recognition/ora-resource/ora_reference_lookups.md#source-column-evidence) and [target column evidence](../../manage-service-mappings-for-subscriptions-to-revenue-recognition/ora-resource/ora_reference_lookups.md#target-column-evidence) for documented fields and restrictions. Check current Oracle documentation for release-sensitive questions; the algorithm and mapping supplied for this request establish current runtime names/access.

Do not equate a physical column, UI label, REST attribute, VO attribute and Service Mapping alias by similar spelling. The line extension runtime context VRM_SOURCE_DOCUMENT_LINES intentionally differs from the physical table VRM_SOURCE_DOC_LINES.

## Direct assignment or additional-detail insertion

Resolve the intended target's business meaning and record level first, then inspect the relevant active mapping output entity:

| Evidence | Permitted proposal |
|---|---|
| Relevant output attribute already exposed and writable for the selected algorithm consumer | Assign to the actual mapped alias.attribute in the modification section |
| Requested line DFF/flex target and the corresponding `RmcsDocLines.SrcAttribute*` slot is already exposed in Service Mapping | Do not direct-assign that existing mapped slot unless the implementer explicitly asks to modify that exact slot. Otherwise treat the mapped slot as occupied, choose the next compatible line SRC_ATTRIBUTE slot not present in Service Mapping as an assumption-backed candidate, and use the line `RMCSInterface.insert` contract |
| Attribute exposed but not writable | Stop that write and return the access restriction; do not evade it through insert or modify the seeded entity |
| Header/line target absent from the mapped output, but physical column and requested use are supported | Propose RMCSInterface.insert with the contract below after source/type/context prerequisites pass |
| Subline target absent from the mapped output | Stop: adding new subline values via insert or adding output schema attributes is not supported |
| Alias, equivalence, access or physical support uncertain | Route the mapping question to the companion; hold dependent Groovy |

The protected output entities RmcsDoc, RmcsDocLines and RmcsDocSublines must not be extended or have their definitions modified by the implementer. Assigning an existing writable value is distinct from changing that entity's schema. The [mapping guide](../../manage-service-mappings-for-subscriptions-to-revenue-recognition/resources/ora_service_mapping_guidance.md) owns access/provider validation.

Use the actual mapped attribute, not a guessed physical-column spelling. When the requested output already matches an exposed writable RmcsDoc, non-DFF RmcsDocLines or RmcsDocSublines attribute, the proposal may be a direct mapped assignment such as alias.attribute = value when no extra condition, conversion, null guard or collection handling is needed; otherwise keep the smallest guarded Groovy required by the accepted rule. For `RmcsDocLines.SrcAttributeChar*`, `RmcsDocLines.SrcAttributeNumber*` and `RmcsDocLines.SrcAttributeDate*`, exposed writable mapping is evidence that the slot is already in use. Do not write `RmcsDocLines.SrcAttributeChar1`, `RmcsDocLines.SrcAttributeChar2` and so on for a new line DFF/flex requirement unless the implementer explicitly supplied that exact slot to modify. The inspected mapping makes RmcsDocLines.ExtractionStatus non-writable; do not assume every declared output attribute can be assigned. Control values such as SkipFlag can be writable without a VO provider attribute mapping.

Before proposing a replacement of a value already supplied by delivered or customer logic, state the existing behavior and the requested change explicitly. Use the Groovy guide's [conflicting output review](ora_groovy_function_guidance.md#conflicting-output-review) to resolve retained/new operations; write access alone is not acceptance of a changed business outcome.

## Header and line insert contract

The call form supplied by the user is RMCSInterface.insert([ ... ]). Populate one map for the supported physical target field; do not copy an AR helper or invent a target entity argument.

| Map field | Header action | Line action |
|---|---|---|
| AttributeName | Confirmed physical column of VRM_SOURCE_DOCUMENTS | Confirmed physical column of VRM_SOURCE_DOC_LINES |
| AttributeValue | Approved derived value or literal, with verified type and null behavior | Approved derived value or literal, with verified type and null behavior |
| AttributeContext for standard fields | Standard | Standard |
| AttributeContext for supported SRC_ATTRIBUTE_CHAR / NUMBER / DATE extensions | VRM_SOURCE_DOCUMENTS | VRM_SOURCE_DOCUMENT_LINES |
| SourceId | RmcsDoc.DocumentId | RmcsDocLines.DocumentLineId |
| TransactionType | DOCUMENT | DOCUMENT_LINE |
| FlexContext for standard fields | Omit the key | Omit the key |
| FlexContext for extensions | VRM_SOURCE_DOCUMENTS per the user contract; preserve existing customer values/null unless an approved change requires otherwise | See the confirmation gate below |

SourceId is the fixed row-identity expression shown, NOT a hardcoded numeric record ID. TransactionType and context strings use the exact casing above. Select a physical AttributeName only after confirming column support, type, allowed length/precision and the implementer's intended use. Do not choose a sample slot, force the casing of an existing customer string or hardcode example custom fields/business values.

The source mapping declares the RMCSInterface payload attributes as strings; that declaration alone does not establish runtime coercion of numbers/dates. Apply the canonical [DATE/timestamp value rule and conversion evidence requirements](ora_groovy_function_guidance.md#date-and-timestamp-value-handling), not an AR conversion rule or a guessed cast. AttributeType and XsiType are not mandatory keys in the supplied insert contract; do not add them by borrowing AR behavior or merely because an attribute exists in XML.

### Line FlexContext confirmation

The author's prose specifies VRM_SOURCE_DOCUMENT_LINES, but its illustrative line insert uses FUSION_OSS. Treat this as a known conflict, not two interchangeable defaults. For a new line extension insert, obtain confirmation of the deployed FlexContext before final Groovy approval. Preserve an existing customer value or null unless its change is explicitly in scope. Do not silently substitute FUSION_OSS, null or a header context. This question affects line extension inserts, not standard fields or unrelated direct assignments.

## Subline updates and skip behavior

RMCSInterface.insert is prohibited in subline processing. Use only an existing writable RmcsDocSublines attribute in the structurally selected subline action, for example the confirmed SatisfactionEventQuantity attribute when that is the requirement. Do not allocate SRC_ATTRIBUTE extension slots or infer that documented physical subline columns are writable through this skill. Follow [missing subline step](ora_algorithm_xml_guidance.md#missing-subline-step) when the input lacks the needed action.

For requested skipping, use the existing writable SkipFlag on the correct current row: RmcsDoc for a document, RmcsDocLines for a line, or RmcsDocSublines for a subline. Values are uppercase 'Y' to skip and 'N' not to skip, with the condition and reset behavior confirmed from the requirement. Do not turn a line-only skip into a document-wide skip because an example mentions RmcsDoc. If the relevant row is not current-row scoped in the selected action, resolve scope rather than assigning to a collection.

## Target resolution when omitted

Use this staged recommendation when the implementer supplies an outcome or source value without an exact target. A recommendation is not target acceptance or proof of deployment.

1. Establish the intended document, line or satisfaction-event meaning, the behavior to change and the requested visibility/use of the value. Resolve materially different outcomes before choosing a field. A line-only requirement must not become a document-wide operation because a sample uses RmcsDoc.
2. Read the accepted [source-resolution record](../../manage-service-mappings-for-subscriptions-to-revenue-recognition/resources/ora_service_mapping_guidance.md#source-resolution-record). Establish the actual scalar value type from current mapping or verified provider/describe evidence, together with null and collection handling. A business attribute ending in Id, ID or _ID is numeric only when its type evidence is numeric; codes and display identifiers may be character values. This classification does not change the fixed SourceId expressions in the insert contract.
3. Compare documented, supported standard fields at the selected record level by functional meaning and type. If the implementer gives a business target but not the exact physical column, use the RMCS/VRM documentation evidence referenced by this skill to identify named candidates; the missing exact column blocks final approval only until a candidate, context and usage are accepted. Recommend a standard target only when its definition is a direct business match and the current RMCS operation supports that use. Do not repurpose an amount, date or identifier column merely because its storage type fits.
4. Inspect the existing active output mappings for the intended target or a verified semantic equivalent. Resolve actual alias, consumer access and current-row binding through the companion. Use an existing writable mapped value where the direct-assignment rule applies; a read-only value is a restriction, not permission to bypass it through insert. For line DFF/flex targets, treat every mapped `RmcsDocLines.SrcAttribute*` slot as occupied unless the implementer explicitly says the requirement is to modify that exact slot; occupied mapped slots drive next-slot selection, not direct assignment. Explain any delivered/current value that the proposal would replace.
5. If no supported standard field fits, consider only documented header/line extension fields and their deployed intended use. Select a candidate SRC_ATTRIBUTE_CHAR, SRC_ATTRIBUTE_NUMBER or SRC_ATTRIBUTE_DATE family from the confirmed value type and supported target contract, not its name. For line DFF/flex targets, choose the next numeric slot in that datatype family that is not currently present in the Service Mapping output attributes, then propose `RMCSInterface.insert` for `DOCUMENT_LINE` rather than a `RmcsDocLines.SrcAttribute*` assignment. Timestamp compatibility or other conversion is a separate decision under the [conversion policy](ora_groovy_function_guidance.md#date-and-timestamp-value-handling). Do not infer that an extension family, column or context exists from a numbered example. Sublines cannot use this extension/insert path.
6. Explain each candidate's source/target compatibility, permitted nulls, length/capacity, character-versus-byte limits where documented, numeric precision/scale, date/timestamp semantics and any unresolved conversion limitation. Do not silently truncate, round, stringify or cast a value to make it fit. Inspect current mapping and retained algorithm usage for occupied fields or conflicting context use, but treat that inspection as collision evidence only: absence from the exports does not prove a deployed slot is free. Obtain the actual deployed context/segment, supported capacity and unused/approved slot from the implementer. Never present the first unused number, the next number after the highest used one or an AR reservation heuristic as confirmed evidence; preserve documented seeded uses and reservations.
7. Present the named target candidate, business rationale, evidence and remaining deployment/context decisions in the [final traceability and configuration handoff](ora_use_case_resolution.md#final-traceability-and-configuration-handoff). Require acceptance of the exact target and applicable deployed context/slot before dependent final Groovy. An exact target already supplied by the implementer records intent without a redundant choice question, but its physical support, access and context still need evidence. A missing prerequisite returns to the primary for the precise corrective action rather than an assumed implementation.

Keep source ownership, target business meaning and runtime binding as separate decisions. A confirmed source does not select a target, and a target table column does not prove Service Mapping exposure. The source record and final operation matrix retain their linked canonical owners; do not duplicate either schema in this guide. Resume the primary with accepted decisions and unresolved prerequisites, and keep [approval](ora_algorithm_xml_guidance.md#approval-and-local-artifact) separate from a recommendation.

### Assumption-backed flex/DFF slot suggestion

When the implementer explicitly asks to proceed on assumptions and the requirement names a DFF or flex target without an exact slot, the primary may suggest the next numbered slot only as a conditional assumption. This is a recommendation for review, not proof that the slot is deployed, enabled, unused or safe in Fusion.

Apply this rule per selected algorithm step and target family:

- Step 1 / header writes to `VRM_SOURCE_DOCUMENTS` through `RmcsDoc` or header `RMCSInterface.insert`. Header slots are independent of line slots.
- Step 2 / line writes to `VRM_SOURCE_DOC_LINES` through line `RMCSInterface.insert` for new DFF/flex slots. Direct `RmcsDocLines.SrcAttribute*` assignment is allowed only when the implementer explicitly asks to modify that exact exposed mapped slot. Line slots are independent of header slots.
- Do not compare, reserve or increment slot numbers across Step 1 and Step 2. The same numeric suffix can exist in both target families without representing the same DFF/flex value.
- Do not apply this rule to sublines. Subline `SRC_ATTRIBUTE_*` groups are not customer flex/DFF slots for this skill; subline logic must use an existing writable `RmcsDocSublines` output attribute in the selected subline action.

If the selected step's active Groovy already writes the customer-requested flex/DFF slot, inspect only that step/action expression and suggest the next numeric slot in the same datatype family. For line DFF/flex, also inspect the current Service Mapping output attributes and skip any `RmcsDocLines.SrcAttribute*` slot already present there unless the implementer explicitly asks to modify it. For example, if `RmcsDocLines.SrcAttributeChar1` and `RmcsDocLines.SrcAttributeChar2` are already present in Service Mapping and no exact-slot modification is requested, suggest `SRC_ATTRIBUTE_CHAR3` for a new string line DFF and implement it through `RMCSInterface.insert` with `TransactionType:'DOCUMENT_LINE'` and `SourceId:RmcsDocLines.DocumentLineId`. A second string header insert after `SRC_ATTRIBUTE_CHAR1` can be suggested as `SRC_ATTRIBUTE_CHAR2`. For numeric or date values, use `SRC_ATTRIBUTE_NUMBERn` or `SRC_ATTRIBUTE_DATEn` only after the Service Mapping companion returns compatible datatype evidence from current mapping, describe metadata or an explicitly accepted named assumption.

The proposal and final handoff must label each incremented slot as `assumption-backed`, identify whether the increment came from active Groovy, Service Mapping output occupancy or both, identify the datatype family used for the recommendation, and instruct the implementer to confirm the deployed DFF/flex context, segment, capacity and unused status before import or runtime testing. For line DFF/flex slots, the handoff must say that existing mapped `RmcsDocLines.SrcAttribute*` columns were intentionally not direct-assigned unless an exact-slot modification was requested.
