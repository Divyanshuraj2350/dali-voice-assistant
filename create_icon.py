from PIL import Image, ImageDraw, ImageFont
import os

# Create a 512x512 image with gradient background
size = 512
img = Image.new('RGB', (size, size), color='#0a0e27')
draw = ImageDraw.Draw(img)

# Draw gradient circle
for i in range(100):
    radius = size // 2 - i * 2
    color = (0, 212 - i, 255 - i)
    draw.ellipse([size//2 - radius, size//2 - radius, 
                  size//2 + radius, size//2 + radius], 
                 outline=color, width=3)

# Draw "DALI" text
try:
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 120)
except:
    font = ImageFont.load_default()

text = "DALI"
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
position = ((size - text_width) // 2, (size - text_height) // 2 - 20)

draw.text(position, text, fill='#00d4ff', font=font)

# Save as PNG
img.save('dali_icon.png')
print("✅ Icon created: dali_icon.png")

# Convert to iconset (macOS icon format)
os.makedirs('dali_icon.iconset', exist_ok=True)
sizes = [16, 32, 64, 128, 256, 512]
for size in sizes:
    resized = img.resize((size, size), Image.Resampling.LANCZOS)
    resized.save(f'dali_icon.iconset/icon_{size}x{size}.png')
    if size <= 256:
        resized2x = img.resize((size*2, size*2), Image.Resampling.LANCZOS)
        resized2x.save(f'dali_icon.iconset/icon_{size}x{size}@2x.png')

print("✅ Iconset created")
