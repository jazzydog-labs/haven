import React, { useState, useEffect } from 'react';
import { Diff, Hunk, parseDiff } from 'react-diff-view';
import { PrismLight as SyntaxHighlighter } from 'react-syntax-highlighter';
import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/prism';
import 'react-diff-view/style/index.css';

interface DiffViewerProps {
  diffText: string;
  oldPath?: string;
  newPath?: string;
  language?: string;
}

interface DiffStats {
  filesChanged: number;
  insertions: number;
  deletions: number;
  totalChanges: number;
}

const DiffViewer: React.FC<DiffViewerProps> = ({ 
  diffText, 
  oldPath = '', 
  newPath = '', 
  language = 'javascript' 
}) => {
  const [viewType, setViewType] = useState<'split' | 'unified'>('split');
  const [files, setFiles] = useState<any[]>([]);
  const [stats, setStats] = useState<DiffStats>({
    filesChanged: 0,
    insertions: 0,
    deletions: 0,
    totalChanges: 0
  });

  useEffect(() => {
    if (diffText) {
      try {
        const parsedFiles = parseDiff(diffText);
        setFiles(parsedFiles);
        
        // Calculate stats
        const statsCalc = parsedFiles.reduce((acc, file) => {
          const hunks = file.hunks || [];
          const additions = hunks.reduce((sum, hunk) => 
            sum + hunk.changes.filter(change => change.type === 'insert').length, 0);
          const deletions = hunks.reduce((sum, hunk) => 
            sum + hunk.changes.filter(change => change.type === 'delete').length, 0);
          
          return {
            filesChanged: acc.filesChanged + 1,
            insertions: acc.insertions + additions,
            deletions: acc.deletions + deletions,
            totalChanges: acc.totalChanges + additions + deletions
          };
        }, { filesChanged: 0, insertions: 0, deletions: 0, totalChanges: 0 });
        
        setStats(statsCalc);
      } catch (error) {
        console.error('Failed to parse diff:', error);
      }
    }
  }, [diffText]);

  const renderToken = (token: any, _defaultRender: any, i: number) => {
    return (
      <SyntaxHighlighter
        key={i}
        language={language}
        style={tomorrow}
        customStyle={{
          background: 'transparent',
          padding: 0,
          margin: 0,
          fontSize: 'inherit',
          lineHeight: 'inherit'
        }}
        codeTagProps={{
          style: {
            background: 'transparent',
            fontFamily: 'inherit'
          }
        }}
      >
        {token.value}
      </SyntaxHighlighter>
    );
  };

  if (!diffText) {
    return (
      <div className="flex items-center justify-center h-64 bg-gray-50 rounded-lg">
        <div className="text-center">
          <div className="text-gray-400 text-lg mb-2">📄</div>
          <p className="text-gray-500">No diff data available</p>
        </div>
      </div>
    );
  }

  return (
    <div className="diff-viewer">
      {/* Header with controls and stats */}
      <div className="border-b border-gray-200 bg-white px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <h3 className="text-lg font-medium text-gray-900">
              Diff View
            </h3>
            {(oldPath || newPath) && (
              <div className="text-sm text-gray-600">
                <span className="font-mono bg-gray-100 px-2 py-1 rounded">
                  {oldPath || newPath}
                </span>
              </div>
            )}
          </div>
          
          <div className="flex items-center space-x-4">
            {/* Stats */}
            <div className="flex items-center space-x-3 text-sm">
              <span className="text-gray-600">{stats.filesChanged} files</span>
              <span className="text-green-600">+{stats.insertions}</span>
              <span className="text-red-600">-{stats.deletions}</span>
            </div>
            
            {/* View toggle */}
            <div className="flex border border-gray-300 rounded-md">
              <button
                onClick={() => setViewType('split')}
                className={`px-3 py-1 text-sm font-medium rounded-l-md ${
                  viewType === 'split'
                    ? 'bg-blue-500 text-white'
                    : 'bg-white text-gray-700 hover:bg-gray-50'
                }`}
              >
                Split
              </button>
              <button
                onClick={() => setViewType('unified')}
                className={`px-3 py-1 text-sm font-medium rounded-r-md ${
                  viewType === 'unified'
                    ? 'bg-blue-500 text-white'
                    : 'bg-white text-gray-700 hover:bg-gray-50'
                }`}
              >
                Unified
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Diff content */}
      <div className="bg-white">
        {files.map((file, index) => (
          <div key={index} className="border-b border-gray-200 last:border-b-0">
            {/* File header */}
            <div className="bg-gray-50 px-4 py-2 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <div className="font-mono text-sm">
                  <span className="text-gray-600">
                    {file.oldPath !== '/dev/null' && file.oldPath}
                  </span>
                  {file.oldPath !== file.newPath && file.newPath !== '/dev/null' && (
                    <>
                      <span className="text-gray-400 mx-2">→</span>
                      <span className="text-gray-900">{file.newPath}</span>
                    </>
                  )}
                </div>
                <div className="text-sm text-gray-500">
                  {file.hunks?.length || 0} hunks
                </div>
              </div>
            </div>

            {/* File diff */}
            <div className="diff-content">
              <Diff 
                viewType={viewType}
                diffType={file.type}
                hunks={file.hunks || []}
                tokens={file.tokens}
                renderToken={renderToken}
              >
                {(hunks: any[]) =>
                  hunks.map((hunk) => (
                    <Hunk key={hunk.content} hunk={hunk} />
                  ))
                }
              </Diff>
            </div>
          </div>
        ))}
      </div>

      {files.length === 0 && (
        <div className="flex items-center justify-center h-32 bg-gray-50">
          <p className="text-gray-500">No changes to display</p>
        </div>
      )}
    </div>
  );
};

export default DiffViewer;