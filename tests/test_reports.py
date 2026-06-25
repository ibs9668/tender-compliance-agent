from tender_compliance_agent.extraction import extract_clauses
from tender_compliance_agent.models import DocumentChunk, SourceLocation
from tender_compliance_agent.reports import render_json, render_markdown


def test_report_contains_source_and_clause_text() -> None:
    clauses = extract_clauses(
        [
            DocumentChunk(
                text="评审标准中技术方案占 40 分。",
                source=SourceLocation(file_path="sample.md", line_number=5),
            )
        ]
    )

    markdown = render_markdown(clauses)
    json_report = render_json(clauses)

    assert "标书体检报告" in markdown
    assert "sample.md:5" in markdown
    assert "评审标准" in json_report
