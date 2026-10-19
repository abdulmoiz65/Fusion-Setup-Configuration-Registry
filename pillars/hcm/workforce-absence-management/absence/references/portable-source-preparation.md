# Portable Absence Source Preparation

Use the repository-owned
[`prepare_absence_source.py`](../scripts/prepare_absence_source.py) for local
REST Data Loader source assembly and exact-source verification after the
selected task has resolved its inputs. Do not create replacement generators
under `project/`, `/tmp`, or another run-local directory. Project directories
hold input evidence and generated artifacts, not a separate implementation.

The helper supports these registered business objects:

| Setup task | Business object |
|---|---|
| Absence Types | `absenceTypes` |
| Absence Plans | `absencePlans` |
| Absence Categories | `absenceCategories` |
| Absence Reasons | `absenceReasons` |
| Leave Agreements | `absenceLeaveAgreementTemplates` |
| Absence Certifications | `absenceCertifications` |

This is an offline source-shape, relationship-key, and date-control check, not
universal business validation or a certification that Fusion will accept a
load. It does not perform lookups, authenticate, call Fusion, establish current
metadata freshness, approve an archive, submit a load, or verify saved records.
Existing task rules, resolved live LOVs, permitted defaults, compatibility and
impact checks, and Task Hook evidence remain required. An action absent from the target UI is unavailable, with supported choices.
Missing native contracts or invalid source sections block only the affected
supported execution; listing a business object here does not establish every
operation on every child.

## Local Prerequisites and Metadata

Keep the complete repository layout, including unchanged `core/data-loader`
and core authentication modules. QA must set up its own local
`core/auth/fusionEnv.properties` through the existing environment setup
workflow. Core's module import requires that file to exist even for local
preparation; the helper does not read its credentials or request a token.
Never distribute an authenticated configuration, token cache, or secrets in a
portable package. `--help` works offline without that local configuration:

```bash
python3 pillars/hcm/workforce-absence-management/absence/scripts/prepare_absence_source.py --help
```

Obtain the current registered UCM schema through the already selected
`core.data-loader` read-only metadata workflow. Retain its environment,
freshness, and validation evidence in the task run. Do not use REST describe,
an incomplete sample, or invented metadata as a DAT-template substitute.
At that already-authorized metadata step, serialize the returned native schema
with the shipped `absence_source_io.export_contract(schema)` function. Persist
the returned JSON through the task's existing artifact workflow. Do not write a
project-local schema exporter or reconstruct the native metadata by hand. The
function is offline: it does not fetch or refresh the schema. The local
`--contract` JSON contains:

- `businessObject`: the exact registered root discriminator.
- `schemaSource`: `UCM_TEMPLATE`.
- `sections`: each `schema.sections` discriminator mapped to its ordered
  registered header array, with the root first and children in template order.
- `attributes`: `schema.attributes` mapped to arrays of native attribute
  metadata, including `AttributeName`, LOCAL/PARENT reference classifications,
  user-key alternatives, and applicable field constraints.
- `components`: the native `schema.components` dictionary, retaining the
  registered parent discriminators.

Preserve native field names and metadata; do not replace them with business
labels or hand-authored key rules. The helper parses this capture but does not
prove when or from which target it was obtained. Missing key metadata or a
template mismatch is a blocker, not permission to infer relationships.

## Resolved Input

`--intent` takes one JSON object with `businessObject` and a nonempty `records`
array. Each record has a `values` object, a semantic `operation`, and its
operation-specific business dates. Nested `children` maps exact registered
section names to arrays of the same record shape.

- Leave Agreements accepts `create`, `edit`, and `delete` for current-version
  actions; undated `update` wording normalizes to `edit`. Existing Edit rows derive
  `effectiveOf=RangeMode=CORRECTION;RangeStartDate=<verified stored Start Date>`;
  current Delete rows derive the date-free `effectiveOf=RangeMode=ZAP` control. Neither accepts a new operation date; dated operations are unavailable for this task. Use
  exact returned identities and native metadata for current child keys.
- Other tasks use `create`, `update`, `correction`, `end-date`, `delete-changes`,
  or `zap` only when their UI and current section contract support that action.
- Supply `effectiveStartDate` for date-scoped create/update/correction or
  delete-changes, and `effectiveEndDate` for end-date, as `YYYY-MM-DD`.
  Keep lookup as-of dates separate from ZAP range controls. Resolve any task
  default or date confirmation before invoking the helper; it does not choose
  a business date. Do not silently discard supplied end-date intent.
- `values` contains resolved technical fields with string, integer, or Boolean
  values. Omit unset fields. Never supply caller-authored `RestAction` or
  `effectiveOf`; the helper derives controls from the semantic operation.
  Physical date-field requirements remain task-specific, not universal.
