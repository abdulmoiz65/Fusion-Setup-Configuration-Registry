# Pillar Skills

Pillar skills contain implementation intelligence organized by Oracle Fusion Cloud pillar,
offering, and functional area.

The top-level pillar folders are:

```text
common/
cx/
erp/
hcm/
scm/
```

Use this placement pattern for new pillar-owned content:

```text
pillars/{pillar}/{offering}/
pillars/{pillar}/{offering}/{functional-area}/
```

Repository maintainers regenerate the catalog-backed offering folder structure
and offering-level skills through the catalog-management workflow. The workflow
reads `knowledge/setup-task-catalog/release/pillars-offerings-mapping.json`,
deletes first-level offering folders under the known pillar roots, recreates
`pillars/{pillarSlug}/{offeringSlug}/SKILL.md`, and refreshes the static
hierarchy browser data.

Examples:

```text
pillars/common/public-sector-permits/
pillars/erp/financials/general-ledger/
pillars/hcm/workforce-deployment/global-human-resources/
pillars/scm/order-management/orders/
pillars/cx/sales/leads/
```

Generated pillar skills can be augmented with Oracle FusionApps guidance files
under an `ora-resource/` folder. Add these files through the repository's
pillar-skill generation and FusionApps resource-authoring workflows after the
target pillar skill exists.

Use this resource pattern for functional-area skills and generated nested
setup-task skills:

```text
ora-resource/
|-- ora_input_intake.md
|-- ora_input_validation.md
|-- ora_dependency_readiness.md
|-- ora_reference_lookups.md
|-- ora_defaulting_rules.md
|-- ora_bulk_intake.md
|-- ora_rest_execution.md
|-- ora_design_advisory.md
|-- ora_error_handling.md
`-- ora_design_enforcement.md
```

Newly generated pillar skills should use this `ora-resource/` model for
source-aligned Oracle guidance.

Cross-cutting guidance for integrations, extensibility, data conversion, and
reporting should live in repository-level `shared` capabilities unless it is
specific to a mapped offering or generated functional-area skill.

The `pillars/common` folder is for common setup offerings such as Public Sector
Permits and future Oracle Applications Common setup areas that are represented
in the pillar-offering mapping catalog.
The repository-level `shared` folder remains reserved for cross-pillar implementation
methodology and reusable advisory skills.

This taxonomy is aligned to the current Oracle Fusion Cloud Applications documentation,
including 26B ERP, Procurement, SCM, and latest HCM documentation, plus Oracle's current
Fusion Cloud Applications suite index for CX offerings.

## Token Usage Tracking

Every pillar skill activity must track token usage according to the skill
manifest's `token_usage_tracking` policy. When a pillar skill writes project
artifacts or a skill-run record, include a `token_usage` estimate in the run
record and append or update the project token usage log at:

```text
project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md
```

Use exact tokenizer/API accounting when available; otherwise use the repository
default `chars/4` estimate and note any exclusions.
