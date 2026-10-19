# Custom Time Attributes Reference Lookups

## Source Basis

- User-designated authority for both default data sources, Attribute Category, and occupied Value Locations: the fresh same-task Custom Time Attributes export.

## Data Source Usage Mapping

The Custom Time Attributes export stores the two UI data-source selections in
different usage members. Treat this mapping as authoritative when creating or
updating an attribute:

| UI field | Export member | Row selector | DataSourceCode effect |
|---|---|---|---|
| Default Filtered Data Source for Time Entry | `ORA_CUST_TM_ATRB_DS_USG.csv` | `TimeAttributeFieldName` equals the attribute Name; `UsageType` is `USER` | The row's `DataSourceCode` is the filtered source. |
| Default Unfiltered Data Source for Setup Tasks | `ORA_HWM_CUST_TM_ATRB_DS_ADMIN_USG.csv` | `TimeAttributeFieldName` equals the attribute Name; `UsageType` is `ADMIN` | The row's `DataSourceCode` is the unfiltered source. |

For an update, retain the unrequested usage row unchanged. When both sources
are changed, preserve the user-row link to the administrator usage code in
`ORA_HWM_CUST_TM_ATRB_DS_ADMIN_USG.DataSourceUsageCode`.
- User-provided required field selections and numbered Value Location mappings.

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_filtered_data_source | After fresh same-task export, before package preparation; parent and each dependent attribute | User-designated authority: validated Custom Time Attributes export; supplied Default Filtered Data Source for Time Entry selection; `ORA_CUST_TM_ATRB_DS_USG.csv`; actual exported members, headers, and reference relationships | Match the supplied name or code against `DataSourceCode` in the selected attribute's `UsageType=USER` row and the exported data-source catalog; require one distinct verified identity. Repeated use of the same identity across attributes is not a separate candidate; identical labels with different identities remain ambiguous. Do not assume the export enumerates every possible Fusion choice. | Preserve the matched code and the user-usage row's reference keys. | If no exported reference matches, present the mismatch and request explicit user confirmation that the supplied source is available in Fusion. On confirmation, retain the supplied display value, record the lookup as overridden with the confirmation, and require post-import reconciliation of the requested source link. If several distinct identities match, display them and require explicit selection. Stop on missing or ambiguous field mappings; do not fabricate codes, make live LOV calls, or create reference data through this resolver. |
| resolve_unfiltered_data_source | After fresh same-task export, before package preparation; parent and each dependent attribute | User-designated authority: validated Custom Time Attributes export; supplied Default Unfiltered Data Source for Setup Tasks selection; `ORA_HWM_CUST_TM_ATRB_DS_ADMIN_USG.csv`; actual exported members, headers, and reference relationships | Match the supplied name or code against `DataSourceCode` in the selected attribute's `UsageType=ADMIN` row and the exported data-source catalog; require one distinct verified identity. Repeated use of the same identity across attributes is not a separate candidate; identical labels with different identities remain ambiguous. Do not assume the export enumerates every possible Fusion choice. | Preserve the matched code and the administrator-usage row's reference keys. | If no exported reference matches, present the mismatch and request explicit user confirmation that the supplied source is available in Fusion. On confirmation, retain the supplied display value, record the lookup as overridden with the confirmation, and require post-import reconciliation of the requested source link. If several distinct identities match, display them and require explicit selection. Stop on missing or ambiguous field mappings; do not fabricate codes, make live LOV calls, or create reference data through this resolver. |
| resolve_attribute_category | After fresh same-task export, before package preparation; parent attribute only | User-designated authority: validated Custom Time Attributes export; supplied Attribute Category selection; actual exported members, headers, and reference relationships | Identify the exported field and reference relationship for Attribute Category from package evidence. Match the supplied name or code against the corresponding exported reference values; require one distinct verified identity. Repeated use of the same identity across attributes is not a separate candidate; identical labels with different identities remain ambiguous. Do not assume the export enumerates every possible Fusion choice. | Preserve the matched exported representation and associated reference keys for Attribute Category; use only columns and relationships established by this same-task export | If no exported reference matches, stop and request a selection evidenced by the export or additional verified same-task evidence. If several distinct identities match, display them and require explicit selection. Stop on missing or ambiguous field mappings; do not fabricate codes, make live LOV calls, or create reference data through this resolver. |
| resolve_value_location | After fresh same-task export, before preparing new parent or dependent rows | User-designated authority: fresh Custom Time Attributes export; selected Attribute Category; selected Data Type; Value Locations already reserved for new rows in this package | Filter exported rows to the selected Attribute Category, then inspect Value Locations for the selected data-type prefix. For Text use AttributeVarchar; Number use AttributeNumber; Date use AttributeDate; Time stamp use AttributeTimestamp. Choose the smallest positive integer n whose complete prefix-plus-number value is absent from that category's export rows and current package reservations for that category. Start at 1 and check gaps; do not simply use maximum plus one. Reserve each selected location before processing the next new row. | Value Location as the prefix followed directly by n, without parentheses; keep each Attribute Category and data type's numbered slots independent | If no slots are occupied for the selected Attribute Category and prefix, select suffix 1. If export completeness, the owning CSV member/column, category representation, or occupied-slot interpretation cannot be established, stop before preview; do not treat missing evidence as an empty slot set. |

