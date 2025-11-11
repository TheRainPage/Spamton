import os
import random
from PIL import Image
from pathlib import Path
from tkinter import Tk, filedialog

def shift_image_wrap(image, dx, dy):
    """Shift image by dx, dy pixels, wrapping around edges."""
    w, h = image.size
    shifted = Image.new(image.mode, (w, h))
    
    # Break image into four wrapped parts
    shifted.paste(image.crop((0, 0, w, h)), (dx % w, dy % h))
    shifted.paste(image.crop((w - dx % w, 0, w, h)), (0, dy % h))
    shifted.paste(image.crop((0, h - dy % h, w, h)), (dx % w, 0))
    shifted.paste(image.crop((w - dx % w, h - dy % h, w, h)), (0, 0))
    
    return shifted

def process_folder(folder_path):
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')

    for path in Path(folder_path).rglob('*'):
        if path.suffix.lower() in image_extensions:
            try:
                img = Image.open(path).convert("RGBA")

                # Random shift between -2 and 2 (excluding 0)
                dx = random.choice([-2, -1, 1, 2])
                dy = random.choice([-2, -1, 1, 2])

                shifted_img = shift_image_wrap(img, dx, dy)
                shifted_img.save(path)

                print(f"Shifted {path.relative_to(folder_path)} by ({dx}, {dy})")
            except Exception as e:
                print(f"\u0012 Failed to process {path}: {e}")

def main():
    # Hide the root window
    root = Tk()
    root.withdraw()

    print("\u0000 Please choose a folder containing images...")
    folder = filedialog.askdirectory(title="Select Folder with Images")
    if not folder:
        print("No folder selected. Exiting.")
        return

    print(f"Processing images in: {folder}\n")
    process_folder(folder)
    print("\n\u0001 Done shifting all images!")

if __name__ == "__main__":
    main()