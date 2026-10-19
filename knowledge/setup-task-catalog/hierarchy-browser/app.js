const MAPPING_URL = "../effective/pillars-offerings-mapping.json";
const CATALOG_URL = "../effective/offering-functional-area-task-catalog.json";

const state = {
  mapping: null,
  catalog: null,
  nodesById: new Map(),
  expanded: new Set(),
  selectedId: null,
  selectedPillars: new Set(),
  query: "",
  hierarchy: []
};

const els = {
  catalogMeta: document.getElementById("catalogMeta"),
  pillarCount: document.getElementById("pillarCount"),
  offeringCount: document.getElementById("offeringCount"),
  functionalAreaCount: document.getElementById("functionalAreaCount"),
  taskCount: document.getElementById("taskCount"),
  pillarFilters: document.getElementById("pillarFilters"),
  treeRoot: document.getElementById("treeRoot"),
  visibleCount: document.getElementById("visibleCount"),
  searchInput: document.getElementById("searchInput"),
  collapseButton: document.getElementById("collapseButton"),
  expandMatchesButton: document.getElementById("expandMatchesButton"),
  detailEmpty: document.getElementById("detailEmpty"),
  detailContent: document.getElementById("detailContent"),
  detailType: document.getElementById("detailType"),
  detailTitle: document.getElementById("detailTitle"),
  detailCode: document.getElementById("detailCode"),
  detailFacts: document.getElementById("detailFacts"),
  detailDescription: document.getElementById("detailDescription")
};

function formatNumber(value) {
  return new Intl.NumberFormat("en-US").format(value || 0);
}

function normalize(value) {
  return String(value || "").toLowerCase();
}

function taskSortValue(task) {
  const parsed = Number.parseFloat(task.displaySequence);
  return Number.isFinite(parsed) ? parsed : Number.MAX_SAFE_INTEGER;
}

function makeNode(type, id, title, code, meta = {}, children = []) {
  const node = { type, id, title, code, meta, children };
  state.nodesById.set(id, node);
  return node;
}

function buildHierarchy(mapping, catalog) {
  state.nodesById.clear();
  const byPillar = new Map();

  for (const pillar of mapping.pillarOrder) {
    const pillarSlug = normalize(pillar);
    byPillar.set(pillar, makeNode("pillar", `pillar:${pillarSlug}`, pillar, pillarSlug, {
      pillar,
      pillarSlug
    }));
  }

  for (const item of mapping.items) {
    const pillarNode = byPillar.get(item.pillar);
    if (!pillarNode) {
      continue;
    }

    const offering = catalog.offerings[item.offeringShortName];
    const offeringNode = makeNode(
      "offering",
      `offering:${item.offeringShortName}`,
      item.offeringName,
      item.offeringShortName,
      {
        ...item,
        functionalAreaCount: offering?.functionalAreaCount || 0,
        taskCount: offering?.taskCount || 0,
        enabledFlag: offering?.enabledFlag,
        obsoleteFlag: offering?.obsoleteFlag
      }
    );

    if (offering) {
      for (const areaCode of offering.functionalAreaOrder || []) {
        const area = offering.functionalAreas[areaCode];
        if (!area) {
          continue;
        }

        const areaNode = makeNode(
          "functional-area",
          `area:${item.offeringShortName}:${areaCode}`,
          area.functionalAreaName,
          area.functionalAreaShortName,
          {
            ...area,
            offeringName: item.offeringName,
            offeringShortName: item.offeringShortName,
            pillar: item.pillar,
            taskCount: area.taskCount || (area.tasks || []).length
          }
        );

        const tasks = [...(area.tasks || [])].sort((a, b) => taskSortValue(a) - taskSortValue(b));
        for (const task of tasks) {
          areaNode.children.push(makeNode(
            "setup-task",
            `task:${item.offeringShortName}:${areaCode}:${task.taskShortName}:${task.taskListItemShortName}`,
            task.taskName,
            task.taskShortName,
            {
              ...task,
              offeringName: item.offeringName,
              offeringShortName: item.offeringShortName,
              functionalAreaName: area.functionalAreaName,
              functionalAreaShortName: area.functionalAreaShortName,
              pillar: item.pillar
            }
          ));
        }

        offeringNode.children.push(areaNode);
      }
    }

    pillarNode.children.push(offeringNode);
  }

  return [...byPillar.values()];
}

