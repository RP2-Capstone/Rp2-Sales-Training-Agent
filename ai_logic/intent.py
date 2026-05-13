def detect_intent(message):

    msg = message.lower()

    if "hi" in msg or "hello" in msg:
        return "greeting"

    if "course" in msg:
        return "course"

    if "price" in msg or "fee" in msg:
        return "pricing"

    if "job" in msg:
        return "career"

    return "general"