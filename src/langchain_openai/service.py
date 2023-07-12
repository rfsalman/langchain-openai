
from typing import Type, TypeVar
from pydantic import BaseModel
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
  HumanMessage,
  SystemMessage
)
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import (
  PromptTemplate,
  SystemMessagePromptTemplate, 
  ChatPromptTemplate,
  HumanMessagePromptTemplate
)
from langchain.schema import (
  SystemMessage,
  AIMessage,
  HumanMessage,
)

from config import config
from langchain_prompts.chat import chat_parser_prompt_template

def create_chat_completion(
  system_prompt: SystemMessagePromptTemplate,
  chat_history: list[
    SystemMessage | AIMessage | HumanMessage | HumanMessagePromptTemplate
  ],
  additional_data: dict,
  chat_open_ai_options: dict = {}
) -> AIMessage:
  """
  chat_result = langchain_openai_service.create_chat_completion(
    system_prompt=SystemMessagePromptTemplate.from_template(),
    chat_history=[HumanMessage(), AIMessage()],
    additional_data={} 
  )
  """
  try:
    chat_openai = ChatOpenAI(**chat_open_ai_options, openai_api_key=config.OPENAI_API_KEY)

    messages = [
      system_prompt,
      *chat_history
    ]

    chat_prompt_template = ChatPromptTemplate.from_messages(messages)

    chat_prompt = chat_prompt_template.format_messages(**additional_data)

    chat_result = chat_openai.predict_messages(chat_prompt)

    return chat_result
  except Exception as e:
    print("Error", e)
    
    return None
    
def chat_stringify(chat_history: list[AIMessage | HumanMessage]) -> str:
  chat_history_string = ""

  for message in chat_history:
    if isinstance(message, AIMessage):
      chat_history_string += f"AI: {message.content}\n"
      continue

    if isinstance(message, HumanMessage):
      chat_history_string += f"User: {message.content}"

  return chat_history_string

T = TypeVar("T", bound=BaseModel)

def parse_chat_history(
  chat_history: list[AIMessage | HumanMessage], 
  pydantic_model: Type[T], 
  parser_additional_data: dict = None,
  system_prompt_template: str = chat_parser_prompt_template,
) -> T | None:
  try:
    llm = OpenAI(
      temperature=0.0
    )
    
    chat_parser = PydanticOutputParser(
      pydantic_object=pydantic_model
    )

    chat_parser_prompt = PromptTemplate.from_template(system_prompt_template)

    stringified_chat_history = chat_stringify(chat_history)

    prompt = chat_parser_prompt.format(
      chat_history=stringified_chat_history, 
      format_instructions=chat_parser.get_format_instructions(),
      **(parser_additional_data if parser_additional_data else {})
    )

    parse_result = llm.predict(prompt)

    parsed = chat_parser.parse(parse_result)

    return parsed
  except Exception as e:
    print("Chat parsing error", e)
    return None