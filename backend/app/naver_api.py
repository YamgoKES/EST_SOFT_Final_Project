import os
import urllib.request
import urllib.parse
import json
from dotenv import load_dotenv

load_dotenv()  # .env에서 클라이언트 키 불러오기

def search_naver_items(query, display=1):
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")

    enc_query = urllib.parse.quote(query)
    url = f"https://openapi.naver.com/v1/search/shop.json?query={enc_query}&display={display}"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    try:
        with urllib.request.urlopen(request) as response:
            rescode = response.getcode()
            if rescode == 200:
                response_body = response.read()
                data = json.loads(response_body.decode('utf-8'))

                # 1~3개만 추출
                result_items = []
                for item in data.get("items", [])[:display]:
                    result_items.append({
                        "title": item["title"].replace("<b>", "").replace("</b>", ""),
                        "image": item["image"],
                        "link": item["link"]
                    })
                return result_items
            else:
                print("Error Code:", rescode)
                return []
    except Exception as e:
        print("네이버 검색 API 호출 오류:", e)
        return []