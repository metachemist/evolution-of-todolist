#!/usr/bin/env python3
"""
Root entry point for the todo application.
Detects whether to run in interactive mode or traditional CLI mode.
"""

import sys
import os

def main():
    """
    Main entry point that determines mode based on command-line arguments.
    - If args provided -> Run Typer CLI (existing logic)
    - If no args -> Run Interactive Mode (new logic)
    """
    # Add the src directory to the path so we can import from cli
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    # If command-line arguments are provided, run the CLI mode
    if len(sys.argv) > 1:
        # Import and run the existing Typer CLI app
        from cli.main import app
        app()
    else:
        # Import and run the interactive mode
        from cli.interactive import interactive_main
        interactive_main()


if __name__ == "__main__":
    main()