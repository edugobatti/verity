from pydantic import BaseModel
from typing import List
from langchain.tools import Tool
from src.worker.sql_worker import describe_tables, run_sqlite_query



class RunQueryArgsSchema(BaseModel):
    query: str


run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Execute a consulta no sqlite.",
    func=run_sqlite_query,
    args_schema=RunQueryArgsSchema
)



class DescribeTablesArgsSchema(BaseModel):
    tables_names: List[str]


describe_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Dada uma lista de nomes de tabelas, retorna o esquema dessas tabelas",
    func=describe_tables,
    args_schema=DescribeTablesArgsSchema
)
