import tkinter as tk
from tkinter import ttk
from services.logger_service import log_queue

def start_dashboard():
    root = tk.Tk()
    root.title("Live Execution Logs")

    tree = ttk.Treeview(
        root,
        columns=("Time", "Order", "Step", "Tool", "Status"),
        show="headings"
    )

    for col in ("Time", "Order", "Step", "Tool", "Status"):
        tree.heading(col, text=col)
        tree.column(col, width=150)

    tree.pack(fill="both", expand=True)

    def poll_logs():
        while not log_queue.empty():
            log = log_queue.get()
            tree.insert("", "end", values=(
                log["timestamp"],
                log["order"],
                log["description"],
                log["tool"],
                log["status"]
            ))
        root.after(200, poll_logs)

    poll_logs()
    root.mainloop()
