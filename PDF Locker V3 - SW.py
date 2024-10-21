import os
import subprocess
import sys
from tkinter import Tk, filedialog, simpledialog, Button, Label, Frame

# Function to install packages via pip
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try to import required packages, install if they are missing
try:
    from PyPDF2 import PdfReader, PdfWriter
except ImportError:
    print("PyPDF2 not found. Installing...")
    install_package("PyPDF2")
    from PyPDF2 import PdfReader, PdfWriter

def lock_pdf(input_pdf, output_pdf, password):
    # Create a PdfReader object to read the input PDF
    reader = PdfReader(input_pdf)
    # Create a PdfWriter object to write the encrypted PDF
    writer = PdfWriter()

    # Add all pages from the reader to the writer
    for page_num in range(len(reader.pages)):
        writer.add_page(reader.pages[page_num])

    # Encrypt the PDF with the given password
    writer.encrypt(user_pwd=password, owner_pwd=None, use_128bit=True)

    # Write the encrypted PDF to the output file
    with open(output_pdf, 'wb') as output_file:
        writer.write(output_file)

    print(f"Locked {input_pdf} with password.")

def lock_all_pdfs_in_directory(directory, password, save_directory=None):
    # Loop through all files in the given directory
    for filename in os.listdir(directory):
        # Check if the file is a PDF
        if filename.endswith('.pdf'):
            input_pdf = os.path.join(directory, filename)
            # Set the output path (save in custom directory or the same as the input)
            if save_directory:
                output_pdf = os.path.join(save_directory, f"locked_{filename}")
            else:
                output_pdf = os.path.join(directory, f"locked_{filename}")
            # Lock the PDF with the password
            lock_pdf(input_pdf, output_pdf, password)

def select_directory_and_lock():
    pdf_directory = filedialog.askdirectory(title="Select Directory Containing PDFs")
    if pdf_directory:
        pdf_password = ask_password()
        if pdf_password:
            save_directory = filedialog.askdirectory(title="Select Directory to Save Locked PDFs (Leave blank to save in the same folder)")
            if not save_directory:  # If no save directory chosen, save in the same folder
                save_directory = None
            lock_all_pdfs_in_directory(pdf_directory, pdf_password, save_directory)
        else:
            print("No password provided.")
    else:
        print("No directory selected.")

def select_single_pdf_and_lock():
    input_pdf = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF files", "*.pdf")])
    if input_pdf:
        pdf_password = ask_password()
        if pdf_password:
            save_directory = filedialog.askdirectory(title="Select Directory to Save Locked PDF (Leave blank to save in the same folder)")
            if save_directory:
                output_pdf = os.path.join(save_directory, f"locked_{os.path.basename(input_pdf)}")
            else:
                output_pdf = os.path.join(os.path.dirname(input_pdf), f"locked_{os.path.basename(input_pdf)}")
            lock_pdf(input_pdf, output_pdf, pdf_password)
        else:
            print("No password provided.")
    else:
        print("No PDF selected.")

def ask_password():
    password = simpledialog.askstring("Password", "Enter the password for the PDF:", show='*')
    return password

def create_home_page():
    root = Tk()
    root.title("PDF Locker")
    
    # Frame for the buttons and label
    frame = Frame(root)
    frame.pack(pady=20)

    # Add label
    label = Label(frame, text="Select an Option to Lock PDFs", font=("Helvetica", 14))
    label.pack(pady=20)

    # Button to lock all PDFs in a folder
    folder_button = Button(frame, text="Lock PDFs in a Folder", command=select_directory_and_lock, width=30, height=2)
    folder_button.pack(pady=10)

    # Button to lock a single PDF
    single_pdf_button = Button(frame, text="Lock a Single PDF", command=select_single_pdf_and_lock, width=30, height=2)
    single_pdf_button.pack(pady=10)

    # Label for "Made by Sophie Wilson" at the bottom right
    credit_label = Label(root, text="Made by - Sophie Wilson :)", font=("Helvetica", 8))
    credit_label.pack(side="bottom", anchor="e", padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_home_page()
