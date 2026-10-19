# Benefit Provider Reference Resolution

Use core data-loader metadata. `organizationClassificationsLOV?q=ClassificationCode='BEN'` and effective-dated exact `locationsLov` requests must include `REST-Framework-Version: 9`. Require one nonblank ClassificationName and one exact location match; map returned LocationCode and SetCode. Use explicit complete location codes as-is; never use direct REST writes.
