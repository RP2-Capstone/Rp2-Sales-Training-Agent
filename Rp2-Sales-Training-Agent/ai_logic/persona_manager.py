import random

def get_persona(persona_type):

    personas = {
        "beginner": [
            "I’m new to this field…",
            "I don’t have coding experience…"
        ],
        "skeptical": [
            "I’m not sure if this is worth it…",
            "Will this actually help me get a job?"
        ],
        "interested": [
            "This sounds interesting…",
            "I really want to learn this…"
        ]
    }

    return random.choice(personas.get(persona_type, ["I’m just exploring options…"]))