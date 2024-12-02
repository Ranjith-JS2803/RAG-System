from constants import *

from PIL import Image
import pytesseract
from uuid import uuid4

from transformers import pipeline
from nltk.tokenize import sent_tokenize
from datasets import Audio, Dataset

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_core.documents import Document

def vectore_store_pdf(file_path, file_type):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    vector_store.add_documents(documents = documents)
    vector_store.save_local("faiss_index")
    print(f"Succesfully Created the Vector Store!! for uploaded {file_type} file")
    return True

def vectore_store_text(file_path, file_type):
    loader = TextLoader(file_path)
    documents = loader.load()
    vector_store.add_documents(documents = documents)
    vector_store.save_local("faiss_index")
    print(f"Succesfully Created the Vector Store!! for uploaded {file_type} file")
    return True

def vectore_store_docx(file_path, file_type):
    loader = Docx2txtLoader(file_path)
    documents = loader.load()
    vector_store.add_documents(documents = documents)
    vector_store.save_local("faiss_index")
    print(f"Succesfully Created the Vector Store!! for uploaded {file_type} file")
    return True    

def vectore_store_csv(file_path, file_type):
    loader = CSVLoader(file_path)
    documents = loader.load()
    vector_store.add_documents(documents = documents)
    vector_store.save_local("faiss_index")
    print(f"Succesfully Created the Vector Store!! for uploaded {file_type} file")
    return True

def vectore_store_image(file_path, file_type):
    
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    file_name = file_path.split("\\")[-1].split(".")[0]
    
    image = Image.open(file_path)
    extracted_text = pytesseract.image_to_string(image).split("\n")
    extracted_text = list(filter(lambda elem: elem != "", extracted_text))
    
    documents = []
    for text in extracted_text:
        doc = Document(
            page_content = text,
            metadata = {"source" : file_type}
            )
        documents.append(doc)
    
    uuids = [str(uuid4()) for _ in range(len(documents))]
    
    vector_store.add_documents(documents = documents, ids = uuids)
    vector_store.save_local("faiss_index")
    print(f"Succesfully Created the Vector Store!! for uploaded {file_type} file")
    return True

def vectore_store_audio(file_path, file_type):
    print("Converting Audio......")
    data = Dataset.from_dict({"audio" : [file_path]}).cast_column("audio", Audio(sampling_rate=16000))

    asr = pipeline("automatic-speech-recognition")

    try:
        transcription = asr(data[0]["audio"]["array"])
        documents = []
        for text in sent_tokenize(transcription["text"].lower()):
            doc = Document(
                page_content = text,
                metadata = {"source" : file_type}
                )
            documents.append(doc)
        
        uuids = [str(uuid4()) for _ in range(len(documents))]
        
        vector_store.add_documents(documents = documents, ids = uuids)
        vector_store.save_local("faiss_index")
        print(f"Succesfully Created the Vector Store!! for uploaded {file_type} file")
        return True        
    except Exception as e:
        print("Can't Extract Text from the audio")
        print(e)
        return e