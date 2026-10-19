#!/usr/bin/env node
'use strict';

/**
 * Explore one Oracle Fusion VBCS Express Mode target without proposing code.
 * A later assessment consumes this report only after every required gate passes.
 */

const fs = require('node:fs');
const path = require('node:path');
const { fetchRuntimeEvidence } = require('./fetch_runtime_evidence');
const { fetchServiceEvidence } = require('./fetch_service_evidence');
const { buildFieldReport, validateFieldPath } = require('./extract_business_rule_contracts');
const { DEFAULT_PROPERTIES } = require('./fscr_rest_client');
const { safeJoin, sha256 } = require('./runtime_bundle');

class ExplorationError extends Error {
  constructor(code, message) {
    super(message);
    this.name = 'ExplorationError';
    this.code = code;
  }
}

function optionValue(argv, index, optionName) {
  const value = argv[index + 1];
  if (!value || value.startsWith('--')) {
    throw new ExplorationError('INVALID_ARGUMENT', `${optionName} requires a value.`);
  }
  return value;
}

function parseArgs(argv) {
  const options = {
    workspace: null,
    cacheRoot: null,
    repo: null,
    targetRoute: null,
    intent: null,
    fields: [],
    restService: null,
    restVersion: null,
    restResource: null,
    restFields: [],
    restChildren: [],
    propertiesPath: DEFAULT_PROPERTIES,
    tokenCache: null,
    cdnProxy: null,
    timeoutMs: 300000,
    json: false,
    help: false,
  };
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === '--workspace') {
      options.workspace = optionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--cache-root') {
      options.cacheRoot = optionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--repo') {
      options.repo = optionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--target-route') {
      options.targetRoute = optionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--intent') {
      options.intent = optionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--field') {
      options.fields.push(validateFieldPath(optionValue(argv, index, argument)));
      index += 1;
    } else if (argument === '--rest-service') {
      options.restService = optionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--rest-version') {
      options.restVersion = optionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--rest-resource') {
      options.restResource = optionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--rest-field') {
      options.restFields.push(optionValue(argv, index, argument));
      index += 1;
    } else if (argument === '--rest-child') {
      options.restChildren.push(optionValue(argv, index, argument));
      index += 1;
    } else if (argument === '--properties') {
      options.propertiesPath = optionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--token-cache') {
      options.tokenCache = optionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--cdn-proxy') {
      options.cdnProxy = optionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--timeout-ms') {
      options.timeoutMs = Number(optionValue(argv, index, argument));
      index += 1;
    } else if (argument === '--json') {
      options.json = true;
    } else if (argument === '--help' || argument === '-h') {
      options.help = true;
    } else {
      throw new ExplorationError('INVALID_ARGUMENT', `Unknown argument: ${argument}`);
    }
  }
  if (!options.help && (!options.workspace || !options.targetRoute || !options.intent)) {
    throw new ExplorationError(
      'INVALID_ARGUMENT',
      '--workspace, --target-route, and --intent are required.'
    );
  }
  const restParts = [options.restService, options.restVersion, options.restResource].filter(Boolean);
  if (!options.help && restParts.length > 0 && restParts.length !== 3) {
    throw new ExplorationError(
      'INVALID_ARGUMENT',
      '--rest-service, --rest-version, and --rest-resource must be supplied together.'
    );
  }
  options.fields = [...new Set(options.fields)].sort();
  options.restFields = [...new Set(options.restFields)].sort();
  options.restChildren = [...new Set(options.restChildren)].sort();
  return options;
}

