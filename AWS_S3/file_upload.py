import boto3
from bucket_jonghun1 import client,AWS_BUCKET_NAME
from datetime import datetime
import uuid
import json

# 버킷에 파일을 업로드 합니다
# 샘플 코드
# client.upload_file('download/a.txt',AWS_BUCKET_NAME,'manifests/2024-01/a.txt')

# processed data 파일 업로드
csv_s3_path = "processed/2026-01/ncp_focus_format.csv"
# client.upload_file('file_name',AWS_BUCKET_NAME,csv_s3_path)

# Msnifest.json 파일 생성 및 업로드 (제작중)
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
manifest_s3_path = "manifests/2026-01/cost-Manifest.json"
json_str = json.dumps(manifest, indent=2, ensure_ascii=False)
client.put_object(Bucket=AWS_BUCKET_NAME, Key=manifest_s3_path, Body=json_str)