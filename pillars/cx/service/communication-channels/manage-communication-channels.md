---
task_code: "ORA_SVC_MANAGE_COMM_CHANNELS"
task_name: "Manage Communication Channels"
parent_skill_id: "cx.service.communication-channels"
pillar: "CX"
offering: "Service"
functional_area: "Communication Channels"
functional_area_code: "ORA_SVC_COMM_CHANNELS"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Communication Channels

## Setup Task Metadata

- Task name: `Manage Communication Channels`
- Task code: `ORA_SVC_MANAGE_COMM_CHANNELS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``


## FSM Contract

### ORA_SVC_SERVICE_CHANNEL_COMMUNICATION

- `ChannelShortName`: Retain the exact exported channel short name for an existing channel. For an approved new channel, generate it from AccountName by converting the user-friendly account name to uppercase and removing spaces. Verify that the generated value is unique in the same-task export before preparing the package.
- `ChannelTypeCd`: Retain the exported channel type for an existing channel. For a new or changed channel, use the Common skill to pull and validate the ORA_SVC_CHANNEL_TYPE_CD lookup, then use the approved lookup code; do not infer a channel type from the display name, account name, or endpoint.
- `NetworkTypeCd`: Retain the exported value. When it is blank in the same-task export, keep it blank; do not infer or populate a network type.
- `AccountName`: Retain the exported account name for an existing channel. For a new channel, use the approved account name; do not derive it from the display name or channel short name.
- `DisplayName`: Retain the exported value unless an approved display-name change targets the channel. For an approved new channel, when DisplayName is not provided, default it to AccountName.
- `PrivatePToPAllowedFlag`: Retain the exported value unless an approved channel policy change targets it. For an approved new channel, default to Y.
- `OriginalSystemReference`: Retain the exported value for an existing channel. For an approved new channel, default to blank unless it is explicitly required by the same-task export or approved source-system design.
- `EnabledFlag`: Retain the exported value unless an approved active-state change targets the channel. For an approved new channel, default to Y.
- `CreatedBy`: Treat as export-derived audit data. Do not supply or alter it for a new or updated channel unless the same-task package contract explicitly requires it.
- `LastUpdatedBy`: Treat as export-derived audit data. Do not supply or alter it for a new or updated channel unless the same-task package contract explicitly requires it.
- `LastUpdateLogin`: Treat as export-derived audit data. Do not supply or alter it for a new or updated channel unless the same-task package contract explicitly requires it.
- `EndPoint`: Retain the exported value unless an approved endpoint change targets the channel. For an approved new channel, default to blank; do not infer an endpoint from the channel type.
- `Port`: Retain the exported value unless an approved endpoint change targets the channel. For an approved new channel, default to blank; do not infer a port.
- `APIVersion`: Retain the exported value unless an approved integration change targets it. For an approved new channel, default to blank.
- `APIId`: Retain the exported value only when it is non-sensitive and explicitly approved for the package. For an approved new channel, default to blank; do not infer an API identifier.
- `APIPassword`: Do not place a password or other secret in the FSM package. Retain a blank exported value and default to blank for a new channel; obtain and configure secrets only through the approved secure administration path.
- `AuthenticationURL`: Retain the exported value unless an approved integration change targets it. For an approved new channel, default to blank.
- `AuthorizationURL`: Retain the exported value unless an approved integration change targets it. For an approved new channel, default to blank.
- `TokenRequestURL`: Retain the exported value unless an approved integration change targets it. For an approved new channel, default to blank.
- `TokenAccessURL`: Retain the exported value unless an approved integration change targets it. For an approved new channel, default to blank.
- `AccessToken`: Do not place an access token or other secret in the FSM package. Retain a blank exported value and default to blank for a new channel.
- `RefreshToken`: Do not place a refresh token or other secret in the FSM package. Retain a blank exported value and default to blank for a new channel.
- `AuthToken`: Do not place an authentication token or other secret in the FSM package. Retain a blank exported value and default to blank for a new channel.
- `OpenSrCount`: Retain the exported value unless an approved channel behavior change targets it. For an approved new channel, default to blank.
- `ChannelTypeCdLovSwitcher`: Retain the exact exported list-of-values switcher. When it is not provided, leave it blank; do not generate or substitute it.
- `StripeCd`: Retain the exact exported stripe code for an existing channel. For a new or changed channel, use the Common skill to pull and validate the ORA_SVC_STRIPE_CD lookup, then use the approved lookup code; do not infer or substitute a code.
- `BUOrgId`: Retain the exported business-unit organization ID for an existing channel. For a new or changed channel, use the Business Unit skill to pull the approved business-unit organization ID and use the exact ID required by the same-task export contract.
- `BusinessUnitName`: Retain the exported business-unit name for an existing channel. For a new channel, leave it blank.
- `BusinessUnitNameTransientForLOV`: Retain the exported value for an existing channel. For a new channel, leave it blank.
- `BusinessUnitIdFK`: Retain the exported business-unit foreign-key ID for an existing channel. For a new or changed channel, set it to the resolved BUOrgId value.
- `UpdateFlag`: Retain the exact exported package-control value. For an approved new channel, default to TRUE.
- `DeleteFlag`: Retain the exact exported package-control value. For an approved new channel, default to TRUE. Do not use it to delete a channel because deletion is unsupported by this FSM workflow.
- `CollabChannelCreateFlag`: Retain the exact exported package-control value. For an approved new Slack channel, set this Boolean to false; the current Fusion import path rejects a null value. For another new channel type, leave it blank only when the same-task export or documented contract supports omission; do not infer it from ChannelTypeCd.
- `ObjectAttributes`: Retain the exported value. For an approved new channel, default to blank. Do not create or substitute object attributes without same-task export evidence and approved scope.
- `PurposeCd`: Retain the exported purpose for an existing channel. For a new or changed channel, use the Common skill to pull and validate the ORA_SVC_CHANNEL_PURPOSE lookup, then use the approved lookup code.
- `CustomerTypeCd`: Retain the exported value unless an approved channel behavior change targets it. For an approved new channel, default to ORA_SVC_BOTH.
- `MultipleMatchesActionCd`: Retain the exported value unless an approved inbound matching-rule change targets it. For an approved new channel, default to ORA_SVC_NONE.
- `NoMatchActionCd`: Retain the exported value unless an approved inbound matching-rule change targets it. For an approved new channel, default to ORA_SVC_NO_ACTION.
- `IncludeSenderNameFlag`: Retain the exported value unless an approved sender-data handling change targets it. For an approved new channel, default to N.
- `IncludeSenderEmailFlag`: Retain the exported value unless an approved sender-data handling change targets it. For an approved new channel, default to N.
- `SourceCd`: Retain the exact exported source code. For an approved new channel, default to ORA_SVC_ADMIN_UI; do not infer or substitute it.
## Purpose

Manage Service communication channels, including their purpose, display name, and lifecycle.
## Use Cases

### View Communication Channels

View configured communication channels and their account name, display name, channel type, Stripe Code, purpose, active state, and creation date.

1. Read communication channels with core.fusion-api.rest-api-client using the Channels REST resource.
2. Return ChannelId, AccountName, DisplayName, ChannelTypeCd, StripeCd, PurposeCd, EnabledFlag, and CreationDate.

### View Active Communication Channels

View only active communication channels.

1. Read communication channels with core.fusion-api.rest-api-client using the Channels REST resource.
2. Filter the returned channels to EnabledFlag values that indicate active channels; do not infer active state from the display name or channel type.

### View Communication Channel

View a selected communication channel before changing or deleting it using exactly one of ChannelId, ChannelShortName, or DisplayName.

1. Read the selected communication channel with core.fusion-api.rest-api-client using ChannelId, or query the Channels collection for an exact ChannelShortName or DisplayName.
2. Require exactly one matching channel for a short-name or display-name query; stop and request a more specific selector when no channel or more than one channel matches.
3. Return ChannelId, AccountName, DisplayName, ChannelShortName, ChannelTypeCd, StripeCd, PurposeCd, and EnabledFlag.

### Create Communication Channel

Create a communication channel with its required identity, type, Stripe Code, purpose, and active-state settings.

1. Read communication channels with core.fusion-api.rest-api-client and stop if ChannelShortName already matches the requested Channel Code.
2. Confirm the required Stripe Code, Purpose, Channel Type, Account Name, and Channel Code; optionally provide Display Name and the requested initial active state.
3. Export communication-channel setup data with shared.setup-export.task-level-export.
4. Use the completed export of the same setup task as the package baseline; preserve its package structure and add only the approved communication-channel row.
5. Validate the FSM package with shared.validation.setup-data-validator.
6. Import the approved ZIP with core.data-loader.
7. Verify the new channel with a fresh Channels REST read.

### Update Communication Channel

Update a communication channel's editable purpose or display name.

1. Resolve the selected channel with core.fusion-api.rest-api-client using exactly one of ChannelId, ChannelShortName, or DisplayName; require exactly one match for a name selector.
2. Treat Stripe Code, Channel Type, Account Name, and Channel Code as read-only identity values in this workflow; stop if a change to one of them is requested.
3. Confirm the approved Purpose and/or Display Name change.
4. Export communication-channel setup data with shared.setup-export.task-level-export.
5. Use the completed export of the same setup task as the package baseline; retain the selected channel identity and modify only the approved editable fields.
6. Validate the FSM package with shared.validation.setup-data-validator.
7. Import the approved ZIP with core.data-loader.
8. Verify the updated channel with a fresh Channels REST read.

### Delete Communication Channel

Delete a communication channel.

Not supported. Channel deletion is not supported through this FSM workflow. The user interface displays the warning "The channel will be deleted. Do you want to continue?"; use the supported administration path outside this workflow when deletion is required.
## Guard Rails

1. Require an authenticated Fusion user context before any Fusion operation; use `core.auth.fusion-oauth-authentication`.
2. Do not use `core.fusion-api.rest-api-client` to create, update, or delete records.
3. Do not use `shared.setup-import.task-level-import` to create, update, or delete records.
## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Service`
- Functional area / Setup Object: `Communication Channels`
- Setup task name: `Manage Communication Channels`
- Setup task code: `ORA_SVC_MANAGE_COMM_CHANNELS`

