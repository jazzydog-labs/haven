import React, { useState, useEffect } from 'react';
import './DiffViewer.css';

interface DiffLine {
  content: string;
  type: 'context' | 'insert' | 'delete';
  oldNumber?: number;
  newNumber?: number;
}

interface DiffBlock {
  lines: DiffLine[];
  header?: string;
  startLineOld?: number;
  startLineNew?: number;
}

interface DiffFile {
  blocks: DiffBlock[];
  deletedLines: number;
  addedLines: number;
  isCombined: boolean;
  isGitDiff: boolean;
  language?: string;
  newName?: string;
  oldName?: string;
  newMode?: string;
  oldMode?: string;
}

interface CommitInfo {
  hash: string;
  short_hash: string;
  summary: string;
  message: string;
  author_name: string;
  author_email: string;
  committed_at: string;
}

interface DiffData {
  commit: CommitInfo;
  files: DiffFile[];
}

interface DiffViewerProps {
  commitId: number;
}

export const DiffViewer: React.FC<DiffViewerProps> = ({ commitId }) => {
  const [diffData, setDiffData] = useState<DiffData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'unified' | 'split'>('unified');

  useEffect(() => {
    fetchDiffData();
  }, [commitId]);

  const fetchDiffData = async () => {
    try {
      const response = await fetch(`/api/v1/commits/${commitId}/diff-json`);
      if (!response.ok) {
        throw new Error('Failed to fetch diff data');
      }
      const data: DiffData = await response.json();
      setDiffData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load diff');
    } finally {
      setLoading(false);
    }
  };

  const getLineClass = (type: string) => {
    switch (type) {
      case 'insert':
        return 'diff-line-added';
      case 'delete':
        return 'diff-line-deleted';
      default:
        return 'diff-line-context';
    }
  };

  const renderUnifiedDiff = (file: DiffFile) => {
    return (
      <div className="diff-file-content">
        {file.blocks.map((block, blockIndex) => (
          <div key={blockIndex} className="diff-block">
            {block.lines.map((line, lineIndex) => (
              <div key={lineIndex} className={`diff-line ${getLineClass(line.type)}`}>
                <span className="diff-line-number old">
                  {line.oldNumber || ''}
                </span>
                <span className="diff-line-number new">
                  {line.newNumber || ''}
                </span>
                <span className="diff-line-content">
                  <span className="diff-line-sign">
                    {line.type === 'insert' ? '+' : line.type === 'delete' ? '-' : ' '}
                  </span>
                  {line.content}
                </span>
              </div>
            ))}
          </div>
        ))}
      </div>
    );
  };

  const renderSplitDiff = (file: DiffFile) => {
    return (
      <div className="diff-file-content split">
        {file.blocks.map((block, blockIndex) => {
          const leftLines: (DiffLine | null)[] = [];
          const rightLines: (DiffLine | null)[] = [];

          block.lines.forEach(line => {
            if (line.type === 'context') {
              leftLines.push(line);
              rightLines.push(line);
            } else if (line.type === 'delete') {
              leftLines.push(line);
              rightLines.push(null);
            } else if (line.type === 'insert') {
              leftLines.push(null);
              rightLines.push(line);
            }
          });

          // Balance the arrays
          while (leftLines.length < rightLines.length) leftLines.push(null);
          while (rightLines.length < leftLines.length) rightLines.push(null);

          return (
            <div key={blockIndex} className="diff-block">
              {leftLines.map((leftLine, lineIndex) => {
                const rightLine = rightLines[lineIndex];
                return (
                  <div key={lineIndex} className="diff-line-pair">
                    <div className={`diff-line-left ${leftLine ? getLineClass(leftLine.type) : 'diff-line-empty'}`}>
                      <span className="diff-line-number">
                        {leftLine?.oldNumber || ''}
                      </span>
                      <span className="diff-line-content">
                        {leftLine && (
                          <>
                            <span className="diff-line-sign">
                              {leftLine.type === 'delete' ? '-' : ' '}
                            </span>
                            {leftLine.content}
                          </>
                        )}
                      </span>
                    </div>
                    <div className={`diff-line-right ${rightLine ? getLineClass(rightLine.type) : 'diff-line-empty'}`}>
                      <span className="diff-line-number">
                        {rightLine?.newNumber || ''}
                      </span>
                      <span className="diff-line-content">
                        {rightLine && (
                          <>
                            <span className="diff-line-sign">
                              {rightLine.type === 'insert' ? '+' : ' '}
                            </span>
                            {rightLine.content}
                          </>
                        )}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          );
        })}
      </div>
    );
  };

  if (loading) {
    return <div className="diff-viewer-loading">Loading diff...</div>;
  }

  if (error) {
    return <div className="diff-viewer-error">Error: {error}</div>;
  }

  if (!diffData) {
    return <div className="diff-viewer-empty">No diff data available</div>;
  }

  return (
    <div className="diff-viewer">
      <div className="diff-header">
        <div className="diff-commit-info">
          <h3>Commit {diffData.commit.short_hash}</h3>
          <p className="diff-commit-message">{diffData.commit.message}</p>
          <p className="diff-commit-author">
            {diffData.commit.author_name} &lt;{diffData.commit.author_email}&gt;
          </p>
          <p className="diff-commit-date">
            {new Date(diffData.commit.committed_at).toLocaleString()}
          </p>
        </div>
        <div className="diff-view-controls">
          <button
            className={`diff-view-btn ${viewMode === 'unified' ? 'active' : ''}`}
            onClick={() => setViewMode('unified')}
          >
            Unified
          </button>
          <button
            className={`diff-view-btn ${viewMode === 'split' ? 'active' : ''}`}
            onClick={() => setViewMode('split')}
          >
            Split
          </button>
        </div>
      </div>

      <div className="diff-files">
        {diffData.files.length === 0 ? (
          <div className="diff-no-changes">No changes in this commit</div>
        ) : (
          diffData.files.map((file, fileIndex) => (
            <div key={fileIndex} className="diff-file">
              <div className="diff-file-header">
                <span className="diff-file-name">
                  {file.oldName || file.newName || 'Unknown file'}
                </span>
                <span className="diff-file-stats">
                  <span className="diff-additions">+{file.addedLines}</span>
                  <span className="diff-deletions">-{file.deletedLines}</span>
                </span>
              </div>
              {viewMode === 'unified' ? renderUnifiedDiff(file) : renderSplitDiff(file)}
            </div>
          ))
        )}
      </div>
    </div>
  );
};