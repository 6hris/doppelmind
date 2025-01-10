from app.vector_store import vector_store
from app.llm import llm
from datetime import datetime
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re

def preprocess_context_data(raw_text: str, user_id: str) -> list:
    """Preprocess text into clean, chunked documents with metadata."""
    def clean_text(text):
        text = re.sub(r"[^a-zA-Z0-9.,!? ]+", "", text)
        return re.sub(r"\s+", " ", text).strip()

    cleaned_text = clean_text(raw_text)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(cleaned_text)

    timestamp = datetime.utcnow().isoformat()
    return [
        Document(page_content=chunk, metadata={"user_id": user_id, "timestamp": timestamp, "chunk_index": idx})
        for idx, chunk in enumerate(chunks)
    ]

def generate_response(question: str, user_id: str) -> str:
    """Retrieve relevant context and generate an answer using the LLM."""
    
    # Retrieve relevant context for the user
    retrieved_docs = vector_store.similarity_search(question, filter={"user_id": user_id})
    
    # Prepare the context by combining document contents
    context = "\n\n".join(doc.page_content for doc in retrieved_docs)
    
    # Construct the prompt with context and question
    prompt = f"""
    You are a helpful and insightful assistant with access to a user's personalized context.
    Use the provided context to answer the user's question accurately and thoughtfully.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    
    # Pass the prompt to the LLM
    response = llm.invoke([{"role": "user", "content": prompt}])
    
    return response.content
