# AGENTS.md

## Project Focus

This repository is for the first-stage prototype of **Tender Compliance Agent**:
an intelligent pre-review system for tender documents that generates a
traceable "bid health check report" from real tender files.

The first stage must focus on the user's course/project requirement:

- read real tender documents
- extract key compliance requirements
- identify hard constraints, qualification thresholds, scoring rules, and rejection clauses
- preserve the original source location for every extracted item
- assign risk priority
- generate a report that can be demonstrated on site

Do not expand into a full SaaS platform, account system, billing system, or
collaborative workflow before this first-stage closed loop is reliable.

## First-Stage Goal

Given one or more tender-related files, the system should produce a structured
health check report within minutes. The report must help a bid team answer:

- Which clauses may directly cause bid rejection?
- What qualification gates must be satisfied?
- What technical hard requirements must be covered?
- How are scores and weights distributed?
- Which commercial terms need attention?
- Where is each conclusion found in the original document?

The project is judged by whether it can genuinely run against tender examples,
not by whether it only demonstrates a conceptual AI workflow.

## Input And Output Scope

### Supported Inputs

The first stage should prioritize these formats:

- `.docx`: tender documents, bid notices, procurement documents
- `.pdf`: scanned or exported tender files where text extraction is possible
- `.xlsx`: requirement lists, scoring tables, POC checklists
- `.md` and `.txt`: simplified fixtures and converted examples

### Required Outputs

The system should generate:

- `health_check_report.md`: human-readable bid health check report
- `health_check_report.json`: structured machine-readable result
- optional later output: `.xlsx`, `.docx`, or `.pdf` report exports

## Core Report Sections

Every generated report should move toward this structure:

1. Overall summary
2. High-risk rejection clauses
3. Qualification thresholds
4. Technical hard requirements
5. Scoring rules and scoring opportunities
6. Commercial clauses
7. Source trace list for manual review

Each finding should include:

- category
- risk level
- original text
- source file
- page, line, heading, table, row, column, or cell location when available
- matched keywords or extraction rationale
- suggested human review action

## Scoring Criteria For This Project

The implementation should be optimized for these evaluation points:

- **Real run and completeness**: the demo can process actual tender examples and produce a complete report.
- **Coverage**: key hard constraints and rejection clauses are not missed.
- **Traceability**: every important finding can be traced back to the original text.
- **Risk priority**: rejection clauses and hard requirements are surfaced first.
- **Demo clarity**: a reviewer who has not read the tender can quickly understand "why this bid may fail".

## Engineering Principles

- All product code must be Python unless a future decision is explicitly documented.
- Every meaningful change must be tracked by git.
- Keep the first-stage workflow local-first and reproducible.
- Prefer deterministic parsing and rule extraction before adding AI calls.
- AI calls, when introduced, must sit behind explicit interfaces and must not hide source evidence.
- Preserve source traceability: every extracted requirement or risk should point back to file, page, heading, table, paragraph, row, column, or line when available.
- Never silently discard source content. If parsing fails, capture an error record and continue.
- Avoid mixing parsing, extraction, risk scoring, and reporting in the same module.
- Keep modules small, typed, and testable.

## Suggested Architecture

```text
src/tender_compliance_agent/
  cli.py              Command-line entry point
  config.py           Runtime settings
  models.py           Domain dataclasses / schemas
  parsers/            PDF, DOCX, XLSX, Markdown, plain text parsers
  extraction/         Clause and requirement extraction
  review/             Risk grading and coverage checks
  reports/            Markdown, JSON, Excel, Word/PDF report generation
  llm/                Optional AI provider interfaces and prompt templates
tests/
  unit and integration tests
examples/
  sample tender inputs and expected outputs
docs/
  first-stage plan, product spec, technical notes
```

## Agent Roles

### Product Agent

- Keeps the project focused on the first-stage report generator.
- Converts course/project requirements into acceptance criteria.
- Rejects scope creep that does not improve the demo report.
- Ensures the demo answers real bid-team questions, not generic document QA.

### Parser Agent

- Implements document ingestion for PDF, DOCX, XLSX, Markdown, and text.
- Extracts paragraphs, tables, headings, pages, rows, columns, and cells when possible.
- Emits normalized document chunks for downstream extraction.
- Records parse warnings instead of dropping unreadable content silently.

### Extraction Agent

- Finds qualification gates, technical parameters, scoring methods, commercial terms, delivery requirements, and rejection clauses.
- Uses keyword and pattern rules first for high-confidence categories.
- Produces structured findings with category, confidence, source trace, and rationale.
- Keeps extracted text close to the original wording for auditability.

### Risk Agent

- Assigns risk levels:
  - `critical`: rejection, invalid bid, bid denial, non-acceptance
  - `high`: qualification gates and mandatory technical hard requirements
  - `medium`: scoring items, important commercial terms, delivery or service commitments
  - `low`: reminders and weak signals for manual review
- Places critical and high-risk findings at the front of reports.
- Explains why the risk level was assigned.

### Report Agent

- Generates a "bid health check report" readable by non-technical bid teams.
- Includes summary counts, high-risk list, grouped findings, and source evidence.
- Makes the report suitable for an on-site demonstration.
- Avoids unsupported conclusions; each conclusion should cite original text.

### QA Agent

- Adds regression tests for parsers, extraction rules, risk grading, and report rendering.
- Uses small fixture documents and at least one realistic demo case.
- Checks that outputs are stable, explainable, and safe to share.
- Verifies that generated reports contain source traces for important findings.

## Clause Categories

Use these first-stage categories unless a change is documented:

- `qualification`: qualifications, certificates, licenses, business credentials, performance cases
- `technical`: technical parameters, mandatory functions, performance indicators, acceptance requirements
- `scoring`: scoring rules, weights, points, evaluation methods, bonus opportunities
- `rejection`: bid rejection, invalid bid, denial, non-acceptance, disqualification clauses
- `commercial`: payment, delivery, warranty, service period, contract, quotation terms
- `other`: findings that need manual review but do not fit the above categories

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
- Push completed work to GitHub after local verification when credentials are available.

## First-Stage MVP Scope

The first milestone should provide:

- local CLI entry point
- input folder scanning
- Markdown and plain text ingestion
- initial DOCX, PDF, and XLSX ingestion
- normalized document chunk schema with source locations
- rule-based extraction for qualification, technical, scoring, rejection, and commercial clauses
- risk grading with critical/high/medium/low levels
- Markdown and JSON health check report output
- demo sample package
- unit tests for extraction, risk grading, and report rendering

Out of scope for the first milestone:

- user login or multi-tenant SaaS
- payment or billing
- collaborative editing
- production OCR pipeline for poor-quality scans
- automatic legal conclusions without human review
- full bid-response comparison across many suppliers

## Acceptance Criteria

- A user can run the CLI against a folder of tender materials.
- The system produces `health_check_report.md` and `health_check_report.json`.
- The report contains at least qualification, technical, scoring, rejection, and commercial sections when relevant findings exist.
- Critical rejection clauses are highlighted before lower-risk findings.
- Each important finding includes source file and available location metadata.
- At least one demo case can be run end to end.
- Tests cover the core extraction, risk grading, and report rendering path.

## Safety And Compliance

- Treat all tender and bid files as confidential.
- Never send document content to an external AI provider unless the user has configured and approved that provider.
- Mark AI-generated interpretations as review suggestions, not final legal advice.
- Prefer source quotes and evidence over unsupported conclusions.
- Keep generated reports out of git unless they are synthetic demo outputs.
