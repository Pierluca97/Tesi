from transformers import pipeline
from sentence_transformers import SentenceTransformer
import faiss
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama


# set up ZERO-SHOT
user_input = "How did Caravaggio create such dramatic lighting?"

candidate_labels = ['biography', 'technique', 'art']

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
classification = classifier(user_input, candidate_labels)
top_label = classification['labels'][0]
print(f"Classified as: {top_label}\n")

# documents index
documents = [
    {"text": "Caravaggio painted the Supper at Emmaus between 1605 and 1606, that is to say between the end of his stay in Rome and his flight from the city following his conviction for murder.", "category": "biography"},
    {"text": "The essentiality of the scene, along with the strong contrasts of light and shade, lend more drama to the event in the version now in the Pinacoteca.", "category": "technique"},
    {"text": "Saint Catherine of Alexandria by Caravaggio is one of the works in the Collection whose complete provenance allows its history to be traced almost from the time it was painted to the present day.", "category": "art"}
]

# set up embedding
emb_model = SentenceTransformer("all-MiniLM-L6-v2")
texts = [doc['text'] for doc in documents]
embeddings = emb_model.encode(texts)
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# find similar documents
query_embedding = emb_model.encode([user_input])
D, I = index.search(query_embedding, k=3)
print("Top 3 matched documents:")
for i in I[0]:
    print("-", texts[i])

# set up PROMPT + LLM

llm_model = Ollama(model="llama3", base_url="http://localhost:11434")

template = """Question: {question}

Answer: The following information can help answer your question."""
prompt = PromptTemplate.from_template(template)

# Invoke LLM with prompt
chain = prompt | llm_model
response = chain.invoke({"question": user_input})
print("\nLLM Response:\n", response)