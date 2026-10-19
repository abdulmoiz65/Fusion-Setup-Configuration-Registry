# Core Result Bundle

`scripts/expand_worker_manager_requests.py` is a local request-expansion
helper. It never contacts Fusion. The Core REST/BOSS skill executes each entry
from its request manifest and saves the returned JSON in a restricted internal
result bundle:

```json
{
  "environment": "<environment label>",
  "responses": {
    "business_units": { "items": [] },
    "process_catalog": { "items": [] },
    "process_owner_properties": { "items": [] }
  }
}
```

Each manifest entry has a stable `id`; use that id as the key in `responses`.
Preserve each Core JSON response unchanged. Responses containing names, user
identities, or role information must remain outside `project/`.

Before asking the consultant which Level 2 process to work on, the skill reads the complete `process_catalog`
from the directly provided `referenceDataValues` business object and
`process_owner_properties` for current default-owner state in ordered 100-row
pages. Do not use the `allReferenceDataValues` extraction: it unions
user-defined records with provided records. Preserve every returned page;
continue only while Core reports `hasMore=true`, advancing by the nonempty
page size. A missing or malformed continuation signal, empty continuing page,
or incomplete sequence blocks the coverage review. It presents the full
business-process coverage table with one row per Level 2 process. Internally,
each row contains one exact-`valueCode` set of all catalog records with the
same `levelTwo`. A repeated member identity blocks the row and requires a fresh
catalog read. One self-named member is an optional root marker within that set;
no root marker remains valid, while multiple roots block the row. Never add the
root separately. The normal CREATE flow accepts a selected Level 2 row
with unassigned members and changes only those members; configured members
remain informational. UPDATE requires an explicit Level 2 source owner and
changes only members exactly owned by that source. RESET explicitly removes
every existing owner property in the selected Level 2 scope. UPDATE uses the
same candidate route as CREATE; RESET needs no replacement candidate.
No single member, including the root, represents the Level 2 row. Its owner
names and current result must aggregate every scope member before the table is
shown or refreshed; otherwise the coverage row is invalid.
After a CREATE or explicit UPDATE selection, it starts one Core-managed active
department catalog read and semantically evaluates department evidence for each
selected process. It then reads only primary workers from the retained direct
functional departments. It never reads the unfiltered workforce. It does not
ask for a Business Unit or Business Unit-to-process mapping. Returned Business
Unit information or optional customer mapping material may be retained only as
supporting evidence.

When inspecting a response outside the helper, preserve Boolean semantics:
`hasMore: false` is a present, completed result. Do not use a falsey fallback
such as `jq '.hasMore // "missing"'`, because it reports that valid value as
missing. Check the field's type separately from its value.

For each configured USER-owned process in the coverage table, use the
corresponding `process_owner_properties.defaultOwnerUser.name`; for a GROUP,
use `defaultOwnerGroup.name` as the readable current owner when present.
Do not downgrade an available name to **Configured owner**. That generic label
is permitted only when no readable name was returned, and no internal owner
code is shown to the consultant.

For every Level 2 row, classify a member as assigned only when its exact
same-run property row has `defaultOwnerType` USER or GROUP and a nonblank
`defaultOwnerCode`; absent and blank-code properties are unassigned. Aggregate
distinct readable owner names in stable comma-separated order. Derive the
process-level result from the complete scope. Show unassigned members only as
`Unassigned (<reference codes>)`. Use each unassigned member's nonblank catalog
`referenceCode`, including an optional marked root, and sort the codes by
normalized value. The root marker has no display suffix. Do not collapse
distinct members because their Reference Codes match. If an unassigned member
has no usable Reference Code, block the coverage row and require a fresh
catalog read; do not fall back to a process name, hierarchy/category value, or
`valueCode`. Do not enumerate assigned children or display the number of
members in the group; that is internal inventory evidence.
The initial complete coverage table must be rendered in the chat response, not
only stored in the project artifact. A later question about available processes
re-renders the table filtered to Level 2 rows with unassigned members instead
of returning a count-labelled bullet list.

To avoid combining customer data into one file, the helper can instead receive
each Core output directly with repeated `--core-response request_id=path` and
an `--environment` label.

The helper accepts the verified numeric worker identifiers retained by the
department-bounded worker assessment through repeated `--candidate-worker-id`
arguments and an optional `hierarchy` selection. This is the normal
selected-process route; it does not require `--confirmed-mappings`. When no selection is supplied, it
uses `LOWEST_RESOLVABLE` through levels 1, 2, and 3. For `FROM_LEVEL`, it
requests only the configured contiguous manager levels; `TOP` requests full
hierarchy rows. It can be rerun after each Core request batch. It emits only
missing GET requests in this order:

1. requested manager hierarchy rows for every department-bounded worker;
2. BOSS user identities for each retained worker and every returned manager.

The optional Business Unit-evidence route accepts internally recorded resolved
candidate-population `mappings` with `business_unit_id` values. It first emits
worker assignments for every supplied Business Unit, then follows the same
hierarchy and identity sequence. It is never a consultant-facing prerequisite.

For a consultant-supplied exact Fusion username, omit `--confirmed-mappings`.
The direct-owner route validates and resolves only that username and its
verified username label; a Business Unit/process mapping, hierarchy analysis,
and person or assignment record are irrelevant to that route.

The skill, not this helper, performs Business Unit/process matching, hierarchy
selection, customer decisions, assignment preparation, and post-assignment
verification. After Core has completed the bounded candidate-enrichment reads,
the local `scripts/rank_owner_candidates.py` helper creates the restricted owner
recommendation decision record. It has no external-call capability and accepts
only verified Core results and explicitly retained process-function evidence.
After a fresh approval, use the Core REST/BOSS skill for each approved mutation
without automatic write retries. Before approval and before the first write,
confirm that the hidden action plan contains each exact member identity once;
block duplicates rather than issuing repeated bulk requests. For each selected
member, record the redacted physical property state and selected mutation path:
`ABSENT_PROPERTY` with
`CREATE_ABSENT`, `EMPTY_PROPERTY` with `REPLACE_EMPTY_PROPERTY`, or
`ASSIGNED_PROPERTY` with the applicable preserve, update, or reset path. Do
not include member codes, property identifiers, raw request bodies, or
authorization data. Every mutation uses one documented POST to
`referenceDataValueProperties/$bulk` per changed member: CREATE is one
`$operation: CREATE` item for an unassigned member with no property; an
unassigned member with exactly one blank-code property uses a DELETE/CREATE pair with
its verified `$id`. UPDATE is a DELETE/CREATE pair only for a member exactly
owned by the approved source; RESET is one DELETE item for every member with a
valid assigned owner tuple in the selected Level 2 scope. UPDATE, RESET, and
empty-property CREATE require exactly one current property whose `$id` equals
its valueCode.
Never infer a direct PATCH item endpoint or a multi-member bulk atomicity
contract. Re-run `process_owner_properties` for the full scope before approval,
immediately before each changed-member request, and afterwards. Use
`valueCode`, `defaultOwnerType`, and `defaultOwnerCode` to verify CREATE or
UPDATE and confirm property absence to verify RESET. A stale, failed, uncertain,
or verification-mismatched member stops remaining requests in that Level 2
scope; do not retry or compensate it.

A `managerHierarchy` response with `hasMore: false` and an empty `items` array
is a complete result for that worker and level. It is not an authorization,
transport, or pagination failure. The parent skill must finish every requested
worker/level read before reporting the business-facing no-relationship result.
It must not request a manager identity when no manager ID was returned;
department-bounded workers themselves still require identity resolution so
that each candidate can be reviewed.
