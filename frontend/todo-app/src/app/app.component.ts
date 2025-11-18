import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  standalone:false,
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

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

  // 🔥 FIXED BACKEND URL
  private apiUrl = 'https://to-do-list-backend-22oz.onrender.com';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.load();
  }

  // LOAD TASKS
  load() {
    this.http.get<any[]>(`${this.apiUrl}/tasks`).subscribe(res => {
      this.tasks = res;
    });
  }

  // COUNTS
  get pendingCount() {
    return this.tasks.filter(t => !t.done).length;
  }

  get completedCount() {
    return this.tasks.filter(t => t.done).length;
  }

  // THEME
  toggleTheme() {
    this.isDark = !this.isDark;
  }

  // OPEN/CLOSE FORM
  toggleForm() {
    this.showForm = !this.showForm;
  }

  // SAVE TASK
  saveTask() {
    this.http.post(`${this.apiUrl}/tasks`, this.model).subscribe(() => {
      this.showForm = false;
      this.model = { title: "", description: "", due_date: "", done: false };
      this.load();
    });
  }

  // MARK DONE / UNDO
  toggleDone(task: any) {
    task.done = !task.done;
    this.http.put(`${this.apiUrl}/tasks/${task.id}`, task)
      .subscribe(() => this.load());
  }

  // DELETE TASK
  deleteTask(id: number) {
    this.http.delete(`${this.apiUrl}/tasks/${id}`)
      .subscribe(() => this.load());
  }

}
