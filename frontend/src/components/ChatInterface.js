import React, { useState, useEffect, useRef } from 'react';
import { chatService } from '../services/api';

function ChatInterface({ project }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Reset chat when project changes
  useEffect(() => {
    setMessages([]);
    setSessionId(null);
  }, [project.id]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await chatService.sendMessage(project.id, input, sessionId);

      if (!sessionId) {
        setSessionId(response.session_id);
      }

      const assistantMessage = {
        role: 'assistant',
        content: response.assistant_message.content,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Failed to send message:', err);
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, there was an error processing your message.',
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setMessages([]);
    setSessionId(null);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend(e);
    }
  };

  return (
    <div className="chat-area">
      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">💬</div>
            <p>Start a conversation</p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div key={index} className={`message ${message.role}`}>
              <div className="message-role">
                {message.role === 'user' ? 'You' : 'Assistant'}
              </div>
              <div className="message-content">{message.content}</div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <form onSubmit={handleSend}>
          <div className="chat-input-wrapper">
            <textarea
              className="chat-input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type your message... (Shift+Enter for new line)"
              disabled={loading}
            />
            <button type="submit" className="send-btn" disabled={loading}>
              {loading ? 'Sending...' : 'Send'}
            </button>
          </div>
        </form>

        <div className="chat-controls">
          <button className="clear-btn" onClick={handleClear}>
            Clear Chat
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatInterface;
