# Page, service, LOV, and Flexfield discovery

Use this reference when a rule cannot be resolved from the visible Extension
files alone.

## Static discovery

1. Identify the page or dynamic-layout directory.
2. Read `layout*.json` to identify regions and owning objects.
3. Read `data-description*.json` to identify object types, relationships,
   endpoints, and metadata paths.
4. Read `metadata-rules*.json` to identify Business Rules-visible fields,
   validation availability, imports, and seeded restrictions.
5. Search page-specific references and known exceptions.

Static evidence can usually identify the owning object, direct versus child
field, and current-versus-initial value strategy.

Classify each observation using
[field-evidence-and-shape-contracts.md](field-evidence-and-shape-contracts.md).
An internal UI variable or action-chain payload is page-state evidence, not the
Business Rules accessor contract.

## Service discovery

When a child or attribute is missing from page files:

1. Resolve the main REST resource behind the page object.
2. Inspect the target environment’s OpenAPI or REST describe metadata.
3. Walk child resources recursively.
4. Merge field title, type, format, cardinality, and updateability evidence.
5. Reapply page-level Business Rules availability flags.

Use `scripts/fetch_service_evidence.js` for deterministic target-environment
describe evidence when the required service resource is known. The command
accepts identifiers rather than an arbitrary URL and records `rest-schema`
evidence in the shared `project/.vblens-cache/` cache.

A service field is not automatically a Business Rules field. Confirm that the
page exposes or can reference it.

## LOV branches

For Job, Grade, Location, Department, Business Unit, or similar selections:

1. Start from the page region’s owning object.
2. Identify the nested LOV provider or child branch.
3. Determine whether the policy needs an ID, code, or display label.
4. Determine object versus collection shape.
5. Confirm availability of `.$initialValue()` when change detection is needed.

Prefer the exact-page Business Rules Design Report for accessor cardinality.
Do not add array normalization merely because an internal page fragment stores
the selected record in a one-row array.

When the final leaf or shape remains ambiguous, keep it unresolved unless the
user supplies separate observed-runtime evidence. Record supplied evidence for
reuse with its page and release.

## Flexfield discovery

### DFF

Discover DFF fields primarily from REST/OpenAPI branches whose resource or
segment identifies a DFF. Capture:

- Page and owning object
- Context
- Segment code and label
- Data type and format
- Copyable Business Rules field path
- Source and release

### EFF

Discover EFF objects from page metadata, including objects whose names identify
an extensible Flexfield or whose endpoints provide EFF page metadata. Parse
contexts, translation labels, segment metadata, data types, and multi-row
evidence.

Use bracket notation when object names are not JavaScript identifiers:

```js
$fields['oracle-eflexfield-DEPARTMENT'].DEPARTMENT_PAGE.CONTEXT_CODE.SEGMENT_CODE
```

Treat multi-row evidence as collection evidence; otherwise prefer the
page-described object shape and validate runtime differences narrowly.

## Lookup and setup values

Never hardcode a label as the stored value. Resolve:

- Display label
- Stored code or identifier
- Effective dates
- Active status
- Environment-specific setup

Resolve values from the target Fusion environment before asking the user for a
code. Use `scripts/resolve_setup_value.js` for these supported sources:

- Active or installed languages from the FND ADF `languagesLOV` resource
- Enabled standard lookup codes for a known lookup type
- Enabled common lookup codes for a known lookup type

Match a language by its Fusion code, standard language tag, or description.
Use the standard `LanguageTag` as the locale value (`ar` for Arabic), and keep
the uppercase Fusion `LanguageCode` (`AR`) as evidence only. Match a lookup by
its stored code or meaning. Accept only one exact case-insensitive match. If no
active match exists, inspect installed languages before reporting activation as
a setup blocker. Never guess that a familiar label has the same code in every
environment.

For a page-specific business LOV, first use the exact page provider, Business
Rules field evidence, or described child resource. The shared language and
lookup services do not prove a page field's accessor or write contract.

Customer identifiers, salary-basis IDs, context codes, and lookup values are
dependencies, not reusable constants.

For derived defaults and multi-key lookups, follow
[setup-mapping-and-defaulting.md](setup-mapping-and-defaulting.md). Request the
setup-specific mapping when metadata proves the fields but not their business
relationship.

## Observed-runtime evidence

Use separately supplied runtime observation only when static sources cannot prove:

- The final leaf name
- Object versus array shape
- ID versus code versus label
- A branch materialized only after a page action

Accept only the minimum relevant branch and avoid exposing personal or
sensitive payload data in reports. This skill does not launch a browser.
