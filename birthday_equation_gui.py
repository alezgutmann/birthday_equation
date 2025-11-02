#!/usr/bin/env python3
"""
Birthday Equation Generator - GUI Version

A simple graphical user interface for generating arithmetic equations
from date digits and saving them to a file.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import os
from datetime import datetime
from birthday_equation import BirthdayEquationGenerator


class BirthdayEquationGUI:
    """GUI application for birthday equation generation."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Birthday Equation Generator")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variables
        self.date_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
        self.progress_var = tk.DoubleVar()
        
        # Current equations data
        self.current_equations = []
        self.current_date = ""
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface."""
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Birthday Equation Generator", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="Date:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.date_entry = ttk.Entry(input_frame, textvariable=self.date_var, font=("Arial", 12))
        self.date_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.date_entry.bind('<Return>', lambda e: self.generate_equations())
        
        self.generate_btn = ttk.Button(input_frame, text="Generate Equations", 
                                     command=self.generate_equations)
        self.generate_btn.grid(row=0, column=2)
        
        # Example label
        example_label = ttk.Label(input_frame, 
                                text="Examples: 09052005, 09/05/2005, 2005-05-09, 123456", 
                                font=("Arial", 9), foreground="gray")
        example_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(5, 0))
        
        # Progress section
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                          mode='determinate')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        self.status_label.grid(row=0, column=1)
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Generated Equations", padding="10")
        results_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        
        # Results info
        self.results_info = ttk.Label(results_frame, text="No equations generated yet.")
        self.results_info.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Buttons frame
        buttons_frame = ttk.Frame(results_frame)
        buttons_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.preview_btn = ttk.Button(buttons_frame, text="Preview Results", 
                                    command=self.preview_results, state=tk.DISABLED)
        self.preview_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.save_btn = ttk.Button(buttons_frame, text="Save to File", 
                                 command=self.save_to_file, state=tk.DISABLED)
        self.save_btn.grid(row=0, column=1, padx=(0, 10))
        
        self.clear_btn = ttk.Button(buttons_frame, text="Clear Results", 
                                  command=self.clear_results)
        self.clear_btn.grid(row=0, column=2)
        
        # Preview area (initially hidden)
        self.preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="10")
        self.preview_text = scrolledtext.ScrolledText(self.preview_frame, height=15, width=80, 
                                                    font=("Consolas", 10))
        self.preview_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.preview_frame.columnconfigure(0, weight=1)
        self.preview_frame.rowconfigure(0, weight=1)
        
        # Set placeholder text
        self.date_var.set("09052005")
        
    def generate_equations(self):
        """Generate equations in a separate thread to prevent UI freezing."""
        date_input = self.date_var.get().strip()
        
        if not date_input:
            messagebox.showerror("Error", "Please enter a date.")
            return
            
        # Disable button during generation
        self.generate_btn.config(state=tk.DISABLED)
        self.preview_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)
        
        # Start generation in separate thread
        thread = threading.Thread(target=self._generate_equations_thread, args=(date_input,))
        thread.daemon = True
        thread.start()
        
    def _generate_equations_thread(self, date_input):
        """Generate equations in background thread."""
        try:
            self.root.after(0, lambda: self.status_var.set("Initializing..."))
            self.root.after(0, lambda: self.progress_var.set(10))
            
            # Create generator
            generator = BirthdayEquationGenerator(date_input)
            self.current_date = date_input
            
            self.root.after(0, lambda: self.status_var.set("Generating equations..."))
            self.root.after(0, lambda: self.progress_var.set(30))
            
            # Generate equations
            equations = generator.generate_equations()
            
            self.root.after(0, lambda: self.status_var.set("Processing results..."))
            self.root.after(0, lambda: self.progress_var.set(70))
            
            # Remove duplicates and sort
            unique_equations = list(set(equations))
            unique_equations.sort(key=lambda x: (abs(x[2]), len(x[0]), x[0]))
            
            self.current_equations = unique_equations
            
            self.root.after(0, lambda: self.progress_var.set(100))
            self.root.after(0, lambda: self.status_var.set(f"Generated {len(unique_equations)} unique equations"))
            
            # Update UI
            self.root.after(0, self._update_results_ui)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to generate equations:\n{str(e)}"))
            self.root.after(0, lambda: self.status_var.set("Error occurred"))
            self.root.after(0, lambda: self.progress_var.set(0))
        finally:
            # Re-enable button
            self.root.after(0, lambda: self.generate_btn.config(state=tk.NORMAL))
    
    def _update_results_ui(self):
        """Update the results section of the UI."""
        count = len(self.current_equations)
        
        if count > 0:
            self.results_info.config(text=f"Generated {count} unique equations for '{self.current_date}'")
            self.preview_btn.config(state=tk.NORMAL)
            self.save_btn.config(state=tk.NORMAL)
        else:
            self.results_info.config(text="No valid equations found.")
            self.preview_btn.config(state=tk.DISABLED)
            self.save_btn.config(state=tk.DISABLED)
    
    def preview_results(self):
        """Show preview of generated equations."""
        if not self.current_equations:
            messagebox.showwarning("Warning", "No equations to preview.")
            return
        
        # Show preview frame
        self.preview_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Clear and populate preview text
        self.preview_text.delete(1.0, tk.END)
        
        preview_content = self._generate_file_content()
        self.preview_text.insert(1.0, preview_content)
        
        # Scroll to top
        self.preview_text.see(1.0)
    
    def _generate_file_content(self):
        """Generate the content that will be saved to file."""
        lines = []
        lines.append("Birthday Equation Generator Results")
        lines.append("=" * 50)
        lines.append(f"Date Input: {self.current_date}")
        lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if hasattr(self, 'generator') and hasattr(self.generator, 'digits'):
            lines.append(f"Extracted Digits: {self.generator.digits}")
        
        lines.append(f"Total Unique Equations: {len(self.current_equations)}")
        lines.append("")
        lines.append("Valid Equations:")
        lines.append("-" * 30)
        
        for i, (left, right, value) in enumerate(self.current_equations, 1):
            lines.append(f"{i:4d}. {left} = {right}  (= {value})")
        
        lines.append("")
        lines.append("End of Results")
        
        return "\n".join(lines)
    
    def save_to_file(self):
        """Save equations to a file."""
        if not self.current_equations:
            messagebox.showwarning("Warning", "No equations to save.")
            return
        
        # Get default filename
        safe_date = self.current_date.replace("/", "-").replace("\\", "-").replace(":", "-")
        default_filename = f"birthday_equations_{safe_date}.txt"
        
        # Ask user for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialname=default_filename,
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ],
            title="Save Equations to File"
        )
        
        if not file_path:
            return  # User cancelled
        
        try:
            content = self._generate_file_content()
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            messagebox.showinfo("Success", f"Equations saved to:\n{file_path}")
            self.status_var.set(f"Saved {len(self.current_equations)} equations to file")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
    
    def clear_results(self):
        """Clear all results and reset the interface."""
        self.current_equations = []
        self.current_date = ""
        self.results_info.config(text="No equations generated yet.")
        self.preview_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)
        self.status_var.set("Ready")
        self.progress_var.set(0)
        
        # Hide preview frame
        self.preview_frame.grid_remove()
        
        # Clear preview text
        self.preview_text.delete(1.0, tk.END)


def main():
    """Main function to run the GUI application."""
    root = tk.Tk()
    
    # Set app icon (if available)
    try:
        # You can add an icon file here if you have one
        # root.iconbitmap('icon.ico')
        pass
    except:
        pass
    
    app = BirthdayEquationGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    # Start the GUI
    root.mainloop()


if __name__ == "__main__":
    main()