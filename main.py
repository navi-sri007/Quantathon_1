
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from db_operations import extract_qr_from_document
from db_operations import (
    insert_user_safe,
    insert_document_safe,
    verify_document,
    extract_text_from_document
)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict to ["http://127.0.0.1:8000"] if you want
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Test Inserts ----------
user = insert_user_safe("Naveena", "naveena@example.com", "profile1.png")
print("User:", user)

doc_content = b"example content of Aadhaar document"
document = insert_document_safe(user_id=user["user_id"], doc_type="Aadhaar",
                               doc_number="123456789012", file_bytes=doc_content)
print("Document:", document)

# ---------- Verification Endpoint ----------
@app.post("/verify_document/{doc_number}")
async def verify(doc_number: str, file: UploadFile):
    file_bytes = await file.read()
    verified, status = verify_document(doc_number, file_bytes)
    return {"verified": verified, "status": status}

# ---------- OCR Endpoint ----------
@app.post("/ocr_document/")
async def ocr_document(file: UploadFile):
    file_bytes = await file.read()
    text = extract_text_from_document(file_bytes)
    return {"extracted_text": text}

@app.post("/upload_qr/")
async def upload_qr(file: UploadFile = File(...)):
    file_bytes = await file.read()
    qr_data = extract_qr_from_document(file_bytes)
    return {"qr_data": qr_data}


