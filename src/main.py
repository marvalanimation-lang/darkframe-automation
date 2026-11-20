
from PIL import Image, ImageDraw
import os
import subprocess
import math
import shutil

W, H = 450, 800
FPS = 15
DURATION = 48

OUT = "output"
FRAMES = f"{OUT}/frames"

os.makedirs(FRAMES, exist_ok=True)

def draw_frame(t):
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)

    # Scene animation
    if t < 15:
        x = 225 + int(70 * math.sin(t * 2))
        title = "WATCH ME!"
    elif t < 30:
        x = 225 + int(100 * math.sin(t * 4))
        title = "OOPS!"
    else:
        x = 225
        title = "I MEANT TO DO THAT!"

    y = 350 if t < 30 else 400

    # Head
    d.ellipse((x-28, y-120, x+28, y-64),
              outline="black", width=6)

    # Sunglasses
    if t < 15:
        d.line((x-24, y-95, x+24, y-95),
               fill="black", width=7)

    # Body
    d.line((x, y-64, x, y+65),
           fill="black", width=7)

    # Arms
    arm = int(35 * math.sin(t * 3))
    d.line((x, y-35, x-55, y+arm),
           fill="black", width=6)
    d.line((x, y-35, x+55, y-arm),
           fill="black", width=6)

    # Legs
    d.line((x, y+65, x-40, y+125),
           fill="black", width=7)
    d.line((x, y+65, x+40, y+125),
           fill="black", width=7)

    d.text((90, 100), title, fill="black", stroke_width=1)

    return im

def main():
    for i in range(FPS * DURATION):
        t = i / FPS
        frame = draw_frame(t)
        frame.save(f"{FRAMES}/frame_{i:05d}.jpg", quality=85)

    subprocess.run([
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", f"{FRAMES}/frame_%05d.jpg",
        "-vf", "scale=720:1280",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        f"{OUT}/darkframe_short.mp4"
    ], check=True)

    shutil.rmtree(FRAMES)
    print("MP4 render completed!")

if __name__ == "__main__":
    main()
    
