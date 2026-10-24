import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil

# --- IMPOSTAZIONI PRINCIPALI ---
APP_NAME = "GoPro Proxy Tool"
APP_VERSION = "1.0"
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 550

# --- CLASSE DELLA FINESTRA PRINCIPALE ---
class AppWindow(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)

        if os.path.exists("assets/icon.ico"):
            self.iconbitmap("assets/icon.ico")

        self.file_list = []

        # Configurazione del layout a griglia
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- WIDGETS DELL'INTERFACCIA ---

        # 1. Titolo
        self.title_label = ctk.CTkLabel(self, text=APP_NAME, font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        # 2. Frame per la lista dei file
        self.file_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.file_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.file_frame.grid_rowconfigure(1, weight=1)
        self.file_frame.grid_columnconfigure(0, weight=1)

        # Textbox per visualizzare i file
        self.file_textbox = ctk.CTkTextbox(self.file_frame, state="disabled", font=ctk.CTkFont(size=12))
        self.file_textbox.grid(row=1, column=0, sticky="nsew")

        self.placeholder_label = ctk.CTkLabel(self.file_frame, text="Use the 'Browse' button to select .LRV files",
                                              font=ctk.CTkFont(size=16, slant="italic"), text_color="gray50")
        self.placeholder_label.place(relx=0.5, rely=0.5, anchor="center")

        # 3. Frame per i pulsanti
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.browse_button = ctk.CTkButton(self.button_frame, text="Browse .LRV Files", command=self.browse_files)
        self.browse_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.clear_button = ctk.CTkButton(self.button_frame, text="Clear List", command=self.clear_list, fg_color="#D32F2F", hover_color="#B71C1C")
        self.clear_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.process_button = ctk.CTkButton(self.button_frame, text="Process Files", command=self.process_files, state="disabled")
        self.process_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # 4. Barra di stato
        self.status_label = ctk.CTkLabel(self, text="Ready.", anchor="w")
        self.status_label.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")

    # --- FUNZIONI LOGICHE ---

    def update_file_display(self):
        self.placeholder_label.place_forget()
        self.file_textbox.configure(state="normal")
        self.file_textbox.delete("1.0", "end")
        if self.file_list:
            display_text = "\n".join(os.path.basename(f) for f in self.file_list)
            self.file_textbox.insert("1.0", f"{len(self.file_list)} file aggiunti:\n\n{display_text}")
            self.process_button.configure(state="normal")
        else:
            self.placeholder_label.place(relx=0.5, rely=0.5, anchor="center")
            self.process_button.configure(state="disabled")
            self.status_label.configure(text="Ready.")
        self.file_textbox.configure(state="disabled")

    def add_files(self, files):
        added_count = 0
        for f in files:
            if f.lower().endswith(".lrv") and f not in self.file_list:
                self.file_list.append(f)
                added_count += 1
        if added_count > 0:
            self.update_file_display()

    def browse_files(self):
        files = filedialog.askopenfilenames(
            title="Seleziona i file GoPro .LRV",
            filetypes=[("File LRV", "*.lrv"), ("Tutti i file", "*.*")]
        )
        if files:
            self.add_files(files)

    def clear_list(self):
        self.file_list.clear()
        self.update_file_display()

    def process_files(self):
        if not self.file_list:
            messagebox.showwarning("Nessun File", "Nessun file nella lista da processare.")
            return

        processed_count = 0
        error_count = 0

        self.process_button.configure(state="disabled")
        self.browse_button.configure(state="disabled")
        self.clear_button.configure(state="disabled")

        for file_path in self.file_list:
            try:
                directory = os.path.dirname(file_path)
                filename = os.path.basename(file_path)

                if filename.upper().startswith("GL") and filename.upper().endswith(".LRV"):
                    new_filename = "GX" + filename[2:-4] + ".MP4"

                    proxy_dir = os.path.join(directory, "proxy")
                    os.makedirs(proxy_dir, exist_ok=True)

                    destination_path = os.path.join(proxy_dir, new_filename)

                    shutil.move(file_path, destination_path)

                    self.status_label.configure(text=f"Processed: {filename} -> {new_filename}")
                    self.update()
                    processed_count += 1
                else:
                    error_count += 1
            except Exception as e:
                error_count += 1
                print(f"Error processing {file_path}: {e}")

        result_message = f"Processing complete!\n\nFiles processed successfully: {processed_count}\nFiles ignored or with errors: {error_count}"
        messagebox.showinfo("Success", result_message)

        self.clear_list()
        self.browse_button.configure(state="normal")
        self.clear_button.configure(state="normal")

if __name__ == "__main__":
    app = AppWindow()
    app.mainloop()
