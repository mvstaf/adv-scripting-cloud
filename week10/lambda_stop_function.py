# Week 10 - EC2 Automation
# lambda_stop_function.py
# Lambda handler that stops EC2 instances tagged env = dev.

import json
import boto3

# Create an EC2 client
ec2 = boto3.client('ec2')


# Stops all EC2 instances (copied from automateEC2.py)
def Stop_EC2():
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

    # Stop all instances in the list
    ec2.stop_instances(InstanceIds=instance_ids)
    print('Stopping instances:', instance_ids)

    # Return the list of instance IDs
    return instance_ids


def lambda_handler(event, context):
    # TODO implement
    # Call Stop_EC2 and get the list of stopped instances
    stopped_instances = Stop_EC2()
    return {
        'statusCode': 200,
        'body': json.dumps(stopped_instances)
    }