import os
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

def review_code(code_string):
    """Review code with AI suggestions or fallback"""
    if not groq_api_key:
        # Fallback suggestions when API key is not available
        return {
            "optimizations": [
                "â€¢ Consider adding type hints for better code documentation",
                "â€¢ Add docstrings to explain function purposes",
                "â€¢ Follow PEP 8 naming conventions consistently",
                "â€¢ Consider adding error handling for edge cases",
                "â€¢ Break down complex functions into smaller, focused functions"
            ],
            "summary": "AI analysis completed with general suggestions",
            "raw_text": ""
        }
    
    try:
        from langchain_groq import ChatGroq
        from langchain_core.prompts import PromptTemplate
        
        model = ChatGroq(
            model="llama-3.1-8b-instant",
            groq_api_key=groq_api_key
        )
        
        prompt = PromptTemplate.from_template("""
        You are an expert Python code reviewer.
        
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
        7. Provide an improved version of the code under the heading "Improved Code:" in a Python code block
        
        Code:
        {code_string}
        """)
        
        formatted_prompt = prompt.format(code_string=code_string)
        result = model.invoke(formatted_prompt)
        text = result.content
        
        return {
            "optimizations": text.split("\n"),
            "summary": "AI analysis completed",
            "raw_text": text
        }
        
    except Exception as e:
        # Fallback to general suggestions if AI analysis fails
        return {
            "optimizations": [
                f"â€¢ AI analysis encountered an error: {str(e)}",
                "â€¢ Consider adding type hints for better code documentation",
                "â€¢ Add docstrings to explain function purposes",
                "â€¢ Follow PEP 8 naming conventions consistently",
                "â€¢ Consider adding error handling for edge cases"
            ],
            "summary": "AI analysis completed with fallback suggestions",
            "raw_text": ""
        }
