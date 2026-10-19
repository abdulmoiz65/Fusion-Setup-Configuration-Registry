# Wage Basis Rules Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Core environment/security context | Verify selected alias, authenticated target identity and required read/HDL privileges through core; do not infer classification from hostname |
| 2 | Applicable business date | Establish the explicit date required by a date-sensitive lookup before that lookup; never use an implicit current date |
| 3 | LDG | Resolve the selected legislative scope or retrieve eligible LDG choices |
| 4 | Component group | Use the resolved LDG and legislation to resolve the group or present current group choices |
| 5 | Reference level | Use the resolved group to obtain current reference definitions; No References follows its metadata-backed skip path |
| 6 | Context values | For active references, resolve each parent before its dependent value and preserve separate write/read representations |
| 7 | Classifications | Resolve primary for LDG and applicable date, then resolve secondary selection or explicit all/none intent under that primary |
| 8 | Components | Resolve eligible components using current group, LDG and reference definitions; preserve each requested inclusion decision |
| 9 | Complete prior state | Only after identity choices are complete, prove Create absence or exact target/history and preserve unaffected sibling baseline |
| 10 | Native contract | Core supplies current template/schema validation and final immutable archive to Task Hook; discovery never reaches this stage |

This order expresses dependencies, not a mandatory questionnaire. Ingest a
complete prompt together and validate its supplied values without re-prompting.
LDG/group/reference discovery can proceed without a classification date when
its own binds are ready; classification calls cannot. Independent questions
may be batched. Never require downstream selections before retrieving the
choices from which the user must select.

For Create, use the explicit start date applicable to each intended rule. For
Update, use the requested boundary for changed-period classification eligibility.
For an existing-rule review or Correct, use the explicit as-of date or the
unambiguously selected existing version's start. If neither is available, ask
for a business date before a date-sensitive lookup. A date used to discover a
whole-history Delete target is only a lookup date, never a deletion boundary.
No selection is valid merely because it was eligible at a different date.

For maintenance, the order is not a requirement to rebuild a selected rule
from Create choices. If the history resolver's complete identity is already
established in this operation, its all-history read can precede missing
change-specific input. It does not need the new inclusion decision or Update
boundary as query inputs. Ask for a date before a classification lookup only
when that lookup is actually required; use the chosen history version for
Correct's date scope. Revalidate applicable eligibility at an Update boundary
without turning the rule's existing classification into a new selection.
Group, reference and context discovery remains applicable where needed to
complete identity or establish native helper-key mappings. A missing mapping
is a technical blocker, not a reason to repeat known business answers.

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| WBR-DATE | Applicable business date | Conditional | Before primary/secondary classification lookup | Verify | Explicit current-request business date or unambiguously resolved existing version from read_wbr_history | find_wbr_classifications | Eligibility is date-sensitive | Supply only the missing or ambiguous date; no implicit today | Full-year applicable date and its operation role |
| WBR-LDG | Legislative scope | Yes | All fresh requests | Lookup | Fusion LDG LOV | find_wbr_ldg | Names/IDs are environment-specific | Choose one current LDG | LDG name, ID, legislation |
| WBR-GROUP | Component group | Yes | Fresh discovery/Create | Lookup | Fusion group LOV | find_wbr_group | Defines eligible reference levels/components | Choose one current group | Group identity |
| WBR-REFERENCE | Reference level | Yes | Fresh discovery/Create | Lookup | Fusion context metadata | find_wbr_reference_level | Defines slot order | Choose a reference level | Six context definitions |
| WBR-CONTEXT | Context values | Conditional | Active context slots after their parent selections resolve | Lookup | Fusion cascading context LOVs and established HDL helper-key mapping | find_wbr_context_values | REST stored code is not HDL authoring key | Supply only missing business reference values; skip inactive levels for No References | HDL keys, stored values, labels |
| WBR-CLASS | Classifications | Yes | Fresh identity resolution after LDG and applicable date resolve | Lookup | Fusion classification LOVs | find_wbr_classifications | Secondary eligibility depends on primary and date | Select current primary and explicit secondary scope using the input secondary-state contract | Classification labels, foreign keys, secondary mode and date scope |
| WBR-COMPONENT | Payroll components | Yes | Fresh identity resolution | Lookup | Fusion context-scoped components | find_wbr_components | Each component is an independent rule | Create selects requested rows; maintenance identifies one existing component rule, then collects only its applicable change inputs | Component labels and foreign keys |
| WBR-HISTORY | Complete prior state | Yes | Mutation or historical read | Verify | Fusion all-history plus ISO physical reads | read_wbr_history | MERGE may update an existing row; DELETE may remove every version | Resolve conflicts or clarify the exact logical target | Complete baseline and target identity |
| WBR-SCHEMA | Native BO contract | Yes | Task Hook mutation validation | Verify | Current core Data Loader validation/template | verify_wbr_hdl_contract | Reject drift and malformed bytes | Rebuild through core if the contract changed | Exact metadata, allowed fields, artifact digest |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| LOOKUP_READY | Core preflight and the next discovery resolver's parent binds are ready; later user selections may be missing | Only that resolver and the declared prerequisite-resolution reads in WBR.RESOLVE_REFERENCES; no archive or approval |
| READY | All applicable dependencies resolve uniquely and current core preflight passed | Declared GETs and subsequent validation only; no implicit write |
| NEEDS_INPUT | Missing meaningful business selection | Offer current eligible labels and ask only the missing question |
| NOT_FOUND or AMBIGUOUS | Required identity absent or nonunique | No dependent write and no substituted record |
| CATALOG_MISMATCH | Contract/alias/metadata/pagination conflict | Stop; no exploratory fallback endpoint |
| CONTEXT_MAPPING_UNRESOLVED | Valid live context lacks a proven native helper key | Read can continue with established REST identity; native preparation is blocked |

