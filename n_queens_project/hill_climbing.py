"""
N-Queens: Hill Climbing with Min-Conflicts Strategy
Subject: Artificial Intelligence | Unit II: Search & Optimization (CO2)

This module implements the Min-Conflicts Local Search (Hill Climbing with Random Restarts)
heuristic algorithm for the N-Queens problem. 

Algorithm Details:
1. Start with a random board configuration (one queen per column).
2. Identify queens involved in conflicts (row and diagonal attacks).
3. If no conflicts exist, the problem is solved.
4. Otherwise, pick a conflicted queen at random.
5. Move that queen to the row in its column that minimizes total conflicts (breaking ties randomly).
6. Repeat up to `max_steps_per_restart`.
7. If stuck in a local minimum / plateau, trigger a random restart.
"""

import random
import time
from typing import List, Optional, Dict, Any, Tuple


def count_conflicts(board: Optional[List[int]]) -> int:
    """
    Calculate the total number of attacking pairs of queens on the board.
    
    Parameters:
        board (Optional[List[int]]): List of row indices per column.
        
    Returns:
        int: Total number of conflicting pairs.
    """
    if board is None:
        return 0
    n = len(board)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts


class MinConflictsSolver:
    """
    High-performance Min-Conflicts solver maintaining O(1) conflict lookups
    using row and diagonal frequency tables.
    """

    def __init__(self, n: int):
        self.n = n
        self.board: List[int] = []
        self.row_counts: List[int] = [0] * n
        self.diag1_counts: List[int] = [0] * (2 * n - 1)  # row + col
        self.diag2_counts: List[int] = [0] * (2 * n - 1)  # row - col + (n - 1)

    def initialize_random_board(self) -> None:
        """Assign each queen to a random row and initialize frequency counters."""
        n = self.n
        self.board = [random.randint(0, n - 1) for _ in range(n)]
        self.row_counts = [0] * n
        self.diag1_counts = [0] * (2 * n - 1)
        self.diag2_counts = [0] * (2 * n - 1)

        for col, row in enumerate(self.board):
            self.row_counts[row] += 1
            self.diag1_counts[row + col] += 1
            self.diag2_counts[row - col + (n - 1)] += 1

    def conflicts_for_queen(self, col: int) -> int:
        """Return how many other queens attack the queen at column `col`."""
        row = self.board[col]
        n = self.n
        # Count other queens on same row or diagonals (subtracting self = 1)
        return (
            (self.row_counts[row] - 1)
            + (self.diag1_counts[row + col] - 1)
            + (self.diag2_counts[row - col + (n - 1)] - 1)
        )

    def conflicts_if_moved(self, col: int, candidate_row: int) -> int:
        """Calculate conflicts if queen in `col` were placed in `candidate_row`."""
        current_row = self.board[col]
        n = self.n
        if candidate_row == current_row:
            return self.conflicts_for_queen(col)
        
        # Candidate conflicts with all OTHER queens in the board
        return (
            self.row_counts[candidate_row]
            + self.diag1_counts[candidate_row + col]
            + self.diag2_counts[candidate_row - col + (n - 1)]
        )

    def move_queen(self, col: int, new_row: int) -> None:
        """Move queen in column `col` to `new_row` and update conflict counts."""
        old_row = self.board[col]
        if old_row == new_row:
            return
        n = self.n

        # Remove old queen contribution
        self.row_counts[old_row] -= 1
        self.diag1_counts[old_row + col] -= 1
        self.diag2_counts[old_row - col + (n - 1)] -= 1

        # Place at new row
        self.board[col] = new_row
        self.row_counts[new_row] += 1
        self.diag1_counts[new_row + col] += 1
        self.diag2_counts[new_row - col + (n - 1)] += 1

    def get_conflicted_columns(self) -> List[int]:
        """Return indices of columns whose queens have at least 1 conflict."""
        conflicted = []
        for col in range(self.n):
            if self.conflicts_for_queen(col) > 0:
                conflicted.append(col)
        return conflicted


