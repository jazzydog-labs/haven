import React, { useState, useEffect, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import Fuse from 'fuse.js';
import { SearchInput } from "../common/SearchInput";
import { CommitFilters } from "./CommitFilters";
import { CommitTypeTag } from "./CommitTypeTag";
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
  review_status?: "pending_review" | "approved" | "needs_revision" | "draft";
  review_count?: number;
  latest_review_at?: string;
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
  repositoryHash?: string;
  onCommitSelect?: (commitId: number) => void;
  selectedCommitId?: number | null;
  branch?: string | null;
}

export const CommitList: React.FC<CommitListProps> = ({
  repositoryId,
  onCommitSelect,
  selectedCommitId,
  branch,
}) => {
  const navigate = useNavigate();
  const [commits, setCommits] = useState<CommitInfo[]>([]);
  const [allCommits, setAllCommits] = useState<CommitInfo[]>([]); // Store all commits for fuzzy search
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [pageSize] = useState(500);
  const [totalPages, setTotalPages] = useState(0);
  const [total, setTotal] = useState(0);
  const [searchMatches, setSearchMatches] = useState<Map<number, any>>(new Map()); // Store search match details
  const [isSearching, setIsSearching] = useState(false);

  // Search and filter states
  const [searchQuery, setSearchQuery] = useState("");
  const [authorFilter, setAuthorFilter] = useState("");
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");
  const [statusFilter, setStatusFilter] = useState<string[]>([]);
  
  // Applied filter states (actual filters being used)
  const [appliedSearchQuery, setAppliedSearchQuery] = useState("");
  const [appliedAuthorFilter, setAppliedAuthorFilter] = useState("");
  const [appliedDateFrom, setAppliedDateFrom] = useState("");
  const [appliedDateTo, setAppliedDateTo] = useState("");
  const [appliedStatusFilter, setAppliedStatusFilter] = useState<string[]>([]);

  // Check if any filters are active
  const hasActiveFilters = !!(appliedSearchQuery || appliedAuthorFilter || appliedDateFrom || appliedDateTo || appliedStatusFilter.length > 0);
  const hasPendingFilters = !!(searchQuery || authorFilter || dateFrom || dateTo || statusFilter.length > 0) && 
    (searchQuery !== appliedSearchQuery || authorFilter !== appliedAuthorFilter || 
     dateFrom !== appliedDateFrom || dateTo !== appliedDateTo || 
     JSON.stringify(statusFilter) !== JSON.stringify(appliedStatusFilter));

  // Build query parameters
  const buildQueryParams = () => {
    const params = new URLSearchParams({
      repository_id: repositoryId.toString(),
      page: page.toString(),
      page_size: pageSize.toString(),
    });

    if (appliedSearchQuery) params.append("search", appliedSearchQuery);
    if (appliedAuthorFilter) params.append("author", appliedAuthorFilter);
    if (appliedDateFrom) params.append("date_from", appliedDateFrom);
    if (appliedDateTo) params.append("date_to", appliedDateTo);
    if (branch) params.append("branch", branch);
    
    // Add status filters
    appliedStatusFilter.forEach(status => {
      params.append("status", status);
    });

    return params.toString();
  };

  // Fetch commits
  const fetchCommits = async () => {
    setLoading(true);
    setError(null);

    try {
      const queryParams = buildQueryParams();
      const response = await fetch(`/api/v1/commits/paginated-with-reviews?${queryParams}`);
      
      if (!response.ok) {
        throw new Error("Failed to fetch commits");
      }

      const data: PaginatedResponse = await response.json();
      setAllCommits(data.items);
      setCommits(data.items);
      setTotal(data.total);
      setTotalPages(data.total_pages);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load commits");
    } finally {
      setLoading(false);
    }
  };

  // Apply filters
  const applyFilters = () => {
    setAppliedSearchQuery(searchQuery);
    setAppliedAuthorFilter(authorFilter);
    setAppliedDateFrom(dateFrom);
    setAppliedDateTo(dateTo);
    setAppliedStatusFilter(statusFilter);
    setPage(1); // Reset to first page
  };

  // Clear all filters
  const clearFilters = () => {
    setSearchQuery("");
    setAuthorFilter("");
    setDateFrom("");
    setDateTo("");
    setStatusFilter([]);
    setAppliedSearchQuery("");
    setAppliedAuthorFilter("");
    setAppliedDateFrom("");
    setAppliedDateTo("");
    setAppliedStatusFilter([]);
    setPage(1); // Reset to first page
  };

  // Fuzzy search setup
  const fuse = useMemo(() => {
    return new Fuse(allCommits, {
      keys: ['message', 'commit_hash', 'author_name', 'author_email'],
      threshold: 0.3,
      includeScore: true,
      includeMatches: true,
      minMatchCharLength: 2,
    });
  }, [allCommits]);

  // Apply client-side fuzzy search with debouncing
  useEffect(() => {
    if (searchQuery && allCommits.length > 0) {
      setIsSearching(true);
      // Apply fuzzy search with a slight delay for better performance
      const timeoutId = setTimeout(() => {
        const results = fuse.search(searchQuery);
        
        // Store match information for highlighting
        const matchMap = new Map();
        results.forEach(result => {
          if (result.item.id) {
            matchMap.set(result.item.id, result.matches);
          }
        });
        setSearchMatches(matchMap);
        
        setCommits(results.map(result => result.item));
        setIsSearching(false);
      }, 150); // 150ms debounce

      return () => {
        clearTimeout(timeoutId);
        setIsSearching(false);
      };
    } else {
      setCommits(allCommits);
      setSearchMatches(new Map());
      setIsSearching(false);
    }
  }, [searchQuery, allCommits, fuse]);

  useEffect(() => {
    fetchCommits();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [repositoryId, page, appliedSearchQuery, appliedAuthorFilter, appliedDateFrom, appliedDateTo, appliedStatusFilter]);

  const handleCommitClick = (commit: CommitInfo) => {
    if (onCommitSelect) {
      onCommitSelect(commit.id);
    }
    // Navigate to commit review page using hash
    navigate(`/commits/${commit.commit_hash}/review`);
  };

  const getReviewStatusBadge = (status?: string) => {
    if (!status) return null;
    
    const statusColors = {
      pending_review: "badge-pending",
      approved: "badge-approved",
      needs_revision: "badge-needs-revision",
      draft: "badge-draft"
    };
    
    const statusLabels = {
      pending_review: "Pending Review",
      approved: "Approved",
      needs_revision: "Needs Revision",
      draft: "Draft"
    };
    
    return (
      <span className={`review-badge ${statusColors[status as keyof typeof statusColors]}`}>
        {statusLabels[status as keyof typeof statusLabels]}
      </span>
    );
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + " " + date.toLocaleTimeString();
  };

  const truncateMessage = (message: string, maxLength: number = 60) => {
    // Remove conventional commit prefix if present (e.g., "feat: ", "fix: ", "docs: ")
    const cleanMessage = message.replace(/^(feat|fix|docs|style|refactor|test|chore|ci|build|perf|revert):\s*/i, '');
    
    if (cleanMessage.length <= maxLength) return cleanMessage;
    return cleanMessage.substring(0, maxLength - 3) + "...";
  };

  const highlightMatch = (text: string, matches: any[] | undefined, fieldKey: string): React.ReactNode => {
    if (!matches || !searchQuery) return text;
    
    const match = matches.find(m => m.key === fieldKey);
    if (!match || !match.indices || match.indices.length === 0) return text;
    
    const parts: React.ReactNode[] = [];
    let lastIndex = 0;
    
    // Sort indices by start position
    const sortedIndices = [...match.indices].sort((a, b) => a[0] - b[0]);
    
    sortedIndices.forEach(([start, end], i) => {
      // Add text before match
      if (start > lastIndex) {
        parts.push(text.substring(lastIndex, start));
      }
      // Add highlighted match
      parts.push(
        <span key={i} className="search-highlight">
          {text.substring(start, end + 1)}
        </span>
      );
      lastIndex = end + 1;
    });
    
    // Add remaining text
    if (lastIndex < text.length) {
      parts.push(text.substring(lastIndex));
    }
    
    return <>{parts}</>;
  };

  return (
    <div className="commit-list">
      <div className="list-header">
        <h2>Commits</h2>
        <div className="commit-count">
          {isSearching ? (
            <span className="searching-indicator">Searching...</span>
          ) : searchQuery ? (
            <span>{commits.length} results found</span>
          ) : (
            <span>{total} total commits{hasActiveFilters && " (filtered)"}</span>
          )}
        </div>
      </div>

      {/* Search Bar */}
      <div className="mb-4">
        <SearchInput
          value={searchQuery}
          onChange={setSearchQuery}
          placeholder="Search commits by message or hash..."
          className="w-full"
        />
      </div>

      {/* Filters */}
      <CommitFilters
        author={authorFilter}
        dateFrom={dateFrom}
        dateTo={dateTo}
        statusFilter={statusFilter}
        onAuthorChange={setAuthorFilter}
        onDateFromChange={setDateFrom}
        onDateToChange={setDateTo}
        onStatusFilterChange={setStatusFilter}
        onClearFilters={clearFilters}
        onApplyFilters={applyFilters}
        hasActiveFilters={hasActiveFilters}
        hasPendingFilters={hasPendingFilters}
      />

      <div className="commits-container">
        {loading ? (
          <div className="loading-container">Loading commits...</div>
        ) : error ? (
          <div className="error-container">{error}</div>
        ) : commits.length === 0 ? (
          <div className="empty-container">
            <p>No commits found{hasActiveFilters ? " matching your filters" : ""}</p>
          </div>
        ) : (
          commits.map((commit) => (
          <div
            key={commit.id}
            className={`commit-item compact ${
              selectedCommitId === commit.id ? "selected" : ""
            }`}
            onClick={() => handleCommitClick(commit)}
          >
            <div className="commit-compact-line">
              <span className="commit-hash">
                {highlightMatch(commit.commit_hash.substring(0, 7), searchMatches.get(commit.id), 'commit_hash')}
              </span>
              <CommitTypeTag message={commit.message} />
              <span className="commit-message">
                {highlightMatch(truncateMessage(commit.message), searchMatches.get(commit.id), 'message')}
              </span>
              <div className="commit-right-info">
                <span className="commit-author">
                  {highlightMatch(commit.author_name, searchMatches.get(commit.id), 'author_name')}
                </span>
                <div className="commit-stats">
                  <span className="stat files">{commit.diff_stats.files_changed}f</span>
                  <span className="stat additions">+{commit.diff_stats.insertions}</span>
                  <span className="stat deletions">-{commit.diff_stats.deletions}</span>
                  {commit.diff_html_path && (
                    <span className="stat diff-ready" title="Diff generated">📄</span>
                  )}
                </div>
                {getReviewStatusBadge(commit.review_status)}
                <span className="commit-date">{formatDate(commit.committed_at)}</span>
              </div>
            </div>
          </div>
          ))
        )}
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