function printHelp() {
  process.stdout.write([
    'Explore an Oracle Fusion VBCS Express Mode page before proposing a change',
    '',
    'Usage:',
    '  node scripts/investigate_express_evidence.js --workspace <project-artifact-root>',
    '    [--cache-root <shared-cache-directory>] --repo <extension-repository>',
    '    --target-route </fscmUI/redwood/application/flow/page> --intent <intent>',
    '    [--field <business-rules-path> ...]',
    '    [--rest-service <service> --rest-version <version> --rest-resource <resource>',
    '      --rest-field <attribute> ... --rest-child <child-path> ...]',
    '    [--token-cache <path>] [--cdn-proxy <auto|anonymous-http-proxy>] [--json]',
    '',
    'With one exact --field, the REST target is derived from deployed service metadata when unique.',
    'Explicit REST options remain available when deployed metadata is absent or ambiguous.',
    'Without --field, the command returns selection_required and a compact durable field index.',
    'Oracle CDN proxy discovery is automatic; --cdn-proxy remains an optional override.',
    'The cache defaults to project/.vblens-cache for a standard project artifact workspace.',
    '',
  ].join('\n'));
}

function inferProjectsRoot(workspace) {
  let current = path.resolve(workspace);
  while (path.dirname(current) !== current) {
    if (path.basename(current) === 'project') return current;
    current = path.dirname(current);
  }
  return null;
}

function resolveSharedCacheRoot(workspace, explicitCacheRoot = null) {
  // Standard project workspaces share one cache without scanning sibling projects.
  if (explicitCacheRoot) return path.resolve(explicitCacheRoot);
  const projectsRoot = inferProjectsRoot(workspace);
  return projectsRoot ? path.join(projectsRoot, '.vblens-cache') : null;
}

function readJson(filePath) {
  // Evidence files are inert JSON and must never be loaded as executable modules.
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function publishExplorationReport(workspace, result) {
  const root = path.resolve(workspace);
  const reportsDirectory = safeJoin(root, 'reports');
  fs.mkdirSync(reportsDirectory, { recursive: true, mode: 0o700 });
  const content = `${JSON.stringify(result, null, 2)}\n`;
  const reportPath = safeJoin(reportsDirectory, `exploration-${sha256(content)}.json`);
  if (!fs.existsSync(reportPath)) {
    // Content-addressed publication keeps each exploration immutable and auditable.
    fs.writeFileSync(reportPath, content, { mode: 0o600, flag: 'wx' });
  } else if (sha256(fs.readFileSync(reportPath)) !== sha256(content)) {
    throw new ExplorationError('EXPLORATION_REPORT_COLLISION', 'Exploration report hash collision.');
  }
  return reportPath;
}

function gate(status, evidence = [], reason = null) {
  return { status, evidence, reason };
}

function collectExtensionOverlays(repo) {
  if (!repo) return [];
  const root = path.resolve(repo);
  if (!fs.existsSync(root) || !fs.statSync(root).isDirectory()) return [];
  const overlays = [];
  const ignoredDirectories = new Set([
    '.git',
    '.idea',
    '.vscode',
    'build',
    'dist',
    'node_modules',
    'webApps',
  ]);
  const visit = (directory) => {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      // Generated output is not customer source and must not masquerade as an editable overlay.
      if (entry.isDirectory() && ignoredDirectories.has(entry.name)) continue;
      const absolute = path.join(directory, entry.name);
      if (entry.isDirectory()) visit(absolute);
      if (entry.isFile() && /(?:metadata-rules|layout|page-r|page)-x\.json$/.test(entry.name)) {
        overlays.push(path.relative(root, absolute).split(path.sep).join('/'));
      }
    }
  };
  visit(root);
  return overlays.sort();
}

function compactField(field) {
  const declarations = field?.businessRules?.combinedDeclarations || {};
  const evidence = [];
  const seenEvidence = new Set();
  const addEvidence = (item) => {
    if (!item?.moduleId) return;
    const compact = {
      moduleId: item.moduleId,
      ...(item.sha256 ? { sha256: item.sha256 } : {}),
      ...(item.pointer ? { pointer: item.pointer } : {}),
      ...(item.definitionModuleId ? { definitionModuleId: item.definitionModuleId } : {}),
    };
    const key = JSON.stringify(compact);
    if (!seenEvidence.has(key)) {
      seenEvidence.add(key);
      evidence.push(compact);
    }
  };
  for (const item of field?.evidence || []) {
    if (item.pointer || item.definitionModuleId) addEvidence(item);
  }
  for (const contract of field?.valueContracts || []) addEvidence(contract);
  return {
    path: field.path,
    labels: field.labels || [],
    types: field.types || [],
    valueContracts: field.valueContracts || [],
    owningObject: field.owningObject || null,
    businessRules: {
      fieldOverrideDeclaredIn: declarations.fieldOverrideDeclaredIn || [],
      declaredOverrideOperations: declarations.declaredOverrideOperations || [],
      listedAsSimpleConditionIn: declarations.listedAsSimpleConditionIn || [],
      listedChildSimpleConditionPaths: declarations.listedChildSimpleConditionPaths || [],
      ruleOverlayOccurrences: declarations.ruleOverlayOccurrences || [],
      accessorCallSiteCount: field?.businessRules?.accessorCallSites?.length || 0,
    },
    evidence,
    restSchema: field.restSchema || [],
  };
}

