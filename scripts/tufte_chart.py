# File: scripts/export_tufte_chart.py

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

def export_tradeoff_chart(materials, property1, property2, assets_dir=None,
                          mp4_name="tufte_tradeoff_chart.mp4",
                          gif_name="tufte_tradeoff_chart.gif"):
    """Export Tufte-style tradeoff chart as MP4 and GIF."""

    # --- Setup assets folder ---
    if assets_dir is None:
        assets_dir = Path(__file__).resolve().parent.parent / "assets"
    assets_dir.mkdir(exist_ok=True)
    (assets_dir / ".gitkeep").touch(exist_ok=True)

    mp4_path = assets_dir / mp4_name
    gif_path = assets_dir / gif_name

    # --- Shared parameters ---
    x = np.arange(len(materials))
    width = 0.35

    # --- Animation function ---
    def animate(frame, bars1, bars2, prop1, prop2):
        for b1, s1, b2, s2 in zip(bars1, prop1, bars2, prop2):
            b1.set_height(min(s1, s1*(frame/20)))
            b2.set_height(min(s2, s2*(frame/20)))
        return bars1 + bars2

    # --- MP4 Figure ---
    fig_mp4, ax_mp4 = plt.subplots(figsize=(8,5))
    bars1_mp4 = ax_mp4.bar(x - width/2, [0]*len(property1), width, label="Property 1", color="#2b7a2b")
    bars2_mp4 = ax_mp4.bar(x + width/2, [0]*len(property2), width, label="Property 2", color="#38a3a5")

    for ax in [ax_mp4]:
        ax.set_ylim(0, max(max(property1), max(property2)) + 2)
        ax.set_xticks(x)
        ax.set_xticklabels(materials)
        ax.set_facecolor('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('#777')
        ax.tick_params(left=False, bottom=False)
        ax.set_ylabel("Score")
        ax.set_title("Top Materials – Tufte-style Tradeoff Chart")
        ax.legend(frameon=False)

    ani_mp4 = FuncAnimation(fig_mp4, animate,
                            fargs=(bars1_mp4, bars2_mp4, property1, property2),
                            frames=21, interval=100, blit=False, repeat=False)
    ani_mp4.save(mp4_path, writer="ffmpeg", fps=24)

    # --- GIF Figure ---
    fig_gif, ax_gif = plt.subplots(figsize=(6,4))
    bars1_gif = ax_gif.bar(x - width/2, [0]*len(property1), width, color="#2b7a2b")
    bars2_gif = ax_gif.bar(x + width/2, [0]*len(property2), width, color="#38a3a5")

    for ax in [ax_gif]:
        ax.set_ylim(0, max(max(property1), max(property2)) + 2)
        ax.set_xticks(x)
        ax.set_xticklabels(materials)
        ax.set_facecolor('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('#777')
        ax.tick_params(left=False, bottom=False)
        ax.set_ylabel("Score")
        ax.set_title("Top Materials – Tufte-style Tradeoff Chart")

    ani_gif = FuncAnimation(fig_gif, animate,
                            fargs=(bars1_gif, bars2_gif, property1, property2),
                            frames=21, interval=100, blit=False, repeat=False)
    ani_gif.save(gif_path, writer="pillow", fps=10)

    print(f"✅ Export complete:\n  {mp4_path}\n  {gif_path}")


# === Example usage ===
if __name__ == "__main__":
    materials = ["Material A", "Material B", "Material C", "Material D", "Material E"]
    property1 = [8.5, 7.2, 9.0, 6.5, 7.8]
    property2 = [5.5, 6.2, 4.0, 6.5, 5.8]

    export_tradeoff_chart(materials, property1, property2)
