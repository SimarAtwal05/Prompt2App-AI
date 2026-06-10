from typing import TypedDict

class MaintenanceState(TypedDict):
    error_log: str
    analysis: str
    root_cause: str
    patch: str
    approved: bool
    signature_valid: bool