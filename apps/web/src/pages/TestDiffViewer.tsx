import React from 'react';
import { useParams } from 'react-router-dom';
import { DiffViewer } from '../components/DiffViewer';

export const TestDiffViewerPage: React.FC = () => {
  const { commitId } = useParams<{ commitId: string }>();
  
  if (!commitId) {
    return <div>No commit ID provided</div>;
  }

  return (
    <div style={{ padding: '20px' }}>
      <h1>Test Diff Viewer</h1>
      <DiffViewer commitId={parseInt(commitId)} />
    </div>
  );
};