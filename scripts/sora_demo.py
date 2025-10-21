import os

# Define output folder
output_folder = os.path.join("..", "assets", "demos")  # relative to scripts folder

# Create folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Define output file path
output_file = os.path.join(output_folder, "floating_rect_demo.mp4")

import os
import numpy as np
from moviepy.editor import VideoClip, ImageClip, TextClip, CompositeVideoClip
from PIL import Image

# === Paths ===
root = os.path.join(os.path.dirname(__file__), "..")
assets_dir = os.path.join(root, "assets", "demos")
os.makedirs(assets_dir, exist_ok=True)
background_path = os.path.join(assets_dir, "abstract_expressionist_rectangles.png")  # prepared image
output_path = os.path.join(assets_dir, "floating_rect_demo.mp4")

# === Constants ===
DURATION = 6          # seconds
FPS = 30              # frames per second
WIDTH, HEIGHT = 600, 600  # 1:1 aspect

# Load background image
bg_image = Image.open(background_path).resize((WIDTH, HEIGHT))

# Generate drifting rectangles & binary
np.random.seed(42)
num_rects = 20
rects = []
for _ in range(num_rects):
    rects.append({
        "x": np.random.uniform(0, WIDTH*0.8),
        "y": np.random.uniform(0, HEIGHT*0.8),
        "w": np.random.uniform(50, 120),
        "h": np.random.uniform(30, 80),
        "dx": np.random.uniform(-1, 1),
        "dy": np.random.uniform(-0.5, 0.5),
        "color": tuple(np.random.uniform(0.3,0.9,3))
    })

num_bin = 40
binaries = []
for _ in range(num_bin):
    binaries.append({
        "x": np.random.uniform(0, WIDTH),
        "y": np.random.uniform(0, HEIGHT),
        "text": ''.join(np.random.choice(['0','1'], size=5)),
        "dy": np.random.uniform(-0.5,0.5)
    })

# Frame generator
def make_frame(t):
    frame = np.array(bg_image).astype(np.uint8)

    # Draw rectangles with soft inner glow
    for r in rects:
        # Update position
        r["x"] += r["dx"]
        r["y"] += r["dy"]
        # Wrap around edges
        r["x"] %= WIDTH
        r["y"] %= HEIGHT
        x0, y0, x1, y1 = int(r["x"]), int(r["y"]), int(r["x"]+r["w"]), int(r["y"]+r["h"])
        # Overlay rectangle
        frame[y0:y1, x0:x1, :3] = (np.array(r["color"])*255*0.4 + frame[y0:y1, x0:x1, :3]*0.6).astype(np.uint8)

    # Draw binary code pulsing
    for b in binaries:
        b["y"] += b["dy"]
        b["y"] %= HEIGHT
        y_pos = int(b["y"])
        x_pos = int(b["x"])
        # Simple pulse by changing brightness
        frame[y_pos:y_pos+10, x_pos:x_pos+30, :] = np.clip(frame[y_pos:y_pos+10, x_pos:x_pos+30, :]+(np.sin(t*2*np.pi)*30),0,255)

    return frame

# Create video clip
clip = VideoClip(make_frame, duration=DURATION)
clip = clip.set_fps(FPS)

# Add headline & subtext
headline = TextClip("One Planet · Brain²", fontsize=40, font="Futura-Bold", color="black", size=(WIDTH, None))
subtext = TextClip("Join the Future of Intelligence", fontsize=20, font="Inter", color="black", size=(WIDTH, None))
copyright_text = TextClip("© 2025 Principia Lab", fontsize=12, font="Inter", color="black", size=(WIDTH, None))

# Position text
headline = headline.set_pos(("center", HEIGHT*0.05)).set_duration(DURATION)
subtext = subtext.set_pos(("center", HEIGHT*0.12)).set_duration(DURATION)
copyright_text = copyright_text.set_pos(("center", HEIGHT*0.92)).set_duration(DURATION)

# Combine
final = CompositeVideoClip([clip, headline, subtext, copyright_text])
final.write_videofile(output_path, fps=FPS, codec="libx264", audio=False, preset="medium", threads=4)
