# Algorithm Input Validation

## Required Inputs

| Input | Required state | If missing |
|---|---|---|
| Mandatory preflight | Runs before every advisory, mapping, Groovy, validation, source-resolution, target-resolution, or use-case request | Stop immediately and request corrected attachments; do not continue to source or target reasoning |
| Business requirement | States the intended Accounts Receivables result and invoice, credit-memo, or both scope | Request the business rule and positive/negative examples |
| `Algorithm_BO.xml` | Complete current export for Subscription Management and Account Receivables Integration, attached or explicitly provided with the same request | Stop and request both current XML exports; do not use chat cache, prior project artifacts, remembered paths, or default assumptions |
| Service Mapping source XML | Current copied Service Mapping source export attached or explicitly provided with the same request; any filename is accepted | Stop and request both current XML exports; do not use chat cache, prior project artifacts, remembered paths, or default assumptions |
| Algorithm identity | The supplied `Algorithm_BO.xml` name equals `Subscription Management and Account Receivables Integration` | Reject the export and request the correct Manage Algorithms export |
| Absolute highest version | All algorithm versions are read and the absolute highest `VersionNum` has `ActiveFlag=Y` | Reject the export as not In Progress; do not use an older active version |
| Service Mapping context | The supplied source contains `contextName="ARInterface"` | Stop and request the Subscription AR Integration source export |
| Target action | Identifies the `StepActionSetup` when the selected version has multiple actions | Request the intended action |
| Input type classification | The prompt is classified as Type 1, 2, 3, 4, or 5 using `references/ora_use_case_resolution.md` before source or target resolution | Do not draft; run the classifier and follow the required next step |
| Omitted source or target | When the business result omits a Subscriptions entity or attribute, or an RA target column, the current `Algorithm_BO.xml` has been inspected for candidates, including active-algorithm DFF usage, and the use-case resolution record identifies evidence and limitations | Do not draft until the implementer accepts a named source and target candidate, or provides exact names |
| Objectless source attribute | A source attribute or business term without an object qualifier has been checked against the current Service Mapping XML and validated through permitted describe across relevant Subscriptions AR source objects before any object is recommended | Do not default to a context entity; route to the Service Mapping companion and block Groovy until the implementer accepts one describe-backed source candidate or provides exact names |
| Duplicate described source labels | Same-name or semantically similar candidates across source families have a recorded functional-owner decision with alternatives listed | Stop when the workflow selected a copied, denormalized, convenience, or easier-cardinality candidate without explicit implementer acceptance |
| Existing Groovy decision | States replace or add-above when executable Groovy is already present | Request the implementer decision and formatting preference |
| Contained-entity cardinality | Every alias used by Groovy is identified from the selected action and its `contain(...).cardinality(...)` declaration is read | Stop when cardinality is missing or ambiguous, or when any `ZeroOrOne` alias is directly dereferenced as `<alias>.<attribute>` in generated Groovy. A non-null guard does not replace `?.`; guarded blocks must still use `<alias>?.<attribute>` unless the value was first assigned from a null-safe expression to a local variable. |
| Mapping dependency | A valid current Service Mapping source is supplied; when a source alias, custom attribute, describe lookup, service access, or mapping publication is relevant, a companion result is supplied | Route to the Service Mapping companion skill |
| Describe runtime availability | When a missing or objectless source requires describe, the companion has either completed the permitted describe successfully or reported the runtime connection failure and received the implementer's chosen next path | Stop and ask whether to resolve the runtime environment connection and rerun describe, or proceed only with named unconfirmed assumptions for review |
| Source-resolution record | Every source used by Groovy is recorded as an accepted existing export attribute, an implementer-provided exact source, or an explicitly accepted named describe candidate | Route to the Service Mapping companion; do not draft Groovy from an unverified assumption |
| Per-request mapping contract | Each requested source alias, AR target or control, context, flex context, transaction scope, and condition is confirmed from the current inputs or the accepted companion result. Named assumptions are allowed only as reviewable recommendations and never bypass confirmation gates | Block Groovy drafting and local XML creation until all items used by Groovy are confirmed |
| RA target contract | Each requested Receivables target exists in the public Oracle `RA_INTERFACE_LINES_ALL` reference, and the current interface contract confirms its `ARInterface.insert` context and any required flex context | Do not infer Standard or DFF context from the column name |
| Missing target recommendation | For a scenario without target columns, a target suggestion record first evaluates documented Standard-column matches by business meaning and XML/describe source type, then DFF candidates by source-type family, invoice/header scope, active-algorithm used slots in the same family, and reservation rules. Use `ATTRIBUTE<n>` for string/varchar/character and Boolean-as-code, `ATTRIBUTE_DATE<n>` for date/datetime, and `ATTRIBUTE_NUMBER<n>` for number/integer/long/decimal/numeric identifiers; do not infer numeric solely from an `Id` suffix | Treat the suggestion as advisory only; block Groovy and XML until the implementer accepts the named target and deployed context |
| TransactionInterfaceLineDff reservation | The subscription origin, deployed interface-line DFF flex context, and requested `INTERFACE_LINE_ATTRIBUTE<n>` segment index are confirmed and the target is not internally reserved | Stop and request a different deployed target when `n` is in `1..4` for `Subscriptions Context` or `1..8` for `ORA_DOO_ORIGIN_SUBSCRIPTIONS` |
| DFF-family context | Each physical DFF target has a confirmed RA family and matching interface context: `ATTRIBUTE<n>`/`ATTRIBUTE_DATE<n>`/`ATTRIBUTE_NUMBER<n>` for regular line DFF, `INTERFACE_LINE_ATTRIBUTE<n>` for interface-line DFF, or the corresponding family-specific context | Do not infer a context from a shared segment number or map a target through another DFF family |
| Header DFF insert alias | For `TransactionInterfaceHeaderDff`, the physical `HEADER_ATTRIBUTE*` target and the derived unprefixed insert `AttributeName` are both identified | Do not emit `HEADER_ATTRIBUTE*` as `AttributeName` for `TransactionInterfaceHeaderDff` without an explicit current-contract override |
| Date target conversion | Every confirmed Receivables target with physical RA catalog data type `DATE` uses `AttributeValue: toDate(<date_expression>)`, except a confirmed complete expression of `now()` which maps directly | Block Groovy review until a non-`now()` date expression is converted with `toDate(...)`, or when `now()` is wrapped in `toDate(...)` |
| Skip-control evidence | A skip request includes a current export, approved reference, or implementer-confirmed runtime contract for `SkipBillLines`, plus the confirmed transaction scope and resolved transaction-class expression or matching literal for `TransactionType` | Do not generate skip behavior from an invented Bill Lines property, an unverified control shape, or a skip map that omits `TransactionType` |

