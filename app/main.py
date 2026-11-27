import json
import os
import time
from fastapi.staticfiles import StaticFiles
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from app.agent.tools import add, avg, safe_div, fetch_repo_count

app = FastAPI(title="Interview Coach")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/calc")
def calc(a: int, b: int):
    return {"a": a, "b": b, "add": add(a, b), "avg": avg([a, b])}

@app.get("/question/{qid}")
def get_question(qid: int):
    return {"id": qid, "text": "请介绍一下你最有代表性的项目"}

@app.get("/div")
def div(a: int, b: int):
    result = safe_div(a, b)
    if result is None:
        return {"error": "除数不能为 0"}
    return {"result": result}

@app.get("/score")
def score(answer: str):
    if not answer.strip():
        raise HTTPException(status_code=400, detail="答案不能为空")
    return {"length": len(answer)}

@app.get("/github/{username}")
def github(username: str):
    return {"repos": fetch_repo_count(username)}

@app.get("/stream-demo")
def stream_demo():
    def generate():
        for i in range(5):
            yield f"data: 第{i+1}段\n\n"
            time.sleep(0.5)

    return StreamingResponse(generate(), media_type="text/event-stream")

@app.get("/generate-question")
def generate_question(jd: str):
    def generate():
        try:
            r = requests.post(
                "https://api.deepseek.com/chat/completions",
                headers={
                    "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {
                            "role": "system",
                            "content": "你是技术面试官。根据岗位 JD 出一道面试题，只输出题目本身，不要解释。",
                        },
                        {"role": "user", "content": jd},
                    ],
                    "stream": True,
                },
                stream=True,
                timeout=60,
            )
            r.raise_for_status()

            for line in r.iter_lines(decode_unicode=True):
                if not line or not line.startswith("data: "):
                    continue
                payload = line[6:]
                if payload == "[DONE]":
                    break
                chunk = json.loads(payload)
                delta = chunk["choices"][0]["delta"].get("content", "")
                if delta:
                    yield f"data: {delta}\n\n"

        except Exception as e:
            yield f"data: [错误] {e}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")