# T-005: Interactive TUI with Rich Tables

## Task Description
Implement an interactive menu-driven interface with rich table visualizations as specified in the updated feature specification. This includes adding the rich library, creating an interactive module with a menu loop, and implementing a root-level main.py that detects whether to run in interactive mode or traditional CLI mode.

## Implementation Plan Reference
Based on: `@specs/2-plan/phase-1-console.md` - Interactive TUI Module section

## Requirements
- Add `rich` library to requirements.txt
- Create `src/cli/interactive.py` module with interactive menu loop
- Implement `rich.table.Table` to render task lists with columns: ID, Status, Title, Created At
- Implement color-coding: Green for "completed", Yellow for "pending"
- Create root-level `src/main.py` that detects:
  - If args provided -> Run Typer CLI (existing logic from main.py)
  - If no args -> Run Interactive Mode (new logic)
- Implement a `while True` loop that accepts single-key inputs (1-6) for navigation:
  - 1: Add Task
  - 2: List Tasks
  - 3: Update Task
  - 4: Complete Task
  - 5: Delete Task
  - 6: Exit
- Clear screen between actions for clarity

## Files to Create/Modify
- requirements.txt (add rich)
- src/main.py (root entry point)
- src/cli/interactive.py (interactive menu logic)
- Update existing src/cli/main.py to be compatible with new structure

## Dependencies
- T-001: Setup Project Structure
- T-002: Core Logic (Task Model and TaskManager)
- T-003: CLI Interface

## Acceptance Criteria
- [x] Rich library is added to requirements.txt
- [x] Interactive menu displays with options (1-6) as specified
- [x] Task list displays in a formatted table with ID, Status, Title, Created At columns
- [x] Status is color-coded (Green for completed, Yellow for pending)
- [x] Menu accepts single-key inputs (1-6) for navigation
- [x] Root main.py detects arguments and switches between interactive/CLI modes
- [x] Screen clears between actions for clarity
- [x] All interactive operations work correctly (add, list, update, complete, delete)
- [x] Interactive mode integrates with existing TaskManager

## Status
- Completed: 2026-02-05
- Verified: Interactive TUI fully implemented with rich tables and menu navigation