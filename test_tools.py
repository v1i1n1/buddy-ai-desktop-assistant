from tools.app_tools import (
    open_notepad,
    open_task_manager,
    open_calculator,
    open_camera
)

print("1. Open Notepad")
print("2. Open Task Manager")
print("3. Open Calculator")
print("4. Open Camera")

choice = input("Enter choice: ")

if choice == "1":
    print(open_notepad())

elif choice == "2":
    print(open_task_manager())

elif choice == "3":
    print(open_calculator())

elif choice == "4":
    print(open_camera())

else:
    print("Invalid choice")