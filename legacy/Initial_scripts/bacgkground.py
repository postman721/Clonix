from PIL import Image, ImageDraw
import os

# Define image properties
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 700
BACKGROUND_COLOR = (30, 30, 30)  # Dark gray

# Create assets directory if it doesn't exist
assets_dir = 'assets'
if not os.path.exists(assets_dir):
    os.makedirs(assets_dir)

def create_background_image():
    img = Image.new('RGB', (SCREEN_WIDTH, SCREEN_HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Add a simple pattern (e.g., grid lines)
    grid_color = (50, 50, 50)
    grid_spacing = 50
    for x in range(0, SCREEN_WIDTH, grid_spacing):
        draw.line([(x, 0), (x, SCREEN_HEIGHT)], fill=grid_color)
    for y in range(0, SCREEN_HEIGHT, grid_spacing):
        draw.line([(0, y), (SCREEN_WIDTH, y)], fill=grid_color)
    
    # Save the image
    img.save(os.path.join(assets_dir, 'background.png'))
    print('Created background.png')

# Generate the background image
create_background_image()
print("Background image created successfully!")

