#!/usr/bin/env node
'use strict';

/**
 * Fetch the exact App UI versions deployed in one Fusion environment, cache
 * their bundles, and publish a static evidence graph for one runtime target.
 */

const crypto = require('node:crypto');
const fs = require('node:fs');
const https = require('node:https');
const path = require('node:path');
const {
  RuntimeEvidenceError,
  acquireCacheLock,
  assertNoSymlinkBetween,
  buildBundleUrl,
  ensureCacheRoot,
  loadBundleCache,
  parseRedwoodRouteUrl,
  publishBundleCache,
  requireApplication,
  resolveApplicationFromRoute,
  resolveApplicationIndex,
  resolveCdnOrigin,
  resolveCachePaths,
  safeJoin,
  sha256,
  validateIdentifier,
} = require('./runtime_bundle');
const { resolveEvidenceGraph } = require('./runtime_graph');
const {
  DEFAULT_PROPERTIES,
  callFusionRest,
  parseSafeEnvironment,
} = require('./fscr_rest_client');
const {
  createCdnProxyAgent,
  resolveAutomaticCdnProxy,
  resolveCdnTransport,
} = require('./cdn_proxy_transport');

const DEFAULT_TIMEOUT_MS = 300000;
const MAX_MANIFEST_BYTES = 10 * 1024 * 1024;
const MAX_BUNDLE_BYTES = 128 * 1024 * 1024;

function sanitizeTransportError(error) {
  // Keep CDN diagnostics useful without returning proxy, credential, or URL details.
  return error && error.code ? String(error.code) : 'HTTPS_REQUEST_FAILED';
}

function readOptionValue(argv, index, optionName) {
  const value = argv[index + 1];
  if (!value || value.startsWith('--')) {
    throw new RuntimeEvidenceError('INVALID_ARGUMENT', `${optionName} requires a value.`);
  }
  return value;
}

function parseArgs(argv) {
  const options = {
    workspace: process.cwd(),
    cacheRoot: null,
    targetUrl: null,
    targetRoute: null,
    targetKind: null,
    extension: null,
    application: null,
    flow: null,
    page: null,
    owner: null,
    layout: null,
    fallbackOwner: null,
    fallbackLayout: null,
    propertiesPath: DEFAULT_PROPERTIES,
    tokenCache: null,
    cdnProxy: null,
    timeoutMs: DEFAULT_TIMEOUT_MS,
    json: false,
    help: false,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === '--workspace') {
      options.workspace = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--cache-root') {
      options.cacheRoot = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--target-url') {
      options.targetUrl = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--target-route') {
      options.targetRoute = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--target-kind') {
      options.targetKind = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--extension') {
      options.extension = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--application') {
      options.application = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--flow') {
      options.flow = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--page') {
      options.page = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--owner') {
      options.owner = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--layout') {
      options.layout = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--fallback-owner') {
      options.fallbackOwner = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--fallback-layout') {
      options.fallbackLayout = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--properties') {
      options.propertiesPath = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--token-cache') {
      options.tokenCache = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--cdn-proxy') {
      options.cdnProxy = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--timeout-ms') {
      options.timeoutMs = Number(readOptionValue(argv, index, argument));
      index += 1;
    } else if (argument === '--json') {
      options.json = true;
    } else if (argument === '--help' || argument === '-h') {
      options.help = true;
    } else {
      throw new RuntimeEvidenceError('INVALID_ARGUMENT', `Unknown argument: ${argument}`);
    }
  }
  return options;
}

function printHelp() {
  process.stdout.write([
    'Resolve deployed Oracle Express Mode runtime evidence',
    '',
    'Usage:',
    '  node scripts/fetch_runtime_evidence.js --workspace <path>',
    '    --target-url <redwood-page-url> [--cdn-proxy <auto|http-proxy-url>] [--json]',
    '    [--cache-root <shared-cache-directory>]',
    '',
    '  node scripts/fetch_runtime_evidence.js --workspace <path>',
    '    --target-route </fscmUI/redwood/application/flow/page> [--cdn-proxy <auto|http-proxy-url>] [--json]',
    '    The Fusion host is resolved exclusively from fusionEnv.properties.',
    '',
    '  node scripts/fetch_runtime_evidence.js --workspace <path>',
    '    --target-kind ui-page --extension <extension-id>',
    '    [--application <application-id>] --flow <flow-path> --page <page-id> [--json]',
    '',
    '  node scripts/fetch_runtime_evidence.js --workspace <path>',
    '    --target-kind dynamic-layout --extension <extension-id>',
    '    --owner <owner-id> --layout <layout-id> [--json]',
    '',
    'The command uses core/auth/fusionEnv.properties and the shared Fusion REST client.',
    'Oracle CDN transport automatically honors HTTPS_PROXY/ALL_PROXY, NO_PROXY, and macOS PAC settings.',
    '--cdn-proxy is an optional anonymous HTTP proxy override; auto is the default behavior.',
    'Cached deployed bundles use the supplied shared cache root when present.',
    '',
  ].join('\n'));
}

