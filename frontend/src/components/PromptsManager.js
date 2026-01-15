import React, { useState, useEffect, useCallback } from 'react';
import { promptService } from '../services/api';

function PromptsManager({ projectId }) {
  const [expanded, setExpanded] = useState(false);
  const [prompts, setPrompts] = useState([]);
  const [newPrompt, setNewPrompt] = useState('');
  const [loading, setLoading] = useState(false);

  const loadPrompts = useCallback(async () => {
    try {
      const data = await promptService.getPrompts(projectId);
      setPrompts(data.prompts || []);
    } catch (err) {
      console.error('Failed to load prompts:', err);
    }
  }, [projectId]);

  useEffect(() => {
    if (expanded && projectId) {
      loadPrompts();
    }
  }, [expanded, projectId, loadPrompts]);

  const handleAddPrompt = async (e) => {
    e.preventDefault();
    if (!newPrompt.trim()) return;

    setLoading(true);
    try {
      await promptService.addPrompt(projectId, newPrompt);
      setNewPrompt('');
      loadPrompts();
    } catch (err) {
      console.error('Failed to add prompt:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="prompts-section">
      <div className="prompts-toggle" onClick={() => setExpanded(!expanded)}>
        <span>System Prompts</span>
        <span>{expanded ? '▼' : '▶'}</span>
      </div>

      {expanded && (
        <div className="prompts-content">
          {prompts.length > 0 && (
            <div style={{ marginBottom: '1rem' }}>
              <div className="section-title">Current Prompts</div>
              {prompts.map((prompt, index) => (
                <div key={index} className="prompt-item">
                  {prompt.content}
                </div>
              ))}
            </div>
          )}

          <form onSubmit={handleAddPrompt}>
            <div className="form-group">
              <label>Add New Prompt</label>
              <textarea
                value={newPrompt}
                onChange={(e) => setNewPrompt(e.target.value)}
                placeholder="Enter system prompt..."
              />
            </div>
            <button type="submit" className="btn" disabled={loading}>
              {loading ? 'Adding...' : 'Add Prompt'}
            </button>
          </form>
        </div>
      )}
    </div>
  );
}

export default PromptsManager;
