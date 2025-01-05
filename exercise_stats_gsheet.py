import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# File to store data
DATA_FILE = 'daily_tracker.json'

# Google Sheets setup
SHEET_NAME = 'Daily Tracker Sheet'
SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
CREDENTIALS_FILE = 'credentials.json'

# Default questions
QUESTIONS = [
    'Sit ups',
    'Push ups',
    'Curls',
    'Vertical press',
    'Bench press',

    'Steps walked',

    'Beers Drunk',
    'Hours Slept',
    'Cups of Coffee',
]

# Boolean questions
BOOLEAN_QUESTIONS = [
    'Breakfast?',
    'Lunch?',
    'Supper?'
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

# Save data to Google Sheets
def save_to_google_sheets(data):
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPES)
    client = gspread.authorize(creds)

    # sheet = client.open(SHEET_NAME).sheet1
    SPREADSHEET_ID = '1V2-KhGYl9B84UFNnBv3--Pf9P1lOOf_sPsgdinT2ic0'
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1


    today = datetime.now().strftime('%Y-%m-%d')
    existing_records = sheet.get_all_records()
    dates = [record.get('Date') for record in existing_records]

    row_data = [today] + [data.get(today, {}).get(q, '') for q in QUESTIONS + BOOLEAN_QUESTIONS]

    if today in dates:
        row_index = dates.index(today) + 2
        # sheet.update(f'A{row_index}', [row_data])
        sheet.update([row_data], f'A{row_index}')
    else:
        sheet.append_row(row_data)

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
        save_to_google_sheets(self.data)
        messagebox.showinfo('Saved', 'Your data has been saved successfully!')

# Run the Application
def main():
    root = tk.Tk()
    app = DailyTrackerApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()

