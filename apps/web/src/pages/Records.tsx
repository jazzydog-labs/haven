import { useState } from "react";
import { useRecords } from "../hooks/useRecords";
import RecordList from "../components/records/RecordList";
import RecordForm from "../components/records/RecordForm";
import RecordDetail from "../components/records/RecordDetail";
import DeleteConfirm from "../components/records/DeleteConfirm";
import { RecordItem } from "../types/record";

const Records = () => {
  const [showForm, setShowForm] = useState(false);
  const [selectedRecord, setSelectedRecord] = useState<RecordItem | null>(null);
  const [viewingRecord, setViewingRecord] = useState<RecordItem | null>(null);
  const [deletingRecord, setDeletingRecord] = useState<RecordItem | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);

  const {
    records,
    currentPage,
    totalPages,
    loading,
    error,
    setCurrentPage,
    createRecord,
    updateRecord,
    deleteRecord,
  } = useRecords(10);

  const handleCreate = () => {
    setSelectedRecord(null);
    setShowForm(true);
  };

  const handleEdit = (record: RecordItem) => {
    setSelectedRecord(record);
    setShowForm(true);
    setViewingRecord(null);
  };

  const handleView = (record: RecordItem) => {
    setViewingRecord(record);
  };

  const handleDelete = (record: RecordItem) => {
    setDeletingRecord(record);
  };

  const handleFormSubmit = async (data: any) => {
    if (selectedRecord) {
      await updateRecord(selectedRecord.id, data);
    } else {
      await createRecord(data);
    }
    setShowForm(false);
    setSelectedRecord(null);
  };

  const handleConfirmDelete = async () => {
    if (deletingRecord) {
      setIsDeleting(true);
      try {
        await deleteRecord(deletingRecord.id);
        setDeletingRecord(null);
      } catch (err) {
        console.error("Failed to delete record:", err);
      } finally {
        setIsDeleting(false);
      }
    }
  };

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="sm:flex sm:items-center sm:justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Records Management
          </h1>
          <p className="mt-2 text-sm text-gray-700">
            Create, view, edit, and delete records with JSON data
          </p>
        </div>
        <div className="mt-4 sm:mt-0">
          <button
            type="button"
            onClick={handleCreate}
            className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <svg
              className="-ml-1 mr-2 h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                clipRule="evenodd"
              />
            </svg>
            New Record
          </button>
        </div>
      </div>

      {showForm && (
        <div className="mb-6">
          <RecordForm
            record={selectedRecord}
            onSubmit={handleFormSubmit}
            onCancel={() => {
              setShowForm(false);
              setSelectedRecord(null);
            }}
          />
        </div>
      )}

      {!showForm && (
        <RecordList
          records={records}
          loading={loading}
          error={error}
          onEdit={handleEdit}
          onDelete={handleDelete}
          onView={handleView}
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={setCurrentPage}
        />
      )}

      {viewingRecord && (
        <RecordDetail
          record={viewingRecord}
          onClose={() => setViewingRecord(null)}
          onEdit={() => {
            handleEdit(viewingRecord);
          }}
        />
      )}

      {deletingRecord && (
        <DeleteConfirm
          record={deletingRecord}
          onConfirm={handleConfirmDelete}
          onCancel={() => setDeletingRecord(null)}
          isDeleting={isDeleting}
        />
      )}
    </div>
  );
};

export default Records;
