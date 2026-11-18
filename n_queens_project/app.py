"""
N-Queens: Backtracking vs Hill Climbing
Subject: Artificial Intelligence | Unit II: Search & Optimization | Outcome: CO2
Streamlit Web Application
"""

import time
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Solvers and benchmark utilities
from backtracking import solve_n_queens_backtracking, count_conflicts as bt_count_conflicts
from hill_climbing import solve_n_queens_hill_climbing, count_conflicts as hc_count_conflicts
from comparison import (
    run_full_benchmark,
    run_single_comparison,
    plot_execution_time,
    plot_success_rate,
    plot_restarts,
    DEFAULT_N_VALUES
)

# Page Configuration
st.set_page_config(
    page_title="N-Queens: Backtracking vs Hill Climbing",
    page_icon="♛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Global styles */
    .main-header {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        padding: 1.8rem 2.2rem;
        border-radius: 14px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.1rem;
        font-weight: 800;
        color: #F8FAFC;
    }
    .badge-bar {
        display: flex;
        gap: 0.6rem;
        flex-wrap: wrap;
        margin-top: 0.8rem;
    }
    .badge {
        background: rgba(59, 130, 246, 0.2);
        border: 1px solid rgba(96, 165, 250, 0.4);
        color: #93C5FD;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
    }
    .badge-accent {
        background: rgba(16, 185, 129, 0.2);
        border: 1px solid rgba(52, 211, 153, 0.4);
        color: #6EE7B7;
    }
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        text-align: center;
        margin-bottom: 0.8rem;
    }
    .metric-title {
        color: #64748B;
        font-size: 0.85rem;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .metric-value {
        color: #0F172A;
        font-size: 1.6rem;
        font-weight: 800;
        margin-top: 0.3rem;
    }
    .status-success {
        color: #10B981 !important;
    }
    .status-failure {
        color: #EF4444 !important;
    }
    /* Chessboard CSS */
    .board-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 1.2rem 0;
    }
    .chessboard {
        display: grid;
        border: 3px solid #334155;
        border-radius: 8px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        background-color: #334155;
        overflow: hidden;
    }
    .cell {
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: bold;
        user-select: none;
        transition: background-color 0.2s;
    }
    .cell-light {
        background-color: #F8FAFC;
    }
    .cell-dark {
        background-color: #94A3B8;
    }
    .queen-icon {
        color: #1E293B;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.35));
        transition: transform 0.2s;
    }
    .queen-icon:hover {
        transform: scale(1.15);
    }
    .cell-queen-active {
        background: radial-gradient(circle, rgba(251,191,36,0.35) 0%, rgba(245,158,11,0.15) 100%);
    }
</style>
""", unsafe_allow_html=True)


def render_html_chessboard(board: list, n: int, title: str = "Chessboard Placement"):
    """
    Renders a responsive, visually appealing HTML chessboard with ♛ symbols.
    """
    if board is None or len(board) != n:
        st.warning(f"No board configuration available to render for {title}.")
        return

    # Dynamic square size based on N
    cell_size = max(24, min(56, int(460 / n)))
    font_size = int(cell_size * 0.72)

    st.markdown(f"<h4 style='text-align: center; color: #334155; margin-bottom: 0.5rem;'>{title}</h4>", unsafe_allow_html=True)
    
    html = f"""
    <div class="board-container">
        <div class="chessboard" style="
            grid-template-columns: repeat({n}, {cell_size}px);
            grid-template-rows: repeat({n}, {cell_size}px);
        ">
    """
    for r in range(n):
        for c in range(n):
            is_light = (r + c) % 2 == 0
            cell_class = "cell-light" if is_light else "cell-dark"
            has_queen = (board[c] == r)
            queen_active = " cell-queen-active" if has_queen else ""

            queen_html = f"<span class='queen-icon' style='font-size: {font_size}px;'>♛</span>" if has_queen else ""
            html += f"<div class='cell {cell_class}{queen_active}' style='width:{cell_size}px; height:{cell_size}px;'>{queen_html}</div>"

    html += "</div></div>"
    st.markdown(html, unsafe_allow_html=True)


# Application Header
st.markdown("""
<div class="main-header">
    <h1>♛ N-Queens: Backtracking vs Hill Climbing</h1>
    <p style="margin-top: 0.4rem; color: #CBD5E1; font-size: 1.05rem;">
        Comparative empirical and theoretical analysis of systematic Constraint Satisfaction (DFS Backtracking)
        versus Stochastic Local Search (Min-Conflicts Hill Climbing with Random Restarts).
    </p>
    <div class="badge-bar">
        <span class="badge">Subject: Artificial Intelligence</span>
        <span class="badge">Unit II: Search & Optimization</span>
        <span class="badge">Course Outcome: CO2</span>
        <span class="badge badge-accent">Intermediate Level</span>
        <span class="badge">Language: Python 3</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation and Configuration
