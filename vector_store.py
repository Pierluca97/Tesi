from langchain_community.vectorstores import Redis
from redis import Redis
from sentence_transformers import SentenceTransformer



emb_model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = emb_model.encode(texts) # restituisce una matrice NumPy
dimension = embeddings.shape[1] # la dimensione del vettore di embedding
# index = faiss.IndexFlatL2(dimension) # distanza tra i vettori
# index.add(embeddings)


vector_store = RedisVectorStore(
    index_name="Eu-demo",
    embedding=SentenceTransformer("all-MiniLM-L6-v2"),
    redis_url="redis://localhost:6379",
)

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=False)