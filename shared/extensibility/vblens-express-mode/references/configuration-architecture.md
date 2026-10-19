# Express Mode configuration architecture

## Ownership layers

Treat effective page behavior as the combination of:

- **FA layer:** Oracle-delivered configuration. Read-only.
- **Extension layer:** Customer-specific overlays. Eligible for minimal changes
  after confirmation.
- **Deployed base-bundle evidence:** Versioned Oracle-delivered modules reported
  by the target environment. Read-only and incomplete when customer overlays
  are unavailable.

Read both layers when the repository or connected source provides them. If the
FA layer is absent, state that the analysis covers only the available Extension
configuration.

## Configuration areas

| Area | FA example | Extension example | Initial write policy |
| --- | --- | --- | --- |
| Business Rules | `metadata-rules.json` | `metadata-rules-x.json` | Allowed |
| Advanced Expressions | `metadataRules/<rule>.js` | `metadataRules/<rule>.js` under Extension ownership | Allowed |
| Page Properties | `page.json` | `page-x.json` | Allowed with verified contract |
| Configure Page Properties | `page-r.json` | `page-r-x.json` | Evidence-dependent |
| Rule-set layouts and containers | `layout.json` | `layout-x.json` | Evidence-dependent |

Repository topology can vary. Confirm exact ownership and names from local
artifacts before applying the table.

Read [express-mode-artifacts.md](express-mode-artifacts.md) before classifying
an artifact or changing its Extension overlay.

## Capability matrix

Track read, write, and verification separately:

| Artifact family | Initial read support | Initial write policy | Minimum verification |
| --- | --- | --- | --- |
| Business Rules | Yes | Allowed with page evidence | Static plus scenarios |
| Advanced Expressions | Yes | Allowed with rule contract | Syntax, imports, scenarios |
| Page Properties | Yes | Evidence-dependent | Page/release contract |
| Configure Page Properties | Yes | Counterpart and shape required | Schema, ordering, property contract |
| Rule-set layouts and containers | Yes | Counterpart and shape required | Rules, variants, fields, sections |
| Supporting Express metadata | Yes | Preserve | Structural and repository tooling |

For Page Properties, do not write until the target repository proves ownership,
property type, allowed values, and overlay behavior.

## Effective configuration

To determine effective behavior:

1. Inventory FA rules in sequence.
2. Inventory Extension additions, overrides, and imports.
3. Resolve imported Advanced Expressions.
4. Apply status, condition, ordering, and overlay semantics.
5. Identify customer rules that depend on FA fields or properties.
6. Explain conflicts or uncertain merge behavior explicitly.

Do not claim that Extension content replaces FA behavior unless the overlay
contract proves that result.

For dynamic components, resolve the page or fragment binding before the
dynamic layout. Evaluate a named layout's rule list top-down and use the first
matching rule. Business Rules remain object-level; supported Business Rule
field-property overrides take precedence over values defined in rule-set
layouts. Neither layer can override properties fixed in the Layout Fields tab. Evaluate
page-property rules independently, keeping built-in and customer ordering
distinct. See
[runtime-question-answering.md](runtime-question-answering.md) for deployed
evidence traversal and citation rules.

## Change boundary

For an approved rule change:

- Prefer an Extension overlay to an FA edit.
- Add or update only the required rule and module import.
- Preserve unrelated ordering and metadata.
- Change Page Properties only after verifying and approving the exact overlay.
- Keep setup-specific identifiers explicit and documented.

For an approved Page Properties change:

- Resolve the FA property definition and current Extension overlay.
- Patch only the approved property in `page-x.json`.
- Preserve unknown keys and unrelated values.
- State whether verification is structural, build-based, scenario-based, or
  runtime-tested.
