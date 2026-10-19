# Manage Worker Unions Input Validation

## Purpose

Validates the operation, required inputs, supported fields, and value shapes before dependency resolution or execution.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | get, create, edit, or delete-effective-split | missing | Ask for one supported operation | Every request |  |
| Read selector | Exact OrganizationId or UnionName; optional bounded name search and legislation context | valid | Return a bounded list when no exact selector is supplied | get | find_manage_worker_unions |
| Create identity | Unique UnionName | missing | Ask for a nonblank name | create | find_manage_worker_unions |
| Create country | Exact country code or name | missing | Ask for one country | create | resolve_worker_union_country |
| Effective context | Explicit EffectiveStartDate | missing | Ask for one valid date for the logical object; never infer one | create or edit |  |
| Current target | Exact OrganizationId or UnionName | missing | Ask for one exact current selector | edit or delete-effective-split | find_manage_worker_unions |
| Effective-split deletion range | Exact existing Worker Union, retained EffectiveStartDate, and last deleted EffectiveEndDate | missing | Resolve complete history and provide the inclusive deletion range | delete-effective-split | resolve_worker_union_delete_history |
| Delete confirmation | Explicit confirmation of the displayed effective-split range | missing | Show basic details and request confirmation | delete-effective-split | resolve_worker_union_delete_history |
| Requested changes | At least one explicit supported business-field change | missing | Ask for the intended change | edit |  |
| Organization structure | Organization parent and Worker Union OrgUnitClassification row | missing | Resolve the registered component contract and classification | create | resolve_worker_union_components |
| Additional Information | `FLEX:PER_ORGANIZATION_INFORMATION_EFF`, `OrgInformationContext`, configured multirow unique-key segments, and typed values | missing | Resolve current classification and context metadata | Additional Information is supplied | resolve_worker_union_eff_context |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| get, edit, or delete has an exact selector | valid only when exactly one current Worker Union matches | Resolve the current target | find_manage_worker_unions |
| create | valid only when no exact UnionName match exists | Run the create uniqueness check | find_manage_worker_unions |
| Country is supplied | valid only when exactly one current country matches | Resolve the country | resolve_worker_union_country |
| A mutation is requested | valid only when one registered Organization contract contains every requested field | Resolve the component hierarchy and field contract | resolve_worker_union_components |
| An OrgInformation row is required | valid only when one effective Worker Union classification parent resolves | Resolve the classification | resolve_worker_union_classification |
| Additional Information is supplied | valid only when each context and segment resolves exactly once with its type and cardinality | Resolve the context metadata | resolve_worker_union_eff_context |
| A supplied EFF segment with no task-specific resolver declares a value set | valid only when one typed stored value resolves through its segment contract | Resolve the segment value | resolve_worker_union_eff_segment_value |
| Associated Bargaining Units is supplied | valid only when each value resolves exactly once through the segment value set; zero matches may use the agreed creation flow | Resolve, conditionally create, and re-resolve each association | resolve_worker_union_bargaining_unit |
| An Additional Information code is supplied or copied | valid only when no other Worker Union uses it | Validate uniqueness | validate_worker_union_information_code |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Loader Boolean value | For an included attribute declared by current loader metadata as Boolean or Flag, write true or Yes as Y and false or No as N; preserve Y or N; do not add an omitted attribute or change REST read values | A Data Loader mutation includes the attribute |  |
| Operation is get, create, edit, or delete-effective-split | Otherwise unsupported | Every request |  |
| UnionName is nonblank and no longer than 240 characters | Otherwise invalid | create or name change | find_manage_worker_unions |
| EffectiveStartDate is an explicit valid date and applies to the Organization row and every included child row | Otherwise invalid; never default today or inherit a copied date | create or edit |  |
| Set, SetCode, and SetId are absent | Otherwise unsupported because Worker Unions are not set enabled | Any request |  |
| Each Additional Information context has a resolved segment, native type, cardinality, and classification parent | Otherwise invalid | Additional Information is supplied | resolve_worker_union_eff_context |
| Each supplied context occurrence remains in its own OrgInformation row under the same Organization load group | Otherwise invalid; do not merge different contexts | Additional Information is supplied | resolve_worker_union_eff_context |
| A value-set-backed EFF segment with no task-specific resolver uses its metadata-declared typed stored value | Otherwise invalid; do not write display text when it differs | The segment is supplied | resolve_worker_union_eff_segment_value |
| Associated Bargaining Units use a typed value re-resolved from the current context segment value set | Otherwise invalid; never write the unresolved user value | An association is supplied | resolve_worker_union_bargaining_unit |
| Additional Information code is unique and remains in its own context row | Otherwise invalid; do not copy or reuse another union's code | A code is supplied or copied | validate_worker_union_information_code |
| Mutation scope keeps the Organization and OrgUnitClassification rows. Include OrgInformation only when the user explicitly specifies an Additional Information change and supplies its resolved context and values; otherwise remove its worksheet and Data Loader Map row before DAT generation. For delete-effective-split, include the reserved `Data Loader Directives` sheet with the single allowlisted `Directive` value `SET PURGE_FUTURE_CHANGES Y`; do not add it to the Data Loader Map. An included OrgInformation row contains operation-required identity, parent, date, classification, flex/context controls, multirow identity, and only the specified or operation-required segments from the resolved context; other contexts and optional unchanged segments are excluded | Otherwise invalid | create, edit, or delete-effective-split | resolve_worker_union_components |
| Date-effective split deletion | Allow deletion of one or more noninitial future effective splits only with `SET PURGE_FUTURE_CHANGES Y`, an `Organization` MERGE row, and at least one operation-required `OrgUnitClassification` association. Require EffectiveStartDate to identify the last record to retain and EffectiveEndDate to identify the final split to delete. Reject HDL DELETE, first-row deletion, and an unbounded, nonadjacent, or misaligned range. | delete-effective-split | resolve_worker_union_delete_history |
| ClassificationName is `Worker Union` and ClassificationCode is `ORA_PER_UNION` | Otherwise invalid | An OrgUnitClassification row is supplied | resolve_worker_union_classification |
| `FLEX:PER_ORGANIZATION_INFORMATION_EFF` and `OrgInformationContext` contain the same deployed context code | Otherwise invalid | An OrgInformation row is supplied | resolve_worker_union_eff_context |
| Every flexfield segment marked as a unique key is present and unique | Otherwise invalid | A multirow OrgInformation context is supplied | resolve_worker_union_eff_context |
| Delete boundary | Reject complete delete or ZAP; allow only the confirmed noninitial future split range | delete-effective-split | resolve_worker_union_delete_history |
| The displayed eligible range is explicitly confirmed before Core Data Loader handoff | Otherwise missing | An eligible range has been displayed | delete-effective-split |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| UNION.VALIDATE | decision | 1 | validate_input | valid->UNION.READ;missing->UNION.ERROR;invalid->UNION.ERROR;unsupported->UNION.ERROR | none | stop | Every Manage Worker Unions request |