function normalizeTarget(options) {
  if (options.targetUrl && options.targetRoute) {
    throw new RuntimeEvidenceError(
      'INVALID_TARGET',
      '--target-url and --target-route cannot be supplied together.'
    );
  }
  if (options.targetUrl) {
    if (
      options.targetKind || options.extension || options.application || options.flow
      || options.page || options.owner || options.layout
    ) {
      throw new RuntimeEvidenceError(
        'INVALID_TARGET',
        '--target-url cannot be combined with explicit target or route options.'
      );
    }
    if (Boolean(options.fallbackOwner) !== Boolean(options.fallbackLayout)) {
      throw new RuntimeEvidenceError(
        'INVALID_TARGET',
        '--fallback-owner and --fallback-layout must be supplied together.'
      );
    }
    if (!Number.isSafeInteger(options.timeoutMs) || options.timeoutMs <= 0) {
      throw new RuntimeEvidenceError('INVALID_ARGUMENT', '--timeout-ms must be a positive integer.');
    }
    return {
      kind: 'redwood-url',
      route: parseRedwoodRouteUrl(options.targetUrl),
      fallbackDynamicLayout: options.fallbackOwner ? {
        owner: validateIdentifier(options.fallbackOwner, 'Fallback dynamic-layout owner'),
        layout: validateIdentifier(options.fallbackLayout, 'Fallback dynamic-layout ID'),
      } : null,
    };
  }
  if (options.targetRoute) {
    if (
      options.targetKind || options.extension || options.application || options.flow
      || options.page || options.owner || options.layout
    ) {
      throw new RuntimeEvidenceError(
        'INVALID_TARGET',
        '--target-route cannot be combined with explicit target or route options.'
      );
    }
    if (Boolean(options.fallbackOwner) !== Boolean(options.fallbackLayout)) {
      throw new RuntimeEvidenceError(
        'INVALID_TARGET',
        '--fallback-owner and --fallback-layout must be supplied together.'
      );
    }
    if (!Number.isSafeInteger(options.timeoutMs) || options.timeoutMs <= 0) {
      throw new RuntimeEvidenceError('INVALID_ARGUMENT', '--timeout-ms must be a positive integer.');
    }
    return {
      kind: 'redwood-route',
      routePath: String(options.targetRoute).trim(),
      fallbackDynamicLayout: options.fallbackOwner ? {
        owner: validateIdentifier(options.fallbackOwner, 'Fallback dynamic-layout owner'),
        layout: validateIdentifier(options.fallbackLayout, 'Fallback dynamic-layout ID'),
      } : null,
    };
  }
  if (options.targetKind !== 'ui-page' && options.targetKind !== 'dynamic-layout') {
    throw new RuntimeEvidenceError(
      'INVALID_TARGET',
      '--target-kind must be ui-page or dynamic-layout.'
    );
  }
  const extension = validateIdentifier(options.extension, 'Extension ID');
  if (!Number.isSafeInteger(options.timeoutMs) || options.timeoutMs <= 0) {
    throw new RuntimeEvidenceError('INVALID_ARGUMENT', '--timeout-ms must be a positive integer.');
  }

  if (options.targetKind === 'ui-page') {
    if (options.owner || options.layout) {
      throw new RuntimeEvidenceError(
        'INVALID_TARGET',
        '--owner and --layout apply only to dynamic-layout targets.'
      );
    }
    if (Boolean(options.fallbackOwner) !== Boolean(options.fallbackLayout)) {
      throw new RuntimeEvidenceError(
        'INVALID_TARGET',
        '--fallback-owner and --fallback-layout must be supplied together.'
      );
    }
    return {
      kind: 'ui-page',
      extension,
      application: options.application
        ? validateIdentifier(options.application, 'Application ID')
        : null,
      flow: validateIdentifier(options.flow, 'Flow path', { allowPath: true }),
      page: validateIdentifier(options.page, 'Page ID'),
      fallbackDynamicLayout: options.fallbackOwner ? {
        owner: validateIdentifier(options.fallbackOwner, 'Fallback dynamic-layout owner'),
        layout: validateIdentifier(options.fallbackLayout, 'Fallback dynamic-layout ID'),
      } : null,
    };
  }

  if (options.application || options.flow || options.page || options.fallbackOwner || options.fallbackLayout) {
    throw new RuntimeEvidenceError(
      'INVALID_TARGET',
      '--application, --flow, --page, and fallback layout options apply only to ui-page targets.'
    );
  }
  return {
    kind: 'dynamic-layout',
    extension,
    owner: validateIdentifier(options.owner, 'Dynamic-layout owner'),
    layout: validateIdentifier(options.layout, 'Dynamic-layout ID'),
  };
}

