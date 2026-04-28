import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

class Request(BaseModel):
    product: str
    price_min: str = ""
    price_max: str = ""
    reviews_count: str = ""

@app.post("/analyze")
async def analyze(request: Request):
    
    prompt = f"""
    Ты эксперт по маркетплейсам Wildberries и Ozon.
    
    Пользователь хочет продавать: {request.product}
    Цена конкурентов: от {request.price_min} до {request.price_max} рублей
    Среднее количество отзывов у топов: {request.reviews_count}
    
    Дай анализ по пунктам:
    1. Стоит ли заходить в эту нишу?
    2. Какую цену поставить для старта?
    3. Главные слабости конкурентов
    4. Что сделать чтобы выделиться
    5. Прогноз первых 3 месяцев
    
    Отвечай конкретно и по делу, без воды.
    """
    
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )
    
    return {"result": response.choices[0].message.content}

@app.get("/")
async def root():
    return {"status": "работает"}
