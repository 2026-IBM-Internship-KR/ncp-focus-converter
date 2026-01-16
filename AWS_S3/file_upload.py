import boto3
from bucket_jonghun1 import client,AWS_BUCKET_NAME
from datetime import datetime
import uuid

# 버킷에 파일을 업로드 합니다

client.upload_file('download/a.txt',AWS_BUCKET_NAME,'manifests/2024-01/a.txt')

csv_path = "processed/2026-01/ncp_focus_format.csv"

# Msnifest.json 파일 생성 및 업로드 (제작중)
manifest = {
    "compression":"gzip",
    "content_Type":"CSV",
    "report_id":str(uuid.uuid4()),
    "root_dir":AWS_BUCKET_NAME,
    "all_report_keys":csv_path,
    "updated_at":datetime.utcnow().isoformat()+"Z",
    "focus_version":"1.0"
}
