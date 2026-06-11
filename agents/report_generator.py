import json
from pathlib import Path
from datetime import datetime

def generate_report(state):

    Path("reports").mkdir(
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    report_path = (
        f"reports/report_{timestamp}.json"
    )

    report = {
        "analysis": state["analysis"],
        "root_cause": state["root_cause"],
        "patch": state["patch"],
        "approved": state["approved"],
        "signature_valid":
            state["signature_valid"],
        "test_results":
            state["test_results"]
    }

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            report,
            f,
            indent=4
        )

    print(
        f"\nReport saved: {report_path}"
    )

    return {
        "report_path": report_path
    }