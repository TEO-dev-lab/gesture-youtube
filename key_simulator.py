import platform
import subprocess


class KeySimulator:
    def __init__(self):
        self.os_name = platform.system()
        self.pyautogui = None

        if self.os_name == "Linux":
            self._check_xdotool()
        elif self.os_name == "Windows":
            import pyautogui
            pyautogui.FAILSAFE = True
            pyautogui.PAUSE = 0.1
            self.pyautogui = pyautogui
        else:
            raise SystemError(f"Unsupported OS: {self.os_name}")

    def _check_xdotool(self):
        try:
            subprocess.run(["xdotool", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("xdotool not installed. Run: sudo pacman -S xdotool")
            raise

    def _send_key(self, key):
        if self.os_name == "Linux":
            subprocess.run(["xdotool", "key", key], capture_output=True)
        elif self.os_name == "Windows":
            self.pyautogui.press(key)

    def next_video(self):
        """Next video"""
        self._send_key("Down" if self.os_name == "Linux" else "down")
        print("Next video")

    def prev_video(self):
        """Prev video"""
        self._send_key("Up" if self.os_name == "Linux" else "up")
        print("Prev video")