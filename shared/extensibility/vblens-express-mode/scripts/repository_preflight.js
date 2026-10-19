#!/usr/bin/env node
'use strict';

/**
 * Inspect a Git-backed Fusion extension workspace without changing it.
 * The script intentionally uses only Node.js built-ins for standalone use.
 */

const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

function parseArgs(argv) {
  const options = {
    repo: process.cwd(),
    base: null,
    protectedBranches: [],
    json: false,
    help: false,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === '--repo') {
      options.repo = argv[index + 1];
      index += 1;
    } else if (value === '--base') {
      options.base = argv[index + 1];
      index += 1;
    } else if (value === '--protected-branch') {
      options.protectedBranches.push(argv[index + 1]);
      index += 1;
    } else if (value === '--json') {
      options.json = true;
    } else if (value === '--help' || value === '-h') {
      options.help = true;
    } else {
      throw new Error(`Unknown argument: ${value}`);
    }
  }

  return options;
}

function printHelp() {
  process.stdout.write(
    [
      'Repository preflight',
      '',
      'Usage:',
      '  node scripts/repository_preflight.js [--repo <path>] [--base <ref>]',
      '    [--protected-branch <name>] [--json]',
      '',
    ].join('\n')
  );
}

function runGit(repo, args, required = true) {
  try {
    return execFileSync('git', args, {
      cwd: repo,
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
    }).trim();
  } catch (error) {
    if (!required) {
      return null;
    }
    const detail = String(error.stderr || error.message || '').trim();
    throw new Error(`Git command failed: git ${args.join(' ')}${detail ? `\n${detail}` : ''}`);
  }
}

function readJsonIfPresent(filePath) {
  if (!fs.existsSync(filePath)) {
    return null;
  }

  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (error) {
    return {
      __parseError: error.message,
    };
  }
}

function findFirstFile(root, predicate) {
  if (!fs.existsSync(root)) {
    return null;
  }

  const queue = [root];
  while (queue.length > 0) {
    const current = queue.shift();
    const entries = fs.readdirSync(current, { withFileTypes: true });
    for (const entry of entries) {
      const entryPath = path.join(current, entry.name);
      if (entry.isDirectory()) {
        queue.push(entryPath);
      } else if (predicate(entryPath)) {
        return entryPath;
      }
    }
  }

  return null;
}

function toPortablePath(root, filePath) {
  if (!filePath) {
    return null;
  }
  return path.relative(root, filePath).split(path.sep).join('/');
}

function redactRemoteUrl(value) {
  if (!value) {
    return null;
  }

  try {
    const remoteUrl = new URL(value);
    if (remoteUrl.username || remoteUrl.password) {
      remoteUrl.username = '';
      remoteUrl.password = '';
    }
    return remoteUrl.toString();
  } catch {
    return value.replace(/:\/\/[^/@\s]+@/, '://');
  }
}

