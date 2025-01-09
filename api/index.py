from fastapi import FastAPI
from datetime import datetime, date
from typing import Dict
import random

### Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")

@app.get("/api/py/helloFastApi")
def hello_fast_api():
    return {"message": "Hello from FastAPI"}

@app.get("/api/py/ageCalculator/{birthday}")
def age_calculator(birthday: str) -> Dict[str, str]:
    """
    생년월일을 입력받아 만나이를 계산하는 API

    :param birthday: 생년월일 (형식: YYYY-MM-DD)
    :return: 생년월일 및 만나이를 포함한 JSON 응답
    """ 
    today = date.today()
    birth_date = datetime.strptime(birthday, "%Y-%m-%d").date()

    age = today.year - birth_date.year
    # TODO 생일 지난 여부 관련 로직 추가 개발 필요 
    if int(today.month) < int(birth_date.month): 
        age = age-1
    elif (today.month == birth_date.month and int(today.day) < int(birth_date.day)): 
        age = age-1

zodiac_animals = [
    "🐀 Rat",      # 자 - 쥐
    "🐂 Ox",       # 축 - 소
    "🐅 Tiger",    # 인 - 호랑이
    "🐇 Rabbit",   # 묘 - 토끼
    "🐉 Dragon",   # 진 - 용
    "🐍 Snake",    # 사 - 뱀
    "🐎 Horse",    # 오 - 말
    "🐐 Goat",     # 미 - 양
    "🐒 Monkey",   # 신 - 원숭이
    "🐓 Rooster",  # 유 - 닭
    "🐕 Dog",      # 술 - 개
    "🐖 Pig"       # 해 - 돼지
]

    def zodiac(birth_year):
      return zodiac_animals[birth_year % 12]

    
    return {
            "birthday": birthday,
            "age": str(age and zodiac),
            "basedate": str(today),
            "message": "Age calculated successfully!"
            }


