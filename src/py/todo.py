#!/usr/bin/env python3
"""
CLI for Task Manager using C backend via ctypes.
"""

import sys
from pathlib import Path
import task_c_wrapper

data_file = Path(__file__).resolve().parent.parent.parent / "data" / "tasks.db"


def load_tasks():
    tasks, count = task_c_wrapper.load_tasks_py(str(data_file))
    return tasks, count

def save_tasks(tasks):
    task_c_wrapper.save_tasks_py(str(data_file), tasks)

def add_task(text):
    tasks, count = load_tasks()
    #from ctypes import Structure
    #from copy import deepcopy
    # create new task
    from task_c_wrapper import Task, get_next_id_py
    next_id = get_next_id_py(tasks)
    new_task = Task()
    new_task.id = next_id
    new_task.done = 0
    new_task.text = text.encode()
    # append
    all_tasks = list(tasks) + [new_task]
    save_tasks(all_tasks)
    print(f"Added task #{next_id}: {text}")


def list_tasks():
    tasks, count = load_tasks()
    if count == 0:
        print("No tasks.")
        return
    for t in tasks:
        status = "[x]" if t.done else "[ ]"
        print(f"{t.id:3d} {{{t.priority}}} {status} {t.text.decode()}")


def mark_done(task_id: int):    
    if task_c_wrapper.mark_done_task_py(tasks, task_id):
        save_tasks(tasks)
        print(f"Marked task #{task_id} as done.")
    else:
        print(f"Task #{task_id} not found.")


def remove_task(task_id: int):
    tasks, count = load_tasks()
    new_count = task_c_wrapper.remove_task_py(tasks, task_id)
    if new_count == count:
        print(f"Task #{task_id} not found.")
        return
    save_tasks(tasks[:new_count])
    print(f"Removed task #{task_id}.")
    
    
def edit_task(task_id: int, text):
    tasks, count = load_tasks()
    success, new_arr = task_c_wrapper.edit_task_py(tasks, task_id, text)
    if not success:
        print("Task not found.")
        exit(1)
    save_tasks(new_arr)
    print("Task updated.")
    exit(0)


def print_usage():
    print("Usage:")
    print("  todo.py add <text>")
    print("  todo.py list")
    print("  todo.py done <id>")
    print("  todo.py remove <id>")
    print("  todo.py edit <id> <text>")


def main():
    if len(sys.argv) < 2:
        print_usage()
        return
    cmd = sys.argv[1]

    if cmd == "add" and len(sys.argv) >= 3:
        add_task(" ".join(sys.argv[2:]))
    elif cmd == "list":
        list_tasks()
    elif cmd == "done" and len(sys.argv) == 3:
        mark_done(int(sys.argv[2]))
    elif cmd == "remove" and len(sys.argv) == 3:
        remove_task(int(sys.argv[2]))
    elif cmd == "edit" and len(sys.argv) >= 3:
        edit_task(int(sys.argv[2]), " ".join(sys.argv[3:]))
    else:
        print_usage()


if __name__ == "__main__":
    main()
