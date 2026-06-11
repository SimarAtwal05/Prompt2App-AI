from maintenance.graph import build_graph

if __name__ == "__main__":

    graph = build_graph()

    result = graph.invoke(
        {
            "error_log": "",
            "analysis": "",
            "root_cause": "",
            "patch": "",
            "approved": False,
            "signature": "",
            "signature_valid": False,
            "test_results": "",
            "report_path": "",
        }
    )

    print(
        "\nMaintenance Workflow Complete"
    )

    print(result)