Examples: occupied AttributeVarchar1 selects AttributeVarchar2; occupied
AttributeNumber1 and AttributeNumber3 selects AttributeNumber2; occupied
AttributeDate1 selects AttributeDate2; occupied AttributeTimestamp1 selects
AttributeTimestamp2. All examples use a complete fresh export.

## Export Stage Boundary

Before export, validate required selections and input shape without claiming
reference resolution. After the invoking workflow obtains the fresh same-task
export, revisit these resolvers and resolve all applicable references before
preparing the package or requesting import approval. A deferred result does
not satisfy the post-export reference gate. Export absence before its scheduled
step is not a missing-reference failure.

The actual CSV member names, columns, and reference keys are discovered from
the fresh package. This guidance defines the lookup authority and procedure,
not invented technical field names.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CTA.RESOLVE_FILTERED_DATA_SOURCE | step | 12 | reference_lookup | resolved->CTA.RESOLVE_UNFILTERED_DATA_SOURCE;not_applicable->CTA.RESOLVE_UNFILTERED_DATA_SOURCE;blocked->CTA.HANDLE_ISSUE | CTA.VALIDATE_INPUT | stop | Resolve required filtered source for parent and each dependent attribute; defer with not_applicable before export, then revisit after export before preview |
| CTA.RESOLVE_UNFILTERED_DATA_SOURCE | step | 14 | reference_lookup | resolved->CTA.RESOLVE_ATTRIBUTE_CATEGORY;not_applicable->CTA.RESOLVE_ATTRIBUTE_CATEGORY;blocked->CTA.HANDLE_ISSUE | CTA.RESOLVE_FILTERED_DATA_SOURCE | stop | Resolve required unfiltered source for parent and each dependent attribute; defer with not_applicable before export, then revisit after export before preview |
| CTA.RESOLVE_ATTRIBUTE_CATEGORY | step | 16 | reference_lookup | resolved->CTA.RESOLVE_VALUE_LOCATION;not_applicable->CTA.RESOLVE_VALUE_LOCATION;blocked->CTA.HANDLE_ISSUE | CTA.RESOLVE_UNFILTERED_DATA_SOURCE | stop | Resolve required parent category; do not require a category on dependents; defer with not_applicable before export, then revisit after export before preview |
| CTA.RESOLVE_VALUE_LOCATION | decision | 17 | reference_lookup | resolved->CTA.APPLY_DEFAULTS;not_applicable->CTA.APPLY_DEFAULTS;blocked->CTA.HANDLE_ISSUE | CTA.RESOLVE_ATTRIBUTE_CATEGORY | stop | Resolve new attribute locations after fresh export; not_applicable before export or when no new attributes are added; invoking workflow must revisit after export before preview |
