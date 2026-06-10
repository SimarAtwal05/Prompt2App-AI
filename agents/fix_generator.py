def fix_generator(state, llm):
    response = llm.invoke(
        f"""
        Generate a unified git diff to fix this bug.

        Root cause:
        {state['root_cause']}

        RULES:
        - Output ONLY a git diff
        - No explanations
        """
    )

    patch = response.content

    with open("patches/fix.diff", "w") as f:
        f.write(patch)

    return {
        "patch": patch
    }