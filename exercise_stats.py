import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

# File to store data
DATA_FILE = 'daily_tracker.json'

# Default questions
QUESTIONS = [
    'Exercise Reps',
    'Steps Walked',
    'Lunch Calories',
    'Beers Drunk',
    'Glasses of Water',
    'Hours Slept',
    'Minutes Meditated',
    'Fruits Eaten',
    'Vegetables Eaten',
    'Cups of Coffee',
    'Snacks Eaten',
    'Screen Time (hrs)'
]

# Boolean questions
BOOLEAN_QUESTIONS = [
    'Did you exercise today?',
    'Did you meditate today?'
]

# Load existing data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save data to file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Main GUI Application
class DailyTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Tracker")

        self.data = load_data()
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.entries = {}
        self.boolean_vars = {}

        # Create labels and entry fields
        tk.Label(root, text=f"Daily Tracker ({self.today})", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        for idx, question in enumerate(QUESTIONS):
            tk.Label(root, text=question).grid(row=idx+1, column=0, sticky='w', padx=10, pady=2)
            entry = tk.Entry(root)
            entry.grid(row=idx+1, column=1, padx=10, pady=2)

            # Prefill entry if data exists
            if self.today in self.data and question in self.data[self.today]:
                entry.insert(0, self.data[self.today][question])

            self.entries[question] = entry

        # Add Boolean questions
        for idx, question in enumerate(BOOLEAN_QUESTIONS, start=len(QUESTIONS)+1):
            var = tk.BooleanVar(value=self.data.get(self.today, {}).get(question, False))
            chk = tk.Checkbutton(root, text=question, variable=var)
            chk.grid(row=idx+1, column=0, columnspan=2, sticky='w', padx=10, pady=2)
            self.boolean_vars[question] = var

        # Save button
        tk.Button(root, text='Save', command=self.save_entries).grid(row=len(QUESTIONS)+len(BOOLEAN_QUESTIONS)+1, column=0, columnspan=2, pady=10)

    def save_entries(self):
        if self.today not in self.data:
            self.data[self.today] = {}

        for question, entry in self.entries.items():
            value = entry.get()
            if value.isdigit():
                self.data[self.today][question] = int(value)
            else:
                self.data[self.today][question] = value

        for question, var in self.boolean_vars.items():
            self.data[self.today][question] = var.get()

        save_data(self.data)
        messagebox.showinfo('Saved', 'Your data has been saved successfully!')

# Run the Application
def main():
    root = tk.Tk()
    app = DailyTrackerApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()

