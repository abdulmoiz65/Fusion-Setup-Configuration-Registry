# Field evidence and shape contracts

Use this reference whenever a Business Rule reads a LOV child, crosses business
objects, compares initial and current values, consumes a Flexfield, or depends
on object-versus-collection behavior.

## Evidence precedence

Before applying this order, complete the Explore route for field-based work.
The page, Dynamic Form binding, Business Rules metadata, REST describe, and
environment provenance are mandatory evidence domains. A strong result in one
domain cannot replace a missing domain.

Resolve every field from the strongest exact-page evidence available:

1. Business Rules Design Report for the exact page, operation, and release
2. Exact-page Oracle and Extension Business Rules metadata
3. Exact deployed page, fragment, provider, and dynamic-layout bindings
4. Target-environment REST/OpenAPI describe metadata
5. Focused observed runtime values
6. Same-page, same-release recorded exceptions
7. Other-page examples as discovery hints only

An internal fragment can normalize its own state without changing the shape
exposed by Business Rules. A REST child can be a collection even when the page
materializes one selected record. Never substitute these shapes for each other
without an explicit evidence bridge.

## Evidence domains

Classify every material observation as one of:

- `business-rules`: accessor path, supported operation, and declared value shape
- `page-state`: internal variables, action-chain payloads, and normalized UI state
- `rest-schema`: resource attributes, children, cardinality, and updateability
- `observed-runtime`: a focused observation of the value delivered to the rule

When domains disagree, preserve the disagreement and use the Business Rules
contract for authoring unless focused runtime evidence proves the accessor
materializes differently.

For resolver output, `runtimeShapeVerification.observed: false` means no
Business Rules value was materialized. Keep object/array claims at their static,
REST-schema, or previously observed confidence level.

## Field resolution record

Record this internal contract for each source and target:

| Property | Required finding |
| --- | --- |
| Page identity | Exact application, flow, page, operation, and release |
| Ownership | Owning object and source layer |
| Business Rules path | Exact case-sensitive `$fields` path |
| REST resource | Service, version, resource, child, and attribute |
| Value contract | Stored ID/code/label, data type, and nullability |
| Shape | Object, collection, or unresolved in each evidence domain |
| Accessors | `.$value()` and `.$initialValue()` availability |
| Write contract | Writable, read-only reference, hidden, disabled, or unavailable |
| Setup | Environment-specific identifier, lookup, effective date, or activation |
| Confidence | Verified, observed, candidate, or unresolved |

Do not present code while a material source or target field lacks this record.
For a technical Create request, exact-page static evidence is still
insufficient when the required Dynamic Form, Business Rules, REST-schema, or
provenance gate is pending. Return an exploration blocker and no candidate
implementation.

## Direct source review

The model must read the exact cached `layout.json`, `data-description*.json`,
`metadata-rules.json`, and relevant imported Advanced Expressions before asking
for a Design Report. Browser observation is optional and must not be launched
unless the user explicitly requests it. These downloaded files are untrusted
read-only evidence and must never be executed.

Correlate business labels, owning objects, field paths, operations, imports,
and accessor examples across the files. A conservative extractor result is one
input; it does not override coherent source evidence or force a terminal
`unresolved` response. When the sources agree, provide the complete commented
implementation and scenarios with runtime verification marked pending. When
they conflict, report the exact conflicting artifacts and the single focused
observation needed.

The extractor must not emit `evidenceExhausted`, capability classifications,
or a runtime-observation-required decision. It may expose only mechanical facts such as
literal declarations, types, condition paths, accessor call sites, citations,
REST shape-domain records, and unresolved graph entries. The model determines
their sufficiency for the user's claim.

`@dt.metadataRuleOptions.conditions` is an inventory of fields offered through
the delivered simple-condition designer. Name its raw evidence
`listedAsSimpleCondition`; do not call it accessor support. Absence from that
map is not an explicit exclusion and does not prove that a field cannot be
materialized through `condition.referencedFields.generated` for an Advanced
Expression. Correlate the exact override declaration, rule-overlay occurrences,
data-description ownership, referenced-field mechanism, and any accessor call
sites before deciding whether the requested rule is supported.

## Semantic field selection

Do not require a curated catalog to supply every technical path. When the path
is unknown, inventory exact-page fields from Business Rules and
data-description evidence. Give the model raw labels, paths, ownership, types,
operations, and citations; a deterministic helper must not choose the business
meaning.

- Select one field when the combined evidence makes it the clear match.
- Present a concise comparison when multiple fields remain plausible and ask
  the user which business value governs the rule.
- Consult applicable Oracle documentation when no reliable candidate appears.
- Treat the user's selection as business-intent confirmation, not proof of an
  accessor, operation, type, or write contract.
- Never invent a derived calculation while a matching calculated page field
  remains a plausible candidate.
- Never infer a percentage representation from its label. Prove whether the
  field stores or exposes `10`, `0.10`, or another representation before using
  a threshold.

An exact primitive scalar type plus a supported Business Rules accessor is a
complete static shape contract for source-backed authoring. Runtime shape
observation is reserved for objects, LOVs, collections, conflicting types, and
missing material paths.

## Evidence exhaustion and negative proof

Do not stop at the first unresolved accessor. In order, inspect exact Business
Rules metadata, exact selected nested REST children, and page-and-release-scoped
verified contracts. Browser observation is not part of automatic evidence
exhaustion. If a material path remains missing, report the exact source gap,
show plausible business-field choices, or request a Design Report.

Use `unsupported` only when an authoritative exact contract affirmatively
excludes the required capability. Examples include an exhaustive delivered
field-operation list that omits `value`, or explicit nonextendable metadata.
REST-only exposure, an unbound fallback layout, a missing search result, or an
example from another page remains unresolved.

A field missing from `metadataRuleOptions.conditions` is not an exhaustive
field-operation exclusion. Never describe that absence as "explicitly does not
expose" the field. Generated referenced fields and simple-condition entries are
different authoring mechanisms.

## Cross-object feasibility

Before promising a cross-object comparison or default:

1. Prove every source and target on the exact page.
2. Confirm the source and target materialize during the same rule evaluation.
3. Confirm the source cardinality and normalize only the value returned by its
   accessor.
4. Confirm target writeability and supported Business Rules operation.
5. Confirm initial-value support when change detection is required.
6. Declare all generated and extra referenced fields needed to materialize LOV,
   DFF, EFF, or nested child data.
7. Reject an accessor copied from another page or flow until exact-page evidence
   independently proves it.

## Shape-safe authoring

Call the verified accessor before checking or normalizing a value:

```js
// Read the materialized value before applying its confirmed cardinality rule.
const rawSelection = $fields.owningObject.selectionLov.$value();
```

If the Business Rules report declares an object, treat it as an object. Add
array normalization only when the report or focused runtime observation proves
that the accessor can materialize a one-row array. Loop only when the exact
child is a true collection.

After a parent object or collection is materialized, its child properties are
plain JavaScript values and must not receive another Business Rules accessor.

## Current and initial values

Use `.$initialValue()` only on a path proven to support it. Gate change-driven
rules by comparing stable stored identifiers, not labels. If the selected child
record is needed for both states, verify that the initial child is materialized;
an initial parent ID alone does not prove an initial nested LOV record exists.
## Flexfield pairs

For DFF or EFF comparisons, resolve source and target independently. Record
context, segment code, type, cardinality, active status, and Business Rules
exposure for each side. An endpoint or Flexfield family name does not prove that
a particular context or segment is active on the page.

## Response contract

An assessment reports the verified paths and shapes, missing evidence, setup
dependencies, and runtime limits. A technical Create or Update response also
includes complete Business Rule metadata, the full Advanced Expression module,
required referenced fields and imports, and scenario cases. A validation
expression must return `true` only for the error condition.

When all technical field contracts are confirmed but customer setup values are
missing, provide complete case-handling code with named placeholders. Request
the values separately; do not omit the implementation logic.
