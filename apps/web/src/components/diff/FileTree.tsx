import React from "react";

interface FileChange {
  path: string;
  type: "added" | "modified" | "deleted" | "renamed";
  insertions: number;
  deletions: number;
  oldPath?: string;
}

interface FileTreeProps {
  files: FileChange[];
  selectedFile?: string;
  onFileSelect: (file: FileChange) => void;
}

const FileTree: React.FC<FileTreeProps> = ({
  files,
  selectedFile,
  onFileSelect,
}) => {
  // Removed unused state for simplicity

  // Simple flat file list display for now
  const getFileIcon = (type: string) => {
    switch (type) {
      case "added":
        return <span className="text-green-500 font-bold">+</span>;
      case "deleted":
        return <span className="text-red-500 font-bold">-</span>;
      case "modified":
        return <span className="text-blue-500 font-bold">M</span>;
      case "renamed":
        return <span className="text-yellow-500 font-bold">R</span>;
      default:
        return <span className="text-gray-500 font-bold">?</span>;
    }
  };

  if (files.length === 0) {
    return (
      <div className="p-4 text-center text-gray-500">
        <div className="text-4xl mb-2">📁</div>
        <p>No files changed</p>
      </div>
    );
  }

  return (
    <div className="file-tree bg-white border-r border-gray-200">
      {/* Header */}
      <div className="border-b border-gray-200 px-4 py-3 bg-gray-50">
        <h3 className="text-sm font-medium text-gray-900">
          Files changed ({files.length})
        </h3>
      </div>

      {/* File list */}
      <div className="overflow-y-auto max-h-96">
        {files.map((file, index) => {
          const isSelected = selectedFile === file.path;

          return (
            <div
              key={index}
              className={`flex items-center py-2 px-4 hover:bg-gray-50 cursor-pointer ${
                isSelected ? "bg-blue-50 border-r-2 border-blue-500" : ""
              }`}
              onClick={() => onFileSelect(file)}
            >
              <div className="flex-shrink-0 mr-3 w-4 text-center">
                {getFileIcon(file.type)}
              </div>

              <span className="text-sm text-gray-900 truncate flex-1 min-w-0">
                {file.path}
              </span>

              <div className="ml-auto flex items-center space-x-1 text-xs">
                {file.insertions > 0 && (
                  <span className="text-green-600">+{file.insertions}</span>
                )}
                {file.deletions > 0 && (
                  <span className="text-red-600">-{file.deletions}</span>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Summary */}
      <div className="border-t border-gray-200 px-4 py-3 bg-gray-50">
        <div className="grid grid-cols-3 gap-4 text-xs">
          <div className="text-center">
            <div className="font-medium text-gray-900">
              {files.filter((f) => f.type === "added").length}
            </div>
            <div className="text-green-600">Added</div>
          </div>
          <div className="text-center">
            <div className="font-medium text-gray-900">
              {files.filter((f) => f.type === "modified").length}
            </div>
            <div className="text-blue-600">Modified</div>
          </div>
          <div className="text-center">
            <div className="font-medium text-gray-900">
              {files.filter((f) => f.type === "deleted").length}
            </div>
            <div className="text-red-600">Deleted</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FileTree;
