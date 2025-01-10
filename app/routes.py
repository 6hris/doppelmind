from fastapi import APIRouter, HTTPException
from app.models import ContextInput, QuestionInput
from app.services import preprocess_context_data, generate_response
from app.vector_store import vector_store

router = APIRouter()

@router.post("/upload_context")
def upload_context(data: ContextInput):
    try:
        processed_docs = preprocess_context_data(data.text, data.user_id)
        vector_store.add_documents(processed_docs)
        return {"status": "Context uploaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask_question")
def ask_question(data: QuestionInput):
    try:
        answer = generate_response(data.question, data.user_id)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
