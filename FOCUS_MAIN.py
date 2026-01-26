import time
import hmac
import hashlib
import base64
import requests
import json
from typing import Dict, Any
import test_api2
import pandas as pd
import etl
import boto3
from datetime import datetime
import uuid

# 변수 입력
AWS_ACCESS_KEY_ID = "AKIARGZ7KIP7MB4T7MZ6"
AWS_SECRET_ACCESS_KEY = "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"
AWS_DEFAULT_REGION = "ap-northeast-2"
AWS_BUCKET_NAME = "ncp-cost-data-jonghun1"
focus_startmonth = "202601"
focus_endmonth = "202601"
focus_startdate = "20260101"
focus_enddate = "20260122"

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


# test_api2.rawdata("202601","202601","20260101","20260119")

# rawdata 파일 생성
test_api2.rawdata(focus_startmonth,focus_endmonth,focus_startdate, focus_enddate)

# focus 포맷으로 변환
etl.cenvert_focus('raw_ncp_data.json')


filenamemonth = focus_startmonth[:4] + '-' + focus_startmonth[4:]

# raw data 파일 업로드
json_s3_path = f"raw/{filenamemonth}/raw_ncp_data.json"
client.upload_file('raw_ncp_data.json',AWS_BUCKET_NAME,json_s3_path)

# processed data 파일 업로드
csv_s3_path = f"processed/{filenamemonth}/ncp_focus_format.csv"
client.upload_file('ncp_focus_format.csv',AWS_BUCKET_NAME,csv_s3_path)

# Msnifest.json 파일 생성 및 업로드
manifest = {
    "compression":"gzip",
    "content_Type":"CSV",
    "report_id":str(uuid.uuid4()),
    "root_dir":AWS_BUCKET_NAME,
    "all_report_keys":[csv_s3_path],
    "updated_at":datetime.utcnow().isoformat()+"Z",
    "focus_version":"1.0"
}

# manifest 파일 업로드
manifest_s3_path = f"manifests/{filenamemonth}/Manifest.json"
json_str = json.dumps(manifest, indent=2, ensure_ascii=False)
client.put_object(Bucket=AWS_BUCKET_NAME, Key=manifest_s3_path, Body=json_str)
