# Reference Lookups

## Territory Geography metadata

During Task Hook validation, route this declared read-only GET through
`core/fusion-api/rest-api-client/scripts/fusion_rest_client.py` using the same
selected properties as Data Loader and `REST-Framework-Version: 9`:

```text
/crmRestApi/resources/11.13.18.05/importExportObjectMetadata/GeoTerritoryInterface
fields=DisplayName,ObjectCode,UcmAccount,ImportSupport
```

Require exactly one record, `ObjectCode=GeoTerritoryInterface`,
`ImportSupport=Y`, and a nonempty slash-separated `UcmAccount` path.
Resolve the account from this live record; do not require a fixed account name.
Require core preflight `cxImportObjectCode` and converted `cxUcmAccount` to agree
with the metadata (append `$` to each account path segment). Stop on missing,
malformed, ambiguous or mismatched metadata before preview or upload.
`validate-metadata` validates a supplied response locally; it does not perform
or replace the live lookup.

Use the core client's one cache-managed authentication refresh only when
permitted. No task-local authentication, SOAP document lookup, identifier
recovery from server error text, or direct `geoZones` scan is part of this route.
Native Data Loader obtains and propagates the upload references itself.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TG.UCM_METADATA | step | 4 | reference_lookup | matched->TG.DEFAULTS;mismatch->TG.ERROR;failed->TG.ERROR | TG.DEPENDENCIES | stop | During preapproval Task Hook validation; compare live metadata with core preflight. |
