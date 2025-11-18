import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { Task } from '../models/task.model';

@Injectable({
  providedIn: 'root'
})
export class TaskService {

  private apiUrl = 'https://to-do-list-backend-22oz.onrender.com';
  private tasks$ = new BehaviorSubject<Task[]>([]);

  constructor(private http: HttpClient) {
    this.loadTasks();
  }

  loadTasks() {
    this.http.get<Task[]>(`${this.apiUrl}/tasks`)
      .subscribe(tasks => this.tasks$.next(tasks));
  }

  getTasks(): Observable<Task[]> {
    return this.tasks$.asObservable();
  }

  addTask(task: Task) {
    return this.http.post<Task>(`${this.apiUrl}/tasks`, task).pipe(
      tap(() => this.loadTasks())
    );
  }

  updateTask(task: Task) {
    return this.http.put<Task>(`${this.apiUrl}/tasks/${task.id}`, task).pipe(
      tap(() => this.loadTasks())
    );
  }

  deleteTask(id: number) {
    return this.http.delete(`${this.apiUrl}/tasks/${id}`).pipe(
      tap(() => this.loadTasks())
    );
  }
}
