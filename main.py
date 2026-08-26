from intent_parser import (
    get_intent,
    add_to_memory,
    clear_memory
)

from voice_input import listen_command
from speech_output import speak

from tools.app_tools import (
    open_notepad,
    open_task_manager,
    open_calculator,
    open_camera,
    open_chrome,
    open_file_explorer,
    open_downloads,
    open_documents,
    open_website,
    google_search,
    take_screenshot,
    type_text,
    calculate_in_calculator,
    volume_up,
    volume_down,
    mute_volume,
    get_battery_status,
    get_cpu_usage,
    get_memory_usage,
    get_system_info,
    close_notepad,
    close_calculator,
    close_chrome
)


ASSISTANT_NAME = "Buddy"


APP_TOOLS = {
    "notepad": open_notepad,
    "task_manager": open_task_manager,
    "calculator": open_calculator,
    "camera": open_camera,
    "chrome": open_chrome,
    "file_explorer": open_file_explorer
}


FOLDER_TOOLS = {
    "downloads": open_downloads,
    "documents": open_documents
}


CLOSE_APP_TOOLS = {
    "notepad": close_notepad,
    "calculator": close_calculator,
    "chrome": close_chrome
}


def execute_intent(intent):
    steps = intent.get("steps", [])

    if not steps:
        return "I couldn't find an action to perform."

    results = []

    for step in steps:
        action = step.get("action")

        if action == "open_app":
            application = step.get("application")
            tool = APP_TOOLS.get(application)

            if tool is None:
                results.append(
                    f"I cannot open {application} yet."
                )
                continue

            results.append(tool())

        elif action == "open_folder":
            folder = step.get("folder")
            tool = FOLDER_TOOLS.get(folder)

            if tool is None:
                results.append(
                    f"I cannot open the {folder} folder yet."
                )
                continue

            results.append(tool())

        elif action == "type_text":
            text = step.get("text")

            if not text:
                results.append(
                    "No text was provided."
                )
                continue

            results.append(
                type_text(text)
            )

        elif action == "open_website":
            url = step.get("url")

            if not url:
                results.append(
                    "No website was provided."
                )
                continue

            results.append(
                open_website(url)
            )

        elif action == "google_search":
            query = step.get("query")

            if not query:
                results.append(
                    "No search query was provided."
                )
                continue

            results.append(
                google_search(query)
            )

        elif action == "take_screenshot":
            results.append(
                take_screenshot()
            )

        elif action == "calculate":
            expression = step.get("expression")

            if not expression:
                results.append(
                    "No calculation was provided."
                )
                continue

            results.append(
                calculate_in_calculator(
                    expression
                )
            )

        elif action == "volume_up":
            results.append(
                volume_up()
            )

        elif action == "volume_down":
            results.append(
                volume_down()
            )

        elif action == "mute_volume":
            results.append(
                mute_volume()
            )

        elif action == "battery_status":
            results.append(
                get_battery_status()
            )

        elif action == "cpu_usage":
            results.append(
                get_cpu_usage()
            )

        elif action == "memory_usage":
            results.append(
                get_memory_usage()
            )

        elif action == "system_info":
            results.append(
                get_system_info()
            )

        elif action == "close_app":
            application = step.get("application")
            tool = CLOSE_APP_TOOLS.get(application)

            if tool is None:
                results.append(
                    f"I cannot close {application} yet."
                )
                continue

            results.append(
                tool()
            )

        else:
            results.append(
                f"The action {action} is not supported yet."
            )

    return " ".join(results)


def process_request(user_input):
    try:
        intent = get_intent(
            user_input
        )

        print(
            "\nIntent:",
            intent
        )

        request_type = intent.get(
            "type"
        )

        if request_type == "conversation":
            response = intent.get(
                "response",
                "How can I help you?"
            )

            print(
                f"{ASSISTANT_NAME}:",
                response
            )

            speak(
                response
            )

            add_to_memory(
                user_input,
                response
            )

        elif request_type == "command":
            result = execute_intent(
                intent
            )

            print(
                f"{ASSISTANT_NAME}:",
                result
            )

            speak(
                result
            )

            add_to_memory(
                user_input,
                result
            )

        else:
            response = (
                "Sorry, I didn't understand that."
            )

            print(
                f"{ASSISTANT_NAME}:",
                response
            )

            speak(
                response
            )

    except Exception as e:
        print(
            "Technical error:",
            e
        )

        response = (
            "Sorry, something went wrong."
        )

        print(
            f"{ASSISTANT_NAME}:",
            response
        )

        speak(
            response
        )


