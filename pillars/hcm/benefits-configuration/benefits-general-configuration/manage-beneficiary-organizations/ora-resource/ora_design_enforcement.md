# Manage Beneficiary Organizations Design Enforcement

| Gate | Applies when | Blocking condition | Required outcome |
|---|---|---|---|
| Business object | Every HDL source | Root object is not `Organization` | Stop; do not use `PersonBeneficiaryOrganization` or another fallback object. |
| DAT sections | Every generated DAT source | `OrgInformation` is present as a `METADATA` or `MERGE` section | Exclude the section; this task permits only `Organization` and `OrgUnitClassification`. |
| Classification shape | Create or update classification is required | Organization or OrgUnitClassification row is absent, or either ClassificationName differs from the one `HR_BEN` LOV result | Rebuild the source with the returned value in both rows. |
| Classification code | Create or update DAT is authored | Any DAT `ClassificationCode` attribute is populated | Remove the value; the code is non-mandatory and must remain blank. |
| Location mapping | Create or update DAT is authored | Location values are a mixed/partial pair, names are emitted instead of codes, or derived values do not come from one exact effective-dated LOV match | Stop and correct the input or mapping. Explicit complete code pairs must be used as-is. |
| Status | OrgUnitClassification is authored | Omitted status was not defaulted to `A`, or supplied status is invalid | Apply the default or stop for correction. |
| Update identity | Update or inactivate | Target or effective-date intent is not exact | Stop for an unambiguous identity. |
| Source integrity | Before preview | Source differs from current metadata or contains unsupported sections/attributes | Stop and regenerate or correct the source. |

Only a passed design gate can move to immutable archive preparation and the
Core Data Loader approval workflow.
