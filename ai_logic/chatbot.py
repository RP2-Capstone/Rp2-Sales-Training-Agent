import random

def get_response(user_message):

    msg = user_message.lower()

    responses = {

        "hello": [
            "Hey! Nice to meet you.",
            "Hello! Can you guide me about your courses?",
            "Hi! I'm looking for a good tech course."
        ],

        "hi": [
            "Hi there!",
            "Hey! I want to build my career in tech.",
            "Hello! Which course is best for beginners?"
        ],

        "data science": [
            "I've heard Data Science has good salary opportunities. Is coding difficult?",
            "Will I get real projects in Data Science?",
            "Do beginners struggle in Data Science?",
            "Do I need strong math for Data Science?"
        ],

        "data analytics": [
            "Is Data Analytics easier than Data Science?",
            "Will I learn Excel, Power BI, and dashboards?",
            "Can beginners get jobs quickly in Data Analytics?",
            "Do companies still hire Data Analysts?"
        ],

        "agentic ai": [
            "Agentic AI sounds futuristic. Is it beginner friendly?",
            "Will I learn AI agents and automation?",
            "Is Agentic AI related to ChatGPT and LLMs?",
            "Do I need Python before learning Agentic AI?"
        ],

        "artificial intelligence": [
            "Artificial Intelligence sounds interesting.",
            "Is AI difficult for beginners?",
            "Do I need Python before learning AI?",
            "Will AI have good career opportunities in the future?"
        ],

        "machine learning": [
            "Is Machine Learning hard to understand?",
            "Will I build real AI models in this course?",
            "Do beginners learn Machine Learning easily?",
            "Is coding compulsory for Machine Learning?"
        ],

        "python": [
            "Is Python easy to learn?",
            "How long does it take to learn Python?",
            "Will Python help me get a job?",
            "Do complete beginners struggle with Python?"
        ],

        "job": [
            "Will I get placement support?",
            "Are there internship opportunities?",
            "What kind of salary can freshers expect?",
            "Which companies hire students from this course?"
        ],

        "fees": [
            "Can I pay the fees in installments?",
            "Is there any scholarship available?",
            "What is the total course fee?",
            "Do you have EMI options?"
        ],

        "placement": [
            "Do you provide placement training?",
            "Which companies hire students?",
            "What is the placement success rate?",
            "Will I get interview preparation support?"
        ],

        "duration": [
            "How many months is the course?",
            "Is the course flexible for working students?",
            "Do you provide recorded classes?",
            "How many hours per week should I study?"
        ],

        "projects": [
            "Will I work on real-world projects?",
            "Do students build portfolio projects?",
            "Will projects help during placements?",
            "Can I add these projects to my resume?"
        ],

        "internship": [
            "Do you provide internships after training?",
            "Are internships paid or unpaid?",
            "Will internships help me get jobs?",
            "Do beginners get internship opportunities?"
        ]
    }

    for keyword, reply_list in responses.items():

        words = keyword.split()

        if any(word in msg for word in words):
            return random.choice(reply_list)

    default_responses = [

        "Can you explain that a little more?",

        "I'm still learning about tech careers.",

        "Which course would you personally recommend?",

        "Can beginners really learn this easily?",

        "What makes your institute different from others?",

        "Do students get real projects here?",

        "Will this course help me get a tech job?",

        "I'm confused between Data Science and Data Analytics."
    ]

    return random.choice(default_responses)