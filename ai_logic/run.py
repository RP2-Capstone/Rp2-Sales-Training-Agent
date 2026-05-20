from ai_logic.chatbot import get_response
from ai_logic.voice import speak, listen

print("🎤 Voice AI started (type 'exit' to stop)\n")

while True:

    user_input = listen()

    if not user_input:
        continue

    if user_input.lower() == "exit":
        speak("Goodbye!")
        break

    response = get_response(user_input)

    print("AI:", response)

    speak(response)