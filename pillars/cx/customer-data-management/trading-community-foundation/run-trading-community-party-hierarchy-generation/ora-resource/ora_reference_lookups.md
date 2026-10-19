# Reference Lookups

## Official Oracle Documentation

| Source | Oracle URL | What It Confirms | Evidence Boundary |
|---|---|---|---|
| Party Hierarchy Generation | https://docs.oracle.com/en/cloud/saas/sales/fauss/party-hierarchy-generation.html | Four business parameters, hierarchy-type labels, Incremental and Force labels, documented defaults, lookup names, roles, privileges, and on-demand usage | Does not publish argument positions, parameter types, hierarchy-type or flattening-method transport codes, compatibility behavior, or a golden request |
| Scheduled Processes for Analytics | https://docs.oracle.com/en/cloud/saas/sales/facaa/scheduled-processes-for-analytics.html#s20074846 | Maps the FSM task to Party Hierarchy Generation and the Flatten Party Hierarchy Rows and Columns description | Does not publish the executable ESS request contract |
| Scheduler request POST | https://docs.oracle.com/en/cloud/saas/applications-common/25d/farca/op-ess-rest-scheduler-v1-requests-post.html | Generic Scheduler request envelope | Does not identify this job or its positional parameters |
| How You Manage Hierarchies | https://docs.oracle.com/en/cloud/saas/customer-data-management/faudm/how-you-manage-hierarchies.html | Predefined tree-structure codes HZ_CUSTOMER_HIERARCHY, HZ_DNB_HIERARCHY, and HZ_PARTY_HIERARCHY | Does not list the Partner hierarchy analytics structure or ESS positional contract |
| ZCA_BI_PARTNER_HIERARCHIES_V | https://docs.oracle.com/en/cloud/saas/sales/oedms/zcabipartnerhierarchiesv-3005.html | Uses HZ_PARTNER_HIERARCHY as the Partner hierarchy TREE_STRUCTURE_CODE | Does not document the scheduled-process request envelope |

## Developer-Provided Contract Facts

| Fact | Value | Runtime Use | Remaining Boundary |
|---|---|---|---|
| Scheduler application | CrmEss | Use exactly in the ESS request envelope | Fixed task identity |
| Job definition | JobDefinition://oracle/apps/ess/cdm/foundation/parties/HzPartyHierarchyFlattenedDataGenJob | Use exactly as jobDefinitionId in the ESS request envelope | Fixed task identity |
| Argument order | submit.argument1 hierarchy type; submit.argument2 hierarchy name; submit.argument3 user-supplied Version value; submit.argument4 flattening method | Build requestParameters in this exact order | Fixed positional contract; do not expose the internal argument3 terminology during user intake |
| Parameter type | STRING for all four arguments | Follow the existing executable ESS skill convention and shared ESS client contract | Developer explicitly authorized deriving this task payload from existing skills |
| Null position | Keep the parameter object and omit value | Never send JSON null, empty string, or #NULL | Applies to omitted hierarchy name or Version value |
| Customer Hierarchy | HZ_CUSTOMER_HIERARCHY | Use as argument1 for canonical CUSTOMER | Complete mapping |
| Duns and Bradstreet Hierarchy | HZ_DNB_HIERARCHY | Use as argument1 for canonical DUNS_AND_BRADSTREET | Complete mapping |
| Partner Hierarchy | HZ_PARTNER_HIERARCHY | Use as argument1 for canonical PARTNER | Complete mapping |
| Trading Community Party Hierarchy | HZ_PARTY_HIERARCHY | Use as argument1 for canonical TRADING_COMMUNITY_PARTY | Complete mapping |
| Hierarchy name | Preserve exact user-supplied text, or null when omitted | Use as argument2 without an LOV lookup | Broad scope still requires an explicit scope selection, which is then included in the consolidated submission approval |
| Hierarchy version | Use the exact user-supplied Version value, or omit value when no version is selected | Use unchanged as submit.argument3 | Do not ask the user for a separate internal identifier |
| Incremental Flattening | INCREMENTAL_FLATTENING | Use as argument4 for canonical INCREMENTAL | Complete mapping |
| Force Flattening | FORCE_FLATTENING | Use as argument4 for canonical FORCE | Complete mapping; force intent and approval remain mandatory |
| Successful execution evidence | Succeeded | Confirms one UI-submitted Customer and Incremental run completed successfully | Establishes the shared job identity and positional request contract; per-combination runtime success still depends on Fusion validation |
| Submission safety | retries 0; one POST; separate requestId polling; no automatic resubmission | Follow the established executable ESS skill pattern | Does not depend on undocumented Scheduler compatibility behavior |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A hierarchy type or flattening method outside the documented option set is selected | Reject it during input validation; do not construct or submit a payload. |
| Hierarchy name or version is absent | Transport null for the omitted value and disclose broad scope when the hierarchy name is null. |
| Hierarchy name is supplied | Preserve the exact user-supplied text as argument2 and do not perform an LOV lookup. |
| Hierarchy version is supplied | Preserve the exact supplied value and pass it unchanged as argument3; do not request another identifier. |
| 401 or 403 | Classify authentication or authorization separately; never report the LOV or hierarchy as absent. |
| No match or multiple matches | Stop and request correction or source-backed disambiguation. |
