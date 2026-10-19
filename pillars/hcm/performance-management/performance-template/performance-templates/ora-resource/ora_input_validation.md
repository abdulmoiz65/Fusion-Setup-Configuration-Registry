# Performance Templates Input Validation

Sources: [REST resource and field guidance](../../performance-template-rest-source-contract.md). Verify UI-only behavior for the target release and validate REST requests against live metadata.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Root template create | Name, DocumentTypeId and non-defaulted mandatory fields from target describe, including StarRatingEnabledFlag when required without a default. Preserve the DateFrom server default when declared; supply a value when mandatory without a default. ProcessFlowId is required when periods exist, rather than for every incomplete definition. Resolve status and other business dependencies for the requested lifecycle. | Reject missing target-required fields or violated conditional requirements; preserve documented server defaults | Supply valid required values. Neither SetCode nor a source-only SetId may be sent when absent from target describe. | Create a template | inspect_template_rest_metadata |
| Root or child partial update | Unambiguous existing identity and changed writable fields only | Do not require unchanged create fields in the PATCH body; validate the effective state formed from the fresh record and the proposed changes | Read current values, preserve omitted fields, distinguish omission from explicit null, and validate the resulting state before preview | Change an existing template or child | read_template_by_id |
| Template roles | At least one template-role record | Reject the new template or FSM import | Add one or more valid template roles before validation or import | A new template definition or FSM package is created | resolve_performance_role |
| New role on an existing template | Exact role identity and every section in which it participates | Stop before mutation when section membership is missing; reject a duplicate role or role action | Resolve the role and section choices, then materialize the complete role and role-action graph through the validated FSM archive workflow. Separate REST child creates are not a valid atomic route because the role action requires the generated `TmplRoleId`. | A role absent from the existing template is added | resolve_template_role_action_context |
| Remove an existing role and its last section action | Exact template, section, template-role, and role-action identities; inventory of every section action and period questionnaire using the role; verified clearing of root references; a compatible assigned process flow; fresh raw ETags for both children | Reject split DELETEs, wildcard or quoted guards, cross-template parts, extra parts, an omitted-row FSM archive, or deletion while the assigned process flow still requires participant selection or feedback | Obtain an explicit replacement-flow choice when the current flow requires the role; never guess or clear a period-required flow. Remove or replace questionnaire and root references with verified effects, refresh both ETags, then use only `atomic_role_delete` with exactly the guarded role-action and template-role parts; it emits one-value `ifMatch` arrays and raw-comma composite keys. Finally read both identities and the preserved graph again. | A template role and its final section membership are removed together | read_template_by_id |
| Child operations | Parent template identity and only the writable child attributes for alerts, eligibility profiles at template or period level, periods, roles, sections, section items, questionnaires, due dates, period document types, or role actions | Reject the child operation | Supply the parent identity and child values through the owning accessor; omit generated ids, business-group context, and derived fields | A child row is created, changed, or deleted | read_template_by_id |
| Template alerts | Fresh parent `TemplateTypeCode` plus a process-flow task supported by a non-Anytime template | Reject an alert create or update for `ORA_ANYTIME` even when REST accepts the row; allow guarded delete only for exact unsupported-row cleanup | Explain that template alerts aren't available for Anytime templates; do not preview, dispatch, or claim a saved reminder | An alert is created, changed, or deleted | read_template_by_id |
| Template period | Optional child record. When supplied: CustomaryName, ShortName, ReviewPeriodId, NominalFromDate, and NominalToDate | Do not require or create a period when it is absent; reject an incomplete supplied period | Provide names within their maximum lengths, a valid review period, and dates within template and review-period ranges | A period is created or changed | read_template_by_id |
| Period eligibility profile | TalentObjectType=`TEMPLATE_PERIOD`, TalentObjectId equal to the owning period identity, a resolved EligibilityProfileId, RequiredFlag, and ColumnValue equal to the owning period's exact ShortName | Reject a missing, null, stale, or guessed ColumnValue; do not copy a null source projection into a create payload | Read the fresh owning period and set ColumnValue from its exact ShortName before preview; verify the saved association under that same period | A period eligibility profile is created or changed through REST | read_template_by_id |
| Period questionnaire | TmplRoleId, QuestionnaireId, and SectionId | Reject a new incomplete questionnaire row; validate an update against its effective existing state | Resolve the selected role to its template-role row, not the standalone performance-role ID; resolve SectionId to the selected template questionnaire section | A questionnaire is added or changed through REST | read_template_by_id |
| Template section and role actions | A section definition and at least one template-role-action record for every template-section record; each role action is keyed by a user role already present in template roles | Reject the section operation | Add a valid action for each section and use only a role present in the template-role set | A template section is created or changed, including FSM import | resolve_template_role_action_context |
| Questionnaire section ownership | The fresh Worker `TmplRoleId` and every template role that will own a period questionnaire association | Reject a Questionnaire section without Worker access, or a period questionnaire whose role lacks access to that section | Bind `questionnaire_worker_tmpl_role_id` from the fresh template-role read; include Worker plus each questionnaire owner as section role actions, then create each period questionnaire association separately | A `QUESTIONNAIRE` template section is created | resolve_template_role_action_context |
| Template section | Existing Section Definition and only supported section overrides | Reject the section operation | Select an effective Section Definition, inherit its attributes, then apply valid dependent overrides | A template section is created or changed | resolve_template_section |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| DateFrom and DateTo are supplied | DateTo must be on or after DateFrom | Correct the date range before processing | |
| A template or child update is requested | Generated ids, business-group context, derived names/meanings, in-use and existence flags, ESS fields, and other nonupdateable attributes must not be in a PATCH payload | Remove read-only and technical attributes | inspect_template_rest_metadata |
| A period is supplied | Period dates must be inside the template and review-period date ranges; a due date must be on or after the period start and isn't allowed for ORA_ANYTIME | Correct the period or due-date values | read_template_by_id |
| A period eligibility profile is supplied | `ColumnValue` must exactly equal the fresh owning period `ShortName`; a null value returned by a source/read projection is not a valid create value | Re-read the owning period and rebuild the immutable payload with its exact ShortName before preview | read_template_by_id |
| Ratings, calculations, or weights are supplied | Rating models, levels, calculation fields, and weight/minimum relationships must be compatible with the parent section settings | Correct incompatible or stale dependent fields | read_template_by_id |
| A delete is requested | Root DELETE is disabled; in-use or document-locked objects can't be deleted | Use only the documented custom template-delete action when lifecycle checks allow it, or stop | read_template_by_id |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Name and comments length | Name is required and has maximum 240 characters; Comments maximum is 4000 characters | Root template create or change | |
| Period names | `CustomaryName` is required, globally unique across performance-template periods, and has maximum 240 characters; `ShortName` is required with maximum 10 characters. Preflight the proposed customary name across templates. When the requested wording describes the period rather than requiring an exact literal name and that name is already owned elsewhere, derive a template-qualified unique name and report the actual name used; ask only when the user explicitly requires the occupied literal name. | Period create, update, or copy | read_template_by_id |
| Boolean and lookup-code fields | Use JSON true/false for target fields described as boolean; normalize clear conversational yes/no values. Do not send FSM/entity Y/N strings as REST booleans. Resolve coded fields against the applicable lookup/accessor domain. | Any flag or coded field is supplied | inspect_template_rest_metadata |
| Participant limits | Enforce documented total and per-role minimum/maximum cross-checks and parent-flag dependencies | Participant counts or flags are supplied | read_template_by_id |
| Role-action user role | For FSM CSV, require the keyed user role to exist in template roles and require `UserRoleTypeCode` to be exactly `WORKER`, `MANAGER`, or `PARTICIPANT`. For REST, resolve that role to `TmplRoleId` in the selected template; do not send `UserRoleTypeCode`, derived `RoleId`, `RoleName`, or `RoleTypeCode` on a role-action row. | A template role action is created or changed | resolve_performance_role |
| Section/item weights | Enforce 0 <= minimum <= weight <= 100 and at most two fractional digits where item weighting applies | A section or item weight is supplied | |
| Coordinated section weights | Resolve the complete effective set of included and excluded sections, require included section weights to total 100, and materialize every dependent calculation and manager-reason change in one validated FSM archive. Reject a sequence of independent REST section PATCH requests when two or more section weights or calculation memberships change, because Fusion validates the total after each request. | Two or more section weights or calculation memberships change together | read_template_by_id |
| FSM goal section type | Normalize the REST/export `SectionTypeCode` value `GOALS` to the FSM lookup code `GOAL` in `HRA_TEMPLATE_SECTION.csv`; do not copy `GOALS` unchanged into an import archive | A goal section is exported and regenerated for FSM import | resolve_section_type |
| Duplicate child rows | Reject duplicate period document types, period questionnaires, section role actions, content items, and scoped section sequences/names | Child create or update | read_template_by_id |
| Period document-type date domain | For every `ORA_HRA_TMPL_PERIOD_DOCUMENT_TYPE.csv` row, resolve the document type by its bare `Name` and require its bare `DateFrom` and `DateTo` to exactly equal the resolved document type effective dates. `HRA_TEMPLATE.DateFrom`, `HRA_TEMPLATE.DateTo`, `HRA_TMPL_PERIODS.TmplDefnDateFrom`, and `HRA_TMPL_PERIODS.TmplDefnDateTo` remain parent-template dates and must not be copied into the bare document-type date columns. | A template-period document type is included in an FSM archive | resolve_active_document_type |

