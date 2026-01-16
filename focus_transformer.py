import pandas as pd
import json

with open('raw_ncp_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

billing_list = data['billing']['getDemandCostListResponse']['demandCostList']
df_billing = pd.json_normalize(billing_list)

# 열 이름이 겹치지 않게 접두사 추가
df_billing = df_billing.add_prefix('billing_')

# 사용 내역(Usage) 추출 및 평면화
usage_list = data['usageDaily']['getContractUsageListByDailyResponse']['contractUsageListByDaily']
df_usage = pd.json_normalize(usage_list)

# 이 데이터셋에는 billing 정보가 1개이므로, 모든 usage 행에 동일한 billing 정보를 복사해서 붙입니다.
df = df_usage.assign(**df_billing.iloc[0].to_dict())
df.to_csv('raw_ncp_data.csv', index=False, encoding='utf-8')
