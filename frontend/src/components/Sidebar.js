import React, { useState } from 'react';
import CreateProjectModal from './CreateProjectModal';

function Sidebar({ projects, currentProject, onSelectProject, onProjectsUpdate, onLogout }) {
  const [showCreateModal, setShowCreateModal] = useState(false);

  return (
    <>
      <div className="sidebar">
        <div className="sidebar-header">
          <div className="logo">CHATBOT</div>
        </div>

        <div className="sidebar-content">
          <div className="section-title">Projects</div>

          <button
            className="create-project-btn"
            onClick={() => setShowCreateModal(true)}
          >
            + New Project
          </button>

          {projects.length === 0 ? (
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
              No projects yet
            </p>
          ) : (
            projects.map((project) => (
              <div
                key={project.id}
                className={`project-card ${currentProject?.id === project.id ? 'active' : ''}`}
                onClick={() => onSelectProject(project)}
              >
                <div className="project-name">{project.name}</div>
                {project.description && (
                  <div className="project-desc">{project.description}</div>
                )}
              </div>
            ))
          )}

          <button className="logout-btn" onClick={onLogout}>
            Logout
          </button>
        </div>
      </div>

      {showCreateModal && (
        <CreateProjectModal
          onClose={() => setShowCreateModal(false)}
          onCreateProject={onProjectsUpdate}
        />
      )}
    </>
  );
}

export default Sidebar;