function compactFields(fields) {
  return (fields || []).map(compactField);
}

function readVerifiedEvidenceJson(item) {
  if (!item?.path || !item.sha256) return null;
  const content = fs.readFileSync(item.path);
  if (sha256(content) !== item.sha256) {
    throw new ExplorationError(
      'EVIDENCE_HASH_MISMATCH',
      `Cached evidence hash does not match ${item.moduleId || '<unknown module>'}.`
    );
  }
  try {
    return JSON.parse(content.toString('utf8'));
  } catch (error) {
    throw new ExplorationError(
      'INVALID_SERVICE_CATALOG',
      `Cached service catalog is invalid JSON: ${error.message}`
    );
  }
}

function serviceTargetFromCatalog(serviceId, catalog, moduleId) {
  const separator = String(serviceId || '').indexOf(':');
  if (separator <= 0) return [];
  const extension = serviceId.slice(0, separator);
  const catalogService = serviceId.slice(separator + 1);
  const definition = catalog?.services?.[catalogService];
  if (!definition) return [];
  const serverUrls = (definition.servers || []).map((server) => server?.url).filter(Boolean);
  const resources = Object.values(definition.paths || {}).flatMap((operation) => (
    Object.values(operation || {}).map((method) => method?.['x-vb']?.queryParameters?.resources)
  )).filter((resource) => typeof resource === 'string' && resource.trim());
  const targets = [];
  for (const serverUrl of serverUrls) {
    const match = String(serverUrl).match(
      /^vb-catalog:\/\/backends\/(?:[^/:]+:)?([A-Za-z][A-Za-z0-9]*Rest)\/([^/:]+)(?::|\/|$)/
    );
    if (!match) continue;
    for (const resource of resources) {
      targets.push({
        extension,
        catalogService,
        service: match[1],
        version: match[2],
        resource: resource.trim(),
        moduleId,
      });
    }
  }
  return targets;
}

function resolveRestTarget(runtimeManifest, fields) {
  if (!fields?.length) {
    return { status: 'not_requested', target: null, candidates: [], reason: null };
  }
  const owners = new Set(fields.map((field) => field.split('.')[0]).filter(Boolean));
  const serviceIds = new Set((runtimeManifest?.nodes || [])
    .filter((node) => {
      if (node.type !== 'dynamic-layout' || !node.serviceId) return false;
      const layoutOwner = String(node.layoutRoot || '').split('/').at(-1);
      return owners.has(layoutOwner);
    })
    .map((node) => node.serviceId));
  const candidates = [];
  for (const serviceId of serviceIds) {
    const extension = String(serviceId).split(':')[0];
    const catalogs = (runtimeManifest.evidence || []).filter((item) => (
      item.role === 'service-metadata'
      && String(item.moduleId || '').startsWith(`text!vx/${extension}/services/`)
    ));
    for (const item of catalogs) {
      candidates.push(...serviceTargetFromCatalog(
        serviceId,
        readVerifiedEvidenceJson(item),
        item.moduleId
      ));
    }
  }
  const unique = [...new Map(candidates.map((candidate) => [
    `${candidate.service}/${candidate.version}/${candidate.resource}`,
    candidate,
  ])).values()];
  if (unique.length !== 1) {
    return {
      status: 'unresolved',
      target: null,
      candidates: unique,
      reason: unique.length === 0
        ? 'No REST describe target could be derived from the selected field owner and deployed service catalog.'
        : 'Multiple REST describe targets match the selected field owner.',
    };
  }
  return {
    status: 'resolved',
    target: {
      service: unique[0].service,
      version: unique[0].version,
      resource: unique[0].resource,
      fields: [...new Set(fields.map((field) => field.split('.').at(-1)))].sort(),
      children: [],
    },
    candidates: unique,
    reason: null,
  };
}