function resolvePropertyBackedRoute(routePath, environment) {
  const normalized = String(routePath || '').trim();
  if (!normalized.startsWith('/fscmUI/redwood/') || normalized.startsWith('//')) {
    throw new RuntimeEvidenceError(
      'INVALID_TARGET_ROUTE',
      '--target-route must be a relative /fscmUI/redwood/<application>/<flow>/<page> path.'
    );
  }
  let environmentUrl;
  try {
    environmentUrl = new URL(environment);
  } catch (error) {
    throw new RuntimeEvidenceError('INVALID_ENVIRONMENT', 'Fusion environment URL is invalid.');
  }
  if (environmentUrl.protocol !== 'https:') {
    throw new RuntimeEvidenceError('INVALID_ENVIRONMENT', 'Fusion environment URL must use HTTPS.');
  }
  return parseRedwoodRouteUrl(new URL(normalized, environmentUrl).toString());
}

function requestText(url, options = {}) {
  const requestFactory = options.requestFactory || https.request;
  const timeoutMs = options.timeoutMs || DEFAULT_TIMEOUT_MS;
  const maxBytes = options.maxBytes;
  const expectedOrigin = options.expectedOrigin;
  if (!Number.isSafeInteger(maxBytes) || maxBytes <= 0) {
    throw new RuntimeEvidenceError(
      'INVALID_REQUEST_LIMIT',
      'HTTPS response size limit must be a positive integer.'
    );
  }
  if (!Number.isSafeInteger(timeoutMs) || timeoutMs <= 0) {
    throw new RuntimeEvidenceError(
      'INVALID_REQUEST_TIMEOUT',
      'HTTPS request timeout must be a positive integer.'
    );
  }
  if (!(url instanceof URL) || url.protocol !== 'https:' || url.origin !== expectedOrigin) {
    throw new RuntimeEvidenceError(
      'UNSAFE_REQUEST_URL',
      `Refusing request to unexpected origin ${url instanceof URL ? url.origin : '<invalid>'}.`
    );
  }
  const headers = {
    ...(options.headers || {}),
    Accept: options.accept || '*/*',
  };
  // CDN evidence requests are intentionally anonymous; reject credential forwarding.
  if (options.authorization || headers.Authorization || headers.authorization) {
    throw new RuntimeEvidenceError('CREDENTIAL_FORWARDING_REJECTED', 'CDN requests must not include authorization.');
  }

  return new Promise((resolve, reject) => {
    const request = requestFactory(
      url,
      {
        // Override an unsafe inherited Node default for every runtime-evidence request.
        rejectUnauthorized: true,
        agent: options.agent,
        method: 'GET',
        headers,
      },
      (response) => {
        const status = response.statusCode || 0;
        if (status >= 300 && status < 400) {
          response.resume();
          reject(new RuntimeEvidenceError(
            'REDIRECT_REJECTED',
            `HTTP redirect from ${url.origin} was rejected.`
          ));
          return;
        }
        const chunks = [];
        let receivedBytes = 0;
        const contentLength = Number(response.headers['content-length']);
        if (Number.isFinite(contentLength) && contentLength > maxBytes) {
          response.resume();
          reject(new RuntimeEvidenceError(
            'RESPONSE_TOO_LARGE',
            `Response from ${url.origin} declared more than ${maxBytes} bytes.`
          ));
          return;
        }
        response.on('aborted', () => {
          reject(new RuntimeEvidenceError(
            'HTTP_RESPONSE_ABORTED',
            `GET ${url.pathname} ended before the complete response was received.`
          ));
        });
        response.on('error', reject);
        response.on('data', (chunk) => {
          const buffer = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
          receivedBytes += buffer.length;
          if (receivedBytes > maxBytes) {
            request.destroy(new RuntimeEvidenceError(
              'RESPONSE_TOO_LARGE',
              `Response from ${url.origin} exceeded ${maxBytes} bytes.`
            ));
            return;
          }
          chunks.push(buffer);
        });
        response.on('end', () => {
          if (status < 200 || status >= 300) {
            reject(new RuntimeEvidenceError(
              'HTTP_REQUEST_FAILED',
              `GET ${url.pathname} failed with HTTP ${status}.`
            ));
            return;
          }
          resolve({
            text: Buffer.concat(chunks).toString('utf8'),
            status,
            headers: {
              etag: typeof response.headers.etag === 'string' ? response.headers.etag : null,
              lastModified: typeof response.headers['last-modified'] === 'string'
                ? response.headers['last-modified']
                : null,
              contentType: typeof response.headers['content-type'] === 'string'
                ? response.headers['content-type']
                : null,
            },
          });
        });
      }
    );
    request.setTimeout(timeoutMs, () => {
      request.destroy(new RuntimeEvidenceError(
        'REQUEST_TIMEOUT',
        `GET ${url.pathname} timed out after ${timeoutMs} ms.`
      ));
    });
    request.on('error', reject);
    // This resolver performs exactly one attempt for every authorized GET.
    request.end();
  });
}

