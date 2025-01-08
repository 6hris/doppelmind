import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)

def llm_call(prompt: str, model: str = "anthropic/claude-3.5-sonnet") -> str:
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return "Sorry, I encountered an error processing your request."

# Example usage:
input = input()
response = llm_call(input)
print(response)
