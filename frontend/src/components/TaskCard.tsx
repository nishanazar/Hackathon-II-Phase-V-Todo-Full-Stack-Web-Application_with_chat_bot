import React from 'react';
import { Task } from '../types/task';

interface TaskCardProps {
  task: Task;
  onToggleComplete: (taskId: string) => void;
  onEdit: (taskId: string) => void;
  onDelete: (taskId: string) => void;
}

const TaskCard: React.FC<TaskCardProps> = ({ task, onToggleComplete, onEdit, onDelete }) => {
  const formatDate = (dateString: string) => {
    const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  const getPriorityColor = (priority: number) => {
    switch (priority) {
      case 1: return 'bg-green-100 text-green-800';
      case 2: return 'bg-lime-100 text-lime-800';
      case 3: return 'bg-yellow-100 text-yellow-800';
      case 4: return 'bg-orange-100 text-orange-800';
      case 5: return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityLabel = (priority: number) => {
    switch (priority) {
      case 1: return 'Low';
      case 2: return 'Med-Low';
      case 3: return 'Medium';
      case 4: return 'Med-High';
      case 5: return 'High';
      default: return 'None';
    }
  };

  return (
    <div className={`border rounded-lg p-4 shadow-sm transition-all duration-200 ${
      task.completed ? 'bg-gray-50 border-gray-200' : 'bg-white border-gray-300 hover:shadow-md'
    }`}>
      <div className="flex justify-between items-start">
        <div className="flex items-start space-x-3">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={() => onToggleComplete(task.id)}
            className="mt-1 h-5 w-5 text-indigo-600 rounded focus:ring-indigo-500"
          />
          <div>
            <h3 className={`font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
              {task.title}
            </h3>
            {task.description && (
              <p className="mt-1 text-sm text-gray-600">{task.description}</p>
            )}
          </div>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={() => onEdit(task.id)}
            className="text-sm font-medium text-indigo-600 hover:text-indigo-900"
          >
            Edit
          </button>
          <button
            onClick={() => onDelete(task.id)}
            className="text-sm font-medium text-red-600 hover:text-red-900"
          >
            Delete
          </button>
        </div>
      </div>

      <div className="mt-3 flex flex-wrap gap-2">
        {/* Priority Badge */}
        <span className={`text-xs px-2 py-1 rounded-full ${getPriorityColor(task.priority)}`}>
          {getPriorityLabel(task.priority)} Priority
        </span>

        {/* Due Date */}
        {task.due_date && (
          <span className="text-xs px-2 py-1 rounded-full bg-blue-100 text-blue-800">
            Due: {formatDate(task.due_date)}
          </span>
        )}

        {/* Recurring Indicator */}
        {task.recurring_interval && (
          <span className="text-xs px-2 py-1 rounded-full bg-purple-100 text-purple-800">
            Repeats: {task.recurring_interval.charAt(0).toUpperCase() + task.recurring_interval.slice(1)}
          </span>
        )}

        {/* Tags */}
        {task.tags && task.tags.length > 0 && (
          <div className="flex flex-wrap gap-1">
            {task.tags.map((tag, index) => (
              <span 
                key={index} 
                className="text-xs px-2 py-1 rounded-full bg-gray-100 text-gray-800"
              >
                #{tag}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default TaskCard;