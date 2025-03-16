import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from src.agents.agent_openai import LangChainAgentOpenAI

import subprocess
import threading

agent_openai = LangChainAgentOpenAI()


app = FastAPI()


@app.get("/")
async def service():
    return "live"


class SolicitationRequest(BaseModel):
    query: str
    llm_model: str


@app.post("/llm")
async def generate(request: SolicitationRequest):
    try:
        response_llm = agent_openai.run_query(request.query)
        return {'content': response_llm}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Função para iniciar o Streamlit
def start_streamlit():
    streamlit_command = ["streamlit", "run", "./src/playground/playground.py"]
    subprocess.Popen(streamlit_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# Iniciar a API e o Streamlit
if __name__ == "__main__":
    # Inicia o Streamlit em uma thread separada
    streamlit_thread = threading.Thread(target=start_streamlit, daemon=True)
    streamlit_thread.start()

    # Inicia a API FastAPI
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
