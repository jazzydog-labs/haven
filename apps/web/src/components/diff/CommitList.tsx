import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronRightIcon } from '@heroicons/react/24/outline';

interface Commit {
  id: string;
  hash: string;
  message: string;
  author: string;
  date: string;
  reviewStatus: 'pending' | 'approved' | 'needs_revision' | 'draft';
  filesChanged: number;
  insertions: number;
  deletions: number;
}

interface CommitListProps {
  repositoryId?: string;
  branch?: string;
  limit?: number;
}

const CommitList: React.FC<CommitListProps> = ({ 
  repositoryId = '1', 
  branch = 'main', 
  limit = 20 
}) => {
  const navigate = useNavigate();
  const [commits, setCommits] = useState<Commit[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'pending' | 'approved' | 'needs_revision'>('all');

  useEffect(() => {
    loadCommits();
  }, [repositoryId, branch, limit]);

  const loadCommits = async () => {
    try {
      setLoading(true);
      
      // Mock data - in reality this would come from the API
      const mockCommits: Commit[] = [
        {
          id: '1',
          hash: 'a1b2c3d4e5f6g7h8',
          message: 'feat: Add enhanced diff viewer with syntax highlighting',
          author: 'John Doe',
          date: '2025-07-17',
          reviewStatus: 'pending',
          filesChanged: 3,
          insertions: 245,
          deletions: 12
        },
        {
          id: '2',
          hash: 'b2c3d4e5f6g7h8i9',
          message: 'fix: Resolve navigation issues in commit viewer',
          author: 'Jane Smith',
          date: '2025-07-16',
          reviewStatus: 'approved',
          filesChanged: 2,
          insertions: 28,
          deletions: 15
        },
        {
          id: '3',
          hash: 'c3d4e5f6g7h8i9j0',
          message: 'docs: Update README with new diff viewer features',
          author: 'Bob Johnson',
          date: '2025-07-16',
          reviewStatus: 'needs_revision',
          filesChanged: 1,
          insertions: 45,
          deletions: 8
        },
        {
          id: '4',
          hash: 'd4e5f6g7h8i9j0k1',
          message: 'refactor: Extract common components from diff viewer\n\nThis refactoring improves code reusability and makes the codebase more maintainable by extracting shared components.',
          author: 'Alice Wilson',
          date: '2025-07-15',
          reviewStatus: 'approved',
          filesChanged: 5,
          insertions: 120,
          deletions: 85
        },
        {
          id: '5',
          hash: 'e5f6g7h8i9j0k1l2',
          message: 'chore: Update dependencies and fix security vulnerabilities',
          author: 'Charlie Brown',
          date: '2025-07-15',
          reviewStatus: 'draft',
          filesChanged: 1,
          insertions: 15,
          deletions: 10
        }
      ];

      setCommits(mockCommits);
    } catch (error) {
      console.error('Failed to load commits:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'approved':
        return 'text-green-600 bg-green-100';
      case 'needs_revision':
        return 'text-red-600 bg-red-100';
      case 'draft':
        return 'text-gray-600 bg-gray-100';
      default:
        return 'text-yellow-600 bg-yellow-100';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'approved':
        return '✅';
      case 'needs_revision':
        return '❌';
      case 'draft':
        return '📝';
      default:
        return '⏳';
    }
  };

  const filteredCommits = commits.filter(commit => {
    if (filter === 'all') return true;
    return commit.reviewStatus === filter;
  });

  const getCommitSummary = (message: string) => {
    return message.split('\n')[0];
  };

  const hasDescription = (message: string) => {
    return message.includes('\n');
  };

  if (loading) {
    return (
      <div className="space-y-4">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="animate-pulse">
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <div className="flex items-center space-x-4">
                <div className="h-10 w-16 bg-gray-200 rounded"></div>
                <div className="flex-1 space-y-2">
                  <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                  <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="commit-list">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-bold text-gray-900">Recent Commits</h2>
          
          {/* Filter */}
          <div className="flex space-x-1 bg-gray-100 rounded-lg p-1">
            {['all', 'pending', 'approved', 'needs_revision'].map((filterOption) => (
              <button
                key={filterOption}
                onClick={() => setFilter(filterOption as any)}
                className={`px-3 py-1 text-sm font-medium rounded-md transition-colors ${
                  filter === filterOption
                    ? 'bg-white text-gray-900 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                {filterOption === 'all' ? 'All' : 
                 filterOption === 'needs_revision' ? 'Needs Review' :
                 filterOption.charAt(0).toUpperCase() + filterOption.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Stats */}
        <div className="mt-4 grid grid-cols-4 gap-4">
          <div className="bg-white p-3 rounded-lg border border-gray-200">
            <div className="text-2xl font-bold text-gray-900">{commits.length}</div>
            <div className="text-sm text-gray-500">Total</div>
          </div>
          <div className="bg-white p-3 rounded-lg border border-gray-200">
            <div className="text-2xl font-bold text-yellow-600">
              {commits.filter(c => c.reviewStatus === 'pending').length}
            </div>
            <div className="text-sm text-gray-500">Pending</div>
          </div>
          <div className="bg-white p-3 rounded-lg border border-gray-200">
            <div className="text-2xl font-bold text-green-600">
              {commits.filter(c => c.reviewStatus === 'approved').length}
            </div>
            <div className="text-sm text-gray-500">Approved</div>
          </div>
          <div className="bg-white p-3 rounded-lg border border-gray-200">
            <div className="text-2xl font-bold text-red-600">
              {commits.filter(c => c.reviewStatus === 'needs_revision').length}
            </div>
            <div className="text-sm text-gray-500">Need Revision</div>
          </div>
        </div>
      </div>

      {/* Commit List */}
      <div className="space-y-3">
        {filteredCommits.map((commit) => (
          <div
            key={commit.id}
            onClick={() => navigate(`/diffs/commit/${commit.hash}`)}
            className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
          >
            <div className="flex items-start space-x-4">
              {/* Commit Hash */}
              <div className="flex-shrink-0">
                <div className="font-mono text-sm bg-gray-100 px-3 py-2 rounded border">
                  {commit.hash.substring(0, 8)}
                </div>
              </div>

              {/* Commit Info */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center space-x-2 mb-2">
                  <h3 className="text-lg font-medium text-gray-900 truncate">
                    {getCommitSummary(commit.message)}
                  </h3>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(commit.reviewStatus)}`}>
                    {getStatusIcon(commit.reviewStatus)} {commit.reviewStatus.replace('_', ' ')}
                  </span>
                </div>

                {hasDescription(commit.message) && (
                  <p className="text-sm text-gray-600 mb-2 line-clamp-2">
                    {commit.message.split('\n').slice(1).join('\n').trim()}
                  </p>
                )}

                <div className="flex items-center space-x-4 text-sm text-gray-500">
                  <span>by <span className="font-medium">{commit.author}</span></span>
                  <span>{commit.date}</span>
                  <span>{commit.filesChanged} files</span>
                  <span className="text-green-600">+{commit.insertions}</span>
                  <span className="text-red-600">-{commit.deletions}</span>
                </div>
              </div>

              {/* Arrow */}
              <div className="flex-shrink-0">
                <ChevronRightIcon className="h-5 w-5 text-gray-400" />
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredCommits.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-400 text-6xl mb-4">📝</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            No commits found
          </h3>
          <p className="text-gray-600">
            {filter === 'all' 
              ? 'No commits available for this repository.'
              : `No commits with status "${filter.replace('_', ' ')}" found.`
            }
          </p>
        </div>
      )}
    </div>
  );
};

export default CommitList;