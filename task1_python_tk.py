import tkinter as tk
from tkinter import messagebox


def on_submit():
    name = name_entry.get().strip()
    group = group_entry.get().strip()
    if not name or not group:
        messagebox.showwarning("Empty field", "Please fill in both name and group.")
        return
    lang = lang_var.get()
    result_label.config(text=f"Hello, {name} from {group}!\nFavourite language: {lang}")


def on_clear():
    name_entry.delete(0, tk.END)
    group_entry.delete(0, tk.END)
    result_label.config(text="")
    name_entry.focus()


root = tk.Tk()
root.title("Tkinter demo — Dzhanteliev Adilkhan EEAIR24")
root.geometry("380x320")
root.resizable(False, False)

tk.Label(root, text="Student form", font=("Arial", 16, "bold")).grid(
    row=0, column=0, columnspan=2, pady=12
)

tk.Label(root, text="Name:").grid(row=1, column=0, sticky="e", padx=8, pady=4)
name_entry = tk.Entry(root, width=25)
name_entry.grid(row=1, column=1, pady=4)
tk.Label(root, text="Group:").grid(row=2, column=0, sticky="e", padx=8, pady=4)
group_entry = tk.Entry(root, width=25)
group_entry.grid(row=2, column=1, pady=4)
lang_var = tk.StringVar(value="Python")
radio_frame = tk.Frame(root)
radio_frame.grid(row=3, column=0, columnspan=2, pady=6)
for lang in ("Python", "Java", "JavaScript"):
    tk.Radiobutton(radio_frame, text=lang, variable=lang_var, value=lang).pack(side="left")

btn_frame = tk.Frame(root)
btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
tk.Button(btn_frame, text="Submit", width=10, command=on_submit).pack(side="left", padx=5)
tk.Button(btn_frame, text="Clear", width=10, command=on_clear).pack(side="left", padx=5)

result_label = tk.Label(root, text="", fg="blue", font=("Arial", 12))
result_label.grid(row=5, column=0, columnspan=2, pady=10)

root.bind("<Return>", lambda e: on_submit())
name_entry.focus()

root.mainloop()
