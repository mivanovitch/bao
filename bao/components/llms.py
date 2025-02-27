from injector import singleton, inject
from bao.components import MODEL_TYPE
from bao.settings.settings import Settings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models.chat_models import BaseChatModel


@singleton
class LLMs:

    @inject
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.google_llm = ChatGoogleGenerativeAI(
            model=settings.google_api.model,
            google_api_key=settings.google_api.api_key,
            temperature=0.01,
            convert_system_message_to_human=True,
            verbose=True,
        )  # type: ignore
        self.openai_eco_gpt = ChatOpenAI(
            model=settings.openai.eco_model,
            temperature=0.01,
            api_key=settings.openai.api_key,
            verbose=True,
        )
        self.openai_supper_gpt = ChatOpenAI(
            model=settings.openai.super_model,
            temperature=0.01,
            api_key=settings.openai.api_key,
            verbose=True,
        )
        # anthropic sonnec
        self.anthropic_eco = ChatAnthropic(
            model_name=settings.anthropic.eco_model, temperature=0.01, verbose=True
        )
        self.anthropic_supper = ChatAnthropic(
            model_name=settings.anthropic.supper_model, temperature=0.01, verbose=True
        )

    def get_llm(self, llm_type: MODEL_TYPE) -> BaseChatModel:  # type: ignore
        if llm_type == "gemini":
            return self.google_llm
        elif llm_type == "gpt-3.5":
            return self.openai_eco_gpt
        elif llm_type == "gpt-4":
            return self.openai_supper_gpt
        elif llm_type == "anthropic-opus":
            return self.anthropic_supper
        elif llm_type == "anthropic-sonnet":
            return self.anthropic_eco
        else:
            raise ValueError(f"Not support model type: {llm_type}")
