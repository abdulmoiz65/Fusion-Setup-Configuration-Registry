# Service Mapping Describe and Source Registry

Run source lookup only after mandatory preflight passes. Use the Input Type 1-5 classification from the primary Manage Algorithms Use-Case Resolution reference to decide lookup scope: Type 1 verifies the stated source against the current export; Type 2 describes only the stated source object when the attribute is unclear or missing; Type 3 scans all exposed entities and then describes every relevant source object for the objectless attribute; Type 4 requires broad source discovery and returns candidates to the primary workflow for target resolution; Type 5 with no source object first uses the Subscription general reference, then current official Oracle documentation or web sources only if needed, to decide which source-object families need environment describe. Do not use describe output to bypass implementer confirmation.

## Read-Only Describe Coverage

| Service Mapping source | Describe URI | Use |
|---|---|---|
| `PricingSubscriptions` | `/crmRestApi/resources/11.13.18.05/subscriptions/describe` | Subscription source attributes |
| `PricingProducts` | `/crmRestApi/resources/11.13.18.05/subscriptionProducts/describe` | Product source attributes |
| `PricingBillLines` | `/crmRestApi/resources/11.13.18.05/subscriptionProducts/describe?partialDescription=billLines` | Bill-line source attributes |
| `PricingCharges` | `/crmRestApi/resources/11.13.18.05/subscriptionProducts/describe?partialDescription=charges` | Charge source attributes |
| `PricingARAssociations` | `/crmRestApi/resources/11.13.18.05/subscriptionProducts/describe?partialDescription=coveredLevels` | Product-association source attributes |

## Candidate Rules

When the attached XML does not expose the requested attribute but the business requirement identifies an object, use only that object's describe URI. Filter its returned attribute names using the business label, inspect type and queryability, and return exact or semantically close candidates with a compatible Service Mapping type. First report relevant existing export attributes, then report only the missing items and their describe candidates. Ask the implementer whether each candidate is intended. The implementer may select a candidate, provide an exact source, or explicitly accept one named recommended default candidate; a generic assumption is not a default. For a String, Number, Date, or Boolean candidate, recommend the matching Service Mapping type and pass the described type to the primary algorithm workflow for omitted-target DFF selection. For target-family guidance, map string/varchar/character/display identifiers/codes/Boolean-as-code to character DFF slots, date/datetime to date DFF slots, and number/integer/long/decimal/numeric identifiers to number DFF slots. Do not classify a source as numeric only because its name ends in `Id`; use a numeric DFF family only when describe or the current XML confirms a numeric source type. For a complex value, require a queryable scalar child attribute. Do not treat describe output as evidence that the attribute is already exposed, accessible, or published; if describe cannot run because of runtime connection, OAuth/authentication, privileges, transport, or endpoint availability, stop and ask whether to resolve the runtime environment connection and rerun describe or proceed only with named unconfirmed assumptions for review. If describe runs but no viable candidate exists, stop and request the source from the implementer.

When the same label or a semantically equivalent label appears in more than one described source family, do not collapse the candidates into a single alias. Apply a functional-owner tie-breaker: the explicitly requested source object wins; otherwise recommend the family that owns the business concept and show any copied, denormalized, or convenience candidates as alternatives. If accepting the functional owner means the primary algorithm must use a `ZeroOrOne` alias, pass that cardinality risk back in the source-resolution record so Groovy uses `?.` on every direct dereference, including guarded blocks and `ARInterface.insert` values. If a guard is used, later reuse must be through a local variable assigned from a null-safe expression, not through `<alias>.<attribute>`. Do not choose a required or primary object solely because it avoids optional-cardinality handling. Use examples only to illustrate this rule; do not hardcode object or attribute choices.

When the business requirement gives an attribute or business term without a source object, do not choose `Subscription`, `Products`, `BillLines`, `Charges`, `ProductAssociations`, or any other entity by default. First scan all exposed attributes in the current Service Mapping XML for exact and semantic matches. Then run the permitted describe checks for every relevant source object whose business area might fit the term. Use the public Subscription Management guide only to interpret the business term and explain why a described candidate fits; it is not confirmation that the attribute exists in the current source object or is exposed. Return all viable described candidates and require the implementer to select one, provide exact names, or explicitly accept one named recommended default. If describe cannot run, report that describe is not working and ask whether to fix the runtime environment connection and rerun describe or proceed only with named unconfirmed assumptions for review. If describe runs but finds no viable scalar candidate, or returns ambiguous candidates without a clear implementer decision, stop.

For Type 5 use cases with no source object, the object search must start from the generic Subscription reference. If that reference does not identify a likely object and attribute, use current official Oracle documentation or web sources for discovery only, then describe the relevant environment object families. Based on business fit, use this coverage: `PricingSubscriptions` for subscriptions, `PricingProducts` for SubscriptionProducts, `PricingBillLines` for billLines, `PricingCharges` for charges, and `PricingARAssociations` with `coveredLevels` for ProductAssociations. If the analysis fits multiple families, describe all of them and return candidates grouped by object-fit reasoning, attribute name, type, queryability, and mapping implication. Do not collapse ProductAssociations into products; treat coveredLevels as the ProductAssociations describe path.

## REST Operation Boundary

The only permitted REST read is the listed `/describe` request. Do not use general resource GET requests, create, POST, invoke actions, PUT, PATCH, or DELETE. Describe is advisory only and cannot create or modify configuration.

## Describe Runtime Failure Gate

If a permitted describe URI fails because the runtime environment connection, OAuth/authentication, privileges, transport, or endpoint availability is not working, stop the source-resolution flow. Do not go with assumptions automatically and do not treat general references, official documentation, web results, or cached chat knowledge as a substitute for describe. Report the failed describe family or URI, classify the failure category when possible, and ask the implementer to choose one of these paths:

- Resolve the runtime environment connection and rerun describe.
- Continue only with named, unconfirmed assumptions for review.

The second path can produce a reviewable recommendation only; it does not create a describe-confirmed source and does not bypass current XML preflight, source-resolution records, service access, publication prerequisites, deployed DFF/context confirmation, Groovy approval, or XML approval.

## Object Selection from the Requirement

| Business object stated in the request | Describe source to use |
|---|---|
| Subscription | `PricingSubscriptions` / subscriptions |
| Subscription product or product | `PricingProducts` / subscription products |
| Billing data or bill line | `PricingBillLines` / subscription products / bill lines |
| Charge | `PricingCharges` / subscription products / charges |
| Product association or covered level | `PricingARAssociations` / subscription products / covered levels |
| Attribute stated without object | Scan all exposed Service Mapping entities, then describe every relevant source object above before recommending an object |

## Task Node

| Rule ID | Node Type | Sequence | Action Type | Transition | Applies When |
|---|---|---:|---|---|---|
| SVC_AR_DESCRIBE_ATTRIBUTES | step | 2 | reference_lookup | confirmed->SVC_AR_CHECK_DEPENDENCIES;unavailable->SVC_AR_BLOCKED | Existing mapping does not identify the requested source, or a source attribute is stated without an object |
