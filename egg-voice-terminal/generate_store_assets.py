from PIL import Image, ImageDraw
import os

def create_store_logo(size):
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((0, 0, size[0], size[1]), fill='#0078D7')
    return img

def create_splash_screen():
    size = (620, 300)
    img = Image.new('RGB', size, '#0078D7')
    draw = ImageDraw.Draw(img)
    text = "Egg Voice Terminal"
    draw.text((50, 100), text, fill="white")
    return img

def main():
    assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
    
    # Create store assets
    logo_sizes = {
        'StoreLogo.png': (50, 50),
        'Square71x71Logo.png': (71, 71),
        'Square310x310Logo.png': (310, 310)
    }
    
    for filename, size in logo_sizes.items():
        logo = create_store_logo(size)
        logo_path = os.path.join(assets_dir, filename)
        logo.save(logo_path)
    
    # Create SplashScreen.png
    splash_screen = create_splash_screen()
    splash_screen_path = os.path.join(assets_dir, 'SplashScreen.png')
    splash_screen.save(splash_screen_path)
    
    print(f"Generated store assets at {assets_dir}")

if __name__ == '__main__':
    main()
