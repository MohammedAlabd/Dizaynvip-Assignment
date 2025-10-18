/**
 * ScoreDisplay component for showing evaluation results.
 */

import React from 'react';
import { Evaluation } from '../lib/api';

interface ScoreDisplayProps {
  evaluation: Evaluation;
  topic: string;
}

const ScoreDisplay: React.FC<ScoreDisplayProps> = ({ evaluation, topic }) => {
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreLabel = (score: number) => {
    if (score >= 90) return 'Excellent!';
    if (score >= 80) return 'Great!';
    if (score >= 70) return 'Good!';
    if (score >= 60) return 'Fair';
    if (score >= 50) return 'Needs Improvement';
    return 'Keep Practicing';
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Evaluation Results</h2>
      
      {/* Total Score */}
      <div className="mb-6 p-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border-2 border-blue-200">
        <div className="text-center">
          <p className="text-gray-600 mb-2">Your Final Score</p>
          <div className={`text-6xl font-bold ${getScoreColor(evaluation.total_score)}`}>
            {evaluation.total_score}
          </div>
          <p className="text-xl text-gray-700 mt-2">{getScoreLabel(evaluation.total_score)}</p>
        </div>
      </div>

      {/* Score Breakdown */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-3">Score Breakdown</h3>
        <div className="space-y-3">
          <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
            <span className="text-gray-700">Keyword Coverage</span>
            <span className="font-semibold text-gray-900">{evaluation.coverage_score} / 40</span>
          </div>
          <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
            <span className="text-gray-700">Contextual Relevance</span>
            <span className="font-semibold text-gray-900">{evaluation.relevance_score} / 40</span>
          </div>
          <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
            <span className="text-gray-700">Depth of Explanation</span>
            <span className="font-semibold text-gray-900">{evaluation.depth_score} / 20</span>
          </div>
        </div>
      </div>

      {/* Keyword Analysis */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-3">Keyword Analysis for "{topic}"</h3>
        <div className="space-y-2">
          {Object.entries(evaluation.keyword_analysis).map(([keyword, analysis]) => (
            <div
              key={keyword}
              className={`p-3 rounded border ${
                analysis.mentioned
                  ? 'bg-green-50 border-green-200'
                  : 'bg-red-50 border-red-200'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-2">
                    <span className="font-medium text-gray-800">{keyword}</span>
                    {analysis.mentioned ? (
                      <span className="text-xs bg-green-200 text-green-800 px-2 py-1 rounded">
                        Mentioned
                      </span>
                    ) : (
                      <span className="text-xs bg-red-200 text-red-800 px-2 py-1 rounded">
                        Not Mentioned
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-gray-600 mt-1">{analysis.comment}</p>
                </div>
                {analysis.mentioned && (
                  <div className="ml-4 text-right">
                    <span className="text-sm text-gray-500">Relevance</span>
                    <div className="font-semibold text-gray-800">{analysis.relevance_score}/10</div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Overall Feedback */}
      <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
        <h3 className="text-lg font-semibold text-gray-800 mb-2">Overall Feedback</h3>
        <p className="text-gray-700">{evaluation.overall_feedback}</p>
      </div>
    </div>
  );
};

export default ScoreDisplay;

