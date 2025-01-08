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

load_dotenv()

template = """Question: {question}
Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])

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

example_context_data = [
    Document(
        page_content="Today I worked on a new AI project. It involved building a personalized assistant.",
        metadata={"user_id": "user_123", "timestamp": "2025-01-07T10:00:00Z", "chunk_index": 0}
    ),
    Document(
        page_content="I went to lunch with a colleague and discussed machine learning trends.",
        metadata={"user_id": "user_123", "timestamp": "2025-01-07T12:30:00Z", "chunk_index": 1}
    ),
    Document(
        page_content="In the evening, I attended a networking event and met some interesting people in the AI industry.",
        metadata={"user_id": "user_123", "timestamp": "2025-01-07T18:00:00Z", "chunk_index": 2}
    )
]

_ = vector_store.add_documents(documents=example_context_data)

# Define prompt for question-answering
prompt = hub.pull("rlm/rag-prompt")


# Define state for application
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


# Define application steps
def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
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

response = graph.invoke({"question": "In the evening, what did I do?"})
print(response["answer"])