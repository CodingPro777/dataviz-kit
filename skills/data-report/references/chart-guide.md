# Chart guide

Choose a form from the analytical question.

- Exact headline: KPI or stat tile.
- Category comparison: sorted horizontal bars.
- Distribution: histogram, box plot, or dot plot.
- Change over time: line chart with a real time scale.
- Relationship between two numeric fields: scatter plot; add a trend only when justified.
- Part-to-whole: stacked bar when totals and components matter. Avoid pie charts when precise comparison matters.
- Many categories: show a defensible top-N plus Other, or use small multiples.
- Different units: separate panels or normalize to an index. Never use dual y-axes.

Use color by role:

- identity: a fixed categorical assignment that remains stable under filtering;
- magnitude: one sequential hue from light to dark;
- polarity: two hues around a neutral midpoint;
- status: reserved semantic colors plus labels or icons.

Accessibility rules:

- Never encode meaning with color alone.
- Label axes and units.
- Use legends for multiple series and direct labels when space permits.
- Keep text contrast at least 4.5:1 for normal text and mark contrast at least 3:1 where practical.
- Make pointer targets at least 24 CSS pixels and support keyboard focus for interactive marks.
- Include a table representation.
- Respect reduced motion and do not require hover to reveal essential values.

Avoid 3D charts, truncated quantitative axes that exaggerate differences, rainbow scales, decorative gradients, and labels on every point.
