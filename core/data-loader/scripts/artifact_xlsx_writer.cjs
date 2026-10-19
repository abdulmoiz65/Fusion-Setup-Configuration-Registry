"use strict";

// Serialize Data Loader workbooks through the bundled artifact tool.  Its XLSX
// exporter creates the full OOXML package required by Codex's spreadsheet preview.

const fs = require("node:fs/promises");
const { FileBlob, SpreadsheetFile, Workbook } = require("@oai/artifact-tool");

function literalText(value) {
  if (value === null || value === undefined) {
    return null;
  }
  const text = String(value);
  return text.startsWith("=") ? "'" + text : text;
}

async function main() {
  const [inputPath] = process.argv.slice(2);
  if (inputPath === "--verify") {
    const [workbookPath] = process.argv.slice(3);
    if (!workbookPath) {
      throw new Error("Usage: artifact_xlsx_writer.cjs --verify <workbook.xlsx>");
    }
    const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(workbookPath));
    const sheets = await workbook.inspect({ kind: "sheet", include: "id,name" });
    const sheetNames = sheets.ndjson
      .trim()
      .split("\n")
      .map((line) => JSON.parse(line).name);
    for (const sheetName of sheetNames) {
      await workbook.render({ sheetName, autoCrop: "all", scale: 1, format: "png" });
    }
    console.log(JSON.stringify({ sheets: sheetNames }));
    return;
  }
  if (!inputPath) {
    throw new Error("Usage: artifact_xlsx_writer.cjs <payload.json>");
  }
  const payload = JSON.parse(await fs.readFile(inputPath, "utf8"));
  const workbook = Workbook.create();

  for (const sourceSheet of payload.sheets || []) {
    const sheet = workbook.worksheets.add(sourceSheet.title);
    const rows = sourceSheet.rows || [];
    const columnCount = rows.reduce((maximum, row) => Math.max(maximum, row.length), 0);
    if (rows.length && columnCount) {
      const values = rows.map((row) => Array.from(
        { length: columnCount },
        (_unused, index) => literalText(row[index]),
      ));
      sheet.getRangeByIndexes(0, 0, values.length, columnCount).values = values;
    }
  }

  const exported = await SpreadsheetFile.exportXlsx(workbook);
  await exported.save(payload.outputPath);
}

main().then(
  () => process.exit(0),
  (error) => {
    console.error(error && error.stack ? error.stack : String(error));
    process.exit(1);
  },
);
