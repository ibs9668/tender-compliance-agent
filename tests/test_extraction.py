from tender_compliance_agent.extraction import extract_clauses
from tender_compliance_agent.models import ClauseCategory, DocumentChunk, SourceLocation


def test_extracts_rejection_clause_as_critical() -> None:
    chunks = [
        DocumentChunk(
            text="未按要求提交资质证明材料的，按无效投标处理。",
            source=SourceLocation(file_path="sample.md", line_number=3),
        )
    ]

    clauses = extract_clauses(chunks)

    assert len(clauses) == 1
    assert clauses[0].category == ClauseCategory.REJECTION
    assert clauses[0].risk_level.value == "critical"


def test_ignores_unrelated_text() -> None:
    chunks = [
        DocumentChunk(
            text="欢迎参加本项目。",
            source=SourceLocation(file_path="sample.md", line_number=1),
        )
    ]

    assert extract_clauses(chunks) == []
