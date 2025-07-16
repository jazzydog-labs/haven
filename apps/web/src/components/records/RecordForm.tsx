import { useState, useEffect } from 'react';
import { RecordItem, RecordCreateDTO, RecordUpdateDTO } from '../../types/record';

interface RecordFormProps {
  record?: RecordItem | null;
  onSubmit: (data: RecordCreateDTO | RecordUpdateDTO) => Promise<void>;
  onCancel: () => void;
}

const RecordForm = ({ record, onSubmit, onCancel }: RecordFormProps) => {
  const [data, setData] = useState('{}');
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (record) {
      setData(JSON.stringify(record.data, null, 2));
    } else {
      setData('{}');
    }
  }, [record]);

  const validateJSON = (value: string): boolean => {
    try {
      JSON.parse(value);
      return true;
    } catch {
      return false;
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!validateJSON(data)) {
      setError('Invalid JSON format');
      return;
    }

    setSubmitting(true);
    try {
      const parsedData = JSON.parse(data);
      await onSubmit({ data: parsedData });
      onCancel(); // Close form on success
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="bg-white shadow sm:rounded-lg">
      <div className="px-4 py-5 sm:p-6">
        <h3 className="text-lg leading-6 font-medium text-gray-900">
          {record ? 'Edit Record' : 'Create New Record'}
        </h3>
        
        <form onSubmit={handleSubmit} className="mt-5">
          <div>
            <label htmlFor="data" className="block text-sm font-medium text-gray-700">
              Record Data (JSON)
            </label>
            <div className="mt-1">
              <textarea
                id="data"
                name="data"
                rows={10}
                className={`shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border rounded-md font-mono ${
                  error ? 'border-red-300' : 'border-gray-300'
                }`}
                value={data}
                onChange={(e) => setData(e.target.value)}
                placeholder='{\n  "key": "value"\n}'
              />
            </div>
            {error && (
              <p className="mt-2 text-sm text-red-600">{error}</p>
            )}
            <p className="mt-2 text-sm text-gray-500">
              Enter valid JSON data for the record
            </p>
          </div>

          <div className="mt-5 flex space-x-3">
            <button
              type="submit"
              disabled={submitting}
              className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {submitting ? 'Saving...' : (record ? 'Update' : 'Create')}
            </button>
            <button
              type="button"
              onClick={onCancel}
              className="inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RecordForm;