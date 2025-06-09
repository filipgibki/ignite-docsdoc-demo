export type Priority = 'Low' | 'Medium' | 'High';

export interface Task {
  id: number;
  title: string;
  completed: boolean;
  priority: Priority;
} 