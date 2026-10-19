#!/usr/bin/env python3
"""Offline Trees payload planning, normalized validation and reconciliation. No I/O to Fusion."""
import argparse
import copy
import hashlib
import json
import re
import sys
import unicodedata
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

BASE = '/fscmRestApi/resources/11.13.18.05/'
HCM_BASE = '/hcmRestApi/resources/11.13.18.05/'
HCM_NODE_READBACK_COLLECTIONS = {
    'PER_POS_TREE_STRUCTURE': HCM_BASE + 'positionTreeNodesLOV',
    'PER_DEPT_TREE_STRUCTURE': HCM_BASE + 'departmentTreeNodesLOV',
    'PER_ORG_TREE_STRUCTURE': HCM_BASE + 'organizationTreeNodesLOV',
}
RESOURCES = {'tree': 'fndTrees', 'version': 'fndTreeVersions',
             'label': 'fndLabels', 'association': 'fndTreeLabels',
             'parameter': 'fndTreeDataSourceParams', 'node': 'fndTreeNodes'}
FIELDS = {
    'tree': {'TreeStructureCode', 'TreeCode', 'TreeName', 'Description', 'SetId'},
    'version': {'TreeStructureCode', 'TreeCode', 'TreeVersionName', 'Description',
                'EffectiveStartDate', 'EffectiveEndDate', 'Status',
                'ChangedSinceValidation', 'LevelCount', 'NodeCount'},
    'label': {'TreeStructureCode', 'DataSourceId', 'LabelName', 'LabelShortName',
              'Description', 'EffectiveStartDate', 'EffectiveEndDate', 'SetId'},
    'association': {'TreeStructureCode', 'TreeCode', 'DataSourceId', 'TreeLabelId'},
    'parameter': {'TreeStructureCode', 'TreeCode', 'DataSourceId', 'ParameterId', 'ParameterValue'},
    'node': {'DataSourceId', 'Pk1StartValue', 'Pk2StartValue', 'ParentTreeNodeId'},
}
REQUIRED = {
    'tree': ['TreeStructureCode', 'TreeCode', 'TreeName'],
    'version': ['TreeStructureCode', 'TreeCode', 'TreeVersionName'],
    'label': ['TreeStructureCode', 'DataSourceId', 'LabelName', 'LabelShortName'],
    'association': ['TreeStructureCode', 'TreeCode', 'DataSourceId', 'TreeLabelId'],
    'parameter': ['TreeStructureCode', 'TreeCode', 'DataSourceId', 'ParameterId', 'ParameterValue'],
    'node': ['DataSourceId', 'Pk1StartValue'],
}

class Gap(ValueError):
    pass


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key: ' + key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(Path(path).read_text(), object_pairs_hook=unique_pairs)


def empty(value):
    return value is None or isinstance(value, str) and not value.strip()


