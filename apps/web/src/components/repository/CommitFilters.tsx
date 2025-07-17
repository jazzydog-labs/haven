import React from 'react';
import { FunnelIcon, CalendarIcon, UserIcon } from '@heroicons/react/24/outline';

interface CommitFiltersProps {
  author: string;
  dateFrom: string;
  dateTo: string;
  onAuthorChange: (value: string) => void;
  onDateFromChange: (value: string) => void;
  onDateToChange: (value: string) => void;
  onClearFilters: () => void;
  hasActiveFilters: boolean;
}

export const CommitFilters: React.FC<CommitFiltersProps> = ({
  author,
  dateFrom,
  dateTo,
  onAuthorChange,
  onDateFromChange,
  onDateToChange,
  onClearFilters,
  hasActiveFilters,
}) => {
  const [isExpanded, setIsExpanded] = React.useState(false);

  return (
    <div className="bg-gray-50 rounded-lg p-4 mb-4">
      <div className="flex items-center justify-between mb-4">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="flex items-center space-x-2 text-gray-700 hover:text-gray-900"
        >
          <FunnelIcon className="h-5 w-5" />
          <span className="font-medium">Filters</span>
          {hasActiveFilters && (
            <span className="ml-2 px-2 py-0.5 text-xs bg-blue-100 text-blue-800 rounded-full">
              Active
            </span>
          )}
        </button>
        {hasActiveFilters && (
          <button
            onClick={onClearFilters}
            className="text-sm text-blue-600 hover:text-blue-800"
          >
            Clear all
          </button>
        )}
      </div>

      {isExpanded && (
        <div className="space-y-4">
          {/* Author Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              <UserIcon className="inline h-4 w-4 mr-1" />
              Author
            </label>
            <input
              type="text"
              value={author}
              onChange={(e) => onAuthorChange(e.target.value)}
              placeholder="Filter by author name or email"
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>

          {/* Date Range */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                <CalendarIcon className="inline h-4 w-4 mr-1" />
                From Date
              </label>
              <input
                type="date"
                value={dateFrom}
                onChange={(e) => onDateFromChange(e.target.value)}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                <CalendarIcon className="inline h-4 w-4 mr-1" />
                To Date
              </label>
              <input
                type="date"
                value={dateTo}
                onChange={(e) => onDateToChange(e.target.value)}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};