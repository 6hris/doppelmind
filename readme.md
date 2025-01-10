# Doppelgänger AI

A personalized AI assistant that evolves with its user by storing and retrieving contextual life data. Built with FastAPI, Pinecone vector database, and a powerful LLM, this project allows users to log daily experiences and ask context-aware questions.

## 📊 Project Features

- 🔮 **Contextual Understanding:** Stores and retrieves user-specific data for personalized responses.
- 🛠️ **Vector Database Integration:** Uses Pinecone for efficient similarity search.
- 👨‍💻 **FastAPI Backend:** Provides RESTful endpoints for uploading context and querying the AI.
- 🔬 **NLP Preprocessing:** Cleans and chunks user input for optimal embedding and retrieval.
- 🌐 **Scalable & Modular:** Easily extendable and deployable with a clear project structure.

## 📂 Project Structure

```
doppelganger_ai/
├── app/
│   ├── main.py               # FastAPI server and API routes
│   ├── routes.py             # API endpoints (upload context, ask question)
│   ├── services.py           # Core logic: preprocessing, retrieval, generation
│   ├── models.py             # Pydantic models (ContextInput, QuestionInput)
│   ├── vector_store.py       # Vector DB setup and connection
│   └── llm.py                # LLM initialization and configuration
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (API keys, etc.)
└── README.md                 # Project documentation
```

## 📚 Setup Instructions

### 1. **Clone the Repository**
```bash
git clone https://github.com/your-username/doppelganger_ai.git
cd doppelganger_ai
```

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Configure Environment Variables**
Create a `.env` file:
```bash
OPENROUTER_API_KEY=your_openrouter_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

### 4. **Run the Server**
```bash
uvicorn app.main:app --reload
```

The server will be available at `http://127.0.0.1:8000`.

### 5. **Test the API with Postman or cURL**

**Upload Context:**
```bash
POST /upload_context
{
  "user_id": "user_123",
  "text": "Today I worked on a new AI project involving personalized assistants."
}
```

**Ask a Question:**
```bash
POST /ask_question
{
  "user_id": "user_123",
  "question": "What project am I working on?"
}
```

## 📊 API Endpoints

### `POST /upload_context`
- **Description:** Uploads user context data.
- **Request Body:**
  ```json
  {
    "user_id": "string",
    "text": "string"
  }
  ```
- **Response:**
  ```json
  {
    "status": "Context uploaded successfully."
  }
  ```

### `POST /ask_question`
- **Description:** Asks a context-aware question.
- **Request Body:**
  ```json
  {
    "user_id": "string",
    "question": "string"
  }
  ```
- **Response:**
  ```json
  {
    "answer": "string"
  }
  ```
  
## 🛠️ License

This project is open-source and available under the [MIT License](LICENSE).

---

🚀 **Ready to build your personal AI companion? Let's go!**

