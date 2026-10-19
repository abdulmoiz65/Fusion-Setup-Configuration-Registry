# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 05 | Route user-requested task export | Start the routed task-level export without a second protected-data confirmation or approval. |
| 10 | Enforce non-secret Draft configuration | Permit only hCAPTCHA, non-secret inputs, and Draft lifecycle intent. |
| 20 | Enforce minimal-delta provider-header package and metadata-repair boundary | Permit only the verified multi-provider parent CSV containing requested rows and required task metadata; when XML parsing finds the exact null provider collection, apply the Empty-Export Metadata Replacement Contract in a new package; exclude source configuration rows and credential/settings artifacts. |
| 30 | Enforce controlled import handoff | Require target audit and immutable multi-provider package review before one handoff to core.data-loader, which owns final import approval. |
| 40 | Enforce post-import reconciliation | Require a fresh post-import export before reporting the requested Code and Name, Provider ID, and Draft status for every requested record. |
| 50 | Enforce manual secure boundary | Keep credential entry, validation, and activation outside this skill. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A configuration is prepared or imported. | Blocker | | The provider is not hCAPTCHA. | Select the supported hCAPTCHA provider. | Yes |
| A configuration preview, CSV row, diagnostic, durable repository/project artifact, or non-FSM package input is evaluated. | Blocker | | Site Key, Secret Key, token, tenant data, customer configuration value, credential, session data, or an environment/requester value outside required process metadata in a local FSM source or generated ZIP is present. | Remove and redact the prohibited value before continuing. Required non-secret Fusion process metadata may remain unchanged only inside the local source and generated FSM ZIPs; do not quote, log, commit, or persist it elsewhere. | Yes |
| A task-level export is explicitly requested. | Not a blocker | | None. The direct export request is sufficient; do not require a second protected-data confirmation or approval. A possible, theoretical, or historical indication of protected content is not a blocker. | Route to shared.setup-export.task-level-export. Do not refuse, substitute a template-only export, or redirect to manual Fusion based on a prediction. Required non-secret process metadata inside the local source or generated FSM ZIPs under the Empty-Export Metadata Replacement Contract is not a protected value for this rule; do not quote or log it. For any other protected value, do not persist or quote it and return a sanitized diagnostic. | Yes |
| The initial authoring outcome is prepared or imported. | Blocker | | The configuration is not Draft or requests Active status. | Keep the configuration as Draft. | Yes |
| A provider-header CSV package is generated or reviewed. | Blocker | | The package includes anything other than ORA_IRC_CX_PROVIDERS_CONFIGS.csv and ASM_SETUP_CSV_METADATA.xml, the parent CSV header is not ConfigCode, ConfigDescription, ConfigName, ConfigStatus, ProviderId in that order, the candidate contains an existing source configuration row, any requested ConfigCode or ConfigName is duplicated within the batch or matches a fresh target source row, any requested record is invalid or omitted, its row order differs from the caller-supplied requested record order, or any constructed row does not use the requested Code, optional or blank Description, requested Name, Draft status, and hCAPTCHA ProviderId 2 in that column order. | Build only the requested delta with required metadata context; do not submit an eligible subset. | Yes |
| XML parsing finds an exact null MigrationProcessBusinessObjectCSVMetadata1 collection in a fresh target export. | Blocker | | The Empty-Export Metadata Replacement Contract preconditions or output checks fail, the original export is altered, or the output package has extra members, a different CSV header, a different requested record set, or an unverified replacement collection. | Treat the export as empty-target audit evidence. Create a new immutable package only under the contract below, retain the source export, and exclude all settings and credential artifacts. | Yes |
| A controlled multi-provider import is requested. | Blocker | | A fresh target export, an allowed immutable package, its verified requested record set, or SHA-256 for the exact target and package identity is missing. | Complete target audit/preflight and hand off the generated package SHA-256 once only to core.data-loader. Do not request a duplicate task-level approval. | Yes |
| A post-import reconciliation is requested. | Blocker | | A fresh post-import task export is unavailable, or it does not provide the requested Code and Name exactly, plus Provider ID and Draft status, for every requested record. | Obtain the fresh export and reconcile every requested record before reporting success. | Yes |
| Credential completion, hCAPTCHA validation, or activation is requested. | Blocker | | The requested action would enter credentials or activate the provider through this skill. | Complete secure credentials, validation, and activation manually in Fusion after the separate approval process. | No |

## Empty-Export Metadata Replacement Contract

Use this contract only for `ORA_IRC_CAPTCHA_PROVIDER_CONFIGURATION`. The
canonical mapping below is fixed task guidance captured from the approved
authoring reference; do not ask the runtime user to supply an XML reference.
Parse XML; do not use a text substitution.

## Metadata-Only Export Decision Order

Evaluate this decision before applying a generic missing-CSV blocker:

1. When the fresh export for `ORA_IRC_CAPTCHA_PROVIDER_CONFIGURATION` contains
   only `ASM_SETUP_CSV_METADATA.xml`, parse and validate the exact null-export
   form in this contract.
2. If every contract precondition passes, treat the export as empty-target
   audit evidence and execute the Empty-Export Metadata Replacement Contract.
   Do not require source provider rows to prove a collision-free target.
