#!/usr/bin/env python3
"""
Advanced Birthday Equation Generator - Enhanced GUI Version

Enhanced GUI with more features including advanced equation generation,
multiple export formats, and better user experience.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import json
import os
import csv
from datetime import datetime
from birthday_equation import BirthdayEquationGenerator
from advanced_birthday_equation import AdvancedBirthdayEquationGenerator


class EnhancedBirthdayEquationGUI:
    """Enhanced GUI application with more features."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Birthday Equation Generator")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')  # Use a more modern theme
        
        # Variables
        self.date_var = tk.StringVar()
        self.generator_type_var = tk.StringVar(value="basic")
        self.status_var = tk.StringVar(value="Ready")
        self.progress_var = tk.DoubleVar()
        self.max_display_var = tk.IntVar(value=50)
        self.sort_by_var = tk.StringVar(value="value_asc")
        
        # Current data
        self.current_equations = []
        self.current_date = ""
        self.current_digits = []
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the enhanced user interface."""
        # Main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.setup_generator_tab()
        self.setup_results_tab()
        self.setup_settings_tab()
        
    def setup_generator_tab(self):
        """Set up the main generator tab."""
        self.generator_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.generator_frame, text="Generator")
        
        # Configure grid
        self.generator_frame.columnconfigure(0, weight=1)
        self.generator_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(self.generator_frame, text="Birthday Equation Generator", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20), sticky=tk.W)
        
        # Input section
        input_frame = ttk.LabelFrame(self.generator_frame, text="Input Configuration", padding="15")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        input_frame.columnconfigure(1, weight=1)
        
        # Date input
        ttk.Label(input_frame, text="Date:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.date_entry = ttk.Entry(input_frame, textvariable=self.date_var, font=("Arial", 12), width=30)
        self.date_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.date_entry.bind('<Return>', lambda e: self.generate_equations())
        
        # Example label
        example_label = ttk.Label(input_frame, 
                                text="Examples: 09052005, 09/05/2005, 2005-05-09, 123456, 31121999", 
                                font=("Arial", 9), foreground="gray")
        example_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # Generator type selection
        ttk.Label(input_frame, text="Generator Type:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(15, 0))
        
        type_frame = ttk.Frame(input_frame)
        type_frame.grid(row=2, column=1, sticky=tk.W, pady=(15, 0))
        
        ttk.Radiobutton(type_frame, text="Basic Generator", variable=self.generator_type_var, 
                       value="basic").grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        ttk.Radiobutton(type_frame, text="Advanced Generator", variable=self.generator_type_var, 
                       value="advanced").grid(row=0, column=1, sticky=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(20, 0))
        
        self.generate_btn = ttk.Button(button_frame, text="Generate Equations", 
                                     command=self.generate_equations, style="Accent.TButton")
        self.generate_btn.grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(button_frame, text="Clear All", 
                  command=self.clear_all).grid(row=0, column=1)
        
        # Progress section
        progress_frame = ttk.LabelFrame(self.generator_frame, text="Progress", padding="10")
        progress_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                          mode='determinate', length=400)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var, font=("Arial", 10))
        self.status_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # Quick info section
        self.info_frame = ttk.LabelFrame(self.generator_frame, text="Information", padding="10")
        self.info_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.info_text = tk.Text(self.info_frame, height=8, font=("Arial", 10), 
                               wrap=tk.WORD, state=tk.DISABLED)
        info_scrollbar = ttk.Scrollbar(self.info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=info_scrollbar.set)
        
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        info_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.info_frame.columnconfigure(0, weight=1)
        self.info_frame.rowconfigure(0, weight=1)
        
        # Set placeholder
        self.date_var.set("09052005")
        self._update_info("Welcome! Enter a date and click 'Generate Equations' to start.")
        
    def setup_results_tab(self):
        """Set up the results viewing tab."""
        self.results_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.results_frame, text="Results")
        
        self.results_frame.columnconfigure(0, weight=1)
        self.results_frame.rowconfigure(1, weight=1)
        
        # Results header
        header_frame = ttk.Frame(self.results_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(1, weight=1)
        
        self.results_info_label = ttk.Label(header_frame, text="No results yet", 
                                          font=("Arial", 12, "bold"))
        self.results_info_label.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        
        # Export buttons
        export_frame = ttk.Frame(header_frame)
        export_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        self.export_txt_btn = ttk.Button(export_frame, text="Export as TXT", 
                                       command=lambda: self.export_results("txt"), state=tk.DISABLED)
        self.export_txt_btn.grid(row=0, column=0, padx=(0, 5))
        
        self.export_csv_btn = ttk.Button(export_frame, text="Export as CSV", 
                                       command=lambda: self.export_results("csv"), state=tk.DISABLED)
        self.export_csv_btn.grid(row=0, column=1, padx=(0, 5))
        
        self.export_json_btn = ttk.Button(export_frame, text="Export as JSON", 
                                        command=lambda: self.export_results("json"), state=tk.DISABLED)
        self.export_json_btn.grid(row=0, column=2, padx=(0, 15))
        
        # Sorting controls
        ttk.Label(export_frame, text="Sort by:").grid(row=0, column=3, padx=(15, 5))
        sort_combo = ttk.Combobox(export_frame, textvariable=self.sort_by_var, width=12, state="readonly")
        sort_combo['values'] = (
            "value_asc", "value_desc", 
            "length_asc", "length_desc",
            "alphabetic", "original"
        )
        sort_combo.grid(row=0, column=4, padx=(0, 10))
        sort_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_results_display())
        
        # Display limit
        ttk.Label(export_frame, text="Display limit:").grid(row=0, column=5, padx=(10, 5))
        limit_spinbox = ttk.Spinbox(export_frame, from_=10, to=1000, width=8, 
                                  textvariable=self.max_display_var)
        limit_spinbox.grid(row=0, column=6, padx=(0, 5))
        ttk.Button(export_frame, text="Refresh", 
                  command=self.refresh_results_display).grid(row=0, column=7)
        
        # Results display
        self.results_text = scrolledtext.ScrolledText(self.results_frame, font=("Consolas", 10), 
                                                    wrap=tk.NONE)
        self.results_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def setup_settings_tab(self):
        """Set up the settings/help tab."""
        self.settings_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.settings_frame, text="Settings & Help")
        
        # About section
        about_frame = ttk.LabelFrame(self.settings_frame, text="About", padding="10")
        about_frame.pack(fill=tk.X, pady=(0, 15))
        
        about_text = """Birthday Equation Generator v2.0
        
