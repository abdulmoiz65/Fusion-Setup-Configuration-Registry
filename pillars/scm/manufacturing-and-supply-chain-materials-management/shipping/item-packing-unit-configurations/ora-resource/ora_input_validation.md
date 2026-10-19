# Item Packing Unit Configurations Input Validation

Source: approved Default-field contract, Redwood Packing Unit Configuration page, and live Data Loader metadata for configureDefaultPackingUnits.

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Default friendly-value normalization | For REST/Data Loader, accept Default as Yes, yes, Y, y, True, or true and emit DefaultFlag as the string true. Accept No, no, N, n, Flase, or false and emit DefaultFlag as the string false. For FSM, emit PreferredFlag as Y or N respectively. | Default is supplied | |
| FSM PreferredFlag representation | Preserve a blank PreferredFlag in an FSM source row. When PreferredFlag is populated directly in an FSM source, accept only Y or N. | FSM import is explicitly selected | |
| LPN route mapping | Accept LPN as the user-facing packing-unit input. For REST/Data Loader, populate PackingUnitItemNumber. For FSM, populate ContainerItemNumber. Do not resolve the supplied LPN to an ID locally. | LPN is supplied | |
| FSM-to-REST field names | Treat ContainerItemNumber as the FSM representation of PackingUnitItemNumber and MaxLoadQuantity as the FSM representation of MaximumQuantity. OrganizationCode and ItemNumber use the same names on both routes. | FSM import is explicitly selected | |
| Backend-owned attributes | Do not locally resolve Item, Packing Unit, Organization, Maximum Quantity, RestAction, audit attributes, IDs, or DFF values. Treat FSM AttributeCategory, Attribute1 through Attribute15, AttributeDate1 through AttributeDate5, AttributeNumber1 through AttributeNumber10, AttributeTimestamp1 through AttributeTimestamp5, JobDefinitionName, JobDefinitionPackage, and ObjectVersionNumber as export-template-owned fields. Current Data Loader metadata and Fusion own their lookup, required-value, datatype, and server-side validation behavior. | Any of these attributes is absent or supplied | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IPUC.VALIDATE_DEFAULT | decision | 10 | validate_input | valid->IPUC.APPLY_DEFAULT;invalid->IPUC.HANDLE_ISSUE | none | stop | Item Packing Unit Configurations input is prepared for Data Loader handoff |
