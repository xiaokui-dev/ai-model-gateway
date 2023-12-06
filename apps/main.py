from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn
import openai
from loguru import logger
from logging_middleware import RequestIDMiddleware, LoggerConfig
from config import settings
import json

app = FastAPI()
app.add_middleware(RequestIDMiddleware)
LoggerConfig.setup_logger()


class ChatRequest(BaseModel):
    messages: list
    functions: Optional[list] = None


@app.get("/hello")
def hello():
    return "success"


@app.post("/chat/model/azure")
def azure(request: ChatRequest):
    logger.info("params = {}", request.model_dump_json())

    openai.api_type = "azure"
    openai.api_base = settings.AZURE_API_BASE
    openai.api_version = settings.AZURE_API_VERSION
    openai.api_key = settings.AZURE_API_KEY

    if not request.functions:
        response = openai.ChatCompletion.create(
            temperature=0,
            engine=settings.AZURE_DEPLOYMENT_NAME,
            messages=request.messages
        )
    else:
        response = openai.ChatCompletion.create(
            temperature=0,
            engine=settings.AZURE_DEPLOYMENT_NAME,
            messages=request.messages,
            functions=request.functions
        )
    logger.info("response = {}", json.dumps(response, ensure_ascii=False))

    return response


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080, access_log=False)
