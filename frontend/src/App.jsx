
import { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

import {
  uploadDocument,
  searchDocument,
  getChatHistory
} from "./api";

function App() {

  const [file, setFile] = useState(null);

  const [documentId, setDocumentId] = useState(
    () => localStorage.getItem("documentId") || ""
  );

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [history, setHistory] = useState([]);

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  // Load chat history
  const loadChatHistory = async (id) => {

    if (!id) return;

    try {
      const response = await getChatHistory(id);

      setHistory(response.data.history || []);

      console.log("CHAT HISTORY:", response.data);

    } catch (error) {
      console.error("History loading failed:", error);
    }
  };

  // Load history when page opens
  useEffect(() => {

    if (documentId) {
      loadChatHistory(documentId);
    }

  }, [documentId]);


  // Upload PDF
  const handleUpload = async () => {

    if (!file) return;

    try {

      setLoading(true);
      setMessage("Uploading PDF...");

      const response = await uploadDocument(file);

      const id = response.data.document.document_id;

      setDocumentId(id);

      localStorage.setItem("documentId", id);

      setHistory([]);
      setAnswer("");

      setMessage("PDF uploaded successfully!");

      console.log("UPLOAD RESPONSE:", response.data);

    } catch (error) {

      setMessage(
        error.response?.data?.error || "PDF upload failed"
      );

    } finally {

      setLoading(false);

    }
  };


  // Search document
  const handleSearch = async () => {

    if (!question.trim() || !documentId) return;

    try {

      setLoading(true);
      setAnswer("Searching document...");

      const response = await searchDocument(
        question,
        documentId
      );

      console.log("SEARCH RESPONSE:", response.data);
      console.log("ANSWER SOURCE:", response.data.answer_source);

      setAnswer(response.data.answer);

      setQuestion("");

      // Refresh chat history
      await loadChatHistory(documentId);

    } catch (error) {

      setAnswer(
        error.response?.data?.error || "Search failed"
      );

    } finally {

      setLoading(false);

    }
  };


  return (

    <div className="container py-5">

      <div className="text-center mb-5">

        <h1 className="fw-bold">
          Chat With Documents
        </h1>

        <p className="text-muted">
          Upload your PDF and ask questions
        </p>

      </div>


      {/* PDF Upload */}

      <div
        className="card shadow-sm p-4 mx-auto"
        style={{ maxWidth: "700px" }}
      >

        <h4>Upload Your PDF</h4>

        <input
          type="file"
          className="form-control my-3"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <button
          className="btn btn-primary"
          onClick={handleUpload}
          disabled={!file || loading}
        >

          {loading ? "Please wait..." : "Upload Document"}

        </button>

        {message && (
          <p className="mt-3">{message}</p>
        )}

      </div>


      {/* Ask Document */}

      <div
        className="card shadow-sm p-4 mx-auto mt-4"
        style={{ maxWidth: "700px" }}
      >

        <h4>Ask Your Document</h4>

        <input
          type="text"
          className="form-control my-3"
          placeholder="Ask a question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") handleSearch();
          }}
        />

        <button
          className="btn btn-success"
          onClick={handleSearch}
          disabled={!documentId || !question.trim() || loading}
        >

          Ask Question

        </button>

        {answer && (
          <div className="alert alert-info mt-3">

            <strong>Latest Answer:</strong>

            <p className="mb-0">{answer}</p>

          </div>
        )}

      </div>


      {/* Chat History */}

      <div
        className="card shadow-sm p-4 mx-auto mt-4"
        style={{ maxWidth: "700px" }}
      >

        <h4>Chat History</h4>

        {!documentId && (
          <p className="text-muted mt-3">
            Upload a PDF to view chat history.
          </p>
        )}

        {documentId && history.length === 0 && (
          <p className="text-muted mt-3">
            No previous conversations found.
          </p>
        )}

        {history.map((chat) => (

          <div
            key={chat.id}
            className="border rounded p-3 mt-3"
          >

            <p>
              <strong>Question:</strong>
              <br />
              {chat.question}
            </p>

            <p className="mb-2">
              <strong>Answer:</strong>
              <br />
              {chat.answer}
            </p>

            <small className="text-muted">
              {new Date(chat.created_at).toLocaleString()}
            </small>

          </div>

        ))}

      </div>

    </div>

  );

}

export default App;
