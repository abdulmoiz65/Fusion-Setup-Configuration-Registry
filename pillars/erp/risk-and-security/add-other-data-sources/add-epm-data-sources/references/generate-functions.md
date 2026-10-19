# Generate Functions

## Purpose

Generate the function definitions used by connector attribute mappings for
documented fixed, defaulted, or derived values.

## Inputs

- Generated `attributeMappings` output from `generate-mappings.md`
- Source and target attribute metadata
- Approved transformation, defaulting, and derivation context

## Procedure

1. Read every mapping whose `fromType` is `FUNCTION` or whose recorded mapping
   requirement needs a fixed, defaulted, or derived value.
2. Determine the function type, inputs, properties, and output data type from
   the approved mapping context and the target attribute definition.
3. Generate a unique function identifier and function name for each mapping
   requirement.
4. Populate the function's properties, inputs, and outputs using the resolved
   source and target metadata.
5. Add the completed function object to the owning mapping entry's `functions`
   array.
6. Update the related `mappings` item so its function identifier and
   `fromType` reference the generated function.
7. Verify every function output is compatible with its mapped target attribute
   and every function reference resolves within the same mapping entry.

## Generated Function Syntax

```json
{
  "attributeMappingDetails": {
    "functions": [
      {
        "functionId": "<function identifier>",
        "functionType": "<function type>",
        "functionName": "<function name>",
        "functionProperty": [
          {
            "dataType": "<property data type>",
            "key": "<property key>",
            "name": "<property name>",
            "value": "<property value>"
          }
        ],
        "functionInput": [
          {
            "dataType": "<input data type>",
            "name": "<input name>"
          }
        ],
        "functionOutput": [
          {
            "dataType": "<output data type>",
            "name": "<output name>"
          }
        ]
      }
    ]
  }
}
```

Populate the angle-bracket fields from the mapping requirement and resolved
source and target metadata. Merge this `functions` array into its owning
`attributeMappingDetails` object in the final connector-model JSON.
