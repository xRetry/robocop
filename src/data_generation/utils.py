import subprocess

def exec_command(command: str):
    output = subprocess.run(command.split(" "), capture_output=True)
    
