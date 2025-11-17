console.log("🔥 THIS IS THE DOWNLOADS VERSION 🔥");
import { Component, OnInit } from '@angular/core';
import { TaskService } from '../../services/task.service';
import { Task } from '../../models/task.model';

@Component({
  standalone: false,
  selector: 'app-task-list',
  templateUrl: './task-list.component.html',
  styleUrls: ['./task-list.component.css']
})
export class TaskListComponent implements OnInit {

  tasks: Task[] = [];
  hoveredTask: number | null = null;

  showUndoPopup = false;
  lastDeletedTask: Task | null = null;
  deleteTimeout: any;

  constructor(private svc: TaskService) {}

  ngOnInit(): void {
    this.load();
  }

  load() {
    this.svc.getTasks().subscribe(res => this.tasks = res);
  }

  toggleDone(task: Task) {
    if (task.done) return;

    const updated = { ...task, done: true };

    this.svc.updateTask(updated).subscribe(() => this.load());
  }

  edit(task: Task) {
    console.log("Edit feature coming soon:", task);
  }

  delete(task: Task) {
    this.lastDeletedTask = { ...task };

    this.tasks = this.tasks.filter(t => t.id !== task.id);

    this.showUndoPopup = true;

    this.deleteTimeout = setTimeout(() => {
      this.showUndoPopup = false;
    }, 5000);

    this.svc.deleteTask(task.id!).subscribe();
  }

  undoDelete() {
    if (!this.lastDeletedTask) return;

    const newTask = {
      title: this.lastDeletedTask.title,
      description: this.lastDeletedTask.description,
      done: this.lastDeletedTask.done
    };

    this.svc.addTask(newTask).subscribe(() => {
      clearTimeout(this.deleteTimeout);
      this.showUndoPopup = false;
      this.lastDeletedTask = null;
      this.load();
    });
  }
}
