# Performance Management CSV Setup-Data Import Guidance

## Applicability

Apply this guidance to every Performance Management setup task whose catalog
metadata declares `CSVExportImportSupportedFlag: Y`. It supplements the
task-specific validation and `core.data-loader` workflow; it does not replace
the catalog contract, task validation, or the approval gate.

## Verified Archive Pattern

The following pattern was verified in the configured Fusion environment by
Data Loader request `63648` for a one-parent, two-translation Performance
Template Sections update:

1. Start from the exported task archive and retain its metadata XML and every
   CSV entity needed for the changed record.
2. Build the smallest complete record set. When a parent record is changed,
   include that parent row and all required translation rows for the record.
   When a changed parent field also exists in a related translation CSV entity,
   update that field in the applicable translation rows as part of the same
   archive. This applies to every shared field, including descriptions, names,
   comments, and other translatable attributes; do not assume the parent CSV
   value alone updates the translated UI value.
3. Use normal CSV escaping, not blanket quoting: leave headers and values
   unquoted unless a value contains a comma, double quote, carriage return, or
   line feed. Quote and escape only those values that need it. Never assemble a
   CSV row by string concatenation, interpolation, `join`, or a hand-written
   comma-delimited template.
   This is a blocking pre-approval check: reject and rebuild an archive when a
   header or a value without one of those characters is double-quoted. A
   validated ZIP that fails this check must not be approved or imported.

### CSV Creation Rule

When creating or regenerating a CSV member, use a standards-compliant CSV
writer for every header and every row (for Python, `csv.writer` or
`csv.DictWriter` with its default minimal quoting). Never assemble a row by
string concatenation, interpolation, `join`, or a hand-written comma-delimited
template. Do not copy the blanket quoting used by an export, and do not add
quotes merely because the file is CSV. The writer must add double quotes only
when CSV escaping is required for that individual value: a comma, a double
quote, a carriage return, or a line feed; it must double embedded quotes.

Before packaging the ZIP, reparse each generated UTF-8 CSV member with a
standards-compliant CSV reader and fail closed when any data row has a field
count different from its header. Verify the parsed value for every populated
field equals the source value by header name; this is mandatory for free-text
fields such as `Description`, `Comments`, and `Instructions`. For example, a
description containing commas must parse back as one `Description` value, not
as shifted flag values or surplus columns. A Data Loader success status confirms
that Fusion processed the archive; it does not replace this pre-import mapping
verification.
4. For an update, preserve the export's columns, column order, UTF-8 text,
   effective-date values, identifiers, grouping keys, and active/inactive
   status unless the requested change explicitly alters one of them. For a
   new record, preserve only the layout, required transport/relationship
   values, key formatting, and required translation lineage. Never copy a
   comparator's business or configuration values as implied defaults: populate
   them only from the user's request or a documented task default; otherwise
   use null, `N` for flags, or `0` for numeric amounts and counts. Where a
   task-specific rule applies, it takes precedence: Performance Template
   Sections with `WeightSectionFlag=N` must leave `SectionWeight` and
   `SectionMinWeight` blank/null.
5. Validate the ZIP, bind task-level validation to its SHA-256, obtain a fresh
   approval, and then submit that exact archive through `core.data-loader`.

### Parent-Child Completeness Requirement

This is a mandatory CSV-import preparation and pre-approval check for every
CSV-enabled task under Performance Management:

- If a child record is created, updated, or removed, include its owning parent
  record in the same FSM import archive.
- Retain the parent row unchanged unless the requested scope explicitly changes
  the parent. Include the exported parent identity, effective dates, and
  relationship keys required to associate the child row with that parent.
- Preserve every required related row from the exported record lineage,
  including translations when they are part of the entity being changed.
- Reject the archive before approval when a changed child row has no matching
  parent row in the archive. Rebuild it from a fresh export; do not attempt to
  submit an orphaned child row.

Examples of child records include template periods, roles, sections, section
items, questionnaires, due dates, role actions, and comparable dependent
records for other Performance Management tasks.

### Strict Template-Derivation Gate

