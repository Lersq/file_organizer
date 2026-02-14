import customtkinter as ctk
import os, shutil
from tkinter import filedialog

# Настройки темы
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("File Organizer")
        self.geometry("500x440")
        self.resizable(False, False)

        self.label = ctk.CTkLabel(self, text="Выберите папку для сортировки", font=("Arial", 16))
        self.label.pack(pady=20)

        self.select_button = ctk.CTkButton(self, text="Выбрать папку", command=self.select_folder)
        self.select_button.pack(pady=10)

        self.path_label = ctk.CTkLabel(self, text="Путь не выбран", text_color="gray")
        self.path_label.pack(pady=5)

        self.start_button = ctk.CTkButton(self, text="Начать сортировку", 
                                         command=self.organize_logic,
                                         state="disabled", fg_color="green", hover_color="darkgreen")
        self.start_button.pack(pady=20)

        self.log_box = ctk.CTkTextbox(self, width=400, height=150)
        self.log_box.pack(pady=10)
        self.log_box.tag_config("error", foreground="red")
        self.log_box.tag_config("success", foreground="green")
        self.log_box.tag_config("info", foreground="white")
        if os.path.isfile("./icon.ico"):
            self.iconbitmap("./icon.ico")
        else:
            self.log_box.insert("end", "Не удалось установить иконку для программы, будет использована стандартная", "error")
        self.log_box.configure(state="disabled")

        self.target_dir = ""

        self.open_btn = ctk.CTkButton(self, text="Открыть папку", 
                             command=self.open_folder,
                             fg_color="transparent", border_width=1, hover_color="#1A1A1A",
                             state="disabled")
        self.open_btn.pack(pady=5)

    def select_folder(self):
        self.target_dir = filedialog.askdirectory()
        if self.target_dir:
            self.start_button.configure(state="normal")
            self.open_btn.configure(state="normal")
            self.path_label.configure(text=self.target_dir)

    def organize_logic(self):
        if not self.target_dir:
            return

        formats = {
            "Images": [".jpg", ".png", ".jpeg", ".gif"],
            "Docs": [".pdf", ".docx", ".txt", ".xlsx"],
            "Archives": [".zip", ".rar", ".7z"]
        }

        for file in os.listdir(self.target_dir):
            try:
                if os.path.isfile(os.path.join(self.target_dir, file)):
                    if os.path.splitext(file)[1] in formats["Images"]:
                        os.makedirs(os.path.join(self.target_dir, "Images"), exist_ok=True)
                        shutil.move(os.path.join(self.target_dir, file), os.path.join(self.target_dir, "Images"))

                        self.log_box.configure(state="normal")
                        self.log_box.insert("end", f"Изображение '{file}' было перемещено в '{os.path.join(self.target_dir, "Image")}'\n\n", "info")
                        self.log_box.configure(state="disabled")
                    elif os.path.splitext(file)[1] in formats["Docs"]:
                        os.makedirs(os.path.join(self.target_dir, "Documents"), exist_ok=True)
                        shutil.move(os.path.join(self.target_dir, file), os.path.join(self.target_dir, "Documents"))
                        
                        self.log_box.configure(state="normal")
                        self.log_box.insert("end", f"Документ '{file}' был перемещен в '{os.path.join(self.target_dir, "Image")}'\n\n", "info")
                        self.log_box.configure(state="disabled")
                    elif os.path.splitext(file)[1] in formats["Archives"]:
                        os.makedirs(os.path.join(self.target_dir, "Archives"), exist_ok=True)
                        shutil.move(os.path.join(self.target_dir, file), os.path.join(self.target_dir, "Archives"))
                        
                        self.log_box.configure(state="normal")
                        self.log_box.insert("end", f"Архив '{file}' был перемещен в '{os.path.join(self.target_dir, "Image")}'\n\n", "info")
                        self.log_box.configure(state="disabled")
            except Exception as e:
                self.log_box.configure(state="normal")
                self.log_box.insert("end", f"Произошла ошибка: {e}\n\n", "error")
                self.log_box.configure(state="disabled")
                return

        self.log_box.configure(state="normal")        
        self.log_box.insert("end", "Готово!\n\n", "success")
        self.log_box.configure(state="disabled")

    def open_folder(self):
        if not self.target_dir:
            return
        
        path = os.path.realpath(self.target_dir)
    
        if os.name == 'nt':
            os.startfile(path)
        elif os.name == 'posix':
            import subprocess
            cmd = 'open' if os.uname().sysname == 'Darwin' else 'xdg-open'
            subprocess.call([cmd, path])

if __name__ == "__main__":
    app = App()
    app.mainloop()