# Profile Options

## Purpose and Sources

Use this reference for two distinct workflows:

1. Read effective profile values for the authenticated user's current Fusion
   session through the published `profileValues` resource.
2. Read profile definitions and create, update, or delete their site, product,
   or user-level values through the internal `profileOptions` CRUD resource.

The first workflow is documented in [Profile Values REST
Endpoints](https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-profile-values.html).
The second is based on the provided export of the internal **Profiles CRUD REST
Service** page (introduced in Rel13 19.10). The parent `profileOptions`
resource is read-only; only its value child resources are mutable.

## 1. Read Effective Profile Values

`profileValues` resolves values for the current user session. Use it to verify
the effective value Fusion will use, not to update a configured value.

| Operation | Method | Endpoint |
| --- | --- | --- |
| Get all effective profile values | `GET` | `/fscmRestApi/resources/11.13.18.05/profileValues` |
| Get one effective profile value | `GET` | `/fscmRestApi/resources/11.13.18.05/profileValues/{profileValues_Id}` |

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  /fscmRestApi/resources/11.13.18.05/profileValues

python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  '/fscmRestApi/resources/11.13.18.05/profileValues/<profileValues_Id>'
```

`profileValues_Id` is only valid for this resource. Do not use it in a
`profileOptions` URL.

## 2. Manage Configured Profile Option Values

The `profileOptions` parent exposes the definition, keyed by
`ProfileOptionName` (the internal profile code), and its values. It has a
`ProfileNameFinder` that requires `ProfileOptionName`. The parent has these
read operations:

| Operation | Method | Endpoint |
| --- | --- | --- |
| Describe service metadata | `GET` | `/fscmRestApi/resources/11.13.18.05/profileOptions/describe` |
| Get a profile definition and values | `GET` | `/fscmRestApi/resources/11.13.18.05/profileOptions/{ProfileOptionName}` |

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  /fscmRestApi/resources/11.13.18.05/profileOptions/describe

python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  '/fscmRestApi/resources/11.13.18.05/profileOptions/<ProfileOptionName>'
```

The parent response identifies whether each level is enabled and updatable:
`SiteLevelEnabled`, `SiteLevelUpdatable`, `ProductLevelEnabled`,
`ProductLevelUpdatable`, `UserLevelEnabled`, and `UserLevelUpdatable`. Verify
the relevant pair is `Y` before attempting a value write.

### Level-Specific Child Resources

| Level | Child resource | Key and value fields | Supported operations |
| --- | --- | --- | --- |
| Site | `siteProfileOptionValues` | Item key `SITE`; `ProfileOptionValue` | `GET`, `POST`, `PATCH`, `DELETE` |
| Product | `productProfileOptionValues` | Item key `LevelValue` (application short name); `ProfileOptionValue` | `GET`, `POST`, `PATCH`, `DELETE` |
| User | `userProfileOptionValues` | Item key `UserName`; create body uses `LevelValue` (user GUID) and `ProfileOptionValue` | `GET`, `POST`, `PATCH`, `DELETE` |

The internal service defaults the site level's hidden key fields to
`('SITE', 'SITE')`; the `SITE` item therefore has at most one value. Product
and user child records represent their respective application or user scope.

### Site-Level Read and Update

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  '/fscmRestApi/resources/11.13.18.05/profileOptions/<ProfileOptionName>/child/siteProfileOptionValues'

python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  '/fscmRestApi/resources/11.13.18.05/profileOptions/<ProfileOptionName>/child/siteProfileOptionValues/SITE' \
  --method PATCH \
  --body '{"ProfileOptionValue":"N"}'
```

### User-Level Read, Create, and Update

The user child resource uses `UserName` in its item URL, but its create body
requires the user's GUID as `LevelValue`. Resolve that GUID first through the
service's `profileUsers` resource; do not use a display name as the GUID.

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  '/fscmRestApi/resources/11.13.18.05/profileUsers/<UserName>'

python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  '/fscmRestApi/resources/11.13.18.05/profileOptions/<ProfileOptionName>/child/userProfileOptionValues' \
  --method POST \
  --body '{"LevelValue":"<UserGuid>","ProfileOptionValue":"Y"}'

python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  '/fscmRestApi/resources/11.13.18.05/profileOptions/<ProfileOptionName>/child/userProfileOptionValues/<UserName>' \
  --method PATCH \
  --body '{"ProfileOptionValue":"N"}'
```

For the documented create-or-update form, use `POST` to the user child
collection and add `--header Upsert-Mode=true`; still resolve `UserGuid` first.

### Product-Level Values

Use the product child collection below. The item's `LevelValue` is the target
application short name. Retrieve the profile and child record first, then use
the returned item link or that documented level value for a write.

```text
/fscmRestApi/resources/11.13.18.05/profileOptions/{ProfileOptionName}/child/productProfileOptionValues
/fscmRestApi/resources/11.13.18.05/profileOptions/{ProfileOptionName}/child/productProfileOptionValues/{LevelValue}
```

## Preconditions and Safety

The internal service identifies `FND_APP_MANAGE_ALL_PROFILE_VALUES_PRIV` as
the permission governing CRUD operations. Before a write, verify that
privilege, the requested level's enabled/updatable flags, profile option name,
scope key, current value, and intended value. Obtain explicit approval for the
named target and new value; do not retry a mutating request automatically.

Return the HTTP status, response summary, and ECID or request ID when present.
Do not log OAuth tokens, Authorization headers, or a sensitive profile value.
