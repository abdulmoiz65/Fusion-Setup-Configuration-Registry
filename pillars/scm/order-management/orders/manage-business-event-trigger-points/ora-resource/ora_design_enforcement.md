# Manage Business Event Trigger Points Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Resolve event code | Match the supplied event meaning exactly through the documented lookup-code endpoint and map the returned lookup code to EventCode. |
| 2 | Resolve Order Header Status Update event criteria | When a status value is supplied for Order Header Status Update, match it exactly to Display Name and map the returned Event Criteria Id to EventCriteriaId. |
| 2a | Resolve Order Attribute Update event criteria | When `ORDER_ATTRIBUTE_UPDATE` includes triggering attributes, match each supplied attribute exactly to AttributeName through `eventOrderAttributesLOV`, map the returned Event Criteria Id, and prepare a separate attribute row per match. |
| 2b | Resolve existing Order Attribute Update attributes | Before an add, removal, or re-add, retrieve configured attribute rows and compare each requested EventCriteriaId. Create a row for an unambiguously missing attribute; retain-and-disable matching rows for removal; re-enable each matching disabled row; report each matching enabled row as a duplicate. |
| 3 | Resolve explicit event action | For an explicit parent-event enable request, retrieve the `LookupCode` for the requested event name, query `/fscmRestApi/resources/11.13.18.05/omBusinessEventDetails?q=LookupCode='<resolved LookupCode>'`, match its returned LookupCode exactly, and map EventDetailId -1 to ConfigurationAction create with a blank parent-event source EventDetailId; otherwise map it to update with the returned EventDetailId. |
| 4 | Set fixed event criteria | Set EventCriteriaId to -1 for `CANCEL_BACKORDERS`, `CHANGE_COMP_COMPLETE`, `FULFILL_LINE_CLOSE`, `FLINE_STATUS_UPDATE`, `HOLD`, `RELEASE_HOLD`, and `SPLIT`. |
| 5 | Set event-enabled flag | Map an explicit parent-event activate or inactivate intent to the EventEnabledFlag of the `ORDER_ATTRIBUTE_UPDATE` row with EventCriteriaId -1; never infer that parent-row flag from attribute activity. Set EventEnabledFlag true on a new or re-added disabled separate `ORDER_ATTRIBUTE_UPDATE` attribute row. |
| 6 | Select setup-data business object | Use `connectors` whenever a connector or service is specified; otherwise use `eventDetails` for event-detail setup data. |
| 7 | Confirm Data Loader design contract | Confirm the selected `eventDetails` or `connectors` REST Data Loader business object through live metadata, then use the `core/data-loader` file-to-ZIP REST contract for upload, `initiateDataLoad`, approval, and status verification. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A request changes business event trigger-point configuration | Critical | resolve_event_code_by_meaning | The supplied event meaning has no unique exact lookup-code match. | Correct the event meaning and rerun validation. | Yes |
| An activation request has resolved the LookupCode for the requested event name | Critical | resolve_existing_business_event_detail_for_activation | No unique omBusinessEventDetails record has LookupCode exactly matching that LookupCode, so EventDetailId and ConfigurationAction cannot be derived. | Correct the event identity or source data and rerun validation. | Yes |
| An Order Header Status Update request includes a status value | Critical | resolve_order_status_update_event_criteria_id | The supplied status value has no unique exact Display Name match. | Correct the status value and rerun validation. | Yes |
| An `ORDER_ATTRIBUTE_UPDATE` request includes one or more triggering attributes | Critical | resolve_order_attribute_update_event_criteria | A supplied attribute has no unique exact AttributeName match from `eventOrderAttributesLOV`. | Correct the attribute name and rerun validation. | Yes |
| An explicit `ORDER_ATTRIBUTE_UPDATE` parent-event action is requested | Critical | resolve_order_attribute_update_event_enabled_flag | The parent-event row does not have EventCriteriaId -1 or does not use the explicit intent. | Prepare a separate parent-event row and apply the explicit intent only to that row. | Yes |
| An `ORDER_ATTRIBUTE_UPDATE` add or re-add request includes one or more triggering attributes | Critical | resolve_order_attribute_update_event_enabled_flag | A missing attribute row is not created with EventEnabledFlag true, a re-added disabled row does not have EventEnabledFlag true, or an already-enabled row is included in the import source. | Create missing rows and set EventEnabledFlag true only for new or disabled rows; report an enabled row as duplicate and omit it from the source. | Yes |
| An `ORDER_ATTRIBUTE_UPDATE` add, removal, or re-add request includes attributes | Critical | resolve_existing_order_attribute_update_attributes | The configured attribute response is incomplete or ambiguous. | Stop and retrieve a complete, unambiguous configured attribute-row set; do not infer missing, removal, re-enable, or duplicate behavior. | Yes |
| A request specifies a connector or service | Critical | resolve_setup_data_business_object | The source is not routed to `connectors`. | Select the registered REST Data Loader `connectors` business object before source preparation. | Yes |
| A request changes business event trigger-point configuration | Critical | validate_data_loader_contract | The live metadata does not confirm the selected `eventDetails` or `connectors` REST Data Loader object and its DAT attributes. | Refresh the BO metadata and resolve the mismatch before source preparation. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_event_code_by_meaning | Before any activation or inactivation configuration preview | Exact matched meaning and returned lookup code mapped to EventCode | ora_reference_lookups.md |
| resolve_existing_business_event_detail_for_activation | Before any activation configuration preview | Exact LookupCode filter and match, EventDetailId, and derived ConfigurationAction | ora_reference_lookups.md |
| resolve_order_status_update_event_criteria_id | Before any Order Header Status Update configuration preview that includes a status value | Exact matched Display Name and returned Event Criteria Id mapped to EventCriteriaId | ora_reference_lookups.md |
| resolve_order_attribute_update_event_criteria | Before any `ORDER_ATTRIBUTE_UPDATE` configuration preview that includes triggering attributes | Every exact matched AttributeName and returned Event Criteria Id | ora_reference_lookups.md |
| resolve_existing_order_attribute_update_attributes | Before any `ORDER_ATTRIBUTE_UPDATE` removal or re-add preview | Exact configured EventCriteriaId set and EventEnabledFlag for every matched attribute row | ora_reference_lookups.md |
| resolve_order_attribute_update_event_enabled_flag | Before an `ORDER_ATTRIBUTE_UPDATE` attribute or explicit parent-event row is prepared | Per-row EventEnabledFlag action; explicit parent-event intent for EventCriteriaId -1 | ora_reference_lookups.md |
| resolve_setup_data_business_object | Before source preparation when a connector or service is specified | `connectors` business object selection | ora_input_validation.md |
| validate_data_loader_contract | Before source preparation and submission | Registered selected `eventDetails` or `connectors` metadata, immutable DAT/ZIP source, UCM upload contract, `initiateDataLoad` payload, approval, and status verification | core/data-loader/SKILL.md and references/fusion-zip-rest.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BUSINESS_EVENT_TRIGGER_POINTS.RESOLVE_SETUP_DATA_BUSINESS_OBJECT | step | 45 | design_enforcement | connectors-selected->BUSINESS_EVENT_TRIGGER_POINTS.ENFORCE_CONTRACT;event-details-selected->BUSINESS_EVENT_TRIGGER_POINTS.ENFORCE_CONTRACT | BUSINESS_EVENT_TRIGGER_POINTS.APPLY_EVENT_ENABLED_FLAG | stop | Before source preparation: select `connectors` when a connector or service is specified; otherwise select `eventDetails`. |
| BUSINESS_EVENT_TRIGGER_POINTS.ENFORCE_CONTRACT | step | 50 | design_enforcement | contract-ready->RETURN_SUCCESS;metadata-mismatch->RETURN_ISSUES | BUSINESS_EVENT_TRIGGER_POINTS.RESOLVE_SETUP_DATA_BUSINESS_OBJECT | stop | Before source preparation or configuration-changing Fusion operation for this task |