| FSM CSV escaping | When creating or regenerating a CSV member, write headers and ordinary values without double quotes. Add double quotes only for an individual value containing a comma, double quote, carriage return, or line feed; double embedded quotes. Reject blanket-quoted CSV members. | FSM CSV import is prepared or revalidated | |

## Generated-ID Null Handling

An `...Id` column is a generated technical identifier, rather than a business
key, when it is blank in the exported create-source row and the corresponding
row is identified by a `GroupingKey` or parent-reference fields. For a new FSM
record, leave such columns empty. Do not write the literal string `#null`.

For a new `HRA_TEMPLATE_SECTION.csv` row, the following generated IDs must be
blank unless Fusion has already returned a real ID for an existing-row update:

- `ContentTypeId`
- `PerfRatingModelId`
- `ProfileId`
- `ProfileTypeId`
- `SectionDefId`

`#null` is not an empty value for this import contract. Fusion can treat it as
a supplied technical value, preventing the parent Template Section from being
materialized and leaving a dependent Template Role Action without a resolvable
`SectionId`. Reject the archive before approval when any of these five fields
contains `#null` for a new section row.

## FSM Grouping-Key Composition

For a new or regenerated Performance Templates FSM CSV row, derive
`GroupingKey` from the complete ordered business-key values below. Join values
with commas and format every date component as `YYYY-MM-DD`, even though the
corresponding CSV date field is formatted as `YYYY/MM/DD`. Do not trim,
shorten, reorder, or substitute a display value for a key component. Preserve
meaningful whitespace in an exported source value, and use ordinary CSV
escaping when a component itself contains a comma.

