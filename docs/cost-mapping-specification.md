# 📊 NCP to FOCUS v1.1 Mapping Table

| 상태 | FOCUS | NCP | FOCUS 형태 예시 | 데이터 타입 | 비고 |
|:---|:---|:---|:---|:---|:---|
| `확정` | BillingAccountId | `getDemandCostList` - demandCostList > memberNo | "3649505" | `String` | - |
| `확정` | BillingAccountName | "Mir Lee" | "Mir Lee" | `String` | 하드코딩 |
| `확정` | BillingCurrency | `getDemandCostList` - demandCostList > payCurrency > code | "KRW" | `String` | - |
| `확정` | BillingPeriodStart | `getDemandCostList` - billing...demandMonth 기반 | '2024-01-01T00:00:00Z' | `ISO 8601` | 202401 → 2024-01-01T00:00:00Z |
| `확정` | BillingPeriodEnd | `getDemandCostList` - billing...demandMonth 기반 | '2024-01-01T00:00:00Z' | `ISO 8601` | 202401 → 2024-01-01T00:00:00Z |
| `확정` | BilledCost | `getDemandCostList` - thisMonthDemandAmount | 1300 | `Decimal` | - |
| `검토 필요` | ContractedCost | `getContractDemandCostList` - `useAmount - (promiseDiscountAmount + customerDiscountAmount + productDiscountAmount + memberPriceDiscountAmount + memberPromiseDiscountAddAmount)` | 1100 | `Decimal` | List |
| `확정` | ListCost | `getDemandCostList` - demandCostList > useAmount | 36290 | `Decimal` | 할인이나 크레딧이 적용되기 전의 서비스 표준 정가. |
| `확정` | EffectiveCost | `getDemandCostList` - totalDemandAmount | 0 | `Decimal` | - |
| `검토 필요` | ChargeCategory | `getDemandCostList` - demandAttribute(CODE) | Usage | `String` | PRM은 기준 설정해서 Purchase와 Adjustment로 분류 |
| `확정` | ChargeClass | "Regular" | "Regular" | - | 아직까지 방법 없음 (일단 문서상 NULL값) |
| `확정` | ChargeDescription | `getContractUsageListByDailyResponse` - usage.meteringType.codeName | - | `String` | usage.codename과 contractType.codeName을 결합하면 좋을 듯 |
| `검토 필요` | ChargePeriodStart | getContractUsageListByDaily - useDate.useStartDate | "2024-01-09T00:00:00+0900" | `ISO 8601` | - |
| `검토 필요` | ChargePeriodEnd | getContractUsageListByDaily - useDate.useEndDate | "2024-01-09T23:59:59+0900" | `ISO 8601` | - | 
| `확정` | PricingQuantity | getContractUsageListByDaily - userUsageQuantity | 12.4975 | `Decimal` | - |
| `확정` | PricingUnit | getContractUsageListByDaily - userUnit.codeName | 시간 또는 GB(Hours, GB) | `String` | Hours(code: HOUR) | BillingAccountId | `getDemandCostList` - demandCostList > memberNo | "3649505" | `String` | - |
| `확정` | ProviderName | "NAVER Cloud Platform" | "NAVER Cloud Platform" | `String` | 고정값 |
| `확정` | PublisherName | "NAVER Cloud Platform" | "NAVER Cloud Platform" | `String` | 고정값 |
| `확정` | InvoiceIssuerName | "NAVER Cloud Corp." | "NAVER Cloud Corp." | `String` | 고정값 |
| `확정` | ServiceCategory | getContractUsageListByDaily - contractUsageListByDaily > contractProduct > productItemKind.codeName | "Compute" | `String` | 서비스 대분류는 상품의 속성임. contractProduct에서 가져오며, 구체적인 서비스 명칭은 계약의 성격에 따라 contract에서 가져오는 것이 적절 |
| `확정` | ServiceName | getContractUsageListByDaily - contractUsageListByDaily > contract > contractType.codeName | "VPC (Virtual Private Cloud)" | `String` | - |


---
*Last Updated: 2026-01-19* </br>
*Author: Jaewon Kim*