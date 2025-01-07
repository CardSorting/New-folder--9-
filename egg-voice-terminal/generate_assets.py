from PIL import Image, ImageDraw, ImageFont
import os

# Create assets directory if it doesn't exist
os.makedirs('assets', exist_ok=True)

def create_logo(size, text, output_path):
    """Create a logo image with transparent background"""
    try:
        # Create gradient background
        base = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(base)
        
        # Draw gradient from blue to purple
        for i in range(size[1]):
            r = int(50 + 150 * i/size[1])
            g = int(50 + 50 * i/size[1])
            b = int(200 - 50 * i/size[1])
            draw.line((0, i, size[0], i), fill=(r, g, b, 255))
        
        # Load font
        try:
            font = ImageFont.truetype("arial.ttf", min(size)//2)
        except:
            font = ImageFont.load_default()
        
        # Calculate text position
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
        
        # Draw text with shadow
        shadow_offset = max(2, min(size)//50)
        draw.text((position[0]+shadow_offset, position[1]+shadow_offset), 
                 text, fill=(0, 0, 0, 128), font=font)
        draw.text(position, text, fill="white", font=font)
        
        # Add microphone icon if space allows
        if min(size) >= 44:
            try:
                mic = Image.open('assets/mic_icon.png').convert('RGBA')
                mic_size = min(size)//3
                mic = mic.resize((mic_size, mic_size))
                
                # Position icon to the right of text
                icon_x = position[0] + text_width + 10
                icon_y = position[1] + (text_height - mic_size)//2
                
                # Composite icon onto base image
                base.paste(mic, (icon_x, icon_y), mic)
            except Exception as e:
                print(f"Couldn't add microphone icon: {str(e)}")
        
        img = base
        
        # Verify image has content before saving
        if img.getbbox() is None:
            raise ValueError("Generated image is empty")
            
        # Save with explicit format and compression
        img.save(output_path, format='PNG', compress_level=9)
        
        # Verify file was written
        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            raise IOError("Failed to write image file")
            
    except Exception as e:
        print(f"Error creating {output_path}: {str(e)}")
        raise

def generate_assets():
    # Get absolute path to assets directory
    assets_dir = os.path.abspath('assets')
    print(f"Assets directory: {assets_dir}")
    
    # Verify assets directory exists
    if not os.path.exists(assets_dir):
        print(f"Creating assets directory: {assets_dir}")
        os.makedirs(assets_dir)
    
    # Create required logo assets with absolute paths
    create_logo((44, 44), 'EV', os.path.join(assets_dir, 'Square44x44Logo.png'))
    create_logo((150, 150), 'EV', os.path.join(assets_dir, 'Square150x150Logo.png'))
    create_logo((310, 150), 'Egg Voice', os.path.join(assets_dir, 'Wide310x150Logo.png'))
    
    print("Generated Windows Store logo assets")

if __name__ == '__main__':
    generate_assets()
