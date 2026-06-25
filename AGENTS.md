# AGENTS.md

## Product Mission

Build a Python product named **Tender Compliance Agent**: an intelligent pre-review system for tender and bidding documents. Given hundreds of pages of tender files, the system should quickly produce a structured "bid health check report" that extracts and traces:

- qualification thresholds
- technical hard requirements
- commercial clauses
- scoring rules and weights
- disqualification / rejection clauses
- source locations in the original documents
- bidder risk warnings and priority

The product must help government-enterprise customers, system integrators, and consulting teams reduce missed clauses, reduce bid rejection risk, and speed up response preparation.

## Core User Flow

1. Upload tender documents, bid documents, requirements lists, POC checklists, and supporting spreadsheets.
2. Parse document text, tables, headings, attachments, and page references.
3. Extract compliance-related clauses and normalize them into structured records.
4. Compare tender requirements against bid response materials.
5. Generate a traceable report that shows coverage, gaps, risks, evidence, and source locations.
6. Export results as Markdown, JSON, Excel, and eventually Word/PDF reports.

## Engineering Principles

- All product code must be Python unless a future decision is explicitly documented.
- Every meaningful change must be tracked by git.
- Keep behavior deterministic where possible; AI calls must be wrapped behind explicit interfaces.
- Preserve source traceability: every extracted requirement or risk should point back to file, page, heading, table, paragraph, or cell when available.
- Prefer small, testable modules over large scripts.
- Avoid mixing parsing, extraction, scoring, and reporting in the same module.
- Never silently discard source content. If parsing fails, capture an error record and continue.

## Suggested Architecture

```text
src/tender_compliance_agent/
  cli.py              Command-line entry point
  config.py           Runtime settings
  models.py           Domain dataclasses / schemas
  parsers/            PDF, DOCX, XLSX, Markdown, plain text parsers
  extraction/         Requirement and clause extraction
  review/             Coverage, risk, and compliance scoring
  reports/            Markdown, JSON, Excel, Word/PDF report generation
  storage/            Local artifacts and future database adapters
  llm/                AI provider interfaces and prompt templates
tests/
  unit and integration tests
examples/
  sample inputs and expected outputs
docs/
  product and technical notes
```

## Agent Roles

### Product Agent

- Clarifies workflows for procurement, bidding, consulting, and integration teams.
- Converts business needs into concrete acceptance criteria.
- Keeps the first usable version focused on one path: upload tender files and generate a structured pre-review report.

### Parser Agent

- Implements document ingestion for PDF, DOCX, XLSX, Markdown, and text.
- Preserves layout hints such as page number, heading, table position, and cell reference.
- Emits normalized document chunks for downstream extraction.

### Extraction Agent

- Finds qualification gates, technical parameters, scoring methods, commercial terms, delivery requirements, and rejection clauses.
- Produces structured records with confidence, source trace, and rationale.
- Uses rule-based extraction first where reliable; uses LLM extraction only through controlled interfaces.

### Review Agent

- Compares tender requirements against bid response materials.
- Flags missing evidence, weak responses, conflicting statements, and hard rejection risks.
- Assigns risk severity and suggests remediation priorities.

### Report Agent

- Generates a "bid health check report" that is readable by non-technical bid teams.
- Includes summary, key risks, requirement coverage, rejection clauses, scoring opportunities, and source evidence.
- Keeps every conclusion traceable to original text.

### QA Agent

- Adds regression tests for parsers, extraction rules, review logic, and report rendering.
- Uses small fixture documents where possible.
- Checks that outputs are stable, explainable, and safe to share.

## Python Standards

- Target Python 3.11+.
- Use type hints for public functions.
- Prefer dataclasses or Pydantic-style schemas for structured domain objects.
- Keep CLI behavior thin; business logic belongs in importable modules.
- Use `pytest` for tests.
- Use `ruff` for linting and formatting when configured.
- Do not commit secrets, uploaded customer files, model API keys, or generated private reports.

## Git Workflow

- Work on feature branches named `codex/<short-description>` unless the user requests otherwise.
- Keep commits focused and descriptive.
- Before committing, run the relevant tests or explain why they were not run.
- Do not rewrite or discard user changes without explicit instruction.

## MVP Scope

The first milestone should provide:

- local CLI entry point
- document manifest loading
- plain text / Markdown ingestion
- initial requirement schema
- simple rule-based extraction for qualification, scoring, rejection, and technical requirement keywords
- Markdown and JSON health check report output
- unit tests for extraction and report generation

Out of scope for the first milestone:

- multi-tenant SaaS accounts
- payment / billing
- collaborative editing
- production OCR pipeline
- automatic legal conclusions without human review

## Acceptance Criteria

- A user can point the CLI at a folder of tender materials.
- The system produces a structured report with extracted clauses.
- Each extracted clause includes source file and available location metadata.
- Disqualification clauses and hard requirements are clearly highlighted.
- Tests cover the core extraction and report rendering path.

## Safety And Compliance

- Treat all tender and bid files as confidential.
- Never send document content to an external AI provider unless the user has configured and approved that provider.
- Mark AI-generated interpretations as review suggestions, not final legal advice.
- Prefer source quotes and evidence over unsupported conclusions.