Use this notation in the table:

- `T` = `TemplateName,TemplateDateFrom,TemplateDateTo`
- `R` = `RoleTypeCode,RoleName,RoleDateFrom,RoleDateTo`
- `S` = `SectionDefnName,SectionDefnDescription,SectionDefnDateFrom,SectionDefnDateTo`

| CSV record | Required `GroupingKey` composition | Notes |
|---|---|---|
| `HRA_TEMPLATE.csv` | `T` | Use the template name and effective dates. |
| `HRA_TEMPLATE_TRANSLATION.csv` | `T` | The translation row uses the same root key. |
| `HRA_TEMPLATE_ROLE.csv` | `T,R` | The role's type, name, and effective dates are all required. |
| `HRA_TEMPLATE_SECTION.csv` | `T,S` | The section description and effective dates are key components; do not use only the section name. |
| `HRA_TEMPL_SEC_ITEMS.csv` | `T,S,CiName,CiContextName` | Use the content item's exact name and context. |
| `HRA_PROCESS_STEP_ALERTS.csv` | `T,StepCode` | The process step code identifies the alert row. |
| `HRA_TMPL_PERIODS.csv` | `CustomaryName` | The template-period customary name is the sole key. |
| `HRA_TMPL_PERIODS_TRANSLATION.csv` | `CustomaryName` | The translation row uses the same period key. |
| `HRA_TMPL_PERIOD_DATES.csv` | `CustomaryName,StepCode` | The process step code identifies the due-date row. |
| `ORA_TMPL_PERIOD_ELIGIBILITY_PROFILE.csv` | `CustomaryName,EligibilityProfileName` | Use the eligibility profile's resolved name. |
| `ORA_HRA_TMPL_PERIOD_QSTNR.csv` | `CustomaryName,UserRoleTypeCode,RoleName,RoleDateFrom,RoleDateTo` | The questionnaire name/code is not part of this grouping key. |
| `ORA_HRA_TEMPLATE_ROLE_ACTION.csv` | `T,R,S` | This is an 11-component key. Include the full section composite, especially description and effective dates. |
| `ORA_HRA_TMPL_PERIOD_DOCUMENT_TYPE.csv` | Leave `GroupingKey` blank | This entity is parent-resolved from its supplied template/period/document-type fields; never invent a grouping key. |

