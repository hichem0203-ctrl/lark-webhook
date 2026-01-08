from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/lark/approval")
async def lark_approval(req: Request):
    try:
        payload = await req.json()
    except Exception:
        # If JSON parsing fails
        return JSONResponse(content={"code": 0})

    print("Received payload:", payload)

    # 🔑 Lark challenge verification
    if "challenge" in payload:
        return JSONResponse(content={"challenge": payload["challenge"]})

    # Acknowledge other events
    return JSONResponse(content={"code": 0})

