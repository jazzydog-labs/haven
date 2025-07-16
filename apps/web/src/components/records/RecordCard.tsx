import { RecordItem } from '../../types/record';

interface RecordCardProps {
  record: RecordItem;
  onEdit: (record: RecordItem) => void;
  onDelete: (record: RecordItem) => void;
  onView: (record: RecordItem) => void;
}

const RecordCard = ({ record, onEdit, onDelete, onView }: RecordCardProps) => {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="bg-white shadow rounded-lg p-6 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <h3 className="text-lg font-medium text-gray-900">
            Record ID: {record.id.slice(0, 8)}...
          </h3>
          <p className="text-sm text-gray-500 mt-1">
            Created: {formatDate(record.created_at)}
          </p>
          <p className="text-sm text-gray-500">
            Updated: {formatDate(record.updated_at)}
          </p>
        </div>
      </div>

      <div className="mb-4">
        <h4 className="text-sm font-medium text-gray-700 mb-2">Data:</h4>
        <pre className="bg-gray-50 p-3 rounded text-xs overflow-x-auto">
          {JSON.stringify(record.data, null, 2)}
        </pre>
      </div>

      <div className="flex space-x-3">
        <button
          onClick={() => onView(record)}
          className="text-sm text-blue-600 hover:text-blue-900"
        >
          View
        </button>
        <button
          onClick={() => onEdit(record)}
          className="text-sm text-green-600 hover:text-green-900"
        >
          Edit
        </button>
        <button
          onClick={() => onDelete(record)}
          className="text-sm text-red-600 hover:text-red-900"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default RecordCard;