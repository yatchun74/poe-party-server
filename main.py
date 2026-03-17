from fastapi import FastAPI
from pydantic import BaseModel
import fastapi_poe as fp
import os

app = FastAPI()
POE_API_KEY = os.environ.get("POE_API_KEY", "")

class TopicRequest(BaseModel):
    keyword: str

@app.post("/generate")
async def generate_topic(request: TopicRequest):
    keyword = request.keyword
    prompt = "你係香港派對主持人，用繁體中文，針對關鍵字「" + keyword + "」生成一條有趣派對話題問題，再加三條延伸問題，格式：[問題]問題內容[延伸]• 問題一• 問題二• 問題三"
    message = fp.ProtocolMessage(role="user", content=prompt)
    result = ""
    async for partial in fp.get_bot_response(messages=[message], bot_name="Claude-3-Haiku", api_key=POE_API_KEY):
        result += partial.text
    parts = result.split("[延伸]")
    main_q = parts[0].replace("[問題]", "").strip() if parts else result
    follow = parts[1].strip() if len(parts) > 1 else "• 大家有冇類似經歷？\n• 你會點處理？\n• 有冇唔同睇法？"
    return {"success": True, "mainQuestion": main_q, "followUpQuestions": follow}

@app.get("/")
def health_check():
    return {"status": "ok"}
