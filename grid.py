import sys
import png
from pathlib import Path

LINE_WIDTH = 1
LINE_SPACE = 20

def add_grid_to_image(input_path):
    # Read the PNG file
    reader = png.Reader(filename=input_path)
    width, height, pixels, metadata = reader.read()
    
    # Convert pixels to a list of lists for easier manipulation
    pixel_data = list(pixels)
    
    # Determine if image has alpha channel
    planes = metadata['planes']  # 1=grayscale, 2=grayscale+alpha, 3=RGB, 4=RGBA
    
    # Draw horizontal lines
    for y in range(0, height, LINE_SPACE):
        for line_offset in range(LINE_WIDTH):
            if y + line_offset < height:
                row = pixel_data[y + line_offset]
                for x in range(width):
                    # Set pixel to black
                    if planes == 1:  # Grayscale
                        row[x] = 0
                    elif planes == 2:  # Grayscale + Alpha
                        row[x * 2] = 0
                        row[x * 2 + 1] = 255  # Full opacity
                    elif planes == 3:  # RGB
                        row[x * 3] = 0      # R
                        row[x * 3 + 1] = 0  # G
                        row[x * 3 + 2] = 0  # B
                    elif planes == 4:  # RGBA
                        row[x * 4] = 0      # R
                        row[x * 4 + 1] = 0  # G
                        row[x * 4 + 2] = 0  # B
                        row[x * 4 + 3] = 255  # A (full opacity)
    
    # Draw vertical lines
    for x in range(0, width, LINE_SPACE):
        for line_offset in range(LINE_WIDTH):
            if x + line_offset < width:
                for y in range(height):
                    row = pixel_data[y]
                    pixel_x = x + line_offset
                    # Set pixel to black
                    if planes == 1:  # Grayscale
                        row[pixel_x] = 0
                    elif planes == 2:  # Grayscale + Alpha
                        row[pixel_x * 2] = 0
                        row[pixel_x * 2 + 1] = 255
                    elif planes == 3:  # RGB
                        row[pixel_x * 3] = 0
                        row[pixel_x * 3 + 1] = 0
                        row[pixel_x * 3 + 2] = 0
                    elif planes == 4:  # RGBA
                        row[pixel_x * 4] = 0
                        row[pixel_x * 4 + 1] = 0
                        row[pixel_x * 4 + 2] = 0
                        row[pixel_x * 4 + 3] = 255
    
    # Generate output filename
    input_file = Path(input_path)
    output_filename = f"grid-{input_file.name}"
    output_path = input_file.parent / output_filename
    
    # Write the modified image
    with open(output_path, 'wb') as f:
        writer = png.Writer(width=width, height=height, **metadata)
        writer.write(f, pixel_data)
    
    print(f"Grid image saved as: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <image.png>")
        sys.exit(1)
    
    add_grid_to_image(sys.argv[1])
