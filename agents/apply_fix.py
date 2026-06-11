import os


def apply_fix(state):
    print("\nAPPLYING PATCH...")

    patch = state["patch"]

    os.makedirs("generated_patches", exist_ok=True)

    with open(
        "generated_patches/latest_patch.txt",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(patch)

    print("Patch saved")

    return {}