function findAttribute(schema, attributeName) {
  const matches = [];
  const visit = (node, location) => {
    for (const attribute of node?.attributes || []) {
      if (String(attribute.name).toLowerCase() === attributeName.toLowerCase()) {
        matches.push({ location, ...attribute });
      }
    }
    for (const child of node?.children || []) visit(child, child.path || child.name || location);
  };
  visit(schema, 'root');
  return matches;
}

function fieldHasBusinessRuleEvidence(field) {
  const declarations = field?.businessRules?.combinedDeclarations;
  return Boolean(
    field
    && (
      // Business Rules declarations prove field exposure; REST remains the separate type gate.
      declarations?.fieldOverrideDeclaredIn?.length
      || declarations?.listedAsSimpleConditionIn?.length
      || declarations?.ruleOverlayOccurrences?.length
      || field.businessRules.accessorCallSites?.length
    )
  );
}

function restTargetHasRuntimeBinding(runtimeManifest, restResource) {
  if (!restResource) return false;
  const expected = String(restResource).toLowerCase();
  const nodes = runtimeManifest?.nodes || [];
  const evidence = runtimeManifest?.evidence || [];
  return nodes.some((node) => String(node.serviceId || '').toLowerCase().includes(expected))
    || evidence.some((item) => (
      item.role === 'service-metadata'
      && String(item.moduleId || '').toLowerCase().includes(expected)
    ));
}

function percentageScaleEvidence(fields) {
  return fields.flatMap((field) => (field.valueContracts || []).filter((contract) => (
    contract.percentScale !== null
    || contract.scaleFactor !== null
    || /percent/i.test(String(contract.format || ''))
  )).map((contract) => ({ field: field.path, ...contract })));
}

function exploredSurface(runtimeManifest) {
  const nodes = runtimeManifest?.nodes || [];
  const evidence = runtimeManifest?.evidence || [];
  const selectNodes = (type, keys) => nodes.filter((node) => node.type === type).map((node) => (
    Object.fromEntries(keys.filter((key) => node[key] !== undefined).map((key) => [key, node[key]]))
  ));
  const selectEvidence = (role) => evidence
    .filter((item) => item.role === role)
    .map((item) => ({ moduleId: item.moduleId, sha256: item.sha256 }));
  return {
    // Keep raw source identities separate so later assessment can trace every claim.
    counts: {
      nodes: nodes.length,
      edges: runtimeManifest?.edges?.length || 0,
      unresolved: runtimeManifest?.unresolved?.length || 0,
    },
    pageSources: selectEvidence('page-source'),
    fragmentSources: selectEvidence('fragment-source'),
    dynamicComponents: selectNodes('dynamic-component', [
      'id', 'tag', 'consumerKind', 'metadataName', 'layout', 'literalLayouts',
    ]),
    dynamicLayouts: selectNodes('dynamic-layout', [
      'id', 'extension', 'layoutRoot', 'selectedLayout', 'serviceId',
    ]),
    namedLayouts: selectNodes('named-layout', ['id', 'layoutRoot', 'name', 'type']),
    ruleSetRules: selectNodes('rule-set-rule', ['id', 'layoutRoot', 'ruleId', 'status']),
    serviceBindings: selectNodes('dynamic-layout', [
      'layoutRoot', 'selectedLayout', 'serviceId',
    ])
      .filter((node) => node.serviceId)
      .map((node) => ({
        layoutRoot: node.layoutRoot,
        selectedLayout: node.selectedLayout,
        serviceId: node.serviceId,
      })),
    serviceMetadata: selectEvidence('service-metadata'),
    businessRuleSources: selectEvidence('business-and-validation-rules'),
    dataDescriptions: selectEvidence('data-description'),
    advancedExpressions: selectEvidence('advanced-expression'),
    pagePropertyRules: selectEvidence('page-property-rules'),
    unresolved: runtimeManifest?.unresolved || [],
  };
}

