export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  due_date?: string; // ISO string format
  priority: number; // 1-5 scale
  tags?: string[]; // Array of tag strings
  recurring_interval?: 'daily' | 'weekly' | 'monthly' | 'yearly';
  user_id: string;
  created_at: string; // ISO string format
  updated_at: string; // ISO string format
}

export interface TaskCreate {
  title: string;
  description?: string;
  due_date?: string; // ISO string format
  priority?: number; // 1-5 scale, defaults to 3
  tags?: string[]; // Array of tag strings
  recurring_interval?: 'daily' | 'weekly' | 'monthly' | 'yearly';
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
  due_date?: string; // ISO string format
  priority?: number; // 1-5 scale
  tags?: string[]; // Array of tag strings
  recurring_interval?: 'daily' | 'weekly' | 'monthly' | 'yearly';
}