import tkinter as tk
import math
import random

# Draw heart shape
def draw_heart(canvas, width, height, offset_y, scale):
    offset_x = width // 2
    points = []
    for t in range(0, 360):
        angle = math.radians(t)
        x = scale * 16 * math.sin(angle) ** 3
        y = -scale * (13 * math.cos(angle) - 5 * math.cos(2 * angle)
                      - 2 * math.cos(3 * angle) - math.cos(4 * angle))
        points.append((offset_x + x, offset_y + y))
    return canvas.create_line(points, fill="#ff3366", width=2, smooth=True)

# Glowing ring
def draw_glowing_ring(canvas, x, y, radius, layers=4):
    for i in range(layers):
        glow_radius = radius + i * 3
        canvas.create_oval(
            x - glow_radius, y - glow_radius,
            x + glow_radius, y + glow_radius,
            outline="#ffd700", width=1
        )

# Twinkling star class
class Star:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.size = random.randint(1, 3)
        self.brightness = random.choice(["#333333", "#666666", "#999999", "#ffffff"])
        self.id = canvas.create_oval(self.x, self.y, self.x+self.size, self.y+self.size, fill=self.brightness, outline="")

    def twinkle(self):
        self.brightness = random.choice(["#333333", "#666666", "#999999", "#ffffff"])
        self.canvas.itemconfig(self.id, fill=self.brightness)

# Main wedding card
def create_wedding_card():
    root = tk.Tk()
    root.title("Wedding Invitation")
    root.geometry("600x750")
    root.resizable(False, False)

    canvas = tk.Canvas(root, width=600, height=750, bg="#000000", highlightthickness=0)
    canvas.pack()

    # Create stars
    stars = [Star(canvas, 600, 750) for _ in range(80)]
    def twinkle_stars():
        for star in stars:
            star.twinkle()
        root.after(300, twinkle_stars)

    # Draw heart
    heart_scale = [5]
    heart_id = draw_heart(canvas, 600, 750, offset_y=130, scale=heart_scale[0])

    def beat_heart():
        nonlocal heart_id
        canvas.delete(heart_id)
        heart_scale[0] = 5 + 0.3 * math.sin(beat_heart.phase)
        heart_id = draw_heart(canvas, 600, 750, offset_y=130, scale=heart_scale[0])
        beat_heart.phase += 0.2
        root.after(100, beat_heart)
    beat_heart.phase = 0

    # Draw ring
    ring_x, ring_y = 300, 615
    draw_glowing_ring(canvas, ring_x, ring_y, radius=12)
    canvas.create_text(ring_x, ring_y, text="💍", font=("Arial", 20), fill="#ffd700")

    # Text content
    texts = [
        ("Wedding Invitation", 300, 220, ("Times New Roman", 28, "bold")),
        ("Aishaa", 300, 270, ("Brush Script MT", 36, "italic")),
        ("weds", 300, 310, ("Georgia", 16)),
        ("Javee", 300, 350, ("Brush Script MT", 36, "italic")),
        ("On the 12th of December, 2025", 300, 410, ("Georgia", 16)),
        ("At 6:00 PM", 300, 440, ("Georgia", 16)),
        ("Venue:", 300, 480, ("Georgia", 16)),
        ("Noor Mahal Wedding Hall\nChennai, Tamil Nadu", 300, 510, ("Georgia", 16)),
        ("With love & blessings,", 300, 560, ("Georgia", 16)),
        ("The Families of Aishaa & Javee", 300, 590, ("Georgia", 16)),
        ("“Two hearts, one soul, one promise forever…”", 300, 630, ("Georgia", 14, "italic"))
    ]

    def show_text(index):
        if index < len(texts):
            text, x, y, f = texts[index]
            canvas.create_text(x, y, text=text, font=f, fill="#800080")
            root.after(400, show_text, index + 1)

    # Save the Date button
    def on_save():
        print("💾 Save the Date clicked!")

    save_btn = tk.Button(root, text="💌 Save the Date", font=("Arial", 12, "bold"),
                         bg="#800080", fg="white", command=on_save)
    save_btn.place(x=230, y=680)

    show_text(0)
    twinkle_stars()
    beat_heart()
    root.mainloop()

create_wedding_card()
