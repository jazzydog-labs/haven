import React, { useState } from 'react';
import './InlineComment.css';

interface InlineCommentProps {
  lineNumber: number;
  fileName: string;
  commitHash: string;
  onSave: (comment: string) => void;
  onCancel: () => void;
}

export const InlineComment: React.FC<InlineCommentProps> = ({
  lineNumber,
  fileName,
  commitHash,
  onSave,
  onCancel,
}) => {
  const [comment, setComment] = useState('');

  const handleSave = () => {
    if (comment.trim()) {
      onSave(comment.trim());
      setComment('');
    }
  };

  return (
    <div className="inline-comment-form">
      <div className="comment-header">
        <span className="comment-location">
          Commenting on line {lineNumber} of {fileName}
        </span>
      </div>
      <textarea
        className="comment-input"
        placeholder="Leave a comment..."
        value={comment}
        onChange={(e) => setComment(e.target.value)}
        rows={3}
        autoFocus
      />
      <div className="comment-actions">
        <button 
          className="btn btn-primary btn-sm"
          onClick={handleSave}
          disabled={!comment.trim()}
        >
          Add Comment
        </button>
        <button 
          className="btn btn-secondary btn-sm"
          onClick={onCancel}
        >
          Cancel
        </button>
      </div>
    </div>
  );
};