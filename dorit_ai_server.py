from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="DoritAI")


class GenerateRequest(BaseModel):
    messages: list[dict]
    temperature: float = 0.7
    max_tokens: int = 2048


@app.get("/")
async def root():
    return {
        "status": "online",
        "name": "DoritAI",
    }


@app.post("/generate")
async def generate(request: GenerateRequest):
    # Временно проверяем, что HTTP-связь работает.
    # Модель подключим сюда следующим шагом.

    user_message = ""

    for message in reversed(request.messages):
        if message.get("role") == "user":
            user_message = message.get("content", "")
            break

    return {
        "answer": (
            "DoritAI получил сообщение: "
            + user_message
        )
    }
