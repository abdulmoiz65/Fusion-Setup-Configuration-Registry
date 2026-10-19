#!/usr/bin/env node
// Run from a temporary directory linked to the installed spreadsheet runtime.
import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";
import { FileBlob, SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const [command, ...argv] = process.argv.slice(2);
if (command === "--help" || !command) {
  console.log("Usage: intake_workbook.mjs create|read|validate|review --input FILE --output FILE [--catalog intake-fields.json] [--render-prefix PATH] [--render-range A1:H8]");
  process.exit(0);
}
const args = {};
for (let i = 0; i < argv.length; i += 2) {
  if (!argv[i].startsWith("--") || !argv[i + 1]) throw new Error("Expected --option value pairs.");
  args[argv[i].slice(2)] = argv[i + 1];
}
if (!args.input || !args.output) throw new Error("--input and --output are required.");
try { await fs.access(args.output); throw new Error("Refusing to overwrite " + args.output); }
catch (error) { if (error.code !== "ENOENT") throw error; }
await fs.mkdir(path.dirname(args.output), {recursive: true});
const norm = value => String(value ?? "").trim().replace(/[*†‡]+$/, "").trim().toLowerCase();
const present = value => value !== null && value !== undefined && String(value).trim() !== "";
const excelText = value => typeof value === "string" && value.startsWith("=") ? "'" + value : value;
const textValue = value => typeof value === "string" && value.startsWith("'=") ? value.slice(1) : value;
const blankBehaviorChoice = (field, value) => field.key.startsWith("field_behaviors.")
  && typeof value === "string" && value.trim().toLowerCase() === "blank";
const normalizedInputValue = (field, value) => blankBehaviorChoice(field, value) ? null : value;
const column = index => {
  let n = index + 1, result = "";
  while (n) { n--; result = String.fromCharCode(65 + n % 26) + result; n = Math.floor(n / 26); }
  return result;
};
function note(wb, sh, address, body) {
  wb.notes.add({id: sh.name + ":" + address, target:{cell:{sheetName:sh.name, sheetId:sh.sheetId, address}},
    authorId:"", createdAt:"", body:{plainText:body}});
}
function style(sh, row, count, section = false) {
  const r = sh.getRangeByIndexes(row, 0, 1, count);
  r.format = {fill: section ? "#256046" : "#DCEBDC", font:{name:"Arial",size:11,bold:true,color:section?"#FFFFFF":"#173D2A"},
    wrapText:true, verticalAlignment:"center", rowHeight:section?27:82};
}
function dateText(value) {
  if (typeof value === "number") {
    const d = new Date(Date.UTC(1899, 11, 30) + Math.round(value * 86400000));
    return Number.isFinite(d.getTime()) ? d.toISOString().slice(0, 10) : String(value);
  }
  return value instanceof Date ? value.toISOString().slice(0, 10) : value;
}
function parseCsv(text) {
  // Workbook.fromCSV evaluates cells beginning with "=" in this runtime.
  // Parse the review source literally so no source formula can execute.
  const rows=[], row=[];
  let field="", quoted=false, closed=false;
  for(let i=0;i<text.length;i++){
    const c=text[i];
    if(quoted){
      if(c==='"' && text[i+1]==='"'){field+='"';i++;}
      else if(c==='"'){quoted=false;closed=true;}
      else field+=c;
    }else if(c===","){
      row.push(field);field="";closed=false;
    }else if(c==="\r"||c==="\n"){
      row.push(field);rows.push([...row]);row.length=0;field="";closed=false;
      if(c==="\r"&&text[i+1]==="\n")i++;
    }else if(c==='"'&&!field&&!closed){
      quoted=true;
    }else{
      if(closed||c==='"')throw new Error("Malformed quoted CSV field.");
      field+=c;
    }
  }
  if(quoted)throw new Error("Unterminated quoted CSV field.");
  if(field||row.length||closed){row.push(field);rows.push([...row]);}
  return rows;
}
function checkValue(field, value) {
  value = normalizedInputValue(field, value);
  if (!present(value)) return field.requiredFor === "always" ? "Required value is missing." : null;
  if (value === "Clear") return field.nullable ? null : "Clear is only valid for nullable existing-record fields.";
  if (field.kind === "text" && typeof value !== "string") return "Enter text; keep identifiers and leading zeros as text.";
  if (field.options && !field.options.includes(value)) return "Select " + field.options.join(", ") + ".";
  if (field.maximum && String(value).length > field.maximum) return "Maximum length is " + field.maximum + ".";
  if (field.kind === "number" && (typeof value === "boolean" || !/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$/.test(String(value)) || !Number.isFinite(Number(value))))
    return "Enter a finite number without a currency symbol/code.";
  if (field.kind === "date" && (!/^\d{4}-\d{2}-\d{2}$/.test(value) || !Number.isFinite(Date.parse(value)) || new Date(value).toISOString().slice(0,10) !== value))
    return "Enter a real date as YYYY-MM-DD.";
  return null;
}

function validateModel(catalog, result) {
  // Recompute value errors, but never erase unresolved workbook/source errors
  // when revalidating chat corrections. Reparse a corrected workbook to clear them.
  result.issues = [...(result.source_issues ?? [])];
  result.pending_checks = [];
  const entries = [];
  for (const block of result.blocks) {
    const section = catalog.sections.find(s=>s.key===block.section);
    if (!section || !Array.isArray(block.rows)) throw new Error("Unknown section or invalid rows.");
    block.rows.forEach((record, index)=>{
      for (const field of section.fields) record[field.key]=normalizedInputValue(field,record[field.key]);
      if (!Object.values(record).some(present)) return;
      const locations=block.source_cells?.[index] ?? {};
      const sourceRow=Number(Object.values(locations)[0]?.match(/\d+$/)?.[0]) || index+catalog.first_data_row;
      const issue=(field,message)=>result.issues.push({sheet:section.sheet_name,row:sourceRow,cell:locations[field]??null,field,message});
      entries.push({section:section.key,record,issue});
      for(const key of Object.keys(record)) if(!section.fields.some(f=>f.key===key)) issue(key,"Unsupported input field. Card and policy changes are outside this cash-only workflow.");
      for(const f of section.fields){
        const msg=checkValue(f,record[f.key]);
        if(msg)issue(f.key,msg);
        if(!present(record[f.key]) && f.requiredFor==='create'){
          result.pending_checks.push({sheet:section.sheet_name,field:f.key,reason:'Require this value if the fresh target export classifies the identity as new.'});
        }
        if(record[f.key]==='Clear'){
          result.pending_checks.push({sheet:section.sheet_name,field:f.key,reason:'Confirm that the fresh target export classifies this identity as existing before applying Clear.'});
        }
      }
      const end=record.end_date??record.inactive_date;
      if(record.start_date && end && end!=="Clear" && end<record.start_date)issue("end_date","End date cannot precede start date.");
      for(const f of section.fields.filter(f=>f.requiredWhen)){
        const [shortKey,value]=f.requiredWhen.split('=');
        const key=shortKey==='cash_receipt_required'?'receipt_rules.cash_receipt_required':shortKey;
        if(record[key]===value && (!present(record[f.key]) || record[f.key]==='Clear')){
          result.pending_checks.push({sheet:section.sheet_name,field:f.key,reason:`Validate this value against the fresh baseline when ${key} is ${value}; it is required if the identity is new.`});
        }
      }
    });
  }
  for(const section of catalog.sections){
    const identities={templates:['business_unit','name'],types:['template_name','name'],itemizations:['business_unit','template_name','parent_type_name','child_type_name']};
    const keys=identities[section.key];
    if(!keys)throw new Error('No identity contract for '+section.key);
    const seen=new Set();
    for(const e of entries.filter(e=>e.section===section.key)){
      if(keys.some(k=>!present(e.record[k])))continue;
      const key=JSON.stringify(keys.map(k=>norm(e.record[k])));
      if(seen.has(key))e.issue(keys.at(-1),'Duplicate record identity. Keep one intended operation per record.');
      seen.add(key);
    }
  }
  for(const e of entries.filter(e=>e.section==='types')){
    const matches=entries.filter(t=>t.section==='templates' && norm(t.record.name)===norm(e.record.template_name));
    if(matches.length>1)e.issue('template_name','Ambiguous parent: Expense Types has no Business Unit. Separate same-named templates into different workbooks.');
    if(matches.length===0)result.pending_checks.push({sheet:'Expense Types',field:'template_name',reason:'Resolve the existing parent and its Business Unit uniquely from the fresh baseline before building.'});
  }
  for(const e of entries.filter(e=>e.section==='itemizations')){
    const owner=e.record.parent_type_name;
    const matches=entries.filter(t=>t.section==='types' && norm(t.record.template_name)===norm(e.record.template_name) && norm(t.record.name)===norm(owner));
    const configuredTemplate=entries.filter(t=>t.section==='templates' && norm(t.record.name)===norm(e.record.template_name));
    const localParentTemplates=new Set(entries.filter(t=>t.section==='types' && norm(t.record.name)===norm(owner))
      .map(t=>norm(t.record.template_name)));
    const localChildTemplates=new Set(entries.filter(t=>t.section==='types' && norm(t.record.name)===norm(e.record.child_type_name))
      .map(t=>norm(t.record.template_name)));
    const sharedLocalTemplate=[...localParentTemplates].filter(template=>localChildTemplates.has(template));
    let mappingScopeInvalid=false;
    if(!matches.length && sharedLocalTemplate.length===1){
      e.issue('template_name',`Itemization parent and child are configured for template ${JSON.stringify(sharedLocalTemplate[0])}, but this mapping specifies ${JSON.stringify(norm(e.record.template_name))}.`);
      mappingScopeInvalid=true;
    }
    if(configuredTemplate.length===1 && norm(configuredTemplate[0].record.business_unit)!==norm(e.record.business_unit)){
      e.issue('business_unit',`Itemization mapping business unit ${JSON.stringify(e.record.business_unit)} does not match template ${JSON.stringify(e.record.template_name)} business unit ${JSON.stringify(configuredTemplate[0].record.business_unit)}.`);
      mappingScopeInvalid=true;
    }
    const control=matches[0]?.record.itemization;
    if(control==='Disabled')e.issue('parent_type_name','Mapping conflicts with the owning type’s Disabled setting.');
    if(!control && !mappingScopeInvalid)result.pending_checks.push({sheet:e.section,field:'owner',reason:'Validate the owning type and retained control in the fresh baseline.'});
    if(norm(owner)===norm(e.record.child_type_name))e.issue('child_type_name','An expense type cannot itemize itself.');
    if(e.record.include==='No')e.issue('include','Include No requires a verified FSM deletion contract; row omission does not remove an existing relationship.');
    if(present(e.record.end_date))e.issue('end_date','The exported itemization mapping has no Effective End Date column; end-dating and Clear are not supported for this relationship.');
  }
  result.status=result.issues.length?'needs_correction':entries.length?'local_shape_valid':'needs_input';
  if(!entries.length)result.issues.push({field:'workbook',message:'No populated records. Provide at least one row in the V3 workbook.'});
  return result;
}

let wb;
if (command === "create") {
  if (!args.catalog) throw new Error("--catalog is required.");
  const catalog=JSON.parse(await fs.readFile(args.catalog,'utf8'));
  const model=JSON.parse(await fs.readFile(args.input,'utf8'));
  if(!Array.isArray(model.blocks))throw new Error('A blocks array is required.');
  if(model.blocks.some(b=>!catalog.sections.some(s=>s.key===b.section)))throw new Error('Unknown intake section.');
  wb=Workbook.create();
  for(const section of catalog.sections){
    const sh=wb.worksheets.add(section.sheet_name);
    const records=model.blocks.filter(b=>b.section===section.key).flatMap(b=>b.rows.map(r=>Object.values(r).some(present)?{...r}:{}));
    const width=section.fields.length, count=Math.max(catalog.entry_rows,records.length);
    sh.getRangeByIndexes(0,0,1,Math.min(6,width)).merge();
    sh.getCell(0,0).values=[[section.title]];
    sh.getRangeByIndexes(0,0,1,width).format={fill:'#595959',font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},rowHeight:27};
    for(const [r,text,height] of [[1,section.description,86],[2,'* Required for every populated row. † Required if the fresh target export identifies a new record. ‡ Conditionally required. Existing-record blanks mean unchanged; Clear removes a nullable value. Blank rows are ignored.',42]]){
      // Keep the merged instruction block within six columns. Wider merged
      // cells can render as a blank overlay in Excel for these wide tables.
      sh.getRangeByIndexes(r,0,1,Math.min(6,width)).merge();
      sh.getCell(r,0).values=[[text]];
      sh.getRangeByIndexes(r,0,1,width).format={wrapText:true,verticalAlignment:'center',rowHeight:height};
    }
    sh.getRangeByIndexes(3,0,1,width).values=[section.fields.map(f=>f.label+({always:'*',create:'†',conditional:'‡'}[f.requiredFor]??''))];
    for(let c=0;c<width;c++){
      const field=section.fields[c],range=sh.getRangeByIndexes(4,c,count,1);
      note(wb,sh,column(c)+'4',field.note);
      range.setNumberFormat(field.kind==='date'?'yyyy-mm-dd':field.kind==='number'?'0.########':'@');
      if(field.options)range.dataValidation={rule:{type:'list',values:field.options},errorAlert:{style:'stop',title:'Choose a listed value',message:'Select a listed value or leave blank when applicable.'}};
      for(let r=0;r<records.length;r++){
        const record=records[r];
        if(Object.keys(record).some(k=>!section.fields.some(f=>f.key===k)))throw new Error('Unmapped display fields.');
        let v=normalizedInputValue(field,record[field.key]??null);
        if(field.kind==='date' && typeof v==='string' && /^\d{4}-\d{2}-\d{2}$/.test(v) && !checkValue(field,v))v=new Date(v+'T00:00:00Z');
        sh.getCell(r+4,c).values=[[excelText(v)]];
      }
    }
    sh.getRangeByIndexes(0,0,count+4,width).format.font.name='Arial';
    sh.getRangeByIndexes(0,0,count+4,width).format.font.size=11;
    sh.getRangeByIndexes(0,0,count+4,width).format.columnWidth=25;
    sh.getRangeByIndexes(0,0,count+4,1).format.columnWidth=34;
    sh.getRangeByIndexes(4,0,count,width).format.rowHeight=26;
    sh.getRangeByIndexes(4,0,count,width).format.borders={preset:'all',style:'thin',color:'#808080'};
    const table=sh.tables.add(`A4:${column(width-1)}${count+4}`,true,'Intake_'+section.key);
    table.style='TableStyleLight1';
    sh.getRangeByIndexes(3,0,1,width).format={fill:'#D0D0D0',font:{name:'Arial',size:11,bold:true,color:'#000000'},wrapText:true,verticalAlignment:'center',rowHeight:82};
    sh.freezePanes.freezeRows(4);
  }
} else if (command === "read" || command === "validate") {
  if(!args.catalog)throw new Error('--catalog is required.');
  const catalog=JSON.parse(await fs.readFile(args.catalog,'utf8'));
  let result;
  if(command==='validate'){
    result=JSON.parse(await fs.readFile(args.input,'utf8'));
  }else{
    if(path.extname(args.input).toLowerCase()!=='.xlsx')throw new Error('Provide the V3 .xlsx workbook, not a macro-enabled or other file format.');
    wb=await SpreadsheetFile.importXlsx(await FileBlob.load(args.input));
    const names=wb.worksheets.items.map(s=>s.name);
    if(names.includes('Project Expenditure Mappings'))throw new Error('Project Expenditure Mappings is not part of the current workbook: Projects is disabled for this import flow.');
    if(names.length!==catalog.sections.length || catalog.sections.some(s=>!names.includes(s.sheet_name)))throw new Error('Provide the current workbook with its required named sheets.');
    result={schema_version:catalog.schema_version,blocks:[],source_issues:[]};
    for(const section of catalog.sections){
      const sh=wb.worksheets.getItem(section.sheet_name),range=sh.getUsedRange();
      const values=range.values,formulas=range.formulas;
      const cells=values[catalog.header_row-1]??[];
      const headers=cells.map(v=>section.fields.find(f=>norm(f.label)===norm(v)));
      if((formulas[catalog.header_row-1]??[]).some(present))result.source_issues.push({sheet:sh.name,cell:'A4',message:'Formula headers are not accepted. Use the unchanged V3 header row.'});
      const known=headers.filter(Boolean).map(f=>f.key);
      if(new Set(known).size!==known.length)throw new Error('Duplicate field header in '+sh.name);
      for(let c=0;c<cells.length;c++)if(present(cells[c])&&!headers[c])result.source_issues.push({sheet:sh.name,cell:column(c)+'4',message:'Unsupported header: '+cells[c]});
      for(const f of section.fields)if(!known.includes(f.key))result.source_issues.push({sheet:sh.name,cell:'A4',field:f.key,message:'Missing V3 field header.'});
      const block={section:section.key,operation:'target-resolved',rows:[],source_cells:[]};
      result.blocks.push(block);
      for(let row=catalog.first_data_row-1;row<values.length;row++){
        const cells=values[row]??[];
        if(!cells.some(present) && !(formulas[row]??[]).some(present))continue;
        const record={},locations={};
        for(let c=0;c<Math.max(cells.length,headers.length,(formulas[row]??[]).length);c++){
          const field=headers[c],address=column(c)+(row+1);
          if(!field){
            if(present(cells[c]) || present(formulas[row]?.[c]))result.source_issues.push({sheet:sh.name,cell:address,message:'Value has no mapped field header.'});
            continue;
          }
          let value=field.kind==='date'?dateText(cells[c]):textValue(cells[c]??null);
          value=normalizedInputValue(field,value);
          record[field.key]=value;locations[field.key]=address;
          if(present(formulas[row]?.[c])){
            record[field.key]=null;
            result.source_issues.push({sheet:sh.name,cell:address,field:field.key,message:'Formula inputs are not accepted.'});
          }
        }
        block.rows.push(record);block.source_cells.push(locations);
      }
    }
  }
  validateModel(catalog,result);
  await fs.writeFile(args.output,JSON.stringify(result,null,2)+'\n',{flag:'wx'});
  console.log(JSON.stringify({status:result.status,blocks:result.blocks.length,issues:result.issues.length,pending_checks:result.pending_checks.length}));
  process.exit(0);
} else if(command==="review"){
  const manifest=JSON.parse(await fs.readFile(args.input,"utf8"));
  const zipHash=crypto.createHash("sha256").update(await fs.readFile(manifest.candidate.zip)).digest("hex");
  if(zipHash!==manifest.candidate.sha256) throw new Error("Candidate changed after CSV review extraction.");
  wb=Workbook.create();
  const index=wb.worksheets.add("Package");
  index.getRange("A1:C3").values=[["FSM CSV review",null,null],["Candidate SHA-256",manifest.candidate.sha256,null],["CSV member","Rows","Sheet"]];
  index.getRange("B2:C2").merge();
  index.getRange("B2").values=[[manifest.candidate.sha256]];
  index.getRange("A1:C1").format.font={bold:true,size:14};
  style(index,2,3);
  for(let i=0;i<manifest.csvs.length;i++){
    const entry=manifest.csvs[i];
    if(path.basename(entry.member)!==entry.member) throw new Error("Unsafe review member name.");
    const content=await fs.readFile(path.join(path.dirname(args.input),entry.member));
    if(crypto.createHash("sha256").update(content).digest("hex")!==entry.sha256) throw new Error("Review CSV changed: "+entry.member);
    const name=String(i+1).padStart(2,"0")+" "+entry.member.replace(/\.csv$/i,"").slice(0,28);
    const sh=wb.worksheets.add(name);
    sh.showGridLines=false;
    const rows=entry.rows;
    const csvValues=parseCsv(content.toString("utf8").replace(/^\uFEFF/,""));
    if(JSON.stringify(csvValues)!==JSON.stringify(rows)) throw new Error("Review grid differs from extracted CSV: "+entry.member);
    if(crypto.createHash("sha256").update(JSON.stringify(rows)).digest("hex")!==entry.grid_sha256)
      throw new Error("Review manifest grid changed: "+entry.member);
    if(rows.length!==entry.row_count+1 || rows.some(r=>r.length!==entry.columns.length) || JSON.stringify(rows[0])!==JSON.stringify(entry.columns))
      throw new Error("Review manifest grid mismatch: "+entry.member);
    const range=sh.getRangeByIndexes(0,0,rows.length,entry.columns.length);
    range.setNumberFormat("@");range.values=rows.map(r=>r.map(excelText));
    range.format.font={name:"Arial",size:11};range.format.wrapText=true;
    for(let col=0;col<entry.columns.length;col++){
      const width=Math.max(18,Math.min(48,rows.reduce((max,r)=>Math.max(max,r[col].length),0)+2));
      sh.getRangeByIndexes(0,col,rows.length,1).format.columnWidth=width;
    }
    range.format.autofitRows();
    style(sh,0,entry.columns.length);
    sh.freezePanes.freezeRows(1);
    const actual=range.values;
    if(rows.some((r,ri)=>r.some((value,ci)=>actual[ri][ci]!==value && actual[ri][ci]!==excelText(value))))
      throw new Error("Review values changed in workbook: "+entry.member);
    index.getRangeByIndexes(i+3,0,1,3).values=[[entry.member,entry.row_count,name]];
  }
  index.showGridLines=false;index.getRange("A1:C"+(manifest.csvs.length+3)).format.columnWidth=38;
  index.getRange("A3:C3").format.rowHeight=26;
}else throw new Error("Unknown command: "+command);

wb.recalculate();
const errors=await wb.inspect({kind:"match",searchTerm:"#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#SPILL!|#CALC!",options:{useRegex:true,maxResults:20}});
if(args["render-prefix"]){
  for(let i=0;i<wb.worksheets.items.length;i++){
    const sh=wb.worksheets.getItemAt(i);
    const preview=await wb.render({sheetName:sh.name,range:args["render-range"] ?? (command==="create"?"A1:G45":"A1:F8"),scale:1,format:"png"});
    await fs.writeFile(args["render-prefix"]+"-"+i+".png",new Uint8Array(await preview.arrayBuffer()));
  }
}
await (await SpreadsheetFile.exportXlsx(wb)).save(args.output);
console.log(JSON.stringify({status:"written",sheets:wb.worksheets.items.length,output:args.output,formula_scan:errors.ndjson}));
