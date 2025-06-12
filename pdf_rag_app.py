import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import io

# Global variable to store PDF text content
pdf_text = ""
uploaded_file_content = None

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    global pdf_text
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_text = ""
        for page in pdf_reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:  # Ensure text is not None
                pdf_text += extracted_text + "\n"
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error processing PDF: {e}")
        return False

# Function to search text in PDF content
def search_text(query):
    global pdf_text
    if not pdf_text:
        return "No PDF processed yet. Please upload and process a PDF first."
    if not query:
        return "Please enter a search query."
    
    # Case-insensitive search for keywords or sentences
    results = []
    lines = pdf_text.split("\n")
    query = query.lower()
    for i, line in enumerate(lines, 1):
        if line and query in line.lower():  # Ensure line is not empty
            results.append(f"Line {i}: {line.strip()}")
    
    if results:
        return "\n".join(results)
    else:
        return f"No results found for '{query}'."

# Function to handle file upload
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

# Function to process the uploaded PDF
def process_pdf():
    global pdf_text, uploaded_file_content
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

# Function to handle search
def perform_search():
    query = search_box.get().strip()
    result = search_text(query)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, result)

# Function to reset the application
def reset_app():
    global pdf_text, uploaded_file_content
    pdf_text = ""
    uploaded_file_content = None
    search_box.delete(0, tk.END)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Application reset. Please upload a new PDF.")
    process_button.config(state="disabled")
    search_button.config(state="disabled")

# Create the main GUI window
root = tk.Tk()
root.title("PDF RAG System")
root.geometry("800x600")

# Left Panel (Upload and Process)
left_frame = tk.Frame(root, padx=10, pady=10)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

upload_button = tk.Button(left_frame, text="Upload PDF", command=upload_pdf, bg="lightblue")
upload_button.pack(pady=5)

process_button = tk.Button(left_frame, text="Process", command=process_pdf, state="disabled", bg="lightgreen")
process_button.pack(pady=5)

# Right Panel (Search and Results)
right_frame = tk.Frame(root, padx=10, pady=10)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

search_label = tk.Label(right_frame, text="Search:")
search_label.pack(anchor="w")

search_box = tk.Entry(right_frame, width=50)
search_box.pack(anchor="w", pady=5)

search_button = tk.Button(right_frame, text="Search from PDF", command=perform_search, state="disabled", bg="lightblue")
search_button.pack(anchor="w", pady=5)

reset_button = tk.Button(right_frame, text="Reset", command=reset_app, bg="salmon")
reset_button.pack(anchor="w", pady=5)

output_text = scrolledtext.ScrolledText(right_frame, width=70, height=30, wrap=tk.WORD)
output_text.pack(pady=10, fill=tk.BOTH, expand=True)

# Start the GUI event loop
root.mainloop()
