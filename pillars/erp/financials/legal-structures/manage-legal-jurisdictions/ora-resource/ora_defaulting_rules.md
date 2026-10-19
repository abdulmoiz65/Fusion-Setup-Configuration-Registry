# Manage Legal Jurisdictions Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Technical FSM values | Apply the reusable defaults below; derive other technical values from current FSM metadata/template or leave unresolved | Every FSM package request | No | verify_jurisdiction_package_baseline |
| Legislative Category | Resolved internal LEGISLATIVE_CATEGORY lookup code | User supplies an exact meaning and export evidence permits the field | No | resolve_legislative_category |
| Legal Entity Registration Code | Resolved internal XLE_REG_CODE lookup code | User supplies an exact meaning and export evidence permits the field | No | resolve_legal_entity_registration_code |
| Legal Reporting Unit Registration Code | Resolved internal XLE_REG_CODE_EST lookup code | User supplies an exact meaning and export evidence permits the field | No | resolve_lru_registration_code |
| Effective From and Effective To | Null independently when the current export/template permits omission | User omits either or both dates | Yes | verify_jurisdiction_package_baseline |
| Identifying Flag outcome | Preserve supplied Y/N. Verify existing identifying jurisdiction(s) when canonical mapping is available; otherwise exclude only that impact check with warning under the task policy. Disclose Oracle identifying behavior without asserting that no identifying jurisdiction exists. | Every create or identifying-flag update | No | find_legal_jurisdiction_existing |
| RequiredEtbFlag | Blank | Create when omitted | No |  |
| RequiredLeFlag | Blank | Create when omitted | No |  |
| Active | Y | Create when omitted | No |  |
| AttributeCategory | Blank | Create when omitted | No |  |
| JurisdictionCode | Exact supplied Name | Create when omitted | No |  |
| RequiredFlag | Y | Legal Function child row when omitted | No |  |
| ORA_XLE_JURISDICTION_DATA child | Header-only when no Legal Function is supplied; otherwise one row per resolved FunctionCode with the exact parent geography transient values and RequiredFlag defaulting to Y | Every FSM package request | No | resolve_legal_jurisdiction_function_code |

The permitted date patterns are: neither date, Effective From only, Effective To only, or both dates. When both are present, Effective From must not be later than Effective To. Do not synthesize a missing date.

## Reusable Create Defaults

These are task-level create-policy defaults, independent of existing jurisdiction
data. They are not claims about Oracle service or database defaults. These
constants and the Name-derived code need no lookup, so their Resolver cells are
blank. Apply
an explicit user value first, including an explicitly requested blank; apply a
default only when the input is absent. Validate flags as Y/N when nonblank and
validate JurisdictionCode uniqueness and its 240-character limit. Preserve Name
exactly when deriving JurisdictionCode. A blank AttributeCategory means no DFF
context; validate any supplied context and segments. These create defaults must
not clear or overwrite omitted attributes on an update.

A fresh same-target export is still required to verify columns, types, parent/
child relationships, encoding, and node order. A header-only template does not
block these documented defaults. Do not copy values from existing jurisdiction
rows or require one as a prerequisite. Record each value's provenance as user
input or this reusable default policy; other unresolved technical fields remain
blocking. RequiredFlag defaults to Y for each Legal Function child row, with
explicit valid user input taking precedence.

## Default Policy Review Scenarios

| Scenario | Expected result |
|---|---|
| New create omits technical inputs | RequiredEtbFlag, RequiredLeFlag, and AttributeCategory blank; Active Y; JurisdictionCode exact Name; supplied Legal Function RequiredFlag Y |
| Valid explicit technical value is supplied | Preserve that value and validate it; do not overwrite it with the default |
| Explicit blank is supplied | Preserve only where the current field contract permits blank; reject an invalid blank rather than silently defaulting it |
| Update omits a technical field | Do not clear or reset that existing attribute using create defaults |
| Current template contains headers and no business rows | Verify structure and use the local create policy; do not demand a populated data export |
| Shared parent/child geography value differs | Block before preview and correct the reference values |

## Geography Carrier Omission

Populate verified country, type, name, and available hierarchy values from the
selected source row. If geography code, geography use, or first-level hierarchy
is unavailable through the supported endpoints, preserve a blank and record a
readiness warning with the complete receipts. Do not synthesize a code, usage,
country name, or hierarchy level, or retrieve existing jurisdiction rows to
fill the gap. Keep corresponding parent/child values identical. These supported
omissions do not waive input, identity, applicable duplicate, package, or
approval checks. The separate two-check policy applies only when canonical
geography mapping is unavailable for a valid create.

## Legal Function Child Contract

`RequiredFlag` is a required technical string attribute on every non-header-only
`ORA_XLE_JURISDICTION_DATA.csv` row. Use `Y` when RequiredFlag is omitted for a resolved Legal Function child row.
Preserve an explicitly supplied valid RequiredFlag instead. This is a schema-level package rule, not a
lookup or copied value from an existing Legal Jurisdiction; it must not cause
creation to depend on any existing jurisdiction's business data.

Before package generation, verify the `RequiredFlag` contract against a fresh,
same-target export and its FSM metadata. Validate an explicit override against the current contract; block
the function branch if the current package contract does not contain this
attribute or does not support the documented value.

## FSM CSV Row-Shape Contract

For every generated `XLE_JURISDICTION.csv` and
`ORA_XLE_JURISDICTION_DATA.csv` member, preserve the exact exported header,
column order, delimiter, quoting, and UTF-8-without-BOM encoding. Before the
archive is considered ready, parse each CSV with a CSV-aware parser and prove
that every data row has exactly the same field count as its header. Do not
construct rows by manually padding comma-separated strings. A missing or extra
field, including a trailing empty field, is a package-contract blocker: rebuild
the row from a header-indexed value map and restart validation.

For this task, parent and Legal Function child rows must also be compared by
header name for their shared geography-transient values. The child rows must
match the parent exactly for every shared geography field before packaging.

Never infer an internal code, metadata member, column, delimiter, encoding, or technical default from a failed import. Record each generated/defaulted value and its export, read-only metadata, Oracle documentation, or EDM source in the import-readiness record.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LJ.APPLY_DEFAULTS | step | 40 | apply_default | applied->LJ.ENFORCE_DESIGN;blocked->LJ.HANDLE_ERROR | LJ.CHECK_DEPENDENCIES | stop | After dependencies are ready |
