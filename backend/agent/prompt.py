from langchain_core.prompts import PromptTemplate
from dotenv import dotenv_values

prompt_config = dotenv_values("prompts.env")

extract_prompt = PromptTemplate(
    template=prompt_config["extract"],
    input_variables=["first_token", "start_header", "end_header", "end_message", "user_message"],
)

search_prompt = PromptTemplate(
    template=prompt_config["web_query"],
    input_variables=["first_token", "start_header", "end_header", "end_message", "topic",
                     "platform", "audience", "additional_information"],
)

generate_prompt = PromptTemplate(
    template=prompt_config["generate"],
    input_variables=["first_token", "start_header", "end_header", "end_message", "question", "topic",
                     "platform", "audience", "additional_information", "context"],
)
