from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

from .search import web_search_tool
from .llm import model as llm
from .prompt import *

extraction_chain = extract_prompt | llm | JsonOutputParser()
search_chain = search_prompt | llm | JsonOutputParser()
generate_chain = generate_prompt | llm | StrOutputParser()


def extraction_information(state):
    print("Step: Information extraction")
    input_dict = {
        "user_message": state["user_message"],
        "first_token": state["first_token"],
        "start_header": state["start_header"],
        "end_header": state["end_header"],
        "end_message": state["end_message"]
    }
    request = extraction_chain.invoke(input_dict)
    # print(request)
    return {
        "topic": request["Тема"],
        "platform": request["Социальная сеть"],
        "audience": request["Целевая аудитория"],
        "additional_information": request["Дополнительная информация"],
    }


def generate_search_request(state):
    print("Step: Generate Query for Web Search")
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
    request = search_chain.invoke(input_dict)
    # print(request)
    return {"search_query": request["query"]}


def web_search(state):
    search_query = state['search_query']
    print(f'Step: Searching the Web for: "{search_query}"')

    search_result = web_search_tool.invoke(search_query)
    # print(f"{search_result=}")
    return {"context": search_result}


def generate(state):
    print("Step: Post generation")
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
    generation = generate_chain.invoke(input_dict)
    return {"generation": generation}
