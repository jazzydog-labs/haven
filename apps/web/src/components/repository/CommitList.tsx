import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./CommitList.css";

interface CommitInfo {
  id: number;
  repository_id: number;
  commit_hash: string;
  message: string;
  author_name: string;
  author_email: string;
  committed_at: string;
  diff_stats: {
    files_changed: number;
    insertions: number;
    deletions: number;
  };
  diff_html_path?: string;
  diff_generated_at?: string;
}

interface PaginatedResponse {
  items: CommitInfo[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

interface CommitListProps {
  repositoryId: number;
  onCommitSelect?: (commitId: number) => void;
  selectedCommitId?: number | null;
}

export const CommitList: React.FC<CommitListProps> = ({
  repositoryId,
  onCommitSelect,
  selectedCommitId,
}) => {
  const navigate = useNavigate();
  const [commits, setCommits] = useState<CommitInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [pageSize] = useState(20);
  const [totalPages, setTotalPages] = useState(0);
  const [total, setTotal] = useState(0);

  // Fetch commits
  const fetchCommits = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `/api/v1/commits/paginated?repository_id=${repositoryId}&page=${page}&page_size=${pageSize}`
      );
      
      if (!response.ok) {
        throw new Error("Failed to fetch commits");
      }

      const data: PaginatedResponse = await response.json();
      setCommits(data.items);
      setTotal(data.total);
      setTotalPages(data.total_pages);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load commits");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCommits();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [repositoryId, page]);

  const handleCommitClick = (commit: CommitInfo) => {
    if (onCommitSelect) {
      onCommitSelect(commit.id);
    }
    // Navigate to commit review page
    navigate(`/commits/${commit.id}/review`);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + " " + date.toLocaleTimeString();
  };

  const truncateMessage = (message: string, maxLength: number = 80) => {
    if (message.length <= maxLength) return message;
    return message.substring(0, maxLength - 3) + "...";
  };

  if (loading) {
    return <div className="commit-list loading">Loading commits...</div>;
  }

  if (error) {
    return <div className="commit-list error">{error}</div>;
  }

  if (commits.length === 0) {
    return (
      <div className="commit-list empty">
        <p>No commits found for this repository</p>
      </div>
    );
  }

  return (
    <div className="commit-list">
      <div className="list-header">
        <h2>Commits</h2>
        <div className="commit-count">{total} total commits</div>
      </div>

      <div className="commits-container">
        {commits.map((commit) => (
          <div
            key={commit.id}
            className={`commit-item ${
              selectedCommitId === commit.id ? "selected" : ""
            }`}
            onClick={() => handleCommitClick(commit)}
          >
            <div className="commit-header">
              <span className="commit-hash">{commit.commit_hash.substring(0, 7)}</span>
              <span className="commit-date">{formatDate(commit.committed_at)}</span>
            </div>
            
            <div className="commit-message">
              {truncateMessage(commit.message)}
            </div>
            
            <div className="commit-meta">
              <span className="commit-author">
                <strong>{commit.author_name}</strong>
              </span>
              <div className="commit-stats">
                <span className="stat files">{commit.diff_stats.files_changed} files</span>
                <span className="stat additions">+{commit.diff_stats.insertions}</span>
                <span className="stat deletions">-{commit.diff_stats.deletions}</span>
                {commit.diff_html_path && (
                  <span className="stat diff-ready" title="Diff generated">
                    📄
                  </span>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {totalPages > 1 && (
        <div className="pagination">
          <button
            className="btn-page"
            onClick={() => setPage(p => Math.max(1, p - 1))}
            disabled={page === 1}
          >
            Previous
          </button>
          
          <span className="page-info">
            Page {page} of {totalPages}
          </span>
          
          <button
            className="btn-page"
            onClick={() => setPage(p => Math.min(totalPages, p + 1))}
            disabled={page === totalPages}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};