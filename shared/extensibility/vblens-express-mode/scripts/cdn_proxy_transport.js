'use strict';

/**
 * Resolve an anonymous proxy only for approved Oracle CDN bundle requests.
 * Authenticated Fusion REST continues to use the FSCR central REST client.
 */

const childProcess = require('node:child_process');
const fs = require('node:fs');
const http = require('node:http');
const https = require('node:https');
const os = require('node:os');
const path = require('node:path');
const tls = require('node:tls');
const { RuntimeEvidenceError } = require('./runtime_bundle');

const APPROVED_CDN_HOSTS = new Set(['static.oracle.com', 'static-stage.oracle.com']);
const AUTO_PROXY_TIMEOUT_MS = 60000;
const MACOS_PROXY_RESOLVER = path.join(__dirname, 'resolve_cdn_proxy_macos.swift');
const MACOS_PROXY_MODULE_CACHE = path.join(os.tmpdir(), 'fscr-vblens-swift-module-cache-v1');

function firstDefinedEnvironmentValue(environment, lowerKey, upperKey) {
  if (Object.prototype.hasOwnProperty.call(environment, lowerKey)) return environment[lowerKey];
  return environment[upperKey];
}

function selectedEnvironmentProxy(environment = process.env) {
  const httpsProxy = firstDefinedEnvironmentValue(environment, 'https_proxy', 'HTTPS_PROXY');
  if (typeof httpsProxy === 'string' && httpsProxy.trim()) return httpsProxy.trim();
  const allProxy = firstDefinedEnvironmentValue(environment, 'all_proxy', 'ALL_PROXY');
  return typeof allProxy === 'string' && allProxy.trim() ? allProxy.trim() : null;
}

function selectedNoProxy(environment = process.env) {
  const noProxy = firstDefinedEnvironmentValue(environment, 'no_proxy', 'NO_PROXY');
  return typeof noProxy === 'string' ? noProxy : '';
}

function proxyBypassedForUrl(url, environment = process.env) {
  let parsed;
  try {
    parsed = url instanceof URL ? url : new URL(String(url || ''));
  } catch (error) {
    return false;
  }
  const host = parsed.hostname.toLowerCase();
  const port = parsed.port || (parsed.protocol === 'https:' ? '443' : '80');
  return selectedNoProxy(environment)
    .split(',')
    .map((entry) => entry.trim().toLowerCase())
    .filter(Boolean)
    .some((entry) => {
      if (entry === '*') return true;
      const separator = entry.lastIndexOf(':');
      const hasSinglePort = separator > 0 && entry.indexOf(':') === separator;
      const patternHost = hasSinglePort ? entry.slice(0, separator) : entry;
      const patternPort = hasSinglePort ? entry.slice(separator + 1) : null;
      if (patternPort && patternPort !== port) return false;
      if (patternHost.startsWith('.')) {
        return host === patternHost.slice(1) || host.endsWith(patternHost);
      }
      return host === patternHost || host.endsWith(`.${patternHost}`);
    });
}

function validateCdnTarget(url) {
  if (
    !(url instanceof URL)
    || url.protocol !== 'https:'
    || url.username
    || url.password
    || !APPROVED_CDN_HOSTS.has(url.hostname)
  ) {
    throw new RuntimeEvidenceError(
      'INVALID_CDN_PROXY_TARGET',
      'CDN proxy resolution is limited to approved Oracle CDN hosts.'
    );
  }
  return url;
}

function validateCdnProxyOrigin(proxyValue, label = 'CDN proxy') {
  let proxy;
  try {
    proxy = new URL(String(proxyValue || ''));
  } catch (error) {
    throw new RuntimeEvidenceError('INVALID_CDN_PROXY', `${label} must be a valid HTTP URL.`);
  }
  if (
    proxy.protocol !== 'http:'
    || proxy.username
    || proxy.password
    || proxy.pathname !== '/'
    || proxy.search
    || proxy.hash
  ) {
    throw new RuntimeEvidenceError(
      'INVALID_CDN_PROXY',
      `${label} must be an anonymous HTTP origin without a path.`
    );
  }
  return proxy;
}

function createCdnProxyAgent(proxyValue) {
  const proxy = validateCdnProxyOrigin(proxyValue);
  const agent = new https.Agent({ keepAlive: false });
  agent.createConnection = (options, callback) => {
    const connectRequest = http.request({
      host: proxy.hostname,
      port: proxy.port || 80,
      method: 'CONNECT',
      path: `${options.host}:${options.port || 443}`,
      headers: { Host: `${options.host}:${options.port || 443}` },
    });
    connectRequest.once('connect', (response, socket, head) => {
      if (response.statusCode !== 200) {
        socket.destroy();
        callback(new RuntimeEvidenceError('CDN_PROXY_CONNECT_FAILED', 'CDN proxy tunnel was rejected.'));
        return;
      }
      if (head.length > 0) socket.unshift(head);
      const secureSocket = tls.connect({
        socket,
        servername: options.servername || options.host,
        rejectUnauthorized: true,
      });
      secureSocket.once('secureConnect', () => callback(null, secureSocket));
      secureSocket.once('error', (error) => callback(error));
    });
    connectRequest.once('error', (error) => callback(error));
    connectRequest.end();
  };
  return agent;
}

