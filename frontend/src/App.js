import React, { useState, useEffect, useCallback } from 'react';
import './App.css';
import AuthPage from './components/AuthPage';
import Sidebar from './components/Sidebar';
import ChatInterface from './components/ChatInterface';
import PromptsManager from './components/PromptsManager';
import { projectService } from './services/api';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [projects, setProjects] = useState([]);
  const [currentProject, setCurrentProject] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadProjects = useCallback(async () => {
    try {
      const data = await projectService.getProjects();
      setProjects(data.projects || []);
    } catch (err) {
      console.error('Failed to load projects:', err);
      handleLogout();
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      setIsAuthenticated(true);
      loadProjects();
    } else {
      setLoading(false);
    }
  }, [loadProjects]);

  const handleLogin = () => {
    setIsAuthenticated(true);
    loadProjects();
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    setIsAuthenticated(false);
    setProjects([]);
    setCurrentProject(null);
  };

  const handleSelectProject = (project) => {
    setCurrentProject(project);
  };

  if (loading) {
    return (
      <div className="loading">
        <p>Loading...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <AuthPage onLogin={handleLogin} />;
  }

  return (
    <div className="app-container">
      <Sidebar
        projects={projects}
        currentProject={currentProject}
        onSelectProject={handleSelectProject}
        onProjectsUpdate={loadProjects}
        onLogout={handleLogout}
      />

      <div className="main-content">
        {currentProject ? (
          <>
            <div className="main-header">
              <h1 className="project-title">{currentProject.name}</h1>
              {currentProject.description && (
                <p style={{ color: 'var(--text-secondary)' }}>
                  {currentProject.description}
                </p>
              )}
              <PromptsManager projectId={currentProject.id} />
            </div>
            <ChatInterface project={currentProject} />
          </>
        ) : (
          <div className="empty-state">
            <div className="empty-state-icon">🚀</div>
            <h2>Welcome to Chatbot Platform</h2>
            <p>Select or create a project to start chatting</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