This application generates arithmetic equations using digits from dates.
It tries all possible combinations of operators (+, -, *, /, ^, root) and factorial 
to find valid equations where the left side equals the right side.

Supported operations:
• Basic arithmetic: +, -, *, /
• Exponentiation: ^ (power)
• Root functions: root(a,b) for b-th root of a
• Factorial: fact(n) for n! (up to 12!)

Two generation modes are available:
• Basic: Standard equation generation with sequential digit splitting
• Advanced: Enhanced generation with better operator precedence and grouping"""
        
        ttk.Label(about_frame, text=about_text, justify=tk.LEFT, font=("Arial", 10)).pack(anchor=tk.W)
        
        # Instructions section
        instructions_frame = ttk.LabelFrame(self.settings_frame, text="How to Use", padding="10")
        instructions_frame.pack(fill=tk.X, pady=(0, 15))
        
        instructions_text = """1. Enter a date in any format (e.g., 09052005, 09/05/2005, 2005-05-09)
2. Choose between Basic or Advanced generation mode
3. Click "Generate Equations" to start processing
4. View results in the Results tab
5. Export equations in TXT, CSV, or JSON format
6. Use the display limit to control how many equations are shown"""
        
        ttk.Label(instructions_frame, text=instructions_text, justify=tk.LEFT, font=("Arial", 10)).pack(anchor=tk.W)
        
        # Settings section  
        settings_section = ttk.LabelFrame(self.settings_frame, text="Settings", padding="10")
        settings_section.pack(fill=tk.X)
        
        ttk.Label(settings_section, text="Default export location:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        location_frame = ttk.Frame(settings_section)
        location_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.export_location_var = tk.StringVar(value=os.path.expanduser("~/Desktop"))
        ttk.Entry(location_frame, textvariable=self.export_location_var, 
                 font=("Arial", 10)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(location_frame, text="Browse", 
                  command=self.browse_export_location).pack(side=tk.RIGHT)
        
    def _update_info(self, message):
        """Update the info text area."""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, message)
        self.info_text.config(state=tk.DISABLED)
        
    def generate_equations(self):
        """Generate equations in background thread."""
        date_input = self.date_var.get().strip()
        
        if not date_input:
            messagebox.showerror("Error", "Please enter a date.")
            return
            
        # Disable UI during generation
        self.generate_btn.config(state=tk.DISABLED)
        self._disable_export_buttons()
        
        # Start generation thread
        thread = threading.Thread(target=self._generate_equations_thread, 
                                args=(date_input, self.generator_type_var.get()))
        thread.daemon = True
        thread.start()
        
    def _generate_equations_thread(self, date_input, generator_type):
        """Background equation generation."""
        try:
            self.root.after(0, lambda: self.status_var.set("Initializing generator..."))
            self.root.after(0, lambda: self.progress_var.set(5))
            
            # Create appropriate generator
            if generator_type == "advanced":
                generator = AdvancedBirthdayEquationGenerator(date_input)
                self.root.after(0, lambda: self._update_info(f"Using Advanced Generator\nDate: {date_input}\nDigits: {generator.digits}"))
            else:
                generator = BirthdayEquationGenerator(date_input)
                self.root.after(0, lambda: self._update_info(f"Using Basic Generator\nDate: {date_input}\nDigits: {generator.digits}"))
            
            self.current_date = date_input
            self.current_digits = generator.digits
            
            self.root.after(0, lambda: self.progress_var.set(20))
            self.root.after(0, lambda: self.status_var.set("Generating equations..."))
            
            # Generate equations
            if generator_type == "advanced":
                equations = generator.find_matching_equations()
            else:
                equations = generator.generate_equations()
            
            self.root.after(0, lambda: self.progress_var.set(70))
            self.root.after(0, lambda: self.status_var.set("Processing results..."))
            
            # Process results
            unique_equations = list(set(equations))
            unique_equations.sort(key=lambda x: (abs(x[2]), len(x[0]), x[0]))
            
            self.current_equations = unique_equations
            
            self.root.after(0, lambda: self.progress_var.set(100))
            self.root.after(0, lambda: self.status_var.set(f"Complete! Generated {len(unique_equations)} unique equations"))
            
            # Update UI
            self.root.after(0, self._update_results_ui)
            
        except Exception as e:
            error_msg = f"Generation failed: {str(e)}"
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            self.root.after(0, lambda: self.status_var.set("Error occurred"))
            self.root.after(0, lambda: self._update_info(f"Error: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.generate_btn.config(state=tk.NORMAL))
    
    def _update_results_ui(self):
        """Update UI after equation generation."""
        count = len(self.current_equations)
        
        if count > 0:
            info_text = f"Generated {count} unique equations for '{self.current_date}'\n"
            info_text += f"Digits used: {self.current_digits}\n"
            info_text += f"Generator: {self.generator_type_var.get().title()}\n\n"
            info_text += "Switch to the Results tab to view and export the equations."
            
            self._update_info(info_text)
            self.results_info_label.config(text=f"{count} equations generated for '{self.current_date}'")
            self._enable_export_buttons()
            self.refresh_results_display()
            
            # Switch to results tab
            self.notebook.select(self.results_frame)
        else:
            self._update_info("No valid equations found for this date. Try a different date or generator type.")
            self.results_info_label.config(text="No results")
    
    def refresh_results_display(self):
        """Refresh the results display with current limit and sorting."""
        if not self.current_equations:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(1.0, "No equations generated yet.")
            return
        
        # Apply sorting based on selected option
        sorted_equations = self._sort_equations(self.current_equations)
        
        limit = self.max_display_var.get()
        display_equations = sorted_equations[:limit]
        
        self.results_text.delete(1.0, tk.END)
        
        sort_desc = self._get_sort_description()
        content = f"Showing {len(display_equations)} of {len(self.current_equations)} equations for '{self.current_date}'\n"
        content += f"Digits: {self.current_digits}\n"
        content += f"Sorted by: {sort_desc}\n"
        content += "=" * 80 + "\n\n"
        
        for i, (left, right, value) in enumerate(display_equations, 1):
            content += f"{i:4d}. {left} = {right}  (= {value})\n"
        
        if len(self.current_equations) > limit:
            content += f"\n... and {len(self.current_equations) - limit} more equations\n"
            content += "Increase display limit to see more results."
        
        self.results_text.insert(1.0, content)
    
    def _sort_equations(self, equations):
        """Sort equations based on the selected sorting method."""
        sort_method = self.sort_by_var.get()
        
        if sort_method == "value_asc":
            return sorted(equations, key=lambda x: x[2])
        elif sort_method == "value_desc":
            return sorted(equations, key=lambda x: x[2], reverse=True)
        elif sort_method == "length_asc":
            return sorted(equations, key=lambda x: (len(x[0]) + len(x[1]), x[2]))
        elif sort_method == "length_desc":
            return sorted(equations, key=lambda x: (len(x[0]) + len(x[1]), x[2]), reverse=True)
        elif sort_method == "alphabetic":
            return sorted(equations, key=lambda x: (x[0], x[1]))
        else:  # original
            return equations
    
    def _get_sort_description(self):
        """Get human-readable description of current sorting method."""
        sort_method = self.sort_by_var.get()
        
        descriptions = {
            "value_asc": "Value (ascending)",
            "value_desc": "Value (descending)", 
            "length_asc": "Expression length (shortest first)",
            "length_desc": "Expression length (longest first)",
            "alphabetic": "Alphabetical order",
            "original": "Original order"
        }
        
        return descriptions.get(sort_method, "Unknown")
    
    def export_results(self, format_type):
        """Export results in specified format."""
        if not self.current_equations:
            messagebox.showwarning("Warning", "No equations to export.")
            return
        
        # Get save location
        safe_date = self.current_date.replace("/", "-").replace("\\", "-").replace(":", "-")
        
        if format_type == "txt":
            default_name = f"birthday_equations_{safe_date}.txt"
            filetypes = [("Text files", "*.txt"), ("All files", "*.*")]
        elif format_type == "csv":
            default_name = f"birthday_equations_{safe_date}.csv"
            filetypes = [("CSV files", "*.csv"), ("All files", "*.*")]
        else:  # json
            default_name = f"birthday_equations_{safe_date}.json"
            filetypes = [("JSON files", "*.json"), ("All files", "*.*")]
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=f".{format_type}",
            initialname=default_name,
            initialdir=self.export_location_var.get(),
            filetypes=filetypes,
            title=f"Export as {format_type.upper()}"
        )
        
        if not file_path:
            return
        
        try:
            if format_type == "txt":
                self._export_txt(file_path)
            elif format_type == "csv":
                self._export_csv(file_path)
            else:
                self._export_json(file_path)
            
            messagebox.showinfo("Success", f"Equations exported to:\n{file_path}")
            self.status_var.set(f"Exported {len(self.current_equations)} equations as {format_type.upper()}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Export failed:\n{str(e)}")
    
    def _export_txt(self, file_path):
        """Export as text file."""
        sorted_equations = self._sort_equations(self.current_equations)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("Birthday Equation Generator Results\n")
            f.write("=" * 60 + "\n")
            f.write(f"Date Input: {self.current_date}\n")
            f.write(f"Extracted Digits: {self.current_digits}\n")
            f.write(f"Generator Type: {self.generator_type_var.get().title()}\n")
            f.write(f"Sorted by: {self._get_sort_description()}\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Unique Equations: {len(sorted_equations)}\n\n")
            
            f.write("Valid Equations:\n")
            f.write("-" * 40 + "\n")
            
            for i, (left, right, value) in enumerate(sorted_equations, 1):
                f.write(f"{i:4d}. {left} = {right}  (= {value})\n")
    
    def _export_csv(self, file_path):
        """Export as CSV file."""
        sorted_equations = self._sort_equations(self.current_equations)
        
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Number', 'Left Side', 'Right Side', 'Value', 'Date', 'Digits', 'Sort_Method'])
            
            for i, (left, right, value) in enumerate(sorted_equations, 1):
                writer.writerow([i, left, right, value, self.current_date, str(self.current_digits), self._get_sort_description()])
    
    def _export_json(self, file_path):
        """Export as JSON file."""
        sorted_equations = self._sort_equations(self.current_equations)
        
        data = {
            'metadata': {
                'date_input': self.current_date,
                'extracted_digits': self.current_digits,
                'generator_type': self.generator_type_var.get(),
                'sort_method': self.sort_by_var.get(),
                'sort_description': self._get_sort_description(),
                'generated_on': datetime.now().isoformat(),
                'total_equations': len(sorted_equations)
            },
            'equations': [
                {
                    'number': i,
                    'left_side': left,
                    'right_side': right,
                    'value': value
                }
                for i, (left, right, value) in enumerate(sorted_equations, 1)
            ]
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _enable_export_buttons(self):
        """Enable export buttons."""
        self.export_txt_btn.config(state=tk.NORMAL)
        self.export_csv_btn.config(state=tk.NORMAL)
        self.export_json_btn.config(state=tk.NORMAL)
    
    def _disable_export_buttons(self):
        """Disable export buttons."""
        self.export_txt_btn.config(state=tk.DISABLED)
        self.export_csv_btn.config(state=tk.DISABLED)
        self.export_json_btn.config(state=tk.DISABLED)
    
    def browse_export_location(self):
        """Browse for export location."""
        location = filedialog.askdirectory(initialdir=self.export_location_var.get())
        if location:
            self.export_location_var.set(location)
    
    def clear_all(self):
        """Clear all data and reset interface."""
        self.current_equations = []
        self.current_date = ""
        self.current_digits = []
        self.results_info_label.config(text="No results yet")
        self._disable_export_buttons()
        self.status_var.set("Ready")
        self.progress_var.set(0)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, "No equations generated yet.")
        self._update_info("Cleared all results. Ready for new generation.")


def main():
    """Main function."""
    root = tk.Tk()
    
    # Configure window
    try:
        root.state('zoomed')  # Maximize on Windows
    except:
        pass
    
    app = EnhancedBirthdayEquationGUI(root)
    
    # Center window if not maximized
    root.update_idletasks()
    
    root.mainloop()


if __name__ == "__main__":
    main()