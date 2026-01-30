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
[A. Mapping NCP Column to FOCUS format](#A-Mapping-NCP-Column-to-FOCUS-format)<br/>
[B. Requesting data from API](#B-Requesting-data-from-API)<br/>
[C. Convert JSON to FOCUS format CSV(ETL)](#C-Convert-JSON-to-FOCUS-format-CSV(ETL))<br/>
[D. Upload to AWS S3](#D-Upload-to-AWS-S3)<br/>
[E. Construct Pipeline](#E-Construct-Pipeline)<br/>
[F. Test on Clouda*bility](#F-Test-on-Cloudability)<br/>
* * *
#### **A. Mapping NCP Column to FOCUS format**
>Since explicit definitions for NCP's billing API fields are unavailable, we inferred the meaning of each key and mapped them to the most semantically similar FOCUS columns.
* * *
#### **B. Requesting data from API**
>Retrieves billing data via the NCP Billing API and exports it to JSON and XMP formats. 

Static values are injected into the code to account for specific data fields that are not provided by the API.


```python
ACCOUNT_NAME_MAP = {
    "3649505":"Mir Lee",
    # Add keys and values of users if needed
    # ex) "1234567":"Account Name"
}
```

The 'Account Name' can be manually injected into the dictionary as a static value.

```python
PROVIDER_NAME = "Naver Cloud Platform"
INVOICE_ISSUER_NAME = "NAVER Cloud Corp."
PUBLISHER_NAME = "NAVER Cloud Platform"
```

Added name values as a static value.

```python
def get_account_name(member_no: str) -> str:
    return ACCOUNT_NAME_MAP.get(member_no, f"Account-{member_no}")
```
* * *
#### **C. Convert JSON to FOCUS format CSV(ETL)**
>To convert JSON to FOCUS format CSV, importing pandas and json package is necessary.


```python
import pandas as pd
import json
```

Import JSON data

```python
with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
```

Since some data required normalization, added code to normalize it.

```python
# Example
billing_list = data['billing']['getDemandCostListResponse']['demandCostList']
df_billing = pd.json_normalize(billing_list)
```

As a final step, use to_csv to convert the JSON file to CSV format.

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
#### **D. Upload to AWS S3**
>Upload the converted CSV file to the AWS S3 bucket using Python to achieve the primary goal of migrating the NCP billing dataset.


To upload files to AWS S3 using Python, you must import boto3, the standard AWS SDK for Python.

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

Upload processed data to AWS bucket.

```python
client.upload_file('ncp_focus_format.csv',AWS_BUCKET_NAME,csv_s3_path)
```

Generates a metadata manifest to prepare for future Cloudability integration, ensuring the system is ready for automated ingestion.

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


Upload Manifest.json to AWS S3

```python
manifest_s3_path = f"manifests/{filenamemonth}/Manifest.json"
json_str = json.dumps(manifest, indent=2, ensure_ascii=False)
client.put_object(Bucket=AWS_BUCKET_NAME, Key=manifest_s3_path, Body=json_str)
```
* * *
#### **E. Construct Pipeline**
>This pipeline is designed to streamline the conversion, storage, and analysis of billing data.

Encapsulated the column renaming and CSV conversion logic in etl.py into a single function.

```python
def cenvert_focus(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    billing_list = data['billing']['getDemandCostListResponse']['demandCostList']
    ...
```

Import encapsulated functions(including test_api2.py) into the main Python script.

```python
import etl
import test_api2
...
```

The pipeline generates both raw data and the FOCUS-converted CSV in a single line of code using encapsulated functions.

```python
test_api2.rawdata(focus_startmonth,focus_endmonth,focus_startdate, focus_enddate)
etl.cenvert_focus('raw_ncp_data.json')
```

Upload both the converted dataset and raw data file to AWS S3.

```python
# raw data upload
json_s3_path = f"raw/{filenamemonth}/raw_ncp_data.json"
client.upload_file('raw_ncp_data.json',AWS_BUCKET_NAME,json_s3_path)

# processed data(FOCUS converted csv) upload
csv_s3_path = f"processed/{filenamemonth}/ncp_focus_format.csv"
client.upload_file('ncp_focus_format.csv',AWS_BUCKET_NAME,csv_s3_path)
```

The pipeline concludes by uploading manifest file to AWS S3.
* * *
#### **F. Test on Cloudability**
