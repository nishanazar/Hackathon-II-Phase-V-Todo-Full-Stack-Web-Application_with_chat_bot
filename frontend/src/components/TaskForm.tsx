import React, { useState, useEffect } from 'react';
import { Task, TaskCreate } from '../types/task';
import DatePicker from './DatePicker';
import PrioritySelector from './PrioritySelector';
import TagInput from './TagInput';

interface TaskFormProps {
  task?: Task; // If provided, we're editing an existing task
  onSubmit: (taskData: TaskCreate) => void;
  onCancel: () => void;
}

const TaskForm: React.FC<TaskFormProps> = ({ task, onSubmit, onCancel }) => {
  const isEditing = !!task;

  const [formData, setFormData] = useState<TaskCreate>({
    title: task?.title || '',
    description: task?.description || '',
    due_date: task?.due_date || undefined,
    priority: task?.priority || 3,
    tags: task?.tags || [],
    recurring_interval: task?.recurring_interval || undefined,
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (task) {
      setFormData({
        title: task.title,
        description: task.description || '',
        due_date: task.due_date || undefined,
        priority: task.priority,
        tags: task.tags || [],
        recurring_interval: task.recurring_interval || undefined,
      });
    }
  }, [task]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handlePriorityChange = (priority: number) => {
    setFormData(prev => ({
      ...prev,
      priority
    }));
  };

  const handleTagsChange = (tags: string[]) => {
    setFormData(prev => ({
      ...prev,
      tags
    }));
  };

  const handleDateChange = (date: Date | null) => {
    setFormData(prev => ({
      ...prev,
      due_date: date ? date.toISOString() : undefined
    }));
  };

  const handleRecurringChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value as 'daily' | 'weekly' | 'monthly' | 'yearly' | '';
    setFormData(prev => ({
      ...prev,
      recurring_interval: value || undefined
    }));
  };

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    } else if (formData.title.length < 1 || formData.title.length > 200) {
      newErrors.title = 'Title must be between 1 and 200 characters';
    }

    if (formData.description && formData.description.length > 1000) {
      newErrors.description = 'Description must be less than 1000 characters';
    }

    if (formData.tags && formData.tags.length > 10) {
      newErrors.tags = 'Maximum 10 tags allowed';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (validate()) {
      onSubmit(formData);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700">
          Title *
        </label>
        <input
          type="text"
          id="title"
          name="title"
          value={formData.title}
          onChange={handleChange}
          className={`mt-1 block w-full px-3 py-2 border ${
            errors.title ? 'border-red-500' : 'border-gray-300'
          } rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500`}
        />
        {errors.title && <p className="mt-1 text-sm text-red-600">{errors.title}</p>}
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700">
          Description
        </label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          rows={3}
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        />
        {errors.description && <p className="mt-1 text-sm text-red-600">{errors.description}</p>}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <DatePicker 
            selectedDate={formData.due_date ? new Date(formData.due_date) : null}
            onChange={handleDateChange}
            label="Due Date"
          />
        </div>

        <div>
          <label htmlFor="recurring_interval" className="block text-sm font-medium text-gray-700">
            Recurring Interval
          </label>
          <select
            id="recurring_interval"
            name="recurring_interval"
            value={formData.recurring_interval || ''}
            onChange={handleRecurringChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="">Does not repeat</option>
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
            <option value="yearly">Yearly</option>
          </select>
        </div>
      </div>

      <div>
        <PrioritySelector
          selectedPriority={formData.priority}
          onChange={handlePriorityChange}
        />
      </div>

      <div>
        <TagInput
          selectedTags={formData.tags || []}
          onChange={handleTagsChange}
        />
      </div>

      <div className="flex justify-end space-x-3 pt-4">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Cancel
        </button>
        <button
          type="submit"
          className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          {isEditing ? 'Update Task' : 'Create Task'}
        </button>
      </div>
    </form>
  );
};

export default TaskForm;