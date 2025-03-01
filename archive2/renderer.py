from PIL import Image, ImageDraw
import math

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

def render(commands, img_size=(512, 512)):
    img = Image.new("RGB", img_size, "white")
    draw = ImageDraw.Draw(img)
    for cmd in commands:
        color, coords, thickness = parse_command(cmd)
        draw_smooth_line(draw, coords, color, thickness)
    img.show()
    img.save("output.png")

if __name__ == "__main__":
    commands = ["black 302 228 318 278 1;", "black 386 410 401 428 1;", "black 319 308 374 378 1;", "black 324 88 342 59 3;", "black 254 239 285 285 1;", "black 317 334 343 308 2;", "black 160 62 178 92 3;", "black 254 153 303 104 3;"]
    render(commands)
