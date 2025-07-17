import React, { useState, useEffect } from "react";
import "./CommitDiffViewer.css";

interface CommitInfo {
  id: number;
  repository_id: number;
  commit_hash: string;
  message: string;
  author_name: string;
  author_email: string;
  committed_at: string;
  diff_html_path?: string;
  diff_generated_at?: string;
  diff_stats: {
    files_changed: number;
    insertions: number;
    deletions: number;
  };
}

interface CommitReview {
  id: number;
  commit_id: number;
  reviewer_id: number;
  status: "pending_review" | "approved" | "needs_revision" | "draft";
  notes?: string;
  reviewed_at?: string;
}

interface CommitDiffViewerProps {
  commitHash: string;
  onReviewComplete?: () => void;
}

export const CommitDiffViewer: React.FC<CommitDiffViewerProps> = ({
  commitHash,
  onReviewComplete,
}) => {
  const [commit, setCommit] = useState<CommitInfo | null>(null);
  const [reviews, setReviews] = useState<CommitReview[]>([]);
  const [diffHtml, setDiffHtml] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [reviewStatus, setReviewStatus] =
    useState<CommitReview["status"]>("pending_review");
  const [reviewNotes, setReviewNotes] = useState("");

  // Fetch commit information
  const fetchCommit = async () => {
    try {
      // First get repository ID - we'll need to pass it as a query param
      // For now, assume repository_id=1 - in production, this would come from context
      const repositoryId = 1; // TODO: Get from route or context
      
      const response = await fetch(`/api/v1/commits/by-hash/${commitHash}?repository_id=${repositoryId}`);
      if (!response.ok) throw new Error("Failed to fetch commit");
      const data = await response.json();
      setCommit(data);

      // Fetch reviews
      const reviewsResponse = await fetch(
        `/api/v1/commits/${data.id}/reviews`
      );
      if (reviewsResponse.ok) {
        const reviewsData = await reviewsResponse.json();
        setReviews(reviewsData);
      }

      // Auto-generate diff if not available
      if (!data.diff_html_path) {
        await generateDiff(data.id);
      } else {
        await loadDiffHtml(data.id);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load commit");
    } finally {
      setLoading(false);
    }
  };

  // Load diff HTML content
  const loadDiffHtml = async (commitId: number) => {
    try {
      const response = await fetch(`/api/v1/commits/${commitId}/diff-html`);
      if (!response.ok) throw new Error("Failed to load diff");
      const html = await response.text();
      setDiffHtml(html);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load diff");
    }
  };

  // Generate diff if not available
  const generateDiff = async (commitId?: number) => {
    setGenerating(true);
    setError(null);

    try {
      const id = commitId || commit?.id;
      if (!id) throw new Error("No commit ID available");
      
      const response = await fetch(
        `/api/v1/commits/${id}/generate-diff`,
        {
          method: "POST",
        }
      );
      if (!response.ok) throw new Error("Failed to generate diff");

      // Reload commit and diff
      await fetchCommit();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate diff");
    } finally {
      setGenerating(false);
    }
  };

  // Submit review
  const submitReview = async () => {
    try {
      if (!commit) throw new Error("No commit loaded");
      
      const response = await fetch(`/api/v1/commits/${commit.id}/reviews`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          reviewer_id: 1, // TODO: Get from auth context
          status: reviewStatus,
          notes: reviewNotes,
        }),
      });

      if (!response.ok) throw new Error("Failed to submit review");

      // Refresh reviews
      await fetchCommit();

      // Clear form
      setReviewNotes("");

      if (onReviewComplete) {
        onReviewComplete();
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit review");
    }
  };

  useEffect(() => {
    fetchCommit();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [commitHash]);

  if (loading) {
    return <div className="commit-diff-viewer loading">Loading...</div>;
  }

  if (error) {
    return <div className="commit-diff-viewer error">{error}</div>;
  }

  if (!commit) {
    return <div className="commit-diff-viewer error">Commit not found</div>;
  }

  const getStatusClass = (status: CommitReview["status"]) => {
    switch (status) {
      case "approved":
        return "status-approved";
      case "needs_revision":
        return "status-needs-revision";
      case "draft":
        return "status-draft";
      default:
        return "status-pending";
    }
  };

  return (
    <div className="commit-diff-viewer">
      {/* Commit Header */}
      <div className="commit-header">
        <div className="commit-header-top">
          <h2>Commit {commit.commit_hash.substring(0, 7)}</h2>
          <div className="review-badges">
            {reviews.map((review) => (
              <span
                key={review.id}
                className={`review-badge ${getStatusClass(review.status)}`}
              >
                {review.status.replace("_", " ")}
              </span>
            ))}
          </div>
        </div>

        <h3 className="commit-message">{commit.message}</h3>

        <div className="commit-meta">
          <span>
            <strong>Author:</strong> {commit.author_name} ({commit.author_email}
            )
          </span>
          <span>
            <strong>Date:</strong>{" "}
            {new Date(commit.committed_at).toLocaleString()}
          </span>
        </div>

        <div className="diff-stats">
          <span className="stat">{commit.diff_stats.files_changed} files</span>
          <span className="stat additions">
            +{commit.diff_stats.insertions}
          </span>
          <span className="stat deletions">-{commit.diff_stats.deletions}</span>
        </div>
      </div>

      {/* Diff Viewer */}
      <div className="diff-viewer-container">
        <div className="diff-viewer-header">
          <h3>Diff View</h3>
          {commit.diff_html_path && (
            <div className="diff-actions">
              <button
                onClick={() => generateDiff()}
                disabled={generating}
                className="btn btn-sm"
              >
                {generating ? "Generating..." : "Refresh"}
              </button>
              <button
                onClick={() =>
                  window.open(`/api/v1/commits/${commit.id}/diff-html`, "_blank")
                }
                className="btn btn-sm"
              >
                Open in New Tab
              </button>
            </div>
          )}
        </div>

        <div className="diff-viewer-content">
          {commit.diff_html_path && diffHtml ? (
            <div
              className="diff-html-container"
              dangerouslySetInnerHTML={{ __html: diffHtml }}
            />
          ) : commit.diff_html_path && !diffHtml ? (
            <div className="loading">Loading diff...</div>
          ) : (
            <div className="no-diff">
              <p>No diff generated yet</p>
              <button
                onClick={() => generateDiff()}
                disabled={generating}
                className="btn btn-primary"
              >
                {generating ? "Generating..." : "Generate Diff"}
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Review Form */}
      <div className="review-form">
        <h3>Submit Review</h3>

        <div className="form-group">
          <label htmlFor="review-status">Review Status</label>
          <select
            id="review-status"
            value={reviewStatus}
            onChange={(e) =>
              setReviewStatus(e.target.value as CommitReview["status"])
            }
            className="form-control"
          >
            <option value="pending_review">Pending Review</option>
            <option value="approved">Approved</option>
            <option value="needs_revision">Needs Revision</option>
            <option value="draft">Draft</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="review-notes">Review Notes</label>
          <textarea
            id="review-notes"
            rows={4}
            value={reviewNotes}
            onChange={(e) => setReviewNotes(e.target.value)}
            className="form-control"
            placeholder="Add your review comments here..."
          />
        </div>

        <button onClick={submitReview} className="btn btn-primary">
          Submit Review
        </button>
      </div>

      {/* Previous Reviews */}
      {reviews.length > 0 && (
        <div className="review-history">
          <h3>Review History</h3>

          {reviews.map((review) => (
            <div key={review.id} className="review-item">
              <div className="review-item-header">
                <span
                  className={`review-badge ${getStatusClass(review.status)}`}
                >
                  {review.status.replace("_", " ")}
                </span>
                <span className="review-date">
                  {review.reviewed_at
                    ? new Date(review.reviewed_at).toLocaleString()
                    : "Not reviewed yet"}
                </span>
              </div>
              {review.notes && <p className="review-notes">{review.notes}</p>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
