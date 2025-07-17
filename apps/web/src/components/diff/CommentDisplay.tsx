import React from 'react';
import './CommentDisplay.css';

interface CommentDisplayProps {
  comment: {
    id: number;
    content: string;
    reviewer_id: number;
    created_at: string;
    updated_at: string | null;
  };
}

export const CommentDisplay: React.FC<CommentDisplayProps> = ({ comment }) => {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  return (
    <div className="comment-display">
      <div className="comment-header">
        <span className="comment-author">User #{comment.reviewer_id}</span>
        <span className="comment-date">{formatDate(comment.created_at)}</span>
      </div>
      <div className="comment-body">
        {comment.content}
      </div>
    </div>
  );
};