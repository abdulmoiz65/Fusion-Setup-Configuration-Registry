# Generate Mappings

## Purpose

Generate validated `attributeMappings` for the connector-model JSON. This
workflow combines OpenAPI-derived source attributes with the target object and
attribute metadata resolved by the approved Data Integrator adapter.

## Inputs

- Generated operation output from `extract-operations.md`
- Complete source attribute sets from `dataExtractionObjects.items`
- Complete target object and attribute sets returned by connector-template
  resolution
- Connector type, connector name, and approved mapping context
- Optional current mapping-candidate evidence

## Mapping Preparation

1. Create one mapping work item for each source-to-target object relationship
   selected by the connector-template resolution stage.
2. Copy the supplied source and target object identifiers, names, descriptions,
   object codes, and attribute sets into the work item exactly as resolved.
3. Require complete `items` arrays for both source and target attribute sets.
   Each attribute used for mapping provides its exact `attributeCode` and
   `attributePath`.
4. Build candidate pairs from the current source and target attribute sets.
   Candidate evidence may rank exact prior matches and normalized semantic
   matches; the current resolved metadata remains the authority for all IDs and
   paths.
5. Retain the prepared work item, candidate evidence, and mapping result as one
   reviewable mapping record when durable project artifacts are requested.

## Matching Procedure

1. Build `source.nodes` and `target.nodes` from every attribute in the
   corresponding complete runtime attribute set. Each node contains only its
   exact `attributeId`.
2. Evaluate exact candidate matches first after confirming that both current
   attributes still exist.
3. Evaluate ranked semantic candidates next using current attribute path, code,
   name, description, data type, and object meaning.
4. Select a mapping only when its business meaning and data type are compatible
   with the selected target attribute.
5. Emit direct source-to-target mappings with the exact source and target paths
   and attribute codes from the current work item.
6. Record a fixed, defaulted, or derived-value requirement for
   `generate-functions.md` when a direct mapping cannot express it.
7. Add the completed mapping entry to the `attributeMappings` array in the
   `extractedData` object produced by `extract-operations.md`.
8. Verify that every object identifier, node attribute identifier, mapping path,
   and mapping attribute identifier resolves in the current work item.

## Generated Mapping Syntax

```json
{
  "attributeMappings": [
    {
      "attributeMappingDetails": {
        "source": {
          "nodes": [
            {
              "attributeId": "<exact source attributeCode>"
            }
          ],
          "ODId": "<resolved source object identifier>",
          "ODLabel": "<resolved source object label>"
        },
        "target": {
          "nodes": [
            {
              "attributeId": "<exact target attributeCode>"
            }
          ],
          "ODId": "<resolved target object identifier>",
          "ODLabel": "<resolved target object label>"
        },
        "mappings": [
          {
            "from": "<exact source attributePath>",
            "fromAttributeId": "<exact source attributeCode>",
            "fromType": "SOURCE",
            "to": "<exact target attributePath>",
            "toAttributeId": "<exact target attributeCode>",
            "toType": "TARGET"
          }
        ],
        "functions": []
      },
      "name": "<resolved mapping name>",
      "description": "<resolved mapping description>",
      "targetObjectDefinition": {
        "id": "<resolved target extraction-object identifier>"
      },
      "sourceObjectDefinition": {
        "id": "<resolved source extraction-object identifier>"
      }
    }
  ]
}
```

## Function Handoff

Pass each recorded transformation requirement and its owning mapping entry to
`generate-functions.md`. That workflow adds the function definitions and their
mapping edges to the same `attributeMappingDetails` object.

## Mapping Outcome

Produce one result for every prepared work item:

```json
{
  "results": [
    {
      "wfObjectId": "<prepared work-item identifier>",
      "status": "SUCCESS",
      "payload": {
        "attributeMappingDetails": {},
        "name": "<resolved mapping name>",
        "description": "<resolved mapping description>",
        "targetObjectDefinition": {
          "id": "<resolved target extraction-object identifier>"
        },
        "sourceObjectDefinition": {
          "id": "<resolved source extraction-object identifier>"
        }
      }
    },
    {
      "wfObjectId": "<prepared work-item identifier>",
      "status": "FAILED",
      "error": "<validation or mapping-resolution error>"
    }
  ]
}
```

Use `SUCCESS` when the generated payload validates against the current source
and target metadata. Use `FAILED` with the prepared work-item identifier and a
concise validation or resolution error when the work item cannot produce a
valid mapping. Convert successful payloads into `extractedData.attributeMappings`
only after all required work-item results are present.
