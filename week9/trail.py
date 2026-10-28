"""
trail.py - Week 9 Activity: Enable CloudTrail to log API calls

Creates an S3 bucket for CloudTrail logs, gives the CloudTrail service
permission to write to it, then creates a trail and starts logging.
Once the trail is logging, S3 API calls like CreateBucket are recorded and
sent to EventBridge (CloudWatch Events), which is what triggers our Lambda.
"""

import json

import boto3

# Reuse the bucket functions we already wrote in s3enforce.py
import s3enforce


def CreateTrail(trail_name, bucket_name):
    """Create a CloudTrail trail that writes to bucket_name and start logging."""
    # Create a CloudTrail client to make CloudTrail API calls
    cloudtrail = boto3.client('cloudtrail')

    response = None
    try:
        # create_trail sets up the trail and points it at our log bucket.
        # This fails if the bucket policy doesn't let CloudTrail write to it,
        # which is why SetBucketPolicy() runs before this in main().
        response = cloudtrail.create_trail(Name=trail_name, S3BucketName=bucket_name)
        print(f"Created trail: {trail_name}")
    except cloudtrail.exceptions.TrailAlreadyExistsException:
        # If the script is re-run, the trail is already there. Catch the
        # error and continue so we still make sure logging is started.
        print(f"Trail {trail_name} already exists, continuing.")

    # A new trail does NOT record anything until logging is started
    cloudtrail.start_logging(Name=trail_name)
    print(f"Logging started for trail: {trail_name}")

    return response


def main():
    # Use STS (Security Token Service) to look up our AWS account ID
    # (same approach as week 5's stop_low_ec2.py). The ID is needed in the
    # bucket policy and makes the bucket name unique.
    sts = boto3.client('sts')
    account_id = sts.get_caller_identity()['Account']
    print(f"Account ID: {account_id}")

    bucket_name = f"mustafh-week9-trail-logs-{account_id}"
    trail_name = 'CloudTrail'

    # Create the bucket that CloudTrail will deliver its log files to
    s3enforce.CreateBucket(bucket_name)

    # Bucket policy that lets the CloudTrail service:
    #   1. read the bucket's ACL (CloudTrail checks this before writing)
    #   2. write log files under AWSLogs/<account_id>/ in the bucket,
    #      with the bucket owner getting full control of each file
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AWSCloudTrailAclCheck20150319",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "s3:GetBucketAcl",
                "Resource": f"arn:aws:s3:::{bucket_name}"
            },
            {
                "Sid": "AWSCloudTrailWrite20150319",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "s3:PutObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/AWSLogs/{account_id}/*",
                "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}
            }
        ]
    }

    # put_bucket_policy expects a string, so convert the dictionary to JSON
    policy_string = json.dumps(policy)

    # Attach the policy to the log bucket
    s3enforce.SetBucketPolicy(bucket_name, policy_string)

    # Create the trail and start logging API calls
    CreateTrail(trail_name, bucket_name)


if __name__ == '__main__':
    main()