# Manage Prorate Conventions: Defaulting and Prorate-Date Generation

## Standard Defaults

| Field | Internal | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|---|
| Reference Data Set | No | Enterprise Set | Omitted during create preparation; preserve the existing selection on updates | No; keep an explicit selection | validate_reference_data_set_name |
| Description | No | Exact Prorate Convention Name for create only. For update, preserve the existing Description when the request omits Description. | Description is absent or blank during create preparation; update preparation uses the exact current parent row from resolve_existing_prorate_parent | No; keep a supplied Description | resolve_existing_prorate_parent for update |
| Prorate day position | No | First day | Input validation resolves Monthly or Following month without a first-day, mid-month, or last-day qualifier | No; keep the supported day position resolved by input validation | |
| DeprWhenAcquiredFlag | No | No for a create; preserve the value returned by resolve_existing_prorate_parent for an update | Depreciate when placed in service is omitted during create or update preparation | No; keep a supplied Yes or No and use the export-proven representation | resolve_existing_prorate_parent |
| Unspecified Convention Info DFF columns | No | Blank for a create; preserve each current value returned by resolve_existing_prorate_parent for an update | Convention Info is absent or omits an export column during create or update preparation | No; never copy values from a different convention | resolve_existing_prorate_parent |

Apply the Enterprise Set default before required-input validation; do not ask the
customer to supply a Reference Data Set when this default applies. Verify its
exact dropdown name and resolve SetCode through the existing lookup. Show the
resolved set in the preview; never hardcode its code or substitute another set
if Enterprise Set cannot be verified.

## Audit-Field Defaults

| Situation | What Happens |
|---|---|
| Scope | During create/update preparation, apply this policy only to CreatedBy, CreationDate, LastUpdatedBy, LastUpdateDate, and LastUpdateLogin when present in the parent or detail export header. These are system-managed fields, not business inputs. |
| New parent or detail row, including a new detail during update | Serialize a true empty CSV field: a zero-length value, not whitespace, null, None, or a date placeholder. Never source it from user input, the configured/authenticated username, current time, a login/session identifier, or another row. |
| Existing row in an explicit update | Preserve the exact audit text from that same row using resolve_existing_prorate_parent. Do not regenerate or reformat it. A missing or ambiguous existing-row match does not permit copying another row or blanking an existing row. |
| Unchanged baseline rows | Preserve their audit text when retained by the approved package scope. |
| Contract evidence | Populated audit samples and absent nullability annotations do not override this default. An explicit same-task import constraint contradicting this policy is a technical mapping gap. |
| Existing immutable ZIP | Not applicable; follow Immutable artifact in Design Rules. |

Pass this policy with the task mapping to the parent. Integrity and header
fidelity checks belong to [Design Rules](ora_design_enforcement.md#design-rules).

## Generation Contract

Consume the variant from [Prorate Basis Resolution](ora_input_validation.md#prorate-basis-resolution)
without reinterpreting business input. Output supplies prorate_date_rows.

| Topic | Behavior |
|---|---|
| Input | Consume normalizedFiscalYearRows from resolve_prorate_fiscal_year_range. Process each returned year separately in its supplied order using its own startDate, endDate, and nullable midyearStartDate. Apply Fiscal-year setup preservation in [Design Rules](ora_design_enforcement.md#design-rules). |
| Monthly and Following month ranges | Enumerate each year's intersecting calendar months in ascending order. StartDate is the later of the fiscal-year start and the month's first day; EndDate is the earlier of the fiscal-year end and the month's last day. Preserve separate clipped rows at a fiscal-year boundary within a month. |
| Monthly and Following month target | Monthly uses the source row's calendar month; Following month uses the next calendar month, including December-to-January rollover. |
| Day position | For those two families, First day is day 1, Mid-month is day 15, and Last day is the actual final day of the target month. |
| Half-year | Emit exactly one full-year tuple per returned fiscal-year interval: StartDate and EndDate are that year's exact boundaries; ProrateDate is its non-null midyearStartDate, otherwise the fallback below. |
| Half-year null-midpoint fallback | Only when that row's midyearStartDate is null, calculate inclusiveMonthCount as the calendar-month difference between start and end plus one. Add floor(inclusiveMonthCount divided by two) calendar months to that year's startDate, clamping the day only when the target month requires it. |
| Calendar arithmetic | Use date-only arithmetic without timezone conversion, actual month lengths, and leap years; never fixed-day increments. For Monthly and Following month, do not clip ProrateDate to the generated range: it may precede a clipped StartDate or exceed the fiscal-year end. Half-year's in-range requirement is enforced in Design Rules. |
| Existing-ZIP basis resolution | Use the archive's exact FiscalYearName and generate six Monthly/Following month candidates and one Half-year candidate separately for each returned fiscal year. A candidate that cannot be derived is not a match; retain its reason when no valid match remains or it was explicitly requested. Compare each candidate with the archive using the tuple-multiset check in Complete per-year coverage under [Design Rules](ora_design_enforcement.md#design-rules). Accept one unique match, or a supplied basis hint selecting one of multiple matches; otherwise return a basis-resolution gap. Apply Design Rules to the matched archive. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PRC.GENERATE_DATES | step | 20 | apply_default | generated->PRC.ENFORCE_DESIGN;generation_failed->PRC.HANDLE_GENERATION | PRC.LOOKUP_CONTEXT | stop | Apply Standard Defaults and Generation Contract to the resolved context, including immutable-archive candidate matching when applicable. Apply Audit-Field Defaults only to proposed create/update rows, without creating a ZIP. Pass any audit mapping conflict forward as a technical package gap. |
