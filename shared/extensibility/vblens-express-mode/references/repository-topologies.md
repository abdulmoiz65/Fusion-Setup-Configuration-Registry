# Repository topologies

Classify the workspace before assuming build, metadata, or preview behavior.

## AppUI extension

Common evidence:

- `extension1/sources/vb-extension.json`
- `extension1/sources/ui/self/applications/.../app.json`
- A single application `urlId` or `id`

This topology can usually produce one direct preview route after packaging.
Validate the actual repository build contract before running any helper.

## Multi-product Fusion Extension

Common evidence:

- `extension1/sources/extension.json`
- `extension1/sources/dynamicLayouts/<producer>/<page>/`
- `extension1/sources/ui/<producer>/applications/.../*-x.*`
- Dependencies on several Oracle-delivered producer applications

This topology can extend multiple pages and applications. Do not require one
`ui/self` application or one preview `urlId`. Resolve each changed UI path from
its `applications/<application>/flows/<flow>/pages/<page>` ownership. Use
`fscmUI` for every derived page URL regardless of the extension family. Report
dynamic-layout or other targets without deterministic UI ownership as
unresolved rather than guessing.

## Dynamic Layout artifacts

Typical Extension files include:

- `metadata-rules-x.json`
- `layout-x.json`
- `layout-x.html`
- `layout-x.js`
- `data-description-x.json`
- `data-description-x.js`
- `metadataRules/<rule>.js`

The `-x` suffix or customer-extension directory is evidence of Extension
ownership. Confirm ownership from the repository rather than relying only on a
filename.

## UI overlay artifacts

Typical page overlay files include:

- `<page>-x.json`
- `<page>-x.js`
- `<page>-rules-x.json`
- `<page>-x-chains/*.js`

Read producer files only as evidence when they are available. Do not add or
modify unsuffixed Oracle-delivered page files in an Extension repository.

## Express Mode artifact families

Inventory Business Rules, Advanced Expressions, Page Properties, Configure Page
Properties, field ordering, data descriptions, and supporting dynamic-layout
metadata. App UI paths remain relevant for page URL derivation and packaging,
but Advanced Mode-only source is outside the customization scope.

## Unknown topology

If neither extension metadata format is present:

1. Locate `package.json` and `Gruntfile.js`.
2. Search for nested extension roots.
3. Inspect repository documentation and build scripts.
4. Report the topology as unknown.
5. Do not install, build, or mutate until the extension root is confirmed.

## Build readiness

Static readiness requires:

- A recognized topology
- A valid `package.json`
- A declared Visual Builder build dependency
- A repository build entry point or supported build API

Operational readiness additionally requires installed dependencies and any
required private package or Component Exchange access. Installing dependencies
requires user approval.
