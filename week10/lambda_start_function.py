# Week 10 - EC2 Automation
# lambda_start_function.py
# Lambda handler that starts EC2 instances tagged env = dev.

import json
import boto3

# Create an EC2 client
ec2 = boto3.client('ec2')


# Starts all EC2 instances (copied from automateEC2.py)
def Start_EC2():
    # Get all instances that have the tag env = dev
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:env',
                'Values': ['dev']
            }
        ]
    )

    # List to hold the instance IDs
    instance_ids = []

    # Loop through the response to get each instance
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            # Print the instance ID (shows up in the CloudWatch logs)
            print(instance['InstanceId'])
            # Add the instance ID to the list
            instance_ids.append(instance['InstanceId'])

    # Start all instances in the list
    ec2.start_instances(InstanceIds=instance_ids)
    print('Starting instances:', instance_ids)

    # Return the list of instance IDs
    return instance_ids


def lambda_handler(event, context):
    # TODO implement
    # Call Start_EC2 and get the list of started instances
    started_instances = Start_EC2()
    return {
        'statusCode': 200,
        'body': json.dumps(started_instances)
    }