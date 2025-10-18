/**
 * API client for communicating with the backend chatbot service.
 */

import axios from "axios";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:5001/api";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export interface StartConversationResponse {
  session_id: string;
  topic: string;
  message: string;
  is_complete: boolean;
}

export interface SendMessageResponse {
  message: string;
  is_complete: boolean;
  evaluation?: Evaluation;
}

export interface Evaluation {
  keyword_analysis: {
    [keyword: string]: {
      mentioned: boolean;
      relevance_score: number;
      comment: string;
    };
  };
  coverage_score: number;
  relevance_score: number;
  depth_score: number;
  total_score: number;
  overall_feedback: string;
}

export interface Message {
  role: "user" | "assistant";
  content: string;
}

/**
 * Start a new conversation with a random topic
 */
export async function startConversation(): Promise<StartConversationResponse> {
  const response = await apiClient.post<StartConversationResponse>(
    "/conversation/start"
  );
  return response.data;
}

/**
 * Send a message in an ongoing conversation
 */
export async function sendMessage(
  sessionId: string,
  message: string
): Promise<SendMessageResponse> {
  const response = await apiClient.post<SendMessageResponse>(
    "/conversation/message",
    {
      session_id: sessionId,
      message,
    }
  );
  return response.data;
}

/**
 * Manually end a conversation and get evaluation
 */
export async function endConversation(
  sessionId: string
): Promise<{ evaluation: Evaluation; is_complete: boolean }> {
  const response = await apiClient.post("/conversation/end", {
    session_id: sessionId,
  });
  return response.data;
}

/**
 * Get list of available topics
 */
export async function getTopics(): Promise<string[]> {
  const response = await apiClient.get<{ topics: string[] }>("/topics");
  return response.data.topics;
}
