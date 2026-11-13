# DocuGuard AI — Enterprise Document Intelligence & Vendor Compliance Risk Engine

## Overview
An automated FastAPI microservice that extracts structured invoice data from uploaded PDFs, retrieves matching clauses from internal procurement policies (data/company_policy.txt), and enforces schema-level compliance validation to flag vendor risks.

## Key Features (MVP)
- **PDF Document Extraction:** Automated text parsing and regex field extraction via pypdf (PdfReader).
- **Policy Rule Retrieval:** Keyword-scored retrieval engine matching invoice attributes against internal compliance rules (data/company_policy.txt).
- **Strict Schema Validation:** Type-safe contract and invoice enforcement using Pydantic (InvoiceChecklist) exposed over a REST API (FastAPI).

## Demo Output
![DocuGuard AI Demo 1](docuguard_demo_1.png)
![DocuGuard AI Demo 2](docuguard_demo_2.png)
![DocuGuard AI Demo 3](docuguard_demo_3.png)
![DocuGuard AI Demo 4](docuguard_demo_4.png)

## Tech Stack
- **Backend & API:** Python, FastAPI, Uvicorn
- **Document Parsing & Validation:** PyPDF, Pydantic, Regex
- **Policy Store:** Structured Plaintext Rule Corpus (data/company_policy.txt)

## Quickstart
```bash
pip install fastapi uvicorn pypdf pydantic python-multipart
uvicorn main:app --reload
```
Open http://127.0.0.1:8000/docs to test PDF invoice compliance checks interactively.
