# Sales Insights API

Esta API fornece insights de vendas utilizando um agente OpenAI para responder perguntas sobre vendas e listar os produtos mais vendidos.

## Tecnologias Utilizadas
- Langchain
- FastAPI
- OpenAI API
- Pydantic
- Uvicorn

## Como Executar

### Pré-requisitos
- Python 3.11+
- Instalar dependências:
  ```bash
  pip install -r requeriments.txt
  ```

### Iniciar a API
```bash
uvicorn main:app --host 0.0.0.0 --port 5000
```
### Iniciar a API
#### É necessario colocar a API key no .env
```bash
OPENAI_API_KEY=
```


## Endpoints Disponíveis

### `post /llm`
**Descrição:** Retorna resposta baseados em uma pergunta fornecida.

**Parâmetro de Query:**
- `query` (string, opcional): Pergunta sobre insights de vendas.

**Exemplo de Requisição:**
```bash
curl -X 'POST' 'http://localhost:5000/llm' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/json' \
     -d '{"query": "quantos usuarios tenho na base?"}'
```

**Resposta Exemplo:**
```json
{
   "response": "Você tem 5 usuários na base de dados."
}
```



