from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/lark/approval")
async def lark_approval(req: Request):
    payload = await req.json()
    print("Received payload:", payload)

    # 🔑 Lark webhook challenge verification
    if "challenge" in payload:
        return JSONResponse(content={"challenge": payload["challenge"]})

    # For now, just acknowledge the event
    return JSONResponse(content={"code": 0})

