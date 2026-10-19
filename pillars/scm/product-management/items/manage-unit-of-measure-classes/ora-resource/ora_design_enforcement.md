# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Check for probable spelling errors | Before semantic assessment, compare the requested ClassCode and ClassName with the approved design vocabulary, supplied project design values, and controlled common UOM-class vocabulary. Never silently change the supplied values. |
| 2 | Assess the semantic role of the requested class | Use the user-provided class and base-UOM labels to confirm that the class is a dimension/grouping and not an individual unit. |
| 3 | Check existing class identity | Run the exact ClassCode lookup only after the spelling and semantic assessments pass. |
| 4 | Evaluate duplicate result | Block a create when the requested class code already exists. |

## Probable Typo Detection

Normalize labels by trimming whitespace, uppercasing, and ignoring spaces,
hyphens, underscores, and punctuation. Compare the normalized ClassCode and
ClassName separately against the candidate vocabulary; retain the original
user input for all reporting.

The candidate vocabulary is limited to, in this priority order:

1. Exact class labels in the approved project design and supplied source data.
2. Current live UOM class names returned by read-only lookup or baseline export.
3. Controlled common UOM-class labels: `QUANTITY`, `LENGTH`, `AREA`, `VOLUME`,
   `WEIGHT`, `TIME`, `TEMPERATURE`, `PRESSURE`, `ENERGY`, `POWER`, and `COUNT`.

For an input containing at least five letters, flag a probable typo only when
exactly one candidate has the smallest case-insensitive Damerau-Levenshtein
distance of at most 2 and every other candidate is at least 2 edits farther
away. Do not use a model-only guess as a candidate and do not treat a code that
is intentionally abbreviated as a typo without a qualifying candidate.

On a qualifying result, stop before lookup, sample generation, preview, or
write. Present the original value, the suggested candidate, and edit distance;
ask the user to confirm or replace the value. For example, flag `QUANITY` as a
probable typo and suggest `QUANTITY` (distance 1). Never substitute the
suggestion automatically, even when ClassCode and ClassName share the same
probable typo.

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A UOM class is being created | Blocking |  | ClassCode or ClassName semantically identifies a single UOM, is the same as the BaseUnitOfMeasure after normalization, or is merely a decorated form of that base unit. Normalize by ignoring case, spaces, punctuation, and non-semantic test or numbering decoration. | Provide a broader measurable dimension or grouping for ClassCode and ClassName. Do not infer or default it. | Yes |
| A UOM class is being created | Blocking |  | The supplied labels cannot be determined to represent a class/dimension rather than an individual UOM. | Ask the user to state the intended class/dimension and resubmit the values. | Yes |
| A UOM class is being created | Blocking | check_probable_typo | ClassCode or ClassName has one uniquely high-confidence spelling candidate. | Present the candidate and require the user to confirm or replace the supplied value before continuing. Never auto-correct. | Yes |
| A UOM class is being created | Blocking | find_uom_class_by_exact_code | The exact requested ClassCode already exists. | Reuse or explicitly update the existing class through a separately approved update workflow. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| check_probable_typo | Before semantic assessment and every creation preview | Original ClassCode/ClassName, candidate vocabulary, closest candidate, distance, and separation from second-best candidate | This file |
| find_uom_class_by_exact_code | Before UOM-class creation preview | Existing class code, ID, name, description, and base-UOM attributes | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| UMC.CHECK_PROBABLE_TYPO | decision | 2 | design_enforcement | clear->UMC.ASSESS_CLASS_SEMANTICS;candidate->UMC.HANDLE_ISSUE | UMC.VALIDATE | stop | Creation after input shape validation and before any live lookup or preview |
| UMC.ASSESS_CLASS_SEMANTICS | decision | 3 | design_enforcement | class_category->UMC.FIND_EXISTING;individual_uom->UMC.HANDLE_ISSUE;uncertain->UMC.HANDLE_ISSUE | UMC.CHECK_PROBABLE_TYPO | stop | Creation after probable-typo check |
| UMC.ENFORCE | decision | 5 | design_enforcement | create_allowed->UMC.DONE;existing->UMC.HANDLE_ISSUE | UMC.FIND_EXISTING | stop | Creation after spelling, semantic, and exact class-code checks |