Reject an archive before approval when any populated `GroupingKey` does not
exactly match this composition. In particular, a shortened template-role-action
key cannot resolve its `SectionId` during import.

## Grouping-Key Derivation and Verification Gate

Do not copy a `GroupingKey` from an exported comparator. Populate every row's
business identity, effective dates, and parent-reference fields first; derive
its `GroupingKey` only as the final row transformation. Before archive approval,
reparse each generated CSV member, recompute every nonblank grouping key from
the applicable table above, and reject the archive when the supplied and
recomputed keys differ.

For `HRA_TEMPLATE.csv`, the exact computed key is:

```text
{Name},{DateFrom formatted YYYY-MM-DD},{DateTo formatted YYYY-MM-DD}
```

For example, a row with `Name=Vision 2027 Annual Performance Evaluation`,
`DateFrom=2027/01/01`, and `DateTo=2027/12/31` must use
`Vision 2027 Annual Performance Evaluation,2027-01-01,2027-12-31`; it must
not retain another template's name or dates. Treat a mismatch as a blocking
identity error, even if the CSV shape and Fusion Data Loader validation succeed.

## Pillar-Local FSM Archive Validation Gate

After the final Performance Templates FSM archive is built, and before its
Task Hook preview, approval, or `core.data-loader` submission, run:

```text
python pillars/hcm/performance-management/performance-template/performance-templates/scripts/validate_performance_templates_csv.py <final-fsm-archive.zip>
```

The validator may receive either the final ZIP or its extracted folder. It
recomputes documented `GroupingKey` values, verifies parent-member lineage and
parent-reference resolution within the archive, and rejects literal `#null`
values. A nonzero exit is an input-validation blocker: correct the reported
member and row, rebuild the archive, then run the command again on the rebuilt
archive. Do not continue to Task Hook, approval, or import with an archive that
has not passed this command. Any change after a passing run invalidates that
result and requires a new run.

## FSM Parent-Reference Rewrite Gate

When deriving a new template from an exported comparator, replace every
parent-reference column with the identity of the row's actual parent before
deriving `GroupingKey`. A copied comparator reference is never valid merely
because the child row's own `TmplDefnName` or grouping key was updated.

- For every child, make each `HRA_TEMPLATE.Name`, `HRA_TEMPLATE.DateFrom`, and
  `HRA_TEMPLATE.DateTo` column equal the `HRA_TEMPLATE.csv` parent row.
- For `ORA_HRA_TEMPLATE_ROLE_ACTION.csv`, make each
  `HRA_TEMPLATE_SECTION.TmplDefnName`, `TmplDefnDateFrom`, and
  `TmplDefnDateTo` equal its owning `HRA_TEMPLATE_SECTION.csv` row, as well as
  matching the section's full name, description, and effective dates.
- For every period child, including `ORA_HRA_TMPL_PERIOD_QSTNR.csv` and
  `ORA_TMPL_PERIOD_ELIGIBILITY_PROFILE.csv`, make all
  `HRA_TMPL_PERIODS.TmplDefn*` and `HRA_TMPL_PERIODS.CustomaryName` columns
  equal the owning `HRA_TMPL_PERIODS.csv` row.

- For every `HRA_TEMPLATE_TRANSLATION.csv` row, make
  `HRA_TEMPLATE.Name`, `HRA_TEMPLATE.DateFrom`, `HRA_TEMPLATE.DateTo`,
  `Name`, `TmplDefnName`, `TmplDefnDateFrom`, `TmplDefnDateTo`, and
  `GroupingKey` match the owning `HRA_TEMPLATE.csv` row. Do not retain a
  comparator name, date, or translated comment. If the selected Fusion create
  contract does not support copied translations, stop and obtain authoritative
  guidance before omitting or changing the translation member.

- For every `HRA_TEMPLATE_SECTION.csv` row, require at least one matching
  `ORA_HRA_TEMPLATE_ROLE_ACTION.csv` row. When the design requires Worker and
  Manager access, require one action for each role. Resolve comparator section
  names through an explicit source-to-target map; never assume an active
  section name equals the comparator name.

Before approval, parse every CSV member and verify that every populated
parent-reference tuple resolves to exactly one parent row in the same archive.
Reject the archive if any parent-reference value names the comparator, another
template, or another period. A matching child `GroupingKey` does not repair a
stale parent reference.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PT.VALIDATE_REST_INPUT | decision | 10 | validate_input | valid->PT.DESCRIBE_REST_CONTRACT;invalid->RETURN_ISSUES | none | stop | A Performance Templates REST request is evaluated |
