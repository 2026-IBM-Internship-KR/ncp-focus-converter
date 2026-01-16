import time
import hmac
import hashlib
import base64
import requests
import json
from typing import Dict, Any


# ===== 0. 설정 =====
NCP_ACCESS_KEY = "ncp_iam_BPAMKR2VP4dIe3b9D7yV"
NCP_SECRET_KEY = "ncp_iam_BPKMKR69PEH6WMCa2OjXuuMDgt15Qqc0uf"

# 0-1. memberNo -> BillingAccountName 매핑
ACCOUNT_NAME_MAP = {
    "3649505": "Mir Lee",
    # 필요하면 여기 계속 추가
    # "1234567": "NCP-Prod-Account",
}

# 0.2. FOCUS용 상수
PROVIDER_NAME = "Naver Cloud Platform"
INVOICE_ISSUER_NAME = "NAVER Cloud Corp."
PUBLISHER_NAME = "NAVER Cloud Platform"

def get_account_name(member_no: str) -> str:
    # 매핑 없으면 기본 이름으로
    return ACCOUNT_NAME_MAP.get(member_no, f"Account-{member_no}")


# ===== 1. 공통 시그니처 & HTTP 헬퍼 =====
def make_signature(method: str, uri: str, timestamp: str) -> str:
    message = f"{method} {uri}\n{timestamp}\n{NCP_ACCESS_KEY}"
    signing_key = bytes(NCP_SECRET_KEY, "UTF-8")
    message_bytes = bytes(message, "UTF-8")
    signature = base64.b64encode(
        hmac.new(signing_key, message_bytes, digestmod=hashlib.sha256).digest()
    )
    return signature.decode("UTF-8")


def ncp_get_billing(uri: str) -> Dict[str, Any]:
    """
    Billing 도메인 GET 공통 함수
    """
    method = "GET"
    timestamp = str(int(time.time() * 1000))
    signature = make_signature(method, uri, timestamp) 
    url = f"https://billingapi.apigw.ntruss.com{uri}"

    headers = {
        "x-ncp-apigw-timestamp": timestamp,
        "x-ncp-iam-access-key": NCP_ACCESS_KEY,
        "x-ncp-apigw-signature-v2": signature,
    }

    resp = requests.get(url, headers=headers)

    # 디버깅용
    print("[Billing] status:", resp.status_code)
    if not resp.text:
        print("[Billing] empty body")

    resp.raise_for_status()
    return resp.json()


# ===== 2. NCP Billing / Usage API 호출 =====
def call_get_demand_cost_list(start_month: str, end_month: str) -> Dict[str, Any]:
    """
    월별 청구 요약 (getDemandCostList)
    start_month, end_month: 'YYYYMM'
    """
    uri = (
        "/billing/v1/cost/getDemandCostList"
        f"?startMonth={start_month}&endMonth={end_month}&responseFormatType=json"
    )
    return ncp_get_billing(uri)


def call_get_contract_usage_by_daily(use_start_day: str, use_end_day: str) -> Dict[str, Any]:
    """
    일별 계약 사용량 (getContractUsageListByDaily)
    use_start_day, use_end_day: 'YYYYMMDD'
    """
    uri = (
        "/billing/v1/cost/getContractUsageListByDaily"
        f"?useStartDay={use_start_day}&useEndDay={use_end_day}&responseFormatType=json"
    )
    return ncp_get_billing(uri)


# ===== 3. 기간 메타 생성 =====
def add_period_and_account_info(resp_json: Dict[str, Any]) -> Dict[str, Any]:
    """
    getDemandCostList 응답에서 기간 관련 메타 정보를 추출해 metaPeriodInfo에 넣는다.
    """
    res = resp_json.get("getDemandCostListResponse", {})
    items = res.get("demandCostList", [])

    meta = {}
    billing_account_id = None
    billing_account_name = None

    if items:
        item = items[0]  # totalRows=1 가정
        member_no = item.get("memberNo")

        billing_account_id = member_no
        billing_account_name = get_account_name(member_no)

        meta = {
            "demandMonth": item.get("demandMonth"),
            "writeDate": item.get("writeDate"),
            "paidUpDate": item.get("paidUpDate"),
            "useAmount": item.get("useAmount"),
            "creditDiscountAmount": item.get("creditDiscountAmount"),
        }

    return {
        "metaPeriodInfo": meta,
        "billingAccount": {
            "BillingAccountId": billing_account_id,
            "BillingAccountName": billing_account_name,
        },
        "raw": resp_json,
    }

# === === === === === === === === === === === ===
# === merged JSON -> FOCUS rows 함수 추가 ===
def to_focus_rows(merged_json: dict) -> list[dict]:
    billing_item = merged_json["billing"]["getDemandCostListResponse"]["demandCostList"][0]
    usage_list = merged_json["usageDaily"]["getContractUsageListByDailyResponse"]["contractUsageListByDaily"]

    member_no = billing_item["memberNo"]
    currency = billing_item["payCurrency"]["code"]

    rows = []
    for u in usage_list:
        use_start = u["useDate"]["useStartDate"]
        use_end = u["useDate"]["useEndDate"]

        row = {
            # 계정 정보
            "BillingAccountId": member_no,
            "BillingAccountName": get_account_name(member_no),
            "BillingCurrency": currency,

            # Provider / Invoice 정보 (여기에 추가)
            "ProviderName": PROVIDER_NAME,
            "PublisherName": PUBLISHER_NAME,
            "InvoiceIssuerName": INVOICE_ISSUER_NAME,

            # Charge/기간 관련 예시
            "ChargeCategory": "Usage",
            "ChargeClass": "Regular",
            "ChargePeriodStart": use_start,
            "ChargePeriodEnd": use_end,
        }
        rows.append(row)

    return rows

# ===== 4. 메인 실행 =====
if __name__ == "__main__":
    # 1) 월별 청구 + 기간 메타
    raw_billing = call_get_demand_cost_list("202601", "202601")
    billing_info = add_period_and_account_info(raw_billing)

    # billing_with_period = add_period_and_account_info(raw_billing)
    # 2) 일별 Usage (예: 1~14일)
    usage_json = call_get_contract_usage_by_daily("20260101", "20260116")

    # 3) 하나의 JSON으로 합치기
    merged = {
        "metaPeriodInfo": billing_info["metaPeriodInfo"],
        "billingAccount": billing_info["billingAccount"],   
        "billing": billing_info["raw"],
        "usageDaily": usage_json, # getContractUsageListByDaily 원본
    }

    print("=== Merged NCP JSON ===")
    print(json.dumps(merged, indent=2, ensure_ascii=False))

    # 파일로 저장 (JSON만)
    with open("raw_ncp_data.json", "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

    # 2) FOCUS 행(JSON) 추가로 생성
    focus_rows = to_focus_rows(merged)
    with open("ncp_focus_rows.json", "w", encoding = "utf-8") as f:
        json.dump({"rows": focus_rows}, f, indent = 2, ensure_ascii = False)