function selectedBusinessRuleEvidence(fields) {
  const references = [];
  const seen = new Set();
  const add = (item) => {
    if (!item?.moduleId) return;
    const key = `${item.moduleId}:${item.sha256 || ''}`;
    if (seen.has(key)) return;
    seen.add(key);
    references.push({
      moduleId: item.moduleId,
      ...(item.sha256 ? { sha256: item.sha256 } : {}),
    });
  };
  for (const field of fields || []) {
    const selectedModules = new Set([
      ...(field.businessRules?.combinedDeclarations?.fieldOverrideDeclaredIn || []),
      ...(field.businessRules?.combinedDeclarations?.listedAsSimpleConditionIn || []),
      ...(field.businessRules?.combinedDeclarations?.ruleOverlayOccurrences || [])
        .map((occurrence) => occurrence.moduleId),
    ]);
    for (const declaration of field.businessRules?.declarations || []) {
      if (selectedModules.has(declaration.moduleId)) add(declaration);
    }
    for (const item of field.evidence || []) {
      if (item.pointer || item.definitionModuleId) add(item);
    }
  }
  return references;
}

function evaluateReadiness(runtimeManifest, fieldReport, serviceResult, options = {}) {
  const evidence = runtimeManifest?.evidence || [];
  const nodes = runtimeManifest?.nodes || [];
  const edges = runtimeManifest?.edges || [];
  const forms = nodes.filter((node) => (
    node.type === 'dynamic-component'
    && (node.consumerKind === 'dynamic-form' || String(node.tag).toLowerCase() === 'oj-dyn-form')
  ));
  const boundForms = forms.filter((form) => edges.some((edge) => (
    edge.from === form.id
    && /uses-(?:dynamic|metadata-descriptor|inherited-metadata)-layout/.test(edge.type)
  )));
  const pageEvidence = evidence.filter((item) => item.role === 'page-source');
  const ruleEvidence = evidence.filter((item) => item.role === 'business-and-validation-rules');
  const descriptionEvidence = evidence.filter((item) => item.role === 'data-description');
  const fields = fieldReport?.fields || [];
  const unresolvedFields = fields.filter((field) => !fieldHasBusinessRuleEvidence(field));
  const fieldOwners = new Set(fields.map((field) => field.owningObject).filter(Boolean));
  const targetBoundForms = boundForms.filter((form) => edges.some((edge) => {
    if (
      edge.from !== form.id
      || !/uses-(?:dynamic|metadata-descriptor|inherited-metadata)-layout/.test(edge.type)
    ) {
      return false;
    }
    const layout = nodes.find((node) => node.id === edge.to && node.type === 'dynamic-layout');
    const layoutOwner = String(layout?.layoutRoot || '').split('/').at(-1);
    return fieldOwners.size === 0 || [...fieldOwners].some((owner) => (
      owner === layoutOwner || String(layout?.selectedLayout || '').startsWith(`${owner}_`)
    ));
  }));

  const requestedRestFields = options.restFields?.length
    ? options.restFields
    : fields.map((field) => field.path.split('.').at(-1));
  const restMatches = serviceResult
    ? requestedRestFields.flatMap((field) => findAttribute(serviceResult.schema, field))
    : [];
  const missingRestFields = serviceResult
    ? requestedRestFields.filter((field) => findAttribute(serviceResult.schema, field).length === 0)
    : requestedRestFields;
  const restTargetBound = restTargetHasRuntimeBinding(runtimeManifest, options.restResource);
  const requiresPercentageScale = /percentage|salary-increase-cap/i.test(String(options.intent || ''));
  const scaleEvidence = percentageScaleEvidence(fields);
  const targetClosureProven = Boolean(
    runtimeManifest?.environment
    && pageEvidence.length > 0
    && targetBoundForms.length > 0
    && ruleEvidence.length > 0
    && descriptionEvidence.length > 0
    && unresolvedFields.length === 0
  );

  const gates = {
    page: pageEvidence.length > 0
      ? gate('passed', pageEvidence.map((item) => ({ moduleId: item.moduleId, sha256: item.sha256 })))
      : gate('missing', [], 'Exact deployed page source was not found.'),
    dynamicForm: targetBoundForms.length > 0
      ? gate('passed', targetBoundForms.map((form) => ({
        id: form.id,
        tag: form.tag,
        metadataName: form.metadataName,
      })))
      : gate('missing', forms, 'No Dynamic Form was proven to bind the selected dynamic layout.'),
    businessRules: ruleEvidence.length > 0 && descriptionEvidence.length > 0 && unresolvedFields.length === 0
      ? gate('passed', selectedBusinessRuleEvidence(fields))
      : gate('missing', unresolvedFields.map((field) => ({ field: field.path })),
        'Business Rules, data description, or exact field-operation evidence is incomplete.'),
    restSchema: serviceResult && restTargetBound && missingRestFields.length === 0
      ? gate('passed', restMatches)
      : gate(serviceResult ? 'failed' : 'not_run', missingRestFields.map((field) => ({ field })),
        serviceResult
          ? 'The REST target is not bound by page evidence or does not contain every requested field.'
          : 'REST target evidence was not supplied, so REST describe was not called.'),
    valueContract: !requiresPercentageScale || scaleEvidence.length > 0
      ? gate('passed', scaleEvidence, requiresPercentageScale ? null : 'No percentage scale is required.')
      : gate('missing', [], 'The stored and displayed percentage scale is unresolved.'),
    provenance: targetClosureProven
      ? gate('passed', [{
        environment: runtimeManifest.environment,
        bundles: runtimeManifest.bundles,
        // Unresolved optional branches remain visible without invalidating the proven field path.
        unresolvedOutsideProvenClosure: (runtimeManifest.unresolved || []).length,
      }])
      : gate('failed', runtimeManifest?.unresolved || [], 'The target field path is partial or unbound.'),
  };
  const missingEvidence = Object.entries(gates)
    .filter(([, value]) => value.status !== 'passed')
    .map(([name, value]) => ({ gate: name, status: value.status, reason: value.reason }));
  return {
    gates,
    fields,
    missingEvidence,
    surface: exploredSurface(runtimeManifest),
    ready: missingEvidence.length === 0,
  };
}

