from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/lark/approval")
async def lark_approval(req: Request):
    payload = await req.json()
    
    # 🔹 Step 1: Handle Lark challenge
    if "challenge" in payload:
        return JSONResponse(content={"challenge": payload["challenge"]})
    
    # 🔹 Step 2: Log normal approvals (we’ll keep it simple for now)
    print("Approval payload received:", payload)
    
    return JSONResponse(content={"code": 0})

