# DataVizKit

Two vendor-neutral Agent Skills for turning tabular data into clear, accessible visualizations and self-contained HTML reports.

## Included skills

- **`dataviz`** — chart selection, color roles, accessibility, interaction, and visualization anti-patterns.
- **`data-report`** — profiling and reporting for CSV, TSV, JSON records, basic XLSX workbooks, pasted tables, and exported database query results.

The skills use the portable `SKILL.md` convention and do not require a proprietary artifact runtime, CDN, paid API, or external analytics service.

## Compatibility

They can be used by Claude Code, Codex, Cursor, Gemini CLI, OpenClaw, and other coding agents that can read Markdown and run Python 3. Automatic skill discovery differs by product; when it is unavailable, point the agent directly at the relevant `SKILL.md` file.

## Install

Copy both folders into your agent's skill directory:

```bash
cp -R skills/dataviz /path/to/agent/skills/
cp -R skills/data-report /path/to/agent/skills/
```

Or keep this repository inside a project and ask the agent to follow:

```text
skills/data-report/SKILL.md
```

`data-report` uses `dataviz` when planning or rendering charts, so installing both is recommended.

## Usage

Example requests:

- “Analyze this CSV, show me a chart plan, then create an offline HTML report.”
- “Profile this XLSX workbook and identify the most defensible insights.”
- “Turn these exported SQL query results into an accessible dashboard.”
- “为这份表格选择合适的图表，并生成离线 HTML 报告。”

Run the profiler directly:

```bash
python3 skills/data-report/scripts/profile_data.py path/to/data.csv
```

The profiler uses only the Python standard library. XLSX support targets ordinary cell-based workbooks and reads the first worksheet; macros, formulas requiring recalculation, charts, pivot caches, encrypted files, and legacy `.xls` files are outside its scope.

## Test

```bash
python3 -m unittest discover -s tests -v
```

The tests cover CSV, TSV, JSON, XLSX, malformed input, Python compilation, and valid Skill frontmatter.

## Database safety

The reporting skill accepts database query exports or result tables. It does not automatically connect to live databases or store credentials. Any live connection should be separately authorized and use the host agent's approved secret mechanism.

## License

MIT. This rewritten version is original and does not include the previous Anthropic `dataviz` copy.
