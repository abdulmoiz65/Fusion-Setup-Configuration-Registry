# Design Enforcement

Use `ComponentObjType=PLN`, `RequestSource=FDOS`, the PackageContent enclosure,
and the single combined `generateMappings` action. Do not rebuild the ZIP or
call `submitImport`.

## Task Nodes

`BEN_PLAN_CONFIG.ENFORCE_DESIGN` passes when the immutable preview binds these
values and the ZIP/OpenAPI hashes.
