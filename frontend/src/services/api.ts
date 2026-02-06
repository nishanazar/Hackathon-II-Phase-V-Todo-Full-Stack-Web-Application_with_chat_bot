import axios from 'axios';
import { Task, TaskCreate, TaskUpdate } from '../types/task';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add JWT token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('jwt_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// API functions for task operations
export const taskApi = {
  // Get all tasks for a user
  getTasks: async (userId: string, filters?: { 
    status?: 'all' | 'pending' | 'completed', 
    priority?: number, 
    due_after?: string, 
    due_before?: string, 
    tags?: string 
  }) => {
    const params = new URLSearchParams();
    
    if (filters?.status) params.append('status_filter', filters.status);
    if (filters?.priority) params.append('priority', filters.priority.toString());
    if (filters?.due_after) params.append('due_after', filters.due_after);
    if (filters?.due_before) params.append('due_before', filters.due_before);
    if (filters?.tags) params.append('tags', filters.tags);
    
    const queryString = params.toString();
    const url = queryString ? `/api/${userId}/tasks?${queryString}` : `/api/${userId}/tasks`;
    
    const response = await api.get<Task[]>(url);
    return response.data;
  },

  // Get a specific task
  getTask: async (userId: string, taskId: string) => {
    const response = await api.get<Task>(`/api/${userId}/tasks/${taskId}`);
    return response.data;
  },

  // Create a new task
  createTask: async (userId: string, taskData: TaskCreate) => {
    const response = await api.post<Task>(`/api/${userId}/tasks`, taskData);
    return response.data;
  },

  // Update a task
  updateTask: async (userId: string, taskId: string, taskData: TaskUpdate) => {
    const response = await api.put<Task>(`/api/${userId}/tasks/${taskId}`, taskData);
    return response.data;
  },

  // Partially update a task
  updateTaskPartial: async (userId: string, taskId: string, taskData: TaskUpdate) => {
    const response = await api.patch<Task>(`/api/${userId}/tasks/${taskId}`, taskData);
    return response.data;
  },

  // Mark a task as complete
  completeTask: async (userId: string, taskId: string) => {
    const response = await api.patch<Task>(`/api/${userId}/tasks/${taskId}/complete`);
    return response.data;
  },

  // Delete a task
  deleteTask: async (userId: string, taskId: string) => {
    await api.delete(`/api/${userId}/tasks/${taskId}`);
  },
};