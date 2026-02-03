# ncp-focus-converter

## Table of Contents
[Description](#description)<br/>
[NCP Column Information](#ncp-column-information)<br/>
[Converting Solution](#converting-solution)<br/>

## Description
Naver Cloud Platform (NCP) is a cloud platform provided by Naver, a tech company based in Korea. Our primary goal is to fetch billing data from NCP's Billing API, convert it into the FOCUS format, and save it as a CSV file. Furthermore, our secondary goal is to upload the converted CSV to IBM Cloudability—IBM's cloud cost management and optimization service—to verify if the data works correctly.

## NCP Column Information
Due to significant discrepancies between NCP's billing API column formats and the FOCUS schema, we analyzed the billing dataset to map NCP values to the corresponding FOCUS columns. The following table describes the mandatory FOCUS columns, mapped using the JSON response fields retrieved from the NCP Billing API.

>**※[Note] Mapping Strategy※**


Since explicit definitions for NCP's billing API fields are unavailable, we inferred the meaning of each key and mapped them to the most semantically similar FOCUS columns.

### BillingAccountId
||Key|Value(Example)|DataType|Description|
| --- | --- | --- | --- | --- |
|FOCUS|BillingAccountId|1234567|String|BillingAccountId is the identifier for the account that being charged.|
|NCP|memberNo|3649505|String|memberNo is also the identifier for the account that being charged.|


Mapped NCP's memberNo to FOCUS's BillingAccountId as both fields function as the unique identifier for the account.

### BIllingAccountName
||Key|Value(Example)|DataType|Description|
| --- | --- | --- | --- | --- |
|FOCUS|BillingAccountName|'Mir Lee'|String|Display name that associates with the billing account|
|NCP| - | - | - |No corresponding value exists in the source data.|


Since the source data lacks corresponding values, we could not directly map this column. Instead, we applied a static value to ensure the CSV clearly identifies the billing account associate.

### BillingCurrency
||Key|Value(Example)|DataType|Description|
| --- | --- | --- | --- | --- |
|FOCUS|BillingCurrency|USD|String|Currency Code for the billing data|
|NCP|payCurrency(code)|KRW|String|Also Currency Code for the billing data|


In the NCP billing JSON structure, currency information is provided within the payCurrency object. We extracted the corresponding value from this field to map BillingCurrency.

### BillingPeriodStart
||Key|Value(Example)|DataType|Description|
| --- | --- | --- | --- | --- |
|FOCUS|BillingPeriodStart|2024-01-01T00:00:00Z|ISO8601|The inclusive start date and time of the billing period.|
|NCP|demandMonth|202401|Integer|Indicates the billed month|


NCP's demandMonth provides the billing period in a monthly format (YYYYMM). Since FOCUS requires ISO 8601 format, we transformed this value into the standard datetime format.|

### BillingPeriodEnd
||Key|Value(Example)|DataType|Description|
| --- | --- | --- | --- | --- |
|FOCUS|BillingPeriodEnd|2024-01-01T00:00:00Z|ISO8601|The exclusive end date and time of the billing period.|
|NCP|demandMonth|202401|Integer|Indicates the billed month|


NCP's demandMonth provides the billing period in a monthly format (YYYYMM). Since FOCUS requires ISO 8601 format, we transformed this value into the standard datetime format.

### BilledCost
||Key|Value(Example)|DataType|Description|
| --- | --- | --- | --- | --- |
|FOCUS|BilledCost|1300|Decimal|The actual amount charged on the invoice after all discounts and credits.|
|NCP|thisMonthDemandAmount|0|Decimal|Represents the final billed amount for the current month, after applying discounts and taxes.|


Mapped NCP's thisMonthDemandAmount to FOCUS's BilledCost as both fields function as the final billed amount for the current month after applying discounts and taxes.

### ContractedCost
||Key|Value(Example)|DataType|Description|
| --- | --- | --- | --- | --- |
|FOCUS|ContractedCost|14934|Decimal|The cost calculated based on the negotiated contract rates like Enterprise Discount (before credits).|
|NCP| - | - | - |No corresponding value exists in the source data.|


Although the NCP billing JSON lacks a direct ContractedCost field, the necessary components for this calculation are present in other keys. We analyzed these fields and established a formula to derive the closest equivalent value.

### ListCost
||Key|Value(Example)|DataType|Description|
| --- | --- | --- | --- | --- |
|FOCUS|ListCost|36290|Decimal|The standard price of the service without any discountsd applied.|
|NCP|useAmount|26290|Decimal|Data stored under demandCostList|


Map NCP's useAmount (the original amount before discount) to List Price.

### EffectiveCost
||Key|Value(Example)|DataType|Description|
| --- | --- | --- | --- | --- |
|FOCUS|EffectiveCost|0|Decimal|The amortized cost that includes the distribution of upfront fees (e.g., for reserved instances).|
|NCP|totalDemandAmount|0|Decimal|The total demand amount of the bill|


Map NCP's totalDemandAmount (final adjusted amount) to EffectiveCost.

### ChargeCategory
||Key|Value(Example)|DataType|Description|
| --- | --- | --- | --- | --- |
|FOCUS|ChargeCategory|GEN|String|The high-level category of the charge.|
|NCP|demandAttribute(code)|General|String|Identify the nature of the bill.|


Map NCP attribute codes to FOCUS categories.

### ChargeClass
||Key|Value(Example)|DataType|Description|
| --- | --- | --- | --- | --- |
|FOCUS|ChargeClass|Regular|String|Distinguish between regular charges and adjustments.|
|NCP| - | - | - |No corresponding value exists in the source data.|


Static value. Distinguish between regular charges and adjustments.

### ChargeDescription
||Key|Value(Example)|DataType|Description|
| --- | --- | --- | --- | --- |
|FOCUS|ChargeDescription|VPC Maintenance|String|A detailed description of the line item provided by the billing source.|
|NCP|meteringType(codeName)|VPC Maintenance|String|Provides a summary description to help users understand the reason for the charge.|


Populate the description field using NCP's codeName.

### ChargePeriodStart
||Key|Value(Example)|DataType|Description|
| --- | --- | --- | --- | --- |
|FOCUS|ChargePeriodStart|"2026-01-16T00:00:00+0900"|ISO8601|The actual start date and time when the resource was used.|
|NCP|useDate(useStartDate)|"2026-01-16T00:00:00+0900"|ISO8601|The actual start time of resource usage.|


Map the start time of daily usage data down to the second.

### ChargePeriodEnd
||Key|Value(Example)|DataType|Description|
| --- | --- | --- | --- | --- |
|FOCUS|ChargePeriodEnd|"2026-01-16T00:00:00+0900"|ISO8601|The actual End date and time when the resource was used.|
|NCP|useDate(useEndDate)|"2026-01-16T00:00:00+0900"|ISO8601|The actual End time of resource usage.|


Map the End time of daily usage data down to the second.

### PricingQuantity
||Key|Value(Example)|DataType|Description|
| --- | --- | --- | --- | --- |
|FOCUS|PricingQuantity|12.1|Decimal|The quantity used to calculate the cost (may differ from UsageQuantity).|
|NCP|userUsageQuantity|12.234|Decimal|The actual usage quantity used as the basis for cost calculation.|


Use the usage quantity from NCP as-is, retaining decimal precision.

### PricingUnit
||Key|Value(Example)|DataType|Description|
| --- | --- | --- | --- | --- |
|FOCUS|PricingUnit|Hour(s)|String|The unit of measure associated with the PricingQuantity (e.g., "Hours", "GB").|
|NCP|userUnit(codeName)|Hour|String|Usage Unit|


Convert NCP unit codes (e.g., HOUR) into human-readable units (e.g., Hours).

### ProviderName
||Key|Value(Example)|DataType|Description|
| --- | --- | --- | --- | --- |
|FOCUS|ProviderName|NCP|String|Source entity providing the service.|
|NCP| - | - | - |No corresponding value exists in the source data.|


Set ProviderName to a fixed value, as this is an NCP project.

### PublisherName
||Key|Value(Example)|DataType|Description|
| --- | --- | --- | --- | --- |
|FOCUS|PublisherName|NCP|String|The entity that produces and provides the service.|
|NCP| - | - | - |No corresponding value exists in the source data.|


Since this is not a marketplace item, set Publisher to be the same as ProviderName.

### InvoiceIssuerName
||Key|Value(Example)|DataType|Description|
| --- | --- | --- | --- | --- |
|FOCUS|InvoiceIssuerName|NCP|String|The name of the entity that issued the invoice (useful if billed through a reseller/MSP).|
|NCP| - | - | - |No corresponding value exists in the source data.|


Accurately record the legal name of the billing entity.

### ServiceCategory
||Key|Value(Example)|DataType|Description|
| --- | --- | --- | --- | --- |
|FOCUS|ServiceCategory|VPC(VirtualCloud)|String|The general classification of the service (e.g., "Compute", "Storage", "Database").|
|NCP|productItemKind(codeName)|VPC(VirtualCloud)|String|Core Functional Unit|


Extract category information from the contractProduct path.

### ServiceName
||Key|Value(Example)|DataType|Description|
| --- | --- | --- | --- | --- |
|FOCUS|ServiceName|VPC(VirtualCloud)|String|The specific name of the service consumed.|
|NCP|contractType(codeName)|VPC(VirtualCloud)|String|The specific name of the service or offering consumed.|


Extract the actual service name from the contract path. 


## Converting Solution
### Key Steps
[A. Mapping NCP Column to FOCUS format | FOCUS 형식으로 NCP 컬럼 매핑하기](#A-Mapping-NCP-Column-to-FOCUS-format-|-FOCUS-형식으로-NCP-컬럼-매핑하기)<br/>
[B. Requesting data from API | API에서 데이터 불러오기](#B-Requesting-data-from-API-|-API에서-데이터-불러오기)<br/>
[C. Convert JSON to FOCUS format CSV(ETL)-|-JSON을-FOCUS-형식의-CSV-파일로-변환(ETL)](#C-Convert-JSON-to-FOCUS-format-CSV(ETL)-|-JSON을-FOCUS-형식의-CSV-파일로-변환(ETL))<br/>
[D. Upload to AWS S3 | AWS S3에 업로드 하기](#D-Upload-to-AWS-S3-|-AWS-S3에-업로드-하기)<br/>
[E. Construct Pipeline | 파이프라인 구축](#E-Construct-Pipeline-|-파이프라인-구축)<br/>
[F. Result on Cloudability | Cloudability에서의 결과](#F-Result-on-Cloudability-|-Cloudability에서의-결과)<br/>
* * *
#### **A. Mapping NCP Column to FOCUS format | FOCUS 형식으로 NCP 컬럼 매핑하기**
>Since explicit definitions for NCP's billing API fields are unavailable, we inferred the meaning of each key and mapped them to the most semantically similar FOCUS columns.<br><br>
>NCP 청구 API 필드에서 지원하지 않는 컬럼들이 존재하므로, 각각의 키의 뜻을 파악하고 가장 비슷한 FOCUS 컬럼에 매칭시켜서 매핑했습니다.
* * *
#### **B. Requesting data from API | API에서 데이터 불러오기**
>Retrieves billing data via the NCP Billing API and exports it to JSON and XMP formats. <br><br>
>NCP 청구 API에서 청구 데이터를 받아서 JSON 또는 XMP 파일 형식으로 내보냅니다.

**Static values are injected into the code to account for specific data fields that are not provided by the API.<br>**

API에서 제공되지 않는 데이터는 고정값으로 코드에 입력해두었습니다.


```python
ACCOUNT_NAME_MAP = {
    "3649505":"Mir Lee",
    # Add keys and values of users if needed
    # ex) "1234567":"Account Name"
}
```

**The 'Account Name' can be manually injected into the dictionary as a static value.<br>**

Account Name은 딕셔너리를 이용해서 수동으로 고정값의 형식으로 추가 입력 가능합니다.

```python
PROVIDER_NAME = "Naver Cloud Platform"
INVOICE_ISSUER_NAME = "NAVER Cloud Corp."
PUBLISHER_NAME = "NAVER Cloud Platform"
```

**NCP Billing API does not provides name values, so we added name values as a static value too.<br>**

NCP API에서 Name 값을 제공하지 않기 때문에 다양한 Name 또한 고정값으로 넣어두었습니다.

```python
def get_account_name(member_no: str) -> str:
    return ACCOUNT_NAME_MAP.get(member_no, f"Account-{member_no}")
```
* * *
#### **C. Convert JSON to FOCUS format CSV(ETL) | JSON을 FOCUS 형식의 CSV 파일로 변환(ETL)**
>Since IBM Cloudability support FOCUS format csv, extracted JSON must be converted into FOCUS formatted CSV file.<br><br>
>IBM Cloudability는 FOCUS 형식의 CSV를 지원하기에, 추출된 JSON은 FOCUS 형식의 CSV 파일로 변환 되어야 합니다.

**To convert JSON to FOCUS format CSV, importing pandas and json package is necessary. <br>**

JSON을 FOCUS 형식의 CSV로 변환하기 위해선, pandas와 json 패키지를 무조건 불러와야합니다.

```python
import pandas as pd
import json
```

**Import JSON data<br>**

JSON 데이터 불러오기

```python
with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
```

**Since some data required normalization, added code to normalize it.<br>**

몇몇 데이터는 일반화를 필요로 하므로, 데이터를 일반화하는 코드를 추가합니다.

```python
# Example
billing_list = data['billing']['getDemandCostListResponse']['demandCostList']
df_billing = pd.json_normalize(billing_list)
```

**As a final step, use to_csv to convert the JSON file to CSV format.<br>**

마지막으로, to_csv를 이용하여 JSON 파일을 CSV 형식으로 변환합니다.

```python
map_list = [
    'BillingAccountId',
    'BillingAccountName',
    ...
]

df = df[map_list]
df.to_csv('ncp_focus_format.csv', index=False, encoding='utf-8')
```
* * *
#### **D. Upload to AWS S3 | AWS S3에 업로드 하기**
>Upload the converted CSV file to the AWS S3 bucket using Python to achieve the primary goal of migrating the NCP billing dataset.<br><br>
>파이썬을 이용하여 AWS S3 버킷에 변환된 CSV 파일을 올림으로서 NCP 청구 데이터셋을 IBM Cloudability에 마이그레이션하려는 1차 목표를 달성합니다.


**To upload files to AWS S3 using Python, you must import boto3, the standard AWS SDK for Python.<br>**

파이썬을 이용해 AWS S3에 파일을 업로드 하려면, 파이썬용 AWS SDK인 boto3를 불러와야 합니다.

```python
import boto3
...
client = boto3.client('s3',
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_DEFAULT_REGION
                      )

session = boto3.Session(
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_DEFAULT_REGION
                      )
```

**Upload processed data to AWS bucket.<br>**

AWS 버킷에 가공된 데이터를 업로드 합니다.

```python
client.upload_file('ncp_focus_format.csv',AWS_BUCKET_NAME,csv_s3_path)
```

**Generate a metadata manifest to prepare for future Cloudability integration, ensuring the system is ready for automated ingestion.<br>**

차후 자동화 생성 시스템을 구성하여 Cloudability와의 연동을 진행하기 위해 메타데이터 매니페스트를 생성합니다.

```python
manifest = {
    "compression":"gzip",
    "content_Type":"CSV",
    "report_id":str(uuid.uuid4()),
    "root_dir":AWS_BUCKET_NAME,
    "all_report_keys":[csv_s3_path],
    "updated_at":datetime.utcnow().isoformat()+"Z",
    "focus_version":"1.0"
}
```


**Upload Manifest.json to AWS S3<br>**

AWS S3에 Manifest.json을 업로드 합니다.



```python
manifest_s3_path = f"manifests/{filenamemonth}/Manifest.json"
json_str = json.dumps(manifest, indent=2, ensure_ascii=False)
client.put_object(Bucket=AWS_BUCKET_NAME, Key=manifest_s3_path, Body=json_str)
```
* * *
#### **E. Construct Pipeline | 파이프라인 구축**
>This pipeline is designed to streamline the conversion, storage, and analysis of billing data.<br><br>
>이 자동화 파이프라인은 청구 데이터의 변환, 저장, 분석을 간소화하기 위해 설계되었습니다.

**Encapsulated the column renaming and CSV conversion logic in etl.py into a single function.<br>**

컬럼 이름 재설정과 CSV 변환 코드를 etl.py에 캡슐화하여 하나의 함수로 만들었습니다.

```python
def cenvert_focus(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    billing_list = data['billing']['getDemandCostListResponse']['demandCostList']
    ...
```

**Import encapsulated functions(including test_api2.py) into the main Python script.<br>**

캡슐화된 기능들을 메인으로 사용할 파이썬 스크립트에 불러옵니다.

```python
import etl
import test_api2
...
```

**The pipeline generates both raw data and the FOCUS-converted CSV in a single line of code using encapsulated functions.<br>**

파이프라인은 캡슐화된 함수들을 이용하여 raw data 생성과 FOCUS 형식으로 변환된 CSV 생성을 단 한줄의 코드로 가능하게 합니다.

```python
test_api2.rawdata(focus_startmonth,focus_endmonth,focus_startdate, focus_enddate)
etl.cenvert_focus('raw_ncp_data.json')
```

**Upload both the converted dataset and raw data file to AWS S3.<br>**

변환된 데이터셋과 raw data 파일을 AWS S3에 업로드합니다.

```python
# raw data upload
json_s3_path = f"raw/{filenamemonth}/raw_ncp_data.json"
client.upload_file('raw_ncp_data.json',AWS_BUCKET_NAME,json_s3_path)

# processed data(FOCUS converted csv) upload
csv_s3_path = f"processed/{filenamemonth}/ncp_focus_format.csv"
client.upload_file('ncp_focus_format.csv',AWS_BUCKET_NAME,csv_s3_path)
```

**The pipeline concludes by uploading manifest file to AWS S3.<br>**
파이프라인은 manifest file을 AWS S3에 업로드 함으로서 마무리 됩니다.
* * *
#### **F. Result on Cloudability | Cloudability에서의 결과**
