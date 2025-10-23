from fastapi import FastAPI
import logging

from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

from agent_runner import AgentRunner

app = FastAPI()

logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


agent = AgentRunner()
class QueryIn(BaseModel):
    query: str
    session_id: str | None = None

@app.post("/query")
async def query_endpoint(payload: QueryIn):
    result = await agent.run(payload.query, session_id=payload.session_id)
    return result