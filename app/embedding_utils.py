from gemini_client import client
import numpy as np
from pdf_util import extract_text_from_pdf, chunk_text
# from fastapi import FastAPI

# app = FastAPI()

vector = []

def retrieve(question, k = 3):
    question_embedding = get_embedding(question)

    scores = []
    for item in vector:
        similarity = cosine_similarity(question_embedding, item["embedding"])
        scores.append((similarity, item["text"]))

    scores.sort(reverse=True)
    return scores[:k]

def cosine_similarity(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)

    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def get_embedding(text: str):
    res = client.models.embed_content(
        model = "gemini-embedding-001",
        contents = text
    )

    return res.embeddings[0].values

# print(get_embedding("e never forgot the days when he\nwas the weakest hunter struggling to survive. His journey became a symbol of growth,\ndetermination, and perseverance. The story of Sung Jinwoo inspired hunters everywhere to believe\nthat even the weakest person could rise to greatness through courage and effort."))

# chunks = [
#     "Jinwoo fought the statues.",
#     "The Shadow Monarch appeared.",
#     "Hunters enter gates to fight monsters."
# ]


text = extract_text_from_pdf("../uploads/solo_leveling.pdf")
print(text)
print("----------------------------------------------------------------Chunk")
chunks = chunk_text(text)
print(chunks)
print("----------------------------------------------------------------vector")
for chunk in chunks:
    vector.append(
        {
            "text": chunk,
            "embedding": get_embedding(chunk)
        }
    )

print(vector)
print("----------------------------------------------------------------Retrieve")

results = retrieve(
    "What is Dungeon?"
)
print(results)
print("----------------------------------------------------------------Context")
context = "Context: "+"\n\n".join(item[1] for item in results)
print(context)
print("----------------------------------------------------------------Context2")
context = context + "\n\nQuestion:\nWhy did Jinwoo become stronger?\n\nAnswer using only the provided context"
print(context)

response = client.models.generate_content(
    model = "gemini-2.5-flash",
    contents = context
)
print("------------------Final response by gemini-------------------")
print(response.text)

