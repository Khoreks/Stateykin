from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

from .search import web_search_tool
from .summarization import query_summarization
from .llm import get_llm
from .prompt import *

llm = get_llm()

information_extraction_chain = extraction_prompt | llm | JsonOutputParser()
request_generation_chain = web_request_generation_prompt | llm | JsonOutputParser()
web_page_summarization_chain = web_page_summarization_prompt | llm | StrOutputParser()
post_generation_chain = post_generate_prompt | llm | StrOutputParser()


def extraction_information(state):
    input_dict = {
        "user_message": state["user_message"],
        "first_token": state["first_token"],
        "start_header": state["start_header"],
        "end_header": state["end_header"],
        "end_message": state["end_message"]
    }
    request = information_extraction_chain.invoke(input_dict)
    return {
        "topic": request["Тема"],
        "platform": request["Социальная сеть"],
        "audience": request["Целевая аудитория"],
        "additional_information": request["Дополнительная информация"],
    }


def generate_search_request(state):
    input_dict = {
        "topic": state["topic"],
        "platform": state["platform"],
        "audience": state["audience"],
        "additional_information": state["additional_information"],
        "first_token": state["first_token"],
        "start_header": state["start_header"],
        "end_header": state["end_header"],
        "end_message": state["end_message"]
    }
    request = request_generation_chain.invoke(input_dict)
    return {
        "web_search_queries": request["queries"]
    }


def web_search(state):
    input_dict = {
        'web_search_queries': state['web_search_queries']
    }
    search_results = web_search_tool.invoke(input_dict)

    return {
        "web_pages": search_results
    }


def summarization_web_page(state):
    input_dict = {
        "topic": state["topic"],
        "first_token": state["first_token"],
        "start_header": state["start_header"],
        "end_header": state["end_header"],
        "end_message": state["end_message"]
    }
    context = []
    for query_pages in state["web_pages"]:
        context.append(query_summarization(input_dict, query_pages, web_page_summarization_chain))

    return {
        "context": "\n".join(context)
    }


def generate(state):
    input_dict = {
        "topic": state["topic"],
        "platform": state["platform"],
        "audience": state["audience"],
        "additional_information": state["additional_information"],
        "context": state["context"],
        "first_token": state["first_token"],
        "start_header": state["start_header"],
        "end_header": state["end_header"],
        "end_message": state["end_message"]
    }
    generation = post_generation_chain.invoke(input_dict)
    return {"generation": generation}