For a new Performance Template derived from a comparator, the following are
**blocking** checks. Do not package, approve, or import the archive until every
check passes.

1. Map each comparator section explicitly to its target section definition.
   Never select role actions by an assumed equal section name. After the map is
   applied, assert that every `HRA_TEMPLATE_SECTION.csv` row has at least one
   `ORA_HRA_TEMPLATE_ROLE_ACTION.csv` row and that each required Worker and
   Manager action is present.
2. Treat `HRA_TEMPLATE_TRANSLATION.csv` as a full child of
   `HRA_TEMPLATE.csv`. When it is included, its `HRA_TEMPLATE.*`, `Name`,
   `TmplDefnName`, `TmplDefnDateFrom`, `TmplDefnDateTo`, `GroupingKey`, and
   translated comments must match the target parent and target design. Reject
   stale comparator values. When Fusion's create contract does not support
   copied translations, omit the member only after authoritative confirmation;
   never include an incomplete translation row.
3. Use the exact column aliases present in the exported member. In particular,
   role-action CSVs use `UserRoleTypeCode` as the role-type key, and period
   eligibility CSVs may use `HRA_TMPL_PERIODS.CustomaryName` as the parent
   period key. Validators must normalize these aliases before checking keys or
   parent references.
4. Rebuild the archive only after all content changes are complete. Run the
   minimal-quoting writer as the final serialization step; any subsequent CSV
   exporter that blanket-quotes fields invalidates the quote check and requires
   serialization and validation again.
5. Fail closed when a create-path rule graph forces an update-only lookup.
   A create request must transition from a not-applicable current-record lookup
   directly to dependency validation; it must not stop as `not_found`.

The validator must report the member, row, target section, and missing or
stale field for each failure. A successful generic FSM validation does not
waive any of these gates.

### Foreign-Key Reference Gate

Before Task Hook preview, approval, or `core.data-loader` submission, run the
Performance Management foreign-key validator on the final immutable archive:

```text
python pillars/hcm/performance-management/performance-management-common/scripts/validate_performance_management_foreign_keys.py <final-fsm-archive.zip> --task-code <exact-task-code> --reference-bundle <fresh-reference-bundle.json>
```

The reference bundle is required for every CSV-enabled Performance Management
task. It must identify the exact task code, declare
`"coverage": "all-foreign-keys"`, and enumerate every applicable external
foreign-key tuple and every required in-archive parent reference. Obtain each
external tuple from a fresh authoritative export or the task's declared lookup;
do not copy it from a comparator, infer it from a display label, or replace one
effective date with another. Keep reference bundles containing environment data
outside tracked repository and project-workspace files.

For every external foreign key, declare its CSV member, ordered columns, and
the allowed tuples from the authoritative source. When the `GroupingKey`
contains reference components, also declare its full ordered
`grouping_key_columns` so the validator recomputes it. For every internal
parent reference, declare its child and parent CSV members plus their ordered
reference columns. A missing member or column, unmatched foreign-key tuple,
stale parent reference, altered reference effective date, or mismatched
GroupingKey blocks the import. The validator prints SHA-256 values for both the
archive and reference bundle; any change to either requires another run.

Use this shape, with values from the current task's authoritative source rather
than the synthetic example:

```json
{
  "schema_version": "1.0",
  "task_code": "HRA_MANAGE_PERFORMANCE_TEMPLATES",
  "coverage": "all-foreign-keys",
  "foreign_key_checks": [
    {
      "name": "document type",
      "member": "HRA_TEMPLATE.csv",
      "columns": ["DocTypeId", "DocDateFrom", "DocDateTo", "DocTypeName"],
      "allowed_tuples": [["101", "2000/01/01", "2045/12/31", "Annual Evaluations 1"]],
      "grouping_key_columns": ["Name", "DateFrom", "DateTo", "DocTypeId", "DocDateFrom", "DocDateTo", "DocTypeName"]
    }
  ],
  "parent_reference_checks": [
    {
      "child_member": "HRA_TEMPLATE_ROLE.csv",
      "parent_member": "HRA_TEMPLATE.csv",
      "child_columns": ["HRA_TEMPLATE.Name", "HRA_TEMPLATE.DateFrom", "HRA_TEMPLATE.DateTo"],
      "parent_columns": ["Name", "DateFrom", "DateTo"]
    }
  ]
}
```

