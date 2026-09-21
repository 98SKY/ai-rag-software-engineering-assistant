export interface HealthResponse {
  status: string;
  service: string;
  version: string;
}

export interface Document {
  id: string;
  filename: string;
  stored_filename: string;
  content_type: string;
  size: number;
  characters_extracted: number;
  chunk_count: number;
  created_at: string;
}

export interface DocumentUploadResponse {
  document_id: string;
  filename: string;
  content_type: string;
  size: number;
  characters_extracted: number;
  chunk_count: number;
  message: string;
}

export interface SourceReference {
  source_number: number;
  chunk_id: string;
  document_id: string;
  filename: string;
  chunk_index: number;
  score: number;
}

export interface RetrievalMetadata {
  top_score: number | null;
  top_k_requested: number;
  chunks_retrieved: number;
  retrieval_time_ms: number;
  generation_time_ms: number;
  total_time_ms: number;
}

export interface AskRequest {
  question: string;
  top_k?: number;
}

export interface AskResponse {
  question: string;
  answer: string;
  sources: SourceReference[];
  retrieval: RetrievalMetadata;
}