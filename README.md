# Candidate Intelligence Pipeline

> **A modular multi-source candidate transformation pipeline that consolidates fragmented candidate information into a unified, validated, and explainable profile.**

## Overview

Candidate information rarely exists in a single place. Recruiter spreadsheets, resumes, and developer profiles each provide different pieces of information, but they often contain inconsistencies, duplicate records, conflicting values, and missing fields.

This project approaches candidate transformation as a **data integration problem** rather than a simple parsing task. It integrates information from multiple heterogeneous sources into a canonical candidate profile through a modular ETL pipeline that performs extraction, normalization, identity resolution, configurable merging, validation, confidence scoring, and provenance tracking.

The objective is not just to transform data, but to produce candidate profiles that are **consistent, explainable, maintainable, and ready for downstream systems**.


## Key Features

* Multi-source candidate ingestion

  * Recruiter CSV
  * Resume
  * GitHub Profile
* Structured information extraction
* Data normalization and standardization
* Identity resolution across multiple sources
* Configurable merge strategy
* Field-level provenance tracking
* Explainable merge decisions
* Confidence scoring
* Candidate validation
* Configuration-driven output projection
* Batch processing support


## Pipeline

```text
                    Input Sources
    ┌────────────┬────────────┬────────────┐
    │Recruiter   │   Resume   │  GitHub    │
    │    CSV     │            │  Profile   │
    └─────┬──────┴─────┬──────┴─────┬──────┘
          │            │            │
          └────────────┴────────────┘
                       │
                       ▼
                 Source Readers
                       │
                       ▼
                  Information
                   Extraction
                       │
                       ▼
                 Data Normalization
                       │
                       ▼
               Identity Resolution
                       │
                       ▼
                  Intelligent Merge
                       │
                       ▼
                Confidence Scoring
                       │
                       ▼
                 Data Validation
                       │
                       ▼
              Configurable Projection
                       │
                       ▼
         Canonical Candidate Profile (JSON)
```

## Engineering Decisions

The project is intentionally designed as a modular pipeline rather than a collection of parsing scripts.

The primary challenge is **not extracting candidate information—it is determining how fragmented, conflicting, and incomplete data from multiple sources should be reconciled into a single trustworthy representation.**

To address this, the pipeline separates each responsibility into an independent processing stage while keeping business rules configurable and transformation decisions explainable.

Some of the key architectural decisions include:

* Independent readers for each data source to simplify future integrations.
* A canonical candidate model shared across the entire pipeline.
* Data normalization before merging to improve consistency across heterogeneous inputs.
* Identity resolution to determine whether records represent the same candidate.
* Configuration-driven merge rules and output projection instead of hardcoded business logic.
* Field-level provenance tracking to preserve the origin of every exported attribute.
* Confidence scoring based on source agreement and data completeness.
* Validation before export to improve downstream data quality.

This architecture emphasizes **separation of concerns, maintainability, explainability, and extensibility**, principles commonly used when designing production data engineering systems.


## Technologies

* Python 3
* Object-Oriented Programming (OOP)
* Dataclasses
* CSV & JSON Processing
* Regular Expressions
* Logging



## Example Output

```json
{
  "candidate_id": "CAND-001",
  "full_name": "Pragna",
  "email": "pragna@gmail.com",
  "phone": "+919876543210",
  "skills": [
    "Python",
    "SQL",
    "Java"
  ],
  "education": [
    "B.E. Computer Science"
  ],
  "experience": [
    "Software Engineering Intern"
  ],
  "confidence": 0.95,
  "sources": {
    "email": ["csv", "resume"],
    "phone": ["csv"],
    "skills": ["resume", "github"],
    "education": ["resume"]
  }
}
```

## Future Improvements

* LinkedIn and ATS integrations
* OCR-based resume parsing
* REST API
* Docker deployment
* Automated testing
* AI-assisted candidate enrichment


## Repository Contents

* **README.md** – Project overview and setup
* **DESIGN.md** – Architecture and design decisions
* **src/** – Pipeline implementation
* **config/** – Merge and projection configuration
* **tests/** – Unit tests
* **output/** – Generated pipeline outputs

