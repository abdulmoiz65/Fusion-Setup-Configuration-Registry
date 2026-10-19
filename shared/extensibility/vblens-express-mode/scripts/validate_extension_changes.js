#!/usr/bin/env node
'use strict';

/**
 * Validate changed Fusion extension artifacts without modifying the repository.
 * The checks focus on safe scope, parseability, and Business Rules consistency.
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execFileSync, spawnSync } = require('child_process');

function readOptionValue(argv, index, optionName) {
  const value = argv[index + 1];
  if (!value || value.startsWith('--')) {
    throw new Error(`${optionName} requires a value.`);
  }
  return value;
}

function parseArgs(argv) {
  const options = {
    repo: process.cwd(),
    base: null,
    expectedHead: null,
    evidenceManifest: null,
    allowReleaseToolingUpdate: false,
    requireClean: false,
    requireChanges: false,
    json: false,
    help: false,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === '--repo') {
      options.repo = readOptionValue(argv, index, value);
      index += 1;
    } else if (value === '--base') {
      options.base = readOptionValue(argv, index, value);
      index += 1;
    } else if (value === '--expected-head') {
      options.expectedHead = readOptionValue(argv, index, value);
      index += 1;
    } else if (value === '--evidence-manifest') {
      options.evidenceManifest = readOptionValue(argv, index, value);
      index += 1;
    } else if (value === '--allow-release-tooling-update') {
      options.allowReleaseToolingUpdate = true;
    } else if (value === '--require-clean') {
      options.requireClean = true;
    } else if (value === '--require-changes') {
      options.requireChanges = true;
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
      'Extension change validation',
      '',
      'Usage:',
      '  node scripts/validate_extension_changes.js [--repo <path>] [--base <ref>]',
      '    [--expected-head <commit>] [--evidence-manifest <path>]',
      '    [--allow-release-tooling-update] [--require-clean]',
      '    [--require-changes] [--json]',
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

function addFinding(findings, severity, code, message, file = null) {
  findings.push({
    severity,
    code,
    message,
    file,
  });
}

function escapeRegExp(value) {
  // Field paths are matched literally when checking companion accessor usage.
  return String(value).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function splitLines(value) {
  return value ? value.split(/\r?\n/).map((line) => line.trim()).filter(Boolean) : [];
}

function resolveBase(repo, requestedBase) {
  if (requestedBase) {
    const resolved = runGit(repo, ['rev-parse', '--verify', requestedBase], false);
    if (!resolved) {
      throw new Error(`Unable to resolve base ref: ${requestedBase}`);
    }
    return {
      ref: requestedBase,
      commit: resolved,
    };
  }

  const currentBranch = runGit(repo, ['branch', '--show-current'], false);
  const upstream = runGit(
    repo,
    ['rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{upstream}'],
    false
  );
  const remote = upstream && upstream.includes('/')
    ? upstream.split('/')[0]
    : splitLines(runGit(repo, ['remote'], false))[0];
  const remoteHead = remote
    ? runGit(
      repo,
      ['symbolic-ref', '--quiet', '--short', `refs/remotes/${remote}/HEAD`],
      false
    )
    : null;
  if (remoteHead) {
    const mergeBase = runGit(repo, ['merge-base', 'HEAD', remoteHead], false);
    if (mergeBase) {
      return {
        ref: remoteHead,
        commit: mergeBase,
      };
    }
  }

  const upstreamBranch = upstream && upstream.includes('/')
    ? upstream.slice(upstream.indexOf('/') + 1)
    : upstream;
  // A feature branch tracking itself is not a useful integration base because
  // it can hide the complete committed change set after branch tracking changes.
  if (upstream && upstreamBranch !== currentBranch) {
    const mergeBase = runGit(repo, ['merge-base', 'HEAD', upstream], false);
    if (mergeBase) {
      return {
        ref: upstream,
        commit: mergeBase,
      };
    }
  }

  const head = runGit(repo, ['rev-parse', 'HEAD']);
  return {
    ref: 'HEAD',
    commit: head,
  };
}

function classifyArtifact(relativePath) {
  const portablePath = relativePath.split(path.sep).join('/');
  const baseName = path.posix.basename(portablePath);
  if (resolvePreparedPagePath(portablePath)) {
    return baseName.endsWith('.json')
      ? 'express-page-preparation-json'
      : 'express-page-preparation-module';
  }
  if (portablePath.startsWith('extension1/sources/ui/')) {
    return 'out-of-scope-advanced-artifact';
  }
  if (baseName === 'metadata-rules-x.json') {
    return 'express-business-rules';
  }
  if (portablePath.includes('/metadataRules/') && baseName.endsWith('.js')) {
    return 'express-advanced-expression';
  }
  if (baseName === 'page-x.json') {
    return 'express-page-properties';
  }
  if (baseName === 'page-r-x.json') {
    return 'express-page-property-rules';
  }
  if (baseName === 'layout-x.json') {
    return 'express-rule-set-layout';
  }
  if (
    baseName === 'data-description-x.json'
    || baseName === 'data-description-x.js'
    || baseName === 'layout-x.js'
    || baseName === 'layout-x.html'
  ) {
    return 'express-supporting-metadata-read-only';
  }
  if (
    portablePath === 'extension1/sources/extension.json'
    || portablePath === 'extension1/sources/vb-extension.json'
  ) {
    return 'extension-metadata';
  }
  return isExtensionOwnedPath(portablePath)
    ? 'unknown-express-artifact'
    : 'outside-extension';
}

/**
 * Recognize the named page overlay pair emitted when VB Studio prepares a
 * delivered page for customization. Other UI source remains Advanced Mode.
 */
function resolvePreparedPagePath(relativePath) {
  const portablePath = String(relativePath || '').split(path.sep).join('/');
  const match = portablePath.match(
    /^extension1\/sources\/ui\/([^/]+)\/(applications\/.+\/pages\/([^/]+)-page)-x\.(json|js)$/
  );
  if (!match) return null;
  return {
    owner: match[1],
    basePath: match[2],
    page: match[3],
    extension: match[4],
  };
}

function isReleaseToolingPath(relativePath) {
  const portablePath = relativePath.split(path.sep).join('/');
  return [
    'package.json',
    'package-lock.json',
    'npm-shrinkwrap.json',
  ].includes(portablePath);
}

function fingerprintFile(filePath) {
  if (!fs.existsSync(filePath) || !fs.statSync(filePath).isFile()) {
    return null;
  }
  // SHA-256 binds the verification report to the exact reviewed file bytes.
  return crypto.createHash('sha256').update(fs.readFileSync(filePath)).digest('hex');
}