function nodeSearchText(node) {
  const fields = [node.title, node.code, node.type];
  if (node.meta) {
    fields.push(
      node.meta.pillar,
      node.meta.offeringName,
      node.meta.folderPath,
      node.meta.functionalAreaName,
      node.meta.taskDescription,
      node.meta.taskListItemShortName
    );
  }
  return normalize(fields.filter(Boolean).join(" "));
}

function filterNode(node) {
  if (node.type === "pillar" && !state.selectedPillars.has(node.title)) {
    return null;
  }

  const query = normalize(state.query.trim());
  const ownMatch = !query || nodeSearchText(node).includes(query);
  const filteredChildren = [];

  for (const child of node.children || []) {
    const filtered = filterNode(child);
    if (filtered) {
      filteredChildren.push(filtered);
    }
  }

  if (ownMatch || filteredChildren.length) {
    return { ...node, children: filteredChildren, isMatch: Boolean(query && ownMatch) };
  }

  return null;
}

function descendantCount(node, type) {
  let count = node.type === type ? 1 : 0;
  for (const child of node.children || []) {
    count += descendantCount(child, type);
  }
  return count;
}

function supportsCsvExportImport(flag) {
  return flag === true || String(flag).toUpperCase() === "Y";
}

function badgeFor(node) {
  if (node.type === "pillar") {
    return `${descendantCount(node, "offering")}`;
  }
  if (node.type === "offering") {
    return `${formatNumber(node.meta.taskCount)}`;
  }
  if (node.type === "functional-area") {
    return `${formatNumber(node.meta.taskCount)}`;
  }
  if (node.type === "setup-task") {
    return supportsCsvExportImport(node.meta.csvExportImportSupportedFlag) ? "CSV" : "Task";
  }
  return "";
}

function badgeClass(node) {
  if (node.type === "setup-task" && supportsCsvExportImport(node.meta.csvExportImportSupportedFlag)) {
    return "badge blue";
  }
  return "badge";
}

function hasInlineCustomBadge(node) {
  return node.meta.isCustom && ["offering", "functional-area", "setup-task"].includes(node.type);
}

function subtitleFor(node) {
  if (node.type === "pillar") {
    return `${descendantCount(node, "functional-area")} functional areas`;
  }
  if (node.type === "offering") {
    return `${formatNumber(node.meta.functionalAreaCount)} functional areas`;
  }
  if (node.type === "functional-area") {
    return node.code;
  }
  if (node.type === "setup-task") {
    return node.code;
  }
  return "";
}

function renderNode(node) {
  const li = document.createElement("li");
  li.className = "tree-node";
  li.setAttribute("role", "treeitem");
  li.setAttribute("aria-expanded", node.children?.length ? String(state.expanded.has(node.id)) : "false");

  const row = document.createElement("button");
  row.type = "button";
  row.className = "node-row";
  row.dataset.nodeId = node.id;
  if (node.id === state.selectedId) {
    row.classList.add("is-selected");
  }
  if (node.isMatch) {
    row.classList.add("is-match");
  }

  const toggle = document.createElement("span");
  toggle.className = node.children?.length ? "toggle" : "toggle is-leaf";
  toggle.textContent = node.children?.length ? (state.expanded.has(node.id) ? "v" : ">") : ".";
  row.append(toggle);

  const main = document.createElement("span");
  main.className = "node-main";

  const title = document.createElement("span");
  title.className = "node-title";
  const titleText = document.createElement("span");
  titleText.className = "node-title-text";
  titleText.textContent = node.title;
  title.append(titleText);
  if (hasInlineCustomBadge(node)) {
    const customBadge = document.createElement("span");
    customBadge.className = "inline-custom-badge";
    customBadge.textContent = "Custom";
    title.append(customBadge);
  }
  main.append(title);

  const subtitle = document.createElement("span");
  subtitle.className = "node-subtitle";
  subtitle.textContent = subtitleFor(node);
  main.append(subtitle);

  row.append(main);

  const badge = document.createElement("span");
  badge.className = badgeClass(node);
  badge.textContent = badgeFor(node);
  row.append(badge);

  row.addEventListener("click", () => {
    if (node.children?.length) {
      if (state.expanded.has(node.id)) {
        state.expanded.delete(node.id);
      } else {
        state.expanded.add(node.id);
      }
    }
    state.selectedId = node.id;
    render();
  });

  li.append(row);

  if (node.children?.length && state.expanded.has(node.id)) {
    const ul = document.createElement("ul");
    ul.className = "tree-list";
    ul.setAttribute("role", "group");
    for (const child of node.children) {
      ul.append(renderNode(child));
    }
    li.append(ul);
  }

  return li;
}

