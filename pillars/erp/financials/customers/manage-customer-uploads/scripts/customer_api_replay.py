"""Recompute retained API projections offline; never perform a fallback network read."""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import tempfile

import customers_package as package
import customer_api_collect as collector
import customer_api_effect_review as effects


class RecordedClient:
    def __init__(self, directory, report, inspect_soap):
        self.directory, self.report, self.inspect_soap = Path(directory), report, inspect_soap
        self.records, self.used = {}, set()
        for item in report['captures']:
            key = package.fingerprint([item['kind'], item['operation_or_path'], item['selectors']])
            package.require(key not in self.records, 'API_REPLAY_DUPLICATE_REQUEST')
            self.records[key] = item

    def read(self, kind, route, selectors, output):
        key = package.fingerprint([kind, route, selectors])
        package.require(key in self.records, 'API_REPLAY_CAPTURE_MISSING_NO_NETWORK_FALLBACK')
        item = self.records[key]
        raw = (self.directory/item['response_file']).read_bytes()
        package.require(hashlib.sha256(raw).hexdigest() == item['response_sha256'], 'API_REPLAY_CAPTURE_CHANGED')
        manifest = None
        if kind == 'soap':
            inspected = self.inspect_soap(raw, route, **{k.replace('-', '_'): v for k, v in selectors.items()})
            retained = item['core_manifest']
            package.require(isinstance(retained, dict) and retained.get('read_only') is True and
                retained.get('environment_url') == self.report['environment_url'] and
                all(retained.get(k) == v for k, v in inspected.items()), 'API_REPLAY_CORE_MANIFEST_MISMATCH')
            manifest = {**inspected, 'read_only': True, 'environment_url': self.report['environment_url']}
        with Path(output).open('xb') as stream:
            stream.write(raw)
        self.used.add(key)
        return raw, manifest

    def rest(self, route, selectors, output):
        return self.read('rest', route, selectors, output)[0]

    def soap(self, route, selectors, output):
        return self.read('soap', route, selectors, output)


def recompute(directory, candidate, inspect_soap):
    retained = effects.retained_collection(directory)
    package.require(package.inspect_candidate(candidate, retained['operation_intent'])['candidate_sha256'] ==
                    retained['candidate_sha256'], 'API_REPLAY_CANDIDATE_MISMATCH')
    client = RecordedClient(directory, retained, inspect_soap)
    with tempfile.TemporaryDirectory(prefix='customer-api-replay-') as temporary:
        result = collector.collect(candidate, retained['operation_intent'], retained['environment_url'],
            retained['phase'], Path(temporary)/'recomputed', client, max_requests=retained['request_limit'])
    package.require(client.used == set(client.records), 'API_REPLAY_UNUSED_CAPTURE')
    for key in ('rows', 'reference_review_sha256', 'all_reference_owners_resolved'):
        package.require(result[key] == retained[key], 'API_REPLAY_PROJECTED_SUMMARY_MISMATCH')
    # Preserve original capture times. Reprocessing is not fresh collection or
    # independent server authentication. Never rewrite the retained directory.
    implementation = result['task_implementation_sha256']
    result = copy.deepcopy(retained)
    result['raw_projections_recomputed'] = True
    result['replay_implementation_sha256'] = {
        **implementation,
        'customer_api_replay.py': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    result['fresh_collection_performed'] = False
    return result


def core_inspector(repo):
    # Compatibility name for callers. Parsing is task-owned and pure; never
    # import executable code from a supplied historical checkout.
    from customer_soap_contract import inspect_response
    return inspect_response


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--capture', type=Path, required=True)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        package.require(not args.output.resolve().is_relative_to(args.repo.resolve()),
                        'API_PRIVATE_OUTPUT_OUTSIDE_REPOSITORY_REQUIRED')
        report = recompute(args.capture, args.candidate.read_bytes(), core_inspector(args.repo))
        collector.save(args.output, report)
        print(json.dumps({'status': 'RETAINED_API_PROJECTIONS_RECOMPUTED',
            'capture_count': report['capture_count'], 'fresh_collection_performed': False}))
        return 0
    except Exception as exc:
        print(json.dumps({'status': 'API_REPLAY_INCOMPLETE', 'error_type': type(exc).__name__,
            'error_code': str(exc) if isinstance(exc, package.InvalidInput) else 'REPLAY_REVIEW_REQUIRED',
            'network_fallback': False, 'execution_authorized': False}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
