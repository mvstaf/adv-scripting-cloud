"""
s3enforce.py - Week 9 Activity: Use Boto3 to Enforce S3 Object Versioning

Helper functions that create, delete, version, and set the policy on S3
buckets. trail.py imports this file to reuse CreateBucket() and
SetBucketPolicy(), and EnforceVersioning() is copied into the Lambda
function so new buckets get versioning turned on automatically.
"""

import boto3
from botocore.exceptions import ClientError


def CreateBucket(bucket_name):
    """Create a new S3 bucket with the given name."""
    # Create an S3 client. The client is the low-level boto3 object that
    # makes S3 API calls using the credentials in ~/.aws/credentials.
    s3 = boto3.client('s3')

    # us-east-1 (the lab region) does NOT accept a LocationConstraint,
    # but every other region requires one, so check which region we're in.
    region = s3.meta.region_name

    try:
        if region == 'us-east-1':
            response = s3.create_bucket(Bucket=bucket_name)
        else:
            response = s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region},
            )
        print(f"Created bucket: {bucket_name}")
        return response
    except ClientError as error:
        code = error.response['Error']['Code']
        # If the script is re-run, the bucket may already be ours.
        # That's fine, so report it and keep going instead of crashing.
        if code == 'BucketAlreadyOwnedByYou':
            print(f"Bucket {bucket_name} already exists in your account, continuing.")
            return None
        # Bucket names are global across ALL AWS accounts, so another
        # account may already own this name.
        if code == 'BucketAlreadyExists':
            print(f"The name {bucket_name} is taken by another account. Pick a different name.")
        raise


def DeleteBucket(bucket_name):
    """Delete an S3 bucket. S3 only lets you delete a bucket that is empty."""
    # Create an S3 client
    s3 = boto3.client('s3')

    # delete_bucket removes the bucket itself (it fails if objects remain)
    response = s3.delete_bucket(Bucket=bucket_name)
    print(f"Deleted bucket: {bucket_name}")
    return response


def EnforceVersioning(bucket_name):
    """Turn on object versioning for the given bucket."""
    # Create an S3 client
    s3 = boto3.client('s3')

    # put_bucket_versioning sets the bucket's versioning state.
    # Status 'Enabled' makes S3 keep every version of an object, so files
    # that are overwritten or deleted can be recovered.
    # MFADelete stays 'Disabled' so deletes don't require an MFA device.
    response = s3.put_bucket_versioning(
        Bucket=bucket_name,
        VersioningConfiguration={
            'MFADelete': 'Disabled',
            'Status': 'Enabled',
        },
    )
    print(f"Versioning enabled on bucket: {bucket_name}")
    return response


def SetBucketPolicy(bucket_name, policy):
    """Attach a bucket policy (passed in as a JSON string) to the bucket."""
    # Create an S3 client
    s3 = boto3.client('s3')

    # put_bucket_policy replaces the bucket's resource policy. trail.py uses
    # this to let the CloudTrail service write its log files into the bucket.
    response = s3.put_bucket_policy(Bucket=bucket_name, Policy=policy)
    print(f"Bucket policy applied to: {bucket_name}")
    return response


def main():
    # Bucket names must be globally unique, lowercase, and 3-63 characters
    bucket_name = 'mustafh-week9-versioning-test'

    # Create the bucket, then turn versioning on
    CreateBucket(bucket_name)
    EnforceVersioning(bucket_name)

    # Read the setting back from S3 to prove versioning is really on
    s3 = boto3.client('s3')
    status = s3.get_bucket_versioning(Bucket=bucket_name).get('Status')
    print(f"Versioning status for {bucket_name}: {status}")


# Only run main() when this file is run directly. When trail.py does
# "import s3enforce", this block is skipped so no extra bucket gets created.
if __name__ == '__main__':
    main()