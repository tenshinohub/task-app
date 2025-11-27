// task.h - C core for task management
#ifndef TASK_H
#define TASK_H

#include <stddef.h>

// Task structure
typedef struct {
    int id;
    int done;      // 0 = not done, 1 = done
    int priority;
    char text[256];
} Task;

// Load tasks from file. Returns number of tasks loaded.
// tasks: array to store loaded tasks (capacity given)
size_t load_tasks(const char *filepath, Task *tasks, size_t capacity);

// Save tasks to file.
// count: number of tasks in array
int save_tasks(const char *filepath, Task *tasks, size_t count);

// Compute next task ID from existing tasks.
int get_next_id(Task *tasks, size_t count);

int mark_done_task(Task *tasks, size_t count, int task_id);

size_t remove_task(Task *tasks, size_t count, int task_id);

#endif
