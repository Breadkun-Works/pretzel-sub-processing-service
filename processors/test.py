"""
예시 프로세서 : ?name=홍길동 → {"greeting": "안녕, 홍길동!"}
"""


async def run(params: dict) -> dict:
    # GET 방식이라면 params는 쿼리스트링 dict
    # POST 방식이라면 params는 JSON Body dict
    name = params.get("name", "이름없음")
    return {"greeting": f"안녕, {name}!"}
