"""Fixed Customer Upload attempt GETs through the unchanged core REST CLI.

No submission, polling, authentication implementation or execution authority.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

import customers_package as package
import customer_attempt_review as review
from customer_api_collect import CentralCli

ROOT = '/hcmRestApi/resources/latest/dataLoaderDataSets'
PATH = re.compile(re.escape(ROOT) + r'(?:/[1-9][0-9]*/child/(?:processes|fbdiBusinessObjects(?:/[1-9][0-9]*/child/fbdiErrorMessages)?))?')


class AttemptClient(CentralCli):
    def rest(self, path, query, output):
        package.require(PATH.fullmatch(path) is not None, 'ATTEMPT_READ_PATH')
        args = [path, '--method', 'GET', '--header', 'Accept-Language=en']
        for key, value in sorted(query.items()):
            args += ['--query', key + '=' + str(value)]
        return self._run('fusion_rest_client.py', args, output)


def save(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def collect(candidate, operation, environment, binding, output, client, *, max_requests=64):
    now = lambda: datetime.now(timezone.utc).isoformat()
    observation = {'schema_version': 'ar-customer-task-status-evidence-v1',
        'binding_sha256': package.fingerprint(binding), 'environment_url': environment,
        'captured_at': now(), 'evidence_reference': 'observation.json',
        'task_status': {'RequestId': binding.get('initiation_request_id'),
            'dataSetCount': 0, 'queriedDataSetIds': [], 'dataSets': [], 'fbdiDiagnostics': []}}
    # Validate candidate, origin, immutable binding, IDs and time before any call.
    review.analyze(candidate, operation, environment, binding, observation)
    package.require(type(max_requests) is int and 1 <= max_requests <= 128, 'ATTEMPT_REQUEST_BOUND')
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    save(output/'binding.json', binding)
    captures = []
    def pages(path, query):
        rows = []
        seen_pages = set()
        for _ in range(20):
            package.require(len(captures) < max_requests, 'ATTEMPT_REQUEST_LIMIT')
            selectors = {**query, 'onlyData': 'true', 'limit': '100', 'offset': str(len(rows))}
            name = 'response-' + str(len(captures)) + '.json'
            raw = client.rest(path, selectors, output/name)
            package.require(isinstance(raw, bytes) and len(raw) <= 16*1024*1024
                            and (output/name).read_bytes() == raw, 'ATTEMPT_RESPONSE_RETENTION')
            capture = {'path': path, 'query': selectors, 'response_file': name,
                'response_sha256': hashlib.sha256(raw).hexdigest(), 'captured_at': now(),
                'binding_sha256': observation['binding_sha256']}
            captures.append(capture)
            save(output/(name+'.capture.json'), capture)
            data = json.loads(raw)
            package.require(isinstance(data, dict) and isinstance(data.get('items'), list)
                and type(data.get('hasMore')) is bool and all(isinstance(x, dict) for x in data['items']),
                'ATTEMPT_PAGE_SCHEMA')
            fingerprint = package.fingerprint(data['items'])
            package.require(fingerprint not in seen_pages, 'ATTEMPT_REPEATED_PAGE')
            seen_pages.add(fingerprint)
            rows.extend(data['items'])
            if not data['hasMore']:
                return rows
            package.require(bool(data['items']), 'ATTEMPT_EMPTY_CONTINUATION')
        raise package.InvalidInput('ATTEMPT_PAGE_LIMIT')
    try:
        datasets = pages(ROOT, {'q': 'DataSetRequestId=' + binding['initiation_request_id']})
        package.require(len(datasets) == 1, 'ATTEMPT_DATASET_AMBIGUOUS')
        dataset = datasets[0]
        ds = review.identifier(dataset.get('DataSetId'))
        package.require(ds and dataset.get('SourceType') == 'FBDI'
            and review.identifier(dataset.get('DataSetRequestId')) == binding['initiation_request_id']
            and dataset.get('UcmContentId') == binding['content_id'], 'ATTEMPT_DATASET_BINDING')
        status = observation['task_status']
        status.update(dataSets=datasets, dataSetCount=1, queriedDataSetIds=[ds])
        base = ROOT + '/' + ds + '/child/'
        objects = pages(base+'fbdiBusinessObjects', {})
        package.require(len(objects) == 1 and objects[0].get('BusinessObjectName') == 'customers',
                        'ATTEMPT_CUSTOMERS_OBJECT')
        obj = objects[0]
        object_id = review.identifier(obj.get('DataSetBusObjId'))
        package.require(object_id and ('DataSetId' not in obj or review.identifier(obj['DataSetId']) == ds),
                        'ATTEMPT_OBJECT_PARENT')
        processes = pages(base+'processes', {})
        ids = [review.identifier(x.get('ProcessId')) for x in processes]
        package.require(None not in ids and len(ids) == len(set(ids)) and
            all(review.identifier(x.get('DataSetId')) == ds for x in processes), 'ATTEMPT_PROCESS_PARENT')
        errors = pages(base+'fbdiBusinessObjects/'+object_id+'/child/fbdiErrorMessages', {})
        package.require(all(('DataSetBusObjId' not in x or review.identifier(x['DataSetBusObjId']) == object_id)
            and ('DataSetId' not in x or review.identifier(x['DataSetId']) == ds) for x in errors),
            'ATTEMPT_ERROR_PARENT')
        status['fbdiDiagnostics'] = [{'dataSetId': ds, 'collectionComplete': True,
            'sectionErrors': [], 'businessObjects': [{'record': obj, 'errors': errors,
            'errorsComplete': True}], 'processes': processes}]
        observation['captured_at'] = now()
        result = review.analyze(candidate, operation, environment, binding, observation)
        save(output/'observation.json', observation)
        save(output/'review.json', result)
        save(output/'captures.json', captures)
        return result
    except Exception:
        save(output/'incomplete.json', {'status': 'ATTEMPT_CAPTURE_INCOMPLETE',
            'binding_sha256': observation['binding_sha256'], 'captures': captures,
            'execution_authorized': False, 'retry_authorized': False})
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('repo', 'properties', 'token-cache', 'environment', 'candidate', 'operation', 'binding', 'output'):
        parser.add_argument('--'+name, required=True)
    args = parser.parse_args()
    binding = json.loads(Path(args.binding).read_text(encoding='utf-8'))
    client = AttemptClient(args.repo, args.properties, args.token_cache, args.environment)
    result = collect(Path(args.candidate).read_bytes(), args.operation, args.environment, binding, args.output, client)
    print(json.dumps(result, indent=2))
    return 0 if result['request_association_matches'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
