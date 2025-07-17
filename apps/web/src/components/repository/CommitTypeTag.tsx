import React from 'react';
import { parseConventionalCommit, getCommitTypeInfo } from '../../utils/conventionalCommits';

interface CommitTypeTagProps {
  message: string;
}

export const CommitTypeTag: React.FC<CommitTypeTagProps> = ({ message }) => {
  const { type, breaking } = parseConventionalCommit(message);
  const typeInfo = getCommitTypeInfo(type);
  
  if (!typeInfo) return null;
  
  const colorClasses = {
    purple: 'bg-purple-100 text-purple-800 border-purple-200',
    red: 'bg-red-100 text-red-800 border-red-200',
    blue: 'bg-blue-100 text-blue-800 border-blue-200',
    pink: 'bg-pink-100 text-pink-800 border-pink-200',
    green: 'bg-green-100 text-green-800 border-green-200',
    orange: 'bg-orange-100 text-orange-800 border-orange-200',
    yellow: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    gray: 'bg-gray-100 text-gray-800 border-gray-200',
    indigo: 'bg-indigo-100 text-indigo-800 border-indigo-200',
  };
  
  const colorClass = colorClasses[typeInfo.color as keyof typeof colorClasses] || colorClasses.gray;
  
  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium border ${colorClass}`}>
      <span className="text-base">{typeInfo.emoji}</span>
      <span>{typeInfo.label}</span>
      {breaking && <span className="text-red-600 font-bold">!</span>}
    </span>
  );
};