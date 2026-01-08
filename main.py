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
    except:
        return JSONResponse(content={"code": 0})

    # 🔑 Respond to challenge immediately
    if "challenge" in payload:
        return JSONResponse(
            content={"challenge": payload["challenge"]},
            status_code=200,
            media_type="application/json"
        )

    # Otherwise, acknowledge event
    return JSONResponse(content={"code": 0})