function loginRequiredResult(options) {
  // A login gate returns no field or implementation advice.
  return {
    schemaVersion: 1,
    status: 'login_required',
    target: { route: options.targetRoute, intent: options.intent },
    gates: {
      page: gate('not_run'),
      dynamicForm: gate('not_run'),
      businessRules: gate('not_run'),
      restSchema: gate('not_run'),
      valueContract: gate('not_run'),
      provenance: gate('not_run'),
    },
    fieldCandidates: [],
    existingExtensionOverlays: collectExtensionOverlays(options.repo),
    missingEvidence: [{ gate: 'authentication', status: 'missing', reason: 'Fusion login is required.' }],
    proposalAllowed: false,
    implementationSuggestion: null,
    nextAction: 'Run core.auth.fusion-oauth-authentication, then repeat this exploration.',
  };
}

async function investigateExpressEvidence(options, dependencies = {}) {
  const runtimeFetcher = dependencies.fetchRuntimeEvidence || fetchRuntimeEvidence;
  const cacheRoot = resolveSharedCacheRoot(options.workspace, options.cacheRoot);
  let runtime;
  try {
    runtime = await runtimeFetcher({
      workspace: options.workspace,
      // Runtime and REST evidence share the same environment-versioned cache.
      cacheRoot,
      targetRoute: options.targetRoute,
      propertiesPath: options.propertiesPath,
      tokenCache: options.tokenCache,
      // The runtime fetcher validates and limits this proxy to approved Oracle CDN traffic.
      cdnProxy: options.cdnProxy,
      timeoutMs: options.timeoutMs,
    });
  } catch (error) {
    if (error.code === 'AUTH_REQUIRED') return loginRequiredResult(options);
    throw error;
  }

  if (!runtime.evidenceGraph?.manifestPath) {
    const empty = evaluateReadiness(null, null, null, options);
    return {
      schemaVersion: 1,
      status: 'blocked',
      target: runtime.target,
      gates: empty.gates,
      fieldCandidates: options.fields.map((field) => ({ path: field, status: 'unverified' })),
      exploredSurface: empty.surface,
      existingExtensionOverlays: collectExtensionOverlays(options.repo),
      missingEvidence: [
        ...empty.missingEvidence,
        ...(runtime.evidenceGraph?.unresolved || []),
      ],
      proposalAllowed: false,
      implementationSuggestion: null,
      nextAction: 'Resolve the runtime evidence failure and repeat exploration.',
    };
  }

  const manifest = readJson(runtime.evidenceGraph.manifestPath);
  const fieldBuilder = dependencies.buildFieldReport || buildFieldReport;
  if (options.fields.length === 0) {
    const inventory = fieldBuilder({
      evidenceManifest: runtime.evidenceGraph.manifestPath,
      serviceManifests: [],
      fields: [],
      inventory: true,
      all: false,
    });
    const preliminary = evaluateReadiness(manifest, { fields: [] }, null, {
      ...options,
      intent: '',
      restFields: [],
    });
    return {
      schemaVersion: 1,
      status: 'selection_required',
      target: runtime.target,
      environment: runtime.environment,
      deployedBundles: runtime.bundles,
      gates: {
        ...preliminary.gates,
        businessRules: gate(
          'selection_required',
          [],
          'Select the exact Business Rules field from the compact inventory, then repeat exploration.'
        ),
        restSchema: gate('not_run', [], 'REST describe runs after an exact field is selected.'),
        valueContract: gate('not_run', [], 'Value-contract verification runs after field selection.'),
        provenance: gate('pending', [{
          unresolvedOutsideSelectedClosure: manifest.unresolved?.length || 0,
        }], 'Target-field closure is evaluated after field selection.'),
      },
      fieldCandidates: compactFields(inventory.fields),
      exploredSurface: exploredSurface(manifest),
      existingExtensionOverlays: collectExtensionOverlays(options.repo),
      missingEvidence: [],
      selectionRequired: {
        candidateCount: inventory.fields.length,
        reason: 'Business intent requires semantic field selection; deterministic inventory does not guess.',
      },
      evidenceManifests: {
        runtime: runtime.evidenceGraph.manifestPath,
        rest: null,
      },
      proposalAllowed: false,
      implementationSuggestion: null,
      nextAction: 'Select one exact field from this report, then repeat exploration with --field.',
    };
  }

  const suppliedRestTarget = options.restService && options.restVersion && options.restResource
    ? {
      status: 'supplied',
      target: {
        service: options.restService,
        version: options.restVersion,
        resource: options.restResource,
        fields: options.restFields.length > 0
          ? options.restFields
          : options.fields.map((field) => field.split('.').at(-1)),
        children: options.restChildren,
      },
      candidates: [],
      reason: null,
    }
    : resolveRestTarget(manifest, options.fields);
  const restTarget = suppliedRestTarget.target;
  let serviceResult = null;
  if (restTarget) {
    const serviceFetcher = dependencies.fetchServiceEvidence || fetchServiceEvidence;
    try {
      serviceResult = await serviceFetcher({
        workspace: options.workspace,
        cacheRoot,
        service: restTarget.service,
        version: restTarget.version,
        resource: restTarget.resource,
        fields: restTarget.fields,
        children: restTarget.children,
        propertiesPath: options.propertiesPath,
        tokenCache: options.tokenCache,
        timeoutMs: options.timeoutMs,
      });
    } catch (error) {
      if (error.code === 'AUTH_REQUIRED') return loginRequiredResult(options);
      throw error;
    }
  }

  const fieldReport = fieldBuilder({
    evidenceManifest: runtime.evidenceGraph.manifestPath,
    serviceManifests: serviceResult ? [serviceResult.evidence.manifestPath] : [],
    fields: options.fields,
    inventory: false,
    all: false,
  });
  const effectiveOptions = {
    ...options,
    restService: restTarget?.service || null,
    restVersion: restTarget?.version || null,
    restResource: restTarget?.resource || null,
    restFields: restTarget?.fields || options.restFields,
    restChildren: restTarget?.children || options.restChildren,
  };
  const readiness = evaluateReadiness(manifest, fieldReport, serviceResult, effectiveOptions);
  return {
    schemaVersion: 1,
    status: readiness.ready ? 'explored' : 'blocked',
    target: runtime.target,
    environment: runtime.environment,
    deployedBundles: runtime.bundles,
    gates: readiness.gates,
    fieldCandidates: compactFields(readiness.fields),
    exploredSurface: readiness.surface,
    existingExtensionOverlays: collectExtensionOverlays(options.repo),
    missingEvidence: readiness.missingEvidence,
    evidenceManifests: {
      runtime: runtime.evidenceGraph.manifestPath,
      rest: serviceResult?.evidence?.manifestPath || null,
    },
    restResolution: suppliedRestTarget,
    proposalAllowed: false,
    implementationSuggestion: null,
    nextAction: readiness.ready
      ? 'Review the exploration report, then run a separate feasibility assessment.'
      : 'Collect the missing evidence and repeat exploration; do not propose implementation.',
  };
}

