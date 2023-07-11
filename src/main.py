from langchain.prompts import SystemMessagePromptTemplate
from langchain.schema import AIMessage, HumanMessage

import langchain_openai.service as langchain_openai_service
from langchain_prompts.chat import system_message_prompt_template

system_message_prompt = SystemMessagePromptTemplate.from_template(system_message_prompt_template)

chat_history = [
  HumanMessage(content="Hi, i am {full_name}"),
  AIMessage(content="Hi!, How can i assist you today ?"),
]

result = langchain_openai_service.create_chat_completion(
  system_prompt=system_message_prompt,
  chat_history=chat_history,
  additional_data={
    "full_name": "Dennis Ritchie",
    "date_of_birth": "1999-10-10",
    "gender": "male",
    "interests": "",
    "relationship_goal": "short-term",
  }
)

print("RESULT", result)