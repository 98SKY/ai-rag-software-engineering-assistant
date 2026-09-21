import type {
  AskRequest,
  AskResponse,
  Document,
  DocumentUploadResponse,
  HealthResponse,
} from "../types/api";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ??
  "http://localhost:8000/api/v1";

async function handleResponse<T>(
  response: Response,
): Promise<T> {
  if (!response.ok) {
    let message = `Request failed: ${response.status}`;

    try {
      const error = await response.json();

      if (error.detail) {
        message = error.detail;
      }
    } catch {
      // Response did not contain JSON.
    }

    throw new Error(message);
  }

  return response.json() as Promise<T>;
}

export async function getHealth(): Promise<HealthResponse> {
  const response = await fetch(
    `${API_BASE_URL}/health`,
  );

  return handleResponse<HealthResponse>(response);
}

export async function getDocuments(): Promise<Document[]> {
  const response = await fetch(
    `${API_BASE_URL}/documents`,
  );

  return handleResponse<Document[]>(response);
}

export async function uploadDocument(
  file: File,
): Promise<DocumentUploadResponse> {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/documents/upload`,
    {
      method: "POST",
      body: formData,
    },
  );

  return handleResponse<DocumentUploadResponse>(
    response,
  );
}

export async function askQuestion(
  request: AskRequest,
): Promise<AskResponse> {
  const response = await fetch(
    `${API_BASE_URL}/ask`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question: request.question,
        top_k: request.top_k ?? 5,
      }),
    },
  );

  return handleResponse<AskResponse>(response);
}