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
    # 만 나이 계산 
    if int(today.month) < int(birth_date.month): 
        age = age-1
    elif (today.month == birth_date.month and int(today.day) < int(birth_date.day)): 
        age = age-1

    z = zodiac(birth_date.year)

   #한국식나이계산
    
    import korean_age_calculator as kac

    kage = kac.how_korean_age(year_of_birth=birth_date.year)

    return {
            "birthday": birthday,
            "age": str(age) + " " + z + "한국나이: " + str(kage),
            "kage" str(kage),
            "zodiac": z,
            "speaker": "홍길동"
            "basedate": str(today),
            "message": "Age calculated successfully!"
            }
# 띠 계산
def zodiac(birth_year):
    return zodiac_animals[birth_year % 12 - 4]
    
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
