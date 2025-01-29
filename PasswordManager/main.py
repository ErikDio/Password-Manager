from PIL import Image
import secrets
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import ThemedStyle
import string

# Create the main window
root = tk.Tk()
root.title("Image Viewer")
root.configure(bg='black')
root.geometry("800x600")

# Function to open an image file
def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    sz = 128
    image = Image.open(file_path)
    if image.mode != "RGB":
        image.convert("RGB")
        image.save(file_path)
        image = Image.open(file_path)
    offset = int(str(image.width)[0]) + int(str(image.height)[0])
    pin = f"{secrets.randbelow(10**128):0128d}"
    print(pin)
    pixel_lst = list(image.getdata())
    for cursor in range(1, sz+1):
        r=g=b=a=0
        if(len(image.getbands())==3):
            r, g, b = pixel_lst[cursor*offset]
        elif(len(image.getbands())==4):
            r, g, b, a = pixel_lst[cursor*offset]
        else:
            print("Invalid image format")
            return
        binario = format(int(pin[cursor-1]), '#010b')
        redbin = format(r, '#010b')
        greenbin = format(g, '#010b')
        bluebin = format(b, '#010b')
        r = int(f"{redbin[:-2]+binario[-2:]}", 2)
        g = int(f"{greenbin[:-1]+binario[-3]}", 2)
        b = int(f"{bluebin[:-1]+binario[-4]}", 2)
        x = cursor*offset % image.width
        y = cursor*offset // image.width
        image.putpixel(xy=(x,y), value=(r, g, b))
    image.save("encrypted.png")
    
def decrypt():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    sz = 128
    image = Image.open(file_path)
    if image.mode != "RGB":
        image.convert("RGB")
        image.save(file_path)
        image = Image.open(file_path)
    offset = int(str(image.width)[0]) + int(str(image.height)[0])
    pixel_lst = list(image.getdata())
    conv = ""
    for cursor in range(1, sz+1):
        r=g=b=a=0
        if(len(image.getbands())==3):
            r, g, b = pixel_lst[cursor*offset]
        elif(len(image.getbands())==4):
            r, g, b, a = pixel_lst[cursor*offset]
        else:
            print("Invalid image format")
            return
        redbin = format(r, '#010b')
        greenbin = format(g, '#010b')
        bluebin = format(b, '#010b')
        bincor = f"0b{bluebin[-1]}{greenbin[-1]}{redbin[-2:]}"
        binario = int(bincor, 0)
        conv += str(binario)
    number_label.config(text=conv)

open_button = tk.Button(root, text="Open Image", command=open_image)
decrypt_button = tk.Button(root, text="Decrypt", command=decrypt)
open_button.pack(pady=20)
decrypt_button.pack(pady=20)
number_label = tk.Label(root, text="", bg='black', fg='white', font=("Helvetica", 16),wraplength=750)
number_label.pack(pady=20)

# Run the application
root.mainloop()
