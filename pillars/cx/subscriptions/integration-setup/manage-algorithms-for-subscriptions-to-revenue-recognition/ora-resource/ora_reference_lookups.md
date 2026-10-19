# RMCS Algorithm Reference Lookups

## Scope and authority

This resource owns lookup mechanics and the preserved physical-documentation ledger. The current user enhancement contract authorizes assisted authoring checkpoints using the request's current supplied files and recorded decisions as local evidence. It does not authorize Fusion writes or equate those inputs to published state. The former incomplete live workflow is retained under Unsupported live contracts, outside the assisted graph. The authoring prompt and explicit authority clarification are sources for this route; sample attachments are not bundled.

## Source catalogue

| Source | Documentation | Reviewed scope and status |
|---|---|---|
| S1 | [Using Subscription Management](https://docs.oracle.com/en/cloud/saas/subscription-management/fasum/using-subscription-management.pdf) | Current unversioned guide; Subscription Pricing and Billing, Integration with Revenue Management, printed pages 27-28. Offering context only. |
| S2 | [Using Revenue Management 26B](https://docs.oracle.com/en/cloud/saas/financials/26b/fafrm/using-revenue-management.pdf) | Supplied target guide; Guidelines for Integrating Revenue Management with Subscription Management, printed page 94. Only Subscription integration scope used. |
| S2C | [Using Revenue Management 26C](https://docs.oracle.com/en/cloud/saas/financials/26c/fafrm/using-revenue-management.pdf) | Newer verified guide; same integration section, printed page 94. Used to refresh S2 integration guidance; no general accounting configuration imported. |
| S4 | [OSS_RMCS_DOC_T](https://docs.oracle.com/en/cloud/saas/sales/oedms/ossrmcsdoct-26506.html) | Current Sales table guide, Primary Key and Columns. Original URL verified via the current Sales table of contents. |
| S5 | [OSS_RMCS_DOC_LINES_T](https://docs.oracle.com/en/cloud/saas/sales/oedms/ossrmcsdoclinest-21926.html) | Current Sales table guide, Columns, including revenue identifiers, pricing, revisions and RMCS attributes. |
| S6 | [OSS_RMCS_DOC_SUB_LINES_T](https://docs.oracle.com/en/cloud/saas/sales/oedms/ossrmcsdocsublinest-11773.html) | Current Sales table guide, Primary Key and Columns. |
| T1 | [VRM_SOURCE_DOCUMENTS 25D](https://docs.oracle.com/en/cloud/saas/financials/25d/oedmf/vrmsourcedocuments-26721.html) | Supplied document table baseline. |
| T1B | [VRM_SOURCE_DOCUMENTS 26B](https://docs.oracle.com/en/cloud/saas/financials/26b/oedmf/vrmsourcedocuments-26541.html) | Newer verified document table. A 26C document-table page was not located; confirm environment release compatibility. |
| T2 | [VRM_SOURCE_DOC_LINES 25D](https://docs.oracle.com/en/cloud/saas/financials/25d/oedmf/vrmsourcedoclines-30660.html#Details) | Supplied line table baseline. |
| T2C | [VRM_SOURCE_DOC_LINES 26C](https://docs.oracle.com/en/cloud/saas/financials/26c/oedmf/vrmsourcedoclines-31165.html) | Newer verified line table; use for current physical column checks while retaining T2 provenance. |
| T3 | [VRM_SOURCE_DOC_SUB_LINES 26A](https://docs.oracle.com/en/cloud/saas/financials/26a/oedmf/vrmsourcedocsublines-19061.html) | Supplied subline table baseline. |
| T3C | [VRM_SOURCE_DOC_SUB_LINES 26C](https://docs.oracle.com/en/cloud/saas/financials/26c/oedmf/vrmsourcedocsublines-19621.html) | Newer verified subline table. Source satisfaction-event columns do not have an evidenced one-to-one target mapping here. |

Public documentation links are authoring references, not live Fusion lookup endpoints. Release compatibility is an unresolved deployment fact, not permission to rewrite customer configuration.

## Data model reference

The tier pairing below is the developer-requested source/target scope. It is not a field-level ETL contract or proof that source and target surrogate IDs retain identical values.

| Tier | Source object and identifiers | Target object and identifiers | Mapping boundary |
|---|---|---|---|
| Header | OSS_RMCS_DOC_T: DOCUMENT_ID primary key; DOC_ID_INT_1 carries the subscription identifier. S4. | VRM_SOURCE_DOCUMENTS: DOCUMENT_ID primary key. T1B. | Confirm business-key translation and runtime alias separately. |
| Line | OSS_RMCS_DOC_LINES_T: DOCUMENT_LINE_ID primary key; DOC_ID_INT_2 identifies its parent document; PRODUCT_ID and CHARGE_ID distinguish product and charge. S5. | VRM_SOURCE_DOC_LINES: DOCUMENT_LINE_ID primary key; DOCUMENT_ID links to the target document. T2C. | Do not infer a source DOCUMENT_ID column or equate a revenue-line ID with a bill-line ID. |
| Subline | OSS_RMCS_DOC_SUB_LINES_T: DOCUMENT_SUB_LINE_ID primary key; DOCUMENT_LINE_ID required. S6. | VRM_SOURCE_DOC_SUB_LINES: DOCUMENT_SUB_LINE_ID primary key; DOCUMENT_LINE_ID and DOCUMENT_ID identify target associations. T3C. | Establish the subline type, relationship and supported transformation before mapping. |

## Source column meanings

| Object | Selected columns | Documented meaning or shape |
|---|---|---|
| OSS_RMCS_DOC_T | DOCUMENT_DATE; DOCUMENT_NUMBER; CURRENCY_CODE; CUST_PO_NUMBER | Subscription start date; subscription number; currency; purchase-order number. S4. |
| OSS_RMCS_DOC_T | CURR_CONVERSION_RATE_TYPE; CURR_CONVERSION_RATE; CURR_CONVERSION_RATE_DATE | Conversion attributes; the date is required for fixed-date conversion. S4. |
| OSS_RMCS_DOC_LINES_T | DOC_LINE_ID_CHAR_1; LINE_NUM; LINE_AMOUNT; UNIT_LIST_PRICE | Revenue-line identifier; product number; bill-line amount total; list price excluding adjustments. S5. |
| OSS_RMCS_DOC_LINES_T | VERSION_FLAG; VERSION_NUMBER; REVISION_INTENT_TYPE_CODE; IMMATERIAL_CHANGE_CODE | Revenue data revision fields, not algorithm-definition version controls. S5. |
| OSS_RMCS_DOC_LINES_T | SRC_ATTRIBUTE_CHAR1 through SRC_ATTRIBUTE_CHAR5 | Documented meanings: charge name, price type, periodicity, external asset key and product PUID. These are not presumed unused slots. S5. |
| OSS_RMCS_DOC_LINES_T | RMCS_ATTRIBUTE_CATEGORY; RMCS_ATTRIBUTE1-3; RMCS_ATTRIBUTE_NUMBER1-3; RMCS_ATTRIBUTE_DATE1-2 | Variable-revenue DFF-related source fields; exact deployed context and target mapping are not provided. S5. |
| OSS_RMCS_DOC_SUB_LINES_T | SATISFACTION_MEASUREMENT_DATE; SATISFACTION_EVENT_QUANTITY; SATISFACTION_EVENT_PERCENT | DATE; NUMBER; NUMBER. Percent supports percentage-based satisfaction. S6. |
| OSS_RMCS_DOC_T; OSS_RMCS_DOC_LINES_T; OSS_RMCS_DOC_SUB_LINES_T | PROCESSED_FLAG | Processing indicator exists; accepted values and an end-to-end success predicate are not specified by these table descriptions. S4-S6. |

## Local Lookups

The user explicitly authorizes the current request's supplied XML files and recorded choices as local authoring evidence. They establish file contents and accepted decisions, not Fusion publication or live state. Require the same fingerprints throughout a checkpoint; reject stale substitutions. This task evaluates already supplied evidence locally and makes no Fusion read. Use the canonical guides linked below; do not reproduce their rule text in a second schema.

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_rmcs_algorithm_contract | Every checkpoint | Current raw `Algorithm_BO.xml`, current mapping XML, business requirement and rule_phase supplied in this request | Apply [input preflight and structural selection](../resources/ora_algorithm_xml_guidance.md#input-preflight); run the existing read-only helper on these exact files and inspect current action bindings when the phase needs them | Fingerprinted preflight evidence; selected highest version; selected action identities and scope map when applicable | Stop with exact missing or mismatched input; ambiguous structures require clarification, never an older version |
| resolve_rmcs_mapping_contract | proposal, approved_change or artifact_result | Same validated input pair and current source-resolution/configuration records, including user decisions and companion findings when needed | Match request identity, fingerprints, requirement and source selections against the [source record](../../manage-service-mappings-for-subscriptions-to-revenue-recognition/resources/ora_service_mapping_guidance.md#source-resolution-record); do not require a new companion call for already resolved evidence or invent business-source records for supported literal/runtime-only operations | Matched source/provider/type/scope evidence; current-file access; accepted choices; separate publication state; unresolved mapping questions | Return missing facts and saved-stage context to the caller; the manifest owns companion routing |
| verify_rmcs_approval_evidence | approved_change or artifact_result | Versioned complete proposal, decision reference, input fingerprints, final handoff and approved destination/change scope | Compare with [approval and local artifact](../resources/ora_algorithm_xml_guidance.md#approval-and-local-artifact); approval must cover this exact proposal and current inputs | Approval evidence, proposal version/fingerprint, exact permitted change scope and destination | Stop for missing, ambiguous, changed or stale approval; no permission inferred from a source-selection decision |
| verify_rmcs_artifact_result | artifact_result only | Supplied original inputs, approved proposal and already-created local output plus redacted comparison record | Apply the canonical XML-guide comparison procedure to the actual output; this resolver reads and compares, never creates a file | Extracted-expression comparison, allowlisted XML changes, output evidence and final handoff linkage | Stop on absent artifact, unsupported structural identity or any unapproved difference; do not claim import validation |

## Lookup execution rules

| Situation | What Happens |
|---|---|
| Local evaluation node reached | Evaluate only local resolver rows applicable to rule_phase. The evaluate_result action is intentional: it does not acquire Fusion data. |
| Mapping evidence is missing | Return the precise question; the primary runbook controls any companion call and subsequent checkpoint invocation. |
| Same source appears in physical documentation and XML | Keep physical meaning separate from runtime provider, access, target mapping and deployed state. |
| Runtime result would require a new live operation | Refuse that operation in this assisted route and retain its missing contract below. |

## Unsupported live contracts

These are preserved blocking gaps for a future separately authorized workflow, not resolvers or prerequisites of this assisted checkpoint graph. No current node may evaluate them as passed or turn them into an execution route.

| Future capability | Missing contract | Required completion evidence |
|---|---|---|
| Fusion algorithm mutation/import | TBD: supported executor, privileges, payload/import format, exact-target approval, verification and recovery | RMCS-specific documented live-operation contract |
| Subscription integration setup verification | TBD: authoritative environment/configuration acquisition | Supported read contract and environment-matched evidence |
| Subscription record eligibility lookup | TBD: linked header/product lifecycle acquisition | Supported identity/status read contract |
| Integration process execution and polling | TBD: job/operation identity, submission, retry and timeout contract | Separate approved implementation workflow |
| Transfer-result verification | TBD: correlated source/target outcomes, errors and success predicate | Supported result acquisition and correlation contract |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RMCSALG.RESOLVE_EVIDENCE | step | 20 | evaluate_result | resolved->RMCSALG.CHECK_DEPENDENCIES;unresolved->RMCSALG.REPORT_ISSUES | RMCSALG.VALIDATE_INPUT | stop | Evaluate the phase-applicable Local Lookups against the authoritative current request evidence; never call Fusion or another task. |