function renderTree(filtered) {
  els.treeRoot.replaceChildren();

  if (!filtered.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = "No matching catalog items";
    els.treeRoot.append(empty);
    els.visibleCount.textContent = "0 nodes";
    return;
  }

  let visible = 0;
  const countVisible = (node) => {
    visible += 1;
    if (state.expanded.has(node.id)) {
      for (const child of node.children || []) {
        countVisible(child);
      }
    }
  };
  filtered.forEach(countVisible);

  const ul = document.createElement("ul");
  ul.className = "tree-list";
  for (const node of filtered) {
    ul.append(renderNode(node));
  }
  els.treeRoot.append(ul);
  els.visibleCount.textContent = `${formatNumber(visible)} nodes`;
}

function addFact(fragment, label, value) {
  if (value === undefined || value === null || value === "") {
    return;
  }
  const dt = document.createElement("dt");
  dt.textContent = label;
  const dd = document.createElement("dd");
  dd.textContent = String(value);
  fragment.append(dt, dd);
}

function renderDetails() {
  const node = state.nodesById.get(state.selectedId);
  if (!node) {
    els.detailEmpty.hidden = false;
    els.detailContent.hidden = true;
    return;
  }

  els.detailEmpty.hidden = true;
  els.detailContent.hidden = false;
  els.detailType.textContent = node.type.replace("-", " ");
  els.detailTitle.textContent = node.title;
  els.detailCode.textContent = node.code || "";

  const facts = document.createDocumentFragment();
  if (node.type === "pillar") {
    addFact(facts, "Pillar", node.meta.pillar);
    addFact(facts, "Offerings", descendantCount(node, "offering"));
    addFact(facts, "Functional areas", descendantCount(node, "functional-area"));
    addFact(facts, "Setup tasks", descendantCount(node, "setup-task"));
  } else if (node.type === "offering") {
    addFact(facts, "Pillar", node.meta.pillar);
    addFact(facts, "Folder path", node.meta.folderPath);
    addFact(facts, "Functional areas", node.meta.functionalAreaCount);
    addFact(facts, "Setup tasks", node.meta.taskCount);
    addFact(facts, "Enabled", node.meta.enabledFlag);
    addFact(facts, "Obsolete", node.meta.obsoleteFlag);
    addFact(facts, "Custom offering", node.meta.isCustom ? "Yes" : "No");
  } else if (node.type === "functional-area") {
    addFact(facts, "Pillar", node.meta.pillar);
    addFact(facts, "Offering", node.meta.offeringName);
    addFact(facts, "Feature ID", node.meta.featureId);
    addFact(facts, "Classification", node.meta.featureClassification);
    addFact(facts, "Enabled", node.meta.isFeatureEnabledFlag);
    addFact(facts, "Setup tasks", node.meta.taskCount);
    addFact(facts, "Custom functional area", node.meta.isCustom ? "Yes" : "No");
  } else if (node.type === "setup-task") {
    addFact(facts, "Pillar", node.meta.pillar);
    addFact(facts, "Offering", node.meta.offeringName);
    addFact(facts, "Functional area", node.meta.functionalAreaName);
    addFact(facts, "Custom task", node.meta.isCustom ? "Yes" : "No");
    addFact(facts, "Task list item", node.meta.taskListItemShortName);
    addFact(facts, "Display sequence", node.meta.displaySequence);
    addFact(facts, "Mandatory flag", node.meta.MandatoryFlag);
    addFact(facts, "CSV export/import", node.meta.csvExportImportSupportedFlag);
    addFact(facts, "Export/import", node.meta.exportImportSupportedFlag);
  }

  els.detailFacts.replaceChildren(facts);
  els.detailDescription.textContent = node.meta.taskDescription || "";
  els.detailDescription.hidden = !node.meta.taskDescription;
}

