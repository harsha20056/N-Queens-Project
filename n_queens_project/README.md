# N-Queens: Backtracking vs Hill Climbing

[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB.svg?logo=python&logoColor=white)](https://python.org)
[![Streamlit App](https://img.shields.io/badge/Streamlit-1.39-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Course Outcome CO2](https://img.shields.io/badge/Course_Outcome-CO2-059669.svg)](#course-outcome-alignment)
[![Subject](https://img.shields.io/badge/Subject-Artificial_Intelligence-2563EB.svg)](#academic-metadata)

> **Comparative Empirical & Theoretical Study of Systematic Constraint Satisfaction Search (Backtracking) vs Stochastic Local Search (Hill Climbing with Min-Conflicts Heuristic).**

---

## 🎓 Academic Metadata

| Property | Details |
| :--- | :--- |
| **Project Title** | N-Queens: Backtracking vs Hill Climbing |
| **Subject** | Artificial Intelligence |
| **Unit** | Unit II – Search & Optimization |
| **Difficulty Level** | Intermediate |
| **Course Outcome** | **CO2** (Formulate and solve search and constraint satisfaction problems using search heuristics) |
| **Programming Language** | Python 3.11 |

---

## 📌 Project Objectives

1. **Dual Algorithm Implementation:**
   - **Backtracking:** Place $N$ queens on an $N \times N$ chessboard such that no two queens attack each other across rows, columns, or diagonals using recursive depth-first search (DFS) with constraint pruning.
   - **Hill Climbing (Min-Conflicts):** Complete-state local repair heuristic that starts with a random board and iteratively relocates conflicted queens to positions minimizing conflicts, supported by random restarts to overcome plateaus and local minima.
2. **Empirical Benchmarking:**
   - Systematically evaluate both algorithms across $N \in \{4, 5, 6, 7, 8, 10, 12, 15\}$.
   - Compare performance across **Execution Time**, **Success Rate**, **Number of Restarts**, and **Steps / Recursive Calls**.
3. **Modern Interactive User Interface:**
   - Build a responsive web application using Streamlit featuring real-time board rendering with ♛ glyphs, live metric dashboards, and side-by-side solver comparisons.
4. **Automated Academic Presentation:**
   - Automatically generate a 15-slide PowerPoint deck (`presentation.pptx`) with embedded high-resolution benchmark charts, architecture flowcharts, and comparison tables.

---

## 🗂️ Project Directory Structure

```text
n_queens_project/
│
├── app.py                      # Interactive Streamlit Web Application
├── backtracking.py            # Recursive Backtracking algorithm solver & constraint checks
├── hill_climbing.py           # Min-Conflicts Hill Climbing with Random Restarts
├── comparison.py              # Benchmarking engine & Matplotlib comparison chart generation
├── generate_diagrams.py       # Flowchart and visual chessboard image generator
├── generate_presentation.py   # Automated 15-slide PowerPoint presentation generator (.pptx)
├── requirements.txt           # Python dependency definitions
├── README.md                  # Comprehensive technical documentation & run instructions
├── presentation.pptx          # Generated professional PowerPoint presentation
└── screenshots/               # Generated high-resolution charts & diagrams
    ├── architecture_flowchart.png
    ├── execution_time_comparison.png
    ├── success_rate_comparison.png
    ├── restarts_comparison.png
    ├── chessboard_n8.png
    ├── chessboard_n4.png
    └── benchmark_results.csv
```

---

## ⚙️ Installation & Setup

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on Windows, macOS, or Linux.

### 2. Clone or Navigate to the Workspace
```powershell
cd "c:\Users\Sura Harsha Vardhan\OneDrive\Desktop\ai_project\n_queens_project"
```

### 3. Install Dependencies
Install the required packages using pip:
```powershell
python -m pip install -r requirements.txt
```
*(Dependencies: `streamlit`, `matplotlib`, `pandas`, `python-pptx`, `numpy`, `pillow`)*

---

## 🚀 Running the Project

### A. Launch the Streamlit Web Application
```powershell
python -m streamlit run app.py
```
After running this command, open your browser at `http://localhost:8501`.

#### Web App Features:
- **Interactive Solver:** Enter any board size $N$ (e.g., 4, 8, 12, 15, up to 30), select Backtracking, Hill Climbing, or Side-by-Side comparison, and view the live rendered chessboard with ♛ symbols, execution time, conflicts, and restarts.
- **Performance Comparison:** Execute automated benchmarks across standard test sizes ($N = 4, 5, 6, 7, 8, 10, 12, 15$), view the colored comparison data table, and inspect interactive Matplotlib graphs.
- **Algorithm Theory:** Study formal definitions, state-space representations, and comparison matrices.
- **Presentation Generator:** Rebuild or download `presentation.pptx` directly with a single click.

---

### B. Run the CLI Benchmark & Generate Graphs
To run the automated empirical benchmark from the terminal and update the chart images:
```powershell
python comparison.py
```
This generates:
- `screenshots/benchmark_results.csv`
- `screenshots/execution_time_comparison.png`
- `screenshots/success_rate_comparison.png`
- `screenshots/restarts_comparison.png`

---

### C. Generate the PowerPoint Presentation (.pptx)
You can generate either the concise 6-slide deck or the comprehensive 15-slide deck:
```powershell
# 1. Generate Concise 6-Slide Presentation (presentation.pptx / presentation_short.pptx):
python generate_presentation_short.py

# 2. Generate Comprehensive 15-Slide Presentation (presentation_full_15_slides.pptx):
python generate_presentation.py
```

---

## 🧠 Algorithmic Comparison & Analysis

| Evaluation Metric | Backtracking Algorithm (DFS) | Hill Climbing (Min-Conflicts) |
| :--- | :--- | :--- |
| **Search Paradigm** | Systematic Depth-First Tree Search | Stochastic Local Search / CSP Heuristic |
| **State Representation** | Partial incremental placements | Complete state (all $N$ queens placed) |
| **Completeness** | **Strictly Complete** (Always finds solution or proves none exists) | **Probabilistically Complete** (via Random Restarts) |
| **Optimality** | Finds first lexicographical solution | Finds arbitrary valid configuration |
| **Worst-Case Time Complexity** | $\mathcal{O}(N!)$ (Factorial / Exponential explosion) | $\mathcal{O}(\text{max\_steps} \times N)$ |
| **Empirical Average Time** | Milliseconds for $N \le 10$, surges for $N \ge 15$ | **Near-linear $\mathcal{O}(N)$** across all tested $N$ |
| **Auxiliary Memory** | $\mathcal{O}(N)$ call stack depth | $\mathcal{O}(N)$ frequency tables |
| **Restarts Needed** | **0** (Deterministic systematic exploration) | $0$ to $2$ average restarts on plateaus |
| **Handling of $N=2, 3$** | Correctly proves no solution exists | Detects unsolvability after restart budget |

---

## 📊 Sample Empirical Benchmark Results

Below are the empirical metrics recorded across test runs ($5$ trials per $N$ for Hill Climbing):

| $N$ Value | Backtracking Time (s) | Hill Climbing Avg Time (s) | Backtracking Success | Hill Climbing Success Rate | Hill Climbing Avg Restarts |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **4** | 0.00004 s | 0.00042 s | ✅ Success | 100% | 0.0 |
| **5** | 0.00006 s | 0.00051 s | ✅ Success | 100% | 0.0 |
| **6** | 0.00012 s | 0.00118 s | ✅ Success | 100% | 0.2 |
| **7** | 0.00035 s | 0.00145 s | ✅ Success | 100% | 0.2 |
| **8** | 0.00142 s | 0.00204 s | ✅ Success | 100% | 0.4 |
| **10** | 0.00348 s | 0.00362 s | ✅ Success | 100% | 0.6 |
| **12** | 0.01480 s | 0.00640 s | ✅ Success | 100% | 0.8 |
| **15** | 0.08250 s | 0.01180 s | ✅ Success | 100% | 1.0 |

### Key Analytical Observations:
1. **The Crossover Point ($N \approx 10$):**
   - For small $N \le 8$, Backtracking is faster in wall-clock time due to minimal overhead and immediate pruning.
   - For $N \ge 12$, Backtracking begins to show its exponential characteristics ($0.082$s for $N=15$), while Hill Climbing scales near-linearly ($0.011$s for $N=15$).
2. **Min-Conflicts Robustness:**
   - Augmenting local search with random restarts yields a $100\%$ empirical success rate across all solvable board sizes while requiring on average $\le 1.2$ restarts.

---

## 📑 Slide Deck Overview

### A. Concise 6-Slide Presentation (`presentation.pptx` / `presentation_short.pptx`):
1. **Title Slide:** Project metadata, AI Course Outcome CO2, Unit II, and key stat pills.
2. **Problem Formulation & Algorithmic Paradigms:** Dual-card breakdown of Backtracking vs Min-Conflicts Hill Climbing.
3. **System Architecture & Implementation Workflow:** High-resolution flowchart diagram and modular tech stack.
4. **Empirical Performance Benchmark Table:** Formatted benchmark results ($N=4$ to $15$) and analytical insights.
5. **Performance Graphs & Visual Chessboard:** Execution time bar chart, restarts bar chart, and 8-Queens solution board.
6. **Comparative Trade-offs, CO2 Takeaways & Conclusion:** Completeness vs speed trade-off matrix, CO2 learning conclusions, and future scope.

### B. Comprehensive 15-Slide Academic Deck (`presentation_full_15_slides.pptx`):
Includes dedicated standalone slides for Introduction, Problem Formulation, Objectives, Backtracking Theory, Hill Climbing Theory, Min-Conflicts Heuristic, Architecture, Tech Stack, Chessboard Outputs, Benchmark Table, Time Graph, Success & Restarts Graph, Advantages & Limitations, and Conclusion/Future Scope.

---

## 👨‍💻 Course Outcome Alignment (CO2)
This project fulfills **CO2** by enabling students to:
- Understand and formalize constraint satisfaction problems (CSPs).
- Contrast systematic depth-first search with heuristic local repair.
- Formulate heuristic evaluation functions and address local search vulnerabilities (plateaus and local minima).
- Conduct quantitative empirical benchmarking to substantiate asymptotic algorithmic complexity theories.
