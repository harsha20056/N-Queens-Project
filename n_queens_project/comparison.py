"""
N-Queens: Performance Comparison & Benchmark Analysis
Subject: Artificial Intelligence | Unit II: Search & Optimization (CO2)

This module benchmarks Backtracking and Hill Climbing (Min-Conflicts) across
different N values (default: 4, 5, 6, 7, 8, 10, 12, 15).
It aggregates metrics (Execution Time, Success Rate, Restarts, Steps) and
generates publication-quality Matplotlib charts.
"""

import os
import time
from typing import List, Dict, Any, Optional, Callable
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Import our algorithm solvers
from backtracking import solve_n_queens_backtracking
from hill_climbing import solve_n_queens_hill_climbing

DEFAULT_N_VALUES = [4, 5, 6, 7, 8, 10, 12, 15]


def run_single_comparison(n: int, hc_trials: int = 5) -> Dict[str, Any]:
    """
    Run Backtracking once and Hill Climbing for multiple trials for a single N value.
    
    Parameters:
        n (int): Board dimension and number of queens.
        hc_trials (int): Number of randomized trials for Hill Climbing.
        
    Returns:
        dict: Aggregated performance metrics for this N.
    """
    # 1. Backtracking (deterministic, run once)
    bt_res = solve_n_queens_backtracking(n)
    bt_time = bt_res["execution_time"]
    bt_success = bt_res["success"]
    bt_calls = bt_res["recursive_calls"]

    # 2. Hill Climbing (stochastic, run multiple trials)
    hc_times = []
    hc_successes = []
    hc_restarts = []
    hc_steps = []

    for _ in range(hc_trials):
        hc_res = solve_n_queens_hill_climbing(n)
        hc_times.append(hc_res["execution_time"])
        hc_successes.append(1 if hc_res["success"] else 0)
        hc_restarts.append(hc_res["restarts"])
        hc_steps.append(hc_res["total_steps"])

    hc_avg_time = float(np.mean(hc_times))
    hc_success_rate = float((sum(hc_successes) / hc_trials) * 100.0)
    hc_avg_restarts = float(np.mean(hc_restarts))
    hc_avg_steps = float(np.mean(hc_steps))

    return {
        "N": n,
        "Backtracking Time (s)": round(bt_time, 5),
        "Hill Climbing Avg Time (s)": round(hc_avg_time, 5),
        "Backtracking Success": "Success" if bt_success else "Failure",
        "Hill Climbing Success": f"{hc_success_rate:.0f}%",
        "Hill Climbing Avg Restarts": round(hc_avg_restarts, 2),
        "BT Recursive Calls": bt_calls,
        "HC Avg Steps": round(hc_avg_steps, 1),
        # Raw numeric values for plotting
        "bt_time_raw": bt_time,
        "hc_time_raw": hc_avg_time,
        "bt_success_rate": 100.0 if bt_success else 0.0,
        "hc_success_rate": hc_success_rate,
        "hc_restarts_raw": hc_avg_restarts,
    }


def run_full_benchmark(
    n_values: Optional[List[int]] = None,
    hc_trials: int = 5,
    progress_callback: Optional[Callable[[int, int, str], None]] = None
) -> pd.DataFrame:
    """
    Execute full benchmark across specified N values.
    
    Parameters:
        n_values (Optional[List[int]]): List of N values to test.
        hc_trials (int): Trials per N for Hill Climbing.
        progress_callback (Optional[Callable]): Callback for UI progress updates.
        
    Returns:
        pd.DataFrame: Benchmark results table.
    """
    if n_values is None:
        n_values = DEFAULT_N_VALUES

    rows = []
    total = len(n_values)

    for idx, n in enumerate(n_values):
        if progress_callback:
            progress_callback(idx, total, f"Benchmarking N = {n}...")
        
        row = run_single_comparison(n, hc_trials=hc_trials)
        rows.append(row)

    if progress_callback:
        progress_callback(total, total, "Benchmark complete!")

    df = pd.DataFrame(rows)
    return df


# ============================================================================
# MATPLOTLIB GRAPH GENERATION
# ============================================================================

def setup_plot_style():
    """Apply clean, modern styling to matplotlib figures."""
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.size": 11,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.labelsize": 12,
        "axes.labelweight": "bold",
        "axes.grid": True,
        "grid.alpha": 0.35,
        "grid.linestyle": "--",
        "figure.facecolor": "white",
        "axes.facecolor": "#F8FAFC",
        "axes.edgecolor": "#CBD5E1",
        "axes.linewidth": 1.2
    })


