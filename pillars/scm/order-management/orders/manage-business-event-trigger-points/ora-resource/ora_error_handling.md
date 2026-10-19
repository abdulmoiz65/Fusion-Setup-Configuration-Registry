# Manage Business Event Trigger Points Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| The business event trigger-point detail lookup fails or returns an incomplete response | Stop before reporting configuration state. Preserve sanitized diagnostics and do not retry automatically. |
| The event meaning has no unique exact lookup-code match | Stop before deriving EventCode or EventEnabledFlag. Request a corrected event meaning. |
| The explicit parent-event enable lookup using `q=LookupCode` returns no exact LookupCode match | Stop before deriving the parent-event EventDetailId or ConfigurationAction. Request corrected event identity or source data. |
| An `ORDER_ATTRIBUTE_UPDATE` parent-event row with EventCriteriaId -1 is requested without a valid explicit enablement or inactivation intent, or attribute activity would alter that row | Stop before preparing or altering the parent-event row. Request an explicit activate or inactivate intent. |
| The Order Header Status Update status value has no unique exact Display Name match | Stop before deriving EventCriteriaId. Request a corrected status value. |
| An Order Attribute Update trigger attribute has no unique exact AttributeName match from `eventOrderAttributesLOV` | Stop before deriving EventCriteriaId. Request a corrected attribute name. |
| Configured Order Attribute Update attribute rows are incomplete or ambiguous for an add, removal, or re-add | Stop before preparing a create, disable, re-enable, or duplicate result. An unambiguous missing row is a create action. |
| Live `eventDetails` metadata cannot confirm a registered REST Data Loader object or required attributes | Stop before source preparation, refresh metadata, and resolve the contract mismatch |
| A connector or service is specified but the source is not routed to `connectors` | Stop before source preparation and select the registered `connectors` REST Data Loader business object |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Reference lookup failure | The configured business event trigger-point detail endpoint cannot return a usable response | Report the failed read-only lookup stage and obtain corrected endpoint or access guidance. |
| Invalid event meaning | The supplied meaning has no unique exact lookup-code match | Provide a corrected event meaning. |
| Invalid explicit parent-event detail | The omBusinessEventDetails lookup using `q=LookupCode` returns no unique exact LookupCode match | Provide a corrected event identity or source data. |
| Invalid explicit parent-event intent | An `ORDER_ATTRIBUTE_UPDATE` EventCriteriaId -1 row has no valid explicit activate or inactivate intent, or an attribute operation would alter it | Provide a valid explicit parent-event intent and keep the parent row separate from attribute rows. |
| Invalid Order Header Status Update status value | The supplied status value has no unique exact Display Name match | Provide a corrected status value. |
| Invalid Order Attribute Update trigger attribute | A supplied trigger attribute has no unique exact AttributeName match from `eventOrderAttributesLOV` | Provide a corrected attribute name. |
| Invalid existing Order Attribute Update attribute rows | An add, removal, or re-add cannot establish unambiguous configured EventCriteriaId and flag values | Refresh the authoritative configured details and correct the requested attribute set. |
| Data Loader contract mismatch | Live metadata does not confirm the selected `eventDetails` or `connectors` Data Loader source contract, or a connector/service source is not routed to `connectors` | Refresh the selected BO metadata and correct the source before revalidating. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Detail lookup | The documented read-only endpoint, whether details were returned, and any sanitized lookup failure. |
| Contract check | That the task uses the registered `eventDetails` Data Loader source contract and that the Data Loader approval workflow controls any submission |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| The live `eventDetails` metadata is missing or inconsistent | Infer a direct REST payload, prepare an import, or attempt a configuration-changing Fusion operation |
| A detail lookup is requested | Treat the read-only lookup as authorization to create, update, enable, disable, or import configuration. |
| An add, removal, or re-add request cannot resolve configured attribute rows unambiguously | Delete attribute rows, infer their state, report a duplicate, create an attribute row, or alter the EventCriteriaId -1 parent row. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RETURN_SUCCESS | terminal | 60 | terminal | none | BUSINESS_EVENT_TRIGGER_POINTS.GET_DETAILS | continue | The requested business event trigger-point details were retrieved through the documented read-only lookup. |
| RETURN_DUPLICATE | terminal | 65 | terminal | none | BUSINESS_EVENT_TRIGGER_POINTS.RESOLVE_EXISTING_ORDER_ATTRIBUTE_UPDATE_ATTRIBUTES | continue | The exact requested `ORDER_ATTRIBUTE_UPDATE` attribute set is already enabled; no import source was prepared. |
| RETURN_ISSUES | terminal | 70 | terminal | none | none | continue | A lookup, validation, defaulting, or configuration-contract gate blocked progress. |
