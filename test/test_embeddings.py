from sentence_transformers import SentenceTransformer

print("Starting...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded!")

text = "Python is used for machine learning."

embedding = model.encode(text)

print("Embedding created!")
print(embedding)
print("Vector size:", len(embedding))