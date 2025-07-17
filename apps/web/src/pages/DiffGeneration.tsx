import { useState } from "react";
import CommitList from "../components/diff/CommitList";

const DiffGeneration = () => {
  const [activeTab, setActiveTab] = useState<"commits" | "generate">("commits");

  return (
    <div className="px-4 py-6 sm:px-0">
      {/* Tab Navigation */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab("commits")}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === "commits"
                ? "border-blue-500 text-blue-600"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
            }`}
          >
            Recent Commits
          </button>
          <button
            onClick={() => setActiveTab("generate")}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === "generate"
                ? "border-blue-500 text-blue-600"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
            }`}
          >
            Generate Diffs
          </button>
        </nav>
      </div>

      {/* Tab Content */}
      {activeTab === "commits" && <CommitList />}

      {activeTab === "generate" && (
        <div className="border-4 border-dashed border-gray-200 rounded-lg h-96 p-8">
          <h1 className="text-2xl font-bold text-gray-900 mb-6">
            Generate New Diffs
          </h1>
          <p className="text-gray-600 mb-4">
            Generate diff reports for commit ranges.
          </p>
          <div className="space-y-4 max-w-md">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Base Branch
              </label>
              <input
                type="text"
                defaultValue="main"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Compare Branch
              </label>
              <input
                type="text"
                defaultValue="HEAD"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Max Commits
              </label>
              <input
                type="number"
                defaultValue="50"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <button className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
              Generate Diff Report
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default DiffGeneration;
