# Report layout

Use this order:

1. Header: title, scope, source, generated date.
2. Caveat banner when data quality materially limits interpretation.
3. KPI row: two to five defensible headline metrics.
4. Findings: one section per question, with chart, plain-language takeaway, and caveat.
5. Data-quality summary: nulls, duplicates, exclusions, transformations.
6. Detail table: searchable or scrollable when practical.
7. Footer: row count, source, and methodology.

Make the page responsive. Use CSS grid with a one-column fallback below 720px. Keep wide tables inside an overflow container. Support light and dark color tokens with explicit tested values. Do not load remote fonts, scripts, analytics, or images by default.
