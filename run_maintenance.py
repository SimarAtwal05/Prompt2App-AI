from maintenance.graph import build_graph
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0
)

graph = build_graph(llm)

graph.invoke({
    "error_log": "logs/error.log"
})