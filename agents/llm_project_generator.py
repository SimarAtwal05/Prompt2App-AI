import os
import re
from pathlib import Path
from typing_extensions import TypedDict

from dotenv import load_dotenv
from google import genai
from langgraph.graph import StateGraph, START, END


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Add it inside your .env file.")

client = genai.Client(api_key=api_key)


class ProjectState(TypedDict):
    user_prompt: str
    generated_code: str
    output_folder: str


SYSTEM_PROMPT = """
You are an AI DevOps software generator.

Generate a complete working FastAPI CRUD project.

Generate exactly these files:
- app/__init__.py
- app/main.py
- app/database.py
- app/models.py
- app/schemas.py
- app/crud.py
- tests/test_app.py
- requirements.txt
- Dockerfile
- docker-compose.yml
- .github/workflows/ci.yml
- README.md
- pytest.ini

Rules:
- Use FastAPI.
- Use SQLite.
- Use SQLAlchemy.
- Use Pydantic.
- Use Pytest.
- Use Docker.
- Use Docker Compose.
- Use GitHub Actions.
- Keep code simple.
- Generated app must run with: uvicorn app.main:app --reload
- Generated tests must run with: pytest

Output format for every file:

FILE: app/main.py
~~~content
file content here
~~~

Do not write explanations outside file blocks.
"""


def generate_project_files(state: ProjectState):
    prompt = f"""
{SYSTEM_PROMPT}

User Request:
{state["user_prompt"]}
"""

    models_to_try = [
        "gemini-2.0-flash",
        "gemini-2.5-flash",
        "gemini-2.5-pro",
    ]

    last_error = None

    for model_name in models_to_try:
        try:
            print(f"Trying model: {model_name}")

            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )

            if not response.text:
                raise ValueError("LLM returned empty response.")

            return {"generated_code": response.text}

        except Exception as error:
            print(f"Model failed: {model_name}")
            print(error)
            last_error = error

    raise last_error


def write_files(state: ProjectState):
    output_folder = Path(state["output_folder"])
    output_folder.mkdir(parents=True, exist_ok=True)

    generated_text = state["generated_code"]

    pattern = r"FILE:\s*(.*?)\n~~~content\n(.*?)\n~~~"
    matches = re.findall(pattern, generated_text, re.DOTALL)

    if not matches:
        debug_path = output_folder / "raw_llm_output.txt"
        debug_path.write_text(generated_text, encoding="utf-8")
        raise ValueError(f"No files generated. Raw output saved to {debug_path}")

    for file_path, file_content in matches:
        clean_path = file_path.strip().replace("\\", "/")

        if clean_path.startswith("/") or ".." in clean_path:
            raise ValueError(f"Unsafe path detected: {clean_path}")

        full_path = output_folder / clean_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(file_content.strip() + "\n", encoding="utf-8")

    return {
        "user_prompt": state["user_prompt"],
        "generated_code": state["generated_code"],
        "output_folder": state["output_folder"],
    }


def build_graph():
    graph = StateGraph(ProjectState)

    graph.add_node("generate_project_files", generate_project_files)
    graph.add_node("write_files", write_files)

    graph.add_edge(START, "generate_project_files")
    graph.add_edge("generate_project_files", "write_files")
    graph.add_edge("write_files", END)

    return graph.compile()


if __name__ == "__main__":
    user_prompt = input("Enter project prompt: ")

    app = build_graph()

    result = app.invoke(
        {
            "user_prompt": user_prompt,
            "generated_code": "",
            "output_folder": "generated_projects/output_project",
        }
    )

    print(f"Project generated inside: {result['output_folder']}")
