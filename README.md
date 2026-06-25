# Tender Compliance Agent

投标文件合规预审智能体，用 Python 构建。

目标：上传招标文件、投标文件、需求清单或证明材料后，自动抽取资质门槛、技术硬指标、商务条款、评分规则、废标项，并生成可追溯的标书体检报告。

## MVP

- 本地 CLI
- Markdown / text 文件解析
- 合规条款初步抽取
- 风险分级
- Markdown / JSON 报告输出
- pytest 测试

## Quick Start

```bash
python -m tender_compliance_agent --input examples --output reports
```

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

## Repository Rules

See [AGENTS.md](AGENTS.md) for product direction, agent roles, engineering standards, and git workflow.
