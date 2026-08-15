# key_simulator.py
import subprocess

class KeySimulator:
    def __init__(self):
        # Checks if xdotool installed
        try:
            subprocess.run(["xdotool", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("xdotool not installed. Run: sudo pacman -S xdotool")
            raise
    
    def _send_key(self, key):
        """Sends global key"""
        subprocess.run(["xdotool", "key", key], capture_output=True)
    
    def next_video(self):
        """Next video"""
        self._send_key("Down")
        print("Next video")
    
    def prev_video(self):
        """Prev video"""
        self._send_key("Up")
        print("Prev video")