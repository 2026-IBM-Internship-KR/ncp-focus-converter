import boto3
from bucket_jonghun1 import client,AWS_BUCKET_NAME

# 버킷에 있는 파일을 다운로드 합니다

client.download_file(AWS_BUCKET_NAME, 'tmp/2026.01.14.txt','download/a.txt')
