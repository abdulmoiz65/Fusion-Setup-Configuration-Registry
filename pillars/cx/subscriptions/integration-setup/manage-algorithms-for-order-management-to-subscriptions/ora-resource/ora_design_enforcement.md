# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm mapping evidence | Use the validated companion assessment to determine the mapping outcome and whether an Algorithm is needed |
| 2 | Resolve Service Mapping prerequisites | Return a mapping gap, metadata blocker, or incompatibility to the Service Mapping workflow. A complete exact Entities/Sources/Services UI plan may support an approval-ready provisional draft. When the user explicitly requests code before EFF technical identifiers are known, return only a labelled placeholder-only source draft; neither path claims the mapping is applied or validated |
| 3 | Select the safe version | Edit the latest nonprotected active version; if none exists, create the next unused numeric version with ActiveFlag Y |
| 4 | Produce an inline reviewable draft | Present the target, proposed declarative action, OSSTransactions-first chain, `ZeroOrOne` cardinalities, joins, blank and overwrite behavior, affected mapping assessment, and preservation of the baseline RUN_SCRIPT directly in chat. Put Algorithm source in a fenced Groovy code block; do not create a human-readable Markdown draft file |
| 5 | Require explicit approval | Do not create the local artifact until the exact draft is approved |
| 6 | Gate provisional generation | When mapping changes remain planned, display the prescribed warning and obtain a separate explicit continuation before creating a provisional artifact |
| 7 | Preserve nontarget versions | Return a well-formed Algorithm_BO.xml with only the latest active target changed, or one new active version, and compare every nontarget source/output VersionSetupVORow subtree |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every FOM-to-OSS algorithm recommendation or change request | Blocker | resolve_service_mapping_assessment | The validated assessment is absent, incomplete, context-incompatible, or does not cover the requested outcome | Obtain the corrected companion assessment before determining algorithm necessity | Yes |
| The validated assessment evidences an existing direct mapping and the request has no independent documented logic requirement | Decision | resolve_service_mapping_assessment | A draft or artifact would duplicate the evidenced mapping | Return algorithm_not_required with the mapping rationale; do not request approval or create an artifact | No |
| The validated assessment reports a mapping gap, metadata blocker, or type incompatibility | Blocker | resolve_service_mapping_assessment | An Algorithm would be used to bypass unresolved Service Mapping evidence | Return the Service Mapping prerequisite. A mapping gap with a complete exact three-tab UI plan may proceed to an approval-ready provisional declarative draft. When code is explicitly requested before technical EFF details are known, return only a placeholder-only source draft; neither outcome permits artifact generation yet | Yes |
| The validated assessment uses an interface-table correlation for a cross-entity Algorithm change | Blocker | resolve_service_mapping_assessment | The bridge entity, both correlation keys, or intended cardinality are absent, or the draft chooses an arbitrary unmatched or duplicate record | Return the missing bridge contract. Draft only with the XML-evidenced keys, state SDO API assumptions, and retain the baseline terminal action | Yes |
| The validated assessment exposes a direct product-to-fulfillment-line relation | Decision | resolve_service_mapping_assessment | The draft uses that direct key to replace the required OSSTransactions bridge | Preserve the baseline RUN_SCRIPT and use an OSSTransactions-first ConditionalAction. The direct key may be an additional consistency check only | Yes |
| A local artifact would add a conditional or nested action | Decision |  | The eligible active version has no declarative action step | Add a new separate CONDITIONAL_ACTION with the canonical StepSetupVORow, StepSetSetup, and StepActionSetup structure. Preserve RUN_SCRIPT byte-for-byte and assign the next available sequence number | Yes |
| A Custom EFF Algorithm change is proposed | Blocker | resolve_service_mapping_assessment | The EFF entity, owner-key join, provider attribute mapping, source service exposure, writable target, compatible type, or EFF-to-owner-to-OSSTransactions-to-target path is absent | Return the Service Mapping prerequisite. On an explicit request for code, provide only a placeholder-only source draft for the unknown technical details; do not use an Algorithm to manufacture a missing EFF source or target | Yes |
| A custom-indicator EFF Algorithm change is proposed | Blocker | resolve_service_mapping_assessment | The assessment omits any source EFF identifier, owner join, provider mapping, target alias, service permission, type contract, or allowed-value behavior | Return a mapping-information request for the missing values. Do not infer names, permissions, conversion, or an Algorithm assignment. | Yes |
| A Custom EFF declarative action is proposed | Blocker |  | The draft does not prove the current step type, OSSTransactions-first alias, contained set aliases, `ZeroOrOne` cardinalities, join syntax, action container, and per-field null/blank guard | Return the exact missing representation or revise the draft. On an explicit request for code, label unproven names and layout as literal placeholders; do not generate a synthetic import layout, an unguarded assignment, or an artifact | Yes |
| The validated assessment exposes source and target but no direct assignment and an Algorithm change is proposed | Decision | resolve_service_mapping_assessment | The request lacks a confirmed source or target, expected outcome, or target scope | Draft the preferred declarative action from the validated context, preserve the baseline RUN_SCRIPT, state cardinality and null/blank behavior, and require approval before creating an artifact | Yes |
| A primary/fallback Algorithm rule is proposed | Blocker | resolve_service_mapping_assessment | The assessment does not evidence the two source aliases, primary absence predicate, target overwrite behavior, or deterministic cardinality/selection rule | Return the Service Mapping prerequisite. Do not write executable fallback logic that assumes a first record, implicit aggregation, or string blank semantics for a non-string value. | Yes |
| The selected baseline RUN_SCRIPT has an established downstream terminal action | Blocker |  | The draft removes or reorders that action without explicitly stating the reason and obtaining approval | Keep the baseline RUN_SCRIPT unchanged and add the approved declarative action separately unless its replacement is explicitly drafted and approved | Yes |
| A target version is selected for a reviewable draft or local artifact | Blocker |  | The target is not the latest nonprotected active version, a generated version is not the next unused numeric value with ActiveFlag Y, or the output changes a nonselected version | Edit the latest active target, or create only the next active version when no target exists | Yes |
| A published or historical version contains a useful Custom EFF action | Blocker |  | The draft copies business content, aliases, action text, IDs, or version values from it | Use it only to understand the evidenced representation | Yes |
| An artifact or archive is prepared | Blocker |  | Approval of the exact completed reviewable draft is absent | Present the draft and wait for explicit approval | No |
| An Algorithm draft is returned | Blocker |  | The reviewable recommendation or source is omitted from chat, the source is not in a fenced Groovy code block, or a human-readable Markdown draft file is created | Return the complete inline draft with selected version, safeguards, and source code; do not create the Markdown draft file | Yes |
| A provisional artifact is prepared after an approved draft | Blocker |  | The required Service Mapping UI plan is not exact and complete, the prescribed warning was not shown, or the user did not separately answer yes to continue | Return the warning and ask whether to continue; do not create Algorithm_BO.xml | No |
| An approved artifact is returned | Blocker |  | The file is not named Algorithm_BO.xml, is malformed, has another algorithm identity or target, changes a nonselected version, changes protected Version 0 or 1 content, generates P state, or its ZIP is not named SubscriptionManagementandOrderManagementIntegration.zip with exactly the byte-identical Algorithm_BO.xml at top level | Correct and validate the local XML and archive, preserving every nontarget version subtree unchanged | Yes |
| A provisional artifact is returned | Blocker |  | The validation result and artifact registry do not record `provisional=true`, the unapplied Service Mapping prerequisite, and the import/runtime-test warning, or the XML contains a non-schema provisional marker | Correct the local metadata and retain the exact supported Algorithm_BO.xml schema; never represent it as ready to import | Yes |
| Every Algorithm request | Blocker |  | The request would import, publish, deploy, or runtime-test Fusion configuration | Return only the validated local Algorithm_BO.xml artifact and, when approved, SubscriptionManagementandOrderManagementIntegration.zip, or a draft | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_service_mapping_assessment | Every FOM-to-OSS algorithm recommendation or change request | Context, source and target evidence, permissions, direct-assignment evidence, metadata status, mapping_status, algorithm_recommendation, assumptions, and prerequisites | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OMSUBALGO.ENFORCE.DESIGN | decision | 4 | design_enforcement | algorithm-not-required->OMSUBALGO.RETURN.NO_CHANGE;draft-ready->OMSUBALGO.APPROVAL.GATE;blocked->OMSUBALGO.RETURN.ISSUES | OMSUBALGO.RESOLVE.DEPENDENCIES | stop | Dependency readiness is satisfied |

## Sources

- User-approved FOM-to-OSS version rule: edit the latest nonprotected active version, or create the next version as active only when none exists.
- User-approved FOM-to-OSS artifact rule: return Algorithm_BO.xml only after explicit approval, preserve all nontarget versions, and never generate P state.
- User-approved FOM-to-OSS provisional rule: after an exact provisional draft is approved, show the Service Mapping warning and obtain a separate explicit continuation before generating a local provisional artifact.