3. If any precondition fails, block package preparation. Do not discard,
   substitute, or alter the source export.
4. For a populated export, retain the source as collision evidence and apply
   the Minimal-Delta Import Contract. For every other metadata-only shape,
   retain the normal missing-CSV blocker.

`CAPTCHA.ENFORCE_DESIGN` owns the local composition. It can return the
`import_requested` outcome only after every contract check below has passed.

1. Confirm the fresh export ZIP has exactly one `ASM_SETUP_CSV_METADATA.xml`
   member and exactly one `MigrationProcessCSVMetadataVORow` parent row. The
   parent must have ProcessId `-999`, ObjectShortName
   `ORA_IRC_CAPTCHA_PROVIDER_CONFIGURATION`, ObjectType `TASK`, ProcessType
   `EXPORT`, and ProcessStatus `COMPLETED` or `COMPLETED_WARNINGS`. It must
   retain exactly one matching
   `MigrationProcessMigrationObjectCSVMetadataVORow` for
   `ORA_IRC_CX_PROVIDERS_CONFIGS`, with MigrateFlag `Y` and
   IncludeExternalDataFlag `Y`. A failed, timed-out, or mismatched export is not
   a package source.
2. Select the only `MigrationProcessBusinessObjectCSVMetadata1` child. Continue
   only when it has only `null="true"` as an attribute, has no element children,
   and has no non-whitespace text. Any other attribute, text, or child is a
   mismatch; do not discard it.
3. Construct `MigrationProcessBusinessObjectCSVMetadata1` with exactly one
   `MigrationProcessBusinessObjectCSVMetadataVORow` from this canonical mapping.
   This table is the source of truth: do not read or copy a separate reference
   XML, and do not add parent process, environment, requester, date, release,
   or ESS values.

| Metadata Element | Required XML Representation |
|---|---|
| ProcessId | Child text -999 |
| BusinessObjectShortName | Child text ORA_IRC_CX_PROVIDERS_CONFIGS |
| BatchName | Empty child with XML attribute null="true" |
| XmlAttributeList | Child text ConfigCode,ConfigDescription,ConfigName,ConfigStatus,ProviderId |
| XmlAttributeTypeList | Empty child element |
| XmlNodePath | Child text /ProvidersConfigsVO/ProvidersConfigsVORow |
| NodeSequence | Child text 1 |

4. Create a new ZIP in approved local, nontracked runtime storage; never
   overwrite the fresh export. Retain source and generated ZIPs separately.
   Retain every target XML node and attribute except the exact null child
   collection, replace only that collection with the constructed canonical
   collection, and add only `ORA_IRC_CX_PROVIDERS_CONFIGS.csv` with the verified
   header and one or more requested non-secret Draft rows in the caller-supplied
   order. Require every row to have a distinct `ConfigCode` and `ConfigName`,
   requested Code, optional or blank Description, requested Name, Draft `ConfigStatus`, and
   hCAPTCHA `ProviderId` 2. Required non-secret Fusion
   process metadata may remain unchanged only inside these ZIPs; do not quote,
   log, commit, or persist it elsewhere.
5. Reopen the new ZIP before the handoff. Verify that its XML parses, it
   has only the two allowed members, every unrelated XML node and attribute is
   unchanged, the replacement wrapper has no `null` attribute or extra child,
   and its CSV has exactly the requested non-empty record count, preserves the
   caller-supplied row order, and contains no duplicate `ConfigCode` or
   `ConfigName`. Verify
   the CSV header and every row value against the requested record set.
   Calculate the generated ZIP
   SHA-256 and retain only that identity plus a sanitized validation record;
   provide the exact package identity to core.data-loader for its approval
   workflow. Stop on any mismatch.

## Minimal-Delta Import Contract

Keep every fresh target export unchanged as audit and collision evidence. Build
a separate immutable candidate ZIP with only the required package context: the
verified `ASM_SETUP_CSV_METADATA.xml` member, unchanged for a populated export
or repaired only by the Empty-Export Metadata Replacement Contract for an exact
null collection, and `ORA_IRC_CX_PROVIDERS_CONFIGS.csv`.

For a populated fresh export, the candidate CSV contains its fixed header and
only the caller-supplied requested rows in caller-supplied order. No existing
provider-configuration source row is a required parent or context row: never
copy, append, modify, or otherwise carry one into the candidate.

Before composition, compare every requested `ConfigCode` and `ConfigName` with
every other requested row and every source row in the fresh target export. Any
collision is a package-contract blocker. Stop and require a distinct requested
record; do not rename it automatically, rely on Fusion collision handling, or
submit a partial batch.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CAPTCHA.ENFORCE_DESIGN | decision | 40 | design_enforcement | draft_preview->CAPTCHA.DONE_DRAFT_PREVIEW;import_requested->CAPTCHA.GATE_IMPORT;post_import_reconciliation->CAPTCHA.RECONCILE_EXPORT;blocked->CAPTCHA.HANDLE_DESIGN_BLOCKER | CAPTCHA.APPLY_DEFAULTS | stop | A non-secret Draft preview, controlled multi-provider import, or post-import reconciliation is requested. |
