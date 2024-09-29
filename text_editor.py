
import tkinter as tk
from tkinter import filedialog, messagebox, font
import os

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Text Editor with Formatting")
        self.root.geometry("600x400")
        
        self.text_area = tk.Text(self.root, undo=True, wrap="word")
        self.text_area.pack(fill=tk.BOTH, expand=1)
        self.default_font = font.Font(family="Helvetica", size=12)
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        self.edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=lambda: self.root.focus_get().event_generate("<<Cut>>"))
        self.edit_menu.add_command(label="Copy", command=lambda: self.root.focus_get().event_generate("<<Copy>>"))
        self.edit_menu.add_command(label="Paste", command=lambda: self.root.focus_get().event_generate("<<Paste>>"))
        self.toolbar = tk.Frame(self.root)
        self.toolbar.pack(fill=tk.X)
        self.bold_btn = tk.Button(self.toolbar, text="Bold", command=self.bold_text)
        self.bold_btn.pack(side=tk.LEFT, padx=5)
        self.italic_btn = tk.Button(self.toolbar, text="Italic", command=self.italic_text)
        self.italic_btn.pack(side=tk.LEFT, padx=5)
        self.underline_btn = tk.Button(self.toolbar, text="Underline", command=self.underline_text)
        self.underline_btn.pack(side=tk.LEFT, padx=5)
        self.status_bar = tk.Label(self.root, text="Words: 0", anchor='e')
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.text_area.tag_configure("bold", font=font.Font(self.text_area, self.default_font, weight="bold"))
        self.text_area.tag_configure("italic", font=font.Font(self.text_area, self.default_font, slant="italic"))
        self.text_area.tag_configure("underline", font=font.Font(self.text_area, self.default_font, underline=True))
        self.text_area.bind("<KeyRelease>", self.update_word_count)
        self.file_path = None

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.file_path = None
        self.root.title("New File - Basic Text Editor with Formatting")

    def open_file(self):
        self.file_path = filedialog.askopenfilename(defaultextension=".txt",
                                                    filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
        if self.file_path:
            with open(self.file_path, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, file.read())
            self.root.title(os.path.basename(self.file_path) + " - Basic Text Editor with Formatting")

    def save_file(self):
        if self.file_path:
            try:
                with open(self.file_path, "w") as file:
                    file.write(self.text_area.get(1.0, tk.END))
                messagebox.showinfo("Save", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving file: {str(e)}")
        else:
            self.save_as_file()

    def save_as_file(self):
        self.file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                      filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
        if self.file_path:
            self.save_file()

    def bold_text(self):
        self.toggle_tag("bold")

    def italic_text(self):
        self.toggle_tag("italic")

    def underline_text(self):
        self.toggle_tag("underline")

    def toggle_tag(self, tag):
        try:
            current_tags = self.text_area.tag_names("sel.first")
            if tag in current_tags:
                self.text_area.tag_remove(tag, "sel.first", "sel.last")
            else:
                self.text_area.tag_add(tag, "sel.first", "sel.last")
        except tk.TclError:
            messagebox.showwarning("Warning", "Please select text first to apply formatting.")

    def update_word_count(self, event=None):
        text = self.text_area.get(1.0, "end-1c")
        words = len(text.split())
        self.status_bar.config(text=f"Words: {words}")

if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()
