# Design Enforcement

Apply the parent design review to the selected Opportunity Marketplace requirements. Preserve row-specific findings and missing expected-versus-actual evidence. Require the correct product usage without treating all parent criteria as suitable for every Marketplace use case. A successful import does not prove business eligibility outcomes.

Parent contract: [Design Enforcement](../../../../benefits-configuration/benefits-eligibility/eligibility-profiles/ora-resource/ora_design_enforcement.md). Load it for this node; the child overrides above take precedence.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OM_ELIG.DESIGN | decision | 4 | design_enforcement | passed->OM_ELIG.GATE;blocked->OM_ELIG.FAILED | OM_ELIG.LOOKUPS | stop | Before displaying the immutable preview and design review. |
