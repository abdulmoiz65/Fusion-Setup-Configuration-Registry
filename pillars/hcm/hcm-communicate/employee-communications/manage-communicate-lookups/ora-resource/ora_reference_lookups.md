# Reference Lookups

Use only the Common Lookup view of `core.fusion-api.apps-common.lookups` for live transport. Do not construct REST URLs, call curl, manage OAuth, use browser automation, or duplicate Common Lookups behavior.

## Ownership Baseline Metadata

| Evidence | Version or Date | Authority | Refresh Rule |
|---|---|---|---|
| Developer-provided HCM Communicate ownership rule | 2026-09-09 | Exact LookupType prefix is sufficient to authorize task reads and supported type/code CRUD | If a requested type matches neither of the two prefixes, block and require refreshed approved evidence; do not infer ownership from ModuleId or exports |

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| classify_communicate_lookup_type | A requested or returned Common Lookup type is evaluated for task ownership | Exact LookupType and approved prefixes ORA_IRC, ORA_HCO | Case-sensitive starts-with match against exactly one listed prefix; % in authoring shorthand means prefix matching and is not part of the LookupType | Owned decision, matched prefix, evidence version, and exact eligible LookupType | Zero matches blocks as an ownership-mapping gap; multiple matches are resolved only when one prefix is a literal longer prefix of another, otherwise block ambiguity |

## Approved LookupType Prefixes

| Prefix | SQL-Style Authoring Shorthand | Scope Decision |
|---|---|---|
| ORA_IRC | ORA_IRC% | HCM Communicate-owned |
| ORA_HCO | ORA_HCO% | HCM Communicate-owned |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| list_communicate_common_lookup_types | A complete HCM Communicate Common Lookup inventory is requested | Common Lookup collection and approved prefix baseline | Delegated Apps Common Lookups Common view | Only documented fields actually returned for each type | Require a complete provider result, de-duplicate by exact LookupType, and retain only types passing classify_communicate_lookup_type; never treat a small export sample as complete | Eligible LookupTypes and returned fields; baseline ownership prefix; module metadata only when independently established by approved evidence | Empty eligible result is valid; incomplete collection, ambiguous identity, or provider failure blocks completeness claims |
| resolve_communicate_common_lookup_type | A particular type, its codes, or a type/code mutation is requested | Exact eligible LookupType or exact proposed type for create | Delegated Apps Common Lookups exact Common type read | Only documented type fields actually returned, including identity, meaning, description, and any protection or seed metadata | Existing read/update/delete requires one exact current match; create requires exact absence; the type must pass the prefix baseline before lookup | Current parent state, absence result, returned mutability/protection evidence, and exact parent identity | No match blocks read/update/delete but permits create candidacy; one match blocks create; many matches or uncertain absence blocks mutation |
| resolve_communicate_lookup_code | Codes are listed or a code read/create/update/delete is requested | Exact current eligible parent, requested code or business meaning, and current provider results | Delegated Apps Common Lookups Common code list and exact-code read | Only documented code fields actually returned, including LookupCode, Meaning, Description, EnabledFlag, StartDate, EndDate, Tag, DisplaySequence, and seed or protection fields when present | List only under the exact parent and de-duplicate by LookupType plus LookupCode; create requires exact code absence; update/delete requires one fresh exact code read | Current code list or exact state, absence result, supported mutable fields, protected fields, and minimal delta basis | No match blocks read/update/delete but permits create candidacy; collision blocks create; many matches, missing exact identity, or uncertain protection blocks mutation |
| read_lookup_code_translations | Translations are explicitly requested for an exact current code | Exact eligible LookupType and exact current LookupCode | Delegated Apps Common Lookups translation list or exact-language read | Only documented translation fields actually returned | Require translations to belong to the exact current type and code; de-duplicate by returned language identity | Read-only translation results | No match is reported as empty; ambiguity or ownership mismatch blocks; never create, update, or delete a translation |
| verify_communicate_lookup_change | One approved type or code mutation has returned | Exact target environment, approved type/code identity, approved delta or delete target, and approval fingerprint | Delegated fresh Apps Common Lookups exact type or code read | Only documented fields actually returned | Create/update must match the approved result and preserve unrequested values; delete must prove the exact resource absent | Verified post-change state, preservation comparison, and sanitized evidence | Missing, mismatched, ambiguous, or uncertain verification blocks completion; do not retry the mutation automatically |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| User describes a business outcome | Resolve candidate types and codes internally from eligible provider results; ask for a technical identifier only when multiple valid matches remain. |
| Comparable HCM Communicate configuration is available | Use it to inform a proposal, but independently validate the target's exact current state and supported fields. |
| Provider omits ModuleId or module display name | Do not infer or display them; the prefix baseline proves task ownership but does not manufacture module metadata. |
| Translation mutation is requested | Return current translations as read-only evidence and explain the limitation. |
| Unsupported operation is requested | Stop at the task boundary; do not substitute FSM, browser automation, direct REST, export/import, or another route. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCL.LIST_TYPES | decision | 2 | reference_lookup | complete->CCL.CLASSIFY_SCOPE;issues->CCL.LOOKUP_ISSUES | CCL.VALIDATE | stop | A complete HCM Communicate Common Lookup inventory is requested |
| CCL.CLASSIFY_SCOPE | decision | 3 | evaluate_result | list_review->CCL.DONE_LIST;exact->CCL.READ_PARENT;blocked->CCL.OWNERSHIP_ISSUES | none | stop | Requested or returned LookupTypes require ownership classification |
| CCL.READ_PARENT | decision | 4 | reference_lookup | parent_review->CCL.DONE_PARENT;codes->CCL.READ_CODE;translations->CCL.READ_CODE;create_type->CCL.ENFORCE;update_type->CCL.ENFORCE;delete_type->CCL.ENFORCE;create_code->CCL.READ_CODE;update_code->CCL.READ_CODE;delete_code->CCL.READ_CODE;issues->CCL.LOOKUP_ISSUES | CCL.CLASSIFY_SCOPE | stop | An exact eligible Common Lookup type must be read or checked for absence |
| CCL.READ_CODE | decision | 5 | reference_lookup | reviewed->CCL.DONE_CODES;translations->CCL.READ_TRANSLATIONS;create->CCL.ENFORCE;update->CCL.ENFORCE;delete->CCL.ENFORCE;issues->CCL.LOOKUP_ISSUES | CCL.READ_PARENT | stop | Codes are listed, read, translated, or prepared for mutation |
| CCL.READ_TRANSLATIONS | decision | 7 | reference_lookup | reviewed->CCL.DONE_TRANSLATIONS;issues->CCL.LOOKUP_ISSUES | CCL.READ_CODE | stop | Read-only translations are requested |
| CCL.VERIFY_RESOURCE | decision | 9 | reference_lookup | verified->CCL.DONE_CHANGE;mismatch->CCL.POST_CHANGE_ISSUES;uncertain->CCL.POST_CHANGE_ISSUES | CCL.VALIDATE | stop | A delegated type or code mutation requires fresh verification |
