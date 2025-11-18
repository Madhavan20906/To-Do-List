import { Component, Output, EventEmitter } from '@angular/core';
import { TaskService } from '../../services/task.service';
import { Task } from '../../models/task.model';

@Component({
  standalone: false,
  selector: 'app-task-form',
  templateUrl: './task-form.component.html',
  styleUrls: ['./task-form.component.css']
})
export class TaskFormComponent {

  @Output() saved = new EventEmitter<void>();

  task: Task = {
    title: '',
    description: '',
    due_date: '',
    is_done: false   // ✔ correct field
  };

  constructor(private svc: TaskService) {}

  saveTask() {
    if (!this.task.title.trim()) {
      alert("Task title cannot be empty");
      return;
    }

    // ✔ changed done → is_done
    const newTask = {
      title: this.task.title,
      description: this.task.description,
      due_date: this.task.due_date,
      is_done: this.task.is_done
    };

    this.svc.addTask(newTask).subscribe(() => {
      this.saved.emit();

      // Reset form
      this.task = {
        title: '',
        description: '',
        due_date: '',
        is_done: false
      };
    });
  }
}
