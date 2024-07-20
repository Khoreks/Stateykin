from langchain_core.prompts import PromptTemplate
from dotenv import dotenv_values

prompt_config = dotenv_values("prompts.env")

extraction_prompt = PromptTemplate(
    template=prompt_config["extraction"],
    input_variables=["first_token", "start_header", "end_header", "end_message", "user_message"],
)

web_request_generation_prompt = PromptTemplate(
    template=prompt_config["web_request_generation"],
    input_variables=["first_token", "start_header", "end_header", "end_message", "topic",
                     "platform", "audience", "additional_information"],
)

web_page_summarization_prompt = PromptTemplate(
        template=prompt_config["web_page_summarization"],
        input_variables=["first_token", "start_header", "end_header", "end_message", "topic", "page"],
    )

post_generate_prompt = PromptTemplate(
    template=prompt_config["post_generation"],
    input_variables=["first_token", "start_header", "end_header", "end_message", "question", "topic",
                     "platform", "audience", "additional_information", "context"],
)
