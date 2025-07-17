import { useState, useEffect, useCallback } from "react";
import { RecordItem, RecordCreateDTO, RecordUpdateDTO } from "../types/record";
import { recordsAPI } from "../services/api/records";

export const useRecords = (limit: number = 10) => {
  const [records, setRecords] = useState<RecordItem[]>([]);
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchRecords = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const offset = (currentPage - 1) * limit;
      const response = await recordsAPI.list(limit, offset);
      setRecords(response.items);
      setTotal(response.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  }, [currentPage, limit]);

  useEffect(() => {
    fetchRecords();
  }, [fetchRecords]);

  const createRecord = async (data: RecordCreateDTO) => {
    const newRecord = await recordsAPI.create(data);
    await fetchRecords(); // Refresh the list
    return newRecord;
  };

  const updateRecord = async (id: string, data: RecordUpdateDTO) => {
    const updatedRecord = await recordsAPI.update(id, data);
    await fetchRecords(); // Refresh the list
    return updatedRecord;
  };

  const deleteRecord = async (id: string) => {
    await recordsAPI.delete(id);
    await fetchRecords(); // Refresh the list
  };

  const totalPages = Math.ceil(total / limit);

  return {
    records,
    total,
    currentPage,
    totalPages,
    loading,
    error,
    setCurrentPage,
    createRecord,
    updateRecord,
    deleteRecord,
    refetch: fetchRecords,
  };
};