st.sidebar.image("https://img.icons8.com/color/96/000000/queen-crown.png", width=64)
st.sidebar.title("Navigation & Controls")
app_mode = st.sidebar.radio(
    "Choose Mode",
    ["Interactive Solver", "Performance Comparison", "Algorithm Theory", "Generate Presentation (.pptx)"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Global Algorithm Settings")
max_time_limit = st.sidebar.slider("Timeout per Algorithm (sec)", 5, 60, 30)
hc_max_restarts = st.sidebar.slider("Hill Climbing Max Restarts", 10, 200, 50)
hc_trials_bench = st.sidebar.slider("HC Benchmark Trials per N", 1, 15, 5)

# ============================================================================
# MODE 1: INTERACTIVE SOLVER
# ============================================================================
if app_mode == "Interactive Solver":
    st.subheader("🎯 Interactive N-Queens Solver & Visualization")
    st.write("Configure the chessboard size and execute either algorithm or compare both side-by-side.")

    col1, col2, col3 = st.columns([1.5, 2, 1.2])

    with col1:
        n_input = st.number_input(
            "Enter N (Number of Queens & Board Dimension):",
            min_value=1,
            max_value=30,
            value=8,
            step=1,
            help="Common values: 4, 8, 12, 15. Note: N=2 and N=3 have no solutions."
        )

    with col2:
        algorithm_choice = st.selectbox(
            "Select Algorithm:",
            [
                "Backtracking Algorithm (Systematic DFS)",
                "Hill Climbing (Min-Conflicts Local Search)",
                "Compare Both Algorithms (Side-by-Side)"
            ]
        )

    with col3:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        run_btn = st.button("🚀 Run Solver", type="primary", use_container_width=True)

    if n_input in (2, 3):
        st.info(f"ℹ️ Note: For N = {n_input}, mathematical proofs confirm that no mutually non-attacking queen arrangement is possible.")

    if run_btn:
        # Run Backtracking
        if "Backtracking" in algorithm_choice or "Compare Both" in algorithm_choice:
            with st.spinner("Executing Backtracking Algorithm..."):
                bt_result = solve_n_queens_backtracking(n_input, max_time=float(max_time_limit))
        else:
            bt_result = None

        # Run Hill Climbing
        if "Hill Climbing" in algorithm_choice or "Compare Both" in algorithm_choice:
            with st.spinner("Executing Hill Climbing with Min-Conflicts..."):
                hc_result = solve_n_queens_hill_climbing(
                    n_input,
                    max_restarts=hc_max_restarts,
                    max_time=float(max_time_limit)
                )
        else:
            hc_result = None

        # Display Results
        if algorithm_choice == "Compare Both Algorithms (Side-by-Side)":
            c_left, c_right = st.columns(2)

            with c_left:
                st.markdown("### 🌲 Backtracking Algorithm")
                status_color = "status-success" if bt_result["success"] else "status-failure"
                status_text = "SOLVED" if bt_result["success"] else "FAILED / NO SOL."
                
                m1, m2, m3, m4 = st.columns(4)
                m1.markdown(f"<div class='metric-card'><div class='metric-title'>Status</div><div class='metric-value {status_color}'>{status_text}</div></div>", unsafe_allow_html=True)
                m2.markdown(f"<div class='metric-card'><div class='metric-title'>Time (s)</div><div class='metric-value'>{bt_result['execution_time']:.4f}</div></div>", unsafe_allow_html=True)
                m3.markdown(f"<div class='metric-card'><div class='metric-title'>Restarts</div><div class='metric-value'>{bt_result['restarts']}</div></div>", unsafe_allow_html=True)
                m4.markdown(f"<div class='metric-card'><div class='metric-title'>Conflicts</div><div class='metric-value'>{bt_result['conflicts']}</div></div>", unsafe_allow_html=True)

                st.caption(f"Recursive Calls: **{bt_result['recursive_calls']:,}** | {bt_result['message']}")
                if bt_result["board"] is not None:
                    render_html_chessboard(bt_result["board"], n_input, title=f"Backtracking Solution (N={n_input})")
                    st.code(f"Queen Positions (Col: Row) -> {[(col, r) for col, r in enumerate(bt_result['board'])]}")

            with c_right:
                st.markdown("### 🏔️ Hill Climbing (Min-Conflicts)")
                status_color = "status-success" if hc_result["success"] else "status-failure"
                status_text = "SOLVED" if hc_result["success"] else "FAILED"

                m1, m2, m3, m4 = st.columns(4)
                m1.markdown(f"<div class='metric-card'><div class='metric-title'>Status</div><div class='metric-value {status_color}'>{status_text}</div></div>", unsafe_allow_html=True)
                m2.markdown(f"<div class='metric-card'><div class='metric-title'>Time (s)</div><div class='metric-value'>{hc_result['execution_time']:.4f}</div></div>", unsafe_allow_html=True)
                m3.markdown(f"<div class='metric-card'><div class='metric-title'>Restarts</div><div class='metric-value'>{hc_result['restarts']}</div></div>", unsafe_allow_html=True)
                m4.markdown(f"<div class='metric-card'><div class='metric-title'>Conflicts</div><div class='metric-value'>{hc_result['conflicts']}</div></div>", unsafe_allow_html=True)

                st.caption(f"Min-Conflict Steps: **{hc_result['total_steps']:,}** | {hc_result['message']}")
                if hc_result["board"] is not None:
                    render_html_chessboard(hc_result["board"], n_input, title=f"Hill Climbing Solution (N={n_input})")
                    st.code(f"Queen Positions (Col: Row) -> {[(col, r) for col, r in enumerate(hc_result['board'])]}")

        else:
            # Single algorithm display
            result = bt_result if bt_result is not None else hc_result
            algo_name = "Backtracking Algorithm" if bt_result is not None else "Hill Climbing (Min-Conflicts)"
            
            st.markdown(f"### Results for {algo_name}")
            status_color = "status-success" if result["success"] else "status-failure"
            status_text = "SOLVED" if result["success"] else "FAILED / NO SOL."

            col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
            col_m1.markdown(f"<div class='metric-card'><div class='metric-title'>Status</div><div class='metric-value {status_color}'>{status_text}</div></div>", unsafe_allow_html=True)
            col_m2.markdown(f"<div class='metric-card'><div class='metric-title'>Time</div><div class='metric-value'>{result['execution_time']:.4f}s</div></div>", unsafe_allow_html=True)
            col_m3.markdown(f"<div class='metric-card'><div class='metric-title'>Restarts</div><div class='metric-value'>{result['restarts']}</div></div>", unsafe_allow_html=True)
            col_m4.markdown(f"<div class='metric-card'><div class='metric-title'>Total Conflicts</div><div class='metric-value'>{result['conflicts']}</div></div>", unsafe_allow_html=True)
            step_label = "Recursive Calls" if bt_result is not None else "Total Steps"
            step_val = result.get("recursive_calls", result.get("total_steps", 0))
            col_m5.markdown(f"<div class='metric-card'><div class='metric-title'>{step_label}</div><div class='metric-value'>{step_val:,}</div></div>", unsafe_allow_html=True)

            if result["success"]:
                st.success(f"✅ {result['message']}")
            else:
                st.error(f"❌ {result['message']}")

            if result["board"] is not None:
                render_html_chessboard(result["board"], n_input, title=f"Visual Chessboard (N={n_input})")
                st.markdown("#### ♛ Coordinates Breakdown")
                pos_str = ", ".join([f"Col {c} -> Row {r}" for c, r in enumerate(result["board"])])
                st.info(pos_str)

# ============================================================================
# MODE 2: PERFORMANCE COMPARISON
# ============================================================================
elif app_mode == "Performance Comparison":
    st.subheader("📊 Empirical Performance Comparison: Backtracking vs Hill Climbing")
    st.write("Benchmark both algorithms across standard board sizes (N = 4, 5, 6, 7, 8, 10, 12, 15) to evaluate time complexity, success rates, and restart requirements.")

    col_btn, col_info = st.columns([1.5, 3])
    with col_btn:
        run_bench = st.button("⚡ Run Full Benchmark (N=4 to 15)", type="primary", use_container_width=True)

    with col_info:
        st.markdown(f"**Settings:** Testing N ∈ {DEFAULT_N_VALUES} | Hill Climbing Trials per N = **{hc_trials_bench}**")

    # Session state caching so results persist across tab switches
    if "benchmark_df" not in st.session_state:
        st.session_state.benchmark_df = None

    if run_bench:
        progress_bar = st.progress(0.0)
        status_box = st.empty()

        def update_progress(current, total, msg):
            progress_bar.progress(current / total)
            status_box.info(msg)

        bench_df = run_full_benchmark(
            DEFAULT_N_VALUES,
            hc_trials=hc_trials_bench,
            progress_callback=update_progress
        )
        st.session_state.benchmark_df = bench_df
        status_box.success("🎉 Benchmark evaluation completed successfully!")

    if st.session_state.benchmark_df is not None:
        df = st.session_state.benchmark_df

        st.markdown("### 📋 Performance Comparison Table")
        display_cols = [
            "N",
            "Backtracking Time (s)",
            "Hill Climbing Avg Time (s)",
            "Backtracking Success",
            "Hill Climbing Success",
            "Hill Climbing Avg Restarts"
        ]
        st.dataframe(
            df[display_cols].style.highlight_min(
                subset=["Backtracking Time (s)", "Hill Climbing Avg Time (s)"],
                color="#DCFCE7"
            ),
            use_container_width=True
        )

        st.markdown("### 📈 Visual Performance Graphs")
        tab_time, tab_success, tab_restarts = st.tabs([
            "⏱️ Execution Time Comparison",
            "🎯 Success Rate Comparison",
            "🔄 Number of Restarts (Hill Climbing)"
        ])

        with tab_time:
            fig_time = plot_execution_time(df)
            st.pyplot(fig_time)
            plt.close(fig_time)
            st.markdown("""
            **Observation:** 
            - For small N, Backtracking executes nearly instantaneously. However, its worst-case state space grows factorially ($O(N!)$).
            - Hill Climbing with the Min-Conflicts heuristic operates in polynomial/near-linear empirical time, finding valid configurations rapidly even as N grows.
            """)

        with tab_success:
            fig_success = plot_success_rate(df)
            st.pyplot(fig_success)
            plt.close(fig_success)
            st.markdown("""
            **Observation:** 
            - **Backtracking** is *complete* (always finds a solution if one exists, achieving 100% success for all $N \\ge 4$).
            - **Hill Climbing (Min-Conflicts)** with random restarts achieves near 100% success rate on almost all test sizes, recovering from local plateaus.
            """)

        with tab_restarts:
            fig_restarts = plot_restarts(df)
            st.pyplot(fig_restarts)
            plt.close(fig_restarts)
            st.markdown("""
            **Observation:** 
            - Backtracking is a systematic tree search that never requires restarts (Restarts = 0).
            - Hill Climbing requires occasional random restarts when trapped in dense conflict loops or plateaus, but the average restarts remain remarkably small.
            """)

        # Download CSV
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Benchmark Results (CSV)",
            data=csv_bytes,
            file_name="n_queens_comparison_benchmark.csv",
            mime="text/csv"
        )

# ============================================================================
# MODE 3: ALGORITHM THEORY
# ============================================================================
elif app_mode == "Algorithm Theory":
    st.subheader("📚 Theoretical Foundations & Comparative Architecture")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("""
        ### 🌲 1. Backtracking Algorithm
        - **Paradigm:** Systematic Depth-First Tree Search (DFS) with Constraint Pruning.
        - **Search Space:** Constructs assignments incrementally column-by-column ($c = 0 \\dots N-1$).
        - **Pruning Criterion:** Immediately abandons a partial candidate placement as soon as any row or diagonal attack condition is violated:
          $$\\text{Conflict}(r_1, c_1, r_2, c_2) \\iff (r_1 = r_2) \\lor (|r_1 - r_2| = |c_1 - c_2|)$$
        - **Completeness:** **Complete** (Guaranteed to find a solution or prove none exists).
        - **Optimality:** Finds the first lexicographically smallest solution.
        - **Worst-Case Complexity:** $O(N!)$ time, $O(N)$ auxiliary stack space.
        """)

    with col_t2:
        st.markdown("""
        ### 🏔️ 2. Hill Climbing (Min-Conflicts)
        - **Paradigm:** Stochastic Local Search & Constraint Satisfaction Problem (CSP) Heuristic.
        - **Search Space:** Complete-state formulation. Starts with all $N$ queens placed on the board (one per column).
        - **Heuristic Step:**
          1. Select a randomly conflicted queen (at column $c$).
          2. Compute conflicts for all candidate rows $r \\in [0, N-1]$.
          3. Move queen to the row with the minimal conflict count:
             $$r^* = \\arg\\min_{r} \\{ \\text{Conflicts}(c, r) \\}$$
        - **Plateau Handling:** Random tie-breaking + Random Restarts when step budget is reached.
        - **Empirical Complexity:** Near-linear $O(N)$ time on average.
        """)

    st.markdown("---")
    st.markdown("### ⚖️ Algorithm Comparison Summary Matrix")
    matrix_data = {
        "Criterion": [
            "Algorithmic Paradigm",
            "Completeness",
            "Time Complexity (Worst-Case)",
            "Empirical Scaling",
            "Space Complexity",
            "Restart Requirement",
            "Vulnerability"
        ],
        "Backtracking (DFS Pruning)": [
            "Systematic Constructive Search",
            "Guaranteed Complete",
            "O(N!) Factorial / Exponential",
            "Rapid for small N, explodes for large N",
            "O(N) Call Stack",
            "None (Deterministic, Restarts = 0)",
            "Combinatorial state explosion"
        ],
        "Hill Climbing (Min-Conflicts)": [
            "Iterative Local Repair / CSP",
            "Incomplete (Probabilistically Complete w/ Restarts)",
            "O(max_steps × N)",
            "Virtually linear O(N) average runtime",
            "O(N) Board & Counters",
            "Requires Random Restarts on Plateaus",
            "Local minima, cycles, saddle points"
        ]
    }
    st.table(pd.DataFrame(matrix_data))

# ============================================================================
# MODE 4: GENERATE PRESENTATION
# ============================================================================
elif app_mode == "Generate Presentation (.pptx)":
    st.subheader("📑 PowerPoint Presentation Generator")
    st.write("Generate or download the presentation with benchmark charts, architecture flowcharts, and visual chessboards embedded.")

    pptx_6_path = os.path.join(os.path.dirname(__file__), "presentation.pptx")
    pptx_15_path = os.path.join(os.path.dirname(__file__), "presentation_full_15_slides.pptx")
    
    col_gen1, col_gen2 = st.columns(2)
    with col_gen1:
        if st.button("🎨 Build Concise 6-Slide Presentation", type="primary", use_container_width=True):
            with st.spinner("Generating 6-slide presentation..."):
                try:
                    from generate_presentation_short import create_6_slide_presentation
                    create_6_slide_presentation(pptx_6_path)
                    st.success("🎉 Concise 6-slide presentation built as `presentation.pptx`!")
                except Exception as e:
                    st.error(f"Error: {e}")

    with col_gen2:
        if st.button("📑 Build Comprehensive 15-Slide Presentation", use_container_width=True):
            with st.spinner("Generating 15-slide presentation..."):
                try:
                    from generate_presentation import create_complete_presentation
                    create_complete_presentation(pptx_15_path)
                    st.success("🎉 Full 15-slide presentation built as `presentation_full_15_slides.pptx`!")
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")
    st.markdown("#### 📥 Download Presentations")
    col_dl1, col_dl2 = st.columns(2)

    if os.path.exists(pptx_6_path):
        with open(pptx_6_path, "rb") as f:
            b6 = f.read()
        with col_dl1:
            st.download_button(
                label="📥 Download 6-Slide PPT (Quick Presentation)",
                data=b6,
                file_name="N_Queens_Backtracking_vs_Hill_Climbing_6_Slides.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                use_container_width=True
            )

    if os.path.exists(pptx_15_path):
        with open(pptx_15_path, "rb") as f:
            b15 = f.read()
        with col_dl2:
            st.download_button(
                label="📥 Download 15-Slide PPT (Full Academic Deck)",
                data=b15,
                file_name="N_Queens_Backtracking_vs_Hill_Climbing_15_Slides.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                use_container_width=True
            )

    st.markdown("#### 📑 Slide Structure (6-Slide Concise Deck):")
    slides_info_6 = [
        "1. Title Slide – Project title, Subject (AI), Unit II, Outcome CO2, and core highlights.",
        "2. Problem Formulation & Algorithmic Paradigms – Backtracking vs Min-Conflicts Hill Climbing.",
        "3. System Architecture & Implementation Workflow – End-to-end flowchart and modular design.",
        "4. Empirical Performance Benchmark Table – Test results for N = 4 to 15 with analytical observations.",
        "5. Performance Graphs & Visual Chessboard Outputs – Embedded execution time, restarts charts, and 8-Queens board.",
        "6. Comparative Trade-offs, CO2 Takeaways & Conclusion – Completeness vs speed matrix and CO2 achievements."
    ]
    for s in slides_info_6:
        st.write(f"- {s}")
