import React, { useState, useEffect } from "react";
import "./BranchSelector.css";

interface BranchSelectorProps {
  repositoryIdentifier: string;
  currentBranch: string;
  onBranchChange: (branch: string) => void;
}

export const BranchSelector: React.FC<BranchSelectorProps> = ({
  repositoryIdentifier,
  currentBranch,
  onBranchChange,
}) => {
  const [branches, setBranches] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const fetchBranches = async () => {
      try {
        const response = await fetch(`/api/v1/repositories/${repositoryIdentifier}/branches`);
        if (!response.ok) {
          throw new Error("Failed to fetch branches");
        }
        const data: string[] = await response.json();
        setBranches(data);
      } catch (error) {
        console.error("Error fetching branches:", error);
        setBranches([currentBranch]); // Fallback to current branch
      } finally {
        setLoading(false);
      }
    };

    fetchBranches();
  }, [repositoryIdentifier, currentBranch]);

  const handleBranchSelect = (branch: string) => {
    if (branch !== currentBranch) {
      onBranchChange(branch);
    }
    setIsOpen(false);
  };

  if (loading) {
    return <div className="branch-selector-loading">Loading branches...</div>;
  }

  return (
    <div className="branch-selector">
      <button
        className="branch-selector-button"
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
        aria-haspopup="listbox"
      >
        <svg
          className="branch-icon"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
          />
        </svg>
        <span className="branch-name">{currentBranch}</span>
        <svg
          className={`chevron-icon ${isOpen ? "chevron-up" : ""}`}
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>

      {isOpen && (
        <div className="branch-dropdown">
          <div className="branch-list" role="listbox">
            {branches.map((branch) => (
              <button
                key={branch}
                className={`branch-item ${branch === currentBranch ? "branch-item-selected" : ""}`}
                onClick={() => handleBranchSelect(branch)}
                role="option"
                aria-selected={branch === currentBranch}
              >
                <span className="branch-item-name">{branch}</span>
                {branch === currentBranch && (
                  <svg
                    className="check-icon"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                )}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};