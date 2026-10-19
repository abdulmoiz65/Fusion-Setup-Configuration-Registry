# Manage Third-Party Administrators Defaulting Rules

| Field and section | Default | Applies when | Override |
|---|---|---|---|
| `ClassificationName` in `Organization` | The one `BEN TPA` classifications LOV result | Organization row is authored | No |
| `ClassificationName` in `OrgUnitClassification` | Same LOV-returned value | Classification row is authored | No |
| `ClassificationCode` in all DAT rows | Blank | Create or update | No |
| `LocationCode` and `LocationSetCode` | Complete explicit pair, otherwise location LOV `LocationCode` and `SetCode` | Create or update | Explicit complete pair only |
| `Status` in `OrgUnitClassification` | `A` | Status omitted | Preserve supplied metadata-valid value |

Stop if a non-overridable default cannot be resolved. Never request or accept a
classification override; task location names are lookup-only and are never DAT
substitutes for location codes.
