import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess
import time

class AntiRKNGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AntiRKN")
        self.root.geometry("400x250")
        self.root.configure(bg="#1c2526")

        # Variables
        self.status_var = tk.StringVar(value="Не работает")
        self.strategy_var = tk.StringVar(value="Выберите стратегию")
        self.selected_file = None
        self.bat_folder = "BAT"
        self.winws_running = False

        # Styling
        self.style = ttk.Style()
        self.style.configure("TButton", background="#e74c3c", foreground="white", font=("Arial", 10, "bold"))
        self.style.configure("TLabel", background="#1c2526", foreground="#3498db", font=("Arial", 10))
        self.style.configure("TCombobox", fieldbackground="#2c3e50", foreground="white")

        # GUI Elements
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Label(self.root, text="AntiRKN", font=("Arial", 16, "bold"), fg="#3498db", bg="#1c2526")
        header.pack(pady=10)

        # Status Frame
        status_frame = ttk.Frame(self.root)
        status_frame.pack(pady=5, padx=10, fill=tk.X)
        ttk.Label(status_frame, text="Статус:").pack(side=tk.LEFT)
        ttk.Label(status_frame, textvariable=self.status_var).pack(side=tk.LEFT, padx=5)

        # Strategy Frame
        strategy_frame = ttk.Frame(self.root)
        strategy_frame.pack(pady=5, padx=10, fill=tk.X)
        ttk.Label(strategy_frame, text="Стратегия:").pack(side=tk.LEFT)
        self.strategy_menu = ttk.Combobox(strategy_frame, textvariable=self.strategy_var, state="readonly", width=25)
        self.strategy_menu.pack(side=tk.LEFT, padx=5)
        self.update_strategy_list()

        # Control Buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=15, padx=10)
        start_button = ttk.Button(button_frame, text="Старт", command=self.start_service)
        start_button.pack(side=tk.LEFT, padx=5)
        stop_button = ttk.Button(button_frame, text="Стоп", command=self.stop_service)
        stop_button.pack(side=tk.LEFT, padx=5)

        # Auto Update
        self.root.after(1000, self.check_status)

    def update_strategy_list(self):
        if os.path.exists(self.bat_folder):
            strategies = [f.replace(".bat", "") for f in os.listdir(self.bat_folder) if f.endswith(".bat")]
            self.strategy_menu['values'] = strategies
            if strategies and self.strategy_var.get() == "Выберите стратегию":
                self.strategy_var.set(strategies[0])

    def start_service(self):
        selected_strategy = self.strategy_var.get()
        if selected_strategy and selected_strategy != "Выберите стратегию":
            self.selected_file = os.path.join(self.bat_folder, f"{selected_strategy}.bat")
            if os.path.exists(self.selected_file):
                try:
                    process = subprocess.Popen(["winws.exe", self.selected_file], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    time.sleep(2)  # Ждем запуска
                    if process.poll() is None:
                        self.winws_running = True
                        self.status_var.set("Работает")
                    else:
                        messagebox.showerror("Ошибка", "winws.exe не запустился!")
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")
            else:
                messagebox.showerror("Ошибка", "Файл не найден!")
        else:
            messagebox.showerror("Ошибка", "Выберите стратегию!")

    def stop_service(self):
        if self.winws_running:
            try:
                subprocess.call(["taskkill", "/IM", "winws.exe", "/F"], shell=True)
                time.sleep(1)  # Ждем завершения
                self.winws_running = False
                self.status_var.set("Не работает")
                self.strategy_var.set("Выберите стратегию")
                self.selected_file = None
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")
        else:
            messagebox.showerror("Ошибка", "Процесс не активен!")

    def check_status(self):
        if self.selected_file and os.path.exists(self.selected_file):
            result = subprocess.run(["tasklist"], capture_output=True, text=True)
            self.winws_running = "winws.exe" in result.stdout
            self.status_var.set("Работает" if self.winws_running else "Не работает")
        self.root.after(1000, self.check_status)

if __name__ == "__main__":
    root = tk.Tk()
    app = AntiRKNGUI(root)
    root.mainloop()
