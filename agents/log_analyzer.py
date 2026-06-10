def log_analyzer(state, llm):
    with open("logs/error.log", "r") as f:
        log = f.read()

    response = llm.invoke(
        f"""
        Analyze this error log.
        Return concise explanation.

        {log}
        """
    )

    return {
        "analysis": response.content
    }