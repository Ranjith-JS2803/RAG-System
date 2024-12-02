from model import *

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

file_path = "evaluation_data.csv"
data = pd.read_csv(file_path)

def keyword_matching(retrieved_text, keywords):
    retrieved_words = set(retrieved_text.lower().split())
    keyword_list = set(keywords.lower().split(", "))
    matched_keywords = retrieved_words.intersection(keyword_list)
    return len(matched_keywords) / len(keyword_list)

def cosine_similarity_eval(actual_response, generated_response):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([actual_response, generated_response])
    similarity = cosine_similarity(vectors[0], vectors[1])
    return similarity[0][0]

retrieval_scores = []
generation_scores = []

for _, row in data.iterrows():
    retrieval_score = keyword_matching(retrieveContext(row["User Query"]), row["Retrieval Keywords"])
    generation_score = cosine_similarity_eval(generateResponse(row["User Query"]), row["Generated Text"])
    retrieval_scores.append(retrieval_score)
    generation_scores.append(generation_score)

print("Overall Evaluation Results")
print(f"Retrieval Evaluation for all user queries : {round(100*(sum(retrieval_scores)/len(retrieval_scores)))}.00%")
print(f"Generation Evaluation for all user queries : {round(100*(sum(generation_scores)/len(generation_scores)))}.00%")
