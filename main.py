from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import os

app = FastAPI()

# ================= CONFIG =================
APP_TOKEN = os.getenv("PnkhbMHLHaEoIgskn2Nl9if4g1p")      # bascn...
TENANT_TOKEN = os.getenv("t-g20618llYMN4C2X7DY3QHZZAG4O3YJWPJ3Q4ZHWR") # t-...
TABLE_MAP = {
    "BG6": "tblFK1uFutoK8kxE",
    "KL5": "tblgdLoqoVApFMta"
}

HEADERS = {
    "Authorization": f"Bearer {TENANT_TOKEN}",
    "Content-Type": "application/json"
}

# ================= HEALTH =================
@app.get("/")
def health():
    return {"status": "ok"}

# ================= WEBHOOK =================
@app.post("/lark/approval")
async def lark_approval(req: Request):
    payload = await req.json()

    # 🔑 Challenge verification
    if "challenge" in payload:
        return JSONResponse(content={"challenge": payload["challenge"]})

    model = payload.get("model")
    materials = payload.get("materials")  # <-- LIST

    if not model or not materials:
        return JSONResponse(content={"code": 0})

    table_id = TABLE_MAP.get(model)
    if not table_id:
        return JSONResponse(content={"code": 0})

    for mat in materials:
        item_code = mat.get("item_code")
        quantity = mat.get("quantity")

        if not item_code or not quantity:
            continue

        # 1️⃣ Search record
        search_url = f"https://open.larksuite.com/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{table_id}/records/search"
        search_body = {
            "filter": {
                "conjunction": "and",
                "conditions": [
                    {
                        "field_name": "Item Code",
                        "operator": "is",
                        "value": [int(item_code)]
                    }
                ]
            }
        }

        search_resp = requests.post(search_url, json=search_body, headers=HEADERS).json()
        items = search_resp.get("data", {}).get("items", [])

        if not items:
            print(f"Item not found: {item_code}")
            continue

        record = items[0]
        record_id = record["record_id"]
        current_stock = record["fields"]["Stock"]

        new_stock = max(0, current_stock - int(quantity))

        # 2️⃣ Update stock
        update_url = f"https://open.larksuite.com/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{table_id}/records/batch_update"
        update_body = {
            "records": [
                {
                    "record_id": record_id,
                    "fields": {"Stock": new_stock}
                }
            ]
        }

        requests.post(update_url, json=update_body, headers=HEADERS)
        print(f"{item_code}: {current_stock} → {new_stock}")

    return JSONResponse(content={"code": 0})

@app.post("/lark/test")
async def test_webhook(req: Request):
    payload = await req.json()
    print("Webhook received:", payload)
    return {"code": 0}

