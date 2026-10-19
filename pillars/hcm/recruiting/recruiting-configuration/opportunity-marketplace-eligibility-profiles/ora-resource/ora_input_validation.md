# Input Validation

Apply the parent input contract, using the local Opportunity Marketplace template. Every packaged profile must have BnftCagrPrtnCd ORA_OPP_MARKET_PLACE. The agent checks this before preview, import and monitoring; automated evaluation is not yet migrated. New profile workbooks require Profile Type Participant (PRTP) and Assignment to Use Specific assignment (APS), accepting labels/codes case-insensitively and rejecting conflicting continuation rows. New ZIP previews and imports require ProfileType PRTP and AsmtToUseCd APS before any session or write. Historical monitoring retains usage-only package checks; evaluation remains unavailable in the initial Markdown route. Never silently replace user values; regenerate and review older ANE packages before any new import. The initial Markdown route supports only profile-only Person Type and Department criteria. Stop on other criteria or populated supporting tabs unless the user explicitly excludes those tabs; supporting-only workbooks are not yet supported by this route. Task context and previews must identify ORA_IRC_MP_ELIGIBILITY_PROFILE, never the Benefits task code.

Parent contract: [Input Validation](../../../../benefits-configuration/benefits-eligibility/eligibility-profiles/ora-resource/ora_input_validation.md). Load it for this node; the child overrides above take precedence.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OM_ELIG.INPUT | step | 1 | validate_input | valid->OM_ELIG.DEPENDENCIES;invalid->OM_ELIG.FAILED | none | stop | Before workbook preparation or package preview. |
