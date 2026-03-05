import os
from PIL import Image

dir_path = r"C:\Users\GamingX\.gemini\antigravity\brain\d665ad33-9b9e-4955-92dc-bd716983e9fb"
for filename in os.listdir(dir_path):
    if filename.endswith(".png") and "premium_" in filename:
        img = Image.open(os.path.join(dir_path, filename))
        new_filename = filename.replace(".png", ".webp")
        img.save(os.path.join(dir_path, new_filename), "webp", quality=90)
        print(f"Converted {filename} to {new_filename}")
