# Reference Lookups

Delegate every lookup in this file exclusively to
`core.fusion-api.rest-api-client`, using `REST-Framework-Version: 9`. These
rules define SCM-domain identity and match requirements only; they must not
implement REST transport, OAuth, retry, redaction, or diagnostics.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_attribute_group_by_attribute | An update request supplies AttrName or AttrDispName | AttrName or AttrDispName; optional AttrGroupName after an ambiguity response | Through `core.fusion-api.rest-api-client`, GET `/fscmRestApi/resources/11.13.18.05/itemOperationalAttributeControlLevels?q=AttrName={AttrName}` when AttrName is supplied; use `q=AttrDispName={AttrDispName}` when only AttrDispName is supplied | AttrGroupName, AttrGroupDispName, AttrName, AttrDispName | Require exactly one distinct AttrGroupName and a matching attribute identity; when several group names are returned, use a supplied AttrGroupName only when it identifies one result | AttrGroupName, AttrGroupDispName, AttrName, AttrDispName | When several group names are returned and Group Name is absent, stop with Provide Group Name as there are more than 1 for given attribute name; otherwise stop and request a corrected attribute identity |
| resolve_operational_attribute_control | The attribute group and attribute are resolved | AttrGroupName, AttrName, optional AttrGroupDispName, optional AttrDispName | Through `core.fusion-api.rest-api-client`, GET `/fscmRestApi/resources/11.13.18.05/itemOperationalAttributeControlLevels/` followed by the Fusion-issued composite key, with `REST-Framework-Version: 9`; first resolve with `?finder=PrimaryKey;AttrGroupName={AttrGroupName},AttrName={AttrName}` using the same header | AttrGroupName, AttrGroupDispName, AttrName, AttrDispName, ControlLevel, MaximumDecimalDigits, `@context.key`, versioned item link | Require exactly one primary-key result; require exact matches for all supplied identity values; require that a versioned item-level GET succeeds | Resolved composite-key item link, current ControlLevel, current MaximumDecimalDigits, AttrGroupName, AttrGroupDispName, AttrName, AttrDispName | Stop before preview; request corrected identity values or investigate the versioned item route read-only |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| One attribute group is resolved | Fill AttrGroupName and AttrGroupDispName, then resolve the exact control record |
| More than one group is returned for the attribute and Group Name is absent | Stop with Provide Group Name as there are more than 1 for given attribute name |
| One exact control record is resolved | Retain current values and perform a versioned item-level GET with `REST-Framework-Version: 9`; use only the resulting Fusion-issued composite-key item link for the approval preview and PATCH |
| A versioned item-level GET succeeds | Use the exact composite-key item link and include `REST-Framework-Version: 9` in both the PATCH and post-PATCH GET |
| An unversioned item link returns 404 | Do not retry a PATCH against that link; validate the versioned composite-key route read-only and obtain a new approval preview before any PATCH |
| The identity is absent, nonunique, or does not match | Do not construct an item URL or prepare an approval preview |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OAC.RESOLVE_ATTRIBUTE_GROUP | decision | 20 | reference_lookup | resolved->OAC.RESOLVE_TARGET;multiple_groups->OAC.RETURN_ISSUES;unresolved->OAC.RETURN_ISSUES | OAC.VALIDATE_INPUT | stop | A valid attribute name or display name is available |
| OAC.RESOLVE_TARGET | decision | 30 | reference_lookup | resolved->OAC.CHECK_READINESS;unresolved->OAC.RETURN_ISSUES | OAC.RESOLVE_ATTRIBUTE_GROUP | stop | Attribute group and technical attribute name are resolved |