## Algorithm XML Checks

| Check | Required behavior |
|---|---|
| Algorithm identity | Accept only `Subscription Management and Account Receivables Integration`. |
| Version eligibility | Proceed only when the absolute highest `VersionNum` has `ActiveFlag=Y`; otherwise stop advisory, Groovy, and XML editing. |
| Starter design | A comments-only initial design may be removed before inserting newly approved Groovy. |
| Approval gate | Return Groovy for review before creating or modifying a local `Algorithm_BO.xml` artifact. |
| Review delivery | Present the complete proposed Groovy in chat and persist an identical project artifact; do not require the implementer to open the artifact to review it. |
| Approval target | Tie approval to the exact Groovy presented in chat before creating or modifying `Algorithm_BO.xml`. |
| Approved-Groovy comparison | Extract the changed action expression and compare it with approved Groovy before handoff; allow line-ending differences only. |
| Service Mapping configuration handoff | After creating the approved local `Algorithm_BO.xml`, persist the companion's configuration handoff with selected sources, aliases, types, access, publication prerequisites, and remaining implementer actions. |
| Final source-target table | After approved Groovy and local `Algorithm_BO.xml` creation, show source object, source attribute, Service Mapping alias, target `RA_INTERFACE_LINES_ALL` column, `ARInterface.insert` `AttributeName`, `AttributeContext`, `FlexContext`, transaction scope, and confirmed-or-assumed status for each mapped value. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ALG_AR_VALIDATE_INPUT | step | 1 | validate_input | valid->ALG_AR_ROUTE_SERVICE_MAPPING;missing->ALG_AR_MISSING_INPUT | none | stop | Always |
