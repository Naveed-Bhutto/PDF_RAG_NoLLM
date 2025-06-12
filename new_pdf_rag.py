import pdfplumber
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import io
from tkinter import font

pdf_text_with_pages = []
uploaded_file_content = None

def extract_text_from_pdf(pdf_file):
    global pdf_text_with_pages
    try:
        pdf_text_with_pages = []
        with pdfplumber.open(pdf_file) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                extracted_text = page.extract_text()
                if extracted_text:  # Ensure text is not None
                    pdf_text_with_pages.append((page_num, extracted_text))
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error processing PDF: {e}")
        return False

def search_text(query):
    global pdf_text_with_pages
    if not pdf_text_with_pages:
        return "No PDF processed yet. Please upload and process a PDF first."
    if not query:
        return "Please enter a search query."
    
    results = []
    query = query.lower()
    for page_num, text in pdf_text_with_pages:
        lines = text.split("\n")
        for i, line in enumerate(lines, 1):
            if line and query in line.lower():  # Ensure line is not empty
                results.append(f"Page {page_num}, Line {i}: {line.strip()}")
    
    if results:
        return "\n".join(results)
    else:
        return f"No results found for '{query}'."

def upload_pdf():
    global uploaded_file_content
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        with open(file_path, "rb") as f:
            uploaded_file_content = f.read()
        process_button.config(state="normal")
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Uploaded file: {file_path}. Click 'Process' to extract text.")
    else:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "No file uploaded.")

def process_pdf():
    global pdf_text_with_pages, uploaded_file_content
    if uploaded_file_content is None:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "No file uploaded. Please upload a PDF first.")
        return
    
    pdf_file = io.BytesIO(uploaded_file_content)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Processing PDF, please wait...")
    root.update()  # Update GUI to show processing message
    if extract_text_from_pdf(pdf_file):
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "PDF processed successfully. You can now search the content.")
        search_button.config(state="normal")
    else:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Failed to process PDF. Please ensure the file is a valid PDF with extractable text.")

def perform_search():
    query = search_box.get().strip()
    result = search_text(query)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, result)

def reset_app():
    global pdf_text_with_pages, uploaded_file_content
    pdf_text_with_pages = []
    uploaded_file_content = None
    search_box.delete(0, tk.END)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Application reset. Please upload a new PDF.")
    process_button.config(state="disabled")
    search_button.config(state="disabled")

# Create the main window
root = tk.Tk()
root.title("PDF RAG System without LLM by Naveed Ahmed Bhutto - Version 1.01")
root.geometry("900x600")
root.configure(bg="#f0f0f0")  # Light gray background for modern look

# Define custom fonts
title_font = font.Font(family="Helvetica", size=15, weight="bold")
title_font1 = font.Font(family="Helvetica", size=12)
button_font = font.Font(family="Helvetica", size=12, weight="bold")
text_font = font.Font(family="Helvetica", size=12)

# Left frame for buttons   "#f0f0f0"
left_frame = tk.Frame(root, padx=10, pady=10, bg="lightgray")
left_frame.pack(side=tk.LEFT, fill=tk.Y)

# Title for left frame (using grid instead of pack)
title_label = tk.Label(left_frame, text="PDF RAG Tool", font=title_font, bg="light gray")
title_label1 = tk.Label(left_frame, text="by: Naveed Ahmed Bhutto", font=title_font1, bg="light gray")

title_label.grid(row=0, column=0, pady=10)
title_label1.grid(row=1, column=0, pady=10)

# "#f0f0f0"  "#f0f0f0"
title_label = tk.Label(left_frame, 
    text="Version 1.01",
    font=title_font1,
    bg="light gray")
title_label.grid(row=99, column=0, sticky="sw", padx=10, pady=10)

# Buttons with equal size using grid
button_width = 20
upload_button = tk.Button(left_frame, text="Upload PDF", command=upload_pdf, font=button_font, 
                          bg="#4CAF50", fg="white", width=button_width, relief="flat")
upload_button.grid(row=2, column=0, pady=5)

process_button = tk.Button(left_frame, text="Process", command=process_pdf, state="disabled", font=button_font, 
                           bg="#2196F3", fg="white", width=button_width, relief="flat")
process_button.grid(row=3, column=0, pady=5)

search_button = tk.Button(left_frame, text="Search", command=perform_search, state="disabled", font=button_font, 
                          bg="#FFC107", fg="black", width=button_width, relief="flat")
search_button.grid(row=4, column=0, pady=5)

reset_button = tk.Button(left_frame, text="Reset", command=reset_app, font=button_font, 
                         bg="#F44336", fg="white", width=button_width, relief="flat")
reset_button.grid(row=5, column=0, pady=5)

# Right frame for search and output
right_frame = tk.Frame(root, padx=10, pady=10, bg="light gray")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Search section
search_label = tk.Label(right_frame, text="Search:", font=title_font, bg="light gray")
search_label.pack(anchor="w")

search_box = tk.Entry(right_frame, width=70, font=text_font)
search_box.pack(anchor="w", pady=5)

# Output section
output_text = scrolledtext.ScrolledText(right_frame, width=70, height=30, wrap=tk.WORD, font=text_font, bg="#ffffff", relief="flat")
output_text.pack(pady=10, fill=tk.BOTH, expand=True)

# Start the application
root.mainloop()