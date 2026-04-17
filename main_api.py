from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv

from agent import creer_agent

load_dotenv()

try:
    from fastapi import FastAPI, Header, HTTPException
    from pydantic import BaseModel
except Exception:
    FastAPI = None
    Header = None
    HTTPException = RuntimeError
    BaseModel = object

app = FastAPI(title="TP Agent API") if FastAPI is not None else None
api_key = os.getenv("FASTAPI_API_KEY", "change-me")
agent = creer_agent()

if BaseModel is not object:
    class QueryRequest(BaseModel):
        query: str


    class QueryResponse(BaseModel):
        answer: str
        raw: dict[str, Any] | None = None


    @app.post("/api/agent/query", response_model=QueryResponse)
    def query_agent(payload: QueryRequest, authorization: str | None = Header(default=None)):
        if api_key and api_key != "change-me":
            token = (authorization or "").replace("Bearer", "").strip()
            if token != api_key:
                raise HTTPException(status_code=401, detail="Unauthorized")
        result = agent.invoke({"input": payload.query})
        return QueryResponse(answer=result.get("output", ""), raw=result)


    @app.get("/health")
    def health():
        return {"status": "ok"}
