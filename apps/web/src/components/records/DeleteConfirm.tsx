import { RecordItem } from '../../types/record';

interface DeleteConfirmProps {
  record: RecordItem;
  onConfirm: () => void;
  onCancel: () => void;
  isDeleting: boolean;
}

const DeleteConfirm = ({ record, onConfirm, onCancel, isDeleting }: DeleteConfirmProps) => {
  return (
    <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-md w-full p-6">
        <div className="mb-4">
          <h3 className="text-lg font-medium text-gray-900">Delete Record</h3>
          <p className="mt-2 text-sm text-gray-500">
            Are you sure you want to delete this record? This action cannot be undone.
          </p>
        </div>

        <div className="mb-6 bg-gray-50 p-3 rounded">
          <p className="text-sm text-gray-600">
            <span className="font-medium">Record ID:</span> {record.id}
          </p>
          <p className="text-sm text-gray-600 mt-1">
            <span className="font-medium">Created:</span>{' '}
            {new Date(record.created_at).toLocaleString()}
          </p>
        </div>

        <div className="flex space-x-3 justify-end">
          <button
            type="button"
            onClick={onCancel}
            disabled={isDeleting}
            className="inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={onConfirm}
            disabled={isDeleting}
            className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
          >
            {isDeleting ? 'Deleting...' : 'Delete'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default DeleteConfirm;