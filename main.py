from fastapi import FastAPI
from pydantic import BaseModel
import fastapi_poe as fp
import asyncio
import os

app = FastAPI()

POE_API_KEY = os.environ.get("POE_API_KEY", "")

class TopicRequest(BaseModel):
    keyword: str

@app.post("/generate")
async def generate_topic(request: TopicRequest):
    keyword = request.keyword
    
    prompt = (
        "你係一個香港派對主持人。\n"
        "用家輸入咗關鍵字「" + keyword + "」。\n\n"
        "請用以下格式回覆（繁體中文）：\n\n"
        "[問題]\n"
        "一條有趣嘅派對話題問題，同關鍵字有關，20-40字。\n\n"
        "[延伸]\n"
        "• 延伸問題一\n"
        "• 延伸問題二\n"
        "• 延伸問題三\n\n"
        "只返回以上格式，不需要其他說明。"
    )
    
    message = fp.ProtocolMessage(role="user", content=prompt)
    
    full_response = ""
    async for partial in fp.get_bot_response(
        messages=[message],
        bot_name="Claude-3-Haiku",
        api_key=POE_API_KEY
    ):
        full_response += partial.text
    
    lines = full_response.strip().split("\n")
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
        elif in_question and not line.startswith("

---

## 步驟

1. 去 **GitHub** → 你的 `poe-party-server` repo
2. 打開 `main.py`
3. 按右上角 **鉛筆圖示（Edit）**
4. 將全部內容刪除
5. 貼上上面完整代碼
6. 按 **「Commit changes」**
7. Railway 會自動重新部署（約2分鐘）
8. 再試 app

---

**問題原因：** 原本 `main.py` 入面用咗：
```python
lines = full_response.strip().split("
