import React, { useState } from "react";
import RepositoryDashboard from "../components/dashboards/RepositoryDashboard";

const Dashboards: React.FC = () => {
  const [activeTab, setActiveTab] = useState<"repository" | "quality" | "team">(
    "repository"
  );

  return (
    <div className="px-4 py-6 sm:px-0">
      {/* Tab Navigation */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab("repository")}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === "repository"
                ? "border-blue-500 text-blue-600"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
            }`}
          >
            📊 Repository Overview
          </button>
          <button
            onClick={() => setActiveTab("quality")}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === "quality"
                ? "border-blue-500 text-blue-600"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
            }`}
          >
            🎯 Code Quality
          </button>
          <button
            onClick={() => setActiveTab("team")}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === "team"
                ? "border-blue-500 text-blue-600"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
            }`}
          >
            👥 Team Activity
          </button>
        </nav>
      </div>

      {/* Tab Content */}
      {activeTab === "repository" && <RepositoryDashboard />}

      {activeTab === "quality" && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">🎯</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Code Quality Dashboard
          </h3>
          <p className="text-gray-600 mb-4">
            Review metrics, code complexity, and quality trends will be
            displayed here.
          </p>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 max-w-md mx-auto">
            <h4 className="font-medium text-blue-900 mb-2">Coming Soon</h4>
            <ul className="text-sm text-blue-700 space-y-1 text-left">
              <li>• Review turnaround times</li>
              <li>• Code complexity metrics</li>
              <li>• Quality gate compliance</li>
              <li>• Technical debt tracking</li>
            </ul>
          </div>
        </div>
      )}

      {activeTab === "team" && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">👥</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Team Activity Dashboard
          </h3>
          <p className="text-gray-600 mb-4">
            Team collaboration, velocity, and productivity metrics will be shown
            here.
          </p>
          <div className="bg-green-50 border border-green-200 rounded-lg p-4 max-w-md mx-auto">
            <h4 className="font-medium text-green-900 mb-2">Coming Soon</h4>
            <ul className="text-sm text-green-700 space-y-1 text-left">
              <li>• Velocity tracking</li>
              <li>• Collaboration patterns</li>
              <li>• Review participation</li>
              <li>• Knowledge sharing</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboards;
