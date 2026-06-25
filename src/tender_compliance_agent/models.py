from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ClauseCategory(StrEnum):
    QUALIFICATION = "qualification"
    TECHNICAL = "technical"
    COMMERCIAL = "commercial"
    SCORING = "scoring"
    REJECTION = "rejection"
    OTHER = "other"


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class SourceLocation:
    file_path: str
    line_number: int | None = None
    page_number: int | None = None
    heading: str | None = None


@dataclass(frozen=True)
class DocumentChunk:
    text: str
    source: SourceLocation


@dataclass(frozen=True)
class ComplianceClause:
    category: ClauseCategory
    text: str
    source: SourceLocation
    risk_level: RiskLevel
    reason: str
    keywords: tuple[str, ...] = field(default_factory=tuple)
