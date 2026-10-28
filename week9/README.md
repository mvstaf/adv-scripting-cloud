# Week 9 - Lambda: Enforce S3 Versioning

Uses boto3, CloudTrail, EventBridge, and Lambda to automatically enable
versioning on any newly created S3 bucket.

## Setup
uv init week9
cd week9
uv add boto3

## Run
uv run s3enforce.py
uv run trail.py

## Files
- s3enforce.py - create/delete buckets, enforce versioning, set bucket policy
- trail.py - create CloudTrail log bucket + policy, create trail, start logging
- automateLambda.txt - boto3 methods/parameters to automate creating a Lambda
- lambdaTestResult.jpg, lambdaCode.jpg, lambdaTriggerMetrics.jpg - screenshots