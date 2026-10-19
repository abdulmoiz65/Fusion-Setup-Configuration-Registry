# Express Mode customization workflows

Use these workflows after Common discovery. Source access is evidence, not a
blanket write permission. Oracle-delivered dependency artifacts stay read-only;
only a recognized Extension overlay with the required counterpart can be
changed.

The workflow contracts follow Oracle's Express Mode guide for
[Business Rules](https://docs.oracle.com/en/cloud/paas/visual-builder/visualbuilder-extending-adminmode/what-are-business-rules.html),
[Rule Sets](https://docs.oracle.com/en/cloud/paas/visual-builder/visualbuilder-extending-adminmode/configure-layout-express-mode.html),
[Page Property rules](https://docs.oracle.com/en/cloud/paas/visual-builder/visualbuilder-building-appui/property-values-using-rules.html),
and [container sections](https://docs.oracle.com/en/cloud/paas/visual-builder/visualbuilder-extending-adminmode/control-sections-displayed-page.html).

## Capability discovery

1. Run `scripts/inspect_express_capabilities.js` for the target artifact or
   dynamic-layout directory.
2. Confirm the artifact classification, Oracle counterpart, supported
   workflows, restrictions, and unresolved evidence.
3. Classify each item internally as supported and writable, supported with
   restrictions, setup-dependent, source-visible but not Express-writable,
   unsupported, or unknown.
4. Return a positive business-language inventory of supported customization
   choices. Do not include source paths, filenames, artifact names, technical
   classifications, unsupported items, or unknown items unless the user asks.
5. Do not proceed from unknown or source-visible-only evidence to a write. If
   one blocks a requested change, explain that blocker and the smallest
   supported alternative.

## Implementation routing

When the user selects a supported customization, map the business behavior to
the appropriate Extension overlay internally:

- Field behavior, defaulting, validation, messages, and region properties use
  a Business Rules overlay.
- Complex conditions, mappings, or defensive calculations use an Extension-owned
  Advanced Expression referenced by the Business Rule.
- A verified static page setting uses a Page Properties overlay.
- A verified conditional page setting uses a Page Property rules overlay.
- A Guided Journey uses an exposed page- or section-level Journey Code and
  optional Task Codes Page Property. Use a Page Properties overlay for an
  unconditional value and Page Property rules for a conditional value.
- Field, group, layout, or section composition uses a verified rule-set layout
  overlay.

If the required overlay is absent, create the minimum valid `-x` artifact only
after proving its Oracle counterpart when required, Extension destination,
recognized root shape, and supported fields or properties. Populate the new
artifact with the requested customization in the same change; do not create an
empty placeholder and do not edit the Oracle-delivered counterpart.

## Business Rules

Support form and collection rules, regular nesting, If/Else, Switch, default
values, validation messages, and region properties. Evaluate ordinary Business
Rules bottom-to-top: built-in rules first and Extension rules last, making the
topmost matching override effective. For an If/Else branch, evaluate children
top-to-bottom and stop after the first match. For a Switch, require one switch
parameter, unique case values, and an otherwise branch.

Before writing, verify every field, lock, operation, value type, lookup, and
Advanced Expression import. Region Hidden overrides child visibility; region
Required does not make every child field required; region Read Only and Value
are unsupported.

Field-operation feasibility is narrower than artifact feasibility. Use the
field-contract extractor as a raw source index and the behavior contract as a
reasoning checklist before concluding that a named field supports a default or
validation. Neither helper classifies capability or evidence sufficiency. An
unsupported conclusion must retain affirmative exact-field evidence.

The delivered `metadataRuleOptions.conditions` map describes simple-condition
choices; it is not an exhaustive list of fields usable through generated
referenced fields or Advanced Expressions. Missing membership is not
affirmative negative evidence.

## Validation messages

Require an `oj-dyn-form` consumer before claiming that inline validation is
supported. Validate Summary, Detail, severity, target fields, and the rule
condition. Error blocks submission; Warning does not. Multiple or absent target
fields may require dialog rendering supplied by the page.

## Rule-set layouts

Use `layout-x.json` only when a matching `layout.json` and a recognized overlay
shape prove the contract. Support adding/removing/reordering fields, groups,
conditional rule-set layouts, and container sections that the dependency makes
available. Rule-set rules evaluate top-to-bottom and stop at the first match.
Never add a field from another data resource or invent a section template.

## Page Property rules

Use `page-r-x.json` only when a matching `page-r.json` defines the extendable
properties and the overlay uses a recognized root shape. Extension rules run
after built-in rules. Within the Page Property list, rules run top-to-bottom,
and a later matching rule can replace a value set by an earlier rule. Do not
claim support for the visual expression builder in these rule conditions.

## Guided Journeys

Treat Guided Journeys as an Express Mode Page Properties capability, not an
Advanced Mode customization. Support page-level and section-level Journey Code
and Task Codes properties only when the selected page's Oracle metadata exposes
the exact property and permits customer extension. Never infer a property name
from a naming pattern.

Compare the requested placement, Journey Code, Task Codes, and conditions with
the existing customer values. An existing journey is a no-op only when all
requested values and scope already match. Otherwise update the requested
property while preserving unrelated page and section journeys.

Validate the value using the Oracle property definition. Preserve whether task
codes are represented as a string, comma-separated string, array, or
list-of-values. Treat journey activation and task membership as Fusion setup
dependencies. A runtime or transport failure makes deployed observation pending;
it does not make a source-proven Guided Journey capability unsupported.

## Containers and sections

Allow add/remove/reorder operations only for dependency-provided available
sections. Create a new section only when source evidence proves a section
template. Modify section content only through an exposed editable layout or
editable fragment property; editing the fragment implementation is Advanced
Mode work.

## Precedence

Keep these layers distinct:

1. Layout Fields-tab properties are fixed and cannot be overridden by either a
   rule set or a Business Rule.
2. A rule-set layout selects the displayed structure through top-down
   first-match evaluation.
3. Business Rules are object-level and their supported field-property
   overrides take precedence over values defined by rule-set layouts.
4. Page Property rules are a separate layer and do not participate in field
   property precedence.

## Unsupported-change handoff

When the user directly requests unsupported behavior, or it blocks the selected
change, return an Advanced Mode or product-setup handoff when the requirement
needs an Oracle service-definition change, a seeded rule edit, a less-strict
override, an unavailable data-resource field, an unexposed fragment/action
chain, or a container section without a template. Explain the business reason
and smallest Express-compatible alternative by default. Include source evidence
only when requested, and do not edit the Advanced Mode artifact.
