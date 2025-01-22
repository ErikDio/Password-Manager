from PIL import Image
import secrets
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import ThemedStyle

# Create the main window
root = tk.Tk()
root.title("Image Viewer")
root.configure(bg='black')
root.geometry("800x600")

# Function to open an image file
def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    sz = 128
    image = Image.open(file_path).convert("RGB")
    image.save("conv.png")
    image = Image.open("conv.png")
    offset = int(str(image.width)[0]) + int(str(image.height)[0])
    #print(image.mode)
    pin = f"{secrets.randbelow(10**128):0128d}"
    print(pin)
    #print(len(image.getbands()))
    pixel_lst = list(image.getdata())
    for cursor in range(1, sz+1):        
        r, g, b = pixel_lst[cursor*offset]
        binario = format(int(pin[cursor-1]), '#010b')
        #print(binario, end=" ")
        redbin = format(r, '#010b')
        greenbin = format(g, '#010b')
        bluebin = format(b, '#010b')
        r = int(f"{redbin[:-2]+binario[-2:]}", 2)
        g = int(f"{greenbin[:-1]+binario[-3]}", 2)
        b = int(f"{bluebin[:-1]+binario[-4]}", 2)
        x = cursor*offset % image.width
        y = cursor*offset // image.width
        image.putpixel(xy=(x,y), value=(r, g, b))
        #print(x, y)
    image.save("encrypted.png")
    
def decrypt():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    sz = 128
    image = Image.open(file_path)
    image.convert("RGB")
    offset = int(str(image.width)[0]) + int(str(image.height)[0])
    pixel_lst = list(image.getdata())
    conv = ""
    #print(len(image.getbands()))
    for cursor in range(1, sz+1):
        r=g=b=a=0
        r, g, b = pixel_lst[cursor*offset]
        redbin = format(r, '#010b')
        greenbin = format(g, '#010b')
        bluebin = format(b, '#010b')
        #print(f"{redbin} : {r} {greenbin} : {g} {bluebin} : {b}", end=" | ")
        bincor = f"0b{bluebin[-1]}{greenbin[-1]}{redbin[-2:]}"
        #print(bincor, end=" ")
        binario = int(bincor, 0)
        conv += str(binario)
    number_label.config(text=conv)
# Create a button to open an image
open_button = tk.Button(root, text="Open Image", command=open_image)
decrypt_button = tk.Button(root, text="Decrypt", command=decrypt)
open_button.pack(pady=20)
decrypt_button.pack(pady=20)
number_label = tk.Label(root, text="", bg='black', fg='white', font=("Helvetica", 16),wraplength=750)
number_label.pack(pady=20)

# Run the application
root.mainloop()
