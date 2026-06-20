from app.gemini_client import client
import numpy as np

vectore_store = []
# indexing chunks with text chunk, embedding and doc metadata
def index_dcument(doc_name: str, chunks: list[str]):
    for index, chunk in enumerate(chunks):
        chunk = chunk.strip()
        if not chunk:
            continue

        embedding = get_embedding(chunk)

        vectore_store.append({
            "id": f"{doc_name}::chunk-{index+1}",
            "text": chunk,
            "embedding": embedding,
            "metadata":{
                "document_name": doc_name,
                "chunk_id": index+1
            }
        })

def get_embedding(chunk: str):
    response = client.models.embed_content(
        model= "gemini-embedding-001",
        contents = chunk
    )
    return response.embeddings[0].values

def retrieve(question:str, k = 3):
    question_embedding = get_embedding(question)

    # Result for similarity between question embedding and book embedding 
    result = []
    # Looping through the chunks embedding stored in vectore store
    for item in vectore_store:
        # cosine similarity will return the score that which chunk is nearest to the question embedding
        score = cosine_similarity(
            question_embedding, item["embedding"]
        )
        result.append({
            "score": score,
            "text": item["text"],
            "metadata": item["metadata"]
        })
        # Sorting according to the highest score, high score = high similarity
        result.sort(
            key=lambda x: x["score"],
            reverse=True
        )
    
    return result[:k]

def cosine_similarity(v1, v2) -> float:

    denominator = (np.linalg.norm(v1) * np.linalg.norm(v2))

    if denominator == 0:
        return 0.0

    return float(np.dot(v1, v2) / denominator)