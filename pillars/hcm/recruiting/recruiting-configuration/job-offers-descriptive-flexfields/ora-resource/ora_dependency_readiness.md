# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Canonical catalog identity | Confirm the exact task code and CSV export/import support |
| 2 | Fresh target export | Capture the current IRC_OFFERS_DFF package contract from the selected environment |
| 3 | Exact target identity | Resolve global, context, or context-sensitive target from the export |
| 4 | Approved value-set authority | Resolve it only when a requested segment uses a value set or LOV |
| 5 | Immutable preview and import instruction | Validate the candidate ZIP and retain its SHA-256; an original request that explicitly directs import authorizes the same-run candidate |
| 6 | Separate deployment approval | Require only after successful import reconciliation and before manual deployment |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| catalog_identity | Exact task code and supported FSM route | Yes | Every request | Satisfied | Effective catalog | | Prevent use of generic DFF task | Use ORA_IRC_MANAGE_JOB_OFFERS_DESCRIPTIVE_FLEXFIELD and IRC_OFFERS_DFF | Task identity and CSV flags |
| fresh_export | Fresh immutable task-level export | Yes | Create, Update, Preview, Import, Deploy, or Verify | Lookup | Fresh target export artifact | resolve_dff_export_model | Defines the target-release package contract | Export again from the selected target environment | ZIP metadata, members, CSV headers, keys, contexts, segments, sequences, and storage columns |
| value_set_contract | Approved value-set authority | Conditional | A value set or LOV is supplied | Lookup | Explicitly named approved authority | resolve_value_set_authority | A display label alone is not a value-set identity | Provide the approved value-set authority and exact identifier | Identifier, compatibility, and allowed mapping |
| import_instruction | Explicit import instruction | Yes | Before preparing an Import path | Verify | Original requester instruction | | Prevent an unrequested live mutation | State import and the target environment, DFF identity, operation, and target identity in the original request | Request binding and fingerprint |
| deployment_approval | Separate deployment approval | Yes | Immediately before Deploy | Verify | Requester approval | | Import and deployment are different operations | Approve the reconciled imported definition before manual deployment | Deployment approval |
| tds_scope | Separate approved Transaction Design Studio scope | Conditional | Offer-page visibility or requiredness is requested | Verify | Approved TDS request | | DFF import cannot change Offer-page visibility | Route to the separately approved TDS workflow | Offer action, context, attributes, visibility |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| BLOCKED | Fresh export or value-set authority is missing | No |
| STALE_PREVIEW | Target state or candidate fingerprint changed after preview | No |
| MANUAL_INTERVENTION_REQUIRED | Deployment or TDS action has no proven automated route | No |
| AUTH_REQUIRED | Required FSM or task-specific access is unavailable | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IRC_OFFER_DFF.CHECK_DEPENDENCIES | step | 40 | resolve_dependency | ready->IRC_OFFER_DFF.APPLY_DEFAULTS;blocked->IRC_OFFER_DFF.HANDLE_ISSUE | IRC_OFFER_DFF.RESOLVE_EXPORT | stop | After the export model and any value-set contract resolve |

## Selected OAuth cache

Pass both `--properties <selected-profile>` and `--token-cache <selected-cache>`
to every shared export and core Data Loader validation, upload and status command.
When the user selects `core/auth/fusionEnv.local.properties` and
`.fusionaim_token.json`, retain those exact arguments throughout the workflow.
Do not rely on the loader's default cache location: a URL-valued environment can
produce an invalid default filesystem path on Windows. If authentication fails
before upload, renew login through core.auth.fusion-oauth-authentication using the
same explicit paths, then resume only after verifying that no upload was submitted.