function validateArtifactPolicy(relativePath, artifactType, findings) {
  if (artifactType === 'release-tooling') {
    addFinding(
      findings,
      'info',
      'release-tooling-update',
      'Release-alignment tooling file was explicitly allowed for this validation run.',
      relativePath
    );
    return;
  }
  if (artifactType.endsWith('-read-only')) {
    addFinding(
      findings,
      'blocker',
      'read-preserve-artifact-change',
      'This Express artifact is read-and-preserve and is not approved for writes.',
      relativePath
    );
  } else if (artifactType === 'out-of-scope-advanced-artifact') {
    addFinding(
      findings,
      'blocker',
      'advanced-mode-artifact-change',
      'This file belongs to Advanced Mode-only source outside the skill write scope.',
      relativePath
    );
  } else if (artifactType === 'unknown-express-artifact') {
    addFinding(
      findings,
      'blocker',
      'unknown-express-artifact-change',
      'The changed Extension artifact has no approved Express Mode write contract.',
      relativePath
    );
  } else if (artifactType === 'unproven-advanced-expression') {
    addFinding(
      findings,
      'blocker',
      'advanced-expression-ownership',
      'The JavaScript file is not imported by a sibling Extension Business Rules overlay.',
      relativePath
    );
  }
}

function collectChangedFiles(repo, baseCommit) {
  const committed = splitLines(
    runGit(repo, ['diff', '--name-only', '--diff-filter=ACMRD', `${baseCommit}...HEAD`], false)
  );
  const working = splitLines(
    runGit(repo, ['diff', '--name-only', '--diff-filter=ACMRD'], false)
  );
  const staged = splitLines(
    runGit(repo, ['diff', '--cached', '--name-only', '--diff-filter=ACMRD'], false)
  );
  const untracked = splitLines(
    runGit(repo, ['ls-files', '--others', '--exclude-standard'], false)
  );

  return Array.from(new Set([...committed, ...working, ...staged, ...untracked])).sort();
}

function isExtensionOwnedPath(relativePath) {
  return relativePath === 'extension1/sources/extension.json'
    || relativePath === 'extension1/sources/vb-extension.json'
    || relativePath.startsWith('extension1/sources/dynamicLayouts/')
    || relativePath.startsWith('extension1/sources/ui/');
}

function looksLikeFaArtifact(relativePath) {
  const baseName = path.posix.basename(relativePath);
  const protectedNames = new Set([
    'metadata-rules.json',
    'layout.json',
    'data-description.json',
    'page.json',
    'page-r.json',
  ]);

  return relativePath.startsWith('extension1/sources/dynamicLayouts/')
    && protectedNames.has(baseName);
}

function validateText(relativePath, content, findings) {
  if (/^(<{7}|={7}|>{7})/m.test(content)) {
    addFinding(
      findings,
      'blocker',
      'merge-conflict-marker',
      'The file contains a merge conflict marker.',
      relativePath
    );
  }

  // Build the patterns from portable segments so this script contains no
  // packaged machine path while still detecting common absolute user paths.
  const userDirectory = 'Users';
  const homeDirectory = 'home';
  const localPathPatterns = [
    new RegExp(`/${userDirectory}/[^/\\s]+`, 'i'),
    new RegExp(`/${homeDirectory}/[^/\\s]+`, 'i'),
    new RegExp(`[A-Za-z]:\\\\${userDirectory}\\\\[^\\\\\\s]+`, 'i'),
  ];
  if (localPathPatterns.some((pattern) => pattern.test(content))) {
    addFinding(
      findings,
      'blocker',
      'hardcoded-local-path',
      'The file contains a machine-specific absolute path.',
      relativePath
    );
  }

  const likelySecret = /["']?(password|passwd|secret|access[_-]?token|api[_-]?key)["']?\s*[:=]\s*["'][^"'<>$\s][^"']*["']/i;
  if (likelySecret.test(content)) {
    addFinding(
      findings,
      'blocker',
      'likely-secret',
      'The file contains a value that resembles a credential or secret.',
      relativePath
    );
  }
}

