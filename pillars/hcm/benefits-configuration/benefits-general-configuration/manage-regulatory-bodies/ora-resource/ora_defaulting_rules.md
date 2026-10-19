# Manage Regulatory Bodies Defaulting Rules

Apply defaults only after validation and dependency resolution. Preserve valid
explicit values unless this table marks the value as non-overridable.

| Field and section | Default | Applies when | User override | Failure behavior |
|---|---|---|---|---|
| `ClassificationName` in `Organization` | Value returned by the `REGBOD` organization classifications LOV query | An Organization row is authored | No | Stop if the query does not return exactly one nonblank value. |
| `ClassificationName` in `OrgUnitClassification` | Same LOV-returned value | An OrgUnitClassification row is authored | No | Stop if the query does not return exactly one nonblank value. |
| `ClassificationCode` in all DAT rows | Blank | Create or update | No | Do not populate the attribute. |
| `LocationCode` and `LocationSetCode` in `Organization` | Explicit supplied code pair, otherwise `locationsLov` response `LocationCode` and `SetCode` | Create or update when location is supplied or required | Explicit complete code pair only | Stop on partial input or a non-unique/missing effective-dated name lookup. |
| `Status` in `OrgUnitClassification` | `A` | Status is omitted | Yes | Preserve a supplied valid value; stop if it is invalid. |

Never request `ClassificationCode` or `ClassificationName` from the user or let
an imported value change them. Derive only `ClassificationName` from the
required LOV result; keep `ClassificationCode` blank in DAT. Do not default
effective dates, names, identifiers, or optional EFF values: resolve them from
current metadata or require the necessary business input.

Task Location Name and Location Set Name are input-only lookup values. Never
emit them as substitutes for `LocationCode` or `LocationSetCode` in DAT.
