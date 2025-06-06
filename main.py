import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
from tkinterdnd2 import DND_FILES, TkinterDnD

# --- IMPOSTAZIONI PRINCIPALI ---
APP_NAME = "GoPro Proxy Tool"
APP_VERSION = "1.0"
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 550

# --- CLASSE PRINCIPALE DELL'APPLICAZIONE (che gestisce la logica DND) ---
class AppDND(TkinterDnD.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Nasconde la finestra principale di TkinterDnD, useremo quella di CustomTkinter
        self.withdraw() 
        # Imposta le impostazioni globali di CustomTkinter
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        # Crea e mostra la finestra principale dell'applicazione
        self.app_window = AppWindow(self)
        self.app_window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.app_window.destroy()
        self.destroy()

# --- CLASSE DELLA FINESTRA PRINCIPALE (che gestisce la UI) ---
class AppWindow(ctk.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)
        
        # Imposta l'icona (assicurati di avere 'icon.ico' nella cartella 'assets')
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

        # 2. Frame per la lista dei file (con supporto Drag & Drop)
        self.dnd_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.dnd_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.dnd_frame.grid_rowconfigure(1, weight=1)
        self.dnd_frame.grid_columnconfigure(0, weight=1)
        
        # Registra il frame per accettare il drop di file
        self.dnd_frame.drop_target_register(DND_FILES)
        self.dnd_frame.dnd_bind('<<Drop>>', self.on_drop)

        # Textbox per visualizzare i file
        self.file_textbox = ctk.CTkTextbox(self.dnd_frame, state="disabled", font=ctk.CTkFont(size=12))
        self.file_textbox.grid(row=1, column=0, sticky="nsew")
        
        self.dnd_label = ctk.CTkLabel(self.dnd_frame, text="Drag and drop your .LRV files here or use the ‘Browse’ button", 
                                      font=ctk.CTkFont(size=16, slant="italic"), text_color="gray50")
        self.dnd_label.place(relx=0.5, rely=0.5, anchor="center")

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
        """Aggiorna la textbox con la lista dei file."""
        self.dnd_label.place_forget() # Nasconde il testo "Trascina qui..."
        self.file_textbox.configure(state="normal")
        self.file_textbox.delete("1.0", "end")
        if self.file_list:
            display_text = "\n".join(os.path.basename(f) for f in self.file_list)
            self.file_textbox.insert("1.0", f"{len(self.file_list)} file aggiunti:\n\n{display_text}")
            self.process_button.configure(state="normal")
        else:
            self.dnd_label.place(relx=0.5, rely=0.5, anchor="center") # Mostra di nuovo il testo
            self.process_button.configure(state="disabled")
            self.status_label.configure(text="Ready.")
        self.file_textbox.configure(state="disabled")

    def add_files(self, files):
        """Aggiunge file alla lista, evitando duplicati e file non .LRV."""
        added_count = 0
        for f in files:
            if f.lower().endswith(".lrv") and f not in self.file_list:
                self.file_list.append(f)
                added_count += 1
        if added_count > 0:
            self.update_file_display()

    def on_drop(self, event):
        """Gestisce l'evento di trascinamento dei file."""
        # event.data è una stringa con i percorsi dei file separati da spazi e racchiusi da {}
        # Esempio: '{C:/Users/User/Desktop/GL010001.LRV} {C:/Users/User/Desktop/GL010002.LRV}'
        files_str = self.tk.splitlist(event.data)
        self.add_files(files_str)

    def browse_files(self):
        """Apre la finestra di dialogo per selezionare i file."""
        files = filedialog.askopenfilenames(
            title="Seleziona i file GoPro .LRV",
            filetypes=[("File LRV", "*.lrv"), ("Tutti i file", "*.*")]
        )
        if files:
            self.add_files(files)

    def clear_list(self):
        """Pulisce la lista dei file."""
        self.file_list.clear()
        self.update_file_display()

    def process_files(self):
        """Funzione principale per rinominare e spostare i file."""
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

                # Verifica che il file sia un file LRV GoPro valido (GLxxxxxx.LRV)
                if filename.upper().startswith("GL") and filename.upper().endswith(".LRV"):
                    # Crea il nuovo nome del file
                    new_filename = "GX" + filename[2:-4] + ".MP4"
                    
                    # Crea la cartella 'proxy' se non esiste
                    proxy_dir = os.path.join(directory, "proxy")
                    os.makedirs(proxy_dir, exist_ok=True)
                    
                    # Definisci il percorso di destinazione
                    destination_path = os.path.join(proxy_dir, new_filename)
                    
                    # Sposta e rinomina il file
                    shutil.move(file_path, destination_path)
                    
                    self.status_label.configure(text=f"Processed: {filename} -> {new_filename}")
                    self.update() # Forza l'aggiornamento della UI
                    processed_count += 1
                else:
                    error_count += 1
            except Exception as e:
                error_count += 1
                print(f"Error processing {file_path}: {e}")

        # Messaggio finale
        result_message = f"Processing complete!\n\nFiles processed successfully: {processed_count}\nFiles ignored or with errors: {error_count}"
        messagebox.showinfo("Success", result_message)

        # Ripristina l'interfaccia
        self.clear_list()
        self.browse_button.configure(state="normal")
        self.clear_button.configure(state="normal")

if __name__ == "__main__":
    app = AppDND()
    app.mainloop()
