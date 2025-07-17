import {
  RecordItem,
  RecordCreateDTO,
  RecordUpdateDTO,
  RecordListResponse,
} from "../../types/record";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8080";

export const recordsAPI = {
  list: async (
    limit: number = 10,
    offset: number = 0
  ): Promise<RecordListResponse> => {
    const response = await fetch(
      `${API_BASE_URL}/api/v1/records?limit=${limit}&offset=${offset}`,
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    if (!response.ok) {
      throw new Error(`Failed to fetch records: ${response.statusText}`);
    }

    return response.json();
  },

  create: async (data: RecordCreateDTO): Promise<RecordItem> => {
    const response = await fetch(`${API_BASE_URL}/api/v1/records`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`Failed to create record: ${response.statusText}`);
    }

    return response.json();
  },

  get: async (id: string): Promise<RecordItem> => {
    const response = await fetch(`${API_BASE_URL}/api/v1/records/${id}`, {
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch record: ${response.statusText}`);
    }

    return response.json();
  },

  update: async (id: string, data: RecordUpdateDTO): Promise<RecordItem> => {
    const response = await fetch(`${API_BASE_URL}/api/v1/records/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`Failed to update record: ${response.statusText}`);
    }

    return response.json();
  },

  partialUpdate: async (
    id: string,
    data: RecordUpdateDTO
  ): Promise<RecordItem> => {
    const response = await fetch(`${API_BASE_URL}/api/v1/records/${id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(
        `Failed to partially update record: ${response.statusText}`
      );
    }

    return response.json();
  },

  delete: async (id: string): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/api/v1/records/${id}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error(`Failed to delete record: ${response.statusText}`);
    }
  },
};