def is_wake_word(text):
    text = text.lower().strip()

    wake_words = [
        "hey buddy",
        "buddy",
        "hi buddy",
        "hello buddy"
    ]

    return any(
        wake_word in text
        for wake_word in wake_words
    )


def voice_mode():
    print(
        "\nVoice mode started."
    )

    print(
        "Say: Hey Buddy"
    )

    print(
        "Say: go to sleep to return to wake mode."
    )

    print(
        "Say: return to menu to return "
        "to the main menu.\n"
    )

    while True:
        print(
            "Waiting for wake word: Hey Buddy"
        )

        user_input = listen_command()

        if not user_input:
            continue

        text = user_input.lower().strip()

        if text in [
            "return to menu",
            "back to menu",
            "exit voice mode"
        ]:
            print(
                "\nReturning to main menu..."
            )

            speak(
                "Returning to main menu."
            )

            return

        if not is_wake_word(
            user_input
        ):
            continue

        print(
            "\nWake word detected!"
        )

        response = (
            "Hi! What can I do for you?"
        )

        print(
            f"{ASSISTANT_NAME}:",
            response
        )

        speak(
            response
        )

        while True:
            print(
                "\nListening for your request..."
            )

            command = listen_command()

            if not command:
                continue

            command_text = (
                command.lower().strip()
            )

            if command_text in [
                "go to sleep",
                "sleep",
                "stop listening"
            ]:
                response = (
                    "Okay. I'll wait for you."
                )

                print(
                    f"{ASSISTANT_NAME}:",
                    response
                )

                speak(
                    response
                )

                break

            if command_text in [
                "return to menu",
                "back to menu"
            ]:
                response = (
                    "Returning to main menu."
                )

                print(
                    f"{ASSISTANT_NAME}:",
                    response
                )

                speak(
                    response
                )

                return

            if command_text in [
                "clear memory",
                "forget conversation"
            ]:
                clear_memory()

                response = (
                    "Conversation memory cleared."
                )

                print(
                    f"{ASSISTANT_NAME}:",
                    response
                )

                speak(
                    response
                )

                continue

            if command_text in [
                "exit",
                "quit",
                "shutdown assistant",
                "close assistant"
            ]:
                response = "Goodbye."

                print(
                    f"{ASSISTANT_NAME}:",
                    response
                )

                speak(
                    response
                )

                raise SystemExit

            process_request(
                command
            )


def type_mode():
    print(
        "\nType mode"
    )

    print(
        "Type 'back' to return to the main menu."
    )

    print(
        "Type 'clear memory' to reset conversation memory.\n"
    )

    while True:
        user_input = input(
            "You: "
        ).strip()

        if not user_input:
            continue

        if user_input.lower() == "back":
            return

        if user_input.lower() in [
            "clear memory",
            "forget conversation"
        ]:
            clear_memory()

            print(
                f"{ASSISTANT_NAME}: "
                "Conversation memory cleared."
            )

            speak(
                "Conversation memory cleared."
            )

            continue

        if user_input.lower() in [
            "exit",
            "quit"
        ]:
            print(
                f"{ASSISTANT_NAME}: Goodbye."
            )

            speak(
                "Goodbye."
            )

            raise SystemExit

        process_request(
            user_input
        )


print(
    "===================================="
)
print(
    "         BUDDY AI ASSISTANT"
)
print(
    "===================================="
)

speak(
    "Buddy is ready."
)


while True:
    print(
        "\nChoose mode:"
    )

    print(
        "1. Type"
    )

    print(
        "2. Voice"
    )

    print(
        "3. Exit"
    )

    choice = input(
        "\nEnter choice: "
    ).strip()

    if choice == "1":
        type_mode()

    elif choice == "2":
        voice_mode()

    elif choice == "3":
        print(
            f"{ASSISTANT_NAME}: Goodbye."
        )

        speak(
            "Goodbye."
        )

        break

    else:
        print(
            "Please choose 1, 2, or 3."
        )