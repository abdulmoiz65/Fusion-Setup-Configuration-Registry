# Source and Documentation Evidence

Evidence was refreshed on 2026-08-27 for the current skill implementation.
Revalidate release-sensitive paths and metadata before live use.

## Requirement and Catalog Sources

- Jira epic `GROW-8116`: complete V1 scope, acceptance criteria, workbook,
  validation, comparison, handoff, error, naming, and demonstration rules.
- Approved HCM Tool taxonomy: functional area `Profile Rating Model
  Configuration`, setup task `HRT_MANAGE_PROFILE_RATING_MODELS`, FSM `Profile
  Rating Models`, HDL `Rating Model`, and one reusable configuration containing
  header plus applicable levels, categories, review points, and distributions.
- HCM Common Foundation baseline: P0 product-owned foundation; FSM, HDL, REST
  Read and Validation methods; current `Rating Model` hierarchy must be
  confirmed through View Business Objects.

The effective catalog materialized from ATEAM-1375 establishes the canonical
generator identifier `hcm.hcm-tool.profile-rating-model-configuration`. Treat
the former repository identifier `hcm.hcm-tool.profile-rating-model` and its
folder only as legacy project-history references; do not generate new skills or
artifacts under that identity.

## Oracle Documentation

- [Rating Models](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/rating-models.html)
- [How to Create a Rating Model](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/how-to-create-a-rating-model.html)
- [Rating Levels](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/rating-levels.html)
- [Review Points](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/review-points.html)
- [Rating Categories](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/rating-categories.html)
- [Distributions](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/distributions.html)
- [Skills Center Components](https://docs.oracle.com/en/cloud/saas/talent-management/faudy/components-of-skills-center.html)
- [Set Up the Skill Content Section](https://docs.oracle.com/en/cloud/saas/talent-management/faidy/set-up-the-skill-content-section-for-person-profiles.html)
- [Performance Template Sections](https://docs.oracle.com/en/cloud/saas/talent-management/faipm/considerations-for-creating-performance-template-sections.html)
- [Talent Review Box Chart](https://docs.oracle.com/en/cloud/saas/talent-management/fatrs/box-chart-matrix-options.html)
- [Talent Ratings Templates](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/talent-ratings-templates.html)

## Environment and Version Evidence

- Oracle documents the quarterly application release in the authenticated
  **About This Application** dialog. This is supporting product context, not a
  reason to ask the implementation user for a screenshot, manual navigation,
  or a typed release value during read-only preflight.
- Oracle REST resource versions such as `11.13.18.05` or `v1` identify the API
  contract; they are not quarterly application releases such as `26C`. Never
  translate one into the other.
- For this skill, resolve the exact environment from trusted core
  authentication context. Record a quarterly release only when trusted core or
  supported target metadata already provides the value and its source. Prove
  the required runtime compatibility with the source-backed REST API version,
  path, bounded request result, and response coverage.

References:

- [REST API for Common Features](https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/index.html)
- [Check Your Instance's Release Version](https://docs.oracle.com/en/cloud/paas/visual-builder/visualbuilder-building-appui/what-if-dev-prod-instances-arent-same-release.html)

## Source Evidence

- `hcm/.../ProfileOptionSD.xml`: `ORA_HRT_SETUP_REDWOOD_ENABLED` is a route-only
  profile option with site default `N`; it does not change the data contract.
- `components/hcmCoreSetup/src/META-INF/jazn-data.xml`: privilege
  `HRT_MANAGE_TALENT_PROFILE_RATING_MODEL_PRIV` covers the ADF flow, Redwood
  route, service operations and `talentRatingModels` resource.
- `components/hcmCoreSetup/profiles/restModel/.../RatingModelAM_RatingModelVOResources.xml`:
  the resource is `unlisted`, exposes component accessors, and disables delete
  on the root, levels and descriptive flexfield resources.
- Setup business objects include `HRT_RATING_MODELS_B`,
  `ORA_HRT_RATING_LEVELS_B`, and `ORA_HRT_RATING_CATEGORIES`.

The privilege and UI bundle are evidence of product implementation, not
authorization to use unlisted REST writes. Creation remains routed through
verified current FSM or HDL metadata and `core.data-loader`.
