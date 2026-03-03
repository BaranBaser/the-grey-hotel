import os
import re
from PIL import Image

image_dir = r"d:\Ders\CODES\the-grey-hotel\images"
html_path = r"d:\Ders\CODES\the-grey-hotel\index.html"

# Convert images
for filename in os.listdir(image_dir):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        old_path = os.path.join(image_dir, filename)
        name, _ = os.path.splitext(filename)
        new_filename = name + ".webp"
        new_path = os.path.join(image_dir, new_filename)
        
        if not os.path.exists(new_path):
            try:
                with Image.open(old_path) as img:
                    # Convert to RGB if RGBA/P
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    img.save(new_path, "WEBP", quality=85)
                    print(f"Converted {filename} to {new_filename}")
            except Exception as e:
                print(f"Failed to convert {filename}: {e}")

# Update HTML references
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Replace image references, but preserve og:image
def replacer(match):
    original = match.group(0)
    # Don't replace if it's the og:image URL
    if "hero.jpeg" in original and "og:image" in html_content[max(0, match.start()-100):match.start()]:
        return original
    return re.sub(r'\.(jpg|jpeg|png)', '.webp', original, flags=re.IGNORECASE)

new_html_content = re.sub(r'images/[a-zA-Z0-9_\-\.]+\.(jpg|jpeg|png)', replacer, html_content, flags=re.IGNORECASE)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_html_content)

print("Updated HTML references.")