function parseManifestResponse(responseText) {
  try {
    return resolveApplicationIndex(JSON.parse(responseText));
  } catch (error) {
    if (error instanceof RuntimeEvidenceError) throw error;
    throw new RuntimeEvidenceError(
      'MANIFEST_INVALID',
      `App-info response was not valid JSON: ${error.message}`
    );
  }
}

async function loadOrFetchBundle(context, extensionId) {
  const application = requireApplication(context.applicationIndex, extensionId);
  const paths = resolveCachePaths(
    context.workspace,
    context.environment,
    application.id,
    application.version,
    context.cacheRoot
  );
  let corrupt = false;
  try {
    const cache = loadBundleCache(paths, {
      extensionId: application.id,
      version: application.version,
    });
    if (cache) return { ...cache, cacheStatus: 'hit' };
  } catch (error) {
    if (!(error instanceof RuntimeEvidenceError) || error.code !== 'CACHE_CORRUPT') throw error;
    corrupt = true;
  }

  const lock = await acquireCacheLock(paths, { timeoutMs: context.timeoutMs });
  try {
    // Another caller can publish the immutable version while this caller waits.
    try {
      const cache = loadBundleCache(paths, {
        extensionId: application.id,
        version: application.version,
      });
      if (cache) return { ...cache, cacheStatus: 'hit' };
    } catch (error) {
      if (!(error instanceof RuntimeEvidenceError) || error.code !== 'CACHE_CORRUPT') throw error;
      corrupt = true;
    }

    const bundleUrl = buildBundleUrl(application.id, application.version, context.cdnOrigin);
    let fetched;
    let requestStarted = false;
    try {
      const transportResolver = context.resolveCdnTransport || resolveCdnTransport;
      const cdnTransport = transportResolver(bundleUrl, {
        enableProxy: context.enableProxy,
        explicitProxy: context.cdnProxy,
        environment: context.proxyEnvironment,
        platform: context.proxyPlatform,
        spawnSync: context.proxySpawnSync,
        resolveSystemProxy: context.resolveSystemProxy,
      });
      context.cdnProxyModes.add(cdnTransport.mode);
      requestStarted = true;
      fetched = await requestText(bundleUrl, {
        requestFactory: context.requestFactory,
        agent: cdnTransport.agent,
        timeoutMs: context.timeoutMs,
        maxBytes: MAX_BUNDLE_BYTES,
        expectedOrigin: bundleUrl.origin,
        accept: 'application/javascript,text/javascript,*/*;q=0.1',
        // CDN requests intentionally omit Fusion credentials, cookies, and referrers.
      });
      context.requests.cdn += 1;
    } catch (error) {
      if (requestStarted) context.requests.cdn += 1;
      throw new RuntimeEvidenceError(
        'CDN_BUNDLE_UNAVAILABLE',
        `Oracle App UI base bundle for ${application.id}@${application.version} could not be fetched.`
          + (context.enableProxy === false
            ? ` If ${bundleUrl.hostname} is not reachable directly, set enableProxy=true in fusionEnv.properties and retry.`
            : ''),
        {
          origin: bundleUrl.origin,
          causeCode: error && error.code ? error.code : 'HTTPS_REQUEST_FAILED',
          causeMessage: sanitizeTransportError(error),
        }
      );
    }
    const cache = publishBundleCache(paths, fetched.text, {
      environment: context.environment,
      extension: application,
      bundleUrl: bundleUrl.toString(),
      headers: fetched.headers,
      fetchedAt: new Date().toISOString(),
    });
    return { ...cache, cacheStatus: corrupt ? 'repaired' : 'populated' };
  } finally {
    lock.release();
  }
}

