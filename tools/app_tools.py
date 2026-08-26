import subprocess
import os
import pyautogui
import time
import webbrowser
import re
import psutil
import platform


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


def open_chrome():
    try:
        subprocess.Popen(
            ["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"]
        )
        return "Chrome opened successfully."

    except FileNotFoundError:
        try:
            subprocess.Popen(
                ["C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"]
            )
            return "Chrome opened successfully."

        except FileNotFoundError:
            return "Chrome was not found."


def open_file_explorer():
    subprocess.Popen(["explorer.exe"])
    return "File Explorer opened successfully."


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


def open_website(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    webbrowser.open(url)

    return f"Opened website {url}"


def google_search(query):
    search_url = (
        "https://www.google.com/search?q="
        + query.replace(" ", "+")
    )

    webbrowser.open(search_url)

    return f"Searching Google for {query}"


def take_screenshot():
    filename = f"screenshot_{int(time.time())}.png"

    screenshot = pyautogui.screenshot()

    screenshot.save(filename)

    return f"Screenshot saved as {filename}"


def type_text(text):
    time.sleep(1.5)

    pyautogui.write(
        text,
        interval=0.05
    )

    return f"Typed: {text}"


def calculate_in_calculator(expression):
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

    return f"Calculated {expression} in Calculator."


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
    pyautogui.press("volumemute")

    return "Volume mute toggled."


def get_battery_status():
    battery = psutil.sensors_battery()

    if battery is None:
        return "Battery information is not available."

    percentage = battery.percent

    if battery.power_plugged:
        status = "charging"
    else:
        status = "not charging"

    return (
        f"Battery is at {percentage} percent "
        f"and is {status}."
    )


def get_cpu_usage():
    usage = psutil.cpu_percent(
        interval=1
    )

    return (
        f"Current CPU usage is "
        f"{usage} percent."
    )


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