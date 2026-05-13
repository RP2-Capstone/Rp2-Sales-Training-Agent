def update_memory(history, user_message, ai_response):
    history.append({
        "user": user_message,
        "ai": ai_response
    })


def get_context(history, limit=3):
    context = history[-limit:]
    formatted = ""

    for item in context:
        formatted += f"User: {item['user']}\nAI: {item['ai']}\n"

    return formatted