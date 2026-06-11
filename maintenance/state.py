from typing_extensions import TypedDict

class MaintenanceState(TypedDict):
    error_log: str

    analysis: str
    root_cause: str
    patch: str

    approved: bool

    signature: str
    signature_valid: bool

    test_results: str

    report_path: str