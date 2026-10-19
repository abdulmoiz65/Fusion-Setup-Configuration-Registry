"""Collect candidate-bound, read-only observations through the central API CLIs.

This is an explicitly selected assisted read step, never import approval or a
replacement for unresolved pre-import matching or complete effect reconciliation.
"""
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
import argparse
import hashlib
import json
import re
import subprocess
import sys

import customers_package as package
import customer_api_snapshot as snapshot
import customer_api_hierarchy as hierarchy
import customer_api_location_review as locations
import customer_api_receipt_review as receipts
import customer_api_tax_review as tax
import customer_api_dff_review as dff
import customer_api_profile_set_review as profile_sets
import customer_api_business_values as business_values

CRM = '/crmRestApi/resources/11.13.18.05/'
RECEIPTS = '/fscmRestApi/resources/11.13.18.05/receiptMethodAssignments'
TAX = '/fscmRestApi/resources/11.13.18.05/partyTaxProfiles'
ADDRESS_FIELDS = 'AddressId,AddressNumber,LocationId,PartyId,PartyNumber,PartySiteName,Address1,City,State,PostalCode,Country,Status'
PURPOSE_FIELDS = 'AddressId,AddressPurposeId,Purpose,Status'


def save(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


class CentralReadFailure(Exception):
    pass


class CentralCli:
    """Selected REST GETs and task-owned SOAP reads reuse existing core clients."""
    def __init__(self, repo, properties, token_cache, environment_url):
        self.repo = Path(repo).resolve()
        self.scripts = self.repo/'core/fusion-api/rest-api-client/scripts'
        package.require(all((self.scripts/name).is_file() for name in
            ('fusion_rest_client.py', 'rest_client_common.py')),
            'API_CENTRAL_CLIENTS_REQUIRED')
        self.properties, self.token_cache = Path(properties).resolve(), Path(token_cache).resolve()
        # Use the central parser; never persist the profile or its values.
        sys.path.insert(0, str(self.scripts))
        from rest_client_common import read_properties
        props = read_properties(self.properties)
        package.require(props.get('restBaseUrl', '').rstrip('/') == environment_url.rstrip('/'),
                        'API_PROFILE_ENVIRONMENT_MISMATCH')
        self.environment_url = environment_url.rstrip('/')
        del props

    def _run(self, script, args, output):
        command = [sys.executable, str(self.scripts/script), *args,
            '--properties', str(self.properties), '--token-cache', str(self.token_cache),
            '--no-open-browser', '--callback-timeout', '1', '--timeout', '30', '--output', str(output)]
        try:
            result = subprocess.run(command, cwd=self.repo, capture_output=True,
                text=True, encoding='utf-8', timeout=75, shell=False)
        except subprocess.TimeoutExpired as exc:
            raise CentralReadFailure('CENTRAL_READ_TIMEOUT') from exc
        if result.returncode or not output.is_file():
            # Never copy auth URLs, tokens, response bodies or arbitrary stderr.
            combined = result.stdout+'\n'+result.stderr
            category = next((f'HTTP_{code}' for code in (401, 403, 404, 429, 500, 503)
                if f'HTTP Error {code}' in combined or f'"http_status": {code}' in combined),
                'CENTRAL_READ_NOT_COMPLETED')
            raise CentralReadFailure(category)
        package.require(output.stat().st_size <= 16*1024*1024, 'API_RESPONSE_SIZE_LIMIT')
        return output.read_bytes()

    def soap(self, operation, selectors, output):
        allowed = {'source-system-by-name': {'source-name'}, 'customer-account': {'account-id'},
                   'organization-by-number': {'party-number'},
                   'organization-by-site-number': {'site-number'},
                   'customer-account-by-number': {'account-number'},
                   'active-customer-profile': {'account-id', 'account-number'}, 'location': {'location-id'}}
        package.require(operation in allowed and set(selectors) == allowed[operation], 'API_SOAP_SELECTOR_CONTRACT')
        # Customer XML mapping is task-owned; OAuth and transport remain core.
        import customer_soap_read as adapter
        package.require(not Path(output).exists(), 'API_NEW_RESPONSE_PATH_REQUIRED')
        try:
            raw, manifest = adapter.read(adapter.load_core(self.repo), self.properties,
                self.token_cache, self.environment_url, operation, selectors)
        except adapter.ReadContractError as exc:
            raise CentralReadFailure(str(exc)) from None
        with Path(output).open('xb') as stream:
            stream.write(raw)
        return raw, manifest

    def rest(self, path, query, output):
        from customer_rest_identity import ORGANIZATIONS, ACCOUNT_SITES
        package.require(path in (snapshot.RESOURCE, RECEIPTS, TAX, dff.RESOURCE, ORGANIZATIONS, ACCOUNT_SITES) or
            path.startswith(CRM+'hubOrganizations/'), 'API_READ_PATH_NOT_SELECTED')
        args = [path, '--method', 'GET', '--header', 'Accept-Language=en']
        for key, value in sorted(query.items()):
            args += ['--query', key+'='+str(value)]
        return self._run('fusion_rest_client.py', args, output)


def collect(candidate, operation, environment_url, phase, output, client, *, max_requests=256):
    """The injectable client owns central reads; fixtures need no network or SQL."""
    package.require(phase in ('before', 'after'), 'API_CAPTURE_PHASE_REQUIRED')
    package.require(type(max_requests) is int and 1 <= max_requests <= 256, 'API_REQUEST_BOUND')
    inspection = package.inspect_candidate(candidate, operation)
    # Validate the origin and rows before creating output or calling a client.
    snapshot.plan(candidate, operation, environment_url, {})
    rows = [dict(zip(package.columns(), row)) for row in package.inspect_zip(candidate)]
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    binding = {'schema_version': 'ar-customer-api-collection-v1',
        'candidate_sha256': inspection['candidate_sha256'], 'operation_intent': operation,
        'environment_url': environment_url.rstrip('/'), 'phase': phase,
        'started_at': datetime.now(timezone.utc).isoformat(), 'request_limit': max_requests,
        'read_only': True, 'execution_authorized': False, 'persisted_reconciliation_complete': False}
    import customer_soap_contract, customer_soap_read
    modules = [Path(module.__file__) for module in (package, snapshot, hierarchy, locations, receipts, tax, dff, profile_sets, business_values, customer_soap_contract, customer_soap_read)] + [Path(__file__)]
    implementation = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in modules}
    binding['task_implementation_sha256'] = implementation
    save(output/'binding.json', binding)
    captures, cache = [], {}

    def read(kind, operation_or_path, selectors):
        key = package.fingerprint([kind, operation_or_path, selectors])
        if key in cache:
            return cache[key]
        package.require(len(captures) < max_requests, 'API_REQUEST_LIMIT_REACHED')
        name = 'read-'+str(len(captures))+('.xml' if kind == 'soap' else '.json')
        path = output/name
        core = None
        if kind == 'soap':
            raw, core = client.soap(operation_or_path, selectors, path)
            package.require(core.get('environment_url') == binding['environment_url'], 'API_CAPTURE_ENVIRONMENT_MISMATCH')
        else:
            raw = client.rest(operation_or_path, selectors, path)
        # The real central CLI writes the response; fixture clients use the same contract.
        package.require(path.is_file() and path.read_bytes() == raw, 'API_RESPONSE_NOT_RETAINED')
        package.require(isinstance(raw, bytes) and len(raw) <= 16*1024*1024, 'API_RESPONSE_SIZE_LIMIT')
        capture = {'binding_sha256': package.fingerprint(binding), 'kind': kind,
            'operation_or_path': operation_or_path, 'selectors': selectors,
            'response_file': name, 'response_sha256': hashlib.sha256(raw).hexdigest(),
            'captured_at': datetime.now(timezone.utc).isoformat(), 'accept_language': 'en',
            'core_manifest': core, 'principal': 'CORE_AUTHENTICATED_PRINCIPAL_NOT_INDEPENDENTLY_ASSERTED'}
        save(output/(name+'.capture.json'), capture)
        captures.append(capture)
        cache[key] = raw, core
        return raw, core

    def pages(path, query, scope=None):
        result, offset = [], 0
        for _ in range(20):
            raw, _ = read('rest', path, {**query, 'limit': '100', 'offset': str(offset)})
            result.append(json.loads(raw))
            records, complete = (snapshot.scoped_pages(result, scope) if scope is not None
                                 else hierarchy.collection(result))
            if complete:
                return result
            offset = len(records)
        raise CentralReadFailure('API_PAGINATION_LIMIT_REACHED')

    try:
        sources = {}
        for source in sorted({row['ORIG_SOURCE_SYSTEM_NAME'] for row in rows}):
            _, manifest = read('soap', 'source-system-by-name', {'source-name': source})
            package.require(manifest.get('source_system_name') == source and
                            manifest.get('source_system_code'), 'API_SOURCE_NAME_CAPTURE_MISMATCH')
            sources[source] = manifest['source_system_code']
        plan = snapshot.plan(candidate, operation, environment_url, sources)
        save(output/'reference-plan.json', plan)
        observations = {}
        for query_id, query in plan['queries'].items():
            observations[query_id] = {'history': pages(query['path'], query['history_query'], query['scope']),
                'active': pages(query['path'], query['active_query'], query['scope'])
                    if query['active_query'] is not None else None}
        save(output/'reference-observations.json', observations)
        resolved = snapshot.review(plan, observations)
        save(output/'reference-review.json', resolved)
        reviews = []
        for row, reference in zip(rows, resolved['rows']):
            owners = reference['owners']
            item = {'row': reference['row'], 'owners': owners, 'hierarchy': None,
                    'location': None, 'receipt': None, 'tax': None, 'dff': None, 'account_number': None,
                    'party_number': None, 'site_number': None,
                    'receipt_before': None,
                    'profile_set': None,
                    'account_values': None, 'organization_values': None,
                    'active_profile_observed': False, 'gaps': []}
            for field, key, op, selector in (
                    ('PARTY_NUMBER', 'party_number', 'organization-by-number', 'party-number'),
                    ('PARTY_SITE_NUMBER', 'site_number', 'organization-by-site-number', 'site-number')):
                if not row[field]:
                    item['gaps'].append(field+'_NOT_SUPPLIED_NUMBER_READ_NOT_PLANNED')
                    continue
                organization, found = read('soap', op, {selector: row[field]})
                records = found.get('records')
                package.require(found.get('operation') == 'findOrganization' and
                    found.get('selector') == key and found.get('scope') == 'VISIBLE_ORGANIZATIONS_ONLY' and
                    isinstance(records, list) and type(found.get('visible_result_complete')) is bool,
                    'API_ORGANIZATION_NUMBER_CAPTURE_CONTRACT')
                for record in records:
                    package.require(isinstance(record, dict) and
                        hierarchy.identifier(record.get('PartyId')) is not hierarchy.MISSING and
                        record.get('PartyType') == 'ORGANIZATION' and
                        (key != 'party_number' or record.get('PartyNumber') == row[field]) and
                        isinstance(record.get('matching_sites'), list), 'API_ORGANIZATION_NUMBER_CAPTURE_CONTRACT')
                    for site in record['matching_sites']:
                        package.require(isinstance(site, dict) and site.get('PartySiteNumber') == row[field] and
                            site.get('PartyId') == record['PartyId'] and
                            all(hierarchy.identifier(site.get(k)) is not hierarchy.MISSING
                                for k in ('PartySiteId', 'LocationId')), 'API_SITE_NUMBER_CAPTURE_CONTRACT')
                    if key == 'site_number':
                        package.require(bool(record['matching_sites']), 'API_SITE_NUMBER_CAPTURE_CONTRACT')
                matches = (len(records) == 1 and records[0]['PartyId'] == owners.get('party'))
                site_matches = [site for record in records for site in record['matching_sites']]
                if key == 'site_number':
                    matches = matches and len(site_matches) == 1 and (
                        site_matches[0]['PartySiteId'] == owners.get('party_site') and
                        site_matches[0]['LocationId'] == owners.get('location'))
                status = ('NUMBER_SEARCH_INCOMPLETE_OR_AMBIGUOUS' if not found['visible_result_complete'] or
                          len(records) > 1 or (key == 'site_number' and len(site_matches) > 1) else
                          'NO_VISIBLE_ORGANIZATION_NUMBER_NOT_GLOBAL_ABSENCE' if not records else
                          'NUMBER_AND_SOURCE_OWNERS_MATCH' if matches else 'NUMBER_OWNER_REVIEW_REQUIRED')
                item[key] = {'status': status, 'visible_match_count': len(records),
                    'matching_site_count': len(site_matches), 'scope': found['scope'],
                    'global_absence_proven': False, 'execution_authorized': False}
                if key == 'party_number' and status == 'NUMBER_AND_SOURCE_OWNERS_MATCH':
                    item['organization_values'] = business_values.organization_values(row, owners, organization)
            if row['ACCOUNT_NUMBER']:
                _, found = read('soap', 'customer-account-by-number', {'account-number': row['ACCOUNT_NUMBER']})
                records = found.get('records')
                package.require(found.get('operation') == 'findCustomerAccount' and
                    isinstance(records, list) and type(found.get('visible_result_complete')) is bool and
                    all(isinstance(record, dict) and record.get('AccountNumber') == row['ACCOUNT_NUMBER']
                        and all(hierarchy.identifier(record.get(key)) is not hierarchy.MISSING
                                for key in ('CustomerAccountId', 'PartyId')) for record in records),
                    'API_ACCOUNT_NUMBER_CAPTURE_CONTRACT')
                matches = len(records) == 1 and records[0]['CustomerAccountId'] == owners.get('account') and records[0]['PartyId'] == owners.get('party')
                status = ('NUMBER_SEARCH_INCOMPLETE_OR_AMBIGUOUS' if not found['visible_result_complete'] or len(records) > 1 else
                          'NO_VISIBLE_ACCOUNT_NUMBER_NOT_GLOBAL_ABSENCE' if not records else
                          'ACCOUNT_NUMBER_AND_SOURCE_OWNERS_MATCH' if matches else
                          'ACCOUNT_NUMBER_OWNER_REVIEW_REQUIRED')
                item['account_number'] = {'status': status, 'visible_match_count': len(records),
                    'global_absence_proven': False, 'execution_authorized': False}
            else:
                item['gaps'].append('ACCOUNT_NUMBER_NOT_SUPPLIED_NUMBER_READ_NOT_PLANNED')
            if set(owners) != set(snapshot.OWNERS):
                item['gaps'].append('REFERENCE_OWNERS_UNRESOLVED_NO_ABSENCE_OR_CREATION_CLAIM')
            account = None
            if {'party', 'account'} <= set(owners):
                account, _ = read('soap', 'customer-account', {'account-id': owners['account']})
                item['account_values'] = business_values.account_values(row, owners, account)
                _, actual_context = dff.account_dff(owners['account'], account)
                base_raw, _ = read('rest', dff.RESOURCE, {'x':dff.LOCATOR, 'mode':'verbose'})
                context_metadata = None
                if actual_context is not None and actual_context is not hierarchy.MISSING:
                    context_raw, _ = read('rest', dff.RESOURCE, {'x':dff.LOCATOR, 'mode':'verbose',
                        'discrValue':actual_context, 'includesBaseType':'true'})
                    context_metadata = json.loads(context_raw)
                item['dff'] = dff.review(row, owners['account'], account, json.loads(base_raw), context_metadata)
                profile = None
                if row['ACCOUNT_NUMBER']:
                    profile, _ = read('soap', 'active-customer-profile', {'account-id': owners['account'], 'account-number': row['ACCOUNT_NUMBER']})
                else:
                    item['gaps'].append('ACCOUNT_NUMBER_NOT_SUPPLIED_PROFILE_READ_NOT_PLANNED')
                item['profile_set'] = profile_sets.review(row, owners, account, profile)
                item['active_profile_observed'] = item['profile_set']['profile_observed']
            else:
                item['gaps'].append('ACCOUNT_OR_PARTY_OWNER_UNRESOLVED_ACCOUNT_READ_NOT_PLANNED')
            if 'location' in owners:
                location, _ = read('soap', 'location', {'location-id': owners['location']})
                item['location'] = locations.review(row, owners['location'], location)
            else:
                item['gaps'].append('LOCATION_OWNER_UNRESOLVED_LOCATION_READ_NOT_PLANNED')
            if 'party' in owners:
                profiles = pages(TAX, {'q': 'PartyId='+owners['party'], 'fields': ','.join(tax.FIELDS), 'onlyData': 'true'})
                item['tax'] = tax.review(row, owners['party'], profiles)
            else:
                item['gaps'].append('PARTY_OWNER_UNRESOLVED_TAX_READ_NOT_PLANNED')
            if set(owners) == set(snapshot.OWNERS) and row['PARTY_NUMBER'] and row['PARTY_SITE_NUMBER']:
                path = CRM+'hubOrganizations/'+quote(row['PARTY_NUMBER'], safe='')+'/child/Address'
                addresses = pages(path, {'fields': ADDRESS_FIELDS, 'onlyData': 'true'})
                purposes = pages(path+'/'+quote(row['PARTY_SITE_NUMBER'], safe='')+'/child/AddressPurpose',
                                 {'fields': PURPOSE_FIELDS, 'onlyData': 'true'})
                item['hierarchy'] = hierarchy.review(row, owners, account, addresses, purposes)
            else:
                item['gaps'].append('OWNERS_OR_DISPLAY_NUMBERS_UNRESOLVED_FULL_HIERARCHY_READ_NOT_PLANNED')
            if item['account_number'] and item['account_number']['status'] == 'ACCOUNT_NUMBER_AND_SOURCE_OWNERS_MATCH':
                if re.fullmatch(r'[A-Za-z0-9_. -]+', row['ACCOUNT_NUMBER']):
                    assignments = pages(RECEIPTS, {'finder': 'receiptMethodSearch;CustomerAccountNumber='+row['ACCOUNT_NUMBER'], 'onlyData': 'true'})
                    item['receipt'] = receipts.review(row, assignments, response_language='en')
                    if phase == 'before':
                        item['receipt_before'] = receipts.review_before(row, assignments, response_language='en')
                else:
                    item['gaps'].append('RECEIPT_ACCOUNT_FINDER_LITERAL_UNQUALIFIED')
            else:
                item['gaps'].append('ACCOUNT_NUMBER_OWNER_NOT_CONFIRMED_RECEIPT_READ_NOT_PLANNED')
            reviews.append(item)
        package.require(all(hashlib.sha256(path.read_bytes()).hexdigest() == implementation[path.name]
                            for path in modules), 'API_IMPLEMENTATION_CHANGED_DURING_COLLECTION')
        summary = {**binding, 'status': 'API_OBSERVATIONS_CAPTURED_WITH_LIMITATIONS',
            'finished_at': datetime.now(timezone.utc).isoformat(), 'reference_review_sha256': package.fingerprint(resolved),
            'rows': reviews, 'capture_count': len(captures), 'captures': captures,
            'all_reference_owners_resolved': resolved['all_reference_owners_resolved'],
            'sql_input_used': False, 'full_functional_reconciliation': False,
            'remaining_contracts': ['Complete create/update intent proof; number searches are API-visible only and party/site searches cover organizations only',
                'Unexposed physical DFF values, profile history and raw profile-date semantics',
                'All requested/omitted fields, tax callbacks, sibling/default effects and before/after comparison',
                'Staging/request lineage and independent Journey synchronization']}
        save(output/'collection-review.json', summary)
        return summary
    except Exception as exc:
        safe = {'status': 'READ_INCOMPLETE', 'error_type': type(exc).__name__,
            'error_code': str(exc) if isinstance(exc, (package.InvalidInput, CentralReadFailure)) else 'READ_OR_ARTIFACT_FAILURE',
            'captured_requests': len(captures), 'binding_sha256': package.fingerprint(binding),
            'automatic_retry': False, 'import_submitted': False, 'execution_authorized': False}
        save(output/'failure.json', safe)
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--operation', choices=['create', 'update', 'mixed'], required=True)
    parser.add_argument('--environment-url', required=True)
    parser.add_argument('--phase', choices=['before', 'after'], required=True)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--properties', type=Path, required=True)
    parser.add_argument('--token-cache', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--max-requests', type=int, default=256)
    parser.add_argument('--read-scope', choices=['complete', 'rest-identity'], default='complete',
                        help='Explicit partial REST identity observation; never full reconciliation or import approval.')
    args = parser.parse_args(argv)
    try:
        # Raw tenant observations belong in a private evidence directory, outside the checkout.
        package.require(not args.output.resolve().is_relative_to(args.repo.resolve()), 'API_PRIVATE_OUTPUT_OUTSIDE_REPOSITORY_REQUIRED')
        package.require(not args.output.exists(), 'API_NEW_OUTPUT_DIRECTORY_REQUIRED')
        package.require(1 <= args.max_requests <= 256, 'API_REQUEST_BOUND')
        candidate = args.candidate.read_bytes()
        package.inspect_candidate(candidate, args.operation)
        snapshot.plan(candidate, args.operation, args.environment_url, {})
        if args.read_scope == 'rest-identity':
            import customer_rest_identity
            # All selectors are candidate-bound and checked before profile/auth access.
            customer_rest_identity.selections(candidate, args.operation, args.environment_url)
            client = CentralCli(args.repo, args.properties, args.token_cache, args.environment_url)
            result = customer_rest_identity.collect(candidate, args.operation, args.environment_url,
                                                    args.phase, args.output, client)
            print(json.dumps({'status': result['status'], 'execution_authorized': False,
                              'persisted_reconciliation_complete': False, 'output': str(args.output)}))
            return 0 if result['status'] == 'PARTIAL_REST_IDENTITIES_MATCH' else 2
        client = CentralCli(args.repo, args.properties, args.token_cache, args.environment_url)
        result = collect(candidate, args.operation, args.environment_url, args.phase, args.output, client,
                         max_requests=args.max_requests)
        print(json.dumps({key: result[key] for key in ('status', 'candidate_sha256', 'phase',
            'capture_count', 'all_reference_owners_resolved', 'full_functional_reconciliation')}))
        return 0
    except Exception as exc:
        print(json.dumps({'status': 'READ_INCOMPLETE', 'error_type': type(exc).__name__,
                          'error_code': str(exc) if isinstance(exc, (package.InvalidInput, CentralReadFailure)) else 'READ_OR_ARTIFACT_FAILURE',
                          'next_action': 'Review the selected read inputs, core access and retained diagnostics; no import was submitted.',
                          'execution_authorized': False,
                          'automatic_retry': False, 'import_submitted': False}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
