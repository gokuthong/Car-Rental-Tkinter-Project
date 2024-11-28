import subprocess
def open_script(filename, window):
    """Opens a script and closes the current window."""
    try:
        subprocess.Popen(["python", filename])  # Open the specified script
        window.destroy()  # Close the current window
    except Exception as e:
        print(f"Error redirecting to {filename}: {e}")


