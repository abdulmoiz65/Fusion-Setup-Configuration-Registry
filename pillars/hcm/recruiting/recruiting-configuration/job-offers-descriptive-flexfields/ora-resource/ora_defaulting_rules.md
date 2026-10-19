# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Omitted exported attribute | Preserve the current exported value | Update request omits the attribute | No | resolve_dff_export_model |
| Import mode | FSM | The exact task catalog entry confirms CSV export/import support | No | |
| Deployment route | Manual intervention | No supported automated Deploy Flexfield route is proven | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IRC_OFFER_DFF.APPLY_DEFAULTS | step | 50 | apply_default | preserved->IRC_OFFER_DFF.ENFORCE_DESIGN;blocked->IRC_OFFER_DFF.HANDLE_ISSUE | IRC_OFFER_DFF.CHECK_DEPENDENCIES | stop | A validated Create or Update change is prepared |

## New context-sensitive character segment defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Name, Prompt and ShortPrompt | Requested segment Name | New context-sensitive segment | No | |
| DisplayType, DisplayWidth, DisplayHeight | Verified compatible peer presentation | New segment with omitted presentation values | No | resolve_dff_export_model |
| EnabledFlag, RequiredFlag, ReadOnlyFlag | Y, N, N from the verified enabled optional editable peer | New segment without explicit flag changes | No | resolve_dff_export_model |
| BIEnabledFlag, IndexedFlag, MultirowUniqueKeyFlag, ShowValueDescription | Verified compatible peer values | New segment with omitted flags | No | resolve_dff_export_model |
| DefaultType, DefaultValue, DefaultValueNumber, DefaultValueDate, DefaultValueTimestamp | Blank | New segment without a requested default | No | |
| CreationDate, CreatedBy, LastUpdateDate, LastUpdatedBy, LastUpdateLogin | Blank; Fusion supplies audit values | New segment only | No | |

Disclose SegmentIdentifier and all presentation defaults in the preview. Do not
copy Description, help text, checkbox values, RangeType, DerivationValue,
BIEqualizationTag or UomClassCode from a peer; leave unrequested nullable fields
blank. Apply any explicit additional change only after its own contract is resolved.
These new-row rules never clear fields on an existing segment.
