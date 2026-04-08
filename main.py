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
    prompt = (
        f"You are a fun party host. "
        f"Based on the keyword '{keyword}', generate ONE interesting party conversation question in English. "
        f"Then provide 3 short follow-up discussion questions in English. "
        f"Format your response exactly like this:\n"
        f"[Question] your main question here\n"
        f"[Extend]\n• follow-up question 1\n• follow-up question 2\n• follow-up question 3\n"
        f"Do not use any other language. English only."
    )
    message = fp.ProtocolMessage(role="user", content=prompt)
    result = ""
    async for partial in fp.get_bot_response(messages=[message], bot_name="Claude-3-Haiku", api_key=POE_API_KEY):
        result += partial.text
    parts = result.split("[Extend]")
    main_q = parts[0].replace("[Question]", "").strip() if parts else result
    follow = parts[1].strip() if len(parts) > 1 else "• Have you had a similar experience?\n• How would you handle it?\n• Do you have a different opinion?"
    return {"success": True, "mainQuestion": main_q, "followUpQuestions": follow}

@app.get("/")
def health_check():
    return {"status": "ok"}
