import subprocess
import os
import pyautogui
import time
import webbrowser
import re
import psutil
import platform
from urllib.parse import quote_plus


# =========================================================
# CHROME CONFIGURATION
# =========================================================

# IMPORTANT:
# Open chrome://version in your Vinodh Raj Chrome profile.
#
# Look at:
# Profile Path
#
# Example:
# C:\Users\Lenovo PC\AppData\Local\Google\Chrome\User Data\Profile 2
#
# Then use:
# CHROME_PROFILE_DIRECTORY = "Profile 2"
#
# If the path ends with Default, use "Default".

CHROME_PROFILE_DIRECTORY = "Default"


CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
]


def get_chrome_path():

    for chrome_path in CHROME_PATHS:

        if os.path.exists(chrome_path):
            return chrome_path

    return None


def launch_chrome(url=None):

    chrome_path = get_chrome_path()

    if not chrome_path:
        return False

    command = [
        chrome_path,
        f"--profile-directory={CHROME_PROFILE_DIRECTORY}"
    ]

    if url:
        command.append(url)

    subprocess.Popen(command)

    return True


# =========================================================
# OPEN APPLICATIONS
# =========================================================

def open_notepad():

    subprocess.Popen(["notepad.exe"])

    return "Notepad opened successfully."


def open_task_manager():

    os.system("start taskmgr")

    return "Task Manager opened successfully."


def open_calculator():

    subprocess.Popen(["calc.exe"])

    return "Calculator opened successfully."


def open_camera():

    os.system("start microsoft.windows.camera:")

    return "Camera opened successfully."


def take_picture():

    # Open Windows Camera first
    open_camera()

    # Wait for the camera application
    time.sleep(3)

    # Windows Camera generally supports Space as shutter
    pyautogui.press("space")

    return "Picture capture command sent to the Camera app."


def open_chrome():

    if launch_chrome():

        return "Chrome opened successfully using your selected profile."

    return "Chrome was not found."


def open_file_explorer():

    subprocess.Popen(["explorer.exe"])

    return "File Explorer opened successfully."


# =========================================================
# OPEN FOLDERS
# =========================================================

def open_downloads():

    path = os.path.join(
        os.path.expanduser("~"),
        "Downloads"
    )

    os.startfile(path)

    return "Downloads folder opened successfully."


def open_documents():

    path = os.path.join(
        os.path.expanduser("~"),
        "Documents"
    )

    os.startfile(path)

    return "Documents folder opened successfully."


# =========================================================
# WEBSITE
# =========================================================

def open_website(url):

    url = str(url).strip()

    if not url.startswith(
        (
            "http://",
            "https://"
        )
    ):
        url = "https://" + url

    if launch_chrome(url):

        return f"Opened {url} in Chrome using your selected profile."

    # Fallback
    webbrowser.open(url)

    return f"Opened website {url}."


# =========================================================
# GOOGLE SEARCH
# =========================================================

def google_search(query):

    encoded_query = quote_plus(
        str(query)
    )

    search_url = (
        "https://www.google.com/search?q="
        + encoded_query
    )

    if launch_chrome(search_url):

        return (
            f"Searching Google for {query} "
            f"using your selected Chrome profile."
        )

    webbrowser.open(search_url)

    return f"Searching Google for {query}."


# =========================================================
# SCREENSHOT
# =========================================================

def take_screenshot():

    # Main project directory
    project_root = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    # All Buddy screenshots go here
    screenshot_folder = os.path.join(
        project_root,
        "botscreenshot"
    )

    os.makedirs(
        screenshot_folder,
        exist_ok=True
    )

    filename = (
        f"screenshot_{int(time.time())}.png"
    )

    filepath = os.path.join(
        screenshot_folder,
        filename
    )

    screenshot = pyautogui.screenshot()

    screenshot.save(filepath)

    return (
        f"Screenshot saved successfully "
        f"in the botscreenshot folder as {filename}."
    )


# =========================================================
# TYPE TEXT
# =========================================================

def type_text(text):

    time.sleep(1.5)

    text = str(text)

    lines = text.splitlines()

    for index, line in enumerate(lines):

        pyautogui.write(
            line,
            interval=0.04
        )

        if index < len(lines) - 1:
            pyautogui.press("enter")

    return "Text typed successfully."


# =========================================================
# CALCULATOR
# =========================================================

def calculate_in_calculator(expression):

    expression = str(expression)

    if not re.fullmatch(
        r"[0-9+\-*/(). ]+",
        expression
    ):
        return "That calculation is not supported."

    open_calculator()

    time.sleep(2)

    pyautogui.write(
        expression,
        interval=0.15
    )

    pyautogui.press("enter")

    return (
        f"Calculated {expression} "
        f"in Calculator."
    )


# =========================================================
# VOLUME CONTROL
# =========================================================

def volume_up():

    pyautogui.press(
        "volumeup",
        presses=3,
        interval=0.1
    )

    return "Volume increased."


def volume_down():

    pyautogui.press(
        "volumedown",
        presses=3,
        interval=0.1
    )

    return "Volume decreased."


def mute_volume():

    pyautogui.press(
        "volumemute"
    )

    return "Volume mute toggled."


# =========================================================
# BATTERY STATUS
# =========================================================

def get_battery_status():

    battery = psutil.sensors_battery()

    if battery is None:

        return (
            "Battery information "
            "is not available."
        )

    percentage = battery.percent

    status = (
        "charging"
        if battery.power_plugged
        else "not charging"
    )

    return (
        f"Battery is at {percentage} percent "
        f"and is {status}."
    )


# =========================================================
# CPU USAGE
# =========================================================

def get_cpu_usage():

    usage = psutil.cpu_percent(
        interval=1
    )

    return (
        f"Current CPU usage "
        f"is {usage} percent."
    )


# =========================================================
# MEMORY / RAM
# =========================================================

def get_memory_usage():

    memory = psutil.virtual_memory()

    available_gb = round(
        memory.available / (1024 ** 3),
        1
    )

    return (
        f"RAM usage is {memory.percent} percent. "
        f"Available memory is {available_gb} GB."
    )


# =========================================================
# SYSTEM INFORMATION
# =========================================================

def get_system_info():

    system = platform.system()

    release = platform.release()

    machine = platform.machine()

    processor = platform.processor()

    return (
        f"You are running {system} {release}. "
        f"System architecture is {machine}. "
        f"Processor information is {processor}."
    )


# =========================================================
# CLOSE APPLICATIONS
# =========================================================

def close_notepad():

    result = os.system(
        "taskkill /F /IM notepad.exe >nul 2>&1"
    )

    if result == 0:
        return "Notepad closed successfully."

    return "Notepad is not currently running."


def close_calculator():

    result1 = os.system(
        "taskkill /F /IM CalculatorApp.exe >nul 2>&1"
    )

    result2 = os.system(
        "taskkill /F /IM Calculator.exe >nul 2>&1"
    )

    if result1 == 0 or result2 == 0:

        return "Calculator closed successfully."

    return "Calculator is not currently running."


def close_chrome():

    result = os.system(
        "taskkill /F /IM chrome.exe >nul 2>&1"
    )

    if result == 0:

        return "Chrome closed successfully."

    return "Chrome is not currently running."