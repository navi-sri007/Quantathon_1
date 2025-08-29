from supabase_conn import supabase
import hashlib
from datetime import datetime
import easyocr
import cv2
import numpy as np


import cv2
import numpy as np

# ----- OCR Reader -----
reader = easyocr.Reader(['en'])  # initialize once

# ---------- User Functions ----------
def insert_user_safe(name, email, profile_photo=None):
    """Insert user if not exists, return user data"""
    result = supabase.table("users").select("*").eq("email", email).execute()
    if result.data:
        return result.data[0]
    new_user = supabase.table("users").insert({
        "name": name,
        "email": email,
        "profile_photo": profile_photo
    }).execute()
    return new_user.data[0]

# ---------- Document Functions ----------
def hash_document(file_bytes):
    """Return SHA256 hash of the document"""
    return hashlib.sha256(file_bytes).hexdigest()

def insert_document_safe(user_id, doc_type, doc_number, file_bytes):
    """Insert document if not exists, else return existing"""
    result = supabase.table("documents").select("*").eq("doc_number", doc_number).execute()
    if result.data:
        return result.data[0]
    doc_hash = hash_document(file_bytes)
    new_doc = supabase.table("documents").insert({
        "user_id": user_id,
        "doc_type": doc_type,
        "doc_number": doc_number,
        "doc_hash": doc_hash,
        "verification_status": "unverified"
    }).execute()
    return new_doc.data[0]

# ---------- Verification ----------
def verify_document(doc_number, file_bytes):
    """Verify document hash and log attempt"""
    doc_hash = hash_document(file_bytes)
    result = supabase.table("documents").select("*").eq("doc_number", doc_number).execute()
    
    if not result.data:
        return False, "Document not found"
    
    stored_doc = result.data[0]
    verified = stored_doc["doc_hash"] == doc_hash
    status = "verified" if verified else "failed"
    
    # Log verification attempt
    supabase.table("verification_logs").insert({
        "doc_id": stored_doc["doc_id"],
        "timestamp": datetime.now().isoformat(),
        "status": status
    }).execute()
    
    # Update document status if verified
    if verified:
        supabase.table("documents").update({
            "verification_status": "verified"
        }).eq("doc_id", stored_doc["doc_id"]).execute()
    
    return verified, status

# ---------- OCR Function ----------
def extract_text_from_document(file_bytes):
    """Extract text from image using EasyOCR"""
    nparr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    result = reader.readtext(img, detail=0)
    return " ".join(result)




def extract_qr_from_document(file_bytes: bytes):
    """Extract QR codes from an image using OpenCV"""
    nparr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    detector = cv2.QRCodeDetector()
    retval, decoded_info, points, _ = detector.detectAndDecodeMulti(img)

    # Return list of decoded QR strings
    return [d for d in decoded_info if d] if retval else []