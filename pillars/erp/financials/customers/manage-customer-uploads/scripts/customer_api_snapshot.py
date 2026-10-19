"""Pure candidate-scoped API planning/review; no HTTP, OAuth, SQL or mutation."""
from datetime import date
import hashlib
import re
from urllib.parse import urlsplit

import customers_package as package
import customer_identity_review as identity
from customer_rest_reference_review import OWNER_ENTITIES, KEY, FIELDS

RESOURCE = '/crmRestApi/resources/11.13.18.05/hubSourceSystemReferences'
PROJECTION = ','.join((*KEY, 'SourceSystemReferenceId', 'OwnerEntityId', 'Status',
                       'StartDateActive', 'EndDateActive'))
OWNERS = {entity: owner for owner, entity in OWNER_ENTITIES.items()}


def literal(value):
    package.require(isinstance(value, str) and bool(value) and
                    all(ord(c) >= 32 for c in value), 'API_QUERY_LITERAL_REQUIRED')
    return "'" + value.replace("'", "''") + "'"


def plan(candidate, operation, environment_url, source_codes):
    """Plan exact tuples from candidate and separately resolved source names.

    source_codes is the result of the selected central source-name read, not a
    guessed name transformation. Its capture/provenance is bound by the collector.
    Missing sources/unsupported finder literals remain explicit unresolved items.
    """
    package.inspect_candidate(candidate, operation)
    origin = urlsplit(environment_url)
    package.require(origin.scheme == 'https' and origin.hostname and not origin.username
                    and not origin.password and not origin.query and not origin.fragment
                    and origin.path in ('', '/'), 'API_ENVIRONMENT_ORIGIN_REQUIRED')
    package.require(isinstance(source_codes, dict) and all(
        isinstance(k, str) and k.strip() and isinstance(v, str) and v.strip()
        for k, v in source_codes.items()), 'API_SOURCE_CODE_MAP_REQUIRED')
    rows = [dict(zip(package.columns(), r)) for r in package.inspect_zip(candidate)]
    package.require(set(source_codes) <= {r['ORIG_SOURCE_SYSTEM_NAME'] for r in rows},
                    'API_UNREQUESTED_SOURCE_NAME')
    queries, row_scopes, unresolved = {}, [], []
    for number, row in enumerate(rows, 1):
        code = source_codes.get(row['ORIG_SOURCE_SYSTEM_NAME'])
        entities = {}
        for entity, key in identity.reference_candidates(row).items():
            if code is None or not key['reference'] or key['lexical_review_required']:
                unresolved.append({'row': number, 'entity': entity, 'status':
                    'SOURCE_NAME_UNRESOLVED' if code is None else
                    'REFERENCE_LEXICAL_REVIEW_REQUIRED' if key['lexical_review_required'] else
                    'NO_REFERENCE_NO_CONTROL_FALLBACK'})
                continue
            scope = dict(zip(KEY, (code, OWNERS[entity], key['reference'])))
            query_id = package.fingerprint(scope)
            entities[entity] = query_id
            if query_id not in queries:
                # The finder delimiter grammar is not qualified for every legal
                # worksheet string. Never rewrite the value or broaden its query.
                finder_safe = all(re.fullmatch(r'[A-Za-z0-9_. -]+', v) for v in scope.values())
                queries[query_id] = {'scope': scope, 'path': RESOURCE,
                    'history_query': {'q': ';'.join(k+'='+literal(v) for k, v in scope.items()),
                                      'fields': PROJECTION, 'onlyData': 'true'},
                    'active_query': {'finder': 'SSRByOsOsrOwnerEntityObject;' +
                        ','.join(k+'='+v for k, v in scope.items()),
                        'fields': PROJECTION, 'onlyData': 'true'} if finder_safe else None}
            if queries[query_id]['active_query'] is None:
                unresolved.append({'row': number, 'entity': entity,
                                   'status': 'FINDER_LITERAL_GRAMMAR_UNQUALIFIED'})
        row_scopes.append({'row': number, 'entities': entities})
    return {'schema_version': 'ar-customer-api-snapshot-plan-v1',
            'candidate_sha256': hashlib.sha256(candidate).hexdigest(),
            'operation_intent': operation, 'environment_url': environment_url.rstrip('/'),
            'queries': queries, 'row_scopes': row_scopes, 'unresolved': unresolved,
            'execution_authorized': False, 'persisted_reconciliation_complete': False}


