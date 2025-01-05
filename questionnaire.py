import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

# File to store results
RESULTS_FILE = 'questionnaire_results.json'

# Function to save results
def save_results(data):
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as f:
            results = json.load(f)
    else:
        results = []

    results.append(data)

    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=4)

# GUI Questionnaire
def run_questionnaire():
    def submit():
        data = {
            'timestamp': datetime.now().isoformat(),
            'name': name_entry.get(),
            'age': age_entry.get(),
            'satisfaction': satisfaction_var.get(),
            'subscribe': subscribe_var.get()
        }
        save_results(data)
        messagebox.showinfo('Thank You', 'Your responses have been saved!')
        root.destroy()

    root = tk.Tk()
    root.title('Daily Questionnaire')
    root.geometry('400x300')

    tk.Label(root, text='Name:').pack()
    name_entry = tk.Entry(root)
    name_entry.pack()

    tk.Label(root, text='Age:').pack()
    age_entry = tk.Entry(root)
    age_entry.pack()

    tk.Label(root, text='How satisfied are you today?').pack()
    satisfaction_var = tk.StringVar(value='Neutral')
    tk.Radiobutton(root, text='Happy', variable=satisfaction_var, value='Happy').pack()
    tk.Radiobutton(root, text='Neutral', variable=satisfaction_var, value='Neutral').pack()
    tk.Radiobutton(root, text='Sad', variable=satisfaction_var, value='Sad').pack()

    subscribe_var = tk.BooleanVar()
    tk.Checkbutton(root, text='Subscribe to updates?', variable=subscribe_var).pack()

    submit_btn = tk.Button(root, text='Submit', command=submit)
    submit_btn.pack()

    root.mainloop()

if __name__ == '__main__':
    run_questionnaire()

