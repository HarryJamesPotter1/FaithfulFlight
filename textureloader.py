import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import shutil
import time 

# Colors for Light and Dark themes
LIGHT_THEME = {
    "bg": "#FFFFFF",  # Light background
    "text": "#333333",  # Dark text
    "button": "#0096FF",  # Button color
    "accent": "#0096FF",  # Accent color
    "quit": "#FF0000",  # Quit button color
}

DARK_THEME = {
    "bg": "#333333",  
    "text": "#FFFFFF",  
    "button": "#0066CC",  
    "accent": "#0066CC",  
    "quit": "#FF3333",  
}

class TexturePackManager:
    TEXTURE_PACKS_DIR = "Packs"
    
    def __init__(self, root):
        self.root = root
        self.root.title("Texture Pack Manager")
        self.root.geometry("800x600")  # Initial size
        self.current_theme = LIGHT_THEME  # Start with light theme
        self.root.configure(bg=self.current_theme["bg"])

        self.create_widgets()

    def create_widgets(self):
        # Title label
        label = tk.Label(self.root, text="Welcome To Faithful Flight Texture Pack Organizer", 
                         bg=self.current_theme["bg"], fg=self.current_theme["text"])
        label.pack(pady=10)

        # Buttons with a light/dark theme color
        store_button = self.create_styled_button("Store a Texture Pack", self.store_texture_pack)
        use_button = self.create_styled_button("Use a Texture Pack", self.use_texture_pack)
        delete_button = self.create_styled_button("Delete a Texture Pack", self.delete_texture_pack)
        rename_button = self.create_styled_button("Rename a Texture Pack", self.rename_texture_pack)
        quit_button = self.create_styled_button("Quit", self.root.quit, bg_color=self.current_theme["quit"])

        # Theme toggle button
        theme_toggle_button = self.create_styled_button("Toggle Theme", self.toggle_theme)

        # Pack all buttons
        store_button.pack(pady=10)
        use_button.pack(pady=10)
        delete_button.pack(pady=10)
        rename_button.pack(pady=10)
        theme_toggle_button.pack(pady=10)
        quit_button.pack(pady=10)

        # Make the window resizable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def create_styled_button(self, text, command, bg_color=None):
        """Create a styled button with the current theme."""
        if bg_color is None:
            bg_color = self.current_theme["button"]
        return tk.Button(self.root, text=text, command=command, bg=bg_color, fg="white")

    def toggle_theme(self):
        """Toggles between light and dark themes."""
        if self.current_theme == LIGHT_THEME:
            self.current_theme = DARK_THEME
        else:
            self.current_theme = LIGHT_THEME

        # Update the main window and all widgets to match the new theme
        self.root.configure(bg=self.current_theme["bg"])

        # Re-create the buttons with updated theme
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.configure(bg=self.current_theme["button"], fg="white")

        # Update labels' colors
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=self.current_theme["bg"], fg=self.current_theme["text"])

    def browse_directory(self):
        """Open a file dialog to select a directory."""
        file_path = filedialog.askdirectory(initialdir='/', title='Select a directory')
        return file_path

    def create_texture_pack_folder(self, folder_name):
        """Create a folder for storing the texture pack."""
        pack_path = os.path.join(TexturePackManager.TEXTURE_PACKS_DIR, folder_name)
        if not os.path.exists(pack_path):
            os.makedirs(pack_path)
            return pack_path
        else:
            raise FileExistsError(f"Pack '{folder_name}' already exists. Choose a new name.")

    def store_texture_pack(self):
        """Store a new texture pack."""
        time.sleep(0.5)
        store_window = tk.Toplevel(self.root)
        store_window.title("Store a Texture Pack")
        store_window.geometry("300x150")
        store_window.configure(bg=self.current_theme["bg"])

        label = tk.Label(store_window, text="Enter the name of the pack:", bg=self.current_theme["bg"], fg=self.current_theme["text"])
        label.pack(pady=10)

        name_entry = tk.Entry(store_window)
        name_entry.pack()

        def store():
            name = name_entry.get()
            try:
                directory = self.browse_directory()
                if directory:
                    pack_path = self.create_texture_pack_folder(name)
                    if pack_path:
                        shutil.move(directory, pack_path)
                        store_window.destroy()
                        messagebox.showinfo("Success", f'Pack "{name}" saved.')
                else:
                    messagebox.showerror("Error", "Please select a directory.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        store_button = tk.Button(store_window, text="Store", command=store, bg=self.current_theme["button"], fg="white")
        store_button.pack(pady=10)

    def use_texture_pack(self):
        """Allow the user to select and use a texture pack."""
        saved_packs = os.listdir(TexturePackManager.TEXTURE_PACKS_DIR)

        if not saved_packs:
            messagebox.showinfo("Information", "No packs found in the texture pack directory.")
            return

        saved_packs.sort(key=lambda pack: os.path.getctime(os.path.join(TexturePackManager.TEXTURE_PACKS_DIR, pack)), reverse=True)
        time.sleep(0.5)
        use_window = tk.Toplevel(self.root)
        use_window.title("Use a Texture Pack")
        use_window.geometry("350x275")
        use_window.configure(bg=self.current_theme["bg"])

        label = tk.Label(use_window, text="Select a texture pack:", bg=self.current_theme["bg"], fg=self.current_theme["text"])
        label.pack(pady=10)

        listbox = tk.Listbox(use_window)
        for pack_name in saved_packs:
            listbox.insert(tk.END, pack_name)
        listbox.pack()

        def use():
            selected_index = listbox.curselection()
            if selected_index:
                selected_pack = saved_packs[int(selected_index[0])]
                with open("encrypt/workingdir.bin", "w") as f:
                    f.write(os.path.join("\\Packs", selected_pack))
                use_window.destroy()
                messagebox.showinfo("Success", f"Pack '{selected_pack}' selected.")

        use_button = tk.Button(use_window, text="Use", command=use, bg=self.current_theme["button"], fg="white")
        use_button.pack(pady=10)

    def delete_texture_pack(self):
        """Allow the user to delete a texture pack."""
        saved_packs = os.listdir(TexturePackManager.TEXTURE_PACKS_DIR)

        if not saved_packs:
            messagebox.showinfo("Information", "No packs found in the texture pack directory.")
            return

        saved_packs.sort(key=lambda pack: os.path.getctime(os.path.join(TexturePackManager.TEXTURE_PACKS_DIR, pack)), reverse=True)
        time.sleep(0.5)
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete a Texture Pack")
        delete_window.geometry("350x275")
        delete_window.configure(bg=self.current_theme["bg"])

        label = tk.Label(delete_window, text="Select a texture pack to delete:", bg=self.current_theme["bg"], fg=self.current_theme["text"])
        label.pack(pady=10)

        listbox = tk.Listbox(delete_window)
        for pack_name in saved_packs:
            listbox.insert(tk.END, pack_name)
        listbox.pack()

        def delete():
            selected_index = listbox.curselection()
            if selected_index:
                selected_pack = saved_packs[int(selected_index[0])]
                pack_path = os.path.join(TexturePackManager.TEXTURE_PACKS_DIR, selected_pack)

                confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{selected_pack}'? This action is irreversible.")
                if confirm:
                    try:
                        shutil.rmtree(pack_path)
                        delete_window.destroy()
                        messagebox.showinfo("Success", f"Pack '{selected_pack}' deleted.")
                    except Exception as e:
                        messagebox.showerror("Error", str(e))

        delete_button = tk.Button(delete_window, text="Delete", command=delete, bg=self.current_theme["button"], fg="white")
        delete_button.pack(pady=10)

    def rename_texture_pack(self):
        """Allow the user to rename a texture pack."""
        saved_packs = os.listdir(TexturePackManager.TEXTURE_PACKS_DIR)

        if not saved_packs:
            messagebox.showinfo("Information", "No packs found in the texture pack directory.")
            return

        saved_packs.sort(key=lambda pack: os.path.getctime(os.path.join(TexturePackManager.TEXTURE_PACKS_DIR, pack)), reverse=True)
        time.sleep(0.5)
        rename_window = tk.Toplevel(self.root)
        rename_window.title("Rename a Texture Pack")
        rename_window.geometry("350x250")
        rename_window.configure(bg=self.current_theme["bg"])

        label = tk.Label(rename_window, text="Select a texture pack to rename:", bg=self.current_theme["bg"], fg=self.current_theme["text"])
        label.pack(pady=10)

        listbox = tk.Listbox(rename_window)
        for pack_name in saved_packs:
            listbox.insert(tk.END, pack_name)
        listbox.pack()

        def rename():
            selected_index = listbox.curselection()
            if selected_index:
                selected_pack = saved_packs[int(selected_index[0])]
                new_name = simpledialog.askstring("Rename Pack", f"Enter a new name for Pack '{selected_pack}':")
                if new_name:
                    pack_path = os.path.join(TexturePackManager.TEXTURE_PACKS_DIR, selected_pack)
                    new_pack_path = os.path.join(TexturePackManager.TEXTURE_PACKS_DIR, new_name)
                    try:
                        os.rename(pack_path, new_pack_path)
                        rename_window.destroy()
                        messagebox.showinfo("Success", f"Pack '{selected_pack}' renamed to '{new_name}'.")
                    except Exception as e:
                        messagebox.showerror("Error", str(e))

        rename_button = tk.Button(rename_window, text="Rename", command=rename, bg=self.current_theme["button"], fg="white")
        rename_button.pack(pady=10)

def main():
    root = tk.Tk()
    app = TexturePackManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
