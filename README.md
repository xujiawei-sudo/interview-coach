# interview-coach

面试模拟 Agent：输入岗位 JD，AI 出题、追问、按维度打分并生成复盘报告。

> 开发中，当前完成基础接口服务。

## 技术栈

Python 3.11 · FastAPI · uvicorn

## 已完成

- [x] 目录分层：接口层（`app/main.py`）与工具层（`app/agent/tools.py`）
- [x] REST 接口：健康检查、计算、题目、评分
- [x] 异常处理：除零保护、HTTPException 400、外部 API 错误兜底

## 运行

```bash
pip install fastapi "uvicorn[standard]" requests
uvicorn app.main:app --reload
```

打开 http://127.0.0.1:8000/docs 查看接口文档。
