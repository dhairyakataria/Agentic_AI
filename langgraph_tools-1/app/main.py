from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import traceback

from .graph_runner import build_graph, run_graph

app = FastAPI(title="Agent FastAPI")

class InvokeRequest(BaseModel):
    text: str

class InvokeResponse(BaseModel):
    raw: dict

# Build graph once at startup
GRAPH = None


@app.on_event("startup")
async def startup_event():
    global GRAPH
    GRAPH = build_graph()


@app.post("/invoke", response_model=InvokeResponse)
async def invoke(req: InvokeRequest):
    try:
        messages = run_graph(GRAPH, req.text)
        # messages may contain complex objects; convert to serialisable form
        # We'll attempt to call .to_dict or use str() as fallback
        serializable = []
        for m in messages.get("messages", []):
            try:
                serializable.append(m.to_dict())
            except Exception:
                try:
                    serializable.append({"content": str(m)})
                except Exception:
                    serializable.append({"raw": repr(m)})

        return {"raw": {"messages": serializable}}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))