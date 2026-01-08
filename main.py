from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/lark/approval")
async def lark_approval(req: Request):
    try:
        payload = await req.json()
    except:
        return JSONResponse(content={"error": "invalid json"}, status_code=400)

    # 🔹 Handle Lark challenge first
    if "challenge" in payload:
        return JSONResponse(content={"challenge": payload["challenge"]})

    # 🔹 Just log approvals for now
    print("Approval payload received:", payload)

    return JSONResponse(content={"code": 0})