## FSM Data Loader Package Requirements

1. Read the task's fsm_contract first when it is present. Treat its objects and field guidance as the task-specific starting point for classifying each requested change as an existing-root update, new root, existing-child update, new child of an existing parent, new relationship, or mixed package change.
2. Read `ASM_SETUP_CSV_METADATA.xml` in the task export package for business objects, XML paths, node sequence, attributes, scope, and relationships; reconcile it with the task's fsm_contract when one is present.
3. Use the fsm_contract object and field guidance together with metadata-defined node sequence and relationships to determine package order and required object coverage.
4. Verify the selected baseline or template package includes the members, file names, structure, headers, encoding, scope, relationship rows, and fsm_contract objects and fields required for the requested change.
5. Treat a completed export of this same setup task as authoritative evidence for package structure, headers, node order, key and linkage shape, and generated-identity handling. Use it to corroborate the fsm_contract and record provenance for copied template values.
6. For existing-row updates, retain exported identities and all unchanged values, parent rows, child rows, and relationships required by the fsm_contract and package evidence; do not carry unrelated baseline rows into the change package unless they are required for import integrity. Change only approved fields.
7. For a new child or relationship, retain the existing parent identity and use only linkage, keys, and required values specified by the fsm_contract or confirmed by same-task package evidence.
8. For greenfield rows, construct the create contract from the fsm_contract, task-specific documented requirements, `ASM_SETUP_CSV_METADATA.xml`, a completed export of this same task, and supported preview or dry-run results where available.
9. An export whose data CSV members contain only headers is valid structural evidence for a greenfield contract, not an automatic blocker. Use the fsm_contract, exported package structure, and explicit supported inputs to construct the rows; stop only when required fields, keys, relationships, or values remain unresolved or validation rejects the package.
10. Populate every root, child, scoped, localized, and relationship object required by the fsm_contract or confirmed package contract. Populate approved business keys, required values, and reference values; omit generated identities unless explicitly required.
11. Classify every populated fsm_contract field as request-provided, documented requirement, export-derived structural value, export-derived template value, generated or omittable, or unresolved.
12. A fsm_contract field may be omitted only when it is documented as generated or optional, is absent or consistently blank in semantically comparable exports of this same task, or is accepted as omitted by supported preview or dry-run validation. Do not infer a value solely from a field name or description.
13. Do not copy identities, reference keys, parent keys, scope values, localized values, lookup codes, or behavior-changing settings unless the fsm_contract, request, documented guidance, or approved compatible template default explicitly supports the value.
14. Verify every non-generated parent, lookup, code, scope, locale, and related-object reference required by the fsm_contract against approved same-task package evidence or the workflow's documented resolver; include required parents or relationship rows only when the package contract requires them.
15. Build the complete package required by the fsm_contract and package evidence; never use a child-only package or infer fields, defaults, identities, or relationships from another task or object type.
16. Validate package members, fsm_contract objects and fields, metadata, keys, scopes, references, relationships, node order, field-value provenance, and approved changes before import; confirm that no baseline identity, template-only setting, or unrelated row is introduced or modified unintentionally. Use preview or dry-run validation when available.
17. Stop when a required fsm_contract field or object, identity rule, parent-child linkage, scope, dependency, or behavior-changing setting remains unresolved and lacks an explicit approved value or sufficient same-task evidence. Do not block for fields evidenced as generated or validated-omittable.
## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Communication Channels` under `Communication Channels`.