def solve_n_queens_hill_climbing(
    n: int,
    max_restarts: int = 50,
    max_steps_per_restart: Optional[int] = None,
    max_time: float = 60.0,
    random_seed: Optional[int] = None
) -> Dict[str, Any]:
    """
    Solve the N-Queens problem using Min-Conflicts Hill Climbing with Random Restarts.
    
    Parameters:
        n (int): Number of queens (N x N board).
        max_restarts (int): Maximum number of random restarts allowed.
        max_steps_per_restart (Optional[int]): Step limit per restart (defaults to max(100, 3 * n)).
        max_time (float): Timeout in seconds.
        random_seed (Optional[int]): Random seed for reproducible runs.
        
    Returns:
        dict: Performance metrics and solution dictionary containing:
            - n: Size of the board
            - success: True if a 0-conflict solution was found, False otherwise
            - board: List[int] where board[col] = row (or best configuration)
            - execution_time: Time taken in seconds
            - restarts: Number of random restarts used
            - conflicts: Final conflict count (0 if solved)
            - total_steps: Total min-conflict move steps executed
            - message: Human-readable status description
    """
    if random_seed is not None:
        random.seed(random_seed)

    # Validate input
    if not isinstance(n, int) or n < 1:
        return {
            "n": n,
            "success": False,
            "board": None,
            "execution_time": 0.0,
            "restarts": 0,
            "conflicts": 0,
            "total_steps": 0,
            "message": f"Invalid board size N = {n}. N must be a positive integer >= 1."
        }

    # N = 1 trivial
    if n == 1:
        return {
            "n": 1,
            "success": True,
            "board": [0],
            "execution_time": 0.00001,
            "restarts": 0,
            "conflicts": 0,
            "total_steps": 0,
            "message": "N=1 solved trivially."
        }

    # N = 2 and N = 3 are mathematically impossible
    if n in (2, 3):
        return {
            "n": n,
            "success": False,
            "board": None,
            "execution_time": 0.001,
            "restarts": 0,
            "conflicts": 1,
            "total_steps": 0,
            "message": f"Mathematically proven: No valid solution exists for N = {n}."
        }

    if max_steps_per_restart is None:
        max_steps_per_restart = max(150, 4 * n)

    solver = MinConflictsSolver(n)
    start_time = time.perf_counter()
    restarts_count = 0
    total_steps = 0
    best_board: Optional[List[int]] = None
    min_conflicts_seen = float("inf")

    for restart in range(max_restarts + 1):
        if time.perf_counter() - start_time > max_time:
            break

        solver.initialize_random_board()
        if restart > 0:
            restarts_count += 1

        for step in range(max_steps_per_restart):
            total_steps += 1
            conflicted_cols = solver.get_conflicted_columns()

            # Goal test: 0 conflicts found
            if not conflicted_cols:
                elapsed = time.perf_counter() - start_time
                return {
                    "n": n,
                    "success": True,
                    "board": list(solver.board),
                    "execution_time": elapsed,
                    "restarts": restarts_count,
                    "conflicts": 0,
                    "total_steps": total_steps,
                    "message": (
                        f"Solution found in {elapsed:.4f}s with {restarts_count} restarts "
                        f"and {total_steps} total steps."
                    )
                }

            # Update best configuration seen so far
            current_conflicts = len(conflicted_cols)
            if current_conflicts < min_conflicts_seen:
                min_conflicts_seen = current_conflicts
                best_board = list(solver.board)

            # Pick a conflicted queen at random
            col = random.choice(conflicted_cols)

            # Find row(s) in this column that minimize conflicts
            row_conflicts = [
                solver.conflicts_if_moved(col, r) for r in range(n)
            ]
            min_c = min(row_conflicts)
            best_rows = [r for r, c in enumerate(row_conflicts) if c == min_c]

            # Choose randomly among the minimal conflict rows (breaks ties & avoids cycling)
            chosen_row = random.choice(best_rows)
            solver.move_queen(col, chosen_row)

            # Check timeout periodically
            if total_steps % 500 == 0 and (time.perf_counter() - start_time > max_time):
                break

    elapsed = time.perf_counter() - start_time
    final_conflicts = count_conflicts(best_board) if best_board else solver.conflicts_for_queen(0)

    return {
        "n": n,
        "success": False,
        "board": best_board,
        "execution_time": elapsed,
        "restarts": restarts_count,
        "conflicts": final_conflicts,
        "total_steps": total_steps,
        "message": (
            f"Exceeded budget ({max_restarts} restarts, {total_steps} steps) "
            f"without finding a 0-conflict solution. Best conflicts: {final_conflicts}."
        )
    }


if __name__ == "__main__":
    for test_n in [4, 8, 12, 15, 20]:
        res = solve_n_queens_hill_climbing(test_n)
        print(f"Hill Climbing N={test_n}: Success={res['success']}, Restarts={res['restarts']}, Steps={res['total_steps']}, Time={res['execution_time']:.5f}s")
