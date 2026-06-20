from fastapi import FastAPI
from pydantic import BaseModel
from app.gemini_client import client, call_generate_text
from app.vector_store import index_dcument, retrieve
from app.pdf_util import extract_text_from_pdf, chunk_text
app = FastAPI()

chat_history = {}

class AskRequest(BaseModel):
    session_id: str
    question: str


@app.post("/askpdf")
def ask_pdf(request: AskRequest):
    text = extract_text_from_pdf("/Users/animeshsingh/Developer/Python/GenAI/genai-learning/uploads/solo_leveling.pdf")
    chunks = chunk_text(text)
    index_dcument("solo_leveling", chunks)
    retrieved_chunks = retrieve(request.question)
    context_parts = []

    for chunk in retrieved_chunks:
        source = chunk["metadata"]["document_name"]
        chunk_id = chunk["metadata"]["chunk_id"]

        context_parts.append(
            f"""
Source: {source}
Chunks: {chunk_id}
Contents: {chunk["text"]}
"""
        )
    context = "\n\n---\n\n".join(context_parts)
    prompt = f"""
You are a document question-answering assistant.

Use only the provided context to answer the user's question.

If the answer is not present in the context, say:
"I couldn't find that information in the document."

Context:
{context}

Question:
{request.question}

Answer:
"""
    res = call_generate_text(prompt)
    return {
        "res": res 
    }






@app.get("/")
def hello():
    return {"message": "GenAI learning journey started"}

@app.post("/ask")
def ask(request: AskRequest):
    # prompt = {"role": "user", "content": request.question}-
    prompt = []
    if request.session_id in chat_history:
        # prompt.append(" ".join(msg['content'] for msg in chat_history[request.session_id] if 'content' in msg))
        for msg in chat_history[request.session_id]:
            prompt.append(f"{msg['role']}: {msg['content']}")
        prompt.append(f"user: {request.question}")
        chat_history[request.session_id].append({"role":"user", "content": request.question})
    else:
        prompt.append(f"user: {request.question}")
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