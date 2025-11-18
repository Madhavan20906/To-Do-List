import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  standalone:false,
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  private apiUrl = 'https://to-do-list-backend-22oz.onrender.com';

  tasks: any[] = [];
  search = "";
  isDark = false;

  showForm = false;

  model: any = {
    title: "",
    description: "",
    due_date: "",
    done: false
  };

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.load();
  }

  load() {
    this.http.get<any[]>(`${this.apiUrl}/tasks`).subscribe(res => {
      this.tasks = res;
    });
  }

  get pendingCount() {
    return this.tasks.filter(t => !t.done).length;
  }

  get completedCount() {
    return this.tasks.filter(t => t.done).length;
  }

  toggleTheme() {
    this.isDark = !this.isDark;
  }

  toggleForm() {
    this.showForm = !this.showForm;
  }

  saveTask() {
    this.http.post(`${this.apiUrl}/tasks`, this.model).subscribe(() => {
      this.showForm = false;
      this.model = { title: "", description: "", due_date: "", done: false };
      this.load();
    });
  }

  toggleDone(task: any) {
    task.done = !task.done;
    this.http.put(`${this.apiUrl}/tasks/${task.id}`, task).subscribe(() => this.load());
  }

  deleteTask(id: number) {
    this.http.delete(`${this.apiUrl}/tasks/${id}`).subscribe(() => this.load());
  }
}
