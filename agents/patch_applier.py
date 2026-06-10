import subprocess

def apply_patch(state):
    subprocess.run(
        ["git", "apply", "patches/fix.diff"],
        check=True
    )

    return {}