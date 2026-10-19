# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 10 | Metadata-repair preparation | When XML parsing finds the exact null provider-metadata collection in a fresh target export, construct and verify one separate immutable multi-provider package from the task-local canonical mapping in the design rule. |
| 20 | Controlled import preflight | Retain the fresh target export and verified immutable multi-provider package before one handoff to core.data-loader, which owns final import approval. |
| 30 | Post-import reconciliation evidence | Retain a fresh post-import task export before verifying the requested Code and Name, Provider ID, and Draft status for every requested provider record. |

## Dependency Rules

## Metadata-Only Export Branch

Before a controlled-import preflight applies a missing-CSV blocker, inspect a
fresh export for `ORA_IRC_CAPTCHA_PROVIDER_CONFIGURATION` as follows:

1. If `ORA_IRC_CX_PROVIDERS_CONFIGS.csv` is present, use it only as source
   collision evidence and continue with the populated-export branch.
2. If it is absent and the ZIP contains only `ASM_SETUP_CSV_METADATA.xml`,
   validate the exact null-export contract in `ora_design_enforcement.md`.
   A valid result is empty-target audit evidence and must run
   `captcha_csv_metadata_repair` before package composition.
3. If that metadata validation fails, or the ZIP has any other shape, stop
   with the normal missing-CSV blocker.

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| captcha_csv_metadata_repair | Approved CAPTCHA CSV metadata repair | Conditional | After XML parsing, the only MigrationProcessBusinessObjectCSVMetadata1 child is the exact null form and the parent/export contract is valid. | Verify | Task-local canonical mapping in ora_design_enforcement.md. | | The embedded mapping is fixed task guidance derived from the approved authoring reference. The runtime user does not provide a reference XML. | Follow the Empty-Export Metadata Replacement Contract: parse the target XML, construct only the canonical child collection in a new ZIP, retain the fresh target metadata otherwise, add the ordered batch CSV, calculate the generated package SHA-256, and reopen and verify the generated package. | Verified replacement child collection, immutable package path, SHA-256, requested record count, and sanitized validation record. |
| controlled_import_preflight | Fresh target audit and immutable package review | Conditional | A controlled multi-provider import is requested. | Verify | A fresh target export retained as audit and collision evidence, plus a separate candidate with required metadata context and a provider-header CSV containing only one or more requested records; or, for an exact null collection, the fresh target metadata, task-local canonical mapping, and verified immutable repaired package with SHA-256. | | The task must bind one handoff to the reviewed package and target. A metadata-only export is valid empty-target audit evidence only after the Empty-Export Metadata Replacement Contract has verified the constructed replacement collection, CSV member, header, every requested Draft row, record count, and package identity. For a populated export, compare every requested Code and Name with every source row before composition; source rows are audit evidence only and are never copied into the candidate. Core.data-loader owns final execution approval. | Do not submit a direct import or an eligible subset. Complete preflight and hand off the exact package and SHA-256 once only to core.data-loader. | |
| post_import_reconciliation_evidence | Fresh post-import task export | Conditional | A post-import reconciliation is requested. | Verify | Fresh task export after the approved FSM import. | | Reconciliation must report the requested Code and Name exactly, plus Provider ID and Draft status, for every requested record. | Do not report reconciliation success until the fresh export is supplied and every requested record is reconciled. | Requested Code, Name, Provider ID, and Draft status for every requested record |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Authorization | Fusion or the shared exporter denies required task-level export access, or Fusion or core.data-loader denies the requested task-level import operation. | No |
| Preflight blocker | A controlled multi-provider import lacks target audit, an allowed immutable package, its requested record set, or SHA-256. | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CAPTCHA.CHECK_DEPENDENCIES | decision | 20 | resolve_dependency | ready->CAPTCHA.APPLY_DEFAULTS;not_ready->CAPTCHA.HANDLE_DEPENDENCY_ERROR | CAPTCHA.VALIDATE_INPUT | stop | A non-secret Draft preview or controlled multi-provider import is requested. |
