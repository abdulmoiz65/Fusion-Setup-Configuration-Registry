# Intersubinventory Parameters Input Validation

## Source Evidence

| Source | Used For |
|---|---|
| Redwood `intersubinventory-parameters/pages/manage-page-chains/createInterSubinventoryParametersChain.js` | Create payload shaping, exact `All` source-subinventory sentinel, transient-field removal, UI-side DFF shaping, and conditional omission of `ManualReceiptExpenseFlag` |
| Redwood `intersubinventory-parameters/pages/manage-page-chains/saveInterSubinventoryParametersChain.js` | Update payload shaping, transient-field removal, UI-side DFF shaping, and changed-field filtering |
| Redwood `dynamicLayouts/self/interSubinventoryParameters/layout.html` and `layout.json` | UI controls, required fields, DFF presentation, model fields, and conditional enablement |
| Redwood `FormDestTypeChangeChain.js`, `FormTransferTypeChangeChain.js`, `FormReceiptRoutingChangeEventChain.js`, and `FormFromSubinventoryChangeChain.js` | Conditional relationships and mutually incompatible values |
| Redwood `onEditSubinventoryParameter.js` and `manage-page.json` | Transient checkbox-array behavior and canonical Boolean model type |
| Redwood `vbEnterListener.js` and date templates | Start-date lower bound and end-date relationship |
| Live Data Loader metadata for `interSubinventoryParameters` | BO visibility, canonical REST/Data Loader root attributes, and `DFF` child attributes `interSubParametersName` and `__FLEX_Context`; backend-required and key enforcement remains owned by Data Loader and Fusion |
| Fusion Data Loader failure diagnostic for `StartDate` | REST/Data Loader requires date values in exact `YYYY-MM-DD` form and rejects slash-separated output |
| Live FSM template for `ORA_INTERSUBINVENTORY_PARAMETERS` and `ORA_INV_INTERSUB_PARAMETER` | FSM physical column names and column types |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| BO-owned organization and subinventory references | Preserve `OrganizationCode`, `OrganizationId`, `FromSubinventory`, and `ToSubinventory`; do not perform task-local REST resolution | Any organization or subinventory value is supplied |  |
| Source subinventory `All` sentinel | Normalize only exact case-sensitive `All` to blank `FromSubinventory`; reject other wildcard spellings unless separately approved | `FromSubinventory` is supplied as exact `All` |  |
| Destination Type representation | Accept code under `DestinationTypeCode`, meaning under `DestinationType`, or both; require one exact row and normalize for the selected route | Destination type is supplied | resolve_intersub_destination_type |
| Transfer Type representation | Accept code under `TransferTypeCode`, meaning under `TransferType`, or both; require one exact row and normalize for the selected route | Transfer type is supplied | resolve_intersub_transfer_type |
| Receipt Routing representation | Accept code under `ReceiptRoutingCode`, meaning under `ReceiptRouting`, or both; require one exact row and normalize for the selected route | Receipt routing is supplied | resolve_intersub_receipt_routing |
| Conflicting lookup representations | When code and meaning are both supplied for an approved lookup, require both to resolve to the same row | Both representations are supplied |  |
| Common create fields | Require an organization reference, destination type, source subinventory input, and start date after approved defaults | Create operation |  |
| Inventory destination fields | Require destination subinventory and transfer type; omit `ManualReceiptExpenseFlag` | Effective destination type is `INVENTORY` |  |
| Expense destination fields | Reject destination subinventory or transfer type; preserve canonical Boolean `ManualReceiptExpenseFlag` | Effective destination type is `EXPENSE` |  |
| Receipt routing condition | Require routing except for inventory transfer code `1` or expense `ManualReceiptExpenseFlag=false`; reject routing when an exception applies | Destination type, transfer type, and receipt-required values are effective |  |
| Distinct subinventories | Require nonblank source and destination subinventories to differ | Both values are effective |  |
| Date representation | Accept exact `YYYY-MM-DD`; also accept exact `YYYY/MM/DD` and normalize `/` to `-` before REST/Data Loader handoff. Preserve blank `EndDate`. Reject ambiguous ordering, timestamps, and invalid calendar dates | `StartDate` or nonblank `EndDate` is supplied |  |
| Date relationship | Require create `StartDate` not to precede current date; require `EndDate` not to precede effective `StartDate` | Create after defaulting, or any operation supplying both effective dates |  |
| Boolean representation | Preserve canonical Boolean `true` or `false`; do not infer text aliases from transient `checkboxArr` | `ManualReceiptExpenseFlag` is supplied |  |
| DFF child representation | For the REST/Data Loader route, accept `DFF` only as an array of child objects containing `interSubParametersName` and optional `__FLEX_Context`; preserve blank or null context for global data elements. Reject unknown DFF fields, flattened root segments, or DFF input on the FSM route | Any DFF context or segment input is supplied |  |

