# Source intelligence map

This skill was shaped from an Express Mode product requirements document and a
Business Rules Extensibility knowledge package. Its writable domain centers on
Business Rules, Advanced Expressions, and verified Page Properties overlays.
Machine paths, credentials, environment endpoints, and customer-specific
constants are not portable defaults.

## Confidence model

Use these labels:

- **Verified:** confirmed in a recorded target release or runtime.
- **Observed:** supported by product or page evidence but not a complete
  end-to-end rule verification.
- **Candidate:** a plausible solution requiring target-page validation.
- **Unsupported:** recorded as unavailable or unsuccessful in the observed
  release.

Always carry the source release and confidence into recommendations.

## Source coverage

The source package contained:

- 27 Business Rules examples: 8 verified, 18 pending verification, and 1
  unsupported in the observed runtime
- 21 additional solution cases with direct, candidate, setup, field-path, and
  runtime-shape guidance
- Page exceptions and field-path rewrites
- Page-model discovery and report-building guidance
- Advanced Expression, defaulting, date, LOV, runtime, and Flexfield workflows

The data files bundled with this skill are a compact curated index rather than
a verbatim copy.

## Workflow association

| Workflow | Primary reusable intelligence |
| --- | --- |
| Assess | Field selection, availability flags, service discovery, LOV and Flexfield discovery, page exceptions |
| Capability Discovery | Artifact ownership, Oracle counterpart, recognized overlay shape, supported workflow, restrictions, and handoff |
| Explain | Effective configuration, rule inventory, source confidence, report semantics |
| Runtime Evidence | Deployed app-info versions, page/fragment bindings, dynamic layouts, templates, rule ordering, service metadata, and unresolved runtime inputs |
| Create | Business Rules authoring checklist, defaulting choices, Advanced Expression contract, verified patterns |
| Update | Rule and verified Page Properties contracts plus minimal patching, concurrent-change detection, and rollback |
| Test | Accessor rules, designer-safe JavaScript, scenario design, runtime escalation, audits |
| Document | Business-language summaries, technical paths, source and confidence records |
| Export | Dependency discovery, setup-specific mapping, confidence and release metadata |
| Import | Compatibility mapping, conflict analysis, page exceptions, untrusted-input handling |

## Data references

- `data/rule-examples.json`: representative verified, pending, and unsupported
  patterns
- `data/solution-use-cases.json`: representative field-path, setup, and
  runtime-shape guidance
- `data/page-exceptions.json`: durable path and container-shape exceptions
- `data/behavior-contracts.json`: mandatory page-neutral evidence gates,
  forbidden inferences, setup policy, and complete behavioral branches
- `data/solution-library.schema.json`: portable local record contract for rules
  with passed scenario confirmation

Use a stored pattern to guide discovery, not to bypass target repository
evidence.

The source summary counts describe the larger source package. Each data file
also records its actual curated-entry count; do not represent the compact index
as if every source case were embedded.

The compact index also includes page-neutral contracts for future-date true
collections, nth weekday business-day checks, changed LOV classifications, and
null-safe percentage caps. These describe safe logic only; they do not supply
page paths, runtime shapes, holiday calendars, thresholds, or setup values.

Deployed base-bundle artifacts are environment- and version-specific evidence,
not reusable authoring examples. Read their evidence manifest first, preserve
module hashes and source-layer labels, and never execute downloaded modules.
