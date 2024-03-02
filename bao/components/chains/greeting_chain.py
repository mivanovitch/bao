from typing import Any, Dict

from injector import inject, singleton
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableSerializable

from bao.components.llms import LLMs
from bao.settings.settings import Settings


@singleton
class Greeting:
    @inject
    def __init__(self, settings: Settings, llms: LLMs) -> None:
        self.settings = settings
        self.llms = llms

    def chain(self) -> RunnableSerializable[Dict[str, Any], Dict[str, Any]]:
        llm = self.llms.get_llm(llm_type=self.settings.chain_templates.greeting_model)
        chat_template = ChatPromptTemplate.from_messages(
            [
                ("system", self.settings.chain_templates.greeting_template),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
            ]
        )
        return chat_template | llm | StrOutputParser()  # type: ignore
