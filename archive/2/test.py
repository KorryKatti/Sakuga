import re

class CommandParser:
    def __init__(self):
        # Define regex patterns for each command
        self.patterns = {
            "draw": re.compile(r"draw (\d+),(\d+) (#[0-9a-fA-F]{6})"),
            "fill_rect": re.compile(r"fill_rect (\d+),(\d+),(\d+),(\d+) (#[0-9a-fA-F]{6})"),
            "draw_line": re.compile(r"draw_line (\d+),(\d+),(\d+),(\d+) (#[0-9a-fA-F]{6})"),
            "draw_circle": re.compile(r"draw_circle (\d+),(\d+),(\d+) (#[0-9a-fA-F]{6})"),
            "set_bg": re.compile(r"set_bg (#[0-9a-fA-F]{6})")
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
    

# Example command string
command_string = """
set_bg #FFFFFF;
fill_rect 10,10,50,50 #0000FF;
draw_circle 75,75,25 #FF0000;
draw_line 0,0,100,100 #00FF00;
"""

# Parse the commands
parser = CommandParser()
parsed_commands = parser.parse(command_string)

# Print the parsed commands
for cmd in parsed_commands:
    print(cmd)

