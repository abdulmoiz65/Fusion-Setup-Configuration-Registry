# Time Categories Requirement Intake

## Purpose

Turn one plain-language Time and Labor requirement into a bounded Time Category decision before any setup-data package is prepared.

## Requirement Classification

| Result | Use When | Next Action |
|---|---|---|
| `time_category_required` | The requirement identifies a population of time entries that must be included, excluded, filtered, transferred, displayed, totaled, attested, or evaluated by a category. | Derive the population and business purpose, then search existing categories. |
| `time_category_not_required` | The requirement concerns a Time and Labor object without a category-based population decision. | Explain that no Time Category will be created or updated and route only when another task is explicitly requested. |
| `clarification_required` | The requirement cannot reliably establish whether a category is needed. | Ask the user whether the requested outcome depends on selecting a population of time entries. |

## Derived Requirement Record

Create a structured record from the user wording. Preserve the original requirement and record only values that are explicit or confirmed.

| Field | Required Before Existing-Category Search | Notes |
|---|---|---|
| Source requirement | Yes | Retain the original plain-language request. |
| Category need | Yes | Use one classification from Requirement Classification. |
| Intended time-entry population | Yes when category is required | State which entries must be included or excluded. |
| Business purpose | Yes when category is required | State why the population is needed. |
| Candidate business terms | Yes when category is required | Include supplied names, attributes, values, and outcome terms. |
| Unit of measure | No | Retain when supplied; otherwise mark as unresolved rather than defaulting it for requirement interpretation. |
| Condition logic | No | Retain explicit AND, OR, grouping, exclusion, or inclusion wording. |

## Clarification Rules

Ask for clarification before proposing or adding conditions when one or more of these are unresolved: the included or excluded entries, time attribute, attribute value, unit of measure, operator or grouping logic, or intended business purpose. Ask only for the missing business information; do not request technical identifiers, CSV columns, or API details.

After clarification, add only the user-confirmed attributes, values, and logic to the proposed Time Category definition. Never infer an attribute value or condition operator from a similarly named existing category.