- For Leave Agreements, an existing parent `edit` may carry `storedStartDate`
  as read-only context from the exact current before state. This context is
  never serialized. A new child has an explicit `create` operation and inherits
  that stored date for the existing native POST contract; a conflicting new
  child date is rejected. It does not date or reset the parent PATCH.
- Children of a create can inherit its create operation and start date. State
  a different supported child operation/date explicitly. Existing identities
  must be returned and verified by the task workflow, never copied from samples.
- Within one DAT section, every prepared row must have the same field set.
  Never pad arbitrary omissions with blanks. The new-US-type exception below
  resolves two inapplicable rule-metadata fields explicitly in the prepared
  model. For other differing field sets, resolve the intended values or use
  separately reviewed archives only where the task permits independent
  operations. Never split a new type hierarchy to bypass this check.
  An explicitly supplied blank remains distinct from an unresolved omission.
- The helper maps the resolved create start to the physical parent field for
  Reasons and for Categories when current metadata requires it. Other physical
  dates remain task-specific. New type hierarchy rows inherit their parent
  create date; a conflicting child date is rejected, not silently discarded.

The following shape is synthetic; its codes and identifier are not live lookup
evidence and must not be submitted as a ready-made tenant fixture:

```json
{
  "businessObject": "absencePlans",
  "records": [{
    "operation": "create",
    "effectiveStartDate": "2030-01-01",
    "values": {
      "AbsencePlanName": "Example Recording Plan",
      "AbsencePlanTypeCode": "N",
      "AbsencePlanStatusCode": "P",
      "LegislationCode": "US",
      "LegislativeDataGroupId": "100001",
      "AbsencePlanUOM": "H",
      "AbsencePlanPeriodType": "C",
      "CalendarStartMonth": "1",
      "CalendarStartDay": "1"
    }
  }]
}
```

For a supported child-only Types, Plans, Categories, or Leave Agreements operation,
a root record can use
`contextOnly: true`, identity-only `values`, and explicit child operations.
Do not give that root an operation or business changes. It emits a metadata-only
root, not a parent mutation; current external parent identity still requires
the task's live verification. This mode does not replace task-required parent
carrier rows in other flows, such as Reasons flexfield maintenance. A Leave
Agreements child Add additionally carries verified `storedStartDate` on this
context-only parent; current child Edit/Delete need no new date. Whole parent
Delete cannot be combined with nested child mutations or an inferred cascade.
Final verification also rejects child mutations linked to a deleted parent,
including rows that use native business-key alternatives without an explicit
resolved parent identifier proving a distinct parent. Prepare separate sources
when parent separation cannot be established; alternative keys alone do not
prove that the actions are independent.

For a missing Reasons flex child on an already verified existing parent slice,
use the explicit root operation `carrier-create`, its resolved start date, and
only `AbsenceReasonId` in root `values`. Include the flex child with explicit
`operation: create` and the same start date. This emits the documented key-only
parent PATCH and child POST with matching create-style range controls. It is
not a new reason create; it is rejected without a matching child or when parent
business values are supplied. Existing-child correction/update retains its
ordinary operation, exact identity, and task-required parent carrier.

Agreement and Certification flex sections may use deployment-specific names.
They require native component ownership, the date/action controls, and a
registered flex marker; a guessed section name is not sufficient. Physical
start remains blank by default. An explicitly supplied physical start must
equal the operation's range start. The helper preserves that candidate and
lists the existing task/operation/section-specific Fusion evidence requirement
in both the model and receipt. Block preview until that evidence proves dual
population writable; an offline pass or a template column is not that proof.

## Absence Type Relationships

Root maintenance rows use the exact returned `AbsenceTypeId` and must omit
`LegislationCode` and `AbsencePatternCode`: those attributes are immutable.
The helper rejects their presence (including blanks) during preparation and
exact-source verification rather than silently discarding a requested edit.
Keep unchanged identity context in the preview/baseline, not root mutation
values. Metadata-only roots and child relationship carriers still retain
their required business keys; this restriction does not alter create rows.

Before preparing a new type, read its `ora-resource/ora_defaulting_rules.md`
and resolve all applicable create defaults, not just Name/Pattern/LDG/Status.
Preserve explicit user choices and validate lookup-backed defaults through the
declared live resolvers. In particular, resolve Partial Day Rule (documented
default A for Generic/Illness, N for Childbirth/placement) and Maximum Duration
(documented default 4160). When either field is omitted, the helper applies
these documented defaults during create preparation, before validation and
rendering. Do not ask the user to supply an optional input merely because it
was omitted. Validate the default Partial Day Rule through the declared live
resolver and show both resulting values in the preview. Explicit values are
preserved; explicit blanks are not treated as omissions. Exact-source
verification still rejects missing or blank values and never repairs an
immutable ZIP. These defaults do not apply to update, correction, end-date,
or delete rows. Other optional fields without documented defaults stay unset
unless a business validation requires a user decision.

