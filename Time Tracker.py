import tkinter as tk
from tkinter import messagebox, simpledialog
import time
import csv
import os
from datetime import datetime

class StopwatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stopwatch")
        self.start_time = None
        self.end_time = None
        self.elapsed_time = 0
        self.running = False
        
        self.label = tk.Label(root, text="00:00:00", font=("Helvetica", 48))
        self.label.pack()
        
        self.start_button = tk.Button(root, text="Start", command=self.start, font=("Helvetica", 14))
        self.start_button.pack(side="left")
        
        self.stop_button = tk.Button(root, text="Stop", command=self.stop, font=("Helvetica", 14))
        self.stop_button.pack(side="left")
        
        # Automatically create CSV file
        self.create_csv_file()

        self.update_clock()

    def create_csv_file(self):
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.filename = os.path.join(downloads_path, f"timelog_{timestamp}.csv")
        
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Start Time", "End Time", "Elapsed Time (seconds)", "Note"])
        
        messagebox.showinfo("File Created", f"Log file created at {self.filename}")

    def start(self):
        if not self.running:
            self.start_time = time.time()
            self.running = True
            print(f"Stopwatch started at: {self.format_time(self.start_time)}")
            self.label.config(text="Running...")

    def stop(self):
        if self.running:
            self.end_time = time.time()
            self.elapsed_time = self.end_time - self.start_time
            self.running = False
            note = simpledialog.askstring("Input", "Please add a note for this time:")
            self.label.config(text=f"Elapsed Time: {self.elapsed_time:.2f} sec")
            print(f"Stopwatch stopped at: {self.format_time(self.end_time)}")
            print(f"Elapsed time: {self.elapsed_time:.2f} seconds")
            
            if note:
                self.save_entry(note)
                
            # Reset timer
            self.start_time = None
            self.elapsed_time = 0
            self.label.config(text="00:00:00")

    def save_entry(self, note):
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.format_time(self.start_time), self.format_time(self.end_time), self.elapsed_time, note])

    def format_time(self, timestamp):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

    def update_clock(self):
        if self.running:
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            self.label.config(text=time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
        self.root.after(1000, self.update_clock)

# Run the application
root = tk.Tk()
app = StopwatchApp(root)
root.mainloop()
