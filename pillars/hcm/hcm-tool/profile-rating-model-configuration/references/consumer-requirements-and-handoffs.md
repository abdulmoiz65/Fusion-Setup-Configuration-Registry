# Consumer Requirements and Handoffs

Use the union of all selected consumer requirements. Do not weaken a rule
because another consumer does not need that component.

| Consumer | Model requirements owned here | Downstream setup not owned here | Required handoff |
|---|---|---|---|
| Profile Management | Header, ordered levels when the content section requires them, descriptions, dates, translations | Profile type, content section, Talent Rating template, person or model-profile association | Intended profile/content usage, saved model identity, association owner, tests and open decisions |
| Performance Management | Whole-number numeric levels with highest number best; review points and contiguous ranges for average, sum, or band calculations; precision and rounding requirements | Performance template section, calculation configuration, and Target Ratings Distribution | Rating use, method, precision, rounding, mapping, section/template owner, target-distribution requirements and tests |
| Talent Review and Succession | Rating categories and any explicitly required potential-assessment review points | Talent Review template, meeting, succession plan, or XY box-chart setup | Category-to-level mapping, analytic/box-chart purpose, owning skill and tests |
| Compensation | Direct per-level distribution minimum and maximum plus distribution threshold | Compensation plan or worksheet configuration | Direct distribution values, threshold, plan owner and validation expectations |
| Skills Center | Numeric levels with strictly increasing whole numbers, highest number best, and values within 1 through 9 | Skill content section and Skills Center associations | Ordered level IDs/values, content-section owner, dependency warning and tests |

## Cross-Consumer Rules

- A rating scale has at least two uniquely coded, uniquely sequenced levels.
- For Performance Management or Skills Center, numeric values are whole
  numbers, strictly increase in level order, and the highest number is best.
- Skills Center values are in the inclusive range 1 through 9. Once skills are
  added to the associated content section, its rating model cannot be changed.
- Average, sum, and band calculations require review points and nonoverlapping,
  contiguous ranges aligned to the declared calculation precision.
- Rating categories are model-owned and must be finalized before Talent Review
  use. Treat a later category change as a new-governance request, not a V1 edit.
- Compensation distributions live on this rating model. Performance target
  distribution is downstream-owned and must not be loaded as a model
  distribution.
- A Skills-Center-only model must not acquire review points, ranges, categories,
  or distributions without another selected consumer requiring them.

## Exact, Close, and Unsuitable

Compare code, name, descriptions, effective dates, languages, ordered levels,
numeric values, review points, ranges, categories, direct distributions, and
all selected-consumer semantics.

| Classification | Meaning | V1 action |
|---|---|---|
| Exact | Every material value and meaning needed by every selected consumer matches | Reuse the model and emit handoffs |
| Close | Identity or most values match, but at least one material value or meaning differs | List differences; propose a new model or separate impact review; never edit |
| Unsuitable | Scale direction, required components, dates, languages, purpose, or population are incompatible | Exclude it and propose a new model |

## Handoff Contract

Produce one handoff per selected consumer containing: request and environment;
approved model code/name and saved identifier when safely exposable; intended
usage; required downstream association; downstream-owned configuration;
calculation or target-distribution requirements; prerequisites; owning skill or
team; acceptance tests; open decisions; and read-back evidence. A handoff is not
authorization to perform the downstream configuration.
