import pandas as pd
import json
from decimal import Decimal

def cenvert_focus(filename):
    with open(filename, 'r', encoding='utf-8') as f:
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

    focus_map = {
        'account.memberNo' :'BillingAccountId',
        'billing_payCurrency.code':'BillingCurrency',
        'billing_demandMonth':'BillingPeriodStart',
        'billing_thisMonthDemandAmount':'BilledCost',
        'billing_useAmount':'ContractedCost',
        'billing_totalDemandAmount':'EffectiveCost',
        'billing_demandAttribute.code':'ChargeCategory',
        'usage.meteringType.codeName':'ChargeDescription',
        'useDate.useStartDate':'ChargePeriodStart',
        'useDate.useEndDate':'ChargePeriodEnd',
        'usage.userUsageQuantity':'PricingQuantity',
        'usage.userUnit.codeName':'PricingUnit',
        'contractProduct.productItemKind.codeName':'ServiceCategory',
        'contract.contractType.codeName':'ServiceName'
    }
    df = df.rename(columns=focus_map)

    df['BilledCost']
    df['ListCost'] = df['ContractedCost']
    df['BillingAccountName'] = 'Mir Lee' #하드코딩
    df['BillingPeriodEnd'] = df['BillingPeriodStart']
    df['BillingPeriodStart'] = df['BillingPeriodStart'].apply(
    lambda x: f"{str(x)[:4]}-{str(x)[4:6]}-01T00:00:00Z"
    )
    df['BillingPeriodEnd'] = df['BillingPeriodEnd'].apply(
    lambda x: f"{str(x)[:4]}-{str(x)[4:6]}-01T00:00:00Z"
    )
    df['ContractedCost'] = df['ContractedCost'].astype(float) \
        - (df['billing_promiseDiscountAmount'].astype(float) + df['billing_customerDiscountAmount'].astype(float)\
            + df['billing_productDiscountAmount'].astype(float) + df['billing_memberPriceDiscountAmount'].astype(float)\
                +df['billing_memberPromiseDiscountAddAmount'].astype(float))
    df['ChargeClass'] = 'Regular'
    df['ProviderName'] = 'Naver Cloud Platform'
    df['PublisherName'] = 'Naver Cloud Platform'
    df['InvoiceIssuerName'] = 'Naver Cloud Corp'


    map_list = [
        'BillingAccountId',
        'BillingAccountName',
        'BillingCurrency',
        'BillingPeriodStart',
        'BillingPeriodEnd',
        'BilledCost',
        'ContractedCost',
        'ListCost',
        'EffectiveCost',
        'ChargeCategory', 
        'ChargeClass',
        'ChargeDescription',
        'ChargePeriodStart',
        'ChargePeriodEnd',
        'PricingQuantity',
        'PricingUnit',
        'ProviderName',
        'PublisherName',
        'InvoiceIssuerName',
        'ServiceCategory',
        'ServiceName' 
    ]

    df = df[map_list]

    df.to_csv('ncp_focus_format.csv', index=False, encoding='utf-8')