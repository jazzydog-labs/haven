import React, { useState } from "react";
import {
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon,
  DocumentTextIcon,
} from "@heroicons/react/24/outline";

interface ReviewPanelProps {
  currentStatus: "pending" | "approved" | "needs_revision" | "draft";
  onStatusChange: (status: string) => void;
  reviewers?: string[];
  notes?: string;
}

const ReviewPanel: React.FC<ReviewPanelProps> = ({
  currentStatus,
  onStatusChange,
  reviewers = [],
  notes = "",
}) => {
  const [showNotes, setShowNotes] = useState(false);
  const [reviewNotes, setReviewNotes] = useState(notes);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const statusOptions = [
    {
      value: "pending",
      label: "Pending Review",
      icon: ClockIcon,
      color:
        "text-yellow-600 bg-yellow-50 border-yellow-200 hover:bg-yellow-100",
    },
    {
      value: "approved",
      label: "Approved",
      icon: CheckCircleIcon,
      color: "text-green-600 bg-green-50 border-green-200 hover:bg-green-100",
    },
    {
      value: "needs_revision",
      label: "Needs Revision",
      icon: XCircleIcon,
      color: "text-red-600 bg-red-50 border-red-200 hover:bg-red-100",
    },
    {
      value: "draft",
      label: "Draft",
      icon: DocumentTextIcon,
      color: "text-gray-600 bg-gray-50 border-gray-200 hover:bg-gray-100",
    },
  ];

  const handleStatusChange = async (newStatus: string) => {
    setIsSubmitting(true);
    try {
      await onStatusChange(newStatus);
    } catch (error) {
      console.error("Failed to update status:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleNotesSubmit = async () => {
    setIsSubmitting(true);
    try {
      // In a real app, this would save the notes via API
      console.log("Saving review notes:", reviewNotes);
      setShowNotes(false);
    } catch (error) {
      console.error("Failed to save notes:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const currentOption = statusOptions.find(
    (opt) => opt.value === currentStatus
  );

  return (
    <div className="review-panel bg-white border border-gray-200 rounded-lg p-4 min-w-80">
      {/* Current Status */}
      <div className="mb-4">
        <h3 className="text-sm font-medium text-gray-900 mb-2">
          Review Status
        </h3>
        {currentOption && (
          <div
            className={`flex items-center px-3 py-2 rounded-md border ${currentOption.color}`}
          >
            <currentOption.icon className="h-5 w-5 mr-2" />
            <span className="font-medium">{currentOption.label}</span>
          </div>
        )}
      </div>

      {/* Status Change Actions */}
      <div className="mb-4">
        <h4 className="text-sm font-medium text-gray-900 mb-2">
          Change Status
        </h4>
        <div className="space-y-2">
          {statusOptions.map((option) => {
            if (option.value === currentStatus) return null;

            return (
              <button
                key={option.value}
                onClick={() => handleStatusChange(option.value)}
                disabled={isSubmitting}
                className={`w-full flex items-center px-3 py-2 rounded-md border text-sm font-medium transition-colors ${
                  option.color
                } ${isSubmitting ? "opacity-50 cursor-not-allowed" : ""}`}
              >
                <option.icon className="h-4 w-4 mr-2" />
                {option.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* Review Notes */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <h4 className="text-sm font-medium text-gray-900">Review Notes</h4>
          <button
            onClick={() => setShowNotes(!showNotes)}
            className="text-sm text-blue-600 hover:text-blue-800"
          >
            {showNotes ? "Hide" : "Add Notes"}
          </button>
        </div>

        {showNotes && (
          <div className="space-y-3">
            <textarea
              value={reviewNotes}
              onChange={(e) => setReviewNotes(e.target.value)}
              placeholder="Add your review notes here..."
              className="w-full h-24 px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-blue-500 focus:border-blue-500"
            />
            <div className="flex space-x-2">
              <button
                onClick={handleNotesSubmit}
                disabled={isSubmitting || !reviewNotes.trim()}
                className="px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Save Notes
              </button>
              <button
                onClick={() => setShowNotes(false)}
                className="px-3 py-1 bg-gray-200 text-gray-700 text-sm rounded hover:bg-gray-300"
              >
                Cancel
              </button>
            </div>
          </div>
        )}

        {notes && !showNotes && (
          <div className="mt-2 p-3 bg-gray-50 rounded border text-sm text-gray-700">
            {notes}
          </div>
        )}
      </div>

      {/* Reviewers */}
      {reviewers.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-medium text-gray-900 mb-2">Reviewers</h4>
          <div className="space-y-1">
            {reviewers.map((reviewer, index) => (
              <div
                key={index}
                className="flex items-center text-sm text-gray-600"
              >
                <div className="w-6 h-6 bg-gray-300 rounded-full flex items-center justify-center text-xs font-medium mr-2">
                  {reviewer.charAt(0).toUpperCase()}
                </div>
                {reviewer}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="border-t border-gray-200 pt-4">
        <h4 className="text-sm font-medium text-gray-900 mb-2">
          Quick Actions
        </h4>
        <div className="space-y-2">
          <button className="w-full text-left px-3 py-2 text-sm text-gray-600 hover:bg-gray-50 rounded">
            📧 Request Review
          </button>
          <button className="w-full text-left px-3 py-2 text-sm text-gray-600 hover:bg-gray-50 rounded">
            🔗 Copy Commit Link
          </button>
          <button className="w-full text-left px-3 py-2 text-sm text-gray-600 hover:bg-gray-50 rounded">
            📄 Export Diff
          </button>
        </div>
      </div>

      {/* Review History */}
      <div className="border-t border-gray-200 pt-4 mt-4">
        <h4 className="text-sm font-medium text-gray-900 mb-2">
          Review History
        </h4>
        <div className="text-xs text-gray-500 space-y-1">
          <div>Created • Today at 2:30 PM</div>
          <div>Status: Pending Review • Today at 2:30 PM</div>
        </div>
      </div>
    </div>
  );
};

export default ReviewPanel;