## Control and Route Normalization Inventory

| UI Label and Control | Implementation Field | Scope | UI Model Value and Type | Accepted Friendly Input | REST/Data Loader Physical Output | FSM Physical Output | Source Evidence | Conditions and Conflicts | Disposition |
|---|---|---|---|---|---|---|---|---|---|
| Organization; create LOV and update read-only text | `OrganizationId`, `OrganizationCode` | Root row | Create selection stores organization ID; edit displays code | BO-supported `OrganizationCode` or `OrganizationId`; no task-local aliases | Preserve `OrganizationCode` and/or `OrganizationId` for BO-owned resolution | `OrganizationCode` string | Redwood `organizationTemplate`; BO metadata; FSM template | Required for create; read-only in Redwood edit | Backend-owned reference with route-aware field selection |
| Destination Type; LOV/select | `DestinationType`, `DestinationTypeCode` | Root row | Meaning displayed; code string selected | Meaning under `DestinationType`; code under `DestinationTypeCode`; both only when consistent | `DestinationTypeCode` equals returned `LookupCode`; omit display-only meaning | `DestinationType` equals returned `LookupCode` | Redwood `destinationTypeTemplate`; create payload; FSM template | Expense destination is read-only on edit and excludes destination subinventory and transfer type | Route-aware normalization through `resolve_intersub_destination_type` |
| Source Subinventory; LOV/select or read-only text | `FromSubinventory` | Root row | Code/name string; exact UI sentinel `All` | BO-supported code, or exact case-sensitive `All`; no other wildcard aliases | Preserve code; exact `All` becomes blank `FromSubinventory` | Preserve code; exact `All` becomes blank `FromSubinventory` | Redwood source template and create payload; FSM template | Must differ from nonblank destination; read-only on edit | BO-owned reference plus sourced sentinel normalization |
| Destination Subinventory; conditional LOV/select or read-only text | `ToSubinventory` | Root row | Code/name string | BO-supported code; no task-local aliases | `ToSubinventory` string | `ToSubinventory` string | Redwood destination template; FSM template | Required for inventory; blank for expense; must differ from source; read-only on edit | Backend-owned reference with route-aware field selection |
| Transfer Type; LOV/select | `TransferType`, `TransferTypeCode` | Root row | Meaning displayed; code string selected | Meaning under `TransferType`; code under `TransferTypeCode`; both only when consistent | `TransferTypeCode` equals returned `LookupCode`; omit display-only meaning | `TransferType` equals returned `LookupCode` | Redwood transfer template; create payload; FSM template | Required for inventory; absent for expense; code `1` makes routing inapplicable | Route-aware normalization through `resolve_intersub_transfer_type` |
| Receipt Routing; conditional LOV/select | `ReceiptRouting`, `ReceiptRoutingCode` | Root row | Meaning displayed; code string selected | Meaning under `ReceiptRouting`; code under `ReceiptRoutingCode`; both only when consistent | `ReceiptRoutingCode` equals returned `LookupCode`; omit display-only meaning | `ReceiptRouting` equals returned `LookupCode` | Redwood routing template; create payload; FSM template | Required unless inventory transfer code is `1` or expense receipt-required flag is false; reject conflicting routing | Route-aware normalization through `resolve_intersub_receipt_routing` |
| Receipt Required; checkbox | `ManualReceiptExpenseFlag`; transient `checkboxArr` | Root row | Canonical Boolean plus transient string array containing `Y` when checked | Canonical Boolean under `ManualReceiptExpenseFlag` only; no text aliases approved | Boolean `true` or `false`; omit for inventory; never emit `checkboxArr` | `ManualReceiptExpense` string `Y` or `N`; blank for inventory | Redwood checkbox template, change/edit chains, and payload shaping; FSM template and same-field FSM Boolean convention | Applies to expense; false makes routing inapplicable; transient array is presentation-only | Route-aware Boolean serialization; `checkboxArr` is presentation-only |
| Start Date; date input | `StartDate` | Root row | ISO date string | Exact `YYYY-MM-DD` or exact `YYYY/MM/DD`; normalize slash-separated input to `YYYY-MM-DD` | `StartDate` exact `YYYY-MM-DD` string | `StartDate` date column using the selected FSM serializer | Redwood add-new chain, enter listener, and date template; Fusion Data Loader date-format diagnostic; FSM template | Required on create; defaults to current date; create value cannot precede current date; no create default on update; reject ambiguous or invalid dates | Default plus route-aware canonical date normalization |
| End Date; date input | `EndDate` | Root row | Optional ISO date string | Blank, exact `YYYY-MM-DD`, or exact `YYYY/MM/DD`; normalize slash-separated input to `YYYY-MM-DD` | `EndDate` exact `YYYY-MM-DD` string or blank | `EndDate` date column or blank using the selected FSM serializer | Redwood end-date template; Fusion Data Loader date-format diagnostic; FSM template | Cannot precede effective `StartDate`; reject ambiguous or invalid dates | Route-aware optional date normalization |
| Descriptive Flexfields; dynamic form | `DFF`, `interSubParametersName`, and `__FLEX_Context` | `DFF` child | Redwood presents a structured context and segment object | REST/Data Loader route: `DFF` array with `interSubParametersName` and optional `__FLEX_Context`; blank or null context means global data elements | Emit child section `DFF`; preserve `interSubParametersName`; preserve blank or null `__FLEX_Context` for the global context | Not supported by the current FSM contract; reject DFF input when FSM is selected | Redwood DFF layout and load/create/update chains; live Data Loader metadata exposing section `DFF`, segment `interSubParametersName(INV_INTERSUB_PARAMETERS=Global Data Elements)`, and context `__FLEX_Context(INV_INTERSUB_PARAMETERS=Global Data Elements)` | Do not flatten into the root row, infer another context, accept unknown segments, or send the child through FSM | Route-aware structured child for REST/Data Loader; unsupported for FSM |
| Update change filter; client-side transformation | Prepared update payload | Root row and supported `DFF` child | Updated record compared with fetched record | Not applicable | Emit only changed supported root fields and supported DFF child values; omit request when nothing changed | FSM update remains a validated route row using supported FSM physical columns and does not accept DFF input | Redwood `preparePatchPayload` | Create-only defaults must not be injected into update; DFF remains route-specific | Route-aware update transformation for supported fields |

