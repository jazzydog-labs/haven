import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import DiffViewer from './DiffViewer';
import FileTree from './FileTree';
import ReviewPanel from './ReviewPanel';

interface Commit {
  id: string;
  hash: string;
  message: string;
  author: string;
  date: string;
  reviewStatus: 'pending' | 'approved' | 'needs_revision' | 'draft';
}

interface FileChange {
  path: string;
  type: 'added' | 'modified' | 'deleted' | 'renamed';
  insertions: number;
  deletions: number;
  oldPath?: string;
  diff?: string;
}

const CommitViewer: React.FC = () => {
  const { commitHash } = useParams<{ commitHash: string }>();
  const navigate = useNavigate();
  
  const [commit, setCommit] = useState<Commit | null>(null);
  const [files, setFiles] = useState<FileChange[]>([]);
  const [selectedFile, setSelectedFile] = useState<FileChange | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (commitHash) {
      loadCommitData(commitHash);
    }
  }, [commitHash]);

  const loadCommitData = async (hash: string) => {
    try {
      setLoading(true);
      setError(null);

      // Mock data for now - in reality this would come from the API
      const mockCommit: Commit = {
        id: '1',
        hash: hash,
        message: 'feat: Add enhanced diff viewer with syntax highlighting\n\nImplemented comprehensive diff viewer with:\n- Side-by-side and unified views\n- Syntax highlighting\n- File tree navigation\n- Review status tracking',
        author: 'John Doe',
        date: '2025-07-17',
        reviewStatus: 'pending'
      };

      const mockFiles: FileChange[] = [
        {
          path: 'apps/web/src/components/diff/DiffViewer.tsx',
          type: 'added',
          insertions: 245,
          deletions: 0,
          diff: `diff --git a/apps/web/src/components/diff/DiffViewer.tsx b/apps/web/src/components/diff/DiffViewer.tsx
new file mode 100644
index 0000000..a1b2c3d
--- /dev/null
+++ b/apps/web/src/components/diff/DiffViewer.tsx
@@ -0,0 +1,10 @@
+import React from 'react';
+
+const DiffViewer: React.FC = () => {
+  return (
+    <div className="diff-viewer">
+      <h1>Enhanced Diff Viewer</h1>
+    </div>
+  );
+};
+
+export default DiffViewer;`
        },
        {
          path: 'apps/web/src/components/diff/FileTree.tsx',
          type: 'added',
          insertions: 189,
          deletions: 0
        },
        {
          path: 'apps/web/package.json',
          type: 'modified',
          insertions: 3,
          deletions: 1
        }
      ];

      setCommit(mockCommit);
      setFiles(mockFiles);
      
      // Auto-select first file
      if (mockFiles.length > 0) {
        setSelectedFile(mockFiles[0]);
      }

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load commit data');
    } finally {
      setLoading(false);
    }
  };

  const handleReviewStatusChange = async (newStatus: string) => {
    if (!commit) return;

    try {
      // Update review status via API
      // await updateCommitReview(commit.id, newStatus);
      
      // Update local state
      setCommit({
        ...commit,
        reviewStatus: newStatus as any
      });
    } catch (err) {
      console.error('Failed to update review status:', err);
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

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        <span className="ml-2 text-gray-600">Loading commit data...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <div className="flex">
          <div className="text-red-400">⚠️</div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">Error</h3>
            <div className="mt-2 text-sm text-red-700">{error}</div>
            <div className="mt-4">
              <button
                onClick={() => navigate('/diffs')}
                className="text-sm bg-red-100 text-red-800 px-3 py-1 rounded hover:bg-red-200"
              >
                Back to Diffs
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!commit) {
    return (
      <div className="text-center py-12">
        <h3 className="text-lg font-medium text-gray-900">Commit not found</h3>
        <p className="mt-2 text-gray-600">The requested commit could not be loaded.</p>
        <button
          onClick={() => navigate('/diffs')}
          className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Back to Diffs
        </button>
      </div>
    );
  }

  return (
    <div className="commit-viewer h-screen flex flex-col">
      {/* Header */}
      <div className="border-b border-gray-200 bg-white px-6 py-4 flex-shrink-0">
        <div className="flex items-start justify-between">
          <div className="flex-1 min-w-0">
            <div className="flex items-center space-x-3 mb-2">
              <button
                onClick={() => navigate('/diffs')}
                className="text-gray-400 hover:text-gray-600"
              >
                ← Back
              </button>
              <span className="font-mono text-sm bg-gray-100 px-2 py-1 rounded">
                {commit.hash.substring(0, 8)}
              </span>
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(commit.reviewStatus)}`}>
                {getStatusIcon(commit.reviewStatus)} {commit.reviewStatus.replace('_', ' ')}
              </span>
            </div>
            
            <h1 className="text-xl font-semibold text-gray-900 break-words">
              {commit.message.split('\n')[0]}
            </h1>
            
            {commit.message.includes('\n') && (
              <div className="mt-2 text-sm text-gray-600 whitespace-pre-wrap">
                {commit.message.split('\n').slice(1).join('\n').trim()}
              </div>
            )}
            
            <div className="mt-2 text-sm text-gray-500">
              by <span className="font-medium">{commit.author}</span> on {commit.date}
            </div>
          </div>

          {/* Review Panel */}
          <div className="ml-6 flex-shrink-0">
            <ReviewPanel
              currentStatus={commit.reviewStatus}
              onStatusChange={handleReviewStatusChange}
            />
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex overflow-hidden">
        {/* File tree sidebar */}
        <div className="w-80 flex-shrink-0">
          <FileTree
            files={files}
            selectedFile={selectedFile?.path}
            onFileSelect={setSelectedFile}
          />
        </div>

        {/* Diff viewer */}
        <div className="flex-1 overflow-auto">
          {selectedFile ? (
            <DiffViewer
              diffText={selectedFile.diff || ''}
              oldPath={selectedFile.oldPath}
              newPath={selectedFile.path}
              language="typescript"
            />
          ) : (
            <div className="flex items-center justify-center h-full bg-gray-50">
              <div className="text-center">
                <div className="text-gray-400 text-6xl mb-4">📄</div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  Select a file to view changes
                </h3>
                <p className="text-gray-600">
                  Choose a file from the tree on the left to see its diff
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CommitViewer;