# Client-Side Input Validation

Use this guidance for `Manage Document Styles`. Let the selected `purchasingDocumentStyles` business-object configuration determine the operation and the fields in scope. Validate only values supplied in that configuration; do not retrieve existing styles, line types, identifiers, or list-of-values data from Fusion. Oracle documents `purchasingDocumentStyles` as the document-style REST resource and describes its style, status, purchase-basis, and line-type attributes. This resource does not authorize a REST call or server-side validation.

Sources: [Implement Procurement](https://docs.oracle.com/en/cloud/saas/procurement/26c/oapro/implement-procurement.html#s20067550) and [Purchasing Document Styles REST API](https://docs.oracle.com/en/cloud/saas/procurement/26c/fapra/api-purchasing-document-styles.html).

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Style identity | StyleName | Stop client-side preparation | Provide a nonblank style name when the selected configuration includes style identity | StyleName is supplied | |
| Purchase basis | Purchase Basis with one or more comma-separated values of Quantity or Amount, or at least one supplied purchase-basis enabled flag set to true | Stop client-side preparation | Provide supported Purchase Basis values or set at least one enabled flag to true | Purchase-basis fields are supplied | |
| Specified line types | Line Type input | Stop client-side preparation | Provide one or more nonblank Line Type inputs when LineTypeAllowed is Specified | LineTypeAllowed is Specified | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| StyleName is a string of at most 240 characters | Reject a blank or oversized value | StyleName is supplied | |
| StyleDescription is a string of at most 240 characters | Reject an oversized value | StyleDescription is supplied | |
| StatusCode is a string of at most 30 characters | Reject an oversized value | StatusCode is supplied | |
| Purchase Basis value | Accept comma-separated Quantity and Amount values only | Purchase Basis is supplied | |
| Purchase-basis enabled flags | Require boolean true or false values when either flag is supplied; reject the record when both QuantityPurchaseBasisEnabledFlag and AmountPurchaseBasisEnabledFlag are false after local defaulting | Purchase-basis enabled flags are supplied | |
| LineTypeAllowed and Line Type input | Reject a supplied Line Type when LineTypeAllowed is All; reject a Specified record with no Line Type input | LineTypeAllowed is supplied | |
| LineTypeCode derivation input | Require every supplied Line Type input to be nonblank before deriving LineTypeCode | A Line Type input is supplied | |
| Existing-style and line-type existence | Do not perform a client-side duplicate, identifier, or membership lookup; retain supplied values for the approved downstream process | Identity or line-type values are supplied | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Purchase Basis is Quantity | Local input is complete for QuantityPurchaseBasisEnabledFlag defaulting | Apply the documented local default | |
| Purchase Basis is Amount | Local input is complete for AmountPurchaseBasisEnabledFlag defaulting | Apply the documented local default | |
| A Line Type input is supplied | Local input is complete for LineTypeCode derivation | Copy the supplied Line Type into LineTypeCode without lookup | |
| A server-side identity, duplicate, or list-of-values check would be needed | The check is outside this client-side guidance | Stop rather than perform a live lookup or server call | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MDS.VALIDATE_INPUT | step | 10 | validate_input | valid->MDS.APPLY_DEFAULTS;invalid->RETURN_ISSUES | none | stop | A Manage Document Styles business-object configuration is supplied for local preparation |
