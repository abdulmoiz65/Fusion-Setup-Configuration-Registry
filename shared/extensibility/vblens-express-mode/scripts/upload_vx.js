#!/usr/bin/env node
'use strict';

/**
 * Stream one approved VX archive to Fusion with a cached OAuth token.
 * This is the skill's only direct HTTP path because the central client accepts JSON bodies only.
 */

const fs = require('node:fs');
const https = require('node:https');
const path = require('node:path');

const UPLOAD_PATH = '/fscmRestApi/vx/v2/extensions';
const MAX_ARCHIVE_BYTES = 512 * 1024 * 1024;
const MAX_RESPONSE_BYTES = 1024 * 1024;
const TOKEN_EXPIRY_SKEW_SECONDS = 60;

function validateArchive(archivePath) {
  // Reject links and unexpected file types before reading authentication state.
  const resolved = path.resolve(archivePath);
  const stats = fs.lstatSync(resolved);
  if (stats.isSymbolicLink() || !stats.isFile()) {
    throw new Error('The VX archive must be a regular, non-symlink file.');
  }
  if (path.extname(resolved).toLowerCase() !== '.vx') {
    throw new Error('The deployment archive must use the .vx extension.');
  }
  if (stats.size <= 0 || stats.size > MAX_ARCHIVE_BYTES) {
    throw new Error(`VX archive size must be between 1 and ${MAX_ARCHIVE_BYTES} bytes.`);
  }
  return { path: resolved, size: stats.size };
}

function readCachedAccessToken(tokenCache, nowSeconds = Math.floor(Date.now() / 1000)) {
  // Read only the local file cache created by the repository OAuth workflow.
  if (!tokenCache) throw new Error('Deployment requires --token-cache with a local OAuth cache file.');
  const resolved = path.resolve(tokenCache);
  const stats = fs.lstatSync(resolved);
  if (stats.isSymbolicLink() || !stats.isFile() || stats.size > 1024 * 1024) {
    throw new Error('The OAuth token cache must be a small, regular, non-symlink file.');
  }
  let payload;
  try {
    payload = JSON.parse(fs.readFileSync(resolved, 'utf8'));
  } catch (error) {
    throw new Error('The OAuth token cache is not valid JSON.');
  }
  if (payload.token_type && String(payload.token_type).toLowerCase() !== 'bearer') {
    throw new Error('The OAuth token cache must contain a Bearer token.');
  }
  if (typeof payload.access_token !== 'string' || !payload.access_token) {
    throw new Error('The OAuth token cache does not contain an access token.');
  }
  if (!Number.isFinite(Number(payload.expires_at))
      || Number(payload.expires_at) <= nowSeconds + TOKEN_EXPIRY_SKEW_SECONDS) {
    throw new Error('The OAuth token cache is expired; rebuild it with the core OAuth login workflow.');
  }
  return payload.access_token;
}

function resolveUploadEndpoint(restBaseUrl) {
  // Lock the direct request to the configured Fusion origin and fixed upload path.
  const base = new URL(restBaseUrl);
  if (base.protocol !== 'https:' || base.username || base.password) {
    throw new Error('restBaseUrl must be an HTTPS URL without embedded credentials.');
  }
  return new URL(UPLOAD_PATH, `${base.origin}/`);
}

function redactResponse(value) {
  // Remove credential-shaped response fields before returning or persisting results.
  if (Array.isArray(value)) return value.map(redactResponse);
  if (!value || typeof value !== 'object') return value;
  return Object.fromEntries(Object.entries(value).map(([key, child]) => [
    key,
    /(password|secret|token|cookie|authorization|session)/i.test(key)
      ? '[redacted]'
      : redactResponse(child),
  ]));
}

function parseResponse(chunks, truncated) {
  // Return JSON when possible and otherwise return bounded metadata, never raw binary data.
  const body = Buffer.concat(chunks);
  try {
    return redactResponse(JSON.parse(body.toString('utf8')));
  } catch (error) {
    return { encoding: 'opaque', size: body.length, truncated };
  }
}

function defaultStreamArchive(archivePath, request) {
  // Stream the archive so deployment does not allocate the full VX file in memory.
  const stream = fs.createReadStream(archivePath);
  stream.on('error', (error) => request.destroy(error));
  stream.pipe(request);
}

function uploadVxOnce(options, dependencies = {}) {
  // Validate every local input before creating the single outbound POST request.
  const archive = (dependencies.validateArchive || validateArchive)(options.archivePath);
  const accessToken = (dependencies.readCachedAccessToken || readCachedAccessToken)(options.tokenCache);
  const endpoint = resolveUploadEndpoint(options.restBaseUrl);
  const requestFactory = dependencies.requestFactory || https.request;
  const streamArchive = dependencies.streamArchive || defaultStreamArchive;
  const timeoutMs = Number(options.timeoutMs || 300000);
  if (!Number.isSafeInteger(timeoutMs) || timeoutMs <= 0) {
    throw new Error('Upload timeout must be a positive integer.');
  }

  return new Promise((resolve, reject) => {
    // Create one request only; callers must obtain fresh approval before any retry.
    const request = requestFactory(endpoint, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${accessToken}`,
        Accept: 'application/json',
        'Content-Type': 'application/octet-stream',
        'Content-Length': archive.size,
      },
      rejectUnauthorized: true,
    }, (response) => {
      const chunks = [];
      let received = 0;
      let truncated = false;
      response.on('data', (chunk) => {
        const bytes = Buffer.from(chunk);
        if (received < MAX_RESPONSE_BYTES) {
          const remaining = MAX_RESPONSE_BYTES - received;
          chunks.push(bytes.subarray(0, remaining));
        }
        received += bytes.length;
        if (received > MAX_RESPONSE_BYTES) truncated = true;
      });
      response.on('end', () => {
        const status = Number(response.statusCode || 0);
        resolve({
          accepted: status >= 200 && status < 300,
          status,
          response: parseResponse(chunks, truncated),
          failureClass: status === 401
            ? 'auth/authz'
            : status === 403
              ? 'auth/authz'
              : status >= 200 && status < 300
                ? null
                : 'Fusion API',
          requestCount: 1,
          retried: false,
        });
      });
      response.on('error', () => reject(new Error('Fusion upload response failed.')));
    });
    request.setTimeout(timeoutMs, () => request.destroy(new Error('Fusion upload timed out.')));
    request.on('error', () => reject(new Error('Fusion upload transport failed.')));
    streamArchive(archive.path, request);
  });
}

module.exports = {
  MAX_ARCHIVE_BYTES,
  UPLOAD_PATH,
  readCachedAccessToken,
  redactResponse,
  resolveUploadEndpoint,
  uploadVxOnce,
  validateArchive,
};
