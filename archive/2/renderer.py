from PIL import Image, ImageDraw, ImageFont
import re

# Step 1: Define the CommandParser class
class CommandParser:
    def __init__(self):
        # Define regex patterns for each command
        self.patterns = {
            "draw": re.compile(r"draw (\d+),(\d+) (#[0-9a-fA-F]{6})"),
            "fill_rect": re.compile(r"fill_rect (\d+),(\d+),(\d+),(\d+) (#[0-9a-fA-F]{6})"),
            "draw_line": re.compile(r"draw_line (\d+),(\d+),(\d+),(\d+) (#[0-9a-fA-F]{6})"),
            "draw_circle": re.compile(r"draw_circle (\d+),(\d+),(\d+) (#[0-9a-fA-F]{6})"),
            "set_bg": re.compile(r"set_bg (#[0-9a-fA-F]{6})"),
            "fill_gradient": re.compile(r"fill_gradient (\d+),(\d+),(\d+),(\d+) (#[0-9a-fA-F]{6}),(#[0-9a-fA-F]{6})"),
            "draw_text": re.compile(r"draw_text (\d+),(\d+) (.+) (#[0-9a-fA-F]{6})"),
            "draw_polygon": re.compile(r"draw_polygon (.+) (#[0-9a-fA-F]{6})")
        }

    def parse(self, command_string):
        commands = []
        for cmd in command_string.strip().split(";"):
            cmd = cmd.strip()
            if not cmd:
                continue  # Skip empty commands

            # Try to match the command with each pattern
            parsed = None
            for cmd_type, pattern in self.patterns.items():
                match = pattern.match(cmd)
                if match:
                    parsed = {
                        "type": cmd_type,
                        "args": match.groups()
                    }
                    break

            if not parsed:
                raise ValueError(f"Invalid command: {cmd}")
            commands.append(parsed)

        return commands


# Step 2: Define the Renderer class
class Renderer:
    def __init__(self, width=100, height=100):
        self.width = width
        self.height = height
        self.image = Image.new("RGB", (width, height), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()  # Default font for text

    def execute_commands(self, parsed_commands):
        for cmd in parsed_commands:
            cmd_type = cmd["type"]
            args = cmd["args"]

            if cmd_type == "set_bg":
                self._set_background(args[0])
            elif cmd_type == "fill_rect":
                self._fill_rectangle(args)
            elif cmd_type == "draw_circle":
                self._draw_circle(args)
            elif cmd_type == "draw_line":
                self._draw_line(args)
            elif cmd_type == "draw":
                self._draw_pixel(args)
            elif cmd_type == "fill_gradient":
                self._fill_gradient(args)
            elif cmd_type == "draw_text":
                self._draw_text(args)
            elif cmd_type == "draw_polygon":
                self._draw_polygon(args)
            else:
                raise ValueError(f"Unknown command: {cmd_type}")

    def _set_background(self, color):
        self.draw.rectangle([0, 0, self.width, self.height], fill=color)

    def _fill_rectangle(self, args):
        x1, y1, x2, y2 = map(int, args[:4])
        color = args[4]
        self.draw.rectangle([x1, y1, x2, y2], fill=color)

    def _draw_circle(self, args):
        cx, cy, radius = map(int, args[:3])
        color = args[3]
        self.draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=color)

    def _draw_line(self, args):
        x1, y1, x2, y2 = map(int, args[:4])
        color = args[4]
        self.draw.line([x1, y1, x2, y2], fill=color)

    def _draw_pixel(self, args):
        x, y = map(int, args[:2])
        color = args[2]
        self.draw.point((x, y), fill=color)

    def _fill_gradient(self, args):
        x1, y1, x2, y2 = map(int, args[:4])
        color1, color2 = args[4], args[5]
        for i in range(y1, y2 + 1):
            ratio = (i - y1) / (y2 - y1)
            r = int((1 - ratio) * int(color1[1:3], 16) + ratio * int(color2[1:3], 16))
            g = int((1 - ratio) * int(color1[3:5], 16) + ratio * int(color2[3:5], 16))
            b = int((1 - ratio) * int(color1[5:7], 16) + ratio * int(color2[5:7], 16))
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.draw.line([x1, i, x2, i], fill=color)

    def _draw_text(self, args):
        x, y = map(int, args[:2])
        text = args[2]
        color = args[3]
        self.draw.text((x, y), text, fill=color, font=self.font)

    def _draw_polygon(self, args):
        points = list(map(int, args[0].split(",")))
        color = args[1]
        self.draw.polygon(points, fill=color)

    def show_image(self):
        self.image.show()

    def save_image(self, filename="output.png"):
        self.image.save(filename)


# Step 3: Test with example commands
if __name__ == "__main__":
    # Example commands
    command_string = """fill_gradient 0,0,100,50 #FF4500,#FF4500; draw_circle 50,20,15 #FFD700; """

    # Parse the commands
    parser = CommandParser()
    parsed_commands = parser.parse(command_string)

    # Render the image
    renderer = Renderer(width=100, height=100)
    renderer.execute_commands(parsed_commands)
    renderer.show_image()
    renderer.save_image("output.png")