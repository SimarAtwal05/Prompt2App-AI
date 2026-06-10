def human_review(state):
    print("\n===== PROPOSED PATCH =====\n")
    print(state["patch"])

    choice = input("\nApprove patch? (yes/no): ")

    return {
        "approved": choice.strip().lower() == "yes"
    }