def iso(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        raise ValueError('Expected YYYY-MM-DD date')
    return date.fromisoformat(value)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


PARAMETER_KEYS = ('DataSourceId', 'ParameterId', 'ParameterValue')


def normalize_parameter_tuple(value):
    """Return a comparable parameter tuple; reject incomplete caller values."""
    if not isinstance(value, dict):
        raise ValueError('Data Source Parameter must be an object')
    result = []
    for key in PARAMETER_KEYS:
        if key not in value or empty(value[key]):
            raise ValueError('Data Source Parameter.' + key + ' is required')
        result.append(unicodedata.normalize('NFC', str(value[key]).strip()))
    return tuple(result)


def assess_parameter_validation(supplied, existing_trees, tree_structure_code=None):
    """Assess read-back results before a tree POST; never infer a match."""
    if not supplied:
        raise ValueError('At least one Data Source Parameter is required')
    wanted = tuple(sorted(normalize_parameter_tuple(item) for item in supplied))
    structure_code = tree_structure_code or supplied[0].get('TreeStructureCode')
    if empty(structure_code):
        raise ValueError('Data Source Parameter.TreeStructureCode is required')
    relevant = [tree for tree in existing_trees
                if tree.get('TreeStructureCode') == structure_code]
    if not relevant:
        return {'status': 'assumed_correct', 'method': 'no_same_structure_tree',
                'supplied_tuples': wanted, 'matched_tree': None, 'exception': None}
    for tree in relevant:
        actual = tuple(sorted(normalize_parameter_tuple(item)
                              for item in tree.get('FndTreeDataSourceParamsVO', [])))
        if actual == wanted:
            return {'status': 'matched', 'method': 'child_collection_tuple_comparison',
                    'supplied_tuples': wanted, 'matched_tree': tree.get('TreeCode'),
                    'exception': None}
    return {'status': 'exception', 'method': 'child_collection_tuple_comparison',
            'supplied_tuples': wanted, 'matched_tree': None,
            'exception': {'failure_class': 'catalog_or_metadata_mismatch',
                          'message': 'Existing same-structure trees have no matching Data Source Parameters',
                          'recommended_action': 'Correct parameter tuples or retain the diagnostic; do not create'}}


def clean(kind, source, today, notices, create=True):
    if not isinstance(source, dict):
        raise ValueError(kind + ' must be an object')
    obj = copy.deepcopy(source)
    if kind == 'version' and create and 'TreeVersionId' in obj:
        obj.pop('TreeVersionId')
        notices.append('Omitted system-generated TreeVersionId from create')
    unknown = set(obj) - FIELDS[kind]
    if unknown:
        raise Gap('Unestablished ' + kind + ' fields: ' + ', '.join(sorted(unknown)))
    if create:
        for key in REQUIRED[kind]:
            if empty(obj.get(key)):
                raise ValueError(kind + '.' + key + ' is required')
    if kind in {'version', 'label'}:
        for key, default in [('EffectiveStartDate', today), ('EffectiveEndDate', '4712-12-31')]:
            if create and empty(obj.get(key)):
                obj[key] = default
                notices.append(kind + '.' + key + ' defaulted to ' + default)
            if key in obj:
                iso(obj[key])
        if all(k in obj for k in ['EffectiveStartDate', 'EffectiveEndDate']):
            if iso(obj['EffectiveStartDate']) >= iso(obj['EffectiveEndDate']):
                raise ValueError('EffectiveStartDate must precede EffectiveEndDate')
    if kind == 'version':
        if create:
            obj.setdefault('Status', 'DRAFT')
            if empty(obj.get('ChangedSinceValidation')):
                obj['ChangedSinceValidation'] = 'Y'
                notices.append('version.ChangedSinceValidation defaulted to Y')
            for key in ['LevelCount', 'NodeCount']:
                if key not in obj or obj[key] is None:
                    obj[key] = 0
                    notices.append('version.' + key + ' defaulted to 0')
        if 'ChangedSinceValidation' in obj:
            value = obj['ChangedSinceValidation']
            if not isinstance(value, str) or len(value) != 1:
                raise ValueError('ChangedSinceValidation must be a one-character string')
        for key in ['LevelCount', 'NodeCount']:
            if key in obj and (type(obj[key]) is not int or obj[key] < 0):
                raise ValueError(key + ' must be a non-negative integer')
        if 'Status' in obj and obj['Status'] != 'DRAFT':
            raise Gap('Non-DRAFT status requires a separately established audited transition')
    return obj


def item_path(href, environment, resource):
    env, parsed = urlsplit(environment), urlsplit(href)
    if env.scheme != 'https' or not env.netloc or env.username or env.password:
        raise ValueError('environment must be an HTTPS origin')
    if env.path not in ('', '/') or env.query or env.fragment:
        raise ValueError('environment must contain only origin')
    if (parsed.scheme, parsed.netloc) != (env.scheme, env.netloc):
        raise ValueError('Canonical item link must match environment origin')
    prefix = BASE + resource + '/'
    if not parsed.path.startswith(prefix) or not parsed.path[len(prefix):] or parsed.query or parsed.fragment:
        raise ValueError('Unexpected canonical item link')
    if '/' in parsed.path[len(prefix):] or '%' in parsed.path[len(prefix):] or '..' in parsed.path:
        raise ValueError('Unsafe item identifier')
    return parsed.path


def scope_child(obj, parent):
    obj = copy.deepcopy(obj)
    for key in ['TreeStructureCode', 'TreeCode']:
        if key in obj and obj[key] != parent[key]:
            raise ValueError('Nested identity mismatch: ' + key)
        obj[key] = parent[key]
    return obj


def node_reference(node, index):
    """Return a planner-only node reference; never send it to Fusion."""
    ref = node.get('node_ref')
    if empty(ref):
        ref = 'node-%d' % index
    if not isinstance(ref, str) or empty(ref):
        raise ValueError('node_ref must be a nonempty string when supplied')
    return ref


def sequential_node_step(tree, version, node, ref, parent_ref=None):
    """Build a deferred action whose generated IDs are resolved at runtime."""
    body = {
        'treeStructureCode': tree['TreeStructureCode'],
        'treeCode': tree['TreeCode'],
        'treeVersionId': {'resolve': 'version_id', 'tree_version_name': version['TreeVersionName']},
        'dataSourceId': node['DataSourceId'],
        'parentTreeNodeId': '' if parent_ref is None else {'resolve': 'node_id', 'node_ref': parent_ref},
        'pk1Value': node['Pk1StartValue'],
    }
    for index in range(2, 6):
        body['pk%dValue' % index] = node.get('Pk%dStartValue' % index, '')
    return {
        'tree_version_name': version['TreeVersionName'],
        'node_ref': ref,
        'depends_on_node_ref': parent_ref,
        'method': 'POST',
        'path': BASE + 'fndTreeNodeOperations/action/addValueTreeNode',
        'headers': {
            'Content-Type': 'application/vnd.oracle.adf.action+json',
            'Accept': 'application/vnd.oracle.adf.actionresult+json',
        },
        'body_template': body,
    }


def source_member_validation_check(tree_structure_code, data_source_id, member_values, ref):
    """Require domain-resolver evidence for proposed source values, not tree nodes."""
    return {
        'node_ref': ref,
        'tree_structure_code': tree_structure_code,
        'data_source_id': data_source_id,
        'member_values': member_values,
        'resolver_selection': 'existing domain resolver selected from TreeStructureCode and DataSourceId evidence',
        'prohibited_resolver': 'fndTreeNodes is post-create verification only',
        'required_outcome': 'validated',
        'failure_artifact': 'project/{project_id}/artifacts/core/trees/{run_id}/source-member-validation.json',
        'on_unvalidated': 'record failure artifact and stop before all external mutations',
    }


def node_readback_request(tree_structure_code):
    """Select generated-node read-back without treating HCM TreeNodeId as an item key."""
    collection = HCM_NODE_READBACK_COLLECTIONS.get(tree_structure_code)
    if collection:
        return {
            'path': collection,
            'query': {'q': 'TreeNodeId={generated_tree_node_id}'},
            'response_shape': 'collection',
        }
    return {
        'path': BASE + 'fndTreeNodes/{TreeNodeId}',
        'query': None,
        'response_shape': 'item',
    }


def node_readback_check_for(body, node_ref):
    """Verify a generated TreeNodeId only after its action has succeeded."""
    request = node_readback_request(body['treeStructureCode'])
    return {
        'node_ref': node_ref,
        'when': 'after_successful_addValueTreeNode_action',
        'method': 'GET',
        'endpoint': request['path'],
        'query': request['query'],
        'response_shape': request['response_shape'],
        'tree_node_id': {'resolve': 'action_result', 'node_ref': node_ref},
        'required_match': {'returned_count': 1, 'tree_node_id': '{generated_tree_node_id}'},
        'expected': {
            'tree_structure_code': body['treeStructureCode'],
            'tree_code': body['treeCode'],
            'tree_version_id': body['treeVersionId'],
            'parent_tree_node_id': body['parentTreeNodeId'],
            'data_source_id': body['dataSourceId'],
            'pk_values': {'pk%dValue' % i: body['pk%dValue' % i] for i in range(1, 6)},
        },
        'runtime_record': ['selected_endpoint', 'query_string', 'generated_tree_node_id',
                           'returned_count', 'http_result',
                           'returned_identity', 'verification_outcome'],
        'on_verification_failure': 'record verification diagnostic; do not retry node action; continue actions whose create outcome is known',
        'on_create_failure_or_uncertain': 'stop dependent actions',
    }


def node_readback_check(step):
    return node_readback_check_for(step['body_template'], step['node_ref'])


def ordered_steps(steps):
    """Order roots first and children only after their parent node ID exists."""
    pending, resolved, ordered = list(steps), set(), []
    while pending:
        ready = [step for step in pending
                 if step['depends_on_node_ref'] is None or step['depends_on_node_ref'] in resolved]
        if not ready:
            raise ValueError('Sequenced nodes contain a cycle or unresolved parent_ref')
        for step in ready:
            pending.remove(step)
            ordered.append(step)
            resolved.add(step['node_ref'])
    return ordered


def plan(request, timezone, as_of=None):
    now = datetime.now(ZoneInfo(timezone))
    today = as_of or now.date().isoformat()
    iso(today)
    allowed = {'operation', 'object', 'versions', 'associations', 'parameters',
               'label_definitions', 'item_href', 'environment', 'describe'}
    if set(request) - allowed:
        raise ValueError('Unknown intake keys: ' + ', '.join(sorted(set(request) - allowed)))
    op = request['operation']
    for key in ['versions', 'associations', 'parameters', 'label_definitions']:
        if key in request and not isinstance(request[key], list):
            raise ValueError(key + ' must be an array')
    notices, blockers, sequential_steps, data_source_checks = [], [], [], []
    source_member_validation_checks, node_readback_checks = [], []
    all_node_refs = set()
    method, headers = 'POST', {'Content-Type': 'application/json', 'Accept': 'application/json'}
    compound_keys = ['versions', 'associations', 'parameters', 'label_definitions']
    if op != 'create_tree' and any(request.get(k) for k in compound_keys):
        raise Gap('Multiple mutations require an established compound contract; no decomposition')
    if op == 'create_tree':
        obj = clean('tree', request['object'], today, notices)
        path = BASE + 'fndTrees'
        if not request.get('parameters'):
            raise ValueError('Tree creation requires explicit Data Source Parameters')
        if request.get('label_definitions'):
            raise Gap('Nested FndTreeLabelVO creates associations, not label definitions')
        if request.get('associations'):
            raise Gap('fndTrees create payload is limited to the tree, Draft versions, and explicitly valid parameters; create tree-label associations separately')
        versions = []
        for raw in request.get('versions', []):
            raw = copy.deepcopy(raw)
            nodes = raw.pop('nodes', [])
            if not isinstance(nodes, list):
                raise ValueError('nodes must be an array')
            version = clean('version', scope_child(raw, obj), today, notices)
            if any(v['TreeVersionName'] == version['TreeVersionName'] for v in versions):
                raise ValueError('Duplicate requested TreeVersionName')
            node_refs, version_steps = set(), []
            for index, raw_node in enumerate(nodes, start=1):
                node = copy.deepcopy(raw_node)
                ref = node_reference(node, index)
                if ref in all_node_refs:
                    raise ValueError('Duplicate node_ref: ' + ref)
                all_node_refs.add(ref)
                node_refs.add(ref)
                parent_ref = node.pop('parent_ref', None)
                node.pop('node_ref', None)
                if 'TreeNodeId' in node:
                    raise Gap('TreeNodeId is generated after node creation and is not a proposed source-member identifier')
                explicit_parent = node.pop('ParentTreeNodeId', None)
                if not empty(explicit_parent):
                    raise Gap('New nodes must use planner-only parent_ref, not a supplied ParentTreeNodeId')
                node = clean('node', node, today, notices)
                if not empty(parent_ref) and (not isinstance(parent_ref, str) or empty(parent_ref)):
                    raise ValueError('parent_ref must be a nonempty node_ref')
                step = sequential_node_step(obj, version, node, ref, None if empty(parent_ref) else parent_ref)
                version_steps.append(step)
                source_member_validation_checks.append(source_member_validation_check(
                    obj['TreeStructureCode'],
                    node['DataSourceId'],
                    [{'field': 'Pk%dStartValue' % i, 'value': node.get('Pk%dStartValue' % i, '')}
                     for i in range(1, 6) if not empty(node.get('Pk%dStartValue' % i, ''))], ref))
                node_readback_checks.append(node_readback_check(step))
                if node['DataSourceId'] not in data_source_checks:
                    data_source_checks.append(node['DataSourceId'])
            for step in version_steps:
                if (step['depends_on_node_ref'] is not None
                        and step['depends_on_node_ref'] not in node_refs):
                    raise ValueError('parent_ref does not match a node_ref: ' + step['depends_on_node_ref'])
            sequential_steps.extend(version_steps)
            versions.append(version)
        if versions:
            obj['FndTreeVersionVO'] = versions
        if request.get('parameters'):
            # ParameterId and ParameterValue must both be explicitly present; clean enforces this.
            parameters = []
            for raw_parameter in request['parameters']:
                parameter = clean('parameter', scope_child(raw_parameter, obj), today, notices)
                parameter.pop('TreeStructureCode', None)
                parameter.pop('TreeCode', None)
                parameters.append(parameter)
            obj['FndTreeDataSourceParamsVO'] = parameters
        parameter_tuples = [normalize_parameter_tuple(item) for item in obj['FndTreeDataSourceParamsVO']]
    elif op.startswith('create_') and op[7:] in {'version', 'label', 'association', 'parameter'}:
        kind = op[7:]
        obj = clean(kind, request['object'], today, notices)
        path = BASE + RESOURCES[kind]
        if kind == 'label':
            blockers.append('Confirm target fndLabels contract: source base-path disagreement remains')
    elif op == 'add_node':
        obj = copy.deepcopy(request['object'])
        required = ['treeStructureCode', 'treeCode', 'treeVersionId', 'dataSourceId', 'pk1Value']
        allowed = set(required + ['parentTreeNodeId'] + ['pk%dValue' % i for i in range(2, 6)])
        if set(obj) - allowed:
            raise Gap('Unsupported addValueTreeNode fields')
        for key in required:
            if empty(obj.get(key)):
                raise ValueError(key + ' is required')
        obj.setdefault('parentTreeNodeId', '')
        for i in range(2, 6):
            obj.setdefault('pk%dValue' % i, '')
        path = BASE + 'fndTreeNodeOperations/action/addValueTreeNode'
        headers = {'Content-Type': 'application/vnd.oracle.adf.action+json',
                   'Accept': 'application/vnd.oracle.adf.actionresult+json'}
        source_member_validation_checks.append(source_member_validation_check(
            obj['treeStructureCode'],
            obj['dataSourceId'],
            [{'field': 'pk%dValue' % i, 'value': obj.get('pk%dValue' % i, '')}
             for i in range(1, 6) if not empty(obj.get('pk%dValue' % i, ''))], 'new-node'))
        node_readback_checks.append(node_readback_check_for(obj, 'new-node'))
    elif op.startswith('update_') and op[7:] in {'tree', 'version', 'label', 'parameter'}:
        kind = op[7:]
        obj = clean(kind, request['object'], today, notices, create=False)
        if not obj:
            raise ValueError('Empty PATCH')
        if set(obj) & {'TreeStructureCode', 'TreeCode', 'DataSourceId', 'ParameterId'}:
            raise Gap('Identity changes are not supported')
        path = item_path(request['item_href'], request['environment'], RESOURCES[kind])
        method = 'PATCH'
        blockers.append('Verify writable fields and merged existing-state validation before PATCH')
        if kind in {'parameter', 'label'}:
            blockers.append('Incomplete or inconsistent update contract requires target evidence')
    else:
        raise Gap('Unsupported operation; no alternate mutations generated')
    mutation = {'method': method, 'path': path, 'headers': headers, 'body': obj}
    if sequential_steps:
        sequential_steps = ordered_steps(sequential_steps)
        notices.append('fndTrees creates only the tree and Draft version; every node, including each root, runs through addValueTreeNode in dependency order')
        data_source_checks = [{
            'when': 'after_fndTrees_create_and_version_identity_resolution',
            'data_source_id': source_id,
            'read': 'resolved tree child/FndTreeDataSourceParamsVO',
            'on_match': 'continue',
            'on_missing_or_unreadable': 'assume_correct_and_continue; record validation outcome',
        } for source_id in data_source_checks]
    parameter_validation = []
    if op == 'create_tree':
        parameter_validation = [{
            'stage': 'before_any_external_mutation',
            'tree_structure_code': obj['TreeStructureCode'],
            'supplied_tuples': parameter_tuples,
            'tree_lookup': {'method': 'GET', 'path': BASE + 'fndTrees',
                            'filter': 'returned TreeStructureCode equals requested value; paginate fully'},
            'per_tree_read': 'resolved fndTrees item child/FndTreeDataSourceParamsVO',
            'comparison': 'normalized exact collection of DataSourceId, ParameterId, ParameterValue tuples',
            'artifact': 'project/{project_id}/artifacts/core/trees/{run_id}/parameter-validation.json',
            'exception_artifact': 'project/{project_id}/artifacts/core/trees/{run_id}/parameter-validation-exception.json',
            'on_match': 'proceed',
            'on_no_same_structure_tree': 'record assumed_correct and proceed',
            'on_existing_tree_without_match': 'persist exception diagnostic and stop before create/version/node mutation',
        }]
    plan_identity = {'mutations': [mutation], 'sequential_node_steps': sequential_steps,
                     'data_source_checks': data_source_checks,
                     'parameter_validation': parameter_validation,
                     'source_member_validation_checks': source_member_validation_checks,
                     'node_readback_checks': node_readback_checks}
    return {'status': 'preview', 'prepared_at': now.isoformat(), 'timezone': timezone,
            'effective_plan_date': today, 'fixture_date_override': as_of is not None,
            'environment': request.get('environment'), 'mutations': [mutation],
            'sequential_node_steps': sequential_steps, 'data_source_checks': data_source_checks,
            'parameter_validation': parameter_validation,
            'source_member_validation_checks': source_member_validation_checks,
            'node_readback_checks': node_readback_checks,
            'payload_sha256': digest(plan_identity), 'notices': notices, 'contract_blockers': blockers,
            'execution_gates': ['parameter tuple validation', 'source-member validation',
                                'authoritative prerequisites', 'target contract',
                                'final-state validation', 'durable plan', 'immediate explicit approval'],
            'live_executed': False}


def exact_one(items, identity):
    matches = [x for x in items if all(x.get(k) == v for k, v in identity.items())]
    if len(matches) != 1:
        raise ValueError('Exact identity must match one object; matched %d' % len(matches))
    return matches[0]


def validate(model):
    """Normalized final graph; absent source/structure evidence yields unknown."""
    results = []
    def check(name, passed, detail='', applicable=True):
        results.append({'check': name, 'status': 'not_applicable' if not applicable else
                        'unknown' if passed is None else 'pass' if passed else 'fail', 'detail': detail})
    def conditional(name, flag, test, detail=''):
        check(name, None if flag is None else test, detail, applicable=flag is not False)
    flags = model.get('structure', {})
    sources = model.get('sources', {})
    nodes = model.get('nodes', [])
    version = model.get('version', {})
    def booleans(obj, fields):
        for key in fields:
            if key in obj and obj[key] is not None and type(obj[key]) is not bool:
                raise ValueError(key + ' must be a JSON boolean or null (unknown)')
    booleans(flags, ['multiple_roots', 'multiple_active', 'restrict_set', 'restrict_date'])
    booleans(model, ['structure_audited', 'parameters_complete', 'source_keys_resolved', 'ragged_skip_valid'])
    if flags.get('labeling') not in {None, 'None', 'Level', 'Group', 'Depth'}:
        raise ValueError('Unknown labeling scheme')
    if version.get('status') not in {'DRAFT', 'ACTIVE', 'INACTIVE'}:
        raise ValueError('Normalized version status required')
    for ds in sources.values():
        booleans(ds, ['duplicates', 'leaves', 'ranges', 'use_all'])
        limit = ds.get('max_depth')
        if limit is not None and (type(limit) is not int or limit < -1):
            raise ValueError('max_depth must be -1 or a nonnegative integer')
    for node in nodes:
        for key in ['id', 'source']:
            if not isinstance(node.get(key), str) or empty(node[key]):
                raise ValueError('Every node requires ' + key)
        if not isinstance(node.get('keys'), list) or not node['keys']:
            raise ValueError('Every node requires an ordered source keys array')
        if any(isinstance(k, (dict, list)) or empty(k) for k in node['keys']):
            raise ValueError('Source keys must be nonempty scalar values')
        if node.get('type', 'single') not in {'single', 'range', 'reference'}:
            raise ValueError('Unknown node type')
        booleans(node, ['exists', 'label_compatible', 'reference_exists'])
    ids = [n['id'] for n in nodes]
    check('Local unique node identifiers', len(ids) == len(set(ids)))
    by_id = {n['id']: n for n in nodes}
    interval = None
    if version.get('start') and version.get('end'):
        interval = (iso(version['start']), iso(version['end']))
    check('Effective Date', interval[0] < interval[1] if interval else None)
    roots = sum(not n.get('parent') for n in nodes)
    conditional('Root Node', None if 'multiple_roots' not in flags else not flags['multiple_roots'],
                roots == 1 if nodes else True)
    for node in nodes:
        nid, parent = node['id'], node.get('parent')
        ds = sources.get(node['source'], {})
        check('Available Node', node.get('exists'), nid)
        check('Local version membership', node.get('version') == version.get('id')
              if node.get('version') is not None and version.get('id') is not None else None, nid)
        check('Local parent existence', parent in by_id if parent else True, nid)
        seen, cursor, depth, cycle = set(), nid, 0, False
        while cursor in by_id:
            if cursor in seen:
                cycle = True
                break
            seen.add(cursor)
            cursor = by_id[cursor].get('parent')
            if cursor:
                depth += 1
        check('Local acyclic graph', not cycle, nid)
        limit = ds.get('max_depth')
        check('Maximum Depth', None if limit is None else not cycle and (limit == -1 or depth <= limit), nid)
        same = sum(n['source'] == node['source'] and n.get('keys') == node.get('keys') for n in nodes)
        conditional('Duplicate Node', None if 'duplicates' not in ds else not ds['duplicates'], same == 1, nid)
        if parent in by_id:
            permitted = ds.get('parent_sources')
            check('Node Relationship', by_id[parent]['source'] in permitted if permitted is not None else None, nid)
        else:
            check('Node Relationship', True, nid, applicable=bool(parent))
        conditional('SetID Restricted Node', flags.get('restrict_set'),
                    node.get('set_id') == model.get('set_id') if 'set_id' in node and 'set_id' in model else None, nid)
        scheme = flags.get('labeling')
        check('Label Enabled Node', bool(node.get('label')) if scheme is not None else None,
              nid, applicable=scheme != 'None')
        check('Local label compatibility', node.get('label_compatible'), nid, applicable=bool(node.get('label')))
        covered = None
        if interval and node.get('start') and node.get('end'):
            covered = iso(node['start']) <= interval[0] and iso(node['end']) >= interval[1]
        conditional('Date Restricted Node', flags.get('restrict_date'), covered, nid)
        check('Range Based Node', ds.get('ranges'), nid, applicable=node.get('type', 'single') == 'range')
        check('Available referenced version', node.get('reference_exists'), nid,
              applicable=node.get('type') == 'reference')
        leaf = not any(n.get('parent') == nid for n in nodes)
        check('Terminal Node', ds.get('leaves'), nid, applicable=leaf)
    for source, ds in sources.items():
        values = ds.get('all_keys')
        present = {tuple(n.get('keys', [])) for n in nodes if n['source'] == source}
        conditional('Usage Limit', ds.get('use_all'),
                    set(map(tuple, values)) <= present if values is not None else None, source)
    overlaps = None
    if interval and 'other_active_versions' in model:
        overlaps = any(interval[0] <= iso(v['end']) and iso(v['start']) <= interval[1]
                       for v in model['other_active_versions'])
    if version.get('status') == 'ACTIVE':
        conditional('Multiple Active Version', None if 'multiple_active' not in flags else not flags['multiple_active'],
                    not overlaps if overlaps is not None else None)
    else:
        check('Multiple Active Version', True, applicable=False)
    for name in ['structure_audited', 'parameters_complete', 'source_keys_resolved', 'ragged_skip_valid']:
        check('Prerequisite ' + name, model.get(name))
    failures = [r for r in results if r['status'] in {'fail', 'unknown'}]
    return {'status': 'blocked' if failures else 'pass', 'checks': results,
            'errors': failures, 'oracle_audit_performed': False}


def reconcile(plan_doc, response):
    """Conservatively match creations, never claim success from HTTP alone."""
    body = plan_doc['mutations'][0]['body']
    path = plan_doc['mutations'][0]['path']
    ids, errors = [], []
    def record(kind, expected, actual, keys, id_key=None):
        try:
            item = exact_one(actual, {k: expected[k] for k in keys})
            if id_key and empty(item.get(id_key)):
                raise ValueError('Missing generated ' + id_key)
            ids.append({'kind': kind, 'identity': {k: item[k] for k in keys},
                        'id': item.get(id_key) if id_key else None})
            return item
        except (ValueError, KeyError) as exc:
            errors.append({'kind': kind, 'failure_class': 'fusion_api_error',
                           'message': str(exc), 'recommended_action': 'Scoped read-back; do not retry create'})
            return {}
    if not isinstance(response, dict):
        raise ValueError('Response must be an object')
    errors.extend(response.get('errors', []))
    if path.endswith('/fndTrees'):
        record('tree', body, [response], ['TreeStructureCode', 'TreeCode'])
        for version in body.get('FndTreeVersionVO', []):
            record('version', version, response.get('FndTreeVersionVO', []),
                   ['TreeStructureCode', 'TreeCode', 'TreeVersionName'], 'TreeVersionId')
        for child, kind, keys in [('FndTreeLabelVO', 'association', ['DataSourceId', 'TreeLabelId']),
                                  ('FndTreeDataSourceParamsVO', 'parameter', ['DataSourceId', 'ParameterId'])]:
            for item in body.get(child, []):
                record(kind, item, response.get(child, []), keys)
    elif path.endswith('/fndTreeVersions'):
        record('version', body, [response], ['TreeStructureCode', 'TreeCode', 'TreeVersionName'], 'TreeVersionId')
    elif path.endswith('/action/addValueTreeNode'):
        if empty(response.get('result')):
            errors.append({'message': 'Missing generated node result; read back before retry'})
        else:
            ids.append({'kind': 'node', 'id': response['result']})
    elif path.endswith('/fndLabels'):
        record('label', body, [response], ['TreeStructureCode', 'DataSourceId', 'LabelName'], 'LabelId')
    else:
        errors.append({'message': 'Use explicit identity and field read-back for this operation'})
    return {'status': 'partial_or_unverified' if errors else 'identities_reconciled',
            'generated_ids': ids, 'errors': errors, 'verification': 'field read-back still required',
            'audit': 'not_performed', 'activation': 'not_verified', 'flattening': 'not_verified'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('plan', help='Offline only; print one mutation preview')
    p.add_argument('--input', required=True)
    p.add_argument('--timezone', required=True)
    p.add_argument('--as-of', help='Fixture date override; not for live plans')
    p.add_argument('--dry-run', action='store_true', help='Explicit offline intent; all modes are offline')
    p = sub.add_parser('validate', help='Validate a normalized final graph')
    p.add_argument('--input', required=True)
    p = sub.add_parser('reconcile', help='Capture response IDs and partial results')
    p.add_argument('--input', required=True, help='Saved plan JSON')
    p.add_argument('--response', required=True)
    args = parser.parse_args()
    try:
        obj = read_json(args.input)
        if args.command == 'plan':
            result = plan(obj, args.timezone, args.as_of)
        elif args.command == 'validate':
            result = validate(obj)
        else:
            result = reconcile(obj, read_json(args.response))
        print(json.dumps(result, indent=2))
        return 2 if result.get('errors') or result.get('contract_blockers') else 0
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(json.dumps({'status': 'blocked', 'failure_class': 'catalog_or_metadata_mismatch' if isinstance(exc, Gap)
                          else 'input_validation', 'message': str(exc), 'live_executed': False}))
        return 2 if isinstance(exc, Gap) else 1


if __name__ == '__main__':
    sys.exit(main())
