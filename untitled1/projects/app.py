from flask import Flask, render_template, request
from PIL import Image, ImageDraw
import io
import base64
import math
import os
import subprocess
import platform
import tempfile

app = Flask(__name__)

def draw_polygon(sides, size):
    # Create a new image with a white background
    img_size = 400
    img = Image.new("RGBA", (img_size, img_size), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Calculate polygon vertices
    center = img_size // 2
    radius = size // 2
    points = []
    for i in range(sides):
        angle = 2 * math.pi * i / sides - math.pi / 2  # Start from top
        x = center + radius * math.cos(angle)
        y = center + radius * math.sin(angle)
        points.append((x, y))

    # Draw the polygon
    draw.polygon(points, outline="black", width=2)

    # Save image to a BytesIO buffer for display
    img_io = io.BytesIO()
    img.save(img_io, format="PNG")
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.getvalue()).decode()

    # Save image to a temporary file for printing
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        img.save(temp_file, format="PNG")
        temp_file_path = temp_file.name

    img.close()
    img_io.close()
    return img_base64, temp_file_path

def print_image(file_path):
    system = platform.system()
    try:
        if system == "Windows":
            os.startfile(file_path, "print")
        elif system in ["Linux", "Darwin"]:  # Darwin is macOS
            subprocess.run(["lp", file_path], check=True)  # Use 'lp' for Linux/macOS
        else:
            return f"Printing not supported on {system}"
        return None
    except Exception as e:
        return f"Printing failed: {str(e)}"
    finally:
        # Clean up the temporary file
        try:
            os.remove(file_path)
        except Exception:
            pass

@app.route('/', methods=['GET', 'POST'])
def index():
    img_data = None
    sides = 6
    size = 100
    error = None
    print_message = None

    if request.method == 'POST':
        action = request.form.get('action')
        try:
            sides = request.form.get('sides', '6')
            size = request.form.get('size', '100')
            sides = int(sides)
            size = float(size)

            # Validate inputs
            if sides < 3 or sides > 12:
                raise ValueError("Sides must be between 3 and 12")
            if size < 50 or size > 200:
                raise ValueError("Size must be between 50 and 200")

            # Generate the polygon image
            img_base64, temp_file_path = draw_polygon(sides, int(size))
            img_data = f"data:image/png;base64,{img_base64}"

            # Handle print action
            if action == "print" and img_data:
                print_message = print_image(temp_file_path)
            else:
                # Clean up temp file if not printing
                try:
                    os.remove(temp_file_path)
                except Exception:
                    pass

        except ValueError as e:
            error = str(e)
            img_data = None

    return render_template('index.html', img_data=img_data, sides=sides, size=size, error=error, print_message=print_message)

if __name__ == '__main__':
    app.run(debug=True)