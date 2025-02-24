from PIL import Image, ImageDraw
import math
import cv2
import numpy as np

def parse_command(command):
    parts = command.strip(';').split()
    color = parts[0]
    x1, y1, x2, y2, thickness = map(int, parts[1:])
    return color, (x1, y1, x2, y2), thickness

def draw_smooth_line(draw, coords, color, thickness):
    x1, y1, x2, y2 = coords
    num_points = max(abs(x2 - x1), abs(y2 - y1)) * 2  # More points for smoother curves
    points = [(x1 + (x2 - x1) * t / num_points, y1 + (y2 - y1) * t / num_points) for t in range(num_points + 1)]
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=color, width=thickness)

def process_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (512, 512))
    
    # Compute overall contrast
    contrast = np.std(img)
    
    if contrast > 50:
        # High contrast image - use Canny edge detection
        edges = cv2.Canny(img, 50, 150)
    else:
        # Low contrast image - use adaptive thresholding
        edges = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=40, minLineLength=5, maxLineGap=10)
    
    commands = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            thickness = int((255 - img[y1, x1]) / 255 * 5) + 1
            commands.append(f"black {x1} {y1} {x2} {y2} {thickness};")
    return commands

def render(commands, img_size=(512, 512)):
    img = Image.new("RGB", img_size, "white")
    draw = ImageDraw.Draw(img)
    for cmd in commands:
        color, coords, thickness = parse_command(cmd)
        draw_smooth_line(draw, coords, color, thickness)
    img.show()
    img.save("output.png")

if __name__ == "__main__":
    image_path = "input.png"  # Change this to your image path
    commands = process_image(image_path)
    
    # Save commands to a file in list format for direct pasting into renderer
    with open("commands.txt", "w") as f:
        f.write("[" + ", ".join(f'"{cmd}"' for cmd in commands) + "]")
    
    print("Commands saved to commands.txt in list format. You can manually paste them into the renderer.")
    render(commands)