function cliResult(result, reportPath) {
  const gates = Object.fromEntries(Object.entries(result.gates || {}).map(([name, value]) => [
    name,
    {
      status: value.status,
      reason: value.reason,
      evidenceCount: value.evidence?.length || 0,
    },
  ]));
  const candidateCount = result.fieldCandidates?.length || 0;
  return {
    schemaVersion: result.schemaVersion,
    status: result.status,
    target: result.target,
    environment: result.environment,
    gates,
    fieldCandidateCount: candidateCount,
    // Keep exact-field results inline; large inventories remain queryable in the durable report.
    fieldCandidates: candidateCount <= 20 ? result.fieldCandidates : [],
    candidateIndex: candidateCount > 20 ? reportPath : null,
    existingExtensionOverlays: result.existingExtensionOverlays,
    missingEvidence: result.missingEvidence,
    selectionRequired: result.selectionRequired || null,
    evidenceManifests: result.evidenceManifests,
    restResolution: result.restResolution || null,
    proposalAllowed: result.proposalAllowed,
    implementationSuggestion: result.implementationSuggestion,
    nextAction: result.nextAction,
    reportPath,
  };
}

async function main() {
  try {
    const options = parseArgs(process.argv.slice(2));
    if (options.help) return printHelp();
    const result = await investigateExpressEvidence(options);
    const reportPath = publishExplorationReport(options.workspace, result);
    process.stdout.write(`${JSON.stringify(cliResult(result, reportPath), null, 2)}\n`);
    if (result.status === 'login_required') process.exitCode = 2;
    if (result.status === 'blocked') process.exitCode = 3;
  } catch (error) {
    process.stderr.write(`${JSON.stringify({
      error: { code: error.code || 'EXPLORATION_FAILED', message: error.message },
    }, null, 2)}\n`);
    process.exitCode = 1;
  }
}

if (require.main === module) main();

module.exports = {
  ExplorationError,
  cliResult,
  compactField,
  compactFields,
  collectExtensionOverlays,
  evaluateReadiness,
  findAttribute,
  exploredSurface,
  investigateExpressEvidence,
  inferProjectsRoot,
  loginRequiredResult,
  parseArgs,
  publishExplorationReport,
  resolveRestTarget,
  resolveSharedCacheRoot,
  restTargetHasRuntimeBinding,
  serviceTargetFromCatalog,
};
