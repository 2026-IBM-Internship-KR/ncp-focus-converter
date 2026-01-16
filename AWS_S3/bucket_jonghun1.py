import boto3

# AWS 버킷에 대한 정보를 출력합니다

AWS_ACCESS_KEY_ID = "AKIARGZ7KIP7MB4T7MZ6"
AWS_SECRET_ACCESS_KEY = "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"
AWS_DEFAULT_REGION = "ap-northeast-2"
AWS_BUCKET_NAME = "ncp-cost-data-jonghun1"
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

# response = client.list_buckets()

s3 = session.resource('s3')

for bucket in s3.buckets.all():
    print(bucket.name)

buckets = s3.Bucket(name=AWS_BUCKET_NAME)

for obj in buckets.objects.all():
    print(obj)
    print(obj.key)

    