import React, { useState } from "react";
import { useParams } from "react-router-dom";
import { CommitList } from "../components/repository/CommitList";
import "./RepositoryBrowser.css";

export const RepositoryBrowserPage: React.FC = () => {
  const { repositoryId } = useParams<{ repositoryId: string }>();
  const [selectedCommitId, setSelectedCommitId] = useState<number | null>(null);

  if (!repositoryId) {
    return (
      <div className="repository-browser-page">
        <div className="error-message">
          <h1>Invalid repository ID</h1>
        </div>
      </div>
    );
  }

  return (
    <div className="repository-browser-page">
      <div className="page-header">
        <h1>Repository Browser</h1>
        <p className="subtitle">Browse commits and changes</p>
      </div>

      <div className="browser-content">
        <CommitList
          repositoryId={parseInt(repositoryId, 10)}
          onCommitSelect={setSelectedCommitId}
          selectedCommitId={selectedCommitId}
        />
      </div>
    </div>
  );
};