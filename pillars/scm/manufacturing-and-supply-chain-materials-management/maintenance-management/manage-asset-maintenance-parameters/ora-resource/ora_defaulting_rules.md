# Defaulting Rules

## Documented Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Consider Organization Relationships When Creating Maintenance Work Orders | Yes | The parameter has not been changed | Yes | |
| Default Master Organization for Maintenance Management | Null | The parameter has not been configured | Yes | |
| Validation Organization for Customer Assets | Null | The parameter has not been configured | Yes | |
| Generate Maintenance Forecasts from a Maintenance Program | Enabled | The parameter has not been changed | Yes | |
| Generate Work Orders from a Maintenance Program | Enabled | The parameter has not been changed | Yes | |
| Allow Merge and Suppress Across Requirements | Disabled | The parameter has not been changed | No | |

## Source-Grounded Recommendations

| Field | Recommendation | Applies When | Rationale |
|---|---|---|---|
| Default Master Organization for Maintenance Management | Define the enterprise's main master organization, and ensure it is inventory-enabled. | Meter Templates or Fault Analysis Setup are used. | It supplies the default master organization; otherwise users must enter the master organization code manually. |
| Validation Organization for Customer Assets | Define a validation organization before creating customer assets. | Customer assets are created or updated. | Asset creation fails when no validation organization is defined. An item organization validates item properties, but cannot create serial- or lot-controlled assets. |
| Consider Organization Relationships When Creating Maintenance Work Orders | Keep **Yes** when only selected organizations should maintain each other's assets and the required relationships are defined; set **No** when cross-organization maintenance is routine. | Manual work-order creation across organizations. | **Yes** restricts cross-organization work orders to defined relationships; **No** allows eligible organizations under the same master organization. |
| Allow Suppress and Merge Across Work Requirements in a Maintenance Program | Set **No** unless there is an established business requirement and the forecast behavior is understood. | Maintenance programs have overlapping work requirements. | Oracle recommends modeling merge and suppress within a single work requirement; disabling cross-requirement behavior improves forecast clarity and enables incremental forecast actions. |
| Allow Merge and Suppress Across Requirements | For an explicit enable request, set the live-schema field `AllowMergeSuppressAcrossRequirementsFlag` to the enabled value in the generated assetSystemOptions update workbook; for an explicit disable request, set it to the disabled value. | The user explicitly requests this parameter change. | The generated live schema remains authoritative for the exact worksheet and accepted value representation. |
| Generate Maintenance Forecasts from a Maintenance Program | Evaluate whether page-level generation is needed; disable it when scheduled full refresh is the intended operating model. | Forecasts are managed by scheduled processing. | Disabling can avoid unnecessary full-program refreshes while retaining work-requirement or asset-level forecasting when cross-requirement merge and suppress is disabled. |
| Generate Work Orders from a Maintenance Program | Evaluate whether page-level work-order generation is needed; disable it when scheduled processing is the intended operating model. | Work orders are created by scheduled processing. | It helps avoid interactive full-refresh work-order creation when the scheduled process is the controlled execution route. |

Source: Oracle, [Set Up Maintenance — Define Asset Maintenance Parameters](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/set-up-maintenance.html#Define-Asset-Maintenance-Parameters), and linked Maintenance Program guidance. Recommendations are conditional guidance, not automatic changes.
