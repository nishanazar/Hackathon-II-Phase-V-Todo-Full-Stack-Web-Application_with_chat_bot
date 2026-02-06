'use client';

import { useState, useRef, useEffect } from 'react';
import { getCurrentSession } from '@/lib/session-utils';
import { API_BASE_URL } from '@/lib/api';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
}

const FloatingChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      role: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Get the current user ID from the session
      const session = await getCurrentSession();
      if (!session) {
        throw new Error('No active session found. Please log in.');
      }

      const userId = session.user.id;

      // Call backend API to get AI response
      const response = await fetch(`${API_BASE_URL}/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session.token}`,
        },
        body: JSON.stringify({ message: inputValue }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Add AI response
      const aiMessage: Message = {
        id: `ai-${Date.now()}`,
        content: data.response || 'Sorry, I could not process your request.',
        role: 'assistant',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, aiMessage]);

      // Check if tasks were modified and trigger a refresh if needed
      // This will notify other parts of the app to refresh task lists
      if (data.task_created || (data.tool_calls && data.tool_calls.some((call: any) =>
        ['add_task', 'update_task', 'delete_task', 'complete_task'].includes(call.name)))) {
        // Dispatch a custom event to notify other components to refresh tasks
        window.dispatchEvent(new CustomEvent('tasksModified', { detail: { action: 'refresh' } }));
      }
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        content: 'Sorry, there was an error processing your request. Please try again.',
        role: 'assistant',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={`fixed bottom-4 right-4 z-50 transition-all duration-300 ${isOpen ? 'w-full max-w-full md:max-w-md h-[60vh] md:h-[400px] inset-x-0 md:right-4 md:left-auto' : 'w-auto h-auto'}`}>
      {isOpen ? (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl overflow-hidden w-full h-full flex flex-col border border-gray-200 dark:border-gray-700 flex-nowrap">
          <div className="flex justify-between items-center p-3 bg-blue-500 text-white flex-shrink-0">
            <span className="truncate">AI Assistant</span>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white hover:bg-blue-600 rounded-full p-1 transition-colors ml-2"
              aria-label="Close chat"
            >
              ×
            </button>
          </div>
          <div className="flex-grow overflow-y-auto p-3 bg-gray-50 dark:bg-gray-900">
            {messages.length === 0 ? (
              <div className="h-full flex items-center justify-center text-gray-500 dark:text-gray-400 p-4">
                <p className="text-center">Ask me anything! How can I help you today?</p>
              </div>
            ) : (
              <div className="space-y-2">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-lg p-3 ${
                        message.role === 'user'
                          ? 'bg-blue-500 text-white rounded-br-none break-words'
                          : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-bl-none break-words'
                      }`}
                    >
                      {message.content}
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-lg p-3 rounded-bl-none max-w-[80%]">
                      <div className="flex space-x-2">
                        <div className="w-2 h-2 rounded-full bg-gray-500 animate-bounce"></div>
                        <div className="w-2 h-2 rounded-full bg-gray-500 animate-bounce delay-100"></div>
                        <div className="w-2 h-2 rounded-full bg-gray-500 animate-bounce delay-200"></div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>
          <form onSubmit={handleSubmit} className="border-t border-gray-200 dark:border-gray-700 p-2 bg-white dark:bg-gray-800 flex flex-col sm:flex-row gap-2">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Type your message..."
              className="flex-grow px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
              disabled={isLoading}
            />
            <button
              type="submit"
              className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50 whitespace-nowrap"
              disabled={!inputValue.trim() || isLoading}
            >
              Send
            </button>
          </form>
        </div>
      ) : (
        <button
          onClick={() => setIsOpen(true)}
          className="bg-blue-500 text-white rounded-full p-4 shadow-lg hover:bg-blue-600 transition-colors transform hover:scale-105 active:scale-95"
          aria-label="Open chat"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </button>
      )}
    </div>
  );
};

export default FloatingChatWidget;