#!/usr/bin/env node
'use strict';

/**
 * Adapt this Node-based skill to the repository-owned Python Fusion REST CLI.
 * Normal JSON REST calls stay in the central client and tokens never cross this adapter.
 */

const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const REPOSITORY_ROOT = path.resolve(__dirname, '..', '..', '..', '..');
const CLIENT_DIRECTORY = path.join(REPOSITORY_ROOT, 'core', 'fusion-api', 'rest-api-client', 'scripts');
const DEFAULT_PROPERTIES = path.join(REPOSITORY_ROOT, 'core', 'auth', 'fusionEnv.properties');
const SUPPORTED_METHODS = new Set(['GET', 'POST', 'PUT', 'PATCH', 'DELETE']);

class FusionRestAdapterError extends Error {
  constructor(code, message) {
    super(message);
    this.name = 'FusionRestAdapterError';
    this.code = code;
  }
}

function parseSafeEnvironment(propertiesPath = DEFAULT_PROPERTIES) {
  // Read only the non-secret fields needed for request routing and audit output.
  const values = {};
  for (const line of fs.readFileSync(propertiesPath, 'utf8').split(/\r?\n/)) {
    const match = line.match(/^\s*([^#=\s]+)\s*=\s*(.*)$/);
    if (match && ['environment', 'restBaseUrl', 'enableProxy'].includes(match[1])) values[match[1]] = match[2].trim();
  }
  if (!values.environment || !values.restBaseUrl) {
    throw new Error('fusionEnv.properties must define environment and restBaseUrl.');
  }
  if (values.enableProxy !== undefined && !/^(true|false)$/i.test(values.enableProxy)) {
    throw new FusionRestAdapterError('INVALID_ENABLE_PROXY', 'enableProxy must be true or false in fusionEnv.properties.');
  }
  const baseUrl = new URL(values.restBaseUrl);
  if (baseUrl.protocol !== 'https:' || baseUrl.username || baseUrl.password) {
    throw new Error('restBaseUrl must be an HTTPS URL without embedded credentials.');
  }
  return {
    environment: values.environment,
    enableProxy: values.enableProxy === undefined || values.enableProxy.toLowerCase() === 'true',
    restBaseUrl: `${baseUrl.origin}/`,
    propertiesPath: path.resolve(propertiesPath),
  };
}

function runClient(scriptName, args, options = {}) {
  // Bound child-process output because response bytes are written to a private file.
  const run = options.spawnSync || spawnSync;
  return run(options.python || 'python3', [path.join(CLIENT_DIRECTORY, scriptName), ...args], {
    cwd: options.cwd || process.cwd(),
    encoding: 'utf8',
    maxBuffer: options.maxBuffer || 4 * 1024 * 1024,
  });
}

function callFusionRest(options, dependencies = {}) {
  // Pass JSON methods to the existing central client without implementing HTTP here.
  const method = String(options.method || 'GET').toUpperCase();
  if (!SUPPORTED_METHODS.has(method)) throw new Error(`Unsupported Fusion REST method: ${method}`);
  if (options.jsonBody !== undefined && options.bodyFile) {
    throw new Error('Provide jsonBody or bodyFile, not both.');
  }
  const temporaryRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'fscr-fusion-rest-'));
  const outputPath = path.join(temporaryRoot, 'response.bin');
  try {
    const args = [
      options.endpoint,
      '--method', method,
      '--properties', options.propertiesPath || DEFAULT_PROPERTIES,
      '--output', outputPath,
      '--timeout', String(options.timeoutSeconds || 300),
    ];
    for (const query of options.query || []) args.push('--query', query);
    for (const header of options.headers || []) args.push('--header', header);
    if (options.jsonBody !== undefined) args.push('--body', JSON.stringify(options.jsonBody));
    if (options.bodyFile) args.push('--body-file', path.resolve(options.bodyFile));
    if (options.tokenCache) args.push('--token-cache', path.resolve(options.tokenCache));
    const scriptName = String(options.endpoint).startsWith('/api/boss')
      ? 'boss-rest_client.py'
      : 'fusion_rest_client.py';
    const result = runClient(scriptName, args, dependencies);
    if (result.status !== 0) {
      const message = (result.stderr || result.stdout || 'Fusion REST request failed.').trim();
      throw new FusionRestAdapterError('FUSION_REST_FAILED', message);
    }
    const statusMatch = String(result.stdout || '').match(/HTTP\s+(\d+)/);
    return {
      status: statusMatch ? Number(statusMatch[1]) : 200,
      body: fs.readFileSync(outputPath),
      environment: parseSafeEnvironment(options.propertiesPath || DEFAULT_PROPERTIES),
      requestCount: 1,
    };
  } finally {
    fs.rmSync(temporaryRoot, { recursive: true, force: true });
  }
}

module.exports = {
  CLIENT_DIRECTORY,
  DEFAULT_PROPERTIES,
  FusionRestAdapterError,
  callFusionRest,
  parseSafeEnvironment,
};
