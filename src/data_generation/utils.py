"""
This file contains utility functions, which are used across various other files.
"""

import subprocess

def exec_command(command: str):
    """Executes the provided terminal command."""

    output = subprocess.run(command.split(" "), capture_output=True)
    
