// task.c - Implementation for task management in C
#include "task.h"
#include <stdio.h>
#include <string.h>

// Load tasks from TSV file
size_t load_tasks(const char *filepath, Task *tasks, size_t capacity) {
    FILE *fp = fopen(filepath, "r");
    if (!fp) return 0;

    size_t count = 0;
    while (count < capacity) {
        Task t;
        if (fscanf(fp, "%d	%d	%255[^\n]", &t.id, &t.done, t.text) != 3)
            break;
        tasks[count++] = t;
        fgetc(fp); // consume newline
    }

    fclose(fp);
    return count;
}

// Save tasks to TSV file
int save_tasks(const char *filepath, Task *tasks, size_t count) {
    FILE *fp = fopen(filepath, "w");
    if (!fp) return 0;

    for (size_t i = 0; i < count; i++) {
        fprintf(fp, "%d	%d	%s\n", tasks[i].id, tasks[i].done, tasks[i].text);
    }

    fclose(fp);
    return 1;
}

// Compute next task ID
int get_next_id(Task *tasks, size_t count) {
    int max_id = 0;
    for (size_t i = 0; i < count; i++) {
        if (tasks[i].id > max_id) max_id = tasks[i].id;
    }
    return max_id + 1;
}

int mark_done_task(Task *tasks, size_t count, int task_id) {
    for (size_t i = 0; i < count; i++) {
        if (tasks[i].id == task_id) {
            tasks[i].done = 1;
            return 1;
        }
    }
    return 0;
}

size_t remove_task(Task *tasks, size_t count, int task_id) {
    size_t new_count = 0;
    for (size_t i = 0; i < count; i++) {
        if (tasks[i].id != task_id) {
            tasks[new_count++] = tasks[i];
        }
    }
    return new_count;
}
