import boto3

# This script checks whether CloudTrail trails exist
# for auditing activity in the AWS account.

# Create CloudTrail client
cloudtrail = boto3.client("cloudtrail")

try:
    # Get CloudTrail trails
    trails = cloudtrail.describe_trails()["trailList"]

    if len(trails) == 0:
        print("No CloudTrail trails found.")

    # Loop through each trail
    for trail in trails:
        print(f"\nTrail: {trail['Name']}")

except Exception:
    print("Unable to view CloudTrail trails.")