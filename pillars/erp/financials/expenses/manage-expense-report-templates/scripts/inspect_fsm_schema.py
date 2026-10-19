#!/usr/bin/env python3
"""Inspect fresh FSM CSV headers/relationships without copying configuration rows."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

TASK_CODE = 'EXM_MANAGE_EXPENSE_REPORT_TEMPLATES'
META = 'ASM_SETUP_CSV_METADATA.xml'
CHILD_PATHS = {
    'EXM_EXPENSE_TYPE_ITEMIZATION.csv': '/ExpenseTemplateVO/ExpenseTemplateVORow/ExpenseType/ExpenseTypeVORow/ExpenseTypeItemize/ExpenseTypeItemizeVORow',
    'EXM_PROJECT_EXP_TYPE_MAP.csv': '/ExpenseTemplateVO/ExpenseTemplateVORow/ExpenseType/ExpenseTypeVORow/ProjectExpTypeMap/ProjectExpTypeMapVORow',
}
PARENT_HEADERS = ['EXM_EXPENSE_TEMPLATE.BuName', 'EXM_EXPENSE_TEMPLATE.Name',
                  'EXM_EXPENSE_TYPE.BuName', 'EXM_EXPENSE_TYPE.TemplateName', 'EXM_EXPENSE_TYPE.Name']


def inspect_schema(path):
    content = Path(path).read_bytes()
    with zipfile.ZipFile(io.BytesIO(content)) as z:
        names = z.namelist()
        if len(names) != len(set(names)) or any(Path(n).name != n or '\\' in n for n in names):
            raise ValueError('Duplicate or unsafe archive member names.')
        metadata = z.read(META)
        if b'<!DOCTYPE' in metadata.upper() or b'<!ENTITY' in metadata.upper():
            raise ValueError('XML entity declarations are not accepted.')
        root = ET.fromstring(metadata)
        if root.findtext('.//ObjectShortName') != TASK_CODE:
            raise ValueError('Export metadata does not identify the expense-template task.')
        objects = {}
        for row in root.findall('.//MigrationProcessBusinessObjectCSVMetadataVORow'):
            name = row.findtext('BusinessObjectShortName')
            if name in objects:
                raise ValueError('Duplicate business-object metadata.')
            objects[name] = {'node_path': row.findtext('XmlNodePath'),
                             'attributes': (row.findtext('XmlAttributeList') or '').split(','),
                             'types': (row.findtext('XmlAttributeTypeList') or '').split(',')}
        members = {}
        for name in names:
            if not name.lower().endswith('.csv'):
                continue
            reader = csv.reader(io.StringIO(z.read(name).decode('utf-8-sig')))
            headers = next(reader, [])
            if not headers or len(headers) != len(set(headers)):
                raise ValueError('Missing or duplicate headers in ' + name)
            obj = objects.get(name[:-4])
            if not obj or len(obj['attributes']) != len(obj['types']):
                raise ValueError('Missing or malformed metadata for ' + name)
            if any(a not in headers for a in obj['attributes']):
                raise ValueError('CSV and metadata disagree for ' + name)
            if any(len(row) != len(headers) for row in reader):
                raise ValueError('CSV row width mismatch for ' + name)
            members[name] = {'headers': headers, **obj}
        for name, node_path in CHILD_PATHS.items():
            if name not in members or members[name]['node_path'] != node_path:
                raise ValueError('Unverified child relationship: ' + name)
            if any(h not in members[name]['headers'] for h in PARENT_HEADERS):
                raise ValueError('Missing child parent-reference headers: ' + name)
    return {'task_code': TASK_CODE, 'archive_sha256': hashlib.sha256(content).hexdigest(),
            'release': root.findtext('.//ProcessRelease'), 'members': members,
            'limitations': [
                'Itemization Include=No/removal and mapping Effective End Date have no columns in the observed itemization CSV. Do not invent them or assume row omission deletes a mapping.',
                'Project mappings are outside the current v1.5 workbook/import contract because every imported expense type has Projects disabled.',
                'The current v1.5 workbook/import contract writes account-related and tax values as null; it does not resolve the natural-account segment qualifier or collect tax fields.',
                'Headers and XML paths alone do not establish deletion semantics or reference-code validity.'
            ]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--export-zip', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = inspect_schema(args.export_zip)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as output:
        json.dump(result, output, indent=2)
        output.write('\n')
    print(json.dumps({'status': 'schema_inspected', 'csv_members': len(result['members']),
                      'limitations': len(result['limitations'])}))


if __name__ == '__main__':
    main()
