import random
from ai_logic.memory import update_memory, get_context

def get_response(user_message, persona, history):

    msg = user_message.lower().strip()

    if any(word in msg for word in ["hi", "hello", "hey"]):
        reply = random.choice([
            "Hey! I'm actually looking for a course. Can you help me?",
            "Hi! I'm a bit confused about which course to choose.",
            "Hey! I want to learn something new but not sure where to start."
        ])

        update_memory(history, user_message, reply)
        return reply

    if "background" in msg:
        reply = random.choice([
            "I'm actually from a non-technical background.",
            "I'm a beginner. I haven’t done coding before.",
            "I’m just starting out in tech."
        ])

        update_memory(history, user_message, reply)
        return reply

    if "data science" in msg:
        reply = """
I’ve heard Data Science is really popular.

But I have doubts:

• Is coding difficult?
• Do I need strong math?
• Will I get real projects?

Can you explain simply?
"""
        update_memory(history, user_message, reply)
        return reply

    if "data analytics" in msg:
        reply = """
Data Analytics sounds interesting.

But I want to know:

• Is it easier than Data Science?
• Will I learn dashboards and Excel?
• Can beginners get jobs quickly?

What do you think?
"""
        update_memory(history, user_message, reply)
        return reply

    if "agentic ai" in msg or "ai" in msg:
        reply = """
Agentic AI sounds futuristic.

But honestly:

• Is it too advanced?
• Do I need Python?
• Is this related to ChatGPT?

Can beginners learn this?
"""
        update_memory(history, user_message, reply)
        return reply

    reply = """
I'm still confused about which course is best for me.

Can you guide me like a beginner?
"""

    update_memory(history, user_message, reply)
    return reply