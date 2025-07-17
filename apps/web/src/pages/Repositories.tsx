import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "./Repositories.css";

interface Repository {
  id: number;
  repository_hash: string | null;
  name: string;
  full_name: string;
  url: string;
  remote_url: string | null;
  branch: string;
  description: string | null;
  is_local: boolean;
  created_at: string;
  updated_at: string;
}

export const RepositoriesPage: React.FC = () => {
  const [repositories, setRepositories] = useState<Repository[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchRepositories = async () => {
      try {
        const response = await fetch("/api/v1/repositories/");
        if (!response.ok) {
          throw new Error("Failed to fetch repositories");
        }
        const data: Repository[] = await response.json();
        setRepositories(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load repositories");
      } finally {
        setLoading(false);
      }
    };

    fetchRepositories();
  }, []);

  if (loading) {
    return (
      <div className="repositories-page">
        <div className="loading">Loading repositories...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="repositories-page">
        <div className="error-message">
          <h1>Error</h1>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="repositories-page">
      <div className="page-header">
        <h1>Repositories</h1>
        <p className="subtitle">Browse available repositories</p>
      </div>

      <div className="repositories-grid">
        {repositories.length === 0 ? (
          <div className="empty-state">
            <p>No repositories found</p>
          </div>
        ) : (
          repositories.map((repo) => (
            <div key={repo.id} className="repository-card">
              <h3>{repo.full_name || repo.name}</h3>
              
              <div className="repo-details">
                <div className="detail-row">
                  <span className="label">Local Path:</span>
                  <span className="value">{repo.url}</span>
                </div>
                
                {repo.remote_url && (
                  <div className="detail-row">
                    <span className="label">Remote:</span>
                    <span className="value">{repo.remote_url}</span>
                  </div>
                )}
                
                <div className="detail-row">
                  <span className="label">Branch:</span>
                  <span className="value">{repo.branch}</span>
                </div>
                
                {repo.description && (
                  <div className="detail-row">
                    <span className="label">Description:</span>
                    <span className="value">{repo.description}</span>
                  </div>
                )}
              </div>

              <div className="repo-actions">
                {repo.repository_hash ? (
                  <Link 
                    to={`/repository/${repo.repository_hash}/browse`}
                    className="btn btn-primary"
                  >
                    Browse Commits
                  </Link>
                ) : (
                  <div className="no-hash-warning">
                    Repository hash not generated yet. Run update-repository-hashes.py
                  </div>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};