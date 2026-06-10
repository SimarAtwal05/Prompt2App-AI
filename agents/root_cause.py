def root_cause_agent(state, llm):
    response = llm.invoke(
        f"""
        Identify the root cause of this error.

        {state['analysis']}
        """
    )

    return {
        "root_cause": response.content
    }