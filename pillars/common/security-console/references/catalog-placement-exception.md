# Pillar Catalog Placement Exceptions

## COMMON-SECURITY-CONSOLE-001

Approved by explicit repository-user instruction on 2026-10-12. This exception
keeps the eight canonical child skills listed in
[catalog-placement-exceptions.json](catalog-placement-exceptions.json)
under `pillars/common/security-console`. They provide reusable Common security
setup guidance across offerings; `security-console` is a domain folder rather
than a generated Oracle offering.

The exception applies only to `pillar.effective_catalog_hierarchy` placement
for an exact registered path, skill ID, layer and pillar. This local exception
records the user-approved placement decision. The
unmodified central auditor does not consume this local registry and may still
report a catalog-placement finding; do not claim an effective-catalog match.
It does not exempt new siblings, nested descendants,
legacy aliases, moved skills, or mismatched manifests.

Task identities, catalog availability and execution flags, input validation,
source guidance, dependencies, layer boundaries, security, tests and execution
approval remain mandatory. This does not approve a live Fusion operation or
replace repository-owner merge review. Retire or amend the entries if canonical
ownership or placement changes; do not broaden them by path prefix.
