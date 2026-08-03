---
name: "dataviz"
description: "Vendor-neutral chart and dashboard design for accurate, accessible visualization."
---

# Data Visualization

Design visualizations that answer a question without distorting the data.

## Workflow

1. State the analytical question and intended audience.
2. Identify field roles: category, numeric measure, time, geography, identifier, or free text.
3. Choose the simplest form that supports the comparison. Read `references/chart-selection.md`.
4. Assign color by meaning, not decoration. Read `references/color-accessibility.md`.
5. Specify title, takeaway, axes, units, legend, direct labels, tooltip, and table fallback.
6. Render in the user's chosen medium using local or approved dependencies.
7. Verify values against source data and inspect the actual output for overlap, clipping, overflow, contrast, and misleading scales.
8. Check `references/anti-patterns.md` before delivery.

## Invariants

- Never use a dual y-axis.
- Never use 3D perspective for quantitative comparison.
- Do not truncate a quantitative baseline when it materially exaggerates differences.
- Keep entity colors stable under sorting and filtering.
- Do not use color as the only carrier of meaning.
- Do not infer causation from correlation.
- Prefer fewer purposeful charts over charting every available field.
- Include source, units, and material caveats.
- For interactive output, ensure essential information is available without hover.
- For multiple series, provide a legend or direct labels; provide both when complexity requires it.

## Output contract

For each proposed chart, provide:

- question;
- fields and transformations;
- chart form;
- encoding;
- one-sentence takeaway;
- caveat or uncertainty;
- accessibility treatment.

## Compatibility

This skill is vendor-neutral. It applies to HTML/SVG, matplotlib, Plotly, D3, Vega-Lite, Recharts, spreadsheet charts, generated images, and other chart systems. Use the toolchain already available to the agent; do not require a proprietary runtime.
