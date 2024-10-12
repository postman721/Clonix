from PIL import Image, ImageDraw, ImageFont
import os

# Define image properties
BLOCK_SIZE = 60  # Size of each tetromino block
IMAGE_SIZE = (BLOCK_SIZE, BLOCK_SIZE)
FONT_SIZE = 30  # Increased font size for visibility

# Define colors for each tetromino
SHAPE_COLORS = {
    'S': (0, 128, 0),        # Dark Green
    'Z': (128, 0, 0),        # Dark Red
    'I': (0, 128, 128),      # Dark Cyan
    'O': (128, 128, 0),      # Olive
    'J': (255, 140, 0),      # Dark Orange
    'L': (0, 0, 255),        # Blue
    'T': (128, 0, 128)       # Purple
}

# Create assets directory if it doesn't exist
assets_dir = 'assets'
if not os.path.exists(assets_dir):
    os.makedirs(assets_dir)

# Load a font
try:
    font = ImageFont.truetype("arial.ttf", FONT_SIZE)
except IOError:
    font = ImageFont.load_default()
    print("Custom font not found. Using default font.")

def create_tetromino_image(shape, color):
    img = Image.new('RGBA', IMAGE_SIZE, (0, 0, 0, 0))  # Transparent background
    draw = ImageDraw.Draw(img)

    # Draw a filled rectangle for the tetromino
    draw.rectangle([0, 0, BLOCK_SIZE, BLOCK_SIZE], fill=color)

    # Optionally, add the shape letter with shadow
    text = shape
    
    # Calculate text size using textbbox
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_x = (BLOCK_SIZE - text_width) / 2
    text_y = (BLOCK_SIZE - text_height) / 2

    # Draw shadow
    draw.text((text_x + 2, text_y + 2), text, font=font, fill=(0, 0, 0, 100))

    # Draw the main text
    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))

    # Save the image
    img.save(os.path.join(assets_dir, f'{shape}.png'))
    print(f'Created {shape}.png')

# Generate images for each shape
for shape, color in SHAPE_COLORS.items():
    create_tetromino_image(shape, color)

print("All tetromino images created successfully!")
