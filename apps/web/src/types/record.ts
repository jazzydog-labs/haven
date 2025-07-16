export interface Record {
  id: string;
  data: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface RecordCreateDTO {
  data: Record<string, any>;
}

export interface RecordUpdateDTO {
  data: Record<string, any>;
}

export interface RecordListResponse {
  items: Record[];
  total: number;
  limit: number;
  offset: number;
}