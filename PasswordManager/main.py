from PIL import Image
import secrets
import tkinter as tk
from tkinter import filedialog

# Create the main window
root = tk.Tk()
root.title("Image Viewer")
root.configure(bg='black')

# Function to open an image file
def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    sz = 128
    image = Image.open(file_path)
    offset = int(str(image.width)[0]) + int(str(image.height)[0])
    print(image.mode)
    pin = f"{secrets.randbelow(10**128):0128d}"
    print(pin)
    pixel_lst = list(image.getdata())
    for cursor in range(1, sz):
        r=g=b=a=0
        if image.mode == 'RGB':
            r, g, b = pixel_lst[cursor*offset]
        elif image.mode == 'RGBA':
            r, g, b, a = pixel_lst[cursor*offset]
        binario = bin(int(pin[cursor]))[2:].zfill(4)
        print(binario)
        r = int(f"{bin(r)[:-2]}" + binario[-2:], 2)
        g = int(f"{bin(g)[:-2]}" + binario[-4:-2], 2)
        b = int(f"{bin(b)[:-2]}" + binario[-6:-4], 2)
        x = cursor
        y = 0
        while x > image.width:
            x -= image.width
            y += 1
        if image.mode == 'RGB':
            image.putpixel(xy=(x,y), value=(r, g, b))
        elif image.mode == 'RGBA':
            image.putpixel(xy=(x,y), value=(r, g, b, a))
        cursor += 1

# Create a button to open an image
open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.pack(pady=20)

# Run the application
root.mainloop()

