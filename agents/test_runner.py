import subprocess

def run_tests(state):

    print("\nRunning Pytest...\n")

    result = subprocess.run(
        ["pytest"],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    return {
        "test_results": result.stdout
    }