# System Design

## Overview

The Candidate Intelligence Pipeline transforms fragmented candidate information collected from multiple independent sources into a unified canonical candidate profile.

Instead of treating each input independently, the pipeline models candidate transformation as a data integration problem where heterogeneous information must be standardized, reconciled, validated, and exported in a consistent format.

---

# High-Level Architecture

```
Recruiter CSV
Resume
GitHub
      │
      ▼
Readers
      ▼
Extraction
      ▼
Normalization
      ▼
Identity Resolution
      ▼
Merge Engine
      ▼
Confidence Scoring
      ▼
Validation
      ▼
Projection
      ▼
Export
```

---

# Design Goals

The project was designed around four principles:

- Separation of Concerns
- Explainability
- Configurability
- Extensibility

Each processing stage performs one responsibility before passing the candidate to the next stage.

---

# Processing Stages

## Readers

Each source has an independent reader responsible only for loading data.

Current readers:

- Recruiter CSV
- Resume
- GitHub

Adding another source requires creating only another reader.

---

## Extraction

The extractor converts raw resume text into structured candidate attributes.

Examples include:

- Name
- Email
- Phone
- Skills
- Education
- Experience

---

## Normalization

Candidate information from different systems often follows different formats.

Normalization standardizes values before they are compared or merged.

Examples:

```
python
PYTHON
Python
```

↓

```
Python
```

---

## Identity Resolution

Multiple sources may describe the same candidate.

Identity resolution compares

- Email
- Phone
- Name

to determine whether records should be merged.

---

## Merge Engine

The merge engine combines information from all available sources.

Merge decisions follow configurable priority rules rather than hardcoded logic.

This keeps business rules separate from implementation.

---

## Confidence Scoring

Not every candidate profile has the same reliability.

Confidence is estimated using:

- Source agreement
- Data completeness

Profiles assembled from multiple agreeing sources receive higher confidence scores.

---

## Validation

Validation checks candidate quality before export.

Examples include:

- Missing required fields
- Invalid email
- Duplicate skills

---

## Projection

The projection layer converts the internal candidate model into the final exported JSON using configuration rather than hardcoded fields.

---

# Engineering Decisions

Several architectural decisions were made to improve maintainability and extensibility.

### Modular Pipeline

Each processing stage has one responsibility.

This simplifies testing, debugging, and future enhancements.

---

### Canonical Candidate Model

All sources are transformed into one common representation before further processing.

This reduces complexity in downstream stages.

---

### Configuration over Hardcoding

Merge priorities and output fields are stored in configuration files.

This allows behavior to change without modifying source code.

---

### Provenance Tracking

Every exported attribute records its originating source.

This improves transparency and debugging.

---

### Explainable Transformations

Merge decisions and confidence scores make the transformation process understandable instead of acting as a black box.

---

# Future Improvements

Possible future enhancements include:

- LinkedIn integration
- ATS connectors
- OCR resume parsing
- REST API
- Docker deployment
- LLM-assisted resume understanding
- Vector search
