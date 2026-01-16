# NCP to FOCUS v1.1 Mapping Table

| 상태 | FOCUS | NCP | FOCUS 형태 예시 | 데이터 타입 | 비고 |
|:---|:---|:---|:---|:---|:---|
| 확정 | BillingAccountId | ```getDemandCostList``` - demandCostList > memberNo | "3649505” | String | - |
| 확정 | BillingAccountName | - | “Mir Lee” | String | 하드코딩 |
| 확정 | BillingCurrency | ```getDemandCostList``` - demandCostList > payCurrency > code | "KRW" | String | - |
| 검토 필요 | BillingPeriodStart | billing…demandMonth 기반 | ‘2024-01-01T00:00:00Z’ | ISO 8601 | - |
| 검토 필요 | BillingPeriodEnd | billing…demandMonth 기반 | ‘2024-01-01T00:00:00Z’ | ISO 8601 | - |
| 검토 필요 | BilledCost | totalDemandAmount | 1300 | Decimal | - |
| 검토 필요 | ContractedCost | useAmount | 1100 | Decimal | - |
| 검토 필요 | ListCost | ```getDemandCostList``` - demandCostList > useAmount | 36290 | Decimal | 할인이나 크레딧이 적용되기 전의 서비스 표준 정가. |
| 검토 필요 | EffectiveCost | totalDemandAmount | 0 | Decimal | - |
| 검토 필요 | ChargeCategory | demandAttribute(CODE) | Usage | String | PRM은 기준 설정해서 Purchase와 Adjustment로 분류 |
| 작성 중 | ChargeClass | - | - | - | 아직까지 방법 없음 (일단 문서상 NULL값) |
| 검토 필요 | ChargeDescription | usage.codename | - | String | usage.codename과 contractType.codeName을 결합하면 좋을 듯 |
| 검토 필요 | ChargePeriodStart | demandMonth(그 달 1일) | - | datetime | - |
| 검토 필요 | ChargePeriodEnd | demandMonth(그 달 막일) | - | datetime | - |
| 검토 필요 | PricingQuantity | ```getContractUsageListByDaily``` - userUsageQuantity | 12.4975 | Decimal | - |
| 검토 필요 | PricingUnit | ```getContractUsageListByDaily``` - userUnit.code | 시간 또는 GB(Hours, GB) | String | Hours(code: HOUR) |
| 검토 필요 | ProviderName | "NAVER Cloud” | "NAVER Cloud” | String | 고정값 |
| 검토 필요 | PublisherName | "NAVER Cloud” | "NAVER Cloud” | String | 고정값 |
| 검토 필요 | InvoiceIssuerName | "NAVER Cloud” | "NAVER Cloud” | String | 고정값 |
| 검토 필요 | ServiceCategory | ```getContractUsageListByDaily``` - contractProduct > productItemKind.codeName | (Compute, Storage) | String | 서비스 대분류는 상품의 속성이므로 contractProduct에서 가져오며, 구체적인 서비스 명칭은 contract에서 가져오는 것이 적절함. |
| 검토 필요 | ServiceName | ```getContractUsageListByDaily``` - contract > contractType.codeName | "VPC (Virtual Private Cloud)” | String | - |