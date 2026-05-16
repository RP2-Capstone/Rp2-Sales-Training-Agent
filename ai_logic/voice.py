import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    print(f"AI: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:

            print("Listening...")

            recognizer.adjust_for_ambient_noise(source, duration=1)

            recognizer.pause_threshold = 1.2

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=15
            )

        text = recognizer.recognize_google(audio)

        print(f"You: {text}")

        return text.lower()

    except sr.WaitTimeoutError:
        print("No speech detected.")
        return None

    except sr.UnknownValueError:
        print("Could not understand audio.")
        return None

    except Exception as e:
        print("Voice recognition error:", e)
        return None