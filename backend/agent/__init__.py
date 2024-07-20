from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict

from .actions import web_search, generate_search_request, generate, extraction_information, summarization_web_page


class GraphState(TypedDict):
    first_token: str
    start_header: str
    end_header: str
    end_message: str

    user_message: str
    topic: str
    platform: str
    audience: str
    additional_information: str
    generation: str
    web_search_queries: str
    web_pages: list
    context: str


workflow = StateGraph(GraphState)
workflow.add_node("extraction_information", extraction_information)
workflow.add_node("websearch", web_search)
workflow.add_node("generate_search_request", generate_search_request)
workflow.add_node("summarization_web_page", summarization_web_page)
workflow.add_node("generate", generate)

workflow.set_entry_point("extraction_information")
workflow.add_edge("extraction_information", "generate_search_request")


workflow.add_edge("generate_search_request", "websearch")
workflow.add_edge("websearch", "summarization_web_page")
workflow.add_edge("summarization_web_page", "generate")
workflow.add_edge("generate", END)

Agent = workflow.compile()


def run_agent(user_message):
    output = Agent.invoke({"user_message": user_message})
    print("=======")
    print(output["generation"])
