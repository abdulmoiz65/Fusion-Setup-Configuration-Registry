# One SKILL child in an existing custom catalog

Use this separate certification-only route when the user explicitly requests
a controlled test of one new SKILL item in an existing custom catalog. It extends
local package preparation, not the verified general-use provider registry.
There is no live SKILL acceptance evidence yet. Do not infer HDL permission,
Skills Center enablement, search ingestion, or employee visibility.

For a six-item request, preserve all six in the review. Explain the one-item test
limit and obtain an explicit selection of a separate canary before using this
route. Do not silently trim, split, or sequentially load the full batch. Batch
support and provider promotion require separate reviewed evidence and changes.

## Preconditions

- Task: `ORA_MANAGE_PROFILE_ITEM_CATALOG`; operation: `create`.
- One existing custom catalog with ContextName `SKILL`; exactly one new portable
  child, supplier `C`; empty rating-description member. Keep all existing
  generated/dynamic/rating/translation/relationship-field prohibitions.
- Authenticated target identity and workflow-established non-production
  classification, retained under a sanitized evidence reference. A hostname or
  a bare user assertion is not authentication. The new-catalog-only optional
  user classification confirmation is not accepted in this route.
- A supplied, fresh, complete, unfiltered same-target Item Catalog evidence ZIP
  satisfying the existing receipt/hash/schema and data-handling contract. The
  parent must resolve once and its portable business fields must be unchanged.
  Reject known child code/name collisions. Missing or contradictory evidence
  blocks the test; an empty/template-only ZIP does not prove an existing parent.
- A validated same-task template/baseline and approved exact provider rows.

This controlled certification retains the stronger supplied-evidence checks.
It does **not** add an export to the import workflow. Skip pre-import export;
reuse already available eligible evidence. If it is unavailable, report the
missing certification evidence and stop. Standalone export investigation needs
its own explicit request and approval under the optional-export policy.

## Local preview and preparation

Use the existing parent FSM package-input contract and its full
`catalog_set_contract` binding shape from
[new-catalog-set-contract.md](../../references/new-catalog-set-contract.md), with
these differences:

- `capability_id`: `item-catalog-existing-skill-canary-v1`.
- `registry_sha256`: actual SHA-256 of
  [catalog-existing-skill-fsm-provider.json](catalog-existing-skill-fsm-provider.json).
- `use` and dependency provider use: `controlled-certification`.
- `target_classification`: `non-production`; `target_evidence_reference` must
  identify routed evidence, not a manufactured attestation.
- No `target_classification_confirmation` field.
- Fourteen complete group counts: one Item Catalog anchor, one child, all other
  groups zero. Source fingerprint and confirmed mappings cover both rows.
- The dependency's `item_catalog_content_item_provider_sha256` still binds the
  existing portable-field registry. The separate contract registry hash binds
  the SKILL candidate; neither hash promotes the nine verified providers.

The parent row is an anchor, not a requested new catalog or an update. Preserve
its current portable values and blank generated fields. Managed catalogs listed
in the candidate registry remain blocked.

Run `scripts/prepare_profile_content_library_fsm_package.py` from the parent
skill with all normal required inputs, including `--current-state-zip`, and
`--preview-existing-skill-canary`. This validates every row and returns a complete
review with no files written and no Fusion calls. After actual user approval of
that exact preview, switch to `--prepare-existing-skill-canary` and supply:

```text
--existing-skill-canary-approval "PREPARE EXISTING SKILL CANARY <catalog_set_fingerprint>"
```

The helper never generates approval on the user's behalf. A changed proposal,
target, mapping, registry, evidence or row invalidates the approval. Modes are
mutually exclusive; the ordinary verified-provider and new-catalog modes cannot
be used to bypass this route's checks.

## Core handoff and certification evidence

The output is only `package_ready_for_core_data_loader_preview`, with
`catalog_set_capability=item-catalog-existing-skill-canary-v1`,
`catalog_set_lifecycle=certification-only` and `runtime_verified=false`.
The task's FSM contract resolver must apply this reference when this capability
is selected; do not treat the verified registry alone as SKILL authorization.
Preserve the exact candidate fingerprint/capability/registry in Task Hook
`finalData`. Execute the existing task rules and Core's separate immutable
preview and submission-approval workflow. The local preparation approval never
authorizes upload or initiation. No direct REST/HDL write or automatic retry.

After separately approved execution, retain status and ProcessLog. Attempt
post-import export; report failures and try registered `skillContentItems` reads
under the optional-export policy. Compare the exact new item and all observable
fields. For full certification, additionally require a complete parent no-drift
comparison, unchanged existing children, and local duplicate-rerun rejection
against refreshed observed evidence (not another live import).

Limited REST readback is partial verification, not certification. Failed import
or incomplete readback must never promote the provider or trigger replay. The
new-catalog lifecycle verifier and existing composite batch runner do not
certify this capability; do not relabel its receipts to use them. Keep the
controlled result provisional until the complete evidence is reviewed.
