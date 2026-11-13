from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel, Field, ValidationError
from pypdf import PdfReader
import io, re

app = FastAPI(title="DocuGuard AI")

with open("data/company_policy.txt", "r") as f:
    policy_rules = [line.strip() for line in f.readlines() if line.strip()]

def retrieve_matching_rules(query_words: list[str]) -> list[str]:
    scored_rules = []
    for rule in policy_rules:
        score = sum(1 for word in query_words if word.lower() in rule.lower())
        scored_rules.append((score, rule))
    scored_rules.sort(reverse=True)
    return [rule for score, rule in scored_rules[:2]]

class InvoiceChecklist(BaseModel):
    vendor_name: str
    po_number: str
    amount: float = Field(gt=0)
    payment_terms: str

def read_invoice_details(text: str) -> dict:
    vendor = re.search(r"Vendor:\s*(.+)", text)
    po = re.search(r"PO Number:\s*(.+)", text)
    amount = re.search(r"Amount:\s*\$?([\d,]+\.?\d*)", text)
    terms = re.search(r"Terms:\s*(.+)", text)
    return {
        "vendor_name": vendor.group(1).strip() if vendor else None,
        "po_number": po.group(1).strip() if po else None,
        "amount": float(amount.group(1).replace(",", "")) if amount else 0.0,
        "payment_terms": terms.group(1).strip() if terms else None,
    }

@app.post("/check-invoice/")
async def check_invoice(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    reader = PdfReader(io.BytesIO(pdf_bytes))
    raw_text = "\n".join([page.extract_text() for page in reader.pages])

    extracted_data = read_invoice_details(raw_text)
    try:
        clean_invoice = InvoiceChecklist(**extracted_data)
    except ValidationError as e:
        return {"status": "REJECTED - MISSING INFO", "errors": e.errors()}

    matched_rules = retrieve_matching_rules(["amount", "5,000", clean_invoice.payment_terms, "terms"])

    warnings = []
    if clean_invoice.amount > 5000:
        warnings.append("Amount is over $5,000! Needs VP approval.")
    if clean_invoice.payment_terms.lower() != "net-30":
        warnings.append(f"Terms say '{clean_invoice.payment_terms}', but policy requires Net-30.")

    return {
        "final_decision": "FLAGGED FOR REVIEW" if warnings else "APPROVED",
        "extracted_info": clean_invoice.model_dump(),
        "warnings": warnings,
        "rules_checked": matched_rules
    }