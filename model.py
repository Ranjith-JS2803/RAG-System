from constants import *

import os
from langchain_community.vectorstores import FAISS

def retrieveContext(query):
    if os.path.exists(vectore_store_path):
        relevant_docs = vector_store.similarity_search(query = query, k=2)
        context = "\n".join([doc.page_content for doc in relevant_docs])
        return context
    else:
        return "There is no Vector DB for retrieval"

def generateResponse(query):
    context = retrieveContext(query)
    prompt = f"""
    Your a Chat Assistant, you will understand the query and use the context to answer precisely
    Query : {query}
    Context : {context}"""
    response = llm_model.generate_content(prompt)
    return response.text

