# Reference Lookups

Execute workbook reference resolution through the parent converter and its maintained resolver catalog on the selected target. Inherit its exact-match, pagination, and ambiguity policies from the linked resource. Do not copy endpoint mappings or use database results for import mappings. The separate listing route is declared in SKILL.md and uses core/fusion-api/rest-api-client/scripts/fusion_rest_client.py directly, following the pagination and response-validation instructions in SKILL.md.

Parent contract: [Reference Lookups](../../../../benefits-configuration/benefits-eligibility/eligibility-profiles/ora-resource/ora_reference_lookups.md). Load it for this node; the child overrides above take precedence.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OM_ELIG.LOOKUPS | step | 3 | reference_lookup | resolved->OM_ELIG.DESIGN;blocked->OM_ELIG.FAILED | OM_ELIG.DEPENDENCIES | stop | During preparation; use already validated mappings for an immutable approved package. |

Before approved creation, check all pages of eligibilityProfilesLOV across usages and types for matching names. This GET preflight is required before the first import write; failures stop execution. Visible active scope is not proof of enterprise-wide uniqueness; retain Fusion final validation.
