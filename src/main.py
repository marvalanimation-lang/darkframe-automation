
from PIL import Image, ImageDraw
import os

WIDTH = 720
HEIGHT = 1280
FPS = 24
DURATION = 48

os.makedirs("output", exist_ok=True)

def draw_stickman(draw, x, y, pose="normal"):
    # Head
    draw.ellipse((x-35, y-130, x+35, y-60),
                 outline="black", width=8)

    # Body
    draw.line((x, y-60, x, y+80),
              fill="black", width=9)

    # Arms
    if pose == "cool":
        draw.line((x, y-30, x-75, y-85),
                  fill="black", width=8)
        draw.line((x, y-30, x+75, y-85),
                  fill="black", width=8)
    else:
        draw.line((x, y-30, x-65, y+20),
                  fill="black", width=8)
        draw.line((x, y-30, x+65, y+20),
                  fill="black", width=8)

    # Legs
    draw.line((x, y+80, x-55, y+160),
              fill="black", width=9)
    draw.line((x, y+80, x+55, y+160),
              fill="black", width=9)

def make_frame(second):
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)

    x = WIDTH // 2
    y = 520

    pose = "cool" if second < 20 else "normal"

    if 20 <= second < 35:
        x += int(120 * ((second % 2) - 1))

    if second >= 35:
        y += 100

    draw_stickman(draw, x, y, pose)

    message = (
        "WATCH ME!" if second < 20
        else "OOPS!" if second < 35
        else "I MEANT TO DO THAT!"
    )

    draw.text((150, 150), message, fill="black")

    return image

def main():
    for second in range(DURATION):
        frame = make_frame(second)
        frame.save(f"output/frame_{second:03d}.png")

    print("48 scene frames created successfully!")

if __name__ == "__main__":
    main()
  
