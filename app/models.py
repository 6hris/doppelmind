from pydantic import BaseModel

class ContextInput(BaseModel):
    user_id: str
    text: str

class QuestionInput(BaseModel):
    user_id: str
    question: str
