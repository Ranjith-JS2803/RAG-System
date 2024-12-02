# README.md

## RAG System

This system processes various file types (text, audio transcripts, video transcripts, CSV files, PDF documents, and images) to generate responses using a **Retrieval-Augmented Generation (RAG)** pipeline.

---

### Workflow

1. **Embedding Creation**
   - **Model Used**: [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
   - Text from source files is converted into vector embeddings for storage in the vector database.

2. **Query Processing**
   - User queries are embedded using the same model, and similarity searches retrieve relevant context.

3. **Response Generation**
   - **Model Used**: [gemini-1.5-flash](https://ai.google.dev/gemini-api/docs?gad_source=1&gclid=CjwKCAiA0rW6BhAcEiwAQH28Ikp4FthaEXOgAFekSViXvqcO0wQ9i9iIR2iqqGADcLCG80irQHUIHRoC3vwQAvD_BwE)
   - A prompt is created by combining the user query and retrieved context. The model generates a contextually accurate response.

---

### Implementation Details

1. **Data Preprocessing**
   - **PDF Documents**: Extracted using `PyPDFLoader` ([Reference](https://python.langchain.com/docs/integrations/document_loaders/pypdfloader/)).
   - **Text Files**: Processed using `TextLoader` ([Reference](https://python.langchain.com/v0.1/docs/modules/data_connection/document_loaders/)).
   - **Word Documents**: Handled with `Docx2txtLoader` ([Reference](https://python.langchain.com/docs/integrations/document_loaders/microsoft_word/)).
   - **CSV Files**: Extracted using `CSVLoader` ([Reference](https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.csv_loader.CSVLoader.html)).
   - **Image Files**: Processed with `PIL.Image` and `pytesseract` ([Reference](https://pypi.org/project/pytesseract/)).
   - **Audio Files**: Converted with `datasets.Audio`, `transformers.pipeline`, and `nltk.sent_tokenize` ([Reference](https://huggingface.co/learn/audio-course/en/chapter2/asr_pipeline)).

2. **Embedding Generation**
   - **Model**: [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
   - **Reason**: Maps sentences into a dense vector space, making it ideal for clustering and semantic search tasks.

3. **Vector Indexing**
   - **Database Used**: [FAISS](https://ai.meta.com/tools/faiss/)
   - **Index Type**: Flat indexing for exhaustive search, ensuring high accuracy.

4. **RAG Workflow**
   - Source files are embedded and stored in a vector database (e.g., FAISS).
   - User queries are embedded and matched against stored embeddings for context retrieval.
   - Responses are generated using `gemini-1.5-flash`.

---

### Evaluation

1. **Retrieval Evaluation**: Used keyword matching as the evaluation metric.
2. **Generation Evaluation**: Calculated cosine similarity between actual and generated responses.

---

### Challenges and Solutions

1. **Error: `TesseractNotFoundError`**
   - **Cause**: Missing Tesseract installation for OCR processing.
   - **Solution**: Installed Tesseract ([Reference](https://github.com/UB-Mannheim/tesseract/wiki)).

2. **Error: FFmpeg not found**
   - **Cause**: Missing FFmpeg installation for audio conversion.
   - **Solution**: Installed FFmpeg ([Reference](https://www.wikihow.com/Install-FFmpeg-on-Windows#Steps)).

### Understand Files

- **`constants.py`**: Defines and initializes the LLM, embedding models, and vector database.
- **`vector_store.py`**: Includes functions for data preprocessing, embedding generation, and vector database storage (FAISS).
- **`model.py`**: Implements context retrieval and response generation using the LLM.

### Commands to Run the System

1. **Navigate to the project directory**:
   ```bash
   cd <project-directory>

2. **Run the Streamlit Application**
   To launch the Streamlit web interface for the RAG system:
   ```bash
   python -m streamlit run application.py

3. **Evaluate Retrieval and Generation Performance**
   To evaluate the system's retrieval and response generation metrics:
   ```bash
   python evaluation.py