function evidenceManifestContent(environment, graph) {
  return {
    schemaVersion: 2,
    environment,
    target: graph.target,
    rootNode: graph.rootNode,
    complete: graph.complete,
    // Cache hit/miss status is invocation telemetry, not deployed-source provenance.
    bundles: graph.bundles.map(({ cacheStatus, ...bundle }) => bundle),
    nodes: graph.nodes,
    edges: graph.edges,
    evidence: graph.evidence,
    unresolved: graph.unresolved,
    trustBoundary: {
      downloadedArtifactsAreEvidenceOnly: true,
      customerExtensionOverlaysIncluded: false,
      observedRuntimeValuesIncluded: false,
    },
    runtimeShapeVerification: {
      // Static deployed modules can prove contracts, but they do not observe $value() results.
      observed: false,
      source: 'static-deployed-evidence',
    },
  };
}

function publishEvidenceManifest(paths, content) {
  ensureCacheRoot(paths);
  const evidenceDirectory = safeJoin(paths.schemaRoot, 'evidence');
  fs.mkdirSync(evidenceDirectory, { recursive: true, mode: 0o700 });
  assertNoSymlinkBetween(paths.cacheRoot, evidenceDirectory);
  const identity = {
    // Version the identity so an additive manifest contract cannot collide with immutable v1 files.
    schemaVersion: content.schemaVersion,
    target: content.target,
    bundles: content.bundles.map((bundle) => ({
      extension: bundle.extension,
      version: bundle.version,
      bundleSha256: bundle.bundleSha256,
    })),
    evidence: content.evidence.map((item) => ({
      moduleId: item.moduleId,
      sha256: item.sha256,
    })),
    unresolved: content.unresolved,
  };
  const graphId = sha256(JSON.stringify(identity));
  const manifestPath = safeJoin(evidenceDirectory, `${graphId}.json`);
  const serialized = `${JSON.stringify(content, null, 2)}\n`;
  if (fs.existsSync(manifestPath)) {
    if (sha256(fs.readFileSync(manifestPath)) !== sha256(serialized)) {
      throw new RuntimeEvidenceError(
        'EVIDENCE_CACHE_COLLISION',
        `Evidence manifest ${graphId} already exists with different content.`
      );
    }
    return manifestPath;
  }

  const stagingPath = safeJoin(
    evidenceDirectory,
    `.staging-${graphId}-${process.pid}-${crypto.randomBytes(6).toString('hex')}`
  );
  try {
    fs.writeFileSync(stagingPath, serialized, { mode: 0o600, flag: 'wx' });
    fs.renameSync(stagingPath, manifestPath);
  } catch (error) {
    if (fs.existsSync(stagingPath)) fs.rmSync(stagingPath, { force: true });
    // A concurrent identical publisher wins safely; verify before reusing its result.
    if (fs.existsSync(manifestPath) && sha256(fs.readFileSync(manifestPath)) === sha256(serialized)) {
      return manifestPath;
    }
    throw error;
  }
  return manifestPath;
}

