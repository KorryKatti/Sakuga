import argparse
from renderer import CommandParser, Renderer
from train_ai_model import generate_commands

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="AI Image Generator CLI")
    parser.add_argument("prompt", type=str, help="Text prompt for the image (e.g., 'A beach with golden sand and a bright sun')")
    parser.add_argument("--width", type=int, default=100, help="Width of the output image (default: 100)")
    parser.add_argument("--height", type=int, default=100, help="Height of the output image (default: 100)")
    parser.add_argument("--output", type=str, default="output.png", help="Output file name (default: output.png)")
    parser.add_argument("--show", action="store_true", help="Display the generated image")

    # Parse arguments
    args = parser.parse_args()

    # Generate commands from the prompt
    print(f"Generating commands for: {args.prompt}")
    commands = generate_commands(args.prompt)
    print("Generated Commands:")
    print(commands)

    # Parse and render the commands
    parser = CommandParser()
    renderer = Renderer(width=args.width, height=args.height)

    try:
        parsed_commands = parser.parse(commands)
        renderer.execute_commands(parsed_commands)
        renderer.save_image(args.output)
        print(f"Image saved to {args.output}")

        # Display the image if requested
        if args.show:
            renderer.show_image()
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()



### usage python cli_app.py "A beach with waves and clear sky with sun" --width 200 --height 200 --output beach.png --show