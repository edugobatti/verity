import sqlite3
from typing import List


def get_connection():
    """Cria e retorna uma nova conexão SQLite."""
    return sqlite3.connect("./files/local.db")

def list_tables():
    """Lista todas as tabelas do banco de dados."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = c.fetchall()
    conn.close()
    return [item[0] for item in rows]

def run_sqlite_query(query: str):
    """Executa uma query no banco de dados SQLite."""
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute(query)
        result = c.fetchall()
    except sqlite3.OperationalError as err:
        result = f"The following error occurred: {str(err)}"
    finally:
        conn.close()
    return result


def describe_tables(table_names: List[str]):
    """Retorna o schema das tabelas fornecidas."""
    conn = get_connection()
    c = conn.cursor()
    print(table_names)
    tables = ', '.join(f"'{table}'" for table in table_names)
    try:
        rows = c.execute(f"SELECT sql FROM sqlite_master WHERE type='table' and name IN ({tables});")
        result = '\n'.join(row[0] for row in rows if row[0] is not None)
    finally:
        conn.close()
    return result

