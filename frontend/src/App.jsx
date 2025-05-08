import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import "./App.css";

export default function App() {
  const [messages, setMessages] = useState(() => {
    const saved = localStorage.getItem("chat_messages");
    return saved ? JSON.parse(saved) : [];
  });

  const [pdfFile, setPdfFile] = useState(() => {
    const saved = localStorage.getItem("uploaded_pdf");
    return saved ? JSON.parse(saved) : null;
  });

  const [input, setInput] = useState("");
  const [uploading, setUploading] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    let uid = localStorage.getItem("user_id");
    if (!uid) {
      uid = crypto.randomUUID();
      localStorage.setItem("user_id", uid);
    }
  }, []);
  
  useEffect(() => {
    localStorage.setItem("chat_messages", JSON.stringify(messages));
  }, [messages]);

  useEffect(() => {
    localStorage.setItem("uploaded_pdf", JSON.stringify(pdfFile));
  }, [pdfFile]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const speakText = (text) => {
    setIsSpeaking(true);
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    utterance.onend = () => setIsSpeaking(false);
    speechSynthesis.speak(utterance);
  };

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file || file.type !== "application/pdf") {
      alert("Only PDF files are allowed");
      return;
    }
    const userId = localStorage.getItem("user_id");
    const formData = new FormData();
    formData.append("file", file);
    formData.append("user_id", userId);
    formData.append("is_pdf_uploaded", false);
    try {
      setUploading(true);
      const res = await axios.post("http://localhost:3001/pdf-load", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setPdfFile({ name: file.name, path: res.data.path });
    } catch (err) {
      alert("Error uploading PDF");
    } finally {
      setUploading(false);
    }
  };

  const removePdf = async () => {
    const userId = localStorage.getItem("user_id");
    const formData = new FormData();
    formData.append("user_id", userId);
    formData.append("is_pdf_uploaded", true);
    try {
      await axios.post("http://localhost:3001/pdf-load", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
    } catch (err) {
      console.error("Failed to notify backend about PDF removal");
    }
    setPdfFile(null);
    localStorage.removeItem("uploaded_pdf");
  };
  
  const stopSpeaking = () => {
    speechSynthesis.cancel();
    setIsSpeaking(false);
  };

  const sendMessage = async () => {
    if (!input.trim()) return;
  
    const userId = localStorage.getItem("user_id");
    const newMessages = [...messages, { sender: "user", text: input }];
    setMessages([...newMessages, { sender: "ai", text: "" }]);
    setInput("");
  
    const formData = new FormData();
    formData.append("user_id", userId);
    formData.append("user_message", input);
  
    try {
      const res = await axios.post("http://localhost:3001/pdf-chat", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
  
      const aiMessage = res.data.ai_message;
      let index = 0;
      let currentText = "";
  
      const streamInterval = setInterval(() => {
        currentText += aiMessage[index];
        setMessages(prev => {
          const updated = [...prev];
          updated[updated.length - 1].text = currentText;
          return [...updated];
        });
        index++;
        if (index >= aiMessage.length) clearInterval(streamInterval);
      }, 30);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || "⚠️ Error communicating with AI agent";
      setMessages([
        ...newMessages,
        { sender: "ai", text: errorMessage },
      ]);
    }
  };

  return (
    <div className="chat-container">
      <div className="navbar">
        <h1>
          <span role="img" aria-label="document">📄</span>
          PDF Chat Agent
        </h1>
        <div className="pdf-upload-container">
          {uploading ? (
            <div className="spinner"></div>
          ) : pdfFile ? (
            <div className="pdf-file-info">
              <span role="img" aria-label="pdf">📑</span>
              <span className="truncate max-w-[200px]">{pdfFile.name}</span>
              <button onClick={removePdf} className="remove-pdf-btn" title="Remove PDF">
                ✕
              </button>
            </div>
          ) : (
            <label className="pdf-upload-label">
              <span role="img" aria-label="upload">📤</span>
              Upload PDF
              <input type="file" accept="application/pdf" onChange={handleUpload} className="hidden" />
            </label>
          )}
        </div>
      </div>

      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.sender}`}>
            <div>{msg.text}</div>
            {msg.sender === "ai" && (
              <div className="message-controls">
                <button 
                  onClick={() => speakText(msg.text)} 
                  className="speak-btn"
                  title="Speak message"
                  disabled={isSpeaking}
                >
                  🔊
                </button>
                {isSpeaking && (
                  <button 
                    onClick={stopSpeaking} 
                    className="stop-btn"
                    title="Stop speaking"
                  >
                    ⏹️
                  </button>
                )}
              </div>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Ask something about the PDF..."
        />
        <button onClick={sendMessage}>
          <span role="img" aria-label="send">📤</span>
          Send
        </button>
      </div>
    </div>
  );
}
