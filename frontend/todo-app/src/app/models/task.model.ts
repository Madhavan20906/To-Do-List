export interface Task {
  id?: number;
  title: string;
  description?: string;
  done?: boolean;
  due_date?: string | null;
  created_at?: string;
}
