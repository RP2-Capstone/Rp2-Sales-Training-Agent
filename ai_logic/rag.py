def retrieve_context(user_message):
    try:
        with open("data/course_data.txt", "r") as f:
            data = f.read()
    except:
        return ""

    msg = user_message.lower()

    # -------- SPECIFIC COURSE MATCH --------
    if "data science" in msg:
        return extract_section(data, "DATA SCIENCE")

    if "data analytics" in msg:
        return extract_section(data, "DATA ANALYTICS")

    if "agentic ai" in msg or "ai" in msg:
        return extract_section(data, "AGENTIC AI")

    # -------- GENERAL QUESTIONS --------
    if "duration" in msg:
        return "Most courses range between 3 to 6 months depending on the specialization."

    if "job" in msg or "career" in msg:
        return "These courses offer placement support with resume building and interview preparation."

    if "fee" in msg or "price" in msg:
        return "The course fees usually range between 50,000 and 80,000 with EMI options."

    return data[:300]


# -------- HELPER FUNCTION --------
def extract_section(data, keyword):
    sections = data.split("---")

    for sec in sections:
        if keyword.lower() in sec.lower():
            return sec.strip()

    return ""