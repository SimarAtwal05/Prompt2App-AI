from langgraph.graph import (
    StateGraph,
    START,
    END
)

from maintenance.state import MaintenanceState

from agents.log_analyzer import log_analyzer
from agents.root_cause import root_cause_agent
from agents.fix_generator import fix_generator
from agents.human_review import human_review
from agents.signature import verify_signature
from agents.apply_fix import apply_fix
from agents.test_runner import run_tests
from agents.report_generator import generate_report


def review_router(state):
    if state["approved"]:
        return "approved"
    return "rejected"


def signature_router(state):
    if state["signature_valid"]:
        return "verified"
    return "rejected"


def build_graph():

    graph = StateGraph(MaintenanceState)

    # -------------------------
    # Nodes
    # -------------------------

    graph.add_node("analyze", log_analyzer)

    graph.add_node("root_cause", root_cause_agent)

    graph.add_node("fix", fix_generator)

    graph.add_node("review", human_review)

    graph.add_node("signature", verify_signature)

    graph.add_node("apply_fix", apply_fix)

    graph.add_node("tests", run_tests)

    graph.add_node("report", generate_report)

    # -------------------------
    # Main Flow
    # -------------------------

    graph.add_edge(
        START,
        "analyze"
    )

    graph.add_edge(
        "analyze",
        "root_cause"
    )

    graph.add_edge(
        "root_cause",
        "fix"
    )

    graph.add_edge(
        "fix",
        "review"
    )

    # -------------------------
    # Human Approval Gate
    # -------------------------

    graph.add_conditional_edges(
        "review",
        review_router,
        {
            "approved": "signature",
            "rejected": END,
        }
    )

    # -------------------------
    # Signature Verification
    # -------------------------

    graph.add_conditional_edges(
        "signature",
        signature_router,
        {
            "verified": "apply_fix",
            "rejected": END,
        }
    )

    # -------------------------
    # Auto Fix -> Test -> Report
    # -------------------------

    graph.add_edge(
        "apply_fix",
        "tests"
    )

    graph.add_edge(
        "tests",
        "report"
    )

    graph.add_edge(
        "report",
        END
    )

    return graph.compile()