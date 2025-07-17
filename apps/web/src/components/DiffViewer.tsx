import React, { useState, useEffect } from 'react';
import { InlineComment } from './diff/InlineComment';
import { CommentDisplay } from './diff/CommentDisplay';
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

interface ReviewComment {
  id: number;
  commit_id: number;
  reviewer_id: number;
  line_number: number | null;
  file_path: string | null;
  content: string;
  created_at: string;
  updated_at: string | null;
}

interface DiffViewerProps {
  commitId: number;
}

export const DiffViewer: React.FC<DiffViewerProps> = ({ commitId }) => {
  const [diffData, setDiffData] = useState<DiffData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'unified' | 'split'>('unified');
  const [activeCommentLines, setActiveCommentLines] = useState<Set<string>>(new Set());
  const [selectedLineRange, setSelectedLineRange] = useState<{ start: string; end: string } | null>(null);
  const [existingComments, setExistingComments] = useState<ReviewComment[]>([]);

  useEffect(() => {
    fetchDiffData();
    fetchExistingComments();
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

  const fetchExistingComments = async () => {
    try {
      const response = await fetch(`/api/v1/commits/${commitId}/comments`);
      if (!response.ok) {
        throw new Error('Failed to fetch comments');
      }
      const comments: ReviewComment[] = await response.json();
      setExistingComments(comments);
    } catch (err) {
      console.error('Failed to load comments:', err);
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

  const getLineKey = (fileIndex: number, blockIndex: number, lineIndex: number, side?: 'left' | 'right') => {
    return `${fileIndex}-${blockIndex}-${lineIndex}${side ? `-${side}` : ''}`;
  };

  const getCommentsForLine = (fileName: string, lineNumber: number): ReviewComment[] => {
    return existingComments.filter(
      comment => comment.file_path === fileName && comment.line_number === lineNumber
    );
  };

  const handleLineClick = (lineKey: string, fileName: string, lineNumber: number) => {
    if (activeCommentLines.has(lineKey)) {
      // Remove comment form if clicking on the same line
      setActiveCommentLines(prev => {
        const newSet = new Set(prev);
        newSet.delete(lineKey);
        return newSet;
      });
    } else {
      // Add comment form for this line
      setActiveCommentLines(prev => new Set(prev).add(lineKey));
    }
  };

  const handleCommentSave = async (lineKey: string, comment: string, fileName: string, lineNumber: number) => {
    try {
      const response = await fetch(`/api/v1/commits/${commitId}/comments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          reviewer_id: 1, // TODO: Get actual user ID
          line_number: lineNumber,
          file_path: fileName,
          content: comment,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to save comment');
      }

      const savedComment = await response.json();
      console.log('Comment saved:', savedComment);
      
      // Remove the comment form after saving
      setActiveCommentLines(prev => {
        const newSet = new Set(prev);
        newSet.delete(lineKey);
        return newSet;
      });
      
      // Refresh comments to show the new one
      await fetchExistingComments();
    } catch (error) {
      console.error('Failed to save comment:', error);
      alert('Failed to save comment');
    }
  };

  const handleCommentCancel = (lineKey: string) => {
    setActiveCommentLines(prev => {
      const newSet = new Set(prev);
      newSet.delete(lineKey);
      return newSet;
    });
  };

  const renderUnifiedDiff = (file: DiffFile, fileIndex: number) => {
    const fileName = file.newName || file.oldName || 'Unknown file';
    return (
      <div className="diff-file-content">
        {file.blocks.map((block, blockIndex) => (
          <div key={blockIndex} className="diff-block">
            {block.lines.map((line, lineIndex) => {
              const lineKey = getLineKey(fileIndex, blockIndex, lineIndex);
              const lineNumber = line.newNumber || line.oldNumber || 0;
              const showComment = activeCommentLines.has(lineKey);
              const existingLineComments = getCommentsForLine(fileName, lineNumber);
              
              return (
                <React.Fragment key={lineIndex}>
                  <div 
                    className={`diff-line ${getLineClass(line.type)} ${line.type !== 'context' ? 'clickable' : ''}`}
                    onClick={() => line.type !== 'context' && handleLineClick(lineKey, fileName, lineNumber)}
                  >
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
                      <span>{line.content.replace(/^[+-]\s?/, '')}</span>
                    </span>
                  </div>
                  {existingLineComments.length > 0 && (
                    <div className="diff-comment-row">
                      {existingLineComments.map((comment) => (
                        <CommentDisplay key={comment.id} comment={comment} />
                      ))}
                    </div>
                  )}
                  {showComment && (
                    <div className="diff-comment-row">
                      <InlineComment
                        lineNumber={lineNumber}
                        fileName={fileName}
                        commitHash={diffData?.commit.hash || ''}
                        onSave={(comment) => handleCommentSave(lineKey, comment, fileName, lineNumber)}
                        onCancel={() => handleCommentCancel(lineKey)}
                      />
                    </div>
                  )}
                </React.Fragment>
              );
            })}
          </div>
        ))}
      </div>
    );
  };

  const renderSplitDiff = (file: DiffFile, fileIndex: number) => {
    const fileName = file.newName || file.oldName || 'Unknown file';
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
                const leftLineKey = getLineKey(fileIndex, blockIndex, lineIndex, 'left');
                const rightLineKey = getLineKey(fileIndex, blockIndex, lineIndex, 'right');
                const leftLineNumber = leftLine?.oldNumber || 0;
                const rightLineNumber = rightLine?.newNumber || 0;
                const showLeftComment = leftLine && leftLine.type === 'delete' && activeCommentLines.has(leftLineKey);
                const showRightComment = rightLine && rightLine.type === 'insert' && activeCommentLines.has(rightLineKey);
                const leftExistingComments = leftLine ? getCommentsForLine(fileName, leftLineNumber) : [];
                const rightExistingComments = rightLine ? getCommentsForLine(fileName, rightLineNumber) : [];
                
                return (
                  <React.Fragment key={lineIndex}>
                    <div className="diff-line-pair">
                      <div 
                        className={`diff-line-left ${leftLine ? getLineClass(leftLine.type) : 'diff-line-empty'} ${leftLine && leftLine.type === 'delete' ? 'clickable' : ''}`}
                        onClick={() => leftLine && leftLine.type === 'delete' && handleLineClick(leftLineKey, fileName, leftLineNumber)}
                      >
                        <span className="diff-line-number">
                          {leftLine?.oldNumber || ''}
                        </span>
                        <span className="diff-line-content">
                          {leftLine && (
                            <>
                              <span className="diff-line-sign">
                                {leftLine.type === 'delete' ? '-' : ' '}
                              </span>
                              {leftLine.content.replace(/^[+-]\s?/, '')}
                            </>
                          )}
                        </span>
                      </div>
                      <div 
                        className={`diff-line-right ${rightLine ? getLineClass(rightLine.type) : 'diff-line-empty'} ${rightLine && rightLine.type === 'insert' ? 'clickable' : ''}`}
                        onClick={() => rightLine && rightLine.type === 'insert' && handleLineClick(rightLineKey, fileName, rightLineNumber)}
                      >
                        <span className="diff-line-number">
                          {rightLine?.newNumber || ''}
                        </span>
                        <span className="diff-line-content">
                          {rightLine && (
                            <>
                              <span className="diff-line-sign">
                                {rightLine.type === 'insert' ? '+' : ' '}
                              </span>
                              {rightLine.content.replace(/^[+-]\s?/, '')}
                            </>
                          )}
                        </span>
                      </div>
                    </div>
                    {(leftExistingComments.length > 0 || rightExistingComments.length > 0) && (
                      <div className="diff-comment-row split">
                        {leftExistingComments.length > 0 && (
                          <div className="diff-comment-left">
                            {leftExistingComments.map((comment) => (
                              <CommentDisplay key={comment.id} comment={comment} />
                            ))}
                          </div>
                        )}
                        {rightExistingComments.length > 0 && (
                          <div className="diff-comment-right">
                            {rightExistingComments.map((comment) => (
                              <CommentDisplay key={comment.id} comment={comment} />
                            ))}
                          </div>
                        )}
                        {leftExistingComments.length === 0 && rightExistingComments.length > 0 && (
                          <div className="diff-comment-left"></div>
                        )}
                      </div>
                    )}
                    {(showLeftComment || showRightComment) && (
                      <div className="diff-comment-row split">
                        {showLeftComment && (
                          <div className="diff-comment-left">
                            <InlineComment
                              lineNumber={leftLineNumber}
                              fileName={fileName}
                              commitHash={diffData?.commit.hash || ''}
                              onSave={(comment) => handleCommentSave(leftLineKey, comment, fileName, leftLineNumber)}
                              onCancel={() => handleCommentCancel(leftLineKey)}
                            />
                          </div>
                        )}
                        {showRightComment && (
                          <div className="diff-comment-right">
                            <InlineComment
                              lineNumber={rightLineNumber}
                              fileName={fileName}
                              commitHash={diffData?.commit.hash || ''}
                              onSave={(comment) => handleCommentSave(rightLineKey, comment, fileName, rightLineNumber)}
                              onCancel={() => handleCommentCancel(rightLineKey)}
                            />
                          </div>
                        )}
                      </div>
                    )}
                  </React.Fragment>
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
              {viewMode === 'unified' ? renderUnifiedDiff(file, fileIndex) : renderSplitDiff(file, fileIndex)}
            </div>
          ))
        )}
      </div>
    </div>
  );
};