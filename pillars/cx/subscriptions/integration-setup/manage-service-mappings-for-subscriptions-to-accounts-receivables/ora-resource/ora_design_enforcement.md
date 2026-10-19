# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 0 | Mandatory preflight | Validate both current XMLs, algorithm identity, absolute highest version `ActiveFlag=Y`, and Service Mapping `contextName="ARInterface"` |
| 1 | Classify input type | Identify Type 1, 2, 3, 4, or 5 from the primary algorithm Use-Case Resolution reference |
| 2 | Confirm target level | Identify whether the requirement affects an AR invoice header or line attribute |
| 3 | Confirm data model alignment | Match the Subscription custom attribute data type to the Service Mapping attribute data type |
| 4 | Confirm mapping exposure | Add the custom entity attribute with the _Custom suffix, map it to the view object attribute, and set read and write access |
| 5 | Confirm verification path | Specify test subscription data and the expected AR interface-table result before recommending the change |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any companion advisory starts | Error | Current XML preflight | Either XML is missing, algorithm name is wrong, the absolute highest algorithm version is not `ActiveFlag=Y`, or Service Mapping context is not `ARInterface` | Stop and request corrected current exports | No |
| Source recommendation is requested | Error | Input Type 1-5 classifier | Prompt was not classified before source lookup scope was chosen | Classify using the primary algorithm Use-Case Resolution reference | Yes |
| A custom Subscription attribute is used | Error | | The Subscription attribute data type does not match the Service Mapping attribute data type | Align the types before changing the mapping | Yes |
| A custom descriptive-flexfield attribute is added | Error | | The Service Mapping Attribute value lacks the _Custom suffix | Use the documented _Custom suffix | Yes |
| A mapping is proposed | Error | | The source entity, source attribute, target level, or expected AR result is not identified | Request the missing mapping fact | Yes |
| A source attribute is stated without an object | Error | Current source XML and permitted describe results | A source object is recommended without checking all relevant exposed and described candidates | Show the object candidates and require implementer selection or one named recommended default | No |
| Same or similar source label appears in multiple object families | Error | Current source XML, permitted describe results, and business-term fit | The recommended default does not identify the functional owner or silently chooses a copied/denormalized/easier-cardinality candidate | Prefer the explicitly stated object; otherwise recommend the object family that owns the business concept, list alternatives, and require implementer selection when ownership is unclear | No |
| A service attribute is added | Error | | Read and write access is not defined for the selected entity and attribute | Define the required service access before review | Yes |
| A mapping change affects billing output | Warning | | There is no test case that confirms the expected AR interface result | Define positive and negative test cases before implementation | Yes |
| A mapping is ready for use | Error | | New source attributes are not published through Service Mapping | Require Service Mapping publication before returning the mapping result | No |
| A mapping advisory is returned | Error | | The proposed configuration and requested UI steps are only in an artifact | Present the complete proposal and UI steps in chat; retain artifacts only for traceability | Yes |
| A Groovy source is missing from the current export | Error | Matching object describe | No accepted source-resolution decision exists | Show export matches and describe candidates; require implementer selection, exact source, or acceptance of one named default | No |
| Required describe fails at runtime | Error | Describe runtime failure gate | The workflow continues with assumptions without implementer choice | Tell the implementer describe is not working and ask whether to fix the runtime environment connection and rerun describe or proceed only with named unconfirmed assumptions for review | No |
| A named default is requested | Error | Describe result | The default does not identify one returned candidate | Do not treat a generic assumption as a default | No |
| Named assumptions are used | Error | Source-resolution record | An assumption is not tied to a named evidence-backed recommendation and implementer acceptance | Keep it advisory only; do not bypass preflight, source resolution, publication, DFF context, Groovy approval, or XML approval | No |
| Approved local algorithm XML is handed off | Error | Source-resolution record | Service Mapping configuration handoff is absent or lacks the final source-target table | Persist selected sources, aliases, types, access, publication prerequisites, remaining UI configuration, and the final source-target table | No |

## Source Anchors

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/subscription-management/fasmq/create-and-manage-account-receivables-service-mappings.html | Type compatibility, _Custom suffix, entity/view-object mapping, and service-access requirements |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SVC_AR_ENFORCE_DESIGN | step | 3 | design_enforcement | pass->SVC_AR_ADVISORY_GATE;block->SVC_AR_BLOCKED | SVC_AR_CHECK_DEPENDENCIES | stop | A service-mapping advisory is requested |