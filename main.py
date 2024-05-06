from typer import Typer, Argument, Option
from PIL import Image
from pathlib import Path
from typing_extensions import Annotated
from rich import print

app = Typer(context_settings={"help_option_names": ['-h', '--help']})


@app.command()
def main(path: Annotated[str, Argument(help="Specify the path to the input image")] = "image.png",
         downscale: Annotated[int, Option("--downscale", "-d", "-D", help="Specify the downscale factor")] = 4,
         output_path: Annotated[
             str, Option("--output-path", "-o", "-O", help="Specify the path to the output file")] = None,
         print_in_console: Annotated[bool, Option("--console", "-c", "-C",
                                                  help="Specify whether to print in console or output file.")] = False):
    """
    CLI tool to generate ASCII art from image files.
    """
    image = Image.open(Path(path))
    width, height = [dimension // downscale for dimension in image.size]
    image = image.resize((width, height))
    pixels = image.load()
    output = []
    for y in range(height):
        output.append([])
        for x in range(width):
            brightness = sum(pixels[x, y])
            if brightness == 0:
                output[y].append(" ")
            elif 1 <= brightness < 100:
                output[y].append("'")
            elif 100 <= brightness < 200:
                output[y].append("(")
            elif 200 <= brightness < 300:
                output[y].append("/")
            elif 300 <= brightness < 400:
                output[y].append("+")
            elif 400 <= brightness < 500:
                output[y].append("*")
            elif 500 <= brightness < 600:
                output[y].append("&")
            elif 600 <= brightness < 700:
                output[y].append("%")
            elif 700 <= brightness < 750:
                output[y].append("X")
            else:
                output[y].append("#")
    if print_in_console:
        for row in output:
            print(''.join(row) + '\n')
    else:
        output_path = '.'.join([path.split('.')[0], 'txt']) if not output_path else output_path
        output_file = open(output_path, 'w')
        for row in output:
            output_file.write(''.join(row) + '\n')
        output_file.close()
        print(f"ASCII art saved as [bold green]{output_path}[/bold green]")


if __name__ == "__main__":
    app()