function unresolvedFromError(error) {
  return [{
    code: error instanceof RuntimeEvidenceError ? error.code : 'RUNTIME_EVIDENCE_FAILED',
    source: 'runtime-bundle',
    target: null,
    reason: error.message,
    details: error instanceof RuntimeEvidenceError ? error.details : null,
  }];
}

async function fetchRuntimeEvidence(options, dependencies = {}) {
  let target = normalizeTarget(options);
  const workspace = path.resolve(options.workspace || process.cwd());
  const propertiesPath = options.propertiesPath || DEFAULT_PROPERTIES;
  const environmentContext = (dependencies.parseSafeEnvironment || parseSafeEnvironment)(propertiesPath);
  const environment = environmentContext.restBaseUrl;
  if (target.kind === 'redwood-route') {
    target = {
      kind: 'redwood-url',
      route: resolvePropertyBackedRoute(target.routePath, environment),
      fallbackDynamicLayout: target.fallbackDynamicLayout,
      routeSource: 'fusionEnv.properties',
    };
  }
  const restCall = dependencies.callFusionRest || callFusionRest;
  const manifestResponse = restCall({
    endpoint: '/fscmRestApi/vxmanifest/v2/digests/latest',
    query: ['type=app-ui-info'],
    propertiesPath,
    timeoutSeconds: Math.ceil(options.timeoutMs / 1000),
    tokenCache: options.tokenCache,
  }, dependencies.restDependencies || {});
  if (manifestResponse.body.length > MAX_MANIFEST_BYTES) {
    throw new RuntimeEvidenceError('RESPONSE_TOO_LARGE', 'App-info response exceeded the safe size limit.');
  }
  const applicationIndex = parseManifestResponse(manifestResponse.body.toString('utf8'));
  if (target.kind === 'redwood-url') {
    const route = target.route;
    const resolved = resolveApplicationFromRoute(applicationIndex, route);
    // The supplied URL is route context only; Fusion calls use fusionEnv.properties.
    target = {
      kind: 'ui-page',
      extension: resolved.extension,
      application: resolved.application,
      flow: resolved.flow,
      page: resolved.page,
      fallbackDynamicLayout: target.fallbackDynamicLayout,
      routeResolution: {
        matchReason: resolved.matchReason,
        suppliedOrigin: route.origin,
        environmentOriginMatched: route.origin === new URL(environment).origin,
        routeSource: target.routeSource || 'target-url',
      },
    };
  }
  // Fail before any CDN request when the root target is not deployed.
  requireApplication(applicationIndex, target.extension);

  const context = {
    workspace,
    cacheRoot: options.cacheRoot ? path.resolve(options.cacheRoot) : null,
    environment,
    applicationIndex,
    requestFactory: dependencies.requestFactory,
    cdnOrigin: resolveCdnOrigin(environment),
    enableProxy: environmentContext.enableProxy !== false,
    cdnProxy: options.cdnProxy,
    resolveCdnTransport: dependencies.resolveCdnTransport,
    resolveSystemProxy: dependencies.resolveSystemProxy || (dependencies.resolveCdnProxy
      ? (url) => {
        const proxy = dependencies.resolveCdnProxy(url);
        return { mode: proxy ? 'system-pac' : 'system-direct', proxy };
      }
      : undefined),
    proxyEnvironment: dependencies.proxyEnvironment
      || (dependencies.requestFactory ? {} : process.env),
    proxyPlatform: dependencies.proxyPlatform
      || (dependencies.requestFactory ? 'test' : process.platform),
    proxySpawnSync: dependencies.proxySpawnSync,
    cdnProxyModes: new Set(),
    timeoutMs: options.timeoutMs,
    requests: {
      fusionRest: manifestResponse.requestCount || 1,
      cdn: 0,
    },
  };
    const rootApplication = requireApplication(applicationIndex, target.extension);
    let graph;
    try {
      graph = await resolveEvidenceGraph({
        target,
        applicationIndex,
        loadBundle: (extensionId) => loadOrFetchBundle(context, extensionId),
        limits: dependencies.limits,
      });
    } catch (error) {
      if (!(error instanceof RuntimeEvidenceError) || error.code !== 'CDN_BUNDLE_UNAVAILABLE') {
        throw error;
      }
      // Preserve the environment/app-info evidence when only Oracle CDN retrieval is pending.
      return {
        schemaVersion: 2,
        status: 'blocked',
        proposalAllowed: false,
        environment,
        transport: {
          mode: 'core-rest-plus-anonymous-cdn',
          cdnProxyMode: context.cdnProxyModes.size === 1
            ? [...context.cdnProxyModes][0]
            : (context.cdnProxyModes.size > 1 ? 'mixed' : 'not-used'),
        },
        target,
        bundles: [{
          extension: rootApplication.id,
          version: rootApplication.version,
          description: rootApplication.description || null,
          bundleSha256: null,
          cacheStatus: 'unavailable',
        }],
        evidenceGraph: {
          complete: false,
          nodeCount: 0,
          edgeCount: 0,
          manifestPath: null,
          unresolved: unresolvedFromError(error),
        },
        runtimeValidation: {
          environment: 'verified',
          cdn: 'pending',
        },
        runtimeShapeVerification: {
          observed: false,
          source: 'static-deployed-evidence',
        },
        requests: context.requests,
      };
    }
    const rootPaths = resolveCachePaths(
      workspace,
      environment,
      rootApplication.id,
      rootApplication.version,
      context.cacheRoot
    );
    const manifestPath = publishEvidenceManifest(
      rootPaths,
      evidenceManifestContent(environment, graph)
    );

    return {
      schemaVersion: 2,
      status: graph.complete ? 'complete' : 'blocked',
      proposalAllowed: false,
      environment,
      transport: {
        mode: 'core-rest-plus-anonymous-cdn',
        cdnProxyMode: context.cdnProxyModes.size === 1
          ? [...context.cdnProxyModes][0]
          : (context.cdnProxyModes.size > 1 ? 'mixed' : 'not-used'),
      },
      target: graph.target,
      bundles: graph.bundles,
      evidenceGraph: {
        complete: graph.complete,
        nodeCount: graph.nodes.length,
        edgeCount: graph.edges.length,
        manifestPath,
        unresolved: graph.unresolved,
      },
      runtimeValidation: {
        environment: 'verified',
        cdn: 'verified',
      },
      runtimeShapeVerification: {
        observed: false,
        source: 'static-deployed-evidence',
      },
      requests: context.requests,
    };
}

