import tkinter as tk
import tkinter.messagebox as messagebox
import random

class NikahApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Our Eternal Nikah")
        self.root.geometry("800x600")

        # Canvas Setup
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()

        # Deep blue sky background
        self.canvas.create_rectangle(0, 0, 800, 600, fill="#1B263B", outline="")  # Deep blue sky

        # Smaller Masjid silhouette (lower-left quadrant)
        self.canvas.create_rectangle(100, 400, 300, 500, fill="#FFD700", outline="")  # Gold main structure
        self.canvas.create_arc(150, 350, 250, 450, start=0, extent=180, fill="#FFD700", outline="")  # Central dome
        self.canvas.create_rectangle(80, 350, 100, 450, fill="#FFD700", outline="")  # Left minaret
        self.canvas.create_rectangle(300, 350, 320, 450, fill="#FFD700", outline="")  # Right minaret
        self.canvas.create_oval(75, 340, 105, 360, fill="#C0C0C0", outline="")  # Left minaret top
        self.canvas.create_oval(295, 340, 325, 360, fill="#C0C0C0", outline="")  # Right minaret top
        self.canvas.create_arc(175, 420, 225, 470, start=0, extent=180, fill="#0B3D3D", outline="")  # Teal arch

        # Subtle crescent moon accents in upper canvas
        for _ in range(5):
            x = random.randint(50, 750)
            y = random.randint(50, 200)
            self.canvas.create_oval(x, y, x+10, y+10, fill="#C0C0C0", outline="")  # Small silver crescents

        # Nikah details labels next to masjid with semi-transparent background
        self.nikah_text_ids = []
        self.canvas.create_rectangle(350, 370, 650, 490, fill="#FFFFFF", stipple="gray50", outline="", tags="nikah_background")
        self.nikah_text_ids.append(self.canvas.create_text(500, 400, text="Date: Next Friday", fill="#E0115F", font=("Arial", 20, "bold")))
        self.nikah_text_ids.append(self.canvas.create_text(500, 430, text="Time: After Maghrib prayer", fill="#E0115F", font=("Arial", 20, "bold")))
        self.nikah_text_ids.append(self.canvas.create_text(500, 460, text="Imam: Sheikh Abdul Rahman", fill="#E0115F", font=("Arial", 20, "bold")))

        # Romantic kiss button
        self.button = tk.Button(self.root, text="SEAL OUR LOVE WITH A KISS", command=self.propose, bg="#E0115F", fg="#FFFFFF")
        self.button.pack()

        # List to store firework objects
        self.fireworks = []

        # Nasheed lyrics
        self.nasheed_lines = [
            "Tala'al Badru Alayna",
            "Min Thaniyati Al-Wada",
            "Wajaba Al-Shukru Alayna",
            "Ma Da'a Lillahi Da"
        ]
        self.nasheed_text_ids = []

    def create_firework(self, x, y, size, color):
        """Create a single firework oval and return its ID"""
        return self.canvas.create_oval(
            x - size, y - size, x + size, y + size,
            fill=color, outline=""
        )

    def animate_firework(self, firework_id, size, alpha, step=0):
        """Animate a firework: grow and fade"""
        if step > 20 or alpha <= 0:
            self.canvas.delete(firework_id)
            self.fireworks.remove(firework_id)
            return
        size += 2
        alpha -= 0.05
        self.canvas.coords(firework_id,
                           self.canvas.coords(firework_id)[0] - 2,
                           self.canvas.coords(firework_id)[1] - 2,
                           self.canvas.coords(firework_id)[2] + 2,
                           self.canvas.coords(firework_id)[3] + 2)
        self.root.after(50, self.animate_firework, firework_id, size, alpha, step + 1)

    def draw_boy_girl(self):
        """Draw stylized representations of a boy and a girl"""
        # Boy (left side)
        self.canvas.create_oval(320, 100, 360, 140, fill="#FFD700", outline="")  # Gold face
        self.canvas.create_rectangle(315, 90, 365, 110, fill="#2ECC71", outline="")  # Green cap
        self.canvas.create_rectangle(325, 140, 355, 200, fill="#00B7EB", outline="")  # Blue tunic
        self.canvas.create_line(325, 150, 310, 170, fill="#FFD700", width=3)  # Left arm
        self.canvas.create_line(355, 150, 370, 170, fill="#FFD700", width=3)  # Right arm
        self.canvas.create_line(335, 200, 335, 230, fill="#0B3D3D", width=3)  # Left leg
        self.canvas.create_line(345, 200, 345, 230, fill="#0B3D3D", width=3)  # Right leg

        # Girl (right side)
        self.canvas.create_oval(440, 100, 480, 140, fill="#FFB6C1", outline="")  # Rose face
        self.canvas.create_oval(435, 95, 485, 145, fill="#E0115F", outline="")  # Ruby hijab
        self.canvas.create_oval(445, 105, 475, 135, fill="#FFB6C1", outline="")  # Face cutout
        self.canvas.create_rectangle(445, 140, 475, 200, fill="#9B59B6", outline="")  # Purple dress
        self.canvas.create_line(445, 150, 430, 170, fill="#FFB6C1", width=3)  # Left arm
        self.canvas.create_line(475, 150, 490, 170, fill="#FFB6C1", width=3)  # Right arm
        self.canvas.create_line(455, 200, 455, 230, fill="#0B3D3D", width=3)  # Single leg

        # Heart between them
        heart_points = [
            400, 130, 410, 120, 420, 130,  # Top curves
            420, 140, 415, 150, 400, 160,   # Bottom right
            385, 150, 380, 140               # Bottom left
        ]
        self.canvas.create_polygon(heart_points, fill="#FF69B4", outline="", smooth=True)

        # Romantic text
        self.canvas.create_text(400, 250, text="Together Forever", fill="#E0115F", font=("Arial", 20, "italic"))

    def display_nasheed(self, line_index=0):
        """Display nasheed lyrics line by line with semi-transparent background"""
        if line_index >= len(self.nasheed_lines):
            return
        for text_id in self.nasheed_text_ids:
            self.canvas.delete(text_id)
        self.nasheed_text_ids.clear()
        # Add semi-transparent background for nasheed lyrics
        self.canvas.create_rectangle(300, 260 + line_index * 30, 500, 290 + line_index * 30,
                                     fill="#FFFFFF", stipple="gray50", outline="", tags="nasheed_background")
        for i in range(line_index + 1):
            text_id = self.canvas.create_text(
                400, 270 + i * 30, text=self.nasheed_lines[i],
                fill="#FFD700", font=("Arial", 18, "bold")  # Gold for better visibility
            )
            self.nasheed_text_ids.append(text_id)
        self.root.after(1000, self.display_nasheed, line_index + 1)

    def romantic_kiss(self):
        # Clear Nikah details text and background
        for text_id in self.nikah_text_ids:
            self.canvas.delete(text_id)
        self.nikah_text_ids.clear()
        self.canvas.delete("nikah_background")

        # Draw boy and girl representation in place of Nikah details
        self.draw_boy_girl()

        # Add fireworks with vibrant colors
        colors = ["#FF4500", "#FFD700", "#2ECC71", "#00B7EB", "#E0115F", "#9B59B6"]  # Orange, gold, emerald, blue, ruby, purple
        for _ in range(5):
            x = random.randint(200, 600)
            y = random.randint(50, 200)
            size = random.randint(5, 15)
            color = random.choice(colors)
            firework_id = self.create_firework(x, y, size, color)
            self.fireworks.append(firework_id)
            self.animate_firework(firework_id, size, 1.0)

        # Start nasheed lyrics display
        self.display_nasheed()

    def propose(self):
        response = messagebox.askyesno("Proposal", "Will you marry me and make this Nikah eternal?")
        if response:
            self.romantic_kiss()  # Trigger boy/girl representation, fireworks, and nasheed if accepted
        else:
            self.canvas.create_text(400, 320, text="Maybe another time...", fill="#FFFFFF", font=("Arial", 24, "bold"))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = NikahApp()
    app.run()