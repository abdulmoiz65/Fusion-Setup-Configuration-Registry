#!/usr/bin/env node
'use strict';

/**
 * Resolve a page-neutral behavior checklist without classifying field evidence.
 * This command never reads credentials or changes a Fusion workspace.
 */

const fs = require('node:fs');
const path = require('node:path');

const CONTRACT_PATH = path.resolve(
  __dirname,
  '..',
  'references',
  'data',
  'behavior-contracts.json'
);

class SolutionContractError extends Error {
  constructor(code, message, details = null) {
    super(message);
    this.name = 'SolutionContractError';
    this.code = code;
    this.details = details;
  }
}

function readOptionValue(argv, index, optionName) {
  const value = argv[index + 1];
  if (!value || value.startsWith('--')) {
    throw new SolutionContractError('INVALID_ARGUMENT', `${optionName} requires a value.`);
  }
  return value;
}

function parseArgs(argv) {
  const options = {
    intent: null,
    list: false,
    json: false,
    help: false,
  };
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === '--intent') {
      options.intent = readOptionValue(argv, index, argument);
      index += 1;
    } else if (argument === '--list') {
      options.list = true;
    } else if (argument === '--json') {
      options.json = true;
    } else if (argument === '--help' || argument === '-h') {
      options.help = true;
    } else {
      throw new SolutionContractError('INVALID_ARGUMENT', `Unknown argument: ${argument}`);
    }
  }
  return options;
}

function loadRegistry() {
  const registry = JSON.parse(fs.readFileSync(CONTRACT_PATH, 'utf8'));
  if (registry.schemaVersion !== 1 || !Array.isArray(registry.contracts)) {
    throw new SolutionContractError('INVALID_REGISTRY', 'Behavior contract registry is invalid.');
  }
  const identities = new Map();
  for (const contract of registry.contracts) {
    if (!contract?.id || !Array.isArray(contract.intents)
        || !Array.isArray(contract.requiredCapabilities)
        || !Array.isArray(contract.codeBranches)
        || !Array.isArray(contract.forbiddenInferences)) {
      throw new SolutionContractError(
        'INVALID_REGISTRY',
        `Behavior contract is incomplete: ${contract?.id || 'unknown'}`
      );
    }
    // IDs and aliases share one namespace so resolution remains deterministic.
    for (const identity of [contract.id, ...contract.intents]) {
      const normalized = identity.toLowerCase();
      const existingOwner = identities.get(normalized);
      if (existingOwner && existingOwner !== contract.id) {
        throw new SolutionContractError(
          'INVALID_REGISTRY',
          `Duplicate behavior contract identity: ${identity}`
        );
      }
      identities.set(normalized, contract.id);
    }
  }
  return registry;
}

function resolveContract(registry, intent) {
  const normalized = String(intent || '').trim().toLowerCase();
  if (!normalized) {
    throw new SolutionContractError('INVALID_ARGUMENT', '--intent is required unless --list is used.');
  }
  const matches = registry.contracts.filter((contract) => (
    contract.id.toLowerCase() === normalized
    || contract.intents.some((candidate) => candidate.toLowerCase() === normalized)
  ));
  if (matches.length === 0) {
    throw new SolutionContractError('CONTRACT_NOT_FOUND', `No behavior contract matches intent: ${intent}`);
  }
  if (matches.length > 1) {
    throw new SolutionContractError(
      'CONTRACT_AMBIGUOUS',
      `Multiple behavior contracts match intent: ${intent}`,
      matches.map((contract) => contract.id)
    );
  }
  return matches[0];
}

function buildResult(registry, contract) {
  // Return the reusable checklist unchanged so semantic conclusions remain model-owned.
  return {
    schemaVersion: registry.schemaVersion,
    contract: {
      id: contract.id,
      intents: contract.intents,
      requiredCapabilities: contract.requiredCapabilities,
      setupPolicy: contract.setupPolicy,
      codeBranches: contract.codeBranches,
      forbiddenInferences: contract.forbiddenInferences,
    },
  };
}

function printHelp() {
  process.stdout.write([
    'Resolve an Express Mode behavior contract',
    '',
    'Usage:',
    '  node scripts/resolve_solution_contract.js --list --json',
    '  node scripts/resolve_solution_contract.js --intent <intent> [--json]',
    '',
  ].join('\n'));
}

function main() {
  try {
    const options = parseArgs(process.argv.slice(2));
    if (options.help) return printHelp();
    const registry = loadRegistry();
    if (options.list) {
      const result = registry.contracts.map((contract) => ({ id: contract.id, intents: contract.intents }));
      process.stdout.write(`${JSON.stringify(result, null, options.json ? 2 : 0)}\n`);
      return;
    }
    const contract = resolveContract(registry, options.intent);
    const result = buildResult(registry, contract);
    process.stdout.write(options.json
      ? `${JSON.stringify(result, null, 2)}\n`
      : `${result.contract.id}\n`);
  } catch (error) {
    const payload = {
      error: {
        code: error.code || 'UNEXPECTED_ERROR',
        message: error.message,
        details: error.details || null,
      },
    };
    process.stderr.write(`${JSON.stringify(payload, null, 2)}\n`);
    process.exitCode = 1;
  }
}

if (require.main === module) main();

module.exports = {
  SolutionContractError,
  buildResult,
  loadRegistry,
  parseArgs,
  resolveContract,
};