For a new type, set resolved-intent `hierarchyKeyStrategy` to `native-user-keys`. Omit root and child surrogate IDs. Bind direct children with `LegislationCode` plus `Name`; use unique `AbsenceRegionCode` for regions and unique `AbsenceUsageCode` for usages, with each usage carrying its owning `AbsenceRegionCode`. Verify these LOCAL/PARENT user-key alternatives against fresh registered metadata. Fusion allocates the IDs, so no client-generated-ID collision check or global collision endpoint is required. Include exactly one new type per archive. Retain all region and usage persona lookup/display/default fields from the fresh pattern. Omit standard rule rows and verify Fusion-generated rules after load; explicit rule creation is not supported by this key strategy. Existing-record operations continue to use exact returned IDs. Never automatically replay a create.

Bind direct type children consistently through the canonical parent user keys
`LegislationCode` plus `Name`, including `absenceTypeRegions`, `plans`, and
`reasons`. Use verified plan/reason handoffs for association targets. A reason
association requires an explicitly selected Boolean `DefaultFlag`; being the
only reason does not imply that it is the default. Retain the separate
association-status and priority decisions for plans. The helper does not
replace live pattern/persona resolution or decide which rules to emit.

### Native business-key create

Set `"hierarchyKeyStrategy": "native-user-keys"` in every new absence-type resolved intent. This is the normal supported create route. The older `native-user-keys-validation` spelling remains an input alias, but emits the same canonical strategy. Omitted strategy retains the legacy numeric-key representation solely for backward compatibility; it is not the supported new-type workflow and its unresolved collision gate must not be waived.

The helper accepts exactly one newly created type, unique region and usage codes, and no explicit rule rows. Refreshed metadata must declare region LOCAL alternative `AbsenceRegionCode`, usage LOCAL alternative `AbsenceUsageCode`, and usage PARENT alternative `AbsenceRegionCode`. Missing alternatives, supplied child IDs, multiple roots, and maintenance operations are rejected. Retain each region's own three persona lookup types alongside its usage codes.

Live validation proved root binding, six regions, 25 usages, plan/reason associations, effective date, requested persona values, and three server-generated rules using independently paged readback. The official loader result reported Failed while those values were committed. Preserve that official status and use the existing exact reconciliation policy to distinguish functional success with a reporting false positive from partial or ambiguous state. Never infer success from a serialized response alone, never retry a committed create, and never claim a clean loader result when it failed. This evidence does not establish every pattern or lifecycle operation as live-tested.

### Mixed rule metadata on a new type

US `GENERIC`, `II`, and `MAP` pattern usages legitimately have different rule
metadata: rule-capable usages supply `EnableRuleEdit` and
`RuleReferenceDateLookupType`; other usages omit them. Keep those omissions
in the resolved intent. For a new root and new regions/usages only, the helper
resolves missing cells for these two columns to explicit empty strings when
another usage needs the column. Current native metadata must identify each
resolved column as an optional (`MandatoryStatusCode=ORA_N`), non-key String.
If every usage omits a column, it remains omitted. Supplied values are never
changed. Partly populated rule-metadata pairs are rejected rather than treated
as inapplicable. No other missing field is filled, and this behavior does not apply to
updates, corrections, existing-parent child creation, or other business objects.

This narrow create representation is grounded in correlated historical US
Generic (25 usages), Illness (30), and Maternity (33) DAT/readback checks:
blank pairs on non-rule usages persisted as null/null, while populated
rule-metadata pairs were retained exactly. It is not a general claim that DAT
blanks mean omission. Those historical runs had official loader Failed
statuses with functionally committed exact-ID readback; they are field-level
evidence, not evidence of a clean loader result or a new live acceptance run.

`prepared-model.json` and the verification receipt expose `fieldResolutions`
with row indices and fields, so the preview can disclose this preparation.
Review the unchanged supplied rule values and requested persona values along
with that list. Keep all regions, usages, and requested associations in the
single flattened create archive. The strict source-field and exact-byte checks
remain active after resolution.

## Prepare, Then Verify the Exact Artifact

Run from the repository root with task-run-local input and output paths:

```bash
python3 pillars/hcm/workforce-absence-management/absence/scripts/prepare_absence_source.py \
  --contract <task-run>/contract.json \
  --intent <task-run>/resolved-intent.json \
  --output-dir <task-run>/prepared-source
```

