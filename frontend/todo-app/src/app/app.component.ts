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

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.load();
  }

  // LOAD TASKS
  load() {
    this.http.get<any[]>('/api/tasks').subscribe(res => {
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
    this.http.post('/api/tasks', this.model).subscribe(() => {
      this.showForm = false;
      this.model = { title: "", description: "", due_date: "", done: false };
      this.load();
    });
  }

  // MARK DONE / UNDO
  toggleDone(task: any) {
    task.done = !task.done;
    this.http.put(`/api/tasks/${task.id}`, task).subscribe(() => this.load());
  }

  // DELETE TASK
  deleteTask(id: number) {
    this.http.delete(`/api/tasks/${id}`).subscribe(() => this.load());
  }

}
