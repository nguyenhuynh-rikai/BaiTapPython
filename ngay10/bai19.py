import subprocess

def run_git_status():
    result = subprocess.run(['git', 'status'], capture_output=True, text=True)
    print("System Output:\n", result.stdout)

run_git_status()