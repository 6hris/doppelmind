from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain_core.documents import Document
from langchain import hub
from typing_extensions import List, TypedDict
from langgraph.graph import START, StateGraph
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import re

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Your React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JournalEntry(BaseModel):
    username: str
    entry: str
    timestamp: str

@app.post("/save-entry")
async def save_entry(entry: JournalEntry):
    try:
        # For now, just print to verify we're receiving the data
        print(f"Received entry from {entry.username}: {entry.entry}")
        return {"status": "success"}
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"status": "error", "message": str(e)}

load_dotenv()

llm = ChatOpenAI(
  openai_api_key=os.getenv("OPENROUTER_API_KEY"),
  openai_api_base="https://openrouter.ai/api/v1",
  model_name="anthropic/claude-3.5-sonnet",
)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "user-context-data"
index = pc.Index(index_name)

vector_store = PineconeVectorStore(embedding=embeddings, index=index)

def preprocess_context_data(raw_text: str, user_id: str) -> list:
    """
    Preprocess raw text into chunks and generate metadata for vector storage.
    """
    # Clean the text
    def clean_text(text):
        text = re.sub(r"[^a-zA-Z0-9.,!? ]+", "", text)  # Remove special characters
        return re.sub(r"\s+", " ", text).strip()  # Remove extra spaces

    cleaned_text = clean_text(raw_text)

    # Chunk the text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(cleaned_text)

    # Create documents with metadata
    timestamp = datetime.utcnow().isoformat()
    documents = [
        Document(
            page_content=chunk,
            metadata={"user_id": user_id, "timestamp": timestamp, "chunk_index": idx},
        )
        for idx, chunk in enumerate(chunks)
    ]

    return documents

raw_text = input("Enter your context data: ")
user_id = "user_123"
processed_docs = preprocess_context_data(raw_text, user_id)
_ = vector_store.add_documents(documents=processed_docs)


template = """
You are a helpful and insightful assistant with access to a user's personalized context. 
Use the provided context and your knowledge to answer the following question accurately and thoughtfully.

Context:
{context}

Question:
{question}

Answer:
"""

prompt = PromptTemplate(template=template, input_variables=["context", "question"])


# Define state for application
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


# Define application steps
def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(
        state["question"],
        filter={"user_id": user_id}  # Filter by user_id
    )
    print("Retrieved documents:", retrieved_docs)
    return {"context": retrieved_docs}

def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}

# Compile application and test
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

question = input("What would you like to ask? ")
response = graph.invoke({"question": question})
print(response["answer"])