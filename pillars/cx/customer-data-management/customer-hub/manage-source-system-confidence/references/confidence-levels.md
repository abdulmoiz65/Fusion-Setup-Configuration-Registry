
This file describes how confidence levels are viewed, added and modified. 

Handle all requests to view, add or modify confidence levels using one of 
the behaviors defined in this file and enforce the specified restrictions.

# Confidence Level Schema

| Attribute Name  | Description                                                 | Valid Values         
| ----------------|-------------------------------------------------------------|----------------------------------------------|
| AttributeName   | The attribute that can be updated by the source system.     |                                              |                
| ObjectName      | The object which defines the attribute that is updated.     | object_name in assets/object-attributes.json |                
| SourceSystem    | The source system which can update the attribute value.     | orig_system in assets/source-systems.json    |
| ConfidenceLevel | The level of confidence for updates from the source system. | Integer value between 0 and 100              |

# View Confidence Levels

- Show a table with attribute name, object name, source system and confidence level columns in this order.
- Show case-sensitive exact values for attribute name, object name and source system. 

# Modify Confidence Levels

- Accept user-entered values for confidence level attributes.
- Validate user input based on valid values for each attribute.

# Output File Schema

| Column Name           | Column Value                                                 |
|-----------------------|--------------------------------------------------------------|
| OrigSystem            | populated from SourceSystem in user input                    |   
| TableName             | populated from table_name in assets/object-attributes.json   |
| AttributeName         | populated from attr_names in assets/object-attributes.json   |
| ConfidenceLevel       | populated from ConfidenceLevel in user input                 |  
| EffectiveStartDate    |                                                              |
| EffectiveEndDate      |                                                              |
| EffectiveLatestChange |                                                              |
| ColumnName            | populated from column_names in assets/object-attributes.json |
| CreatedBy             |                                                              |
| EffectiveSequence     |                                                              |
| EntityLevel           | N                                                            |
| LastUpdatedBy         |                                                              |
| ObjDef                | populated from object_def in assets/object-attributes.json   |
| ObjName               | populated from object_type in assets/object-attributes.json  |
| OrigSystem1           | populated from SourceSystem in user input                    |

# Update Confidence Levels

- Find an existing row based on attribute name, object name and source system using case-insensitive exact match.
- Update confidence level of the existing row per output file schema.
- Do not update any other column values of the existing row.

# Add Confidence Levels

- Create a new row if there is no existing row for this attribute name, object name and source system.
- Initialize all column values of the new row per output file schema.
