import tkinter as tk
from tkinter import filedialog, messagebox
from pdf2image import convert_from_path
from PIL import Image, ImageTk
import os

# Function to draw gradient background
def draw_gradient(canvas, color1, color2):
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    
    limit = height
    for i in range(limit):
        color = blend_colors(color1, color2, i / limit)
        canvas.create_line(0, i, width, i, fill=color)

# Function to blend two colors for the gradient
def blend_colors(color1, color2, blend_factor):
    c1 = canvas.winfo_rgb(color1)
    c2 = canvas.winfo_rgb(color2)
    
    r = int(c1[0] + (c2[0] - c1[0]) * blend_factor) // 256
    g = int(c1[1] + (c2[1] - c1[1]) * blend_factor) // 256
    b = int(c1[2] + (c2[2] - c1[2]) * blend_factor) // 256
    
    return f'#{r:02x}{g:02x}{b:02x}'

# Function to create rounded button
def create_rounded_button(text, command, canvas, x, y):
    button = tk.Button(
        canvas, text=text, command=command, fg="black", bg="#c9f6ff", 
        relief="flat", font=("Arial", 12, "bold"), padx=20, pady=10, 
        activebackground="#78e3ff", activeforeground="black"
    )
    button.place(x=x, y=y, width=180, height=50)
    return button

# Function to convert PDF to JPG
def convert_pdf_to_jpg():
    pdf_file = filedialog.askopenfilename(
        title="Select PDF file", 
        filetypes=(("PDF Files", "*.pdf"),)
    )
    
    if not pdf_file:
        return  # No file selected

    output_folder = filedialog.askdirectory(
        title="Select output folder"
    )
    
    if not output_folder:
        return  # No folder selected

    try:
        poppler_path = r'C:\Users\ASUS\Downloads\Release-24.07.0-0\poppler-24.07.0\Library\bin'  # Change to your Poppler path
        pages = convert_from_path(pdf_file, 300, poppler_path=poppler_path)
        for i, page in enumerate(pages):
            jpg_filename = os.path.join(output_folder, f"page_{i+1}.jpg")
            page.save(jpg_filename, "JPEG")
        
        messagebox.showinfo("Success", "PDF converted to JPG successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to convert JPG to PDF
def convert_jpg_to_pdf():
    image_files = filedialog.askopenfilenames(
        title="Select JPG files", 
        filetypes=(("JPG Files", "*.jpg"), ("JPEG Files", "*.jpeg"))
    )
    
    if not image_files:
        return

    output_pdf = filedialog.asksaveasfilename(
        defaultextension=".pdf", 
        filetypes=[("PDF files", "*.pdf")],
        title="Save as PDF"
    )
    
    if not output_pdf:
        return

    try:
        images = [Image.open(img).convert('RGB') for img in image_files]
        images[0].save(output_pdf, save_all=True, append_images=images[1:])
        messagebox.showinfo("Success", "JPG files converted to PDF successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to convert JPG to PNG
def convert_jpg_to_png():
    image_files = filedialog.askopenfilenames(
        title="Select JPG files", 
        filetypes=(("JPG Files", "*.jpg"), ("JPEG Files", "*.jpeg"))
    )
    
    if not image_files:
        return

    output_folder = filedialog.askdirectory(
        title="Select output folder"
    )
    
    if not output_folder:
        messagebox.showerror("Error", "No output folder selected!")
        return

    try:
        for img_file in image_files:
            img = Image.open(img_file)
            base_filename = os.path.splitext(os.path.basename(img_file))[0]
            png_filename = os.path.join(output_folder, f"{base_filename}.png")
            img.save(png_filename, "PNG")
        
        messagebox.showinfo("Success", "JPG files converted to PNG successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Initialize the GUI window
root = tk.Tk()
root.title("PDF-JPG-PNG Converter")
root.geometry("400x400")

# Create a canvas for gradient background
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack(fill="both", expand=True)

# Apply gradient background
root.update()
draw_gradient(canvas, "#8f4ef2", "#f48a4a")  # Colors can be adjusted

# Add buttons with rounded appearance
create_rounded_button("Convert PDF to JPG", convert_pdf_to_jpg, canvas, 110, 100)
create_rounded_button("Convert JPG to PDF", convert_jpg_to_pdf, canvas, 110, 170)
create_rounded_button("Convert JPG to PNG", convert_jpg_to_png, canvas, 110, 240)

# Run the GUI event loop
root.mainloop()
