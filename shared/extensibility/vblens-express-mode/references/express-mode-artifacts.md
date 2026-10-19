# Express Mode artifacts and write policy

Use this reference before selecting files or promising a customization.

## Scope

This skill supports Oracle Fusion Visual Builder Express Mode. An Advanced
Expression is complex Business Rules logic used within Express Mode; it is not
Advanced Mode.

Advanced Mode-only pages, fragments, action chains, services, backends, and
dependencies are outside the customization scope. They may be read only when
needed to identify why an Express requirement cannot be implemented safely.

## Artifact matrix

| Express area | FA evidence | Extension artifact | Read | Write |
| --- | --- | --- | --- | --- |
| Business Rules | `metadata-rules.json` | `metadata-rules-x.json` | Yes | Yes |
| Advanced Expressions | `metadataRules/<rule>.js` under FA ownership | `metadataRules/<rule>.js` under Extension ownership | Yes | Yes |
| Page Properties | `page.json` or release-equivalent page metadata | `page-x.json` or verified page overlay | Yes | Evidence-dependent |
| Configure Page Properties | `page-r.json` | `page-r-x.json` | Yes | Evidence-dependent |
| Rule-set layouts and containers | `layout.json` | `layout-x.json` | Yes | Evidence-dependent |
| Supporting metadata | `data-description.json`, layout and service metadata | `data-description-x.json` and overlays | Yes | Preserve unless separately approved |

Repository topology varies. Confirm paths and ownership from the target
repository rather than relying only on a filename.

## Business Rules

Business Rules are a primary writable capability. Support includes:

- Create, update, explain, activate, and deactivate rules
- Conditions, actions, defaults, validations, messages, and sequence
- Referenced fields, imports, and rule identifiers
- Conflict, overlap, missing-field, lookup, Flexfield, and setup analysis
- Positive, negative, null, boundary, conflict, and setup-missing scenarios

Modify only the minimum rule properties and preserve unrelated ordering and
configuration.

## Advanced Expressions

Use an Advanced Expression when Business Rules logic needs branching, loops,
mapping, value-shape normalization, or defensive handling. Verify:

- Extension ownership and import resolution
- Complete context parameters
- Correct Business Rules field accessors
- Validation return semantics
- JavaScript syntax and designer-safe constructs
- Null, type, date, collection, and setup-specific behavior

## Page Properties

Page Properties are writable only when the target page proves the Extension
overlay contract. Before editing:

1. Locate the FA page-property definition and current Extension overlay.
2. Resolve the exact property name, type, default, allowed values, and runtime
   effect.
3. Confirm the property is intended for customer configuration.
4. Preserve unknown keys and unrelated property values.
5. Patch only the approved property.
6. Validate JSON, overlay ownership, value type, FA counterpart, diff, build,
   and scenario behavior as available.

If the FA counterpart, type, allowed values, or merge behavior is unknown,
return an assessment instead of guessing.

Guided Journeys are supported through exposed Page Properties. Page-level and
section-level Journey Code and Task Codes can be static or conditionally set
with Page Property rules. Support is page-specific: require the exact Oracle
property definition, extendability evidence, value type, and setup values.

## Page Property rules and rule-set layouts

`page-r-x.json` and `layout-x.json` are writable only when the target repository
contains the corresponding `page-r.json` or `layout.json` and the Extension
overlay uses a recognized root shape. Page Property names must be defined by
the Oracle counterpart. Layout fields must belong to the component's data
resource, and container section creation requires an Oracle-provided template.

Read [express-mode-workflows.md](express-mode-workflows.md) and run the
capability inspector before selecting either write route.

## Out-of-scope behavior

When a request requires an Advanced Mode-only artifact:

1. Explain which behavior cannot be represented safely in the supported Express
   artifacts.
2. Identify the Advanced Mode artifact only when repository evidence proves it.
3. Do not modify it.
4. Return the Express alternatives, missing capability, and recommended handoff.
