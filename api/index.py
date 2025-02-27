from fastapi.responses import JSONResponse # 인코딩 UTF-8로 바꾸는 코드 추가
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
            "kage": str(kage),
            "zodiac": z,
            "speaker": "홍길동",
            "basedate": str(today),
            "os-name": get_os_pretty_name(),
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

#함수 이름만으로 기능을 유추할 수 있는 게 좋은 코딩임
def get_os_pretty_name():     
    with open('/etc/os-release', 'r') as file: 
        for line in file:
            if line.startswith('PRETTY_NAME'):
                # PRETTY_NAME=\"Ubuntu 24.0.1 LTS\"\n"
                # \"Ubuntu 24.0.1 LTS\"\n"
                return line.split('=')[1].replace('\n','').strip("\"")
    return None

def test_first():
    v = get_os_pretty_name()
    assert v is not None
    assert v == "Ubuntu 24.04.1 LTS"
    # 문자열에 LTS가 포함되었는지
    assert "LTS" in v
    # 문자열에 문자도 있고, 숫자도 있는지
   #assert v ==
    # .이 포함되어 있는지
    assert v.find(".") != -1
    # 길이가 적어도 얼마 이상인지...
    assert len(v) >= 10
    # 기타 등등...

#@app.get("/api/py/select_all")
#def select_all():
    #import pandas as pd
    # pandas dataframe 임의로 하나 만들어서 10분 가이드 초입
    # 임의로 만든 dataframe 을 아래와 같은 형식으로 리턴
    # dt.to_dict()
    # TODO
    # DB에서 읽어봐서 DataFrame으로 변환 후 아래와 같은 형식으로 리턴
    #import json
    #json_data = '''
    #[
    #    {"id": 1, "name": "Kim"},
    #    {"id": 2, "name": "Lee"}
    #]        
    #'''
    
#    
    
#    data = json.loads(json_data)
#    df = pd.DataFrame(data)    
#    return df.to_dict(orient="records")
    
 
from dotenv import load_dotenv
import psycopg
import os
from psycopg.rows import dict_row

load_dotenv()

DB_CONFIG = {
    "user": os.getenv("POSTGRES_USER"),
    "dbname": os.getenv("POSTGRES_DATABASE"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("DB_PORT", "5432")
}
# DB_CONFIG = {
#     "user": os.getenv("DB_USERNAME"),
#     "dbname": os.getenv("DB_NAME"),
#     "password": os.getenv("DB_PASSWORD"),
#     "host": os.getenv("DB_HOST"),
#     "port": os.getenv("DB_PORT")
# }


@app.get("/api/py/select_all")       
def select_all():
    # query = """
    # SELECT
    #     l.menu_name,
    #     m.name,
    #     l.dt
    # FROM 
    #     lunch_menu l
    #     inner join member m
    #     on l.member_id = m.id

    # """
    with psycopg.connect(**DB_CONFIG, row_factory=dict_row) as conn:
        #cur = conn.execute(query)
        cur = conn.execute("select * from view_select_all")  # DBeaver에서 localdb 쿼리에서 view 사용했음
        rows = cur.fetchall()       
        for row in rows:  # 인코딩 UTF-8로 바꾸는 코드 추가
            for key, value in row.items():  # 인코딩 UTF-8로 바꾸는 코드 추가
                if isinstance(value, date):  # 인코딩 UTF-8로 바꾸는 코드 추가
                    row[key] = value.strftime('%Y-%m-%d')   # 인코딩 UTF-8로 바꾸는 코드 추가
        return JSONResponse(content=rows, headers={"Content-Type": "application/json; charset=utf-8"})
        #return rows
    #df = pd.DataFrame(rows, columns=['id','name', 'dt']) -- row_factory 쓰면 이거 안써도 됨.
    #return df  







    
    #conn = get_connection()
    #cursor = conn.cursor()
    #cursor.execute(query)
    #rows = cursor.fetchall()
    #cursor.close()
    #conn.close()
      
    
    
        
    # return {"message": "Hello from FastAPI"}
