from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="DoritAI")


# =========================================================
# REQUEST
# =========================================================

class GenerateRequest(BaseModel):
    message: str = ""
    prompt: str = ""

    user_id: str = "default"
    chat_id: str = "default"

    # Оставляем возможность использовать messages
    messages: list[dict] | None = None

    temperature: float = 0.7
    max_tokens: int = 2048

    stream: bool = False


# =========================================================
# HEALTH
# =========================================================

@app.get("/")
async def root():

    return {
        "status": "online",
        "name": "DoritAI",
    }


# =========================================================
# GENERATE
# =========================================================

@app.post("/generate")
async def generate(request: GenerateRequest):

    user_message = request.message

    # Если сообщение пришло через messages
    if not user_message and request.messages:

        for message in reversed(request.messages):

            if message.get("role") == "user":

                user_message = (
                    message.get("content", "")
                )

                break

    user_message = user_message.strip()

    print("🤖 DoritAI GENERATE")
    print(f"👤 User: {request.user_id}")
    print(f"💬 Chat: {request.chat_id}")
    print(f"📝 Message: {user_message}")

    # =====================================================
    # ВРЕМЕННЫЙ ОТВЕТ
    # =====================================================

    answer = (
        "DoritAI получил сообщение: "
        + user_message
    )

    print(
        f"✅ DoritAI ANSWER: {answer}"
    )

    return {
        "answer": answer
    }
