from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np

# 🔹 Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# 🔹 Load cleaned data
with open("student_data.json", "r") as f:
    data = json.load(f)

# 🔹 Combine useful text for better understanding
texts = [
    f"{item['course']} {item['question']} {item['answer']}"
    for item in data
]

# 🔹 Convert text → embeddings
embeddings = model.encode(texts, normalize_embeddings=True)

# 🔹 Convert to FAISS format
embeddings = np.array(embeddings).astype("float32")

# 🔹 Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)

# 🔹 Add embeddings to index
index.add(embeddings)

# 🔍 Search function
def search(query, persona=None, k=3):
    print("Search Query:", query)

    query_vector = model.encode([query], normalize_embeddings=True).astype("float32")

    distances, indices = index.search(query_vector, k * 5)

    results = []

    for i, idx in enumerate (indices[0]):
        if idx < len(data):
            item = data[idx]

            if persona and item["persona"] != persona:
                continue

            if distances[0][i] > 0.5:
                results.append(item)

    print("Filtered Results:", len(results))
            
    return results[:k]
