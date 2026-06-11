from agents.gemini_client import generate_with_fallback


def root_cause_agent(state):

    print("STEP 5: ROOT CAUSE AGENT")

    prompt = f"""
    Determine the root cause of this issue.

    Analysis:

    {state["analysis"]}
    """

    root_cause = generate_with_fallback(prompt)

    print("STEP 6: ROOT CAUSE COMPLETE")

    return {
        "root_cause": root_cause
    }