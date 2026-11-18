"""
N-Queens: Backtracking Algorithm
Subject: Artificial Intelligence | Unit II: Search & Optimization (CO2)

This module implements the classic recursive Backtracking algorithm for solving
the N-Queens puzzle by systematically exploring candidate placements column-by-column
and pruning dead ends as soon as a constraint (row or diagonal conflict) is violated.
"""

import time
from typing import List, Optional, Dict, Any


def is_safe(board: List[int], row: int, col: int) -> bool:
    """
    Check if placing a queen at (row, col) is safe from previously placed queens.
    
    Parameters:
        board (List[int]): Current row positions for columns 0 to col-1.
        row (int): Candidate row index for the queen in column `col`.
        col (int): Candidate column index (0-indexed).
        
    Returns:
        bool: True if safe (no row or diagonal attacks), False otherwise.
    """
    for prev_col in range(col):
        prev_row = board[prev_col]
        # Check if another queen is in the same row
        if prev_row == row:
            return False
        # Check diagonal conflicts: |row1 - row2| == |col1 - col2|
        if abs(prev_row - row) == abs(prev_col - col):
            return False
    return True


def count_conflicts(board: Optional[List[int]]) -> int:
    """
    Calculate the total number of conflicting pairs of queens on the board.
    
    Parameters:
        board (Optional[List[int]]): List where board[col] = row.
        
    Returns:
        int: Number of conflicting queen pairs.
    """
    if board is None:
        return 0
    n = len(board)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            # Same row conflict
            if board[i] == board[j]:
                conflicts += 1
            # Diagonal conflict
            elif abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts


def solve_n_queens_backtracking(n: int, max_time: float = 60.0) -> Dict[str, Any]:
    """
    Solve the N-Queens problem using Recursive Backtracking.
    
    Parameters:
        n (int): Number of queens (and board dimension N x N).
        max_time (float): Maximum allowed runtime in seconds before timeout.
        
    Returns:
        dict: Performance metrics and solution dictionary containing:
            - n: Size of the board
            - success: True if a valid solution was found, False otherwise
            - board: List[int] where board[col] = row (or None)
            - execution_time: Time taken in seconds
            - restarts: 0 (deterministic algorithm, no restarts)
            - conflicts: 0 if solved, else remaining conflicts
            - recursive_calls: Total recursive exploration calls made
            - message: Human-readable status description
    """
    # Validate input
    if not isinstance(n, int) or n < 1:
        return {
            "n": n,
            "success": False,
            "board": None,
            "execution_time": 0.0,
            "restarts": 0,
            "conflicts": 0,
            "recursive_calls": 0,
            "message": f"Invalid board size N = {n}. N must be a positive integer >= 1."
        }

    # Handle N = 1 (trivial solution)
    if n == 1:
        return {
            "n": 1,
            "success": True,
            "board": [0],
            "execution_time": 0.00001,
            "restarts": 0,
            "conflicts": 0,
            "recursive_calls": 1,
            "message": "N=1 solved trivially."
        }

    # Handle N = 2 and N = 3 (mathematically impossible to solve)
    if n in (2, 3):
        start_time = time.perf_counter()
        # Still run search to confirm no solution exists
        board = [-1] * n
        call_counter = [0]
        
        def backtrack_impossible(col: int) -> bool:
            call_counter[0] += 1
            if col >= n:
                return True
            for r in range(n):
                if is_safe(board, r, col):
                    board[col] = r
                    if backtrack_impossible(col + 1):
                        return True
                    board[col] = -1
            return False
            
        backtrack_impossible(0)
        elapsed = time.perf_counter() - start_time
        return {
            "n": n,
            "success": False,
            "board": None,
            "execution_time": elapsed,
            "restarts": 0,
            "conflicts": 0,
            "recursive_calls": call_counter[0],
            "message": f"Mathematically proven: No valid solution exists for N = {n}."
        }

    board = [-1] * n
    # Constraint masks for O(1) safety checks to handle larger N efficiently
    row_used = [False] * n
    diag1_used = [False] * (2 * n - 1)  # row + col
    diag2_used = [False] * (2 * n - 1)  # row - col + (n - 1)
    
    recursive_calls = 0
    start_time = time.perf_counter()
    timeout_occurred = False

    def backtrack(col: int) -> bool:
        nonlocal recursive_calls, timeout_occurred
        recursive_calls += 1

        # Check timeout every 2048 calls
        if (recursive_calls & 2047) == 0:
            if time.perf_counter() - start_time > max_time:
                timeout_occurred = True
                return False

        # Base case: all columns have a queen safely placed
        if col >= n:
            return True

        for r in range(n):
            d1 = r + col
            d2 = r - col + (n - 1)

            if not row_used[r] and not diag1_used[d1] and not diag2_used[d2]:
                # Place queen
                board[col] = r
                row_used[r] = True
                diag1_used[d1] = True
                diag2_used[d2] = True

                # Recurse to next column
                if backtrack(col + 1):
                    return True

                if timeout_occurred:
                    return False

                # Backtrack: undo placement
                board[col] = -1
                row_used[r] = False
                diag1_used[d1] = False
                diag2_used[d2] = False

        return False

    solved = backtrack(0)
    elapsed_time = time.perf_counter() - start_time

    if timeout_occurred:
        return {
            "n": n,
            "success": False,
            "board": None,
            "execution_time": elapsed_time,
            "restarts": 0,
            "conflicts": 0,
            "recursive_calls": recursive_calls,
            "message": f"Backtracking timed out after {elapsed_time:.3f}s for N = {n}."
        }

    if solved:
        return {
            "n": n,
            "success": True,
            "board": list(board),
            "execution_time": elapsed_time,
            "restarts": 0,
            "conflicts": 0,
            "recursive_calls": recursive_calls,
            "message": f"Solution found successfully in {elapsed_time:.4f}s with {recursive_calls} recursive calls."
        }
    else:
        return {
            "n": n,
            "success": False,
            "board": None,
            "execution_time": elapsed_time,
            "restarts": 0,
            "conflicts": 0,
            "recursive_calls": recursive_calls,
            "message": f"No solution found for N = {n}."
        }


if __name__ == "__main__":
    # Self-test demonstration
    for test_n in [4, 8, 12, 15]:
        res = solve_n_queens_backtracking(test_n)
        print(f"Backtracking N={test_n}: Success={res['success']}, Time={res['execution_time']:.5f}s, Calls={res['recursive_calls']}")
