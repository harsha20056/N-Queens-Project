"""
N-Queens: Diagram & Visual Asset Generator
Subject: Artificial Intelligence | Unit II: Search & Optimization (CO2)

This script generates visual diagrams (Architecture Flowchart, Visual Chessboards,
and UI mockup graphics) using Matplotlib and Pillow for inclusion in the
presentation and documentation.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


def generate_architecture_flowchart(save_path: str = "screenshots/architecture_flowchart.png"):
    """
    Generates a high-resolution, publication-quality architecture flowchart.
    """
    os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_facecolor("#F8FAFC")
    fig.patch.set_facecolor("#FFFFFF")

    # Define box helper
    def draw_box(x, y, w, h, text, bg_color, border_color, text_color="white", subtitle=""):
        rect = patches.FancyBboxPatch(
            (x - w/2, y - h/2), w, h,
            boxstyle="round,pad=0.25,rounding_size=0.15",
            facecolor=bg_color, edgecolor=border_color, linewidth=2, zorder=3
        )
        ax.add_patch(rect)
        if subtitle:
            ax.text(x, y + 0.12, text, ha="center", va="center", color=text_color,
                    fontsize=11, fontweight="bold", zorder=4)
            ax.text(x, y - 0.14, subtitle, ha="center", va="center", color=text_color,
                    fontsize=8.5, alpha=0.9, zorder=4)
        else:
            ax.text(x, y, text, ha="center", va="center", color=text_color,
                    fontsize=10.5, fontweight="bold", zorder=4)

    def draw_arrow(x1, y1, x2, y2, label=""):
        ax.annotate(
            "", xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(arrowstyle="->", color="#475569", lw=2, mutation_scale=15),
            zorder=2
        )
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mx, my + 0.1, label, ha="center", va="bottom", fontsize=8.5,
                    fontweight="bold", color="#334155",
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#CBD5E1", alpha=0.9))

    # Flowchart Nodes
    # 1. Start / User Input
    draw_box(2.0, 7.0, 3.0, 0.9, "User Input & Configuration", "#0F172A", "#1E293B",
             subtitle="Select N (4..15) & Algorithm Choice")

    # Dispatcher
    draw_box(2.0, 5.0, 2.6, 0.8, "Algorithm Dispatcher", "#334155", "#475569",
             subtitle="Input Validation & Setup")
    draw_arrow(2.0, 6.55, 2.0, 5.4, "")

    # Branch 1: Backtracking (Left Path)
    draw_box(6.0, 6.2, 3.4, 0.9, "Backtracking (DFS Search)", "#2563EB", "#1D4ED8",
             subtitle="Systematic Column-by-Column Placement")
    draw_box(10.0, 6.2, 3.2, 0.85, "Constraint Safety Check", "#1E40AF", "#1E3A8A",
             subtitle="Row & Diagonal Conflict Test O(1)")
    draw_box(10.0, 4.6, 3.2, 0.85, "Goal / Backtrack Decision", "#1D4ED8", "#172554",
             subtitle="Col == N ? Solved : Undo Placement")

    draw_arrow(3.3, 5.2, 4.3, 6.2, "Backtracking")
    draw_arrow(7.7, 6.2, 8.4, 6.2, "Candidate Row")
    draw_arrow(10.0, 5.77, 10.0, 5.02, "Valid")
    draw_arrow(8.4, 4.6, 7.7, 5.8, "Dead End / Backtrack")

    # Branch 2: Hill Climbing (Min-Conflicts)
    draw_box(6.0, 3.2, 3.4, 0.9, "Hill Climbing (Min-Conflicts)", "#059669", "#047857",
             subtitle="Random Initial State (1 Queen/Col)")
    draw_box(10.0, 3.2, 3.2, 0.85, "Min-Conflicts Local Repair", "#047857", "#064E3B",
             subtitle="Pick Conflicted Queen -> Move to Min Row")
    draw_box(10.0, 1.6, 3.2, 0.85, "Restarts & Plateau Logic", "#D97706", "#B45309",
             subtitle="If Max Steps Exceeded -> Random Restart")

    draw_arrow(3.3, 4.8, 4.3, 3.2, "Hill Climbing")
    draw_arrow(7.7, 3.2, 8.4, 3.2, "Calculate Conflicts")
    draw_arrow(10.0, 2.77, 10.0, 2.02, "Plateau / Loop")
    draw_arrow(8.4, 1.6, 6.0, 2.75, "New Random Board")

    # Common Convergence: Benchmark & Visual Presentation
    draw_box(14.0, 4.7, 3.2, 1.0, "Streamlit Web UI", "#7C3AED", "#6D28D9",
             subtitle="Interactive ♛ Chessboard & Metrics")
    draw_box(14.0, 2.7, 3.2, 1.0, "Performance Benchmark", "#DC2626", "#B91C1C",
             subtitle="Time, Success Rate & Restarts Charts")

    draw_arrow(11.6, 4.6, 12.4, 4.7, "0 Conflicts Found")
    draw_arrow(11.6, 3.2, 12.4, 4.5, "0 Conflicts Found")
    draw_arrow(14.0, 4.2, 14.0, 3.2, "Benchmark Trigger")

    ax.set_xlim(0, 16.5)
    ax.set_ylim(0.5, 8.0)
    ax.axis("off")
    ax.set_title("System Architecture & Algorithm Workflow: N-Queens Solver",
                 fontsize=16, fontweight="bold", color="#0F172A", pad=20)

    fig.tight_layout()
    fig.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Generated architecture flowchart at {save_path}")


def generate_visual_chessboard(board: list, n: int, title: str, save_path: str):
    """
    Renders an elegant chessboard image with queen pieces.
    """
    os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 6), dpi=300)
    ax.set_facecolor("#FFFFFF")
    fig.patch.set_facecolor("#FFFFFF")

    # Colors
    light_sq = "#F0D9B5"
    dark_sq = "#B58863"

    for r in range(n):
        for c in range(n):
            color = light_sq if (r + c) % 2 == 0 else dark_sq
            rect = patches.Rectangle((c, n - 1 - r), 1, 1, facecolor=color, edgecolor="#64748B", linewidth=0.5)
            ax.add_patch(rect)

            # Draw Queen symbol
            if board[c] == r:
                ax.text(c + 0.5, n - 1 - r + 0.48, "♛", ha="center", va="center",
                        fontsize=int(220 / n), color="#1E293B", fontweight="bold")

    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_xticks(np.arange(0.5, n, 1))
    ax.set_yticks(np.arange(0.5, n, 1))
    col_labels = [chr(ord('A') + i) for i in range(n)]
    row_labels = [str(n - i) for i in range(n)]
    ax.set_xticklabels(col_labels, fontsize=9, fontweight="bold", color="#334155")
    ax.set_yticklabels(row_labels, fontsize=9, fontweight="bold", color="#334155")
    ax.tick_params(length=0)

    plt.title(title, fontsize=13, fontweight="bold", color="#0F172A", pad=12)
    fig.tight_layout()
    fig.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Generated visual chessboard at {save_path}")


def generate_all_diagram_assets():
    """Generates all diagram and board screenshots."""
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)

    # 1. Architecture Flowchart
    generate_architecture_flowchart(os.path.join(screenshots_dir, "architecture_flowchart.png"))

    # 2. 8-Queens standard solution board
    board_8 = [0, 4, 7, 5, 2, 6, 1, 3]  # Valid 8-queens solution
    generate_visual_chessboard(board_8, 8, "8-Queens Valid Placement (Backtracking Solution)",
                               os.path.join(screenshots_dir, "chessboard_n8.png"))

    # 3. 4-Queens solution board
    board_4 = [1, 3, 0, 2]  # Valid 4-queens solution
    generate_visual_chessboard(board_4, 4, "4-Queens Valid Placement (Min-Conflicts Solution)",
                               os.path.join(screenshots_dir, "chessboard_n4.png"))


if __name__ == "__main__":
    generate_all_diagram_assets()
