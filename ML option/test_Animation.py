import tkinter as tk
from PIL import Image, ImageTk
import itertools

class AnimatedOrb:
    def __init__(self, root):
        self.root = root
        self.root.title("VANI - Siri Style Animation")
        self.root.geometry("500x500")
        self.root.config(bg="#0b002b")

        # Load orb frames
        self.frames = [ImageTk.PhotoImage(file=f"orb/anim_{i}.png") for i in range(1, 16)]  # Total 15 frames
        self.frame_iter = itertools.cycle(self.frames)

        # Canvas to hold animation
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="#0b002b", highlightthickness=0)
        self.canvas.pack(expand=True)

        self.image_id = self.canvas.create_image(200, 200, image=next(self.frame_iter))
        self.animate()

    def animate(self):
        frame = next(self.frame_iter)
        self.canvas.itemconfig(self.image_id, image=frame)
        self.root.after(100, self.animate)  # Adjust speed here (lower = faster)

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimatedOrb(root)
    root.mainloop()
