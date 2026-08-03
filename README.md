# DataVizKit

Two vendor-neutral Agent Skills for turning tabular data into clear, accessible visualizations and self-contained HTML reports.

[English](README.md) | [简体中文](README.zh-CN.md)

![DataVizKit Titanic report example](docs/screenshots/titanic-report.png)

## Video demo

See DataVizKit turn CSV, XLSX, and JSON data into polished reports in 20 seconds.

[![Watch the DataVizKit 20-second demo](docs/screenshots/titanic-report.png)](docs/media/datavizkit-promo.mp4)

▶ **[Watch or download the MP4](docs/media/datavizkit-promo.mp4)**

## Example output

DataVizKit profiles the source data, selects defensible findings, and produces responsive, self-contained HTML reports with KPI cards, charts, caveats, and detail tables.

![DataVizKit Gapminder report example](docs/screenshots/gapminder-report.png)

## Included skills

- **`dataviz`** — chart selection, color roles, accessibility, interaction, and visualization anti-patterns.
- **`data-report`** — profiling and reporting for CSV, TSV, JSON records, basic XLSX workbooks, pasted tables, and exported database query results.

The skills use the portable `SKILL.md` convention and do not require a proprietary artifact runtime, CDN, paid API, or external analytics service.

## Compatibility

They can be used by Claude Code, Codex, Cursor, Gemini CLI, OpenClaw, and other coding agents that can read Markdown and run Python 3. Automatic skill discovery differs by product; when it is unavailable, point the agent directly at the relevant `SKILL.md` file.

## Install with your AI agent

Paste this prompt into Claude Code, Codex, Cursor, Gemini CLI, OpenClaw, or another coding agent:

```text
Install the DataVizKit Agent Skills from
https://github.com/CodingPro777/dataviz-kit.

Detect the correct skills directory for this agent, clone or download the
repository, install both skills/dataviz and skills/data-report, preserve their
directory structure, and verify that both SKILL.md files are discoverable.
Do not install paid services or unrelated dependencies. Tell me the final
installation paths and the result of the verification.
```

The agent should detect its own convention and install both skills in the appropriate global or project-level skills directory. Restart or reload the agent if its skill index is only refreshed at startup.

### Manual fallback

If your agent cannot install skills itself, clone the repository and copy both folders into its documented skills directory:

```bash
git clone https://github.com/CodingPro777/dataviz-kit.git
cd dataviz-kit
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

MIT License. See [LICENSE](LICENSE).
