# stopEC2.py - Lambda function that stops every running EC2 instance
import boto3  # AWS SDK for Python (built into the Lambda runtime)
import json   # Turns the response into JSON for the return body

region = 'us-east-1'
ec2 = boto3.client('ec2', region_name=region)  # EC2 client for us-east-1


def lambda_handler(event, context):
    # Find all instances that are currently running
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': [
                    'running',
                ]
            },
        ],
    )

    # Collect the instance IDs from every reservation
    listofinstanceids = []
    for reservation in response["Reservations"]:
        instances = reservation["Instances"]
        for instance in instances:
            print(instance["InstanceId"])
            listofinstanceids.append(instance["InstanceId"])

    # Stop them if there are any, otherwise report nothing to do
    stop_response = "Nothing needed to be stopped"
    if len(listofinstanceids) != 0:
        stop_response = ec2.stop_instances(InstanceIds=listofinstanceids, DryRun=False)
    print(stop_response)

    # Return a success code and the AWS response as JSON
    return {
        'statusCode': 200,
        'body': json.dumps(stop_response)
    }