function parseAheadBehind(statusText) {
  const match = statusText.match(/^# branch\.ab \+(\d+) -(\d+)$/m);
  return match
    ? { ahead: Number(match[1]), behind: Number(match[2]) }
    : { ahead: null, behind: null };
}

function detectRemote(repo, upstream) {
  if (upstream && upstream.includes('/')) {
    return upstream.split('/')[0];
  }

  const remotes = runGit(repo, ['remote'], false);
  if (!remotes) {
    return null;
  }

  return remotes.split(/\r?\n/).filter(Boolean)[0] || null;
}

function detectDefaultBranch(repo, remote) {
  if (!remote) {
    return null;
  }

  const symbolic = runGit(
    repo,
    ['symbolic-ref', '--quiet', '--short', `refs/remotes/${remote}/HEAD`],
    false
  );
  if (!symbolic) {
    return null;
  }

  return symbolic.startsWith(`${remote}/`)
    ? symbolic.slice(remote.length + 1)
    : symbolic;
}

function detectTopology(repoRoot) {
  const sourcesRoot = path.join(repoRoot, 'extension1', 'sources');
  const vbExtensionPath = path.join(sourcesRoot, 'vb-extension.json');
  const fusionExtensionPath = path.join(sourcesRoot, 'extension.json');
  const selfAppsRoot = path.join(sourcesRoot, 'ui', 'self', 'applications');
  const appPath = findFirstFile(selfAppsRoot, (filePath) => path.basename(filePath) === 'app.json');

  if (fs.existsSync(vbExtensionPath)) {
    return {
      type: 'appui-extension',
      metadataPath: toPortablePath(repoRoot, vbExtensionPath),
      appPath: toPortablePath(repoRoot, appPath),
      previewRouteDiscoverable: Boolean(appPath),
    };
  }

  if (fs.existsSync(fusionExtensionPath)) {
    return {
      type: 'multi-product-fusion-extension',
      metadataPath: toPortablePath(repoRoot, fusionExtensionPath),
      appPath: null,
      previewRouteDiscoverable: false,
    };
  }

  return {
    type: 'unknown',
    metadataPath: null,
    appPath: null,
    previewRouteDiscoverable: false,
  };
}

function inspectArtifactFamilies(repoRoot) {
  const sourcesRoot = path.join(repoRoot, 'extension1', 'sources');
  const families = new Set();
  if (!fs.existsSync(sourcesRoot)) {
    return [];
  }

  const pending = [sourcesRoot];
  while (pending.length > 0) {
    const current = pending.pop();
    for (const entry of fs.readdirSync(current, { withFileTypes: true })) {
      const entryPath = path.join(current, entry.name);
      if (entry.isDirectory()) {
        pending.push(entryPath);
        continue;
      }

      const portablePath = toPortablePath(repoRoot, entryPath);
      const baseName = path.basename(entryPath);
      // Classify Express artifacts without assuming one release-specific page path.
      if (baseName === 'metadata-rules-x.json') {
        families.add('express-business-rules');
      }
      if (portablePath.includes('/metadataRules/')) {
        families.add('express-advanced-expressions');
      }
      if (baseName === 'page-x.json') {
        families.add('express-page-properties');
      }
      if (baseName === 'page-r-x.json') {
        // Write support remains conditional on counterpart and overlay-shape validation.
        families.add('express-page-property-rules-evidence-dependent');
      }
      if (baseName === 'layout-x.json') {
        // Layouts include field ordering, conditional variants, and container sections.
        families.add('express-rule-set-layout-evidence-dependent');
      }
      if (portablePath.startsWith('extension1/sources/ui/')) {
        families.add('out-of-scope-advanced-source');
      }
    }
  }

  return Array.from(families).sort();
}

function inspectBuild(repoRoot) {
  const packagePath = path.join(repoRoot, 'package.json');
  const packageJson = readJsonIfPresent(packagePath);
  const dependencies = packageJson && !packageJson.__parseError
    ? {
        ...(packageJson.dependencies || {}),
        ...(packageJson.devDependencies || {}),
      }
    : {};

  const buildDeclared = Boolean(dependencies['@oracle/grunt-vb-build']);
  const auditDeclared = Boolean(dependencies['@oracle/grunt-vb-audit']);
  const buildApiPath = path.join(
    repoRoot,
    'node_modules',
    '@oracle',
    'grunt-vb-build',
    'lib2',
    'index.js'
  );
  const gruntPath = path.join(repoRoot, 'node_modules', '.bin', 'grunt');

  return {
    packagePath: fs.existsSync(packagePath) ? 'package.json' : null,
    packageJsonValid: Boolean(packageJson && !packageJson.__parseError),
    packageJsonError: packageJson && packageJson.__parseError ? packageJson.__parseError : null,
    buildDeclared,
    auditDeclared,
    dependenciesInstalled: fs.existsSync(path.join(repoRoot, 'node_modules')),
    buildApiInstalled: fs.existsSync(buildApiPath),
    gruntInstalled: fs.existsSync(gruntPath),
    buildReady: buildDeclared && fs.existsSync(buildApiPath),
  };
}

function buildReport(options) {
  const requestedRepo = path.resolve(options.repo || process.cwd());
  const repoRoot = runGit(requestedRepo, ['rev-parse', '--show-toplevel']);
  const currentBranch = runGit(repoRoot, ['branch', '--show-current'], false) || null;
  const head = runGit(repoRoot, ['rev-parse', 'HEAD']);
  const upstream = runGit(
    repoRoot,
    ['rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{upstream}'],
    false
  );
  const remote = detectRemote(repoRoot, upstream);
  const defaultBranch = detectDefaultBranch(repoRoot, remote);
  const statusV2 = runGit(repoRoot, ['status', '--porcelain=v2', '--branch']);
  const statusShort = runGit(repoRoot, ['status', '--porcelain']);
  const changes = statusShort
    ? statusShort.split(/\r?\n/).filter(Boolean)
    : [];
  const explicitProtectedBranches = (options.protectedBranches || []).filter(Boolean);
  const protectedBranchSources = {
    builtIn: ['main', 'master'],
    remoteDefault: defaultBranch ? [defaultBranch] : [],
    explicit: explicitProtectedBranches,
    serverPolicyVerified: false,
  };
  const protectedBranches = Array.from(new Set([
    ...protectedBranchSources.builtIn,
    ...protectedBranchSources.remoteDefault,
    ...protectedBranchSources.explicit,
  ]));
  const remoteUrl = remote
    ? runGit(repoRoot, ['remote', 'get-url', '--push', remote], false)
    : null;
  const baseResolved = options.base
    ? runGit(repoRoot, ['rev-parse', '--verify', options.base], false)
    : null;
  const aheadBehind = parseAheadBehind(statusV2);
  const topology = detectTopology(repoRoot);
  const build = inspectBuild(repoRoot);
  const detached = !currentBranch;
  const protectedBranch = currentBranch
    ? protectedBranches.includes(currentBranch)
    : false;

  return {
    repository: {
      root: repoRoot,
      head,
      currentBranch,
      upstream,
      remote,
      remoteUrl: redactRemoteUrl(remoteUrl),
      defaultBranch,
      requestedBase: options.base,
      resolvedBase: baseResolved,
      ahead: aheadBehind.ahead,
      behind: aheadBehind.behind,
    },
    worktree: {
      clean: changes.length === 0,
      changeCount: changes.length,
      changes,
    },
    branchGate: {
      detached,
      protected: protectedBranch,
      protectedBranches,
      protectionSources: protectedBranchSources,
      safeToModify: !detached && !protectedBranch,
      requiresExistingWorkReview: changes.length > 0,
    },
    topology,
    artifactFamilies: inspectArtifactFamilies(repoRoot),
    build,
  };
}

function printHuman(report) {
  const lines = [
    `Repository: ${report.repository.root}`,
    `Branch: ${report.repository.currentBranch || '<detached>'}`,
    `Default branch: ${report.repository.defaultBranch || '<unknown>'}`,
    `Protected branch: ${report.branchGate.protected ? 'yes' : 'no'}`,
    `Safe to modify: ${report.branchGate.safeToModify ? 'yes' : 'no'}`,
    `Worktree clean: ${report.worktree.clean ? 'yes' : 'no'}`,
    `Topology: ${report.topology.type}`,
    `Extension metadata: ${report.topology.metadataPath || '<not found>'}`,
    `Build dependency declared: ${report.build.buildDeclared ? 'yes' : 'no'}`,
    `Build API installed: ${report.build.buildApiInstalled ? 'yes' : 'no'}`,
  ];
  process.stdout.write(`${lines.join('\n')}\n`);
}

function main() {
  try {
    const options = parseArgs(process.argv.slice(2));
    if (options.help) {
      printHelp();
      return;
    }

    const report = buildReport(options);
    if (options.json) {
      process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
    } else {
      printHuman(report);
    }
  } catch (error) {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = 1;
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  buildReport,
  detectTopology,
  inspectBuild,
  inspectArtifactFamilies,
  parseArgs,
  redactRemoteUrl,
};