def plot_execution_time(df: pd.DataFrame, save_path: Optional[str] = None) -> plt.Figure:
    """
    Generate grouped bar chart comparing execution time of Backtracking vs Hill Climbing.
    """
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)

    n_vals = df["N"].tolist()
    x = np.arange(len(n_vals))
    width = 0.38

    bt_times = df["bt_time_raw"].tolist()
    hc_times = df["hc_time_raw"].tolist()

    rects1 = ax.bar(x - width/2, bt_times, width, label="Backtracking", color="#2563EB", edgecolor="#1D4ED8", alpha=0.9)
    rects2 = ax.bar(x + width/2, hc_times, width, label="Hill Climbing (Min-Conflicts)", color="#10B981", edgecolor="#047857", alpha=0.9)

    ax.set_xlabel("Number of Queens (N)")
    ax.set_ylabel("Execution Time (seconds)")
    ax.set_title("Execution Time Comparison: Backtracking vs Hill Climbing")
    ax.set_xticks(x)
    ax.set_xticklabels([f"N={n}" for n in n_vals])
    ax.legend(frameon=True, facecolor="white", edgecolor="#E2E8F0")

    # Annotate bar tops with clean text
    for rect in rects1:
        height = rect.get_height()
        ax.annotate(f"{height:.4f}s" if height >= 0.0001 else "<0.1ms",
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=8, rotation=35, color="#1E3A8A")

    for rect in rects2:
        height = rect.get_height()
        ax.annotate(f"{height:.4f}s" if height >= 0.0001 else "<0.1ms",
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=8, rotation=35, color="#065F46")

    # Give headroom for annotations
    ax.set_ylim(0, max(max(bt_times), max(hc_times)) * 1.35 if max(bt_times + hc_times) > 0 else 1)
    fig.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    return fig


def plot_success_rate(df: pd.DataFrame, save_path: Optional[str] = None) -> plt.Figure:
    """
    Generate bar chart comparing Success Rate (%) between Backtracking and Hill Climbing.
    """
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)

    n_vals = df["N"].tolist()
    x = np.arange(len(n_vals))
    width = 0.38

    bt_rates = df["bt_success_rate"].tolist()
    hc_rates = df["hc_success_rate"].tolist()

    rects1 = ax.bar(x - width/2, bt_rates, width, label="Backtracking", color="#3B82F6", edgecolor="#1D4ED8", alpha=0.9)
    rects2 = ax.bar(x + width/2, hc_rates, width, label="Hill Climbing (Min-Conflicts)", color="#8B5CF6", edgecolor="#6D28D9", alpha=0.9)

    ax.set_xlabel("Number of Queens (N)")
    ax.set_ylabel("Success Rate (%)")
    ax.set_title("Success Rate Comparison across Board Sizes (N)")
    ax.set_xticks(x)
    ax.set_xticklabels([f"N={n}" for n in n_vals])
    ax.set_ylim(0, 115)
    ax.legend(loc="lower right", frameon=True, facecolor="white")

    for rect in rects1:
        height = rect.get_height()
        ax.annotate(f"{int(height)}%",
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=9, fontweight="bold", color="#1E3A8A")

    for rect in rects2:
        height = rect.get_height()
        ax.annotate(f"{int(height)}%",
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=9, fontweight="bold", color="#4C1D95")

    fig.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    return fig


def plot_restarts(df: pd.DataFrame, save_path: Optional[str] = None) -> plt.Figure:
    """
    Generate bar chart displaying the average number of restarts required by Hill Climbing.
    """
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)

    n_vals = df["N"].tolist()
    x = np.arange(len(n_vals))
    restarts = df["hc_restarts_raw"].tolist()

    bars = ax.bar(x, restarts, width=0.55, color="#F59E0B", edgecolor="#D97706", alpha=0.9, label="Hill Climbing Restarts")

    ax.set_xlabel("Number of Queens (N)")
    ax.set_ylabel("Average Restarts Required")
    ax.set_title("Hill Climbing (Min-Conflicts): Average Restarts to Solution")
    ax.set_xticks(x)
    ax.set_xticklabels([f"N={n}" for n in n_vals])
    
    max_r = max(restarts) if restarts else 1
    ax.set_ylim(0, max(max_r * 1.35, 1.5))

    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:.1f}",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=9, fontweight="bold", color="#92400E")

    ax.axhline(0, color="gray", linewidth=0.8)
    ax.legend(frameon=True, facecolor="white")

    fig.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    return fig


def generate_all_comparison_assets(output_dir: str = "screenshots") -> Dict[str, str]:
    """
    Run full benchmark, save CSV, and generate all high-res Matplotlib chart images.
    
    Parameters:
        output_dir (str): Directory where screenshots and plots will be saved.
        
    Returns:
        dict: Mapping of plot names to saved file paths.
    """
    os.makedirs(output_dir, exist_ok=True)
    print("Running comprehensive benchmark for N = [4, 5, 6, 7, 8, 10, 12, 15]...")
    df = run_full_benchmark(DEFAULT_N_VALUES, hc_trials=5)

    # Save benchmark table
    csv_path = os.path.join(output_dir, "benchmark_results.csv")
    df.to_csv(csv_path, index=False)
    print(f"Saved benchmark CSV to {csv_path}")

    # Generate charts
    time_plot_path = os.path.join(output_dir, "execution_time_comparison.png")
    success_plot_path = os.path.join(output_dir, "success_rate_comparison.png")
    restarts_plot_path = os.path.join(output_dir, "restarts_comparison.png")

    fig1 = plot_execution_time(df, save_path=time_plot_path)
    plt.close(fig1)

    fig2 = plot_success_rate(df, save_path=success_plot_path)
    plt.close(fig2)

    fig3 = plot_restarts(df, save_path=restarts_plot_path)
    plt.close(fig3)

    print("All comparison plots generated successfully.")
    return {
        "csv": csv_path,
        "time_plot": time_plot_path,
        "success_plot": success_plot_path,
        "restarts_plot": restarts_plot_path,
    }


if __name__ == "__main__":
    generate_all_comparison_assets()
