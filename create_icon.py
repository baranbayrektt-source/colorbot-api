"""
QUARXV1 Icon Creator
Creates a professional icon for QUARXV1 ColorBot
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_quarxv1_icon():
    """Create QUARXV1 icon"""
    
    # Icon size (Windows standard)
    size = (256, 256)
    
    # Create image with dark background
    img = Image.new('RGBA', size, (20, 20, 30, 255))
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    for y in range(size[1]):
        alpha = int(255 * (1 - y / size[1] * 0.3))
        color = (30, 30, 50, alpha)
        draw.line([(0, y), (size[0], y)], fill=color)
    
    # Draw outer circle
    center = (size[0] // 2, size[1] // 2)
    radius = 100
    
    # Outer glow
    for r in range(radius + 10, radius - 5, -2):
        alpha = int(100 * (1 - (r - radius + 5) / 15))
        color = (100, 50, 200, alpha)
        draw.ellipse([center[0] - r, center[1] - r, center[0] + r, center[1] + r], 
                    outline=color, width=2)
    
    # Main circle
    draw.ellipse([center[0] - radius, center[1] - radius, 
                  center[0] + radius, center[1] + radius], 
                 outline=(150, 80, 255, 255), width=3)
    
    # Inner circle
    inner_radius = 70
    draw.ellipse([center[0] - inner_radius, center[1] - inner_radius,
                  center[0] + inner_radius, center[1] + inner_radius],
                 outline=(200, 120, 255, 255), width=2)
    
    # Crosshair lines
    line_length = 40
    line_width = 3
    
    # Horizontal line
    draw.line([(center[0] - line_length, center[1]), 
               (center[0] + line_length, center[1])], 
              fill=(255, 255, 255, 255), width=line_width)
    
    # Vertical line
    draw.line([(center[0], center[1] - line_length), 
               (center[0], center[1] + line_length)], 
              fill=(255, 255, 255, 255), width=line_width)
    
    # Center dot
    dot_radius = 4
    draw.ellipse([center[0] - dot_radius, center[1] - dot_radius,
                  center[0] + dot_radius, center[1] + dot_radius],
                 fill=(255, 255, 255, 255))
    
    # QUARXV1 text
    try:
        # Try to use a system font
        font_large = ImageFont.truetype("arial.ttf", 32)
        font_small = ImageFont.truetype("arial.ttf", 16)
    except:
        # Fallback to default font
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # QUARXV1 text
    text = "QUARXV1"
    text_bbox = draw.textbbox((0, 0), text, font=font_large)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = center[0] - text_width // 2
    text_y = center[1] + radius + 10
    
    # Text shadow
    draw.text((text_x + 2, text_y + 2), text, font=font_large, fill=(0, 0, 0, 150))
    
    # Main text
    draw.text((text_x, text_y), text, font=font_large, fill=(255, 255, 255, 255))
    
    # Subtitle
    subtitle = "ColorBot"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_small)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    
    subtitle_x = center[0] - subtitle_width // 2
    subtitle_y = text_y + text_height + 5
    
    draw.text((subtitle_x, subtitle_y), subtitle, font=font_small, fill=(200, 200, 200, 255))
    
    # Save as ICO
    img.save("quarxv1.ico", format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    
    # Also save as PNG for preview
    img.save("quarxv1_icon.png", format='PNG')
    
    print("✅ QUARXV1 icon created successfully!")
    print("📁 Files created:")
    print("   - quarxv1.ico (Windows icon)")
    print("   - quarxv1_icon.png (Preview)")

if __name__ == "__main__":
    create_quarxv1_icon()
