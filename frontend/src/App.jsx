
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
    <div className="app-shell">

      {/* Sidebar */}
      <aside className="sidebar">

        <div className="brand">
          <div className="brand-icon">✦</div>
          <div>
            <h2>DocuMind</h2>
            <span>AI DOCUMENT ASSISTANT</span>
          </div>
        </div>

        <div className="sidebar-section">
          <p className="sidebar-label">WORKSPACE</p>

          <div className="sidebar-link active">
            <span>◈</span>
            Document Chat
          </div>
        </div>

        <div className="sidebar-document">
          <p className="sidebar-label">CURRENT DOCUMENT</p>

          <div className="document-icon">PDF</div>

          <div className="document-info">
            <strong>
              {file?.name || (documentId ? "Document uploaded" : "No document")}
            </strong>
            <span>
              {documentId ? "Ready to chat" : "Upload a PDF to begin"}
            </span>
          </div>

          <div className={`status-dot ${documentId ? "online" : ""}`} />
        </div>

        <div className="sidebar-footer">
          <div className="profile-avatar">A</div>
          <div>
            <strong>My Workspace</strong>
            <span>Personal account</span>
          </div>
        </div>

      </aside>

      {/* Main content */}
      <main className="main-content">

        {/* Topbar */}
        <header className="topbar">
          <div className="breadcrumb">
            Workspace <span>/</span> Document Chat
          </div>

          <div className="topbar-status">
            <span className="status-dot online" />
            AI Workspace
          </div>
        </header>

        {/* Welcome section */}
        <section className="welcome-section">
          <div>
            <span className="eyebrow">YOUR AI DOCUMENT WORKSPACE</span>
            <h1>Chat with your documents<span>.</span></h1>
            <p>
              Upload your files, ask questions, and discover
              information instantly.
            </p>
          </div>

          <div className="welcome-decoration">✦</div>
        </section>

        {/* Dashboard layout */}
        <div className="workspace-grid">

          {/* Left column */}
          <div className="primary-column">

            {/* Upload card */}
            <section className="dashboard-card upload-card">

              <div className="card-heading">
                <div>
                  <span className="section-number">01 / UPLOAD</span>
                  <h3>Upload your document</h3>
                  <p>Choose a PDF file to get started.</p>
                </div>

                <div className="heading-icon">↑</div>
              </div>

              <label className="upload-zone">
                <input
                  type="file"
                  accept=".pdf,application/pdf"
                  onChange={(e) =>
                    setFile(e.target.files?.[0] || null)
                  }
                />

                <div className="upload-icon">↑</div>

                <strong>
                  {file ? file.name : "Drop your PDF here"}
                </strong>

                <span>
                  {file
                    ? "File selected successfully"
                    : "or click to browse your files"}
                </span>

                <small>PDF files only</small>
              </label>

              <button
                className="primary-button upload-button"
                onClick={handleUpload}
                disabled={!file || loading}
              >
                {loading ? "Please wait..." : "Upload document"}
                <span>→</span>
              </button>

              {message && (
                <p className="upload-message">{message}</p>
              )}

            </section>

            {/* Chat card */}
            <section className="dashboard-card chat-card">

              <div className="card-heading">
                <div>
                  <span className="section-number">02 / ASK AI</span>
                  <h3>Ask your document</h3>
                  <p>Your document is your knowledge base.</p>
                </div>

                <div className="ai-icon">✦</div>
              </div>

              <div className="chat-display">

                {!answer ? (
                  <div className="empty-chat">
                    <div className="empty-chat-icon">✧</div>
                    <h4>What would you like to know?</h4>
                    <p>
                      Ask anything about your uploaded PDF.
                      Your answers will appear here.
                    </p>
                  </div>
                ) : (
                  <div className="answer-container">
                    <div className="answer-label">
                      <span>✦</span> AI RESPONSE
                    </div>
                    <div className="answer-text">
                      {answer}
                    </div>
                  </div>
                )}

              </div>

              <form
                className="chat-input-area"
                onSubmit={(e) => {
                  e.preventDefault();
                  handleSearch();
                }}
              >
                <input
                  type="text"
                  placeholder={
                    documentId
                      ? "Ask a question about your PDF..."
                      : "Upload a PDF to start chatting..."
                  }
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  disabled={!documentId || loading}
                />

                <button
                  type="submit"
                  className="send-button"
                  disabled={!documentId || !question.trim() || loading}
                >
                  {loading ? "..." : "↑"}
                </button>
              </form>

              <div className="chat-hint">
                AI responses are based on your uploaded document.
              </div>

            </section>

          </div>

          {/* Right column */}
          <aside className="history-column">

            <section className="dashboard-card history-card">

              <div className="history-heading">
                <div>
                  <span className="section-number">03 / ACTIVITY</span>
                  <h3>Chat history</h3>
                </div>

                <span className="history-count">
                  {history.length}
                </span>
              </div>

              {!documentId && (
                <div className="history-empty">
                  <span>◷</span>
                  <p>Upload a PDF to view your conversations.</p>
                </div>
              )}

              {documentId && history.length === 0 && (
                <div className="history-empty">
                  <span>◷</span>
                  <p>No previous conversations yet.</p>
                </div>
              )}

              <div className="history-list">
                {history.map((chat) => (
                  <div
                    key={chat.id}
                    className="history-item"
                  >
                    <div className="history-question">
                      <span>Q</span>
                      {chat.question}
                    </div>

                    <p className="history-answer">
                      {chat.answer}
                    </p>

                    <small>
                      {new Date(chat.created_at).toLocaleString()}
                    </small>
                  </div>
                ))}
              </div>

            </section>

            <div className="privacy-note">
              <span>✧</span>
              <div>
                <strong>Your documents, your workspace.</strong>
                <p>Ask questions and explore your information.</p>
              </div>
            </div>

          </aside>

        </div>

        <footer className="app-footer">
          Powered by AI <span>•</span> Built with React & Flask
        </footer>

      </main>
    </div>
  );
}

export default App;
