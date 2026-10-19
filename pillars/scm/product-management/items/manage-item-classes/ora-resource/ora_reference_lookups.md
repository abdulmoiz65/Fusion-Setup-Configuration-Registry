# Manage Item Classes Reference Lookups

The fresh same-target Manage Item Classes task export and the approved Run Book
context are the supported evidence sources for this workflow. These rules do
not authorize an undocumented REST fallback.

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| verify_item_class_package_baseline | Before final-package readiness validation | Fresh same-target task-level FSM export, target and release identity, process status, archive inventory, headers, and fingerprint | Require successful task evidence, expected member hierarchy and headers, unrelated-row preservation, and an unchanged baseline fingerprint | Sanitized baseline and package-shape receipt | Stale, partial, wrong-target, warning, failure, missing member, or ambiguous evidence blocks |
| resolve_parent_item_class | Before CREATE or parent change | Complete current item-class export and supplied ParentItemClassName | Require one exact enabled item-class match and reject self-parenting or a hierarchy cycle | Parent natural key and eligibility receipt | Zero, many, disabled, self, or cyclic match blocks |
| find_item_class_conflict | Before CREATE or material UPDATE | Complete current item-class export and requested class identity and definition | Match ItemClassCode and ItemClassName, then compare parent, type, flags, generation methods, and supported associations | Existing match, conflicting definition, or create-candidacy receipt | Equivalent match requires reuse; conflict, duplicate identity, or incomplete scope blocks |
| resolve_item_class_references | Before packaging explicit associations | Fresh task export and approved Run Book references for lifecycle phases, attachment categories, assignees, entities, groups, and attributes | Require one exact applicable match for every explicit non-inherited reference | Natural keys and eligibility receipts only | Zero, many, inactive, incompatible, or unsupported matches block |
| verify_post_import_item_class | After a successful central Data Loader import | Fresh same-target task-level re-export and requested supported definition | Require one exact class and compare all supported non-inherited requested values and NIR graph rows | Sanitized verification receipt and semantic differences | Zero, many, mismatch, warning, or incomplete export requires reconciliation; do not replay blindly |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Task export | Use a fresh same-target Manage Item Classes export with successful task status as the baseline and reference authority. |
| Broader export container | Accept a broader functional-area or offering export only when the archive is available, every member required by this task completed successfully with no warning or partial rows, every failure is proven outside this task, and target, release, freshness, hierarchy, headers, and fingerprint are verified. Record and disclose the scoped exception. |
| Inherited lifecycle phase or attachment category | Treat it only as inheritance evidence and never copy it into the child-class delta. |
| EGO_ITEM_USER_DEF_ATTRS association | Classify it as unsupported in this package path; its presence in an export is not proof that this workflow may create the association. |
| Unresolved reference | Stop. Do not fuzzy-match, select the first row, invent a physical identifier, or call an undocumented endpoint. |
| Receipt | Record target, release, task code, as-of time, normalized inputs, match counts, natural keys, eligibility, process status, archive fingerprint, and sanitized evidence; exclude credentials, tokens, and sensitive payloads. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MICS.RESOLVE_REFERENCES | step | 20 | reference_lookup | resolved->MICS.CHECK_DEPENDENCIES;blocked->MICS.HANDLE_ERROR;failure->MICS.HANDLE_ERROR | MICS.VALIDATE_INPUT | stop | Resolve every applicable local reference from approved export and Run Book evidence |
