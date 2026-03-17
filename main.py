from fastapi import FastAPI
from pydantic import BaseModel
import fastapi_poe as fp
import asyncio

app = FastAPI()

# ⚠️ 換成你嘅 Poe API Key
POE_API_KEY = "你的Poe API Key"

class TopicRequest(BaseModel):
    keyword: str

@app.post("/generate")
async def generate_topic(request: TopicRequest):
    keyword = request.keyword
    
    prompt = f"""
    你係一個香港派對主持人。
    用家輸入咗關鍵字「{keyword}」。
    
    請用以下格式回覆（繁體中文）：
    
    [問題]
    一條有趣嘅派對話題問題，同關鍵字有關，20-40字。
    
    [延伸]
    • 延伸問題一
    • 延伸問題二
    • 延伸問題三
    
    只返回以上格式，不需要其他說明。
    """
    
    message = fp.ProtocolMessage(role="user", content=prompt)
    
    full_response = ""
    async for partial in fp.get_bot_response(
        messages=[message],
        bot_name="Claude-3-Haiku",
        api_key=POE_API_KEY
    ):
        full_response += partial.text
    
    # 解析回應
    lines = full_response.strip().split("
")
    lines = [l.strip() for l in lines if l.strip()]
    
    main_question = ""
    follow_ups = []
    in_question = False
    in_follow_up = False
    
    for line in lines:
        if "[問題]" in line:
            in_question = True
            in_follow_up = False
        elif "[延伸]" in line:
            in_question = False
            in_follow_up = True
        elif in_question and not line.startswith("["):
            main_question = line
            in_question = False
        elif in_follow_up and line.startswith("•"):
            follow_ups.append(line)
    
    return {
        "success": True,
        "mainQuestion": main_question,
        "followUpQuestions": "
".join(follow_ups)
    }
