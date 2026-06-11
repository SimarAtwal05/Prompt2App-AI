from agents.gemini_client import generate_with_fallback


def fix_generator(state):

    print("STEP 7: FIX GENERATOR")

    prompt = f"""
    Generate a patch for this root cause.

    Root Cause:

    {state["root_cause"]}
    """

    patch = generate_with_fallback(prompt)

    print("STEP 8: FIX GENERATED")

    return {
        "patch": patch
    }