The example is structural only; its document-type values are synthetic. A task
with no external foreign keys must still provide a bundle with the coverage
declaration and an empty `foreign_key_checks` list. Never claim complete
coverage while omitting a known foreign key.

## Import Authorization and Creation Boundary

For a task with `CSVExportImportSupportedFlag: Y`, the task-level export and
`core.data-loader` workflow are the authorized CSV export/import route. Do not
reject an import solely because the task's functional documentation lacks a
hand-authored REST or CSV creation schema.

Use one of these source patterns instead:

| Request | Allowed source | Boundary |
|---|---|---|
| Update an existing setup record | A fresh export containing the target row and its required related rows. | Change only requested values; retain the exported identity, relationship, and effective-date fields. |
| Create a new setup record | A fresh export containing a structurally comparable record, or a task-provided CSV template. | Clone only the complete required row structure, transport/relationship values, and translations. Set business/configuration values only when supplied by the user or documented as defaults; otherwise use null, `N` for flags, or `0` for numeric amounts and counts. Apply task-specific exceptions, including blank/null `SectionWeight` and `SectionMinWeight` for a Performance Template Section when `WeightSectionFlag=N`. Validate all references before approval. |
| No comparable export or task template | No loadable source is available yet. | Export a comparable record or obtain an approved task template; never invent headers, hidden identifiers, defaults, or parent/child rows. |

This distinction resolves the contract gap: importing from a validated export
is permitted; synthesizing a new CSV layout from UI guidance alone is not.

## Performance Process Flow Task Roles

## Performance Process Flow Acknowledgement Flags

For a Performance Process Flow CSV, worker acknowledgement of a shared
document is independent from review meetings. Set `WkrAckDocFlag=Y` only when
the worker must acknowledge the shared document. Do not set
`ConductMeetingsFlag` or `WkrAckReviewMtgFlag` to `Y` merely because
`WkrAckDocFlag` is `Y`; leave both as `N` unless the user explicitly requests
conducting meetings or acknowledgement of a review meeting.

For a Performance Process Flow CSV, `FinalFeedbackFlag` is always `N`. When
worker or manager final feedback is requested, set `WkrFinalFeedbckFlag` and/or
`MgrFinalFeedbackFlag` as requested, but do not set `FinalFeedbackFlag` to `Y`.

When a Performance Process Flows archive includes `HRA_PF_TASK_ROLES_B` rows:

1. Retain the user-supplied task order. Set each row's `SequenceNumber` to its
   one-based position in that ordered input list.
2. For each supplied `TaskCode`, use the read-only POST action
   `/hcmRestApi/resources/latest/talentPerformanceEvaluations/service/action/getProcessTaskDefinitions`
   with `Content-Type: application/vnd.oracle.adf.action+json` to retrieve the
   no-payload task-definition catalog. Match the user-supplied
     task name to one returned `TaskName`, and use its `TaskCode`. For every
     resolved code except `MGREVAL`, copy the returned `TaskName` into both
     `MgrTaskName` and `WkrTaskName`. For `MGREVAL`, populate only
     `MgrTaskName` and leave `WkrTaskName` blank.
3. Stop if the action returns no exact task-name match or more than one match;
   do not copy task names from another process flow or invent labels.
4. Preserve the task-role translation rows required by the exported archive
     and apply the same resolved-name mapping: both fields for all codes except
     `MGREVAL`, and manager only for `MGREVAL`.

## Troubleshooting Boundary

Do not treat CSV quoting as the universal explanation for an import failure.
If a load fails, retrieve the Fusion process log and correct the reported
record, required field, parent-child relationship, reference, or lifecycle
condition. Rebuild and revalidate the archive; do not retry the same failed
import unchanged.

## Evidence Scope

The successful result establishes a working pattern for this environment and
route. It is operational guidance, not a claim that every task or every Fusion
environment has identical import behavior.
