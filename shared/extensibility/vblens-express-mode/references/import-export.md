# Reusable rule import and export

## Portable package model

A reusable rule package should contain:

- Package format version
- Source Fusion family, page, and release
- Rule identifiers, labels, descriptions, status, and order
- Conditions, actions, messages, and affected fields
- Advanced Expression modules
- Flexfield, lookup, and setup dependencies
- Environment-specific values that require mapping
- Known conflicts and limitations
- Source confidence and verification status
- Checksums for packaged files
- Integration and rollback notes

Do not include credentials, session data, environment hostnames, local paths,
unrelated configuration, or customer data.

## Export workflow

1. Select the exact rules and modules.
2. Validate them in their source repository.
3. Trace dependencies transitively.
4. Replace setup-specific values with declared mapping requirements rather
   than invented portable values.
5. Record page and release compatibility.
6. Produce a manifest and human-readable summary.
7. Verify that no unrelated files or secrets are included.

The initial skill produces an export plan and manifest design; deterministic
archive generation is an open implementation item.

## Import workflow

Treat all imported content as untrusted:

1. Parse without evaluating JavaScript.
2. Validate package shape and checksums.
3. Inventory rules, modules, fields, and dependencies.
4. Compare source and target topology, page, release, metadata versions,
   fields, Flexfields, lookups, and current rules.
5. Identify identifier collisions, conflicting actions, order changes, and
   unsupported properties.
6. Require explicit mappings for environment-specific values.
7. Produce an import assessment before changing files.
8. Integrate through Create or Update on a feature branch.

Do not execute an imported module merely to inspect it.
