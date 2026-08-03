---
name: "data-report"
description: "Portable tabular analysis and offline HTML reporting, paired with dataviz."
---

# Data Report

Create a truthful, accessible, self-contained HTML report from tabular data.

## Dependency

Load the separate `dataviz` skill before planning or rendering charts. If automatic skill discovery is unavailable, read its `SKILL.md` directly. Do not substitute copied vendor-proprietary content.

## Workflow

1. Normalize the input.
   - Accept CSV, TSV, JSON records, XLSX, pasted tables, or exported database query results.
   - Run `python3 scripts/profile_data.py INPUT`.
   - If parsing fails, report the exact unsupported structure instead of guessing.
2. Audit quality.
   - Check nulls, duplicates, mixed types, suspicious identifiers, outliers, and inconsistent categories.
   - Preserve the original file; write derived data separately.
3. Form candidate insights.
   - Prefer comparisons, distributions, trends, relationships, and composition only when supported by the fields.
   - Distinguish observation from interpretation.
   - Never invent missing values, causal claims, or statistical significance.
4. Show a chart plan before rendering.
   - Follow `dataviz`.
   - List each chart's question, fields, form, takeaway, and caveat.
   - Default to 4–8 charts; use fewer when the data has little signal.
5. Render one self-contained HTML file.
   - Follow `references/report-layout.md`.
   - Use inline CSS and SVG by default; no CDN, tracking, or remote requests.
   - Include source, row count, transformations, and material caveats.
   - Include a table representation for accessibility.
6. Verify.
   - Recompute displayed numbers from source data.
   - Check labels, units, legends, keyboard access, light/dark contrast, responsive layout, and overflow.
   - Open or screenshot the report before declaring completion.

## Database boundary

Treat database query results and exports like other tabular input. Do not connect to a live database unless the user explicitly authorizes the connection workflow and provides an approved credential mechanism. Never embed credentials in reports or repository files.

## Output contract

Return the report path, key findings, data-quality caveats, transformations, and material assumptions.

## Compatibility

Use the common Agent Skills folder convention and portable Python. Do not require Claude Code, Codex, Cursor, Gemini CLI, or any proprietary artifact runtime. Agents without automatic discovery can read this file directly.