function renderFilters() {
  els.pillarFilters.replaceChildren();
  const counts = new Map(state.hierarchy.map((node) => [node.title, descendantCount(node, "offering")]));

  for (const pillar of state.mapping.pillarOrder) {
    const label = document.createElement("label");
    label.className = "pillar-filter";

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = state.selectedPillars.has(pillar);
    checkbox.addEventListener("change", () => {
      if (checkbox.checked) {
        state.selectedPillars.add(pillar);
      } else {
        state.selectedPillars.delete(pillar);
      }
      render();
    });

    const name = document.createElement("span");
    name.textContent = pillar;

    const count = document.createElement("small");
    count.textContent = `${counts.get(pillar) || 0}`;

    label.append(checkbox, name, count);
    els.pillarFilters.append(label);
  }
}

function filteredHierarchy() {
  return state.hierarchy.map(filterNode).filter(Boolean);
}

function expandMatches() {
  const filtered = filteredHierarchy();
  const visit = (node) => {
    if (node.children?.length) {
      state.expanded.add(node.id);
      node.children.forEach(visit);
    }
  };
  filtered.forEach(visit);
  render();
}

function collapseAll() {
  state.expanded.clear();
  for (const node of state.hierarchy) {
    state.expanded.add(node.id);
  }
  render();
}

function render() {
  const filtered = filteredHierarchy();
  renderTree(filtered);
  renderDetails();
}

function initialize() {
  state.hierarchy = buildHierarchy(state.mapping, state.catalog);
  state.selectedPillars = new Set(state.mapping.pillarOrder);
  for (const node of state.hierarchy) {
    state.expanded.add(node.id);
  }

  const offeringCount = state.mapping.items.filter((item) => item.itemType === "offering").length;
  els.pillarCount.textContent = formatNumber(state.mapping.counts.pillars);
  els.offeringCount.textContent = formatNumber(offeringCount);
  els.functionalAreaCount.textContent = formatNumber(state.catalog.counts.functionalAreas);
  els.taskCount.textContent = formatNumber(state.catalog.counts.tasks);
  const sourceCount = Object.values(state.catalog.sourceCatalogs || {}).flat().length;
  const sourceLabel = sourceCount ? ` using ${sourceCount} source catalogs` : "";
  els.catalogMeta.textContent = `${state.catalog.catalogName} from ${state.catalog.sourceEnvironment || "catalog source"}${sourceLabel}`;

  renderFilters();
  render();
}

async function loadCatalogs() {
  try {
    if (window.SETUP_CATALOG_DATA) {
      state.mapping = window.SETUP_CATALOG_DATA.mapping;
      state.catalog = window.SETUP_CATALOG_DATA.catalog;
      initialize();
      return;
    }

    const [mappingResponse, catalogResponse] = await Promise.all([
      fetch(MAPPING_URL),
      fetch(CATALOG_URL)
    ]);

    if (!mappingResponse.ok) {
      throw new Error(`Could not load ${MAPPING_URL}`);
    }
    if (!catalogResponse.ok) {
      throw new Error(`Could not load ${CATALOG_URL}`);
    }

    state.mapping = await mappingResponse.json();
    state.catalog = await catalogResponse.json();
    initialize();
  } catch (error) {
    els.catalogMeta.textContent = "Catalog load failed";
    els.treeRoot.innerHTML = "";
    const errorBox = document.createElement("div");
    errorBox.className = "error-state";
    errorBox.textContent = error.message;
    els.treeRoot.append(errorBox);
  }
}

els.searchInput.addEventListener("input", () => {
  state.query = els.searchInput.value;
  if (state.query.trim()) {
    expandMatches();
  } else {
    render();
  }
});

els.collapseButton.addEventListener("click", collapseAll);
els.expandMatchesButton.addEventListener("click", expandMatches);

loadCatalogs();
