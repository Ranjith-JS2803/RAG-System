import os
import warnings

import faiss

import google.generativeai as genAI
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores.utils import DistanceStrategy

warnings.filterwarnings("ignore", category=FutureWarning)

embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

with open("generativeAI-serviceKey", "r") as f:
    api_key = f.readline()

genAI.configure(api_key = api_key)
llm_model = genAI.GenerativeModel("gemini-1.5-flash")

vectore_store_path = "faiss_index"
if os.path.exists(vectore_store_path):
    vector_store = FAISS.load_local(
        folder_path = vectore_store_path,
        embeddings = embedding_function,
        allow_dangerous_deserialization=True
    )
else:
    index = faiss.IndexFlatL2(len(embedding_function.embed_query("hello world")))
    vector_store = FAISS(
        embedding_function=embedding_function,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
        distance_strategy = DistanceStrategy.COSINE
    )