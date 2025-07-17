import React, { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { format, subDays, parseISO } from 'date-fns';

interface RepositoryStats {
  totalCommits: number;
  totalContributors: number;
  linesOfCode: number;
  activeBranches: number;
  pendingReviews: number;
  approvedCommits: number;
}

interface CommitActivity {
  date: string;
  commits: number;
  additions: number;
  deletions: number;
}

interface ContributorStats {
  name: string;
  commits: number;
  additions: number;
  deletions: number;
  color: string;
}

interface FileTypeStats {
  extension: string;
  files: number;
  lines: number;
  color: string;
}

const RepositoryDashboard: React.FC = () => {
  const [stats, setStats] = useState<RepositoryStats>({
    totalCommits: 0,
    totalContributors: 0,
    linesOfCode: 0,
    activeBranches: 0,
    pendingReviews: 0,
    approvedCommits: 0
  });

  const [commitActivity, setCommitActivity] = useState<CommitActivity[]>([]);
  const [contributors, setContributors] = useState<ContributorStats[]>([]);
  const [fileTypes, setFileTypes] = useState<FileTypeStats[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);

      // Mock data - in reality this would come from the API
      const mockStats: RepositoryStats = {
        totalCommits: 156,
        totalContributors: 8,
        linesOfCode: 45672,
        activeBranches: 12,
        pendingReviews: 7,
        approvedCommits: 142
      };

      // Generate commit activity for last 30 days
      const mockCommitActivity: CommitActivity[] = [];
      for (let i = 29; i >= 0; i--) {
        const date = format(subDays(new Date(), i), 'yyyy-MM-dd');
        mockCommitActivity.push({
          date,
          commits: Math.floor(Math.random() * 8) + 1,
          additions: Math.floor(Math.random() * 500) + 50,
          deletions: Math.floor(Math.random() * 200) + 10
        });
      }

      const mockContributors: ContributorStats[] = [
        { name: 'John Doe', commits: 45, additions: 12450, deletions: 3200, color: '#8884d8' },
        { name: 'Jane Smith', commits: 38, additions: 9800, deletions: 2100, color: '#82ca9d' },
        { name: 'Bob Johnson', commits: 28, additions: 7600, deletions: 1800, color: '#ffc658' },
        { name: 'Alice Wilson', commits: 22, additions: 6200, deletions: 1400, color: '#ff7300' },
        { name: 'Charlie Brown', commits: 15, additions: 4100, deletions: 900, color: '#00ff88' },
        { name: 'David Lee', commits: 8, additions: 2300, deletions: 600, color: '#ff6b6b' }
      ];

      const mockFileTypes: FileTypeStats[] = [
        { extension: '.ts/.tsx', files: 89, lines: 18450, color: '#3178c6' },
        { extension: '.py', files: 67, lines: 15200, color: '#3776ab' },
        { extension: '.md', files: 23, lines: 3400, color: '#083fa1' },
        { extension: '.json', files: 15, lines: 2800, color: '#e34c26' },
        { extension: '.yml/.yaml', files: 12, lines: 1200, color: '#cb171e' },
        { extension: 'Other', files: 28, lines: 4622, color: '#6c757d' }
      ];

      setStats(mockStats);
      setCommitActivity(mockCommitActivity);
      setContributors(mockContributors);
      setFileTypes(mockFileTypes);

    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        <span className="ml-2 text-gray-600">Loading dashboard data...</span>
      </div>
    );
  }

  return (
    <div className="repository-dashboard space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">Repository Overview</h2>
        <div className="flex items-center space-x-2 text-sm text-gray-500">
          <span>Last updated: {format(new Date(), 'MMM dd, yyyy HH:mm')}</span>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <div className="text-2xl font-bold text-blue-600">{stats.totalCommits}</div>
          <div className="text-sm text-gray-500">Total Commits</div>
        </div>
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <div className="text-2xl font-bold text-green-600">{stats.totalContributors}</div>
          <div className="text-sm text-gray-500">Contributors</div>
        </div>
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <div className="text-2xl font-bold text-purple-600">{stats.linesOfCode.toLocaleString()}</div>
          <div className="text-sm text-gray-500">Lines of Code</div>
        </div>
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <div className="text-2xl font-bold text-indigo-600">{stats.activeBranches}</div>
          <div className="text-sm text-gray-500">Active Branches</div>
        </div>
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <div className="text-2xl font-bold text-yellow-600">{stats.pendingReviews}</div>
          <div className="text-sm text-gray-500">Pending Reviews</div>
        </div>
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <div className="text-2xl font-bold text-green-600">{stats.approvedCommits}</div>
          <div className="text-sm text-gray-500">Approved</div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Commit Activity Chart */}
        <div className="bg-white p-6 rounded-lg border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Commit Activity (Last 30 Days)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={commitActivity}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                tickFormatter={(date) => format(parseISO(date), 'MM/dd')}
              />
              <YAxis />
              <Tooltip 
                labelFormatter={(date) => format(parseISO(date), 'MMM dd, yyyy')}
                formatter={(value, name) => [value, name === 'commits' ? 'Commits' : name]}
              />
              <Area 
                type="monotone" 
                dataKey="commits" 
                stroke="#8884d8" 
                fill="#8884d8" 
                fillOpacity={0.6}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Code Changes Chart */}
        <div className="bg-white p-6 rounded-lg border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Code Changes (Last 30 Days)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={commitActivity}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                tickFormatter={(date) => format(parseISO(date), 'MM/dd')}
              />
              <YAxis />
              <Tooltip 
                labelFormatter={(date) => format(parseISO(date), 'MMM dd, yyyy')}
              />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="additions" 
                stroke="#82ca9d" 
                name="Additions"
                strokeWidth={2}
              />
              <Line 
                type="monotone" 
                dataKey="deletions" 
                stroke="#ff7300" 
                name="Deletions"
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Top Contributors */}
        <div className="bg-white p-6 rounded-lg border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Contributors</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={contributors} layout="horizontal">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="name" type="category" width={100} />
              <Tooltip />
              <Bar dataKey="commits" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* File Types Distribution */}
        <div className="bg-white p-6 rounded-lg border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">File Types Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={fileTypes}
                cx="50%"
                cy="50%"
                outerRadius={80}
                dataKey="lines"
                label={({ extension, percent }) => `${extension} ${percent ? (percent * 100).toFixed(0) : 0}%`}
              >
                {fileTypes.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => [`${value} lines`, 'Lines of Code']} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Detailed Tables */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Contributors Details */}
        <div className="bg-white rounded-lg border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">Contributor Statistics</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Contributor
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Commits
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    +/-
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {contributors.map((contributor, index) => (
                  <tr key={index}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="w-3 h-3 rounded-full mr-3" style={{ backgroundColor: contributor.color }}></div>
                        <div className="text-sm font-medium text-gray-900">{contributor.name}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {contributor.commits}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <span className="text-green-600">+{contributor.additions}</span>
                      <span className="text-gray-400 mx-1">/</span>
                      <span className="text-red-600">-{contributor.deletions}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* File Types Details */}
        <div className="bg-white rounded-lg border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">File Type Breakdown</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Type
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Files
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Lines
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {fileTypes.map((fileType, index) => (
                  <tr key={index}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="w-3 h-3 rounded-full mr-3" style={{ backgroundColor: fileType.color }}></div>
                        <div className="text-sm font-medium text-gray-900">{fileType.extension}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {fileType.files}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {fileType.lines.toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RepositoryDashboard;