import threading

from voice_input import listen_command
from speech_output import speak
from intent_parser import get_intent

from tools.app_tools import (
    open_notepad,
    open_task_manager,
    open_calculator,
    open_camera,
    take_picture,
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
    close_chrome,
)


ASSISTANT_NAME = "Buddy"


APP_TOOLS = {
    "notepad": open_notepad,
    "task_manager": open_task_manager,
    "calculator": open_calculator,
    "camera": open_camera,
    "chrome": open_chrome,
    "file_explorer": open_file_explorer,
}


FOLDER_TOOLS = {
    "downloads": open_downloads,
    "documents": open_documents,
}


CLOSE_APP_TOOLS = {
    "notepad": close_notepad,
    "calculator": close_calculator,
    "chrome": close_chrome,
}


class BuddyAssistant:

    def __init__(self):

        self.running = False

        self.thread = None

        self.stop_event = threading.Event()

        self.messages = []

        self.status = "Stopped"

        self.lock = threading.Lock()


    # =====================================================
    # MESSAGE HANDLING
    # =====================================================

    def add_message(
        self,
        role,
        content
    ):

        with self.lock:

            self.messages.append(
                {
                    "role": role,
                    "content": str(content)
                }
            )

            if len(self.messages) > 50:
                self.messages.pop(0)


    def get_messages(self):

        with self.lock:

            return list(
                self.messages
            )


    # =====================================================
    # EXECUTE INTENT
    # =====================================================

    def execute_intent(
        self,
        intent
    ):

        steps = intent.get(
            "steps",
            []
        )

        if not steps:

            return (
                "I couldn't find an action "
                "to perform."
            )


        results = []


        for step in steps:

            action = step.get(
                "action"
            )


            try:

                # -----------------------------------------
                # OPEN APPLICATION
                # -----------------------------------------

                if action == "open_app":

                    application = step.get(
                        "application"
                    )

                    tool = APP_TOOLS.get(
                        application
                    )

                    if tool:

                        results.append(
                            tool()
                        )

                    else:

                        results.append(
                            f"I cannot open "
                            f"{application} yet."
                        )


                # -----------------------------------------
                # CAMERA PICTURE
                # -----------------------------------------

                elif action == "take_picture":

                    results.append(
                        take_picture()
                    )


                # -----------------------------------------
                # OPEN FOLDER
                # -----------------------------------------

                elif action == "open_folder":

                    folder = step.get(
                        "folder"
                    )

                    tool = FOLDER_TOOLS.get(
                        folder
                    )

                    if tool:

                        results.append(
                            tool()
                        )

                    else:

                        results.append(
                            f"I cannot open "
                            f"{folder} yet."
                        )


                # -----------------------------------------
                # TYPE TEXT
                # -----------------------------------------

                elif action == "type_text":

                    text = step.get(
                        "text"
                    )

                    if text:

                        results.append(
                            type_text(text)
                        )


                # -----------------------------------------
                # WEBSITE
                # -----------------------------------------

                elif action == "open_website":

                    url = step.get(
                        "url"
                    )

                    if url:

                        results.append(
                            open_website(url)
                        )


                # -----------------------------------------
                # GOOGLE SEARCH
                # -----------------------------------------

                elif action == "google_search":

                    query = step.get(
                        "query"
                    )

                    if query:

                        results.append(
                            google_search(query)
                        )


                # -----------------------------------------
                # SCREENSHOT
                # -----------------------------------------

                elif action == "take_screenshot":

                    results.append(
                        take_screenshot()
                    )


                # -----------------------------------------
                # CALCULATOR
                # -----------------------------------------

                elif action == "calculate":

                    expression = step.get(
                        "expression"
                    )

                    if expression:

                        results.append(
                            calculate_in_calculator(
                                expression
                            )
                        )


                # -----------------------------------------
                # VOLUME
                # -----------------------------------------

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


                # -----------------------------------------
                # SYSTEM
                # -----------------------------------------

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


                # -----------------------------------------
                # CLOSE APPLICATION
                # -----------------------------------------

                elif action == "close_app":

                    application = step.get(
                        "application"
                    )

                    tool = CLOSE_APP_TOOLS.get(
                        application
                    )

                    if tool:

                        results.append(
                            tool()
                        )

                    else:

                        results.append(
                            f"I cannot close "
                            f"{application} yet."
                        )


                else:

                    results.append(
                        f"The action {action} "
                        f"is not supported yet."
                    )


            except Exception as e:

                print(
                    f"Tool execution error "
                    f"for {action}:",
                    e
                )

                results.append(
                    f"I couldn't complete "
                    f"the {action} action."
                )


        return " ".join(
            results
        )


    # =====================================================
    # PROCESS USER REQUEST
    # =====================================================

    def process_request(
        self,
        user_input,
        speak_response=True
    ):

        if not user_input:
            return None


        try:

            self.status = "Thinking"


            self.add_message(
                "user",
                user_input
            )


            intent = get_intent(
                user_input
            )


            print(
                "Intent:",
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


            elif request_type == "command":

                self.status = "Executing"

                response = self.execute_intent(
                    intent
                )


            else:

                response = (
                    "Sorry, I didn't understand that."
                )


            self.add_message(
                "assistant",
                response
            )


            print(
                f"{ASSISTANT_NAME}:",
                response
            )


            if speak_response:

                speak(
                    response
                )


            if self.running:

                self.status = "Listening"

            else:

                self.status = "Stopped"


            return response


        except Exception as e:

            print(
                "Buddy error:",
                e
            )


            response = (
                "Sorry, something went wrong."
            )


            self.add_message(
                "assistant",
                response
            )


            if speak_response:

                speak(
                    response
                )


            if self.running:

                self.status = "Listening"

            else:

                self.status = "Stopped"


            return response


    # =====================================================
    # TEXT MODE
    # =====================================================

    def process_text_request(
        self,
        user_input
    ):

        return self.process_request(
            user_input,
            speak_response=False
        )


    # =====================================================
    # WAKE WORD
    # =====================================================

    def is_wake_word(
        self,
        text
    ):

        text = (
            text
            .lower()
            .strip()
        )


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


    # =====================================================
    # VOICE LOOP
    # =====================================================

    def assistant_loop(self):

        self.running = True

        self.status = (
            "Waiting for wake word"
        )


        print(
            "Buddy assistant started."
        )


        speak(
            "Buddy is ready."
        )


        while not self.stop_event.is_set():

            self.status = (
                "Waiting for wake word"
            )


            print(
                'Waiting for wake word: '
                '"Hey Buddy"'
            )


            user_input = (
                listen_command()
            )


            if self.stop_event.is_set():
                break


            if not user_input:
                continue


            if not self.is_wake_word(
                user_input
            ):
                continue


            self.add_message(
                "user",
                user_input
            )


            print(
                "Wake word detected."
            )


            response = (
                "Hi! What can I do for you?"
            )


            self.add_message(
                "assistant",
                response
            )


            speak(
                response
            )


            while not self.stop_event.is_set():

                self.status = "Listening"


                print(
                    "Listening for command..."
                )


                command = (
                    listen_command()
                )


                if self.stop_event.is_set():
                    break


                if not command:
                    continue


                text = (
                    command
                    .lower()
                    .strip()
                )


                if text in [
                    "go to sleep",
                    "sleep",
                    "stop listening"
                ]:

                    response = (
                        "Okay. I'll wait for you."
                    )


                    self.add_message(
                        "user",
                        command
                    )


                    self.add_message(
                        "assistant",
                        response
                    )


                    speak(
                        response
                    )

                    break


                self.process_request(
                    command,
                    speak_response=True
                )


        self.running = False

        self.status = "Stopped"


        print(
            "Buddy assistant stopped."
        )


    # =====================================================
    # START / STOP
    # =====================================================

    def start(self):

        if self.running:
            return


        self.stop_event.clear()


        self.thread = threading.Thread(
            target=self.assistant_loop,
            daemon=True
        )


        self.thread.start()


    def stop(self):

        if not self.running:
            return


        self.stop_event.set()

        self.running = False

        self.status = "Stopped"


        print(
            "Stop requested."
        )


    # =====================================================
    # CLEAR CHAT
    # =====================================================

    def clear_chat(self):

        with self.lock:

            self.messages.clear()