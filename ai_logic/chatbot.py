import random

from ai_logic.llm import ask_llm
from ai_logic.config import USE_LLM


def offline_reply(message):

    msg = message.lower()

    greetings = [
        "hey",
        "hello",
        "hi",
        "good morning",
        "good evening",
        "welcome"
    ]

    if any(word in msg for word in greetings):
        return random.choice([
            "Hi sir, I want to know more about your courses.",
            "Hello, I am interested in AI and Data Science.",
            "Hi, can you explain which course is best for beginners?"
        ])

    if "data science" in msg:
        return random.choice([
            "Is Data Science difficult for beginners?",
            "Do we learn machine learning in Data Science?",
            "Can I get an AI job after completing Data Science?"
        ])

    if "data analytics" in msg:
        return random.choice([
            "Do we learn Power BI and SQL in Data Analytics?",
            "Is Data Analytics good for freshers?",
            "Can I switch to Data Science later from Data Analytics?"
        ])

    if "agentic ai" in msg or "ai" in msg:
        return random.choice([
            "Agentic AI sounds interesting. Do we build AI agents?",
            "Will we learn ChatGPT and automation tools?",
            "Is Agentic AI good for future careers?"
        ])

    if "job" in msg or "career" in msg:
        return random.choice([
            "Do you provide placement support?",
            "What kind of jobs can I get after the course?",
            "Are these courses good for working abroad?"
        ])

    if "python" in msg:
        return random.choice([
            "I am a beginner. Can I learn Python easily?",
            "Do you teach Python from basics?",
            "Is Python enough to start AI learning?"
        ])

    if "fees" in msg or "price" in msg:
        return random.choice([
            "Can I pay the fees in installments?",
            "What is the total course fee?",
            "Do you have any discounts for students?"
        ])

    if "duration" in msg or "time" in msg:
        return random.choice([
            "How many months is the course?",
            "Is there a fast-track program available?",
            "How many hours should I study daily?"
        ])

    return random.choice([
        "Can you explain more about the course?",
        "Which course is best for AI careers?",
        "Do I need coding experience before joining?",
        "Can beginners join these programs?",
        "Will there be real projects in the course?"
    ])


def get_response(user_message):

    if USE_LLM:

        prompt = f"""
You are acting like a student interested in courses.

The human user is the trainer/counsellor.

Reply naturally like a real student.

Ask questions sometimes.

Keep replies short and conversational.

User: {user_message}
"""

        llm_reply = ask_llm(prompt)

        if llm_reply:
            return llm_reply

    return offline_reply(user_message)