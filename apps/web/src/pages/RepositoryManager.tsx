import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "./RepositoryManager.css";

interface Repository {
  id: number;
  repository_hash: string | null;
  slug: string | null;
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

interface RepositoryStats {
  total_commits: number;
  total_branches: number;
  latest_commit_date: string | null;
  oldest_commit_date: string | null;
}

interface LoadingState {
  [key: string]: boolean;
}

export const RepositoryManagerPage: React.FC = () => {
  const [repositories, setRepositories] = useState<Repository[]>([]);
  const [repositoryStats, setRepositoryStats] = useState<{[key: string]: RepositoryStats}>({});
  const [loading, setLoading] = useState(true);
  const [loadingStats, setLoadingStats] = useState<LoadingState>({});
  const [loadingCommits, setLoadingCommits] = useState<LoadingState>({});
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchRepositories();
  }, []);

  const fetchRepositories = async () => {
    try {
      const response = await fetch("/api/v1/repositories/");
      if (!response.ok) {
        throw new Error("Failed to fetch repositories");
      }
      const data: Repository[] = await response.json();
      setRepositories(data);
      
      // Fetch stats for each repository
      data.forEach(repo => {
        if (repo.slug || repo.repository_hash) {
          fetchRepositoryStats(repo.slug || repo.repository_hash!);
        }
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load repositories");
    } finally {
      setLoading(false);
    }
  };

  const fetchRepositoryStats = async (identifier: string) => {
    setLoadingStats(prev => ({ ...prev, [identifier]: true }));
    try {
      const response = await fetch(`/api/v1/repository-management/${identifier}/stats`);
      if (!response.ok) {
        throw new Error("Failed to fetch stats");
      }
      const data: RepositoryStats = await response.json();
      setRepositoryStats(prev => ({ ...prev, [identifier]: data }));
    } catch (err) {
      console.error(`Failed to fetch stats for ${identifier}:`, err);
    } finally {
      setLoadingStats(prev => ({ ...prev, [identifier]: false }));
    }
  };

  const loadCommits = async (identifier: string, branch: string = "main") => {
    setLoadingCommits(prev => ({ ...prev, [identifier]: true }));
    try {
      const response = await fetch(`/api/v1/repository-management/${identifier}/load-commits`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          branch,
          limit: null, // Load all commits
        }),
      });
      
      if (!response.ok) {
        throw new Error("Failed to start loading commits");
      }
      
      const data = await response.json();
      alert(`Started loading commits: ${data.message}`);
      
      // Refresh stats after a delay
      setTimeout(() => {
        fetchRepositoryStats(identifier);
      }, 3000);
    } catch (err) {
      alert(`Failed to load commits: ${err instanceof Error ? err.message : "Unknown error"}`);
    } finally {
      setLoadingCommits(prev => ({ ...prev, [identifier]: false }));
    }
  };

  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return "N/A";
    return new Date(dateStr).toLocaleDateString();
  };

  if (loading) {
    return (
      <div className="repository-manager-page">
        <div className="loading">Loading repositories...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="repository-manager-page">
        <div className="error-message">
          <h1>Error</h1>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="repository-manager-page">
      <div className="page-header">
        <h1>Repository Manager</h1>
        <p className="subtitle">Manage repositories and load commit history</p>
      </div>

      <div className="repositories-list">
        {repositories.length === 0 ? (
          <div className="empty-state">
            <p>No repositories found</p>
          </div>
        ) : (
          repositories.map((repo) => {
            const identifier = repo.slug || repo.repository_hash || "";
            const stats = repositoryStats[identifier];
            const isLoadingStats = loadingStats[identifier];
            const isLoadingCommits = loadingCommits[identifier];
            
            return (
              <div key={repo.id} className="repository-card">
                <div className="repo-header">
                  <h3>{repo.full_name || repo.name}</h3>
                  <div className="repo-actions">
                    <Link 
                      to={`/repository/${identifier}/browse`}
                      className="btn btn-secondary"
                    >
                      Browse
                    </Link>
                  </div>
                </div>
                
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
                    <span className="label">Default Branch:</span>
                    <span className="value">{repo.branch}</span>
                  </div>
                </div>

                <div className="repo-stats">
                  {isLoadingStats ? (
                    <div className="loading-inline">Loading stats...</div>
                  ) : stats ? (
                    <>
                      <div className="stat-item">
                        <span className="stat-label">Commits:</span>
                        <span className="stat-value">{stats.total_commits}</span>
                      </div>
                      <div className="stat-item">
                        <span className="stat-label">Branches:</span>
                        <span className="stat-value">{stats.total_branches}</span>
                      </div>
                      <div className="stat-item">
                        <span className="stat-label">Latest:</span>
                        <span className="stat-value">{formatDate(stats.latest_commit_date)}</span>
                      </div>
                      <div className="stat-item">
                        <span className="stat-label">Oldest:</span>
                        <span className="stat-value">{formatDate(stats.oldest_commit_date)}</span>
                      </div>
                    </>
                  ) : (
                    <div className="no-stats">No statistics available</div>
                  )}
                </div>

                <div className="repo-manager-actions">
                  {stats && stats.total_commits === 0 ? (
                    <button
                      className="btn btn-primary"
                      onClick={() => loadCommits(identifier, repo.branch)}
                      disabled={isLoadingCommits}
                    >
                      {isLoadingCommits ? "Loading..." : "Load All Commits"}
                    </button>
                  ) : (
                    <button
                      className="btn btn-secondary"
                      onClick={() => loadCommits(identifier, repo.branch)}
                      disabled={isLoadingCommits}
                    >
                      {isLoadingCommits ? "Loading..." : "Refresh Commits"}
                    </button>
                  )}
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};