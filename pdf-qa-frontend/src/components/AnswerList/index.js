import React from 'react';
import { MessageSquare, User, Bot } from 'lucide-react';

const AnswerList = ({ questions }) => {
  return (
    <div className="space-y-4 sm:space-y-6">
      {questions.map((qa, index) => (
        <div key={index} className="bg-blue-50 rounded-xl p-3 sm:p-6">
          {/* Question */}
          <div className="flex items-start gap-3 sm:gap-4 mb-3 sm:mb-4">
            <div className="flex-shrink-0 bg-blue-100 p-1.5 sm:p-2 rounded-lg">
              <User className="h-4 w-4 sm:h-5 sm:w-5 text-blue-600" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="font-medium text-blue-900 text-sm sm:text-base break-words">
                {qa.question}
              </p>
              <p className="text-xs sm:text-sm text-blue-400 mt-1">
                {new Date(qa.timestamp).toLocaleString()}
              </p>
            </div>
          </div>
          
          {/* Answer */}
          <div className="flex items-start gap-3 sm:gap-4 ml-4 sm:ml-8">
            <div className="flex-shrink-0 bg-green-100 p-1.5 sm:p-2 rounded-lg">
              <Bot className="h-4 w-4 sm:h-5 sm:w-5 text-green-600" />
            </div>
            <p className="flex-1 text-sm sm:text-base text-green-900 bg-green-50 p-3 sm:p-4 rounded-lg border border-green-100 break-words">
              {qa.answer}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default AnswerList;