function errorPayload(error) {
  return {
    error: {
      // Preserve structured authentication and transport codes from core adapters.
      code: error.code || 'RUNTIME_EVIDENCE_FAILED',
      message: error.message,
      details: error instanceof RuntimeEvidenceError ? error.details : null,
    },
  };
}

async function main() {
  try {
    const options = parseArgs(process.argv.slice(2));
    if (options.help) {
      printHelp();
      return;
    }
    const result = await fetchRuntimeEvidence(options);
    if (options.json) {
      process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
      return;
    }
    process.stdout.write([
      `Environment: ${result.environment}`,
      `Transport: ${result.transport.mode} (${result.transport.cdnProxyMode})`,
      `Target: ${result.target.kind} ${result.target.extension}`,
      `Runtime validation: environment ${result.runtimeValidation.environment}, CDN ${result.runtimeValidation.cdn}`,
      `Runtime values observed: ${result.runtimeShapeVerification.observed ? 'yes' : 'no'}`,
      `Evidence complete: ${result.evidenceGraph.complete ? 'yes' : 'no'}`,
      `Evidence manifest: ${result.evidenceGraph.manifestPath}`,
      `Bundles: ${result.bundles.length}`,
      `Requests: Fusion REST ${result.requests.fusionRest}, CDN ${result.requests.cdn}`,
      '',
    ].join('\n'));
  } catch (error) {
    process.stderr.write(`${JSON.stringify(errorPayload(error), null, 2)}\n`);
    process.exitCode = 1;
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  MAX_BUNDLE_BYTES,
  MAX_MANIFEST_BYTES,
  errorPayload,
  evidenceManifestContent,
  fetchRuntimeEvidence,
  loadOrFetchBundle,
  normalizeTarget,
  resolvePropertyBackedRoute,
  parseArgs,
  createCdnProxyAgent,
  resolveAutomaticCdnProxy,
  resolveCdnTransport,
  parseManifestResponse,
  publishEvidenceManifest,
  requestText,
};
