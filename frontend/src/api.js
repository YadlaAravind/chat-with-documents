
import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:5000/api",
});

// Upload PDF
export const uploadDocument = (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return API.post("/documents/upload", formData);
};

// Search document
export const searchDocument = (query, documentId) => {
  return API.post("/documents/search", {
    query,
    document_id: documentId,
  });
};

// Get chat history
export const getChatHistory = (documentId) => {
  return API.get(`/documents/history/${documentId}`);
};

export default API;