## Selection Changes and Revalidation

Keep user-supplied business intent as candidates, but invalidate affected
resolved evidence, displayed choices and page selections immediately. Re-resolve
those candidates in the new scope; do not silently keep an old key, substitute
a similarly named record, or erase unrelated accepted answers. If a candidate
is no longer eligible, explain which earlier change affected it and ask only
for its replacement. Invalidation propagates to every downstream consumer.

| Changed Selection | Evidence to Invalidate | What Can Be Retained |
|---|---|---|
| Environment | All Fusion identities, eligibility, histories, displayed lists and target verification; core must verify the new target | Explicit business intent only, for fresh resolution; no old token, approval or cross-environment ID |
| LDG | Group, reference definitions, context mappings, classifications, components and all rule baselines | Explicit dates and candidate business labels, not their old resolved keys |
| Component group | Reference level, context definitions/values, eligible component list and rule baselines | LDG/date and classification evidence still valid under the unchanged LDG/date; candidate reference and component labels must be re-resolved |
| Reference level | All context-slot evidence, eligible component list and rule baselines | LDG/group/date and independently valid classifications; context labels are candidates only and must not be shifted between slots |
| A context value | That slot's mapping, every descendant context choice and exact rule baselines | Earlier parent contexts and independent classifications; component LOV evidence can remain when group/LDG/reference definitions are unchanged because its binds use definitions, not jurisdiction values |
| Applicable date | Date-sensitive primary/secondary eligibility, all-secondary membership and dated rule baselines | Explicit classification labels or all/none intent for revalidation; unrelated group/reference/context evidence with unchanged scope |
| Primary classification | Secondary eligibility and selections, including all/none validity, and exact rule baselines | LDG/date/group/reference/context choices and independently eligible components; secondary labels are candidates to validate under the new primary |
| Secondary scope or component selection | Affected logical-rule identity, expected combinations and prior-state checks | Unchanged upstream selections; only explicitly supplied inclusion decisions for the requested components |
| Existing rule or history version | Selected target/version, affected history and sibling baseline, derived native identity dates and expected timeline | Unchanged upstream business scope; a proposed inclusion or Update boundary remains only candidate intent and must be checked against the newly selected target |
| Maintenance operation or requested inclusion | Operation-specific readiness, derived dates, expected effect, prepared artifact and approval | Business identity and still-current history evidence in this operation; never carry whole-history intent from a version-limited or ambiguous request |

A changed request, baseline, template or archive invalidates its prepared
preview and approval and requires fresh validation under core. If an explicit
all selection resolves to changed membership, disclose the changed set and
count before core confirmation; never reuse the old expansion. Reuse business
intent, not old IDs, waivers or artifacts. Core owns later approval-time checks;
do not insert a second approval mechanism or automatic refresh/retry loop.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WBR.RESOLVE_DEPENDENCIES | decision | 2 | resolve_dependency | ready->WBR.RESOLVE_REFERENCES;needs_input->WBR.HANDLE_ERROR;blocked->WBR.HANDLE_ERROR | WBR.VALIDATE_INPUT | stop | Validate core preflight and the next applicable resolver prerequisites; ready includes LOOKUP_READY during discovery, not write readiness; missing user prerequisites return needs_input; the reference node alone performs reads |
