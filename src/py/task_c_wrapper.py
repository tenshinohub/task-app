"""
Python ctypes wrapper for task.c
This exposes:
- load_tasks
- save_tasks
- get_next_id

The C library must be compiled first:
Linux/Mac: gcc -shared -o libtask.so -fPIC task.c
Windows:   gcc -shared -o task.dll task.c
"""

import ctypes
from ctypes import c_int, c_char_p, c_size_t, Structure
from pathlib import Path

# ---------------------------
# Task struct (Python side)
# ---------------------------
class Task(Structure):
    _fields_ = [
        ("id", c_int),
        ("done", c_int),
        ("priority", c_int),
        ("text", ctypes.c_char * 256),
    ]

# ---------------------------
# Load C library
# ---------------------------
CURRENT_DIR = Path(__file__).resolve().parent.parent.parent  # プロジェクトルート
#LIB_PATH = None
LIB_PATH = CURRENT_DIR / "lib" / "libtask.so"  # Linux/Mac
if not LIB_PATH.exists():
    raise FileNotFoundError(f"C library not found at {LIB_PATH}")
#if Path("./libtask.so").exists():
#    LIB_PATH = Path("./libtask.so")
#elif Path("./task.dll").exists():
#    LIB_PATH = Path("./task.dll")
#else:
#    raise FileNotFoundError("C library not found. Compile task.c first.")

lib = ctypes.CDLL(str(LIB_PATH))

# ---------------------------
# C function prototypes
# ---------------------------
# load_tasks
lib.load_tasks.argtypes = (c_char_p, ctypes.POINTER(Task), c_size_t)
lib.load_tasks.restype = c_size_t

# save_tasks
lib.save_tasks.argtypes = (c_char_p, ctypes.POINTER(Task), c_size_t)
lib.save_tasks.restype = c_int

# get_next_id
lib.get_next_id.argtypes = (ctypes.POINTER(Task), c_size_t)
lib.get_next_id.restype = c_int

# mark_done_task
lib.mark_done_task.argtypes = (ctypes.POINTER(Task), c_size_t, c_int)
lib.mark_done_task.restype = c_int

# remove_task
lib.remove_task.argtypes = (ctypes.POINTER(Task), c_size_t, c_int)
lib.remove_task.restype = c_size_t

# ---------------------------
# Python wrapper functions
# ---------------------------
def load_tasks_py(filepath: str, capacity: int = 1024):
    arr = (Task * capacity)()
    count = lib.load_tasks(filepath.encode(), arr, capacity)
    return arr[:count], count

def save_tasks_py(filepath: str, tasks):
    arr = (Task * len(tasks))()
    for i, t in enumerate(tasks):
        arr[i].id = t.id
        arr[i].done = t.done
        arr[i].priority = 3 #default priority
        arr[i].text = t.text.encode() if isinstance(t.text, str) else t.text
    return lib.save_tasks(filepath.encode(), arr, len(tasks))

def get_next_id_py(tasks):
    arr = (Task * len(tasks))()
    for i, t in enumerate(tasks):
        arr[i] = t
    return lib.get_next_id(arr, len(tasks))
    
    
def mark_done_task_py(tasks, task_id: int):
    arr = (Task * len(tasks))()
    for i, t in enumerate(tasks):
        arr[i] = t
    return lib.mark_done_task(arr, len(tasks), task_id)


def remove_task_py(tasks, task_id: int):
    arr = (Task * len(tasks))()
    for i, t in enumerate(tasks):
        arr[i] = t
    return lib.remove_task(arr, len(tasks), task_id)

# Small test
"""
if __name__ == "__main__":
    tasks, count = load_tasks_py("data/tasks.db")
    print("Loaded:", count)
    print("Next ID:", get_next_id_py(tasks))
"""