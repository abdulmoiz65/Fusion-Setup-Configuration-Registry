# Collective Agreement Reference Lookups

## Purpose

Defines deterministic, read-only reference resolution for this task.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_manage_collective_agreements | A list search, exact target lookup, or create uniqueness check is requested | Collective agreement identifier, exact code, exact name, or user-supplied name fragment | /hcmRestApi/resources/{version}/collectiveAgreements | Resolve exact names against CollectiveAgreementName. For an explicitly requested contains search, use q=CollectiveAgreementName like '%term%' and replace term with the escaped caller value; read identity, code, name, effective range, and current values. | Return all matches for a caller-supplied list search. Require one exact identifier, code, or name for read, edit, or delete, and zero exact code and name matches for create. | Resolved business identity and effective context | Return zero or all matches for a list search. For read, edit, or delete, stop on zero or multiple exact matches. For create, zero means the identity is available; one or more exact matches block duplicate creation. |
| resolve_status_lookup | A status or configured lookup value is supplied | Exact code or meaning and effective date | [Global Human Resources Common > Manage Common Lookups](../../../global-human-resources-common/manage-common-lookups/SKILL.md), lookup type ACTIVE_INACTIVE for agreement status | Exact enabled code, meaning, and effective range | Require exactly one compatible result; do not choose by result position | Data Loader-supported stored code | Stop and request a more precise value |
| resolve_profile_option_value | A profile option value is needed for setup context | Profile option code, level, and value | [Global Human Resources Common > Manage Administrator Profile Values](../../../global-human-resources-common/manage-administrator-profile-values/SKILL.md) | Applicable profile value and level | Resolve the requested applicable value; do not infer from another agreement | Validated context value | Stop and report the unresolved or ambiguous profile value |
| resolve_collective_agreement_eff_metadata | An extensible-flexfield context or segment is requested | Requested context and segments; for an existing agreement, its fresh EFF envelope | collectiveAgreements root describe followed by the exact collectiveAgreementsEFF polymorphic mapping and child describe returned by Fusion; use current loader metadata for source fields | Context labels and API names, segment labels and attributes, cardinality, updateability, native types, LOV contracts, and loader fields | Require the exact resource, category, context, and segment contract. Create does not require an existing parent or envelope. | Context, segment, target attribute, type, value-set contract, and loader fields | Stop; do not assume a child name, category, or storage attribute |
| read_collective_agreement_eff_context | A Collective Agreement EFF context or segment is read or changed | Exact agreement, effective date, and context or segment | Fresh link-bearing parent and PER_COL_EIT envelope, current polymorphic describe, and returned context child link | Context and segment labels, business values, and row count | Require one exact parent and envelope and one describe-matched returned context link | Business-facing context values | Re-read in link-bearing form before treating a link as missing; never construct a path |
| resolve_collective_agreement_eff_value_set | A proposed EFF segment value is supplied and its current metadata declares an LOV | Exact requested display value and the segment's current describe-declared LOV resource, finder, filter, display attribute, and attribute map | The exact lovResourcePath.resource and filter returned by describe under /fscmRestApi/resources/{resolvedVersion}/, or a fresh server-returned runtime rv URL | Display value, description, identifier or code, target attribute, and native type | Apply the returned finder and filter unchanged. Match the exact requested display text against the declared display attribute; require one compatible result and map attributeMap.source to attributeMap.target in the declared type. | Metadata-declared typed stored code or ID; retain display value only for preview | Stop on no match, multiple matches, type mismatch, target mismatch, or missing metadata |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A describe-declared LOV query is required | Use core.fusion-api.rest-api-client and require one enabled, effective result. |
| A common lookup type is required | Use core.fusion-api.apps-common; do not substitute it for a task-specific or EFF value set. |
| A resolver returns a stored code or ID and a meaning | Retain the stored value separately from its display meaning. |
| EFF context or segment is requested | On create, resolve the current root describe, exact polymorphic collectiveAgreementsEFF mapping, child describe, and loader metadata without requiring a parent. For an existing agreement, also follow only its returned EFF links. |
| Collective Agreement EFF data is requested | Read the exact parent and PER_COL_EIT envelope without `onlyData=true`, then follow the describe-matched returned child link from `links` or `@context.links`. |
| Segment metadata declares an LOV | Use its returned LOV resource, finder, and runtime filters. Add an exact, runtime-encoded display-value filter only when that contract supports it. |
| Value-set result is unique | Keep its display label for preview and map only the metadata-declared stored code or ID, in the declared native type, to the Data Loader field. |
| Runtime rv LOV URL is returned | Follow it only in the current authenticated runtime. Never construct, cache, persist, or reuse the runtime identifier. |
| Segment has no LOV | Treat the value as free text only when current describe marks the target writable and the registered Data Loader object accepts that field; otherwise block. |
| Common lookup is declared instead | Route it through Manage Common Lookups; do not substitute a common lookup for an EFF value-set resolver. |
| Multiple EFF rows use one context | Include the parent and every child in one approved source. Give each row a distinct SequenceNumber and distinct value in the context-specific unique segment returned by the loader template, while repeating the parent IdentificationCode. |
| EFF metadata or values remain to resolve | Run every applicable resolver in graph order in the same turn and continue after each resolved result. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CA.READ | decision | 3 | reference_lookup | resolved->CA.LOOKUPS;list_returned->CA.DEFAULTS;create_available->CA.LOOKUPS;not_found->CA.ERROR;duplicate->CA.ERROR;ambiguous->CA.ERROR;failed->CA.ERROR | CA.DEPENDENCIES | stop | Read is requested, an exact target is required before edit or delete, or a uniqueness check is required before create |
| CA.LOOKUPS | step | 4 | reference_lookup | resolved->CA.DEFAULTS;blocked->CA.ERROR | CA.READ | stop | A supplied status, lookup, or dependent reference needs an exact stored value |

## Date-effective Split Resolution

Use hcmDateEffectiveObjectChanges to resolve the Collective Agreement history definition in current-or-future scope. Return every effective-dated split in order with start and end dates. Require a complete non-overlapping timeline and one selected split start date; display the complete timeline before preview. Retain the selected split, predecessor, successor, and selected split former end date only for the current Data Loader MERGE source.

## hcmDateEffectiveObjectChanges Contract

For every deletion, use HistoryDefClassName oracle.apps.hcm.employment.responsive.publicUiModel.history.definitions.CollectiveAgreementHistoryDef. Resolve PrimaryObjectId from the exact current Collective Agreement target; do not persist or hard-code a record-specific ID. Pass the selected split EffectiveStartDate as the effective context and return the complete ordered timeline for preview and verification.

## Read-only History Service Boundary

hcmDateEffectiveObjectChanges is used only to read split history and verify the resulting timeline. It must not be used to submit delete, update, or date-effective mutation operations.
