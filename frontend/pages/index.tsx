/**
 * Main chat interface page.
 */

import React, { useState } from 'react';
import Head from 'next/head';
import ChatBox from '../components/ChatBox';
import ScoreDisplay from '../components/ScoreDisplay';
import { startConversation, sendMessage, Message, Evaluation } from '../lib/api';

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [topic, setTopic] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationEnded, setConversationEnded] = useState(false);
  const [evaluation, setEvaluation] = useState<Evaluation | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleStartConversation = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await startConversation();
      
      setSessionId(response.session_id);
      setTopic(response.topic);
      setMessages([
        { role: 'assistant', content: response.message }
      ]);
      setConversationEnded(false);
      setEvaluation(null);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to start conversation. Make sure the backend is running.');
      console.error('Error starting conversation:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async (message: string) => {
    if (!sessionId) return;

    try {
      setIsLoading(true);
      setError(null);
      
      // Add user message to display
      const newMessages: Message[] = [...messages, { role: 'user', content: message }];
      setMessages(newMessages);

      // Send to backend
      const response = await sendMessage(sessionId, message);
      
      // Add bot response
      setMessages([...newMessages, { role: 'assistant', content: response.message }]);
      
      // Check if conversation is complete
      if (response.is_complete && response.evaluation) {
        setConversationEnded(true);
        setEvaluation(response.evaluation);
      }
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to send message');
      console.error('Error sending message:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRestart = () => {
    setMessages([]);
    setSessionId(null);
    setTopic('');
    setConversationEnded(false);
    setEvaluation(null);
    setError(null);
  };

  return (
    <>
      <Head>
        <title>AI Chatbot Interview</title>
        <meta name="description" content="AI-powered role-playing chatbot" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <main className="min-h-screen bg-gradient-to-br from-blue-100 via-white to-purple-100 p-4 md:p-8">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-2">
              AI Chatbot Interview
            </h1>
            <p className="text-gray-600 text-lg">
              Engage in an insightful conversation and test your knowledge!
            </p>
          </div>

          {/* Error Display */}
          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-700">{error}</p>
            </div>
          )}

          {/* Main Content */}
          {!sessionId && !evaluation ? (
            // Welcome Screen
            <div className="max-w-2xl mx-auto">
              <div className="bg-white rounded-lg shadow-lg p-8 text-center">
                <div className="mb-6">
                  <svg
                    className="mx-auto h-24 w-24 text-blue-600"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                    />
                  </svg>
                </div>
                <h2 className="text-2xl font-bold text-gray-800 mb-4">
                  Welcome to the AI Interview Experience!
                </h2>
                <p className="text-gray-600 mb-6">
                  I'm a curious journalist looking to learn from your expertise. 
                  We'll have a conversation about a randomly selected topic, and 
                  at the end, you'll receive a detailed evaluation of your responses.
                </p>
                <button
                  onClick={handleStartConversation}
                  disabled={isLoading}
                  className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors text-lg font-semibold"
                >
                  {isLoading ? 'Starting...' : 'Start Interview'}
                </button>
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Chat Area */}
              <div className="lg:col-span-2">
                <div className="mb-4 flex items-center justify-between">
                  {topic && (
                    <div className="bg-white px-4 py-2 rounded-lg shadow">
                      <span className="text-gray-600">Topic: </span>
                      <span className="font-semibold text-gray-800">{topic}</span>
                    </div>
                  )}
                  <button
                    onClick={handleRestart}
                    className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 transition-colors"
                  >
                    New Interview
                  </button>
                </div>
                <div className="h-[600px]">
                  <ChatBox
                    messages={messages}
                    onSendMessage={handleSendMessage}
                    isLoading={isLoading}
                    disabled={conversationEnded}
                  />
                </div>
              </div>

              {/* Score Area */}
              <div className="lg:col-span-1">
                {evaluation ? (
                  <div className="max-h-[680px] overflow-y-auto">
                    <ScoreDisplay evaluation={evaluation} topic={topic} />
                  </div>
                ) : (
                  <div className="bg-white rounded-lg shadow-lg p-6 h-full flex items-center justify-center">
                    <div className="text-center text-gray-500">
                      <svg
                        className="mx-auto h-16 w-16 mb-4 text-gray-400"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                        />
                      </svg>
                      <p className="text-lg">Your evaluation will appear here</p>
                      <p className="text-sm mt-2">Complete the conversation to see your score</p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </main>
    </>
  );
}

