# Week 10 - EC2 Automation
# automateEC2.py
# Uses the boto3 EC2 client to stop and start EC2 instances.

# Import boto3
import boto3

# Create an EC2 client
ec2 = boto3.client('ec2')


# Stops all EC2 instances
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
    # (the response has Reservations, and each Reservation has Instances)
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            # Print the instance ID to see what we have
            print(instance['InstanceId'])
            # Add the instance ID to the list
            instance_ids.append(instance['InstanceId'])

    # Stop all instances in the list
    ec2.stop_instances(InstanceIds=instance_ids)
    print('Stopping instances:', instance_ids)

    # Return the list of instance IDs
    return instance_ids


# Starts all EC2 instances
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
            # Print the instance ID to see what we have
            print(instance['InstanceId'])
            # Add the instance ID to the list
            instance_ids.append(instance['InstanceId'])

    # Start all instances in the list
    ec2.start_instances(InstanceIds=instance_ids)
    print('Starting instances:', instance_ids)

    # Return the list of instance IDs
    return instance_ids


# Main function
def main():
    # Stop the instances
    Stop_EC2()
    # Start the instances
    Start_EC2()


# Main code - only runs main() when this script is run directly
if __name__ == '__main__':
    main()