import React from "react";
import { useParams, useNavigate } from "react-router-dom";
import { CommitDiffViewer } from "../components/CommitDiffViewer";
import "./CommitReview.css";

export const CommitReviewPage: React.FC = () => {
  const { commitHash } = useParams<{ commitHash: string }>();
  const navigate = useNavigate();

  if (!commitHash) {
    return (
      <div className="commit-review-page">
        <div className="error-message">
          <h1>Invalid commit hash</h1>
        </div>
      </div>
    );
  }

  return (
    <div className="commit-review-page">
      <div className="page-header">
        <button className="btn-back" onClick={() => navigate(-1)}>
          ← Back to Commits
        </button>
      </div>

      <CommitDiffViewer
        commitHash={commitHash}
        onReviewComplete={() => {
          // Could navigate back or show a success message
          console.log("Review completed");
        }}
      />
    </div>
  );
};
