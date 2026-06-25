from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from tender_compliance_agent.models import ComplianceClause


def write_reports(clauses: list[ComplianceClause], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "health_check_report.md").write_text(render_markdown(clauses), encoding="utf-8")
    (output_dir / "health_check_report.json").write_text(render_json(clauses), encoding="utf-8")


def render_markdown(clauses: list[ComplianceClause]) -> str:
    counts = Counter(clause.category.value for clause in clauses)
    lines = [
        "# 标书体检报告",
        "",
        "## 总览",
        "",
        f"- 共抽取合规相关条款：{len(clauses)} 条",
    ]

    for category, count in sorted(counts.items()):
        lines.append(f"- {category}: {count} 条")

    lines.extend(["", "## 风险与条款明细", ""])
    for clause in clauses:
        source = clause.source
        location = source.file_path
        if source.line_number is not None:
            location = f"{location}:{source.line_number}"
        lines.extend(
            [
                f"### {clause.category.value} / {clause.risk_level.value}",
                "",
                f"- 原文：{clause.text}",
                f"- 来源：{location}",
                f"- 命中关键词：{', '.join(clause.keywords)}",
                f"- 复核原因：{clause.reason}",
                "",
            ]
        )

    return "\n".join(lines)


def render_json(clauses: list[ComplianceClause]) -> str:
    payload = [
        {
            "category": clause.category.value,
            "text": clause.text,
            "risk_level": clause.risk_level.value,
            "reason": clause.reason,
            "keywords": list(clause.keywords),
            "source": {
                "file_path": clause.source.file_path,
                "line_number": clause.source.line_number,
                "page_number": clause.source.page_number,
                "heading": clause.source.heading,
            },
        }
        for clause in clauses
    ]
    return json.dumps(payload, ensure_ascii=False, indent=2)
