
from uuid import uuid4
from pathlib import Path

import fitz

from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

from app.services.pdf_service import extract_pdf_text
from app.services.chunking_service import split_text_into_chunks
from app.services.embedding_service import generate_embeddings
from app.services.vector_store import store_embeddings


documents_bp = Blueprint("documents", __name__)

ALLOWED_EXTENSION = {".pdf"}


@documents_bp.route("/documents/upload", methods=["POST"])
def upload_document():

    # 1. Check whether file exists
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    # 2. Check filename
    if not file.filename:
        return jsonify({"error": "No file selected"}), 400

    original_name = secure_filename(file.filename)

    # 3. Validate extension
    if Path(original_name).suffix.lower() not in ALLOWED_EXTENSION:
        return jsonify({"error": "Only PDF files are allowed"}), 400

    # 4. Validate PDF signature
    signature = file.stream.read(5)
    file.stream.seek(0)

    if signature != b"%PDF-":
        return jsonify({"error": "Invalid PDF file"}), 400

    # 5. Generate unique filename
    unique_name = f"{uuid4().hex}.pdf"

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    file_path = upload_folder / unique_name

    # 6. Save PDF
    file.save(str(file_path))

    try:
        # 7. Extract PDF text
        pages = extract_pdf_text(file_path)

        total_text = sum(
            len(page["content"]) for page in pages
        )

        print("TOTAL PAGES:", len(pages))
        print("TOTAL CHARACTERS:", total_text)

        # 8. Reject empty or scanned PDFs
        if total_text == 0:
            file_path.unlink(missing_ok=True)

            return jsonify({
                "error": "No readable text found. Scanned PDF OCR is not supported yet."
            }), 422

        # 9. Split text into chunks
        chunks = split_text_into_chunks(pages)

        print("TOTAL CHUNKS:", len(chunks))

        # 10. Generate embeddings
        embedded_chunks = generate_embeddings(chunks)

        print("EMBEDDED CHUNKS:", len(embedded_chunks))

        # 11. Store embeddings in ChromaDB
        document_id = Path(unique_name).stem

        print("BEFORE CHROMA STORAGE")
        print("DOCUMENT ID:", document_id)

        stored_count = store_embeddings(
            document_id,
            embedded_chunks
        )

        print("AFTER CHROMA STORAGE:", stored_count)

        # 12. Return response
        return jsonify({
            "status": "success",
            "message": "PDF uploaded and processed successfully",
            "document": {
                "document_id": document_id,
                "original_name": original_name,
                "stored_name": unique_name,
                "total_pages": len(pages),
                "total_characters": total_text,
                "total_chunks": len(chunks),
                "total_stored_chunks": stored_count,
                "pages": pages,
                "chunks": chunks
            }
        }), 201

    except (fitz.FileDataError, ValueError):

        file_path.unlink(missing_ok=True)

        return jsonify({
            "error": "Unable to read this PDF"
        }), 400

    except Exception:

        file_path.unlink(missing_ok=True)

        current_app.logger.exception(
            "PDF processing failed"
        )

        return jsonify({
            "error": "PDF processing failed"
        }), 500
