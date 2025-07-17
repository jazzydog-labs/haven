import { useQuery } from "@tanstack/react-query";

const Dashboard = () => {
  const { data: health, isLoading } = useQuery({
    queryKey: ["health"],
    queryFn: async () => {
      const response = await fetch("/api/health");
      if (!response.ok) {
        throw new Error("Failed to fetch health status");
      }
      return response.json();
    },
  });

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="border-4 border-dashed border-gray-200 rounded-lg h-96 p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">
          Haven Dashboard
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Health Status Card */}
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                    <svg
                      className="w-5 h-5 text-white"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      API Health
                    </dt>
                    <dd className="text-lg font-medium text-gray-900">
                      {isLoading
                        ? "Checking..."
                        : health
                        ? "Healthy"
                        : "Unavailable"}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Quick Actions
              </h3>
              <div className="space-y-2">
                <a
                  href="/records"
                  className="block w-full text-left px-3 py-2 text-sm text-indigo-600 hover:bg-indigo-50 rounded"
                >
                  📝 View Records
                </a>
                <a
                  href="/repository/1/browse"
                  className="block w-full text-left px-3 py-2 text-sm text-indigo-600 hover:bg-indigo-50 rounded"
                >
                  🔍 Browse Repository
                </a>
                <a
                  href="/dashboards"
                  className="block w-full text-left px-3 py-2 text-sm text-indigo-600 hover:bg-indigo-50 rounded"
                >
                  📊 View Analytics
                </a>
                <a
                  href="/api/docs"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block w-full text-left px-3 py-2 text-sm text-indigo-600 hover:bg-indigo-50 rounded"
                >
                  📚 API Documentation
                </a>
              </div>
            </div>
          </div>

          {/* Stats */}
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                System Info
              </h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-500">Environment</span>
                  <span className="text-sm font-medium">Development</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-500">Version</span>
                  <span className="text-sm font-medium">0.1.0</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
