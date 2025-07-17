import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { CommitList } from "../components/repository/CommitList";
import "./RepositoryBrowser.css";

interface RepositoryInfo {
  id: number;
  repository_hash: string;
  slug: string | null;
  name: string;
  full_name: string;
  url: string;  // Local path
  remote_url: string | null;
  branch: string;
  description: string | null;
  is_local: boolean;
  created_at: string;
  updated_at: string;
  commit_count: number;
  branch_count: number;
  current_branch: string | null;
}

export const RepositoryBrowserPage: React.FC = () => {
  const { repositoryHash } = useParams<{ repositoryHash: string }>();
  const [repository, setRepository] = useState<RepositoryInfo | null>(null);
  const [selectedCommitId, setSelectedCommitId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchRepository = async () => {
      if (!repositoryHash) return;
      
      try {
        const response = await fetch(`/api/v1/repositories/${repositoryHash}`);
        if (!response.ok) {
          throw new Error("Repository not found");
        }
        const data: RepositoryInfo = await response.json();
        setRepository(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load repository");
      } finally {
        setLoading(false);
      }
    };

    fetchRepository();
  }, [repositoryHash]);

  if (!repositoryHash) {
    return (
      <div className="repository-browser-page">
        <div className="error-message">
          <h1>Invalid repository hash</h1>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="repository-browser-page">
        <div className="loading">Loading repository...</div>
      </div>
    );
  }

  if (error || !repository) {
    return (
      <div className="repository-browser-page">
        <div className="error-message">
          <h1>Error</h1>
          <p>{error || "Repository not found"}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="repository-browser-page">
      <div className="page-header">
        <h1>{repository.full_name}</h1>
        <div className="repository-info">
          <div className="info-row">
            <span className="label">Local Path:</span>
            <span className="value">{repository.url}</span>
          </div>
          {repository.remote_url && (
            <div className="info-row">
              <span className="label">Remote URL:</span>
              <span className="value">{repository.remote_url}</span>
            </div>
          )}
          <div className="info-row">
            <span className="label">Current Branch:</span>
            <span className="value">{repository.current_branch || repository.branch}</span>
          </div>
          <div className="info-row">
            <span className="label">Total Commits:</span>
            <span className="value">{repository.commit_count}</span>
          </div>
          <div className="info-row">
            <span className="label">Branches:</span>
            <span className="value">{repository.branch_count}</span>
          </div>
          {repository.description && (
            <div className="info-row">
              <span className="label">Description:</span>
              <span className="value">{repository.description}</span>
            </div>
          )}
        </div>
      </div>

      <div className="browser-content">
        <CommitList
          repositoryId={repository.id}
          repositoryHash={repository.repository_hash}
          onCommitSelect={setSelectedCommitId}
          selectedCommitId={selectedCommitId}
        />
      </div>
    </div>
  );
};