import boto3
import json

s3client = boto3.client('s3')

myBucketname = 'my-unique-bucket-name-mustaffall26'

s3client.create_bucket(Bucket=myBucketname)
print("Bucket created successfully!")

s3client.delete_public_access_block(Bucket=myBucketname)
print("Public access block deleted successfully!")

bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AddPerm",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::%s/*" % myBucketname
        }
    ]
}

s3client.put_bucket_policy(
    Bucket=myBucketname,
    Policy=json.dumps(bucket_policy)
)

s3client.put_bucket_website(
    Bucket=myBucketname,
    WebsiteConfiguration={
        'ErrorDocument': {'Key': 'error.html'},
        'IndexDocument': {'Suffix': 'index.html'},
    }
)
print("Website configuration added successfully!")

files = ['index.html', 'error.html']

for file in files:
    with open(file, 'rb') as hFile:
        s3client.put_object(
            Body=hFile,
            Bucket=myBucketname,
            Key=file,
            ContentType='text/html'
        )
print("Website created successfully!")