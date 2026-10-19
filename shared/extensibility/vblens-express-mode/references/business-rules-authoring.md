# Business Rules authoring

Use this reference before creating or changing a Business Rule or Advanced
Expression.

Do not use this reference to invent a solution. First consume a successful
Explore report that proves the exact page, Dynamic Form, Business Rules, REST
schema, field operations, and environment provenance.

An Advanced Expression is a Business Rules expression capability used in
Express Mode. Read [express-mode-artifacts.md](express-mode-artifacts.md) when
choosing between Business Rules, an Advanced Expression, and a Page Properties
overlay.

## Contents

- Evidence order
- Field availability
- Value access
- Expression selection
- Validation Advanced Expression
- Designer-safe JavaScript
- Date-only values
- Self-review

## Evidence order

Resolve the target field from the strongest available evidence:

1. Business Rules Design Report for the exact page and release
2. Page-specific FA and Extension metadata
3. `data-description*.json`, `metadata-rules*.json`, and `layout*.json`
4. REST OpenAPI or service describe metadata
5. Flexfield and lookup metadata
6. Page exceptions and verified examples
7. Separate observed-runtime evidence supplied through an approved external workflow

Never reuse a similar-page path without verifying it on the target page.
Never use a repository test fixture as target-page evidence.
Apply [field-evidence-and-shape-contracts.md](field-evidence-and-shape-contracts.md)
when evidence sources expose different shapes. The Business Rules Design Report
controls accessor authoring unless focused runtime evidence proves that the
accessor materializes differently.

## Field availability

Determine whether the field is:

- Present and writable
- Present but hidden or disabled
- Available only through an LOV child
- A DFF or EFF segment
- Present in the service but unavailable to Business Rules
- Missing from the current release

When metadata marks a valid region or segment hidden or `off`, first consider an
Extension overlay that exposes it. Use Extra Referenced Fields only for a
confirmed designer/reference-resolution problem, not as the default solution
for hidden content.

## Value access

Read Business Rules values with the appropriate accessor:

```js
const rawAmount = $fields.compensationSalaries.SalaryAmount.$value();
```

Use `.$initialValue()` only for intentional before/after comparisons. After
calling `.$value()` on a parent object or collection, child properties are
plain JavaScript values and must not receive another `.$value()` call.

Only when exact-page evidence proves that an object-described child can
materialize as a one-row array:

```js
const rawDff = $fields.employmentWorkRelationships.employmentWorkRelationshipsDFF.$value();
const dffRow = Array.isArray(rawDff) ? rawDff[0] : rawDff;
```

Loop only when metadata or runtime evidence proves the child is a true
collection.

Do not infer Business Rules array shape from an internal fragment that
normalizes its private page state into an array.

## Expression selection

Expression selection begins only after exploration resolves the exact field and
its value contract. Do not derive a fallback formula merely because its inputs
are common business concepts.

Default to a simple `[[ ... ]]` expression when the complete result is readable
as one expression. Null checks, optional chaining, or a ternary do not by
themselves require a separate module when the result stays clear.

Select an Advanced Expression without asking the user only when the
implementation needs extra code, such as:

- Helper variables or several return branches
- A collection loop
- Current-versus-initial comparisons
- Object/array normalization
- Setup-specific mappings
- Date or number normalization
- Defensive handling that cannot remain clear in one expression

Present only the selected form. Do not frame simple and advanced expressions as
equivalent user choices.

Put common gating logic in the rule condition and keep a default-value
expression focused on returning its value.

For setup-specific mappings and defaults, also follow
[setup-mapping-and-defaulting.md](setup-mapping-and-defaulting.md). Preserve a
nonempty user-entered target unless the approved business policy explicitly
allows overwrite.

## Validation Advanced Expression

Keep this complete wrapper:

```js
/* eslint-disable dot-notation */
define([], () => {
  'use strict';

  /**
   * Evaluate whether the validation error should be shown.
   * @param {object} context
   * @return {boolean}
   */
  function runCondition(context) {
    const { $componentContext, $fields, $modules, $user, $objectContext } = context;

    // Read values through Business Rules accessors before comparing them.
    return false;
  }

  return { runCondition };
});
```

For validation conditions, return `true` only when the error should be shown.

## Designer-safe JavaScript

Prefer:

- Explicit `if` and `return` branches
- Plain `for` loops
- Null checks before `Number`, `Date`, string, or array operations
- Bracket notation for non-identifier field segments

Avoid unverified callback-heavy expressions such as arrow callbacks with
`.some()`, `.find()`, `.map()`, `.filter()`, or `.reduce()`. A normal
`forEach(function (value) { ... })` pattern has worked in known designer
contexts, but still requires target-release verification.

## Date-only values

Treat `YYYY-MM-DD` values as calendar dates. Avoid browser-local parsing that
can move the selected day across a timezone boundary.

```js
const parts = String(rawDate).substring(0, 10).split('-').map(Number);
const selectedDate = new Date(Date.UTC(parts[0], parts[1] - 1, parts[2]));
```

Use UTC getters and setters for date-only comparison and month arithmetic.
Document a required business timezone separately when the policy depends on
one.

## Self-review

Before finishing, check:

- Exact target page and release were verified.
- Every field path is supported by evidence.
- Values use the correct accessor.
- Materialized child properties do not use redundant accessors.
- Object/array shapes are handled according to evidence.
- Validation return semantics are correct.
- The full wrapper and imports are present.
- Rule identifiers and module imports are unique and resolvable.
- Messages describe the actual error condition.
- Setup-specific values are identified as dependencies.
- Initial/current comparisons use stable identifiers and verified accessors.
- Defaults do not overwrite user-entered values without explicit authorization.
- Technical Create or Update output includes complete metadata, code, imports,
  referenced fields, and scenario cases.

Use `data/rule-examples.json`, `data/solution-use-cases.json`, and
`data/page-exceptions.json` as patterns, not universal truth. Resolve the
matching page-neutral contract in `data/behavior-contracts.json` before
authoring. The contract controls evidence gates and behavioral branches, while
exact page evidence controls paths and customer setup controls values.
