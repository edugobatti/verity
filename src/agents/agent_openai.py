from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.schema import SystemMessage
from langchain.agents import create_openai_functions_agent, AgentExecutor
from dotenv import load_dotenv
import os
from src.tool.sql_consult import run_query_tool, describe_tables_tool
from src.worker.sql_worker import list_tables

# Carregar variáveis de ambiente
load_dotenv()

class LangChainAgentOpenAI:
    def __init__(self, model: str = "gpt-4o", temperature: float = 0):
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("A variável de ambiente OPENAI_API_KEY não está definida.")
        
        self.chat = ChatOpenAI(
            temperature=temperature,
            model=model,
            openai_api_key=openai_api_key
        )

        self.tools = [run_query_tool, describe_tables_tool]
        tables = list_tables()

        prompt = ChatPromptTemplate(
            messages=[
                SystemMessage(content=(
                    "Você é uma IA que tem acesso a um banco de dados SQLite.\n"
                    f"O banco de dados possui tabelas de: {tables}.\n"
                    "Não faça suposições sobre quais tabelas existem ou quais colunas existem.\n"
                    "Em vez disso, use a função 'describe_tables'."
                    "não deve responder nada que não tenha haver com o banco de dados"
                )),
                HumanMessagePromptTemplate.from_template("{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ]
        )

        # Criar o agente atualizado
        agent = create_openai_functions_agent(
            llm=self.chat,
            prompt=prompt,
            tools=self.tools
        )

        # Criar executor do agente
        self.agent_executor = AgentExecutor(
            agent=agent,
            verbose=True,
            tools=self.tools,
        )

    def run_query(self, query: str):
        try:
            response = self.agent_executor.invoke({"input": query})
            return response["output"]
        except Exception as e:
            raise RuntimeError(f"Erro ao processar a consulta: {str(e)}")
