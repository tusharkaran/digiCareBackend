import tkinter as tk
from tkinter import messagebox
import random
import requests
import json
from datetime import datetime

class HealthRecorder:
    def __init__(self, master):
        self.master = master
        self.master.title("Health Parameters Recorder")

        # Labels for entry fields
        self.label_un = tk.Label(master, text="Username:")
        self.label_un.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.label_bp = tk.Label(master, text="Blood Pressure (mmHg):")
        self.label_bp.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.label_bo = tk.Label(master, text="Blood Oxygen (%):")
        self.label_bo.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.label_temp = tk.Label(master, text="Temperature (°C):")
        self.label_temp.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.label_hr = tk.Label(master, text="Heart Rate (bpm):")
        self.label_hr.grid(row=4, column=0, padx=10, pady=5, sticky="e")

        # Entry fields
        self.entry_un = tk.Entry(master, width=10)
        self.entry_un.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.entry_bp = tk.Entry(master, state='readonly', width=10)
        self.entry_bp.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.entry_bo = tk.Entry(master, state='readonly', width=10)
        self.entry_bo.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.entry_temp = tk.Entry(master, state='readonly', width=10)
        self.entry_temp.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.entry_hr = tk.Entry(master, state='readonly', width=10)
        self.entry_hr.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Record button
        self.record_button = tk.Button(master, text="Record", command=self.record_parameters)
        self.record_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def record_parameters(self):
        # Disable record button during loading
        self.record_button.config(state='disabled')

        # Simulate loading delay
        self.master.after(2000, self.send_recorded_parameters)

    def send_recorded_parameters(self):
        username = self.entry_un.get()
        systolic_pressure = random.randint(70, 110)
        diastolic_pressure = random.randint(110, 150)
        blood_oxygen = random.randint(85, 100)
        temperature = round(random.uniform(36.0, 38.0), 1)
        heart_rate = random.randint(50, 100)

        bp_string = f"{systolic_pressure} / {diastolic_pressure}"

        self.entry_un.config(state='normal')
        self.entry_bp.config(state='normal')
        self.entry_bo.config(state='normal')
        self.entry_temp.config(state='normal')
        self.entry_hr.config(state='normal')

        self.entry_un.delete(0, tk.END)
        self.entry_bp.delete(0, tk.END)
        self.entry_bo.delete(0, tk.END)
        self.entry_temp.delete(0, tk.END)
        self.entry_hr.delete(0, tk.END)

        self.entry_un.insert(0, username)
        self.entry_bp.insert(0, bp_string)
        self.entry_bo.insert(0, str(blood_oxygen))
        self.entry_temp.insert(0, str(temperature))
        self.entry_hr.insert(0, str(heart_rate))

        self.entry_un.config(state='normal')
        self.entry_bp.config(state='readonly')
        self.entry_bo.config(state='readonly')
        self.entry_temp.config(state='readonly')
        self.entry_hr.config(state='readonly')

        # Enable record button after displaying parameters
        self.record_button.config(state='normal')

        # Show user feedback message
        # messagebox.showinfo("Recorded", "Parameters recorded successfully.")

        # Prepare data to send to API
        data = {
            'patient_username': username,
            'timestamp': datetime.now().isoformat(),
            'blood_pressure': bp_string,
            'heart_rate': str(heart_rate),
            'o2': str(blood_oxygen),
            'temperature': str(temperature)
        }


        # Send data to API
        api_url = 'http://127.0.0.1:5000/api/record-data/' + username  # Replace with your API endpoint URL
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(api_url, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # Raise an error for bad response status
            messagebox.showinfo("Recorded", "Parameters recorded successfully.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to record parameters api: {e}")

        # Enable record button after sending parameters
        self.record_button.config(state='normal')

def main():
    root = tk.Tk()
    app = HealthRecorder(root)
    root.mainloop()

if __name__ == "__main__":
    main()


