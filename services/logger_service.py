import queue
from datetime import datetime

log_queue = queue.Queue()
_step_counter = 0

def log_step(description, tool, status):
    global _step_counter
    _step_counter += 1

    log_queue.put({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "order": _step_counter,
        "description": description,
        "tool": tool,
        "status": status
    })
