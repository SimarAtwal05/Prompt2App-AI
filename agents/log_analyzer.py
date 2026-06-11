from agents.gemini_client import (
    generate_with_fallback
)

def log_analyzer(state):

    print("STEP 1: ENTERED LOG ANALYZER")

    with open("logs/error.log", "r") as f:
        log_data = f.read()

    print("STEP 2: READ LOG FILE")

    prompt = f"""
    Analyze this application error.

    Return:
    - Error Type
    - File
    - Line Number
    - Explanation

    Error:

    {log_data}
    """

    print("STEP 3: CALLING GEMINI")

    analysis = generate_with_fallback(prompt)

    print("STEP 4: GEMINI RETURNED")

    return {
        "analysis": analysis
    }