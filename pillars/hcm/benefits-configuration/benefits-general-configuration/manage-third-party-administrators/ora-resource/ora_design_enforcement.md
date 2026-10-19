# Manage Third-Party Administrators Design Enforcement

| Gate | Blocking condition | Required outcome |
|---|---|---|
| Business object | Root is not `Organization` | Stop; do not use a fallback object. |
| DAT sections | `OrgInformation` is present | Exclude it; permit only `Organization` and `OrgUnitClassification`. |
| Classification shape | Rows are absent or names do not equal the one `BEN TPA` LOV value | Rebuild the source. |
| Classification code | Any DAT code value is populated | Remove it; the field must remain blank. |
| Location mapping | Inputs are partial/mixed or names replace codes | Stop and correct; explicit complete codes are used as-is. |
| Status | Omitted status is not `A`, or supplied status is invalid | Apply the default or stop. |

Only a passed design gate can proceed to immutable archive preparation and the
Core Data Loader approval workflow.
