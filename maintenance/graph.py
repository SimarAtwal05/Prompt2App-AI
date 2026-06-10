from langgraph.graph import StateGraph, END

from maintenance.state import MaintenanceState
from agents.log_analyzer import log_analyzer
from agents.root_cause import root_cause_agent
from agents.fix_generator import fix_generator
from agents.human_review import human_review
from agents.signature import sign_patch, verify_signature
from agents.patch_applier import apply_patch

def build_graph(llm):
    graph = StateGraph(MaintenanceState)

    graph.add_node("analyze", lambda s: log_analyzer(s, llm))
    graph.add_node("root", lambda s: root_cause_agent(s, llm))
    graph.add_node("fix", lambda s: fix_generator(s, llm))
    graph.add_node("review", human_review)
    graph.add_node("sign", sign_patch)
    graph.add_node("verify", verify_signature)
    graph.add_node("apply", apply_patch)

    graph.set_entry_point("analyze")

    graph.add_edge("analyze", "root")
    graph.add_edge("root", "fix")
    graph.add_edge("fix", "review")

    graph.add_conditional_edges(
        "review",
        lambda s: "sign" if s["approved"] else END
    )

    graph.add_edge("sign", "verify")

    graph.add_conditional_edges(
        "verify",
        lambda s: "apply" if s["signature_valid"] else END
    )

    graph.add_edge("apply", END)

    return graph.compile()