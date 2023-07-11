
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
  HumanMessage,
  SystemMessage
)
from langchain.prompts import (
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
    