function resolveSystemCdnProxy(url, dependencies = {}) {
  validateCdnTarget(url);
  const platform = dependencies.platform || process.platform;
  if (platform !== 'darwin') return { mode: 'direct', proxy: null };
  const spawnSync = dependencies.spawnSync || childProcess.spawnSync;
  let result;
  try {
    fs.mkdirSync(MACOS_PROXY_MODULE_CACHE, { recursive: true, mode: 0o700 });
    const cacheStat = fs.lstatSync(MACOS_PROXY_MODULE_CACHE);
    if (!cacheStat.isDirectory() || cacheStat.isSymbolicLink()) {
      throw new Error('unsafe module-cache path');
    }
    fs.chmodSync(MACOS_PROXY_MODULE_CACHE, 0o700);
    result = spawnSync('/usr/bin/swift', [MACOS_PROXY_RESOLVER, url.toString()], {
      encoding: 'utf8',
      env: {
        ...process.env,
        CLANG_MODULE_CACHE_PATH: MACOS_PROXY_MODULE_CACHE,
        SWIFT_MODULECACHE_PATH: MACOS_PROXY_MODULE_CACHE,
      },
      maxBuffer: 64 * 1024,
      timeout: AUTO_PROXY_TIMEOUT_MS,
      windowsHide: true,
    });
  } catch (error) {
    throw new RuntimeEvidenceError(
      'CDN_PROXY_AUTO_RESOLUTION_FAILED',
      'The macOS Oracle CDN proxy resolver could not be started safely.'
    );
  }
  if (result.error || result.status !== 0) {
    throw new RuntimeEvidenceError(
      'CDN_PROXY_AUTO_RESOLUTION_FAILED',
      'macOS could not resolve an anonymous proxy for the Oracle CDN request.'
    );
  }
  let payload;
  try {
    payload = JSON.parse(String(result.stdout || ''));
  } catch (error) {
    throw new RuntimeEvidenceError(
      'CDN_PROXY_AUTO_RESOLUTION_FAILED',
      'macOS returned an invalid Oracle CDN proxy decision.'
    );
  }
  if (payload.mode === 'DIRECT') return { mode: 'system-direct', proxy: null };
  if (payload.mode !== 'PROXY' || typeof payload.proxy !== 'string') {
    throw new RuntimeEvidenceError(
      'CDN_PROXY_AUTO_RESOLUTION_FAILED',
      'macOS returned an unsupported Oracle CDN proxy decision.'
    );
  }
  validateCdnProxyOrigin(payload.proxy, 'macOS CDN proxy');
  return { mode: 'system-pac', proxy: payload.proxy };
}

function resolveAutomaticCdnProxy(url, dependencies = {}) {
  return resolveSystemCdnProxy(url, dependencies).proxy;
}

function resolveCdnTransport(url, options = {}) {
  validateCdnTarget(url);
  if (options.enableProxy === false) return { mode: 'direct', agent: undefined };
  const environment = options.environment || process.env;
  const explicitProxy = options.explicitProxy;
  if (explicitProxy && explicitProxy !== 'auto') {
    return {
      mode: 'explicit',
      agent: createCdnProxyAgent(explicitProxy),
    };
  }
  if (proxyBypassedForUrl(url, environment)) {
    return { mode: 'no-proxy', agent: undefined };
  }
  const environmentProxy = selectedEnvironmentProxy(environment);
  if (environmentProxy) {
    validateCdnProxyOrigin(environmentProxy, 'Environment CDN proxy');
    return {
      mode: 'environment',
      agent: createCdnProxyAgent(environmentProxy),
    };
  }
  const system = (options.resolveSystemProxy || resolveSystemCdnProxy)(url, {
    platform: options.platform,
    spawnSync: options.spawnSync,
  });
  return {
    mode: system.mode,
    agent: system.proxy ? createCdnProxyAgent(system.proxy) : undefined,
  };
}

module.exports = {
  APPROVED_CDN_HOSTS,
  createCdnProxyAgent,
  firstDefinedEnvironmentValue,
  proxyBypassedForUrl,
  resolveAutomaticCdnProxy,
  resolveCdnTransport,
  resolveSystemCdnProxy,
  selectedEnvironmentProxy,
  selectedNoProxy,
  validateCdnProxyOrigin,
  validateCdnTarget,
};
