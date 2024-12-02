from vector_store import *
from model import *

import streamlit as st
import time
import os

upload_dir = "Uploads"
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

def generator(response):
    words = response.split(" ")
    for word in words:
        yield word + " "
        time.sleep(0.02)

if "page" not in st.session_state:
    st.session_state.page = "file_upload"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processing" not in st.session_state:
    st.session_state.processing = False
if "query_enabled" not in st.session_state:
    st.session_state.query_enabled = False
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

if st.session_state.page == "file_upload":
    st.title("Chat Assistant")
    uploaded_file = st.file_uploader("Upload your file", type=["pdf", "txt", "docx", "csv", "png", "jpeg", "jpg", "mp3", "wav", "flac"])

    if uploaded_file:
        st.session_state.uploaded_file = uploaded_file
    if uploaded_file:
        file_extension = uploaded_file.name.split('.')[-1].lower()

        if file_extension in ["pdf", "txt", "csv"]:
            file_type = file_extension.upper()
        elif file_extension in ["png", "jpeg", "jpg"]:
            file_type = "IMAGE"
        elif file_extension in ["mp3", "wav", "flac"]:
            file_type = "AUDIO"            
        elif file_extension == "docx":
            file_type = "WORD"
        else:
            file_type = None

        if file_type:
            st.write(f"File type: {file_type}")
            if st.button("Process File"):
                st.session_state.processing = True
                st.session_state.query_enabled = False

                with st.spinner("Processing..."):
                    
                    save_path = os.path.join(upload_dir, uploaded_file.name)
                    with open(save_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    print(f"File saved at: {save_path}")  

                    if file_type == "TXT":
                        vectore_store_text(save_path, file_type)

                    elif file_type == "PDF":
                        vectore_store_pdf(save_path, file_type)
                    
                    elif file_type == "WORD":
                        vectore_store_docx(save_path, file_type)                        

                    elif file_type == "CSV":
                        vectore_store_csv(save_path, file_type)

                    elif file_type == "IMAGE":
                        vectore_store_image(save_path, file_type)
                    
                    elif file_type == "AUDIO":
                        vectore_store_audio(save_path, file_type)

                    time.sleep(3)

                    st.session_state.processing = False
                    st.session_state.query_enabled = True

        else:
            st.warning("Unsupported file type. Please upload a valid file.")

    if st.session_state.processing:
        st.write("File is being processed. Please wait...")

    if st.session_state.query_enabled or os.path.exists("faiss_index"):
        if st.button("Ask Query"):
            st.session_state.page = "ans_query"

elif st.session_state.page == "ans_query":
    if not st.session_state.uploaded_file and not os.path.exists("faiss_index"):
        st.warning("You must upload and process a file first!")
        st.session_state.page = "file_upload"
        st.stop()

    st.title("Chat Assistant")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = generateResponse(prompt)
            st.write_stream(generator(response))
            st.session_state.messages.append({"role": "assistant", "content": response})
