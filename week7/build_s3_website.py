import boto3
import json
import argparse
import random
import string

from botocore.exceptions import ClientError

# Create S3 client
s3client = boto3.client('s3')

# Allow user to enter a bucket name with --sitename
parser = argparse.ArgumentParser()
parser.add_argument('--sitename', type=str)
args = parser.parse_args()

# Generate a random bucket name if --sitename is not provided
random_string = "".join(random.choices(string.ascii_lowercase, k=10))

if args.sitename:
    myBucketname = args.sitename
else:
    myBucketname = 'my-website-' + random_string

print("Using bucket name:", myBucketname)

try:
    # Create bucket
    s3client.create_bucket(Bucket=myBucketname)
    print("Bucket created successfully!")

    # Allow public access
    s3client.delete_public_access_block(Bucket=myBucketname)
    print("Public access block deleted successfully!")

    # Create bucket policy
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

    # Add bucket policy
    s3client.put_bucket_policy(
        Bucket=myBucketname,
        Policy=json.dumps(bucket_policy)
    )

    # Configure bucket as a website
    s3client.put_bucket_website(
        Bucket=myBucketname,
        WebsiteConfiguration={
            'ErrorDocument': {'Key': 'error.html'},
            'IndexDocument': {'Suffix': 'index.html'},
        }
    )
    print("Website configuration added successfully!")

    # Upload website files
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

# Handle bucket name that already exists
except s3client.exceptions.BucketAlreadyExists as err:
    print(
        "Bucket {} already exists!".format(
            err.response['Error']['BucketName']
        )
    )

# Handle other AWS client errors
except ClientError as err:
    error_code = err.response['Error']['Code']

    if error_code == 'InvalidToken':
        print("Invalid Token. Please update your AWS credentials file.")
    else:
        print(error_code)