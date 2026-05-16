from openai import OpenAI

client = OpenAI(
    api_key="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"
)

def ask_llm(prompt):

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content