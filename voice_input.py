import speech_recognition as sr


def listen_command():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("\nListening... Speak now.")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=8
            )

        text = recognizer.recognize_google(audio)

        print("You said:", text)

        return text

    except sr.WaitTimeoutError:
        print("AI: I didn't hear anything. Please try again.")
        return None

    except sr.UnknownValueError:
        print("AI: I heard something, but couldn't understand it.")
        return None

    except sr.RequestError as e:
        print("Speech recognition service error:", e)
        return None

    except Exception as e:
        print("Microphone error:", e)
        return None