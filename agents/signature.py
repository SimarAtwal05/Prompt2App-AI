from config.reviewers import APPROVED_REVIEWERS


def verify_signature(state):

    print("\n===== HUMAN APPROVAL GATE =====")

    reviewer = input(
        "Reviewer Email: "
    ).strip()

    token = input(
        "Approval Token: "
    ).strip()

    valid = (
        reviewer in APPROVED_REVIEWERS
        and
        APPROVED_REVIEWERS[reviewer] == token
    )

    print(
        f"\nReviewer: {reviewer}"
    )

    print(
        f"Signature Valid: {valid}"
    )

    return {
        "signature": reviewer,
        "signature_valid": valid
    }