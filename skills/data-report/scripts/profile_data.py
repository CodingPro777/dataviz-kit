#!/usr/bin/env python3
"""Profile CSV, TSV, JSON records, and basic XLSX workbooks using Python stdlib."""
from __future__ import annotations
import csv, json, math, re, statistics, sys, zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

NULLS = {"", "na", "n/a", "nan", "null", "none"}
DATE_RE = re.compile(r"^(?:\d{4}-\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}/\d{2,4})(?:[ T].*)?$")

def is_null(v):
    return v is None or (isinstance(v, str) and v.strip().lower() in NULLS)

def col_name(ref):
    letters = re.match(r"[A-Z]+", ref or "")
    n = 0
    for ch in (letters.group(0) if letters else "A"):
        n = n * 26 + ord(ch) - 64
    return n - 1

def load_xlsx(path):
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
          "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
    with zipfile.ZipFile(path) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall("m:si", ns):
                shared.append("".join(t.text or "" for t in si.iterfind(".//m:t", ns)))
        workbook = ET.fromstring(z.read("xl/workbook.xml"))
        sheet = workbook.find(".//m:sheets/m:sheet", ns)
        if sheet is None:
            return []
        rel_id = sheet.attrib.get("{%s}id" % ns["r"])
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        target = None
        for rel in rels:
            if rel.attrib.get("Id") == rel_id:
                target = rel.attrib.get("Target")
                break
        if not target:
            raise ValueError("Cannot locate first worksheet")
        sheet_path = target.lstrip("/")
        if not sheet_path.startswith("xl/"):
            sheet_path = "xl/" + sheet_path
        root = ET.fromstring(z.read(sheet_path))
        matrix = []
        for row in root.findall(".//m:sheetData/m:row", ns):
            vals = {}
            for c in row.findall("m:c", ns):
                idx = col_name(c.attrib.get("r", "A1"))
                typ = c.attrib.get("t")
                v = c.find("m:v", ns)
                inline = c.find("m:is/m:t", ns)
                value = inline.text if inline is not None else (v.text if v is not None else "")
                if typ == "s" and value != "":
                    value = shared[int(value)]
                elif typ == "b":
                    value = value == "1"
                vals[idx] = value
            width = max(vals.keys(), default=-1) + 1
            matrix.append([vals.get(i, "") for i in range(width)])
    if not matrix:
        return []
    headers = [str(v).strip() or "column_%d" % (i + 1) for i, v in enumerate(matrix[0])]
    return [{h: row[i] if i < len(row) else "" for i, h in enumerate(headers)} for row in matrix[1:]]

def load_rows(path):
    p = Path(path)
    suffix = p.suffix.lower()
    if suffix == ".xlsx":
        return load_xlsx(p)
    if suffix == ".json":
        data = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            for key in ("data", "rows", "records"):
                if isinstance(data.get(key), list):
                    data = data[key]
                    break
        if not isinstance(data, list) or any(not isinstance(x, dict) for x in data):
            raise ValueError("JSON must be a list of records or an object containing data/rows/records")
        return data
    if suffix not in (".csv", ".tsv", ".txt"):
        raise ValueError("Unsupported input type: %s" % suffix)
    delimiter = "\t" if suffix == ".tsv" else ","
    with p.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=delimiter))

def infer(values):
    non = [v for v in values if not is_null(v)]
    if not non:
        return "empty"
    text = [str(v).strip() for v in non[:200]]
    numeric = 0
    for v in text:
        try:
            float(v.replace(",", ""))
            numeric += 1
        except ValueError:
            pass
    if numeric / len(text) >= 0.95:
        return "numeric"
    if all(DATE_RE.match(v) for v in text[:50]):
        return "datetime"
    unique_ratio = len(set(map(str, non))) / len(non)
    return "id_or_text" if len(non) > 20 and unique_ratio > 0.95 else "categorical"

def profile(name, values):
    non = [v for v in values if not is_null(v)]
    kind = infer(values)
    out = {"name": name, "type": kind, "count": len(values),
           "null_rate": round(1 - len(non) / len(values), 4) if values else 0.0}
    if kind == "numeric":
        nums = [float(str(v).replace(",", "")) for v in non]
        finite = [v for v in nums if math.isfinite(v)]
        out.update({"min": min(finite), "max": max(finite),
                    "mean": round(statistics.mean(finite), 4),
                    "median": statistics.median(finite),
                    "stdev": round(statistics.pstdev(finite), 4) if len(finite) > 1 else 0.0})
    elif kind in ("categorical", "id_or_text"):
        counts = Counter(map(str, non))
        out.update({"cardinality": len(counts), "top_values": counts.most_common(10)})
    elif kind == "datetime":
        vals = sorted(map(str, non))
        out.update({"min": vals[0], "max": vals[-1]})
    return out

def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: profile_data.py <csv|tsv|json|xlsx>")
    rows = load_rows(sys.argv[1])
    columns = list(dict.fromkeys(k for row in rows for k in row))
    result = {"row_count": len(rows), "columns": [profile(c, [r.get(c) for r in rows]) for c in columns]}
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("error: %s" % exc, file=sys.stderr)
        raise SystemExit(2)
