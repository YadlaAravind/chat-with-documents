\# Chat with Documents – AI-Powered RAG Application



An AI-powered web application that allows users to upload PDF documents and ask questions based on their content. The application extracts document text, generates embeddings, retrieves relevant information, and provides answers with source references.



\## Features



\- Upload PDF documents.

\- Extract text from PDF files.

\- Split documents into smaller chunks.

\- Generate text embeddings using Sentence Transformers.

\- Store and retrieve document vectors using ChromaDB.

\- Ask questions based on uploaded documents.

\- Retrieve relevant document chunks using semantic search.

\- Display source information for retrieved content.

\- Store and display chat history.



\## Tech Stack



\*\*Frontend\*\*

\- React.js

\- Vite

\- Bootstrap

\- Axios



\*\*Backend\*\*

\- Python

\- Flask

\- REST APIs

\- SQLAlchemy



\*\*AI and Retrieval\*\*

\- Sentence Transformers (all-MiniLM-L6-v2)

\- ChromaDB

\- LangChain Text Splitters

\- PyMuPDF



\*\*Database\*\*

\- SQLite

\- ChromaDB



\## Project Architecture



1\. User uploads a PDF through the React frontend.

2\. Flask receives the PDF through a REST API.

3\. PyMuPDF extracts the document text.

4\. LangChain splits the text into chunks.

5\. Sentence Transformers generates embeddings.

6\. ChromaDB stores the embeddings.

7\. User submits a question.

8\. The application retrieves relevant chunks using semantic similarity.

9\. A response is generated from the retrieved document content.

10\. Chat history is stored and displayed.



\## Project Structure



```text

chat-with-documents/

├── backend/

│   ├── app/

│   │   ├── models/

│   │   ├── routes/

│   │   └── services/

│   ├── tests/

│   ├── requirements.txt

│   └── run.py

├── frontend/

│   ├── public/

│   ├── src/

│   ├── package.json

│   └── vite.config.js

└── .gitignore

```



\## Installation and Setup



\### 1. Clone the repository



```bash

git clone https://github.com/YadlaAravind/chat-with-documents.git

cd chat-with-documents

```



\### 2. Backend Setup



```bash

cd backend

python -m venv .venv

```



Activate the virtual environment on Windows:



```bash

.venv\\Scripts\\activate

```



Install dependencies:



```bash

pip install -r requirements.txt

```



Start the Flask backend:



```bash

python run.py

```



Backend URL: `http://127.0.0.1:5000`



\### 3. Frontend Setup



Open another terminal:



```bash

cd frontend

npm install

npm run dev

```



Frontend URL: `http://localhost:5173`



\## Future Improvements



\- Integrate reliable LLM-based answer generation.

\- Improve answer accuracy and relevance.

\- Add support for multiple document formats.

\- Improve document management.

\- Add user authentication.



\## Author



\*\*Aravind Yadla\*\*



\- GitHub: https://github.com/YadlaAravind

\- LinkedIn: https://linkedin.com/in/yadlaaravind

