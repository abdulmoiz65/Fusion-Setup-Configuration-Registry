# Time Rule Sets Input Validation

Source: Existing authored defaults, the requested discriminator-aware Time Rule Set member workflow, observed parent/member import and post-import export results, the developer-requested new-Time-Rule preview and approval gate, developer-provided failed-import evidence for BOM-prefixed headers and a parent row with more fields than the Fusion export schema, and generic FSM schema-contract requirements.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Rule set parent row | RuleSetName, RuleType, EffectiveStartDate, EffectiveEndDate | Block the parent row | Provide the required business values; retain a user-provided EffectiveStartDate, or when it is absent apply Current Date as its only value. When EffectiveEndDate is blank, defaulting supplies 4712/12/31, together with ViewInstanceName and GroupingKey; Fusion assigns RuleSetUnqId only after the parent is committed | Always for a parent row | |
| Common member row | ProcessingOrder, RuleSetName, MemberType, committed RuleSetUnqId | Block the member row | Provide a positive ProcessingOrder, one parent RuleSetName, and a valid discriminator; resolve RuleSetUnqId from the authoritative current Time Rule Sets export | Always for a member row | resolve_parent_rule_set_unique_id |
| Rule member identity | RuleName | Block the member row | Supply the Time Rule name and resolve it to one verified compatible Time Rule | MemberType identifies a Time Rule member | resolve_member_time_rule |
| New Time Rule requirement | RuleType, RuleName, condition, threshold, period, and intended result | Block only when the request is incomplete or ambiguous; otherwise hand the normalized requirement to the supported Time Rules workflow for archive preparation and validation | Derive from an exact verified sibling when available; otherwise use a documented compatible template | No verified existing Time Rule matches the requested condition | |
| Nested Rule Set member identity | RuleSetName1 | Reject the member row | Nested Time Rule Set members are outside this task contract; use a dedicated supported workflow when available | MemberType identifies a nested Time Rule Set member | resolve_member_child_rule_set |
| Member Time Category | TcatCd or TcatName | Block the member row when required behavior has no category | Resolve an explicitly supplied or behavior-required category to exactly one supported category | A category is supplied or required by the selected rule behavior | resolve_member_time_category |
| CSV package encoding and first headers | ORA_HWM_RULE_SET.csv and ORA_HWM_RULE_SET_MBR.csv are UTF-8 without a byte-order mark; their first headers are RuleSetName and ProcessingOrder respectively | Reject the entire package before import | Rewrite both CSVs as UTF-8 without BOM, then re-read the first three bytes and parse the first header of each file | Before any Time Rule Sets parent or member CSV import is previewed or submitted | |
| Parent-only archive identity | A parent-stage archive contains exactly ORA_HWM_RULE_SET.csv and ASM_SETUP_CSV_METADATA.xml; it contains no ORA_HWM_RULE_SET_MBR.csv; parsed parent names exactly equal the approved parent Rule Set names | Reject the archive before preview, approval, or import | Rebuild the archive from the finalized parent CSV only; list archive members and parsed parent names in the validation evidence | Every parent-stage archive for a new Rule Set | |
| Fresh schema and field states | The fresh export supplies the current staged-object headers and metadata; every new row is generated from normalized intent. Explicit blank strings, `0`, and `#null` retain their literal value in any supplied supported field | Reject the package before preview, approval, or import | Reprepare the stage package from normalized intent and the fresh export contract; do not clone a source Rule Set row | Every parent or member package | read_rule_set_schema_contract |
| Fresh schema contract | A valid current export with the staged object headers and metadata | Stop preparation | Use the exact staged-object headers and unchanged metadata while generating rows from normalized intent and preserving explicit literal field states | When creating or updating a Time Rule Set from an exported baseline | read_rule_set_schema_contract |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Any member row is supplied | Require exactly one committed exported parent with the same RuleSetName and an effective interval covering the member | Block missing, ambiguous, date-incompatible, or uncommitted parent matches; for a new parent, import the parent alone and refresh the export before member preparation | resolve_parent_rule_set_unique_id |
| Either CSV starts with hexadecimal bytes EF BB BF or its parsed first header differs from RuleSetName or ProcessingOrder as applicable | Invalid package encoding | Stop before import; create a new BOM-free package and repeat full package validation | |
| MemberType identifies a Time Rule | Require exactly one verified Time Rule and compatible RuleType | Block missing, ambiguous, unverified, or incompatible matches | resolve_member_time_rule |
| No verified existing Time Rule matches the requested condition | Require a complete normalized rule requirement, then prepare and validate the immutable Time Rules archive | Continue without a design-confirmation prompt; require approval only immediately before the Fusion import of that exact archive | |
| Any prepared Time Rule detail changes after archive preview | Treat the prior archive approval as stale | Rebuild and validate the archive, then request approval for the revised exact archive before Fusion import | |
| MemberType identifies a nested Time Rule Set | Require exactly one existing or previously created ready child and no self, direct, or indirect cycle | Block missing, ambiguous, unready, or cyclic child references | resolve_member_child_rule_set |
| A Time Category is supplied or required | Require exactly one supported category by exact code or name | Block missing or ambiguous categories; do not create one automatically | resolve_member_time_category |
| The requested design requires members | Require at least one valid member | Block an empty member collection | |
| The approved design contains members and the new parent import succeeds | Preserve the approved member list, refresh the authoritative parent identity, and prepare the member preview automatically | Do not ask the user to restate or separately request the association; require only the member archive's own exact upload approval | resolve_parent_rule_set_unique_id |
| The approved design contains no members | Treat the verified parent import as the complete configuration | Do not prepare an empty member import | |
| Parent, rule, child Rule Set, or category dates do not overlap for the intended effective period | Effective-date incompatibility | Block the affected member | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Parent field types | Validate RuleSetName, RuleType, ViewInstanceName, GroupingKey, and RuleSetUnqId as strings; validate effective dates as dates | Parent row | |
| Effective Start Date selection | Use exactly one date: retain the user-provided EffectiveStartDate, or when absent apply Current Date; reject any result that retains both values | Parent row after defaulting | |
| Member field types | Validate ProcessingOrder as a positive integer and the remaining identifiers as source-supported strings | Member row | |
| Parent ViewInstanceName | Require RuleSetsVO after defaulting | Parent row | |
| Parent GroupingKey | Require exact equality with RuleSetName | Parent row | |
| Parent RuleSetUnqId | Require blank input for a new parent; after a successful parent import, accept only the value found on the matching committed row in the authoritative current Time Rule Sets export | Parent creation and later member preparation | resolve_parent_rule_set_unique_id |
| Member ViewInstanceName | Require RuleSetMbrsVO after defaulting | Member row | |
| Member RuleSetUnqId | Require exact equality with the committed exported parent RuleSetUnqId; reject values sourced only from import responses, process logs, exception keys, failed transactions, or local prediction | Member row | resolve_parent_rule_set_unique_id |
| Member GroupingKey | Require committed RuleSetUnqId followed by a comma and ProcessingOrder with no spaces | Member row | resolve_parent_rule_set_unique_id |
| ProcessingOrder uniqueness | Require unique positive ProcessingOrder values within each parent RuleSetName | All members of a parent | |
| Member discriminator | Accept only `RULE` | Member row | |
| Rule-only fields | Permit RuleName only for a Time Rule member; reject it for a nested Rule Set member | Member row | resolve_member_time_rule |
| Rule-Set-only fields | Permit RuleSetName1 only for a nested Rule Set member; reject it for a Time Rule member | Member row | resolve_member_child_rule_set |
| Rule type compatibility | Require `RuleType=TER` for a `TER` parent Rule Set | Time Rule member | resolve_member_time_rule |
| New Time Rule requirement completeness | Require Rule Type, rule name, condition and threshold, period, and intended result; derive remaining compatible settings from an exact verified sibling or documented template | Before preparing a new Time Rules archive | |
| Time Rule import approval identity | Require explicit approval for the exact validated Time Rules archive; reject implied approval, approval for a different archive, or approval made stale by any material change | Immediately before importing a new Time Rule into Fusion | |
| Child readiness and cycle check | Require child readiness before parent preparation and reject self-reference and every reachable dependency cycle | Nested Rule Set member | resolve_member_child_rule_set |
| Member identity uniqueness | Reject duplicate member identity at the same ProcessingOrder within one parent | Member row | |
| Effective-date compatibility | Require the parent effective interval to overlap the referenced rule interval from the current Time Rules export; when a member category is supplied, require it to be present on that verified rule input | Every resolved member | |
| CSV processing order | When the parent is new, use separate stages: import the parent row, verify its committed exported RuleSetUnqId, then import member rows in ProcessingOrder sequence; do not rely on parent-first ordering inside one package to supply the member identifier | Package preparation | resolve_parent_rule_set_unique_id |
| Parent-stage archive contents | Require exactly one ORA_HWM_RULE_SET.csv and no ORA_HWM_RULE_SET_MBR.csv; require the parsed RuleSetName set to equal the approved parent set exactly, with no extra, missing, or duplicate rows | Every parent-stage archive before validation, preview, approval, or import | |
| Approval separation | Require one exact Data Loader `approve` for the parent archive and a later separate exact `approve` for the immutable member archive | Every new parent with approved members | |
| Post-import member verification | Require a refreshed authoritative Time Rule Sets export to contain the exact RuleSetName, committed RuleSetUnqId, ProcessingOrder, and referenced RuleName or RuleSetName1 member row | After every member import, including an import reported as successful | resolve_parent_rule_set_unique_id |
| UTF-8 BOM exclusion | Read the first three bytes of both CSVs and reject EF BB BF; a visual header check alone does not pass because text readers may hide the BOM | Every Time Rule Sets parent or member package | |
| File-specific first-header identity | Parse the first header after the byte check; require RuleSetName for ORA_HWM_RULE_SET.csv and ProcessingOrder for ORA_HWM_RULE_SET_MBR.csv | Every Time Rule Sets parent or member package | |
| CSV row width | Parse each CSV with the same CSV parser used for package validation; require every data row to contain exactly the same number of fields as that file's header, including trailing empty fields | Before any parent or member package is previewed, approved, or submitted | |
| Schema-driven field preservation | Use exactly the current header order and preserve every supplied literal value, including trailing blanks, `0`, and `#null`; do not add, remove, reorder, or infer fields | When generating a Time Rule Set from a fresh exported schema | read_rule_set_schema_contract |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| RULESET.VALIDATE_INPUT | step | 4 | validate_input | valid->RULESET.DEPENDENCY;invalid->RULESET.INPUT_ERROR | RULESET.APPLY_MEMBER_DEFAULTS | stop | A Time Rule Sets CSV package is prepared |