Use a new output directory; the helper refuses to overwrite one. It creates
`<businessObject>.dat`, `prepared-model.json`, and `source-validation.json`.
Retain the model unchanged as the expected normalized source. The existing core
Data Loader formatter is reused; existing packaging, live schema validation,
Task Hook, preview, approval, and upload behavior remain unchanged.

After core prepares the final immutable upload archive, verify those exact
bytes against the model and the current captured contract before approval:

```bash
python3 pillars/hcm/workforce-absence-management/absence/scripts/prepare_absence_source.py \
  --contract <task-run>/contract.json \
  --model <task-run>/prepared-source/prepared-model.json \
  --verify <task-run>/<final-archive>.zip
```

`--verify` also accepts an exact DAT file. ZIP verification accepts one DAT
member only, with no extra entries. It checks the actual serialized rows and
returns hashes and row counts; caller-declared passing rule results are not
substitutes for this check. A mismatch or failed check stops preparation.
The model and receipt include `contractSha256`; changing the captured column
or key metadata requires regeneration and revalidation against that contract.
For existing-parent Leave Agreement child Create, `leaveCurrentContexts`
retains exact parent identity and stored Start Date outside DAT data, with an
integrity fingerprint. Final model/source verification rechecks each child
create control against that retained context. This checks integrity, not that
the supplied context originated from a live read; the task must still verify it.
Correct the resolved intent or contract and regenerate through the helper;
do not hand-edit the model to conceal a changed source. Any source, model,
schema, or final-archive change requires fresh validation and the existing
immutable approval cycle. Local success never authorizes upload or retry.

This requirement applies only to the selected REST Data Loader source flow.
It does not change FSM exports/imports, XLSX sample generation, read-only search,
or the task's existing post-load status and exact-record reconciliation route.

## Task Hook Continuation

For all six absence setup tasks above, read
[`core.data-loader.task-hook`](../../../../../core/data-loader/task-hook/SKILL.md)
after core has persisted the task-routed immutable preflight. Keep the exact
selected task context, name, sequence, environment, and archive; do not create
a replacement evaluator, approval envelope, or task selection.

When `data-load` returns `taskValidation.taskValidationStatus: ready`, the
registry is ready to execute; the task rules have not yet passed. Continue in
the same workflow: read the returned `executionGuide`, registry, and source
rules, evaluate applicable nodes in prerequisite/transition order, and record
node evidence. Execute only declared live lookups through the shared client.
The lack of an automatic rule-executor command is not a blocker. Do not return
to the user simply because the response contains a plan rather than results.

Aggregate the evaluated evidence into the ordered `ruleResults` required by
the core guide, with `source`, `status`, `issues`, and `changes`. Then use the
existing Task Hook commands, not direct Task Validator calls:

1. `build-data-load-preview --input-stdin`: supply the selected task context,
   final data including the exact archive SHA-256, and evaluated rule results.
2. Present the successful preview through the core Data Loader approval flow.
   Only after approval use `approve-data-load-preview --input-stdin`.
3. Use `verify-approved-data-load-archive --input-stdin --archive <final-zip>`
   with that preview and approval. Persist its returned
   `taskValidationEnvelope` unchanged and hand it to the existing loader with
   the approved preflight. Follow core's evidence registration requirements.

These commands are subcommands of
`core/data-loader/task-hook/scripts/task_hook.py`, run with Python from the
repository root. Read its skill for the complete input contract; these steps
do not replace its Run Book binding, preflight, approval, or integrity checks.

If evaluation encounters a real unsupported lookup, failed rule, or missing
input, report the exact rule and evidence rather than “Task Hook only returned
a plan.” A 404 collision lookup remains a blocker, not a passing or
not-applicable result. Preserve explicit test-only waivers as `overridden`
with the original finding and reason under core's waiver contract; never
carry a developer's test waiver into a recipient's fresh QA/customer run.
Offline verification, registry readiness, evaluated validation, approval,
submission, and verified Fusion completion are distinct states. Report only
the state established by the current run's evidence.

## Offline Regression Checks

After completing the local configuration prerequisite, run from the repository
root using Python's standard library:

```bash
python3 -m unittest discover -s pillars/hcm/workforce-absence-management/tests -q
```

This covers source preparation, exact-byte checks, six-object operation cases,
and clean-copy execution without private helpers or live connections. Fixtures
are synthetic, not target metadata or live acceptance evidence. Also run each
task's existing `tests` directory with the same unittest discovery command to
check its source-rule regressions. Do not ship temporary outputs or credentials.