function validateJavaScript(repo, relativePath, content, findings) {
  const absolutePath = path.join(repo, relativePath);
  const result = spawnSync(process.execPath, ['--check', absolutePath], {
    cwd: repo,
    encoding: 'utf8',
  });
  if (result.status !== 0) {
    addFinding(
      findings,
      'blocker',
      'javascript-syntax',
      String(result.stderr || result.stdout || 'JavaScript syntax validation failed.').trim(),
      relativePath
    );
  }

  if (relativePath.includes('/metadataRules/') && content.includes('runCondition')) {
    const requiredNames = [
      '$componentContext',
      '$fields',
      '$modules',
      '$user',
      '$objectContext',
    ];
    const destructuringMatch = content.match(/const\s*\{([^}]+)\}\s*=\s*context\s*;/);
    const destructuring = destructuringMatch ? destructuringMatch[1] : '';
    // Validation modules use the designer's complete, stable context contract
    // even when one particular expression currently reads only a subset.
    const missingNames = requiredNames.filter((name) => !destructuring.includes(name));
    if (missingNames.length > 0) {
      addFinding(
        findings,
        'blocker',
        'advanced-expression-context',
        `Validation Advanced Expression is missing context values: ${missingNames.join(', ')}.`,
        relativePath
      );
    }
  }

  const unsafePatterns = [
    { pattern: /Array\.isArray\s*\(\s*\$fields\b/, label: 'Array.isArray on a field object' },
    { pattern: /Number\s*\(\s*\$fields\b/, label: 'Number conversion on a field object' },
    { pattern: /new\s+Date\s*\(\s*\$fields\b/, label: 'Date construction from a field object' },
    { pattern: /\$fields(?:\.[A-Za-z_$][\w$-]*)+\.length\b/, label: 'length read from a field object' },
  ];
  for (const unsafe of unsafePatterns) {
    if (unsafe.pattern.test(content)) {
      addFinding(
        findings,
        'blocker',
        'field-accessor-required',
        `${unsafe.label}; read the value through a verified accessor first.`,
        relativePath
      );
    }
  }

  const numericAccessorPattern = /(\$fields(?:\.[A-Za-z_$][\w$-]*|\[['"][^'"]+['"]\])+?)\.\$numberValue\s*\(\s*\)/g;
  const warnedNumericPaths = new Set();
  let numericMatch = numericAccessorPattern.exec(content);
  while (numericMatch) {
    const fieldPath = numericMatch[1];
    const rawValuePattern = new RegExp(
      `${escapeRegExp(fieldPath)}\\.\\$(?:value|initialValue)\\s*\\(\\s*\\)`
    );
    if (!rawValuePattern.test(content) && !warnedNumericPaths.has(fieldPath)) {
      // This remains a warning because some target-verified designer patterns
      // intentionally use numeric accessors directly.
      addFinding(
        findings,
        'warning',
        'numeric-accessor-null-contract',
        `${fieldPath} uses .$numberValue() without a raw value read for null handling.`,
        relativePath
      );
      warnedNumericPaths.add(fieldPath);
    }
    numericMatch = numericAccessorPattern.exec(content);
  }
}

function validateMetadataRules(repo, relativePath, parsed, findings, validationContext) {
  const rules = parsed && Array.isArray(parsed.addMetadataRules) ? parsed.addMetadataRules : [];
  if (rules.length === 0) {
    addFinding(
      findings,
      'blocker',
      'empty-business-rules-overlay',
      'The Business Rules overlay must contain at least one Extension rule.',
      relativePath
    );
  }
  const businessRuleEvidence = resolveBusinessRulesProof(
    validationContext,
    repo,
    relativePath,
    'metadata-rules.json'
  ) || resolveBusinessRulesProof(
    validationContext,
    repo,
    relativePath,
    'data-description.json'
  );
  if (!businessRuleEvidence) {
    addFinding(
      findings,
      'blocker',
      'business-rules-not-proven',
      'No unambiguous Oracle Business Rules or data-resource contract proves this page capability.',
      relativePath
    );
  }
  const identifiers = new Set();
  // Referenced-field blocks vary slightly by release, so accept either a flat
  // array or named array groups while rejecting values that cannot be resolved.
  const validateReferencedFields = (value, ruleId, location) => {
    if (value === undefined || value === null) return;
    const groups = Array.isArray(value) ? { fields: value } : value;
    if (!groups || typeof groups !== 'object' || Array.isArray(groups)) {
      addFinding(
        findings,
        'blocker',
        'referenced-fields-shape',
        `Rule ${ruleId} ${location} referencedFields must be an array or an object of arrays.`,
        relativePath
      );
      return;
    }
    for (const [groupName, fields] of Object.entries(groups)) {
      if (!Array.isArray(fields)) {
        addFinding(
          findings,
          'blocker',
          'referenced-fields-shape',
          `Rule ${ruleId} ${location} referencedFields.${groupName} must be an array.`,
          relativePath
        );
        continue;
      }
      const seenFields = new Set();
      for (const field of fields) {
        if (typeof field !== 'string' || !field.trim()) {
          addFinding(
            findings,
            'blocker',
            'referenced-field-name',
            `Rule ${ruleId} ${location} contains an empty or non-string referenced field.`,
            relativePath
          );
          continue;
        }
        if (seenFields.has(field)) {
          addFinding(
            findings,
            'blocker',
            'duplicate-referenced-field',
            `Rule ${ruleId} ${location} repeats referenced field ${field}.`,
            relativePath
          );
        }
        seenFields.add(field);
      }
    }
  };
  // Walk the rule because referencedFields can be owned by conditions,
  // messages, or field/property overlays depending on the generated schema.
  const validateAllReferencedFields = (value, ruleId, location = 'rule') => {
    if (Array.isArray(value)) {
      value.forEach((item, index) => validateAllReferencedFields(item, ruleId, `${location}[${index}]`));
      return;
    }
    if (!value || typeof value !== 'object') return;
    for (const [key, child] of Object.entries(value)) {
      // Child rules are validated independently by visitRule below.
      if (key === 'children' || key === 'rules' || key === 'cases') continue;
      if (key === 'referencedFields') validateReferencedFields(child, ruleId, location);
      else validateAllReferencedFields(child, ruleId, `${location}.${key}`);
    }
  };
  const validateTargetFields = (value, ruleId) => {
    if (value === undefined || value === null) return;
    if (!Array.isArray(value) || value.some((field) => typeof field !== 'string' || !field.trim())) {
      addFinding(
        findings,
        'blocker',
        'validation-message-target-fields',
        `Rule ${ruleId} validation message targetFields must be an array of non-empty field names.`,
        relativePath
      );
      return;
    }
    if (new Set(value).size !== value.length) {
      addFinding(
        findings,
        'blocker',
        'duplicate-message-target-field',
        `Rule ${ruleId} validation message targetFields must not contain duplicates.`,
        relativePath
      );
    }
  };
  // Nested rules can use several child-property names across supported releases.
  const visitRule = (rule, parentType = null) => {
    if (!rule || !rule.id) {
      addFinding(
        findings,
        'blocker',
        'missing-rule-id',
        'Every added metadata rule must have an identifier.',
        relativePath
      );
      return;
    }
    if (identifiers.has(rule.id)) {
      addFinding(
        findings,
        'blocker',
        'duplicate-rule-id',
        `Duplicate rule identifier: ${rule.id}.`,
        relativePath
      );
    }
    identifiers.add(rule.id);
    const normalizedType = String(rule.type || rule.ruleType || '').toLowerCase();
    const normalizedStatus = String(rule.status || '').toLowerCase();
    if (normalizedStatus && normalizedStatus !== 'active' && normalizedStatus !== 'inactive') {
      addFinding(
        findings,
        'blocker',
        'invalid-rule-status',
        `Rule ${rule.id} uses unsupported status ${rule.status}.`,
        relativePath
      );
    }
    const children = ['children', 'rules', 'cases']
      .flatMap((key) => (Array.isArray(rule[key]) ? rule[key] : []));
    if ((normalizedType === 'ifelse' || normalizedType === 'if/else') && children.length < 2) {
      addFinding(
        findings,
        'blocker',
        'if-else-branches',
        `If/Else rule ${rule.id} must contain at least two child branches.`,
        relativePath
      );
    }
    if (
      (normalizedType === 'ifelse' || normalizedType === 'if/else')
      && children.length >= 2
      && !children.some((child) => child?.otherwise === true || child?.isDefault === true)
    ) {
      addFinding(
        findings,
        'blocker',
        'if-else-otherwise',
        `If/Else rule ${rule.id} must contain an otherwise branch.`,
        relativePath
      );
    }
    if (normalizedType === 'switch') {
      const switchParameter = rule.switchParameter || rule.switchExpression || rule.parameter;
      if (!switchParameter) {
        addFinding(
          findings,
          'blocker',
          'switch-parameter',
          `Switch rule ${rule.id} must define one switch parameter.`,
          relativePath
        );
      }
      const seenCases = new Set();
      for (const child of children) {
        const values = Array.isArray(child.caseValues)
          ? child.caseValues
          : Object.prototype.hasOwnProperty.call(child, 'caseValue')
            ? [child.caseValue]
            : [];
        for (const value of values) {
          const key = JSON.stringify(value);
          if (seenCases.has(key)) {
            addFinding(
              findings,
              'blocker',
              'duplicate-switch-case',
              `Switch rule ${rule.id} contains duplicate case value ${key}.`,
              relativePath
            );
          }
          seenCases.add(key);
        }
      }
      if (!children.some((child) => child?.otherwise === true || child?.isDefault === true)) {
        addFinding(
          findings,
          'blocker',
          'switch-otherwise',
          `Switch rule ${rule.id} must contain an otherwise branch.`,
          relativePath
        );
      }
    }
    const collectOverrideNames = (value, names = new Set()) => {
      if (Array.isArray(value)) {
        value.forEach((item) => collectOverrideNames(item, names));
        return names;
      }
      if (!value || typeof value !== 'object') return;
      for (const [key, child] of Object.entries(value)) {
        if (/^(hidden|required|readOnly|value)$/i.test(key)) names.add(key.toLowerCase());
        collectOverrideNames(child, names);
      }
      return names;
    };
    const overrideNames = collectOverrideNames(rule.properties || rule.overrides) || new Set();
    if (
      /collection|table/.test(normalizedType)
      && Array.from(overrideNames).some((name) => name !== 'hidden')
    ) {
      addFinding(
        findings,
        'blocker',
        'collection-rule-property',
        `Collection rule ${rule.id} may override only the Hidden property.`,
        relativePath
      );
    }
    const regionOverrides = rule.regions || rule.regionProperties;
    const regionNames = collectOverrideNames(regionOverrides) || new Set();
    if (
      regionOverrides
      && (regionNames.has('readonly') || regionNames.has('value'))
    ) {
      addFinding(
        findings,
        'blocker',
        'region-rule-property',
        `Region rule ${rule.id} cannot override Read Only or Value.`,
        relativePath
      );
    }
    const directMessages = Array.isArray(rule.messages) ? rule.messages : [];
    const addedMessages = rule.addMessages && Array.isArray(rule.addMessages.messages)
      ? rule.addMessages.messages
      : [];
    if (rule.addMessages && !Array.isArray(rule.addMessages.messages)) {
      addFinding(
        findings,
        'blocker',
        'validation-message-shape',
        `Rule ${rule.id} addMessages.messages must be an array.`,
        relativePath
      );
    }
    const messages = [...directMessages, ...addedMessages];
    for (const message of messages) {
      const severity = String(message?.severity || '').toLowerCase();
      if (severity && severity !== 'error' && severity !== 'warning') {
        addFinding(
          findings,
          'blocker',
          'validation-message-severity',
          `Rule ${rule.id} uses unsupported message severity ${message.severity}.`,
          relativePath
        );
      }
      if (!message?.summary || !message?.detail) {
        addFinding(
          findings,
          'blocker',
          'validation-message-text',
          `Rule ${rule.id} validation messages require Summary and Detail text.`,
          relativePath
        );
      }
      validateTargetFields(message?.targetFields, rule.id);
    }
    validateAllReferencedFields(rule, rule.id);
    for (const child of children) visitRule(child, normalizedType || parentType);
  };
  for (const rule of rules) visitRule(rule);

  const modules = parsed.imports && parsed.imports.modules
    ? parsed.imports.modules
    : {};
  for (const [moduleName, moduleDefinition] of Object.entries(modules)) {
    const modulePath = typeof moduleDefinition === 'string'
      ? moduleDefinition
      : moduleDefinition && moduleDefinition.path;
    if (!modulePath) {
      addFinding(
        findings,
        'blocker',
        'missing-module-path',
        `Imported module ${moduleName} has no path.`,
        relativePath
      );
      continue;
    }

    const baseDirectory = path.dirname(path.join(repo, relativePath));
    const resolvedPath = path.resolve(baseDirectory, modulePath.endsWith('.js') ? modulePath : `${modulePath}.js`);
    if (!resolvedPath.startsWith(`${repo}${path.sep}`) || !fs.existsSync(resolvedPath)) {
      addFinding(
        findings,
        'blocker',
        'unresolved-module-import',
        `Imported module ${moduleName} does not resolve to an existing JavaScript file.`,
        relativePath
      );
    }
  }

  const serialized = JSON.stringify(parsed);
  const referencedModules = new Set();
  // Support both common module reference notations in generated expressions.
  const modulePattern = /\$modules(?:\.([A-Za-z_$][\w$]*)|\[['"]([^'"]+)['"]\])/g;
  let match = modulePattern.exec(serialized);
  while (match) {
    referencedModules.add(match[1] || match[2]);
    match = modulePattern.exec(serialized);
  }

  for (const moduleName of referencedModules) {
    if (!Object.prototype.hasOwnProperty.call(modules, moduleName)) {
      addFinding(
        findings,
        'blocker',
        'missing-module-import',
        `Expression references $modules.${moduleName}, but no matching import exists.`,
        relativePath
      );
    }
  }
}

function resolveArtifactCounterparts(repo, relativePath, counterpartName) {
  const portablePath = relativePath.split(path.sep).join('/');
  const segments = portablePath.split('/');
  const dynamicLayoutsIndex = segments.indexOf('dynamicLayouts');
  if (dynamicLayoutsIndex < 0) {
    return [];
  }

  const pageName = segments[dynamicLayoutsIndex + 2];
  const dynamicLayoutsRoot = path.join(
    repo,
    ...segments.slice(0, dynamicLayoutsIndex + 1)
  );
  if (!pageName || !fs.existsSync(dynamicLayoutsRoot)) {
    return [];
  }

  // Prefer the conventional FA self layer, then inspect other delivered owners.
  const owners = [
    'self',
    ...fs.readdirSync(dynamicLayoutsRoot).filter((owner) => owner !== 'self').sort(),
  ];
  const matches = [];
  for (const owner of owners) {
    const candidate = path.join(dynamicLayoutsRoot, owner, pageName, counterpartName);
    if (fs.existsSync(candidate) && fs.statSync(candidate).isFile()) {
      matches.push(candidate);
    }
  }
  // A self-layer artifact is the canonical Oracle contract when present.
  const selfMatch = matches.find((candidate) => candidate.includes(`${path.sep}dynamicLayouts${path.sep}self${path.sep}`));
  return selfMatch ? [selfMatch] : matches;
}

function resolveArtifactCounterpart(repo, relativePath, counterpartName) {
  const matches = resolveArtifactCounterparts(repo, relativePath, counterpartName);
  return matches.length === 1 ? matches[0] : null;
}

function readEvidenceManifest(manifestPath) {
  if (!manifestPath) return null;
  const resolvedPath = path.resolve(manifestPath);
  const parsed = JSON.parse(fs.readFileSync(resolvedPath, 'utf8'));
  if (!parsed || Array.isArray(parsed) || typeof parsed !== 'object') {
    throw new Error(`Evidence manifest is not a JSON object: ${resolvedPath}`);
  }
  return parsed;
}

function resolveEvidenceManifestCounterpart(evidenceManifest, relativePath, counterpartName) {
  if (!evidenceManifest || !Array.isArray(evidenceManifest.evidence)) return null;
  const portablePath = relativePath.split(path.sep).join('/');
  const segments = portablePath.split('/');
  const dynamicLayoutsIndex = segments.indexOf('dynamicLayouts');
  if (dynamicLayoutsIndex < 0) return null;
  const pageName = segments[dynamicLayoutsIndex + 2];
  if (!pageName) return null;
  const suffix = `/dynamicLayouts/`;
  const matches = evidenceManifest.evidence.filter((item) => {
    const moduleId = String(item.moduleId || '');
    // Runtime evidence module IDs include the deployed owner, which can differ from the extension overlay owner.
    return moduleId.includes(suffix)
      && moduleId.endsWith(`/${pageName}/${counterpartName}`)
      && item.sourceLayer === 'oracle-delivered';
  });
  return matches.length === 1 ? matches[0] : null;
}

/** Resolve the exact Oracle base page that authorizes a minimal page-preparation overlay. */
function resolvePreparedPageEvidence(evidenceManifest, relativePath) {
  const prepared = resolvePreparedPagePath(relativePath);
  if (!prepared || !evidenceManifest || !Array.isArray(evidenceManifest.evidence)) return null;
  const moduleId = prepared.extension === 'json'
    ? `text!vx/${prepared.owner}/ui/self/${prepared.basePath}.json`
    : `vx/${prepared.owner}/ui/self/${prepared.basePath}`;
  const matches = evidenceManifest.evidence.filter((item) => (
    item.moduleId === moduleId
    && item.sourceLayer === 'oracle-delivered'
    && item.role === 'page-source'
  ));
  return matches.length === 1 ? matches[0] : null;
}

/** Validate that a prepared page contains only the standard Express Mode skeleton. */
function validatePreparedPage(
  relativePath,
  content,
  parsed,
  findings,
  validationContext
) {
  if (!resolvePreparedPageEvidence(validationContext.evidenceManifest, relativePath)) {
    addFinding(
      findings,
      'blocker',
      'page-preparation-counterpart',
      'The standard page overlay requires exact deployed Oracle page evidence.',
      relativePath
    );
  }

  const prepared = resolvePreparedPagePath(relativePath);
  if (prepared.extension === 'json') {
    const expectedKeys = [
      'description',
      'eventListeners',
      'events',
      'imports',
      'options',
      'types',
      'variables',
    ];
    const actualKeys = Object.keys(parsed || {}).sort();
    const emptyObjectKeys = ['variables', 'types', 'eventListeners', 'events', 'imports'];
    const hasOnlyEmptyObjects = emptyObjectKeys.every((key) => (
      parsed?.[key]
      && !Array.isArray(parsed[key])
      && typeof parsed[key] === 'object'
      && Object.keys(parsed[key]).length === 0
    ));
    if (
      JSON.stringify(actualKeys) !== JSON.stringify(expectedKeys.sort())
      || parsed.description !== ''
      || !hasOnlyEmptyObjects
      || JSON.stringify(parsed.options) !== JSON.stringify({ constantsRules: 'on' })
    ) {
      addFinding(
        findings,
        'blocker',
        'page-preparation-shape',
        'The page JSON exceeds the standard VB Studio preparation skeleton.',
        relativePath
      );
    }
    return;
  }

  // Comments and formatting may vary, but executable content must remain the empty page module.
  const compactModule = content
    .replace(/\/\*[\s\S]*?\*\//g, '')
    .replace(/\/\/[^\n\r]*/g, '')
    .replace(/\s+/g, '');
  const allowedModules = new Set([
    "define([],()=>{'usestrict';classPageModule{}returnPageModule;});",
    'define([],()=>{"usestrict";classPageModule{}returnPageModule;});',
  ]);
  if (!allowedModules.has(compactModule)) {
    addFinding(
      findings,
      'blocker',
      'page-preparation-shape',
      'The page JavaScript exceeds the standard empty VB Studio page module.',
      relativePath
    );
  }
}

function resolveBusinessRulesProof(validationContext, repo, relativePath, counterpartName) {
  return resolveArtifactCounterpart(repo, relativePath, counterpartName)
    || resolveEvidenceManifestCounterpart(validationContext.evidenceManifest, relativePath, counterpartName);
}

function isImportedExtensionExpression(repo, relativePath) {
  const portable = relativePath.split(path.sep).join('/');
  const markerIndex = portable.indexOf('/metadataRules/');
  if (markerIndex < 0) return false;
  const pageRoot = portable.slice(0, markerIndex);
  const rulesPath = path.join(repo, pageRoot, 'metadata-rules-x.json');
  if (!fs.existsSync(rulesPath)) return false;
  let rules;
  try {
    rules = JSON.parse(fs.readFileSync(rulesPath, 'utf8'));
  } catch (error) {
    return false;
  }
  const modules = rules?.imports?.modules;
  if (!modules || Array.isArray(modules) || typeof modules !== 'object') return false;
  const target = path.resolve(repo, relativePath);
  return Object.values(modules).some((definition) => {
    const modulePath = typeof definition === 'string' ? definition : definition?.path;
    if (!modulePath) return false;
    const candidate = path.resolve(
      path.dirname(rulesPath),
      modulePath.endsWith('.js') ? modulePath : `${modulePath}.js`
    );
    // Prevent an Extension import from granting write access outside its own page root.
    return candidate === target && candidate.startsWith(`${path.join(repo, pageRoot)}${path.sep}`);
  });
}

function resolvePagePropertiesCounterpart(repo, relativePath) {
  if (path.posix.basename(relativePath) !== 'page-x.json') return null;
  return resolveArtifactCounterpart(repo, relativePath, 'page.json');
}

function hasRecognizedRoot(parsed, keys) {
  return parsed && !Array.isArray(parsed) && typeof parsed === 'object'
    && keys.some((key) => Object.prototype.hasOwnProperty.call(parsed, key));
}

function findObjectKey(value, expectedKey) {
  if (Array.isArray(value)) return value.some((item) => findObjectKey(item, expectedKey));
  if (!value || typeof value !== 'object') return false;
  if (Object.prototype.hasOwnProperty.call(value, expectedKey)) return true;
  return Object.values(value).some((child) => findObjectKey(child, expectedKey));
}

function configuredValueType(value) {
  if (Array.isArray(value)) return 'array';
  if (value === null) return 'null';
  return typeof value;
}

function validatePropertyValue(propertyName, definition, value, relativePath, findings) {
  const expectedType = typeof definition?.type === 'string'
    ? definition.type.toLowerCase()
    : null;
  const actualType = configuredValueType(value);
  const compatibleType = (
    !expectedType
    || value == null
    || expectedType === actualType
    || (expectedType === 'integer' && actualType === 'number' && Number.isInteger(value))
  );
  if (!compatibleType) {
    addFinding(
      findings,
      'blocker',
      'page-property-type',
      `Page Property ${propertyName} expects ${expectedType}, but the overlay supplies ${actualType}.`,
      relativePath
    );
  }
  const allowedValues = Array.isArray(definition?.enum)
    ? definition.enum
    : definition?.allowedValues;
  if (Array.isArray(allowedValues) && value != null && !allowedValues.includes(value)) {
    addFinding(
      findings,
      'blocker',
      'page-property-value',
      `Page Property ${propertyName} is not one of the Oracle-defined allowed values.`,
      relativePath
    );
  }
}

function validatePagePropertyRules(repo, relativePath, parsed, findings) {
  if (!hasRecognizedRoot(parsed, ['rules', 'addRules', 'addPagePropertyRules'])) {
    addFinding(
      findings,
      'blocker',
      'page-property-rules-shape',
      'Page Property rules must use a recognized Extension overlay root shape.',
      relativePath
    );
    return;
  }
  const counterpart = resolveArtifactCounterpart(repo, relativePath, 'page-r.json');
  if (!counterpart) {
    addFinding(
      findings,
      'blocker',
      'page-property-rules-counterpart',
      'No Oracle page-r.json counterpart proves this Page Property rules overlay.',
      relativePath
    );
    return;
  }
  let faRules;
  try {
    faRules = JSON.parse(fs.readFileSync(counterpart, 'utf8'));
  } catch (error) {
    addFinding(
      findings,
      'blocker',
      'page-property-rules-counterpart',
      `Unable to read the Oracle Page Property contract: ${error.message}`,
      relativePath
    );
    return;
  }
  const rules = ['rules', 'addRules', 'addPagePropertyRules']
    .flatMap((key) => (Array.isArray(parsed[key]) ? parsed[key] : []));
  if (rules.length === 0) {
    addFinding(
      findings,
      'blocker',
      'empty-page-property-rules',
      'The Page Property rules overlay must contain at least one Extension rule.',
      relativePath
    );
  }
  const definitions = faRules?.properties;
  if (!definitions || Array.isArray(definitions) || typeof definitions !== 'object') {
    addFinding(
      findings,
      'blocker',
      'page-property-rules-counterpart',
      'The Oracle Page Property contract does not expose a properties definition.',
      relativePath
    );
    return;
  }
  const identifiers = new Set();
  for (const rule of rules) {
    if (!rule || typeof rule !== 'object' || !rule.id) {
      addFinding(findings, 'blocker', 'missing-rule-id', 'Every Page Property rule needs an id.', relativePath);
      continue;
    }
    if (identifiers.has(rule.id)) {
      addFinding(findings, 'blocker', 'duplicate-rule-id', `Duplicate rule identifier: ${rule.id}.`, relativePath);
    }
    identifiers.add(rule.id);
    const normalizedStatus = String(rule.status || '').toLowerCase();
    if (normalizedStatus && normalizedStatus !== 'active' && normalizedStatus !== 'inactive') {
      addFinding(
        findings,
        'blocker',
        'invalid-rule-status',
        `Page Property rule ${rule.id} uses unsupported status ${rule.status}.`,
        relativePath
      );
    }
    const properties = rule.properties || rule.values || {};
    if (!properties || Array.isArray(properties) || typeof properties !== 'object') {
      addFinding(findings, 'blocker', 'page-property-rule-values', `Rule ${rule.id} must define a property-value object.`, relativePath);
      continue;
    }
    if (Object.keys(properties).length === 0) {
      addFinding(
        findings,
        'blocker',
        'page-property-rule-values',
        `Rule ${rule.id} must configure at least one Page Property.`,
        relativePath
      );
    }
    for (const [propertyName, configuredValue] of Object.entries(properties)) {
      const definition = definitions[propertyName];
      if (!definition || typeof definition !== 'object') {
        addFinding(
          findings,
          'blocker',
          'page-property-not-extendable',
          `Page Property ${propertyName} is not defined by the Oracle page-r.json contract.`,
          relativePath
        );
        continue;
      }
      if (definition.extendable !== true) {
        addFinding(
          findings,
          'blocker',
          'page-property-not-extendable',
          `Page Property ${propertyName} is not marked extendable by the Oracle contract.`,
          relativePath
        );
      }
      validatePropertyValue(propertyName, definition, configuredValue, relativePath, findings);
    }
  }
}

function validateRuleSetLayout(repo, relativePath, parsed, findings) {
  if (!hasRecognizedRoot(parsed, ['layouts', 'addLayouts', 'layoutTypes'])) {
    addFinding(
      findings,
      'blocker',
      'rule-set-layout-shape',
      'Rule-set layout changes must use a recognized Extension overlay root shape.',
      relativePath
    );
    return;
  }
  const counterpart = resolveArtifactCounterpart(repo, relativePath, 'layout.json');
  if (!counterpart) {
    addFinding(
      findings,
      'blocker',
      'rule-set-layout-counterpart',
      'No Oracle layout.json counterpart proves this rule-set overlay.',
      relativePath
    );
    return;
  }
  let baseLayout;
  try {
    baseLayout = JSON.parse(fs.readFileSync(counterpart, 'utf8'));
  } catch (error) {
    addFinding(findings, 'blocker', 'rule-set-layout-counterpart', `Unable to read Oracle layout.json: ${error.message}`, relativePath);
    return;
  }
  const overlayLayouts = parsed.layouts || parsed.addLayouts || {};
  if (Array.isArray(overlayLayouts) || typeof overlayLayouts !== 'object') {
    addFinding(findings, 'blocker', 'rule-set-layout-shape', 'Layout definitions must be a JSON object.', relativePath);
    return;
  }
  if (Object.keys(overlayLayouts).length === 0) {
    addFinding(
      findings,
      'blocker',
      'empty-rule-set-layout',
      'The rule-set overlay must contain at least one Extension layout or rule.',
      relativePath
    );
  }
  const availableRules = new Set([
    ...Object.keys(baseLayout.layouts || {}),
    ...Object.keys(overlayLayouts),
  ]);
  const availableFields = new Set();
  const collectAvailableFields = (value) => {
    if (Array.isArray(value)) return value.forEach(collectAvailableFields);
    if (!value || typeof value !== 'object') return;
    for (const [key, child] of Object.entries(value)) {
      if ((key === 'fields' || key === 'properties') && child && typeof child === 'object') {
        Object.keys(child).forEach((fieldName) => availableFields.add(fieldName));
      }
      collectAvailableFields(child);
    }
  };
  collectAvailableFields(baseLayout);
  const dataDescriptionPath = resolveArtifactCounterpart(
    repo,
    relativePath,
    'data-description.json'
  );
  if (dataDescriptionPath) {
    try {
      collectAvailableFields(JSON.parse(fs.readFileSync(dataDescriptionPath, 'utf8')));
    } catch (error) {
      addFinding(
        findings,
        'blocker',
        'layout-field-contract',
        `Unable to read the data-resource field contract: ${error.message}`,
        relativePath
      );
    }
  }
  const hasSectionTemplate = findObjectKey(baseLayout, 'sectionTemplate')
    || findObjectKey(baseLayout, 'sectionTemplates')
    || findObjectKey(baseLayout, 'newSectionTemplate');
  const addsSections = findObjectKey(parsed, 'addSections')
    || findObjectKey(parsed, 'sections');
  if (addsSections && !hasSectionTemplate) {
    addFinding(
      findings,
      'blocker',
      'container-section-template',
      'The overlay adds container sections without a dependency-provided section template.',
      relativePath
    );
  }
  for (const [layoutName, definition] of Object.entries(overlayLayouts)) {
    if (!definition || typeof definition !== 'object') continue;
    const rules = Array.isArray(definition.rules) ? definition.rules : [];
    if (new Set(rules).size !== rules.length) {
      addFinding(findings, 'blocker', 'duplicate-rule-set-rule', `Layout ${layoutName} repeats a rule reference.`, relativePath);
    }
    const variants = definition.layouts && typeof definition.layouts === 'object'
      ? definition.layouts
      : {};
    for (const [variantName, variant] of Object.entries(variants)) {
      const usedIn = Array.isArray(variant?.usedIn) ? variant.usedIn : [];
      for (const ruleName of usedIn) {
        if (!availableRules.has(ruleName)) {
          addFinding(
            findings,
            'blocker',
            'rule-set-rule-not-found',
            `Variant ${layoutName}/${variantName} references unknown rule ${ruleName}.`,
            relativePath
          );
        }
      }
      const fields = variant?.layout?.displayProperties;
      if (Array.isArray(fields) && new Set(fields).size !== fields.length) {
        addFinding(findings, 'blocker', 'duplicate-layout-field', `Variant ${layoutName}/${variantName} repeats a displayed field.`, relativePath);
      }
      if (Array.isArray(fields)) {
        for (const fieldName of fields) {
          if (!availableFields.has(fieldName)) {
            addFinding(
              findings,
              'blocker',
              'layout-field-membership',
              `Layout field ${fieldName} is not proven by the component data resource.`,
              relativePath
            );
          }
        }
      }
    }
  }
}

function validatePageProperties(repo, relativePath, parsed, findings) {
  if (!parsed || Array.isArray(parsed) || typeof parsed !== 'object') {
    addFinding(
      findings,
      'blocker',
      'page-properties-shape',
      'The Page Properties overlay must be a JSON object.',
      relativePath
    );
    return;
  }

  const counterpart = resolvePagePropertiesCounterpart(repo, relativePath);
  if (!counterpart) {
    addFinding(
      findings,
      'blocker',
      'page-properties-fa-counterpart',
      'No FA page.json counterpart was found for this Page Properties overlay.',
      relativePath
    );
    return;
  }

  try {
    const faProperties = JSON.parse(fs.readFileSync(counterpart, 'utf8'));
    if (!faProperties || Array.isArray(faProperties) || typeof faProperties !== 'object') {
      throw new Error('FA page properties are not a JSON object.');
    }
    const extensionDefinitions = parsed.properties;
    const faDefinitions = faProperties.properties;
    if (
      !extensionDefinitions
      || Array.isArray(extensionDefinitions)
      || typeof extensionDefinitions !== 'object'
      || Object.keys(extensionDefinitions).length === 0
    ) {
      addFinding(
        findings,
        'blocker',
        'empty-page-properties-overlay',
        'The Page Properties overlay must contain at least one configured property.',
        relativePath
      );
      return;
    }
    if (!faDefinitions || Array.isArray(faDefinitions) || typeof faDefinitions !== 'object') {
      addFinding(
        findings,
        'blocker',
        'page-properties-fa-counterpart',
        'The Oracle Page Properties counterpart does not define configurable properties.',
        relativePath
      );
      return;
    }
    if (
      extensionDefinitions
      && !Array.isArray(extensionDefinitions)
      && typeof extensionDefinitions === 'object'
      && faDefinitions
      && !Array.isArray(faDefinitions)
      && typeof faDefinitions === 'object'
    ) {
      for (const [propertyName, extensionDefinition] of Object.entries(extensionDefinitions)) {
        const faDefinition = faDefinitions[propertyName];
        if (!faDefinition || typeof faDefinition !== 'object') {
          addFinding(
            findings,
            'blocker',
            'page-property-not-defined',
            `Page Property ${propertyName} is not defined by the FA counterpart.`,
            relativePath
          );
          continue;
        }
        if (faDefinition.extendable === false) {
          addFinding(
            findings,
            'blocker',
            'page-property-not-extendable',
            `Page Property ${propertyName} is not extendable in the Oracle contract.`,
            relativePath
          );
        }

        const configuredValue = (
          extensionDefinition
          && typeof extensionDefinition === 'object'
          && Object.prototype.hasOwnProperty.call(extensionDefinition, 'value')
        )
          ? extensionDefinition.value
          : extensionDefinition;
        validatePropertyValue(propertyName, faDefinition, configuredValue, relativePath, findings);
      }
    }
  } catch (error) {
    addFinding(
      findings,
      'blocker',
      'page-properties-fa-counterpart',
      `Unable to validate the FA Page Properties counterpart: ${error.message}`,
      relativePath
    );
  }
}

function validateJson(repo, relativePath, content, findings, validationContext = {}) {
  let parsed;
  try {
    parsed = JSON.parse(content);
  } catch (error) {
    addFinding(
      findings,
      'blocker',
      'json-syntax',
      `Invalid JSON: ${error.message}`,
      relativePath
    );
    return;
  }

  if (path.posix.basename(relativePath) === 'metadata-rules-x.json') {
    validateMetadataRules(repo, relativePath, parsed, findings, validationContext);
  }
  if (resolvePreparedPagePath(relativePath)?.extension === 'json') {
    validatePreparedPage(relativePath, content, parsed, findings, validationContext);
  }
  if (path.posix.basename(relativePath) === 'page-x.json') {
    validatePageProperties(repo, relativePath, parsed, findings);
  }
  if (path.posix.basename(relativePath) === 'page-r-x.json') {
    validatePagePropertyRules(repo, relativePath, parsed, findings);
  }
  if (path.posix.basename(relativePath) === 'layout-x.json') {
    validateRuleSetLayout(repo, relativePath, parsed, findings);
  }
}

function validateDiffWhitespace(repo, baseCommit, findings) {
  const checks = [
    ['diff', '--check', `${baseCommit}...HEAD`],
    ['diff', '--check'],
    ['diff', '--cached', '--check'],
  ];

  for (const args of checks) {
    const result = spawnSync('git', args, {
      cwd: repo,
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    const output = String(result.stdout || result.stderr || '').trim();
    if (result.status !== 0 && output) {
      addFinding(
        findings,
        'blocker',
        'git-diff-check',
        output
      );
    }
  }
}

function summarize(findings, files) {
  const summary = {
    filesChecked: files.length,
    blockers: 0,
    warnings: 0,
    info: 0,
    passed: true,
  };

  for (const finding of findings) {
    if (finding.severity === 'blocker') {
      summary.blockers += 1;
    } else if (finding.severity === 'warning') {
      summary.warnings += 1;
    } else {
      summary.info += 1;
    }
  }
  summary.passed = summary.blockers === 0;
  return summary;
}

function buildReport(options) {
  const requestedRepo = path.resolve(options.repo || process.cwd());
  const repo = runGit(requestedRepo, ['rev-parse', '--show-toplevel']);
  const base = resolveBase(repo, options.base);
  const changedFiles = collectChangedFiles(repo, base.commit);
  const findings = [];
  const head = runGit(repo, ['rev-parse', 'HEAD']);
  const worktreeStatus = splitLines(runGit(repo, ['status', '--porcelain'], false));
  const artifactTypes = {};
  const fileFingerprints = {};
  const validationContext = {
    evidenceManifest: options.evidenceManifest ? readEvidenceManifest(options.evidenceManifest) : null,
  };

  if (options.expectedHead) {
    const expectedHead = runGit(repo, ['rev-parse', '--verify', options.expectedHead], false);
    if (!expectedHead || expectedHead !== head) {
      addFinding(
        findings,
        'blocker',
        'expected-head-mismatch',
        `Current HEAD ${head} does not match the reviewed commit ${options.expectedHead}.`
      );
    }
  }
  if (options.requireClean && worktreeStatus.length > 0) {
    addFinding(
      findings,
      'blocker',
      'worktree-not-clean',
      'The worktree contains staged, unstaged, or untracked changes.'
    );
  }

  for (const relativePath of changedFiles) {
    const portablePath = relativePath.split(path.sep).join('/');
    const absolutePath = path.join(repo, relativePath);
    artifactTypes[portablePath] = options.allowReleaseToolingUpdate && isReleaseToolingPath(portablePath)
      ? 'release-tooling'
      : classifyArtifact(portablePath);
    if (
      artifactTypes[portablePath] === 'express-advanced-expression'
      && !isImportedExtensionExpression(repo, portablePath)
    ) {
      // A JavaScript location is insufficient proof that the customer owns the expression.
      artifactTypes[portablePath] = 'unproven-advanced-expression';
    }
    fileFingerprints[portablePath] = fingerprintFile(absolutePath);
    validateArtifactPolicy(portablePath, artifactTypes[portablePath], findings);

    if (artifactTypes[portablePath] === 'release-tooling') {
      if (fs.existsSync(absolutePath) && fs.statSync(absolutePath).isFile()) {
        const content = fs.readFileSync(absolutePath, 'utf8');
        validateText(portablePath, content, findings);
        if (portablePath.endsWith('.json')) {
          validateJson(repo, portablePath, content, findings, validationContext);
        }
      }
      continue;
    }

    if (!isExtensionOwnedPath(portablePath)) {
      addFinding(
        findings,
        'blocker',
        'outside-extension-scope',
        'The changed file is outside the approved Fusion Extension source scope.',
        portablePath
      );
      continue;
    }

    if (looksLikeFaArtifact(portablePath)) {
      addFinding(
        findings,
        'blocker',
        'fa-artifact-change',
        'The changed file looks like an unsuffixed Oracle-delivered artifact.',
        portablePath
      );
    }

    if (!fs.existsSync(absolutePath) || !fs.statSync(absolutePath).isFile()) {
      continue;
    }

    const content = fs.readFileSync(absolutePath, 'utf8');
    validateText(portablePath, content, findings);
    if (artifactTypes[portablePath] === 'express-page-preparation-module') {
      validatePreparedPage(portablePath, content, null, findings, validationContext);
    }
    if (portablePath.endsWith('.json')) {
      validateJson(repo, portablePath, content, findings, validationContext);
    }
    if (portablePath.endsWith('.js')) {
      validateJavaScript(repo, portablePath, content, findings);
    }
  }

  validateDiffWhitespace(repo, base.commit, findings);

  if (changedFiles.length === 0) {
    addFinding(
      findings,
      options.requireChanges ? 'blocker' : 'info',
      'no-changed-files',
      options.requireChanges
        ? 'No reviewed Extension changes were found relative to the selected integration base.'
        : 'No changed files were found relative to the selected base and working tree.'
    );
  }

  return {
    repository: repo,
    base,
    reviewedState: {
      head,
      expectedHead: options.expectedHead || null,
      worktreeClean: worktreeStatus.length === 0,
      worktreeStatus,
      artifactTypes,
      fileFingerprints,
    },
    changedFiles,
    findings,
    summary: summarize(findings, changedFiles),
  };
}

function printHuman(report) {
  process.stdout.write(
    [
      `Repository: ${report.repository}`,
      `Base: ${report.base.ref} (${report.base.commit})`,
      `Reviewed HEAD: ${report.reviewedState.head}`,
      `Worktree clean: ${report.reviewedState.worktreeClean ? 'yes' : 'no'}`,
      `Files checked: ${report.summary.filesChecked}`,
      `Blockers: ${report.summary.blockers}`,
      `Warnings: ${report.summary.warnings}`,
      `Result: ${report.summary.passed ? 'PASS' : 'FAIL'}`,
      '',
    ].join('\n')
  );

  for (const finding of report.findings) {
    const file = finding.file ? ` ${finding.file}` : '';
    process.stdout.write(`[${finding.severity.toUpperCase()}] ${finding.code}${file}: ${finding.message}\n`);
  }
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
    if (!report.summary.passed) {
      process.exitCode = 1;
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
  classifyArtifact,
  collectChangedFiles,
  fingerprintFile,
  isExtensionOwnedPath,
  isReleaseToolingPath,
  looksLikeFaArtifact,
  parseArgs,
  readEvidenceManifest,
  resolveBase,
  resolveArtifactCounterpart,
  resolveArtifactCounterparts,
  resolveEvidenceManifestCounterpart,
  resolvePreparedPageEvidence,
  resolvePreparedPagePath,
  resolvePagePropertiesCounterpart,
  isImportedExtensionExpression,
  validatePagePropertyRules,
  validateRuleSetLayout,
};