def scoped_pages(pages, scope):
    """Validate consecutive retained pages; preserve all rows and duplicates."""
    require = package.require
    require(isinstance(pages, list) and 0 < len(pages) <= 20, 'API_PAGES_REQUIRED')
    records, offset = [], 0
    for index, page in enumerate(pages):
        require(isinstance(page, dict) and isinstance(page.get('items'), list)
                and all(type(page.get(k)) is int for k in ('count', 'offset', 'limit'))
                and type(page.get('hasMore')) is bool, 'API_PAGE_SCHEMA')
        items = page['items']
        require(page['offset'] == offset and page['count'] == len(items)
                and page['limit'] > 0 and len(items) <= page['limit'], 'API_PAGE_SEQUENCE')
        require(index == len(pages)-1 or page['hasMore'], 'API_PAGES_AFTER_TERMINAL')
        require(not page['hasMore'] or bool(items), 'API_PAGINATION_NO_PROGRESS')
        for item in items:
            require(isinstance(item, dict) and FIELDS <= set(item), 'API_REFERENCE_FIELDS')
            require(all(item[k] == v for k, v in scope.items()), 'API_REFERENCE_SCOPE_MISMATCH')
            require(all(type(item[k]) is int and item[k] > 0 for k in
                        ('OwnerEntityId', 'SourceSystemReferenceId'))
                    and isinstance(item['Status'], str) and item['Status'].strip(),
                    'API_REFERENCE_VALUE_TYPE')
            bounds = []
            for field in ('StartDateActive', 'EndDateActive'):
                value = item[field]
                if field == 'EndDateActive' and value is None:
                    bounds.append(None)
                    continue
                require(isinstance(value, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', value),
                        'API_REFERENCE_DATE_FORMAT')
                try:
                    bounds.append(date.fromisoformat(value))
                except ValueError as exc:
                    raise package.InvalidInput('API_REFERENCE_DATE_FORMAT') from exc
            require(bounds[1] is None or bounds[1] >= bounds[0], 'API_REFERENCE_DATE_ORDER')
            records.append(item)
        offset += len(items)
    return records, not pages[-1]['hasMore']


def review(plan_document, observations):
    """Resolve API-visible owners without SQL IDs or fabricated expected values.

    The active and unfiltered reads are separate observations, not an atomic
    snapshot. Disagreement or duplicates stops resolution. A resolved owner is
    only a lookup result; hierarchy, values and effect checks remain separate.
    """
    require = package.require
    require(isinstance(plan_document, dict) and plan_document.get('schema_version') ==
            'ar-customer-api-snapshot-plan-v1', 'API_SNAPSHOT_PLAN_VERSION')
    require(isinstance(observations, dict) and set(observations) <= set(plan_document['queries']),
            'API_UNREQUESTED_OBSERVATION')
    findings, resolved = {}, {}
    for query_id, query in plan_document['queries'].items():
        observation = observations.get(query_id)
        status = 'READ_MISSING'
        history, active = [], []
        if observation is not None:
            require(isinstance(observation, dict) and set(observation) == {'history', 'active'},
                    'API_OBSERVATION_SCHEMA')
            history, history_complete = scoped_pages(observation['history'], query['scope'])
            if query['active_query'] is None or observation['active'] is None:
                status = 'ACTIVE_FINDER_UNAVAILABLE'
            else:
                active, active_complete = scoped_pages(observation['active'], query['scope'])
                status = ('INCOMPLETE_PAGINATION' if not history_complete or not active_complete else
                          'AMBIGUOUS_REFERENCE_HISTORY' if len(history) > 1 else
                          'AMBIGUOUS_ACTIVE_REFERENCE' if len(active) > 1 else
                          'NO_VISIBLE_REFERENCE_NOT_GLOBAL_ABSENCE' if not history and not active else
                          'REFERENCE_NOT_SERVER_ACTIVE' if len(history) == 1 and not active else
                          'READS_DISAGREE_OR_CHANGED' if len(history) != 1 or len(active) != 1 or
                              history[0] != active[0] else
                          'ACTIVE_FINDER_STATUS_MISMATCH' if active[0]['Status'] != 'A' else
                          'API_VISIBLE_OWNER_RESOLVED')
                if status == 'API_VISIBLE_OWNER_RESOLVED':
                    resolved[query_id] = str(active[0]['OwnerEntityId'])
        findings[query_id] = {'status': status, 'history_count': len(history),
                              'active_count': len(active)}
    row_results = [{'row': row['row'], 'owners': {entity: resolved[q]
                    for entity, q in row['entities'].items() if q in resolved}}
                   for row in plan_document['row_scopes']]
    return {'schema_version': 'ar-customer-api-snapshot-review-v1',
            'candidate_sha256': plan_document['candidate_sha256'],
            'environment_url': plan_document['environment_url'],
            'operation_intent': plan_document['operation_intent'],
            'plan_sha256': package.fingerprint(plan_document),
            'observations_sha256': package.fingerprint(observations),
            'findings': findings, 'rows': row_results,
            'all_reference_owners_resolved': not plan_document['unresolved'] and
                all(len(r['owners']) == 7 for r in row_results),
            'execution_authorized': False, 'persisted_reconciliation_complete': False,
            'profile_update_date_predicate_verified': False,
            'limitations': ['Visible absence is not global absence or permission to create.',
                'Independent reads are not a transactionally consistent snapshot.',
                'Resolved IDs require parent, number, value and before/after effect review.',
                'Central capture provenance is required; these pure helpers cannot authenticate supplied data.']}
