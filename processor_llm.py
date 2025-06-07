from dotenv import load_dotenv
from groq import Groq
import json, re

load_dotenv()

groq = Groq()

def classify_with_llm(log_msg):
    """
    Generate a variant of the input sentence. For example,
    If input sentence is "User session timed out unexpectedly, user ID: 9250.",
    variant would be "Session timed out for user 9251"
    """
    prompt = f'''Classify the log message into one of these categories: 
- Workflow Error
- Deprecation Warning
- Unclassified

Strictly always and only return the category **inside** <category>...</category> tags, no extra text.  
Log message: {log_msg}'''

    chat_completion = groq.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        # model="llama-3.3-70b-versatile",
        model="deepseek-r1-distill-llama-70b",
        temperature=0.5
    )

    content = chat_completion.choices[0].message.content
    match = re.search(r'<category>(.*?)<\/category>', content, flags=re.DOTALL)
    category = match.group(1) if match else "Unclassified"

    if match:
        category = match.group(1)

    return category


if __name__ == '__main__':
    print(classify_with_llm(
        "Case escalation for ticket ID 7324 failed because the assigned support agent is no longer active."))
    print(classify_with_llm(
        "The 'ReportGenerator' module will be retired in version 4.0. Please migrate to the 'AdvancedAnalyticsSuite' by Dec 2025"))
    print(classify_with_llm("System reboot initiated by user 12345."))