import tkinter as tk
from tkinter import simpledialog, colorchooser, filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk

class SpriteMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("Sprite Maker")
        self.root.geometry("800x600")
        self.grid_size = 16
        self.pixel_size = 20
        self.current_color = "#000000"
        self.selected_cells = set()
        self.transparent_background = True
        self.is_select_mode = False
        self.history = []
        self.redo_stack = []
        self.init_ui()

    def init_ui(self):
        # Frame for all controls
        top_frame = ttk.Frame(self.root, padding="20")
        top_frame.pack(pady=10, fill="x")

        # Title Label
        self.title_label = ttk.Label(top_frame, text="Sprite Maker", font=("Helvetica", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=10, pady=10)

        # Project buttons
        self.new_button = self.create_button(top_frame, "New Project", self.new_project, 1, 0)
        self.open_button = self.create_button(top_frame, "Open Image", self.open_image, 1, 1)
        self.save_button = self.create_button(top_frame, "Save Sprite", self.save_sprite, 1, 2)

        # Color pick and eraser buttons
        self.color_button = self.create_button(top_frame, "Pick Color", self.pick_color, 1, 3)
        self.eraser_button = self.create_button(top_frame, "Eraser", self.set_eraser, 1, 4)

        # Apply color and undo / redo
        self.apply_color_button = self.create_button(top_frame, "Apply Color", self.apply_color_to_selection, 2, 0)
        self.undo_button = self.create_button(top_frame, "Undo", self.undo, 2, 1)
        self.redo_button = self.create_button(top_frame, "Redo", self.redo, 2, 2)

        # Zoom buttons
        self.zoom_in_button = self.create_button(top_frame, "Zoom In", self.zoom_in, 2, 3)
        self.zoom_out_button = self.create_button(top_frame, "Zoom Out", self.zoom_out, 2, 4)

        # Select Mode button
        self.select_button = ttk.Button(top_frame, text="Select Mode", command=self.toggle_select_mode, width=15)
        self.select_button.grid(row=3, column=0, padx=10, pady=5)

        # Transparent background toggle
        self.transparent_var = tk.BooleanVar(value=True)
        self.transparent_button = ttk.Checkbutton(top_frame, text="Transparent BG", variable=self.transparent_var, command=self.toggle_transparency)
        self.transparent_button.grid(row=3, column=1, padx=10, pady=5)

        # Color A to B replace feature
        self.change_color_button = self.create_button2(top_frame, "Change Color A to B", self.change_color_a_to_b, 3, 2)

        # Canvas for sprite grid
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(pady=20, fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.paint_pixel)
        self.canvas.bind("<B1-Motion>", self.paint_pixel)

        # Label to show current selected color
        self.color_label = ttk.Label(top_frame, text=f"Current Color: {self.current_color}")
        self.color_label.grid(row=3, column=3, padx=10, pady=5)

        # Initialize a blank project
        self.new_project()

    def create_button2(self, parent, text, command, row, col):
        return ttk.Button(parent, text=text, command=command, width=20).grid(row=row, column=col, padx=10, pady=5)

    def create_button(self, parent, text, command, row, col):
        return ttk.Button(parent, text=text, command=command, width=15).grid(row=row, column=col, padx=10, pady=5)

    def new_project(self):
        size = simpledialog.askinteger("New Project", "Enter grid size (e.g., 16 for 16x16):", initialvalue=16, minvalue=1, maxvalue=64)
        if size is not None:
            self.grid_size = size

        self.canvas.delete("all")
        self.selected_cells.clear()
        self.pixel_size = 20
        self.grid = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # Draw grid
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x1 = col * self.pixel_size
                y1 = row * self.pixel_size
                x2 = x1 + self.pixel_size
                y2 = y1 + self.pixel_size
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="gray")
                self.grid[row][col] = rect

        self.update_canvas_size()
        self.history.clear()
        self.redo_stack.clear()

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if not file_path:
            return

        try:
            img = Image.open(file_path).convert("RGBA")
            img = img.resize((self.grid_size, self.grid_size), Image.Resampling.NEAREST)
            pixels = img.load()

            self.new_project()
            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    r, g, b, a = pixels[col, row]
                    color = self.rgb_to_hex((r, g, b)) if a > 0 else "white"
                    rect = self.grid[row][col]
                    self.canvas.itemconfig(rect, fill=color)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image: {e}")

    def pick_color(self):
        color_code = colorchooser.askcolor(title="Choose a color")[1]
        if color_code:
            self.current_color = color_code
            self.color_label.config(text=f"Current Color: {self.current_color}")

    def set_eraser(self):
        self.current_color = "white"
        self.color_label.config(text=f"Current Color: Eraser")

    def toggle_transparency(self):
        self.transparent_background = not self.transparent_background

    def zoom_in(self):
        self.pixel_size = min(self.pixel_size + 5, 100)  # Limit max zoom level
        self.redraw_grid()

    def zoom_out(self):
        self.pixel_size = max(self.pixel_size - 5, 5)  # Limit min zoom level
        self.redraw_grid()

    def redraw_grid(self):
        current_colors = {}
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                rect = self.grid[row][col]
                current_colors[(row, col)] = self.canvas.itemcget(rect, "fill")
        
        self.canvas.config(width=self.grid_size * self.pixel_size, height=self.grid_size * self.pixel_size)

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x1 = col * self.pixel_size
                y1 = row * self.pixel_size
                x2 = x1 + self.pixel_size
                y2 = y1 + self.pixel_size

                rect = self.grid[row][col]
                self.canvas.coords(rect, x1, y1, x2, y2)
                self.canvas.itemconfig(rect, fill=current_colors[(row, col)], outline="gray")

        self.update_canvas_size()

        # Reapply the selected cells
        for rect in self.selected_cells:
            self.canvas.itemconfig(rect, outline="red", width=3)

    def update_canvas_size(self):
        self.canvas.config(width=self.grid_size * self.pixel_size, height=self.grid_size * self.pixel_size)

    def toggle_select_mode(self):
        if self.is_select_mode:
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.bind("<Button-1>", self.paint_pixel)
            self.is_select_mode = False
            self.clear_selection()
            self.select_button.config(text="Select Mode")
        else:
            self.canvas.unbind("<Button-1>")
            self.canvas.bind("<Button-1>", self.select_cell)
            self.canvas.bind("<B1-Motion>", self.select_cell)
            self.is_select_mode = True
            self.select_button.config(text="Exit Select Mode")

    def select_cell(self, event):
        col, row = event.x // self.pixel_size, event.y // self.pixel_size
        if 0 <= col < self.grid_size and 0 <= row < self.grid_size:
            rect = self.grid[row][col]
            if rect not in self.selected_cells:
                self.selected_cells.add(rect)
                self.canvas.itemconfig(rect, outline="red", width=3)

    def clear_selection(self):
        for rect in self.selected_cells:
            self.canvas.itemconfig(rect, outline="gray", width=1)
        self.selected_cells.clear()

    def apply_color_to_selection(self):
        for rect in self.selected_cells:
            self.canvas.itemconfig(rect, fill=self.current_color)
        self.history.append(("color", list(self.selected_cells), self.current_color))
        self.selected_cells.clear()

    def paint_pixel(self, event):
        col, row = event.x // self.pixel_size, event.y // self.pixel_size
        if 0 <= col < self.grid_size and 0 <= row < self.grid_size:
            rect = self.grid[row][col]
            self.canvaxds.itemconfig(rect, fill=self.current_color)
            self.history.append(("color", [rect], self.current_color))

    def undo(self):
        if not self.history:
            return

        action = self.history.pop()
        if action[0] == "color":
            for rect in action[1]:
                self.canvas.itemconfig(rect, fill="white")

        self.redo_stack.append(action)

    def redo(self):
        if not self.redo_stack:
            return

        action = self.redo_stack.pop()
        if action[0] == "color":
            for rect in action[1]:
                self.canvas.itemconfig(rect, fill=action[2])

        self.history.append(action)

    def save_sprite(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if not file_path:
            return

        if self.transparent_background:
            image = Image.new("RGBA", (self.grid_size, self.grid_size), (0, 0, 0, 0))
        else:
            image = Image.new("RGBA", (self.grid_size, self.grid_size), (255, 255, 255, 255))

        pixels = image.load()

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                rect = self.grid[row][col]
                color = self.canvas.itemcget(rect, "fill")
                if color == "white" and self.transparent_background:
                    pixels[col, row] = (0, 0, 0, 0)
                else:
                    color_tuple = self.hex_to_rgb(color)
                    pixels[col, row] = (*color_tuple, 255)

        image.save(file_path)

    def hex_to_rgb(self, hex_color):
        if hex_color.startswith("#"):
            hex_color = hex_color.lstrip("#")
            if len(hex_color) == 6:
                try:
                    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                except ValueError:
                    return (255, 255, 255)
        return (255, 255, 255)

    def rgb_to_hex(self, rgb):
        return "#{:02x}{:02x}{:02x}".format(*rgb)

    def change_color_a_to_b(self):
        color_a = colorchooser.askcolor(title="Select Color A")[1]
        color_b = colorchooser.askcolor(title="Select Color B")[1]

        if color_a and color_b:
            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    rect = self.grid[row][col]
                    current_color = self.canvas.itemcget(rect, "fill")
                    if current_color == color_a:
                        self.canvas.itemconfig(rect, fill=color_b)


if __name__ == "__main__":
    root = tk.Tk()
    app = SpriteMaker(root)
    root.mainloop()
