import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llama_cpp import Llama


# =========================================================
# CONFIG
# =========================================================

MODEL_PATH = os.getenv(
    "MODEL_PATH",
    "models/dorit-ai.gguf",
)

N_CTX = int(
    os.getenv("N_CTX", "1024")
)

MAX_TOKENS_LIMIT = 512


# =========================================================
# APP
# =========================================================

app = FastAPI(
    title="DoritAI"
)


# =========================================================
# MODEL
# =========================================================

print("🤖 Запуск DoritAI...")
print(f"🧠 Model: {MODEL_PATH}")

if not Path(MODEL_PATH).exists():
    raise RuntimeError(
        f"Модель не найдена: {MODEL_PATH}"
    )


llm = Llama(
    model_path=MODEL_PATH,

    # Маленький контекст экономит RAM
    n_ctx=N_CTX,

    # CPU
    n_gpu_layers=0,

    # Не выводим лишний лог llama.cpp
    verbose=False,
)

print("✅ DoritAI model loaded")


# =========================================================
# REQUEST
# =========================================================

class GenerateRequest(BaseModel):
    messages: list[dict]

    temperature: float = 0.7
    max_tokens: int = 256


# =========================================================
# HEALTH
# =========================================================

@app.get("/")
async def root():

    return {
        "status": "online",
        "name": "DoritAI",
        "model": "DoritAI Local",
    }


# =========================================================
# GENERATE
# =========================================================

@app.post("/generate")
async def generate(
    request: GenerateRequest,
):

    if not request.messages:

        raise HTTPException(
            status_code=400,
            detail="messages пустой",
        )

    max_tokens = min(
        max(request.max_tokens, 1),
        MAX_TOKENS_LIMIT,
    )

    try:

        print("🧠 DoritAI generating...")

        result = llm.create_chat_completion(
            messages=request.messages,
            temperature=request.temperature,
            max_tokens=max_tokens,
        )

        answer = (
            result["choices"][0]["message"]["content"]
            .strip()
        )

        if not answer:

            raise RuntimeError(
                "Модель вернула пустой ответ"
            )

        print(
            f"✅ DoritAI: {answer[:200]}"
        )

        return {
            "answer": answer,
        }

    except Exception as e:

        print(
            "❌ GENERATION ERROR:",
            repr(e),
        )

        raise HTTPException(
            status_code=500,
            detail="Ошибка генерации DoritAI",
        )
