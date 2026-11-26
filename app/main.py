from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from app.agent.tools import add, avg, safe_div
from app.agent.tools import add, avg, safe_div, fetch_repo_count
app = FastAPI(title="Interview Coach")

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