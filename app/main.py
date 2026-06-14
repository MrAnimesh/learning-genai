from fastapi import FastAPI
from pydantic import BaseModel
from app.gemini_client import client

app = FastAPI()

chat_history = {}

class AskRequest(BaseModel):
    session_id: str
    question: str

@app.get("/")
def hello():
    return {"message": "GenAI learning journey started"}

@app.post("/ask")
def ask(request: AskRequest):
    # prompt = {"role": "user", "content": request.question}
    prompt = []
    if request.session_id in chat_history:
        prompt.append(" ".join(msg['content'] for msg in chat_history[request.session_id] if 'content' in msg))
        prompt.append(request.question)
        chat_history[request.session_id].append({"role":"user", "content": request.question})
    else:
        prompt.append({request.question})
        chat_history[request.session_id] = [{"role": "user", "content": request.question} ]

    print(chat_history)
    print("PROMPT: ",prompt)
    #What is LLM, can you tell me in one sentence


    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = prompt
    )

    
    chat_history[request.session_id].append({"role": "assistant", "content": response.text})
        

    return {
        "answer": response.text
    }