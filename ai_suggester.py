import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=groq_api_key
)

prompt = PromptTemplate.from_template("""
You are an expert Python code review.

Analyze the given code and provide:

1. Time complexity analysis
2. Space complexity analysis
3. Detect logical or syntax errors (if any)
4. Suggest optimal approaches if possible
5. Check naming conventions:
   - Variables and functions should use snake_case
   - Classes should use PascalCase
   - Constants should use UPPER_CASE
6. Suggest improvements clearly in bullet points

Code:
{code_string}
""")

def review_code(code_string):
    formatted_prompt = prompt.format(code_string=code_string)
    result = model.invoke(formatted_prompt)
    print("\n--- AI Suggestions ---\n")
    print(result.content)


# TAKE USER INPUT

print("Enter your Python code (type END on a new line to finish):")

lines = []
while True:
    line = input()
    if line.strip() == "END":
        break
    lines.append(line)

code_string = "\n".join(lines)

# SEND TO AI FOR REVIEW

review_code(code_string)