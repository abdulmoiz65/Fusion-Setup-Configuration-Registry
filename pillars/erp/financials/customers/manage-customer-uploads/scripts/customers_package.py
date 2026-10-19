"""Customers positional package utilities; no Fusion execution capability.

Exercises reviewed template mechanics only. Every result retains semantic and
runtime blockers. It has no authentication, upload, ESS, or import capability.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import stat
import zipfile
from datetime import datetime
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
MEMBER = 'ArUpdCustomers.csv'
LIMIT = 16 * 1024 * 1024  # Local inspection budget, never a product volume limit.


class InvalidInput(ValueError):
    pass


def require(condition, code):
    if not condition:
        raise InvalidInput(code)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'DUPLICATE_JSON_KEY')
        result[key] = value
    return result


def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique_object)


def columns():
    contract = load_json(ROOT / 'assets/customer-contract.json')
    names = [c['name'] for c in contract['columns']]
    require(len(names) == 87 and len(set(names)) == 87, 'INVALID_LAYOUT_CONTRACT')
    return names


def normalize(document):
    require(isinstance(document, dict), 'INPUT_OBJECT_REQUIRED')
    require(set(document) == {'schema_version', 'operation', 'provenance', 'Customers'},
            'UNKNOWN_OR_MISSING_INPUT_SECTION')
    require(document['schema_version'] == 'ar-customers-input-v1', 'INPUT_SCHEMA')
    require(document['operation'] in {'create', 'update', 'mixed'}, 'OPERATION_OUT_OF_SCOPE')
    require(isinstance(document['provenance'], str)
            and document['provenance'] in {'explicit-business-input', 'proposed-business-input'},
            'EXPLICIT_INPUT_REQUIRED')
    rows = document['Customers']
    require(isinstance(rows, list) and bool(rows), 'CUSTOMERS_ROWS_REQUIRED')
    names = columns()
    result = []
    for row_number, row in enumerate(rows, 1):
        require(isinstance(row, dict) and bool(row), f'ROW_{row_number}_OBJECT_REQUIRED')
        require(set(row) <= set(names), f'ROW_{row_number}_UNKNOWN_FIELD')
        values = []
        for name in names:
            value = row.get(name)
            require(value is None or isinstance(value, str),
                    f'ROW_{row_number}_{name}_TEXT_OR_NULL_REQUIRED')
            value = '' if value is None else value
            require('\x00' not in value, f'ROW_{row_number}_{name}_NUL_CHARACTER')
            values.append(value)
        require(any(value.strip() for value in values), f'ROW_{row_number}_BLANK_ROW')
        result.append(values)
    return result


def emit(rows):
    stream = io.StringIO(newline='')
    writer = csv.writer(stream, lineterminator='\r\n', quoting=csv.QUOTE_MINIMAL)
    for row in rows:
        require(len(row) == 87, 'BUSINESS_COLUMN_COUNT')
        require(all(isinstance(v, str) for v in row), 'TEXT_FIELDS_REQUIRED')
        writer.writerow([*row, 'END'])
    data = stream.getvalue().encode('utf-8')
    inspect_csv(data)
    return data


def check_quotes(text):
    """Reject malformed RFC-style quoting tolerated by csv.reader(strict=True)."""
    state = 'start'
    for char in text:
        if state == 'quoted':
            if char == '"':
                state = 'after_quote'
        elif state == 'after_quote':
            if char == '"':
                state = 'quoted'
            elif char in ',\r\n':
                state = 'start'
            else:
                raise InvalidInput('MALFORMED_CSV_QUOTE')
        elif state == 'start':
            if char == '"':
                state = 'quoted'
            elif char not in ',\r\n':
                state = 'plain'
        elif char == '"':
            raise InvalidInput('MALFORMED_CSV_QUOTE')
        elif char in ',\r\n':
            state = 'start'
    require(state != 'quoted', 'UNTERMINATED_CSV_QUOTE')


def inspect_csv(data):
    require(len(data) <= LIMIT, 'LOCAL_INSPECTION_LIMIT_REQUIRES_STREAMING_REVIEW')
    require(not data.startswith(b'\xef\xbb\xbf'), 'UTF8_BOM_NOT_ALLOWED')
    try:
        text = data.decode('utf-8', errors='strict')
    except UnicodeDecodeError as exc:
        raise InvalidInput('INVALID_UTF8') from exc
    require('\x00' not in text, 'NUL_CHARACTER')
    check_quotes(text)
    try:
        rows = list(csv.reader(io.StringIO(text, newline=''), strict=True))
    except csv.Error as exc:
        raise InvalidInput('MALFORMED_CSV') from exc
    require(bool(rows), 'CUSTOMERS_ROWS_REQUIRED')
    names = columns()
    result = []
    for row_number, row in enumerate(rows, 1):
        require(len(row) == 88, f'ROW_{row_number}_SERIALIZED_COLUMN_COUNT')
        require(row[-1] == 'END', f'ROW_{row_number}_END_TRAILER')
        require(row[:-1] != names, 'HEADER_NOT_ALLOWED')
        require(any(v.strip() for v in row[:-1]), f'ROW_{row_number}_BLANK_ROW')
        result.append(row[:-1])
    return result


def pack(data):
    inspect_csv(data)
    stream = io.BytesIO()
    info = zipfile.ZipInfo(MEMBER, (1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_STORED
    info.create_system = 3
    info.external_attr = (stat.S_IFREG | 0o600) << 16
    with zipfile.ZipFile(stream, 'w') as archive:
        archive.writestr(info, data)
    return stream.getvalue()


def inspect_zip(data):
    require(len(data) <= LIMIT, 'LOCAL_INSPECTION_LIMIT_REQUIRES_STREAMING_REVIEW')
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            entries = archive.infolist()
            require(len(entries) == 1 and entries[0].filename == MEMBER, 'EXACT_CUSTOMERS_MEMBER_REQUIRED')
            entry = entries[0]
            require(not entry.flag_bits & 1, 'ENCRYPTED_MEMBER')
            mode = entry.external_attr >> 16
            require(stat.S_IFMT(mode) in (0, stat.S_IFREG), 'NONREGULAR_MEMBER')
            require(entry.file_size <= LIMIT, 'LOCAL_INSPECTION_LIMIT_REQUIRES_STREAMING_REVIEW')
            return inspect_csv(archive.read(entry))
    except (zipfile.BadZipFile, NotImplementedError, RuntimeError) as exc:
        raise InvalidInput('INVALID_ZIP') from exc


def contract():
    return load_json(ROOT / 'assets/customer-contract.json')


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     ensure_ascii=False, allow_nan=False).encode('utf-8')).hexdigest()


def validate_business(rows):
    """Known template input checks; no inferred environment values or product defaults."""
    definition = contract()
    names = columns()
    party_values, account_values = {}, {}
    party_fields = ['PARTY_NAME', 'DUNS_NUMBER', 'TAXPAYER_ID_NUM', 'TAXPAYER_REGISTRATION_NUM', 'GSA_INDICATOR_FLAG']
    account_fields = ['PARTY_NUMBER', 'ACCOUNT_DESCRIPTION', 'ACCOUNT_TYPE', 'ACCOUNT_ESTABLISHED_DATE',
                      'CUSTOMER_CLASS', 'CUSTOMER_PROFILE_CLASS', 'ATTRIBUTE_CATEGORY'] + [f'ATTRIBUTE{i}' for i in range(1, 31)]
    for number, values in enumerate(rows, 1):
        require(len(values) == 87, 'BUSINESS_COLUMN_COUNT')
        row = dict(zip(names, values))
        for field in definition['columns']:
            value = row[field['name']]
            prefix = f"ROW_{number}_{field['name']}"
            require(not field['required'] or bool(value.strip()), prefix + '_REQUIRED')
            if field.get('max_characters'):
                require(len(value) <= field['max_characters'], prefix + '_LENGTH')
            if field.get('max_utf8_bytes'):
                require(len(value.encode('utf-8')) <= field['max_utf8_bytes'], prefix + '_BYTE_LENGTH')
            if value and field.get('allowed_values'):
                require(value in field['allowed_values'], prefix + '_DOMAIN')
        date = row['ACCOUNT_ESTABLISHED_DATE']
        if date:
            require(bool(re.fullmatch(r'\d{4}/\d{2}/\d{2}', date)), f'ROW_{number}_DATE_FORMAT')
            try:
                datetime.strptime(date, '%Y/%m/%d')
            except ValueError as exc:
                raise InvalidInput(f'ROW_{number}_INVALID_DATE') from exc
        # Ambiguous supplied parent definitions are an input-consistency issue,
        # not a product uniqueness rule or a prohibition on repeated parents.
        for cache, key, fields, entity in (
            (party_values, (row['ORIG_SOURCE_SYSTEM_NAME'], row['PARTY_NUMBER']), party_fields, 'PARTY'),
            (account_values, (row['ORIG_SOURCE_SYSTEM_NAME'], row['ACCOUNT_NUMBER']), account_fields, 'ACCOUNT')):
            prior = cache.setdefault(key, {})
            for field in fields:
                value = row[field]
                if value:
                    require(field not in prior or prior[field] == value,
                            f'ROW_{number}_CONFLICTING_{entity}_{field}')
                    prior[field] = value
    return rows


def report(rows, data, operation):
    require(operation in {'create', 'update', 'mixed'}, 'EXPLICIT_OPERATION_INTENT_REQUIRED')
    # Reviewed 26D CK_ASU_LKUP_SET_ID explicitly rejects COMMON on insert.
    # Scope this rule to declared creation; update/mixed still require their
    # separate per-entity target review. Do not default another set or casing.
    if operation == 'create':
        set_index = columns().index('ACCT_ADDRESS_SET_CODE')
        for number, row in enumerate(rows, 1):
            require(row[set_index] != 'COMMON',
                    f'ROW_{number}_ACCT_ADDRESS_SET_CODE_COMMON_INSERT_UNSUPPORTED')
    definition = contract()
    return {
        'schema_version': 'ar-customers-preview-v1', 'status': 'OFFLINE_PREVIEW_LIVE_BLOCKED',
        'task_code': definition['task_code'], 'business_object': definition['business_object'],
        'operation_intent': operation, 'member': MEMBER, 'row_count': len(rows),
        'business_columns': 87, 'serialized_columns': 88,
        'candidate_sha256': hashlib.sha256(data).hexdigest(), 'contract_sha256': fingerprint(definition),
        'known_input_checks': 'PASS', 'execution_authorized': False, 'live_ready': False,
        'semantic_validation_complete': False,
        'loader_validation_gaps': definition['loader_validation_gaps'],
        'live_blockers': definition['live_blockers'],
        'note': 'A preview is not a supported-field update declaration or approval; central live gates remain open.'}


def inspect_candidate(data, operation):
    rows = validate_business(inspect_zip(data))
    return report(rows, data, operation)


def preview(document, output):
    rows = validate_business(normalize(document))
    data = pack(emit(rows))
    require(inspect_zip(data) == rows, 'ROUND_TRIP_MISMATCH')
    result = report(rows, data, document['operation'])
    result.update(input_provenance=document['provenance'],
                  input_sha256=fingerprint(document),
                  proposed_data_requires_approval=document['provenance'] == 'proposed-business-input')
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    (output / 'candidate.zip').write_bytes(data)
    (output / 'preview.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    return result


def review(data, operation, context, acceptance=None):
    result = inspect_candidate(data, operation)
    require(isinstance(context, dict) and set(context) == {
        'environment_url', 'preview_id', 'registration_sha256', 'arguments_sha256'}, 'EXACT_CENTRAL_CONTEXT_REQUIRED')
    require(all(isinstance(v, str) and v.strip() for v in context.values()), 'CONTEXT_VALUES_REQUIRED')
    url = urlsplit(context['environment_url'])
    require(url.scheme == 'https' and bool(url.hostname) and not url.username and not url.password
            and not url.query and not url.fragment and url.path in {'', '/'}, 'INVALID_ENVIRONMENT_ORIGIN')
    for name in ('registration_sha256', 'arguments_sha256'):
        require(bool(re.fullmatch('[0-9a-f]{64}', context[name])), 'INVALID_CONTEXT_FINGERPRINT')
    binding = {key: result[key] for key in ('task_code', 'business_object', 'operation_intent',
                                            'candidate_sha256', 'contract_sha256')}
    binding.update(context)
    binding['gap_set_sha256'] = fingerprint(result['loader_validation_gaps'])
    result.update(binding=binding, acceptance_record_matches=False,
                  status='AWAITING_LOADER_VALIDATION_ACCEPTANCE_LIVE_BLOCKED')
    if acceptance is None:
        return result
    require(isinstance(acceptance, dict) and set(acceptance) == {
        'schema_version', 'decision', 'binding', 'accepted_by', 'accepted_at', 'decision_reference'},
        'EXACT_ACCEPTANCE_RECORD_REQUIRED')
    require(acceptance['schema_version'] == 'fscr-fbdi-loader-validation-acceptance-v1'
            and acceptance['decision'] == 'accept_loader_validation', 'EXPLICIT_ACCEPTANCE_REQUIRED')
    require(acceptance['binding'] == binding, 'STALE_OR_MISMATCHED_ACCEPTANCE')
    for name in ('accepted_by', 'accepted_at', 'decision_reference'):
        require(isinstance(acceptance[name], str) and bool(acceptance[name].strip()), 'ACCEPTANCE_PROVENANCE_REQUIRED')
    try:
        timestamp = datetime.fromisoformat(acceptance['accepted_at'].replace('Z', '+00:00'))
    except ValueError as exc:
        raise InvalidInput('ACCEPTANCE_TIMESTAMP') from exc
    require(timestamp.tzinfo is not None, 'ACCEPTANCE_TIMESTAMP_TIMEZONE')
    result.update(status='ACCEPTANCE_RECORDED_LIVE_BLOCKED', acceptance_record_matches=True)
    result['authority'] = 'Local record match only. Central workflow authenticates the actor, verifies context and permissions, and owns import approval. Remaining hard gates cannot be waived.'
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    build = commands.add_parser('preview')
    build.add_argument('--input', type=Path, required=True)
    build.add_argument('--output-dir', type=Path, required=True)
    for name in ('inspect', 'review'):
        sub = commands.add_parser(name)
        sub.add_argument('--zip', type=Path, required=True)
        sub.add_argument('--operation', choices=['create', 'update', 'mixed'], required=True)
        if name == 'review':
            sub.add_argument('--context', type=Path, required=True)
            sub.add_argument('--acceptance', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'preview':
            result = preview(load_json(args.input), args.output_dir)
        else:
            require(args.zip.stat().st_size <= LIMIT, 'LOCAL_INSPECTION_LIMIT_REQUIRES_STREAMING_REVIEW')
            data = args.zip.read_bytes()
            result = (inspect_candidate(data, args.operation) if args.command == 'inspect' else
                      review(data, args.operation, load_json(args.context),
                             load_json(args.acceptance) if args.acceptance else None))
        print(json.dumps(result, indent=2))
        return 2 if args.command == 'review' else 0  # Hard live gates remain open even after acceptance.
    except (OSError, ValueError) as exc:
        code = str(exc) if isinstance(exc, InvalidInput) else type(exc).__name__
        print(json.dumps({'status': 'BLOCKED', 'error': code, 'execution_authorized': False}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
