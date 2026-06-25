from __future__ import annotations

from collections.abc import Iterable

from tender_compliance_agent.models import (
    ClauseCategory,
    ComplianceClause,
    DocumentChunk,
    RiskLevel,
)


KEYWORD_RULES: dict[ClauseCategory, tuple[str, ...]] = {
    ClauseCategory.REJECTION: ("废标", "无效投标", "否决投标", "不予受理", "按无效处理"),
    ClauseCategory.QUALIFICATION: ("资质", "资格", "业绩", "证书", "许可", "认证"),
    ClauseCategory.SCORING: ("评分", "分值", "得分", "权重", "评审标准"),
    ClauseCategory.TECHNICAL: ("技术参数", "技术指标", "功能要求", "性能", "验收"),
    ClauseCategory.COMMERCIAL: ("付款", "交付", "质保", "合同", "报价", "服务期"),
}


def extract_clauses(chunks: Iterable[DocumentChunk]) -> list[ComplianceClause]:
    clauses: list[ComplianceClause] = []
    for chunk in chunks:
        text = chunk.text.strip()
        if not text:
            continue

        for category, keywords in KEYWORD_RULES.items():
            matched = tuple(keyword for keyword in keywords if keyword in text)
            if not matched:
                continue

            clauses.append(
                ComplianceClause(
                    category=category,
                    text=text,
                    source=chunk.source,
                    risk_level=_risk_level_for(category),
                    reason=_reason_for(category),
                    keywords=matched,
                )
            )
            break

    return clauses


def _risk_level_for(category: ClauseCategory) -> RiskLevel:
    if category == ClauseCategory.REJECTION:
        return RiskLevel.CRITICAL
    if category in {ClauseCategory.QUALIFICATION, ClauseCategory.TECHNICAL}:
        return RiskLevel.HIGH
    if category == ClauseCategory.SCORING:
        return RiskLevel.MEDIUM
    return RiskLevel.LOW


def _reason_for(category: ClauseCategory) -> str:
    reasons = {
        ClauseCategory.REJECTION: "可能直接导致废标或投标无效，需优先核对。",
        ClauseCategory.QUALIFICATION: "涉及投标准入门槛，需确认资质与证明材料齐全。",
        ClauseCategory.TECHNICAL: "涉及技术硬指标或验收要求，需确认响应与证据覆盖。",
        ClauseCategory.SCORING: "涉及评分机会或扣分风险，需用于响应优化。",
        ClauseCategory.COMMERCIAL: "涉及商务承诺，需确认报价、交付、质保或合同响应。",
    }
    return reasons.get(category, "需要人工复核。")