## Validation Boundary

- Reject conflicting conditional values instead of silently deleting user input.
- Do not duplicate BO, Data Loader, or Fusion uniqueness, length, domain, key, or server-side validation.
- Do not add local resolvers for organization or subinventory fields.
- Preserve blanks unless an approved default or exact sourced `All` sentinel applies.
- Normalize only exact `YYYY/MM/DD` date input to `YYYY-MM-DD`; do not infer ambiguous date order or truncate timestamps.
- Select REST/Data Loader versus FSM output only from the workflow-selected route; never infer the route from user-supplied field names.
- Do not expose transient `checkboxArr` or display-only meaning fields in REST/Data Loader output.
- Accept the verified structured `DFF` child only for REST/Data Loader. Reject flattened DFF fields, unknown contexts or segments, and any DFF input on the FSM route.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ISP.VALIDATE_INPUT | step | 10 | validate_input | valid->ISP.CHECK_READINESS;invalid->ISP.HANDLE_ERROR | none | stop | Before read-only lookup resolution; validate semantic input, route selection, BO-owned references, exact `All` sentinel, Boolean input, and route-aware structured DFF child input |
| ISP.VALIDATE_EFFECTIVE_VALUES | step | 70 | validate_input | valid->ISP.DATA_LOADER_HANDOFF;invalid->ISP.HANDLE_ERROR | ISP.APPLY_DEFAULTS | stop | After approved lookups and defaults; enforce sourced UI conditional/date behavior and selected-route physical output |
