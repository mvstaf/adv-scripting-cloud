import boto3
import csv

def Get_instances(filter_name=None, filter_value=None):
    """
    Creates an EC2 client, uses a Boto3 paginator to fetch
    all instances across pages, and applies optional filters
    (Name and Value) if provided.
    """
    ec2_client = boto3.client('ec2')
    paginator = ec2_client.get_paginator('describe_instances')
    filters = []
    if filter_name and filter_value:
        filters.append({'Name': filter_name,
                        'Values': [filter_value]
        })
    page_iterator = paginator.paginate(Filters=filters) if filters else paginator.paginate()
    response_instances = []

    for page in page_iterator:
        for reservation in page['Reservations']:
            for instance in reservation['Instances']:
                response_instances.append(instance)
    return response_instances

def CSV_Writer(header, content):
    """
    Takes a header list and content (list of dictionaries) and writes them to export.csv using Python's csv.DictWriter module.
    """
    with open('export.csv', mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for row in content:
            writer.writerow(row)

def main():
    print("Fetching EC2 instances from AWS...")
    instances = Get_instances("instance-type", "t2.micro")

    header = ["InstanceId", "InstanceType", "State", "PublicIpAddress", "MonitoringState", "InstanceName"]
    content = []
    for instance in instances:

        instance_name = "N/A"

        if "Tags" in instance:
            for tag in instance["Tags"]:
                if tag["Key"] == "Name":
                    instance_name = tag["Value"]

        row = {
            "InstanceId": instance["InstanceId"],
            "InstanceType": instance["InstanceType"],
            "State": instance["State"]["Name"],
            "PublicIpAddress": instance.get("PublicIpAddress", "N/A"),
            "MonitoringState": instance["Monitoring"]["State"],
            "InstanceName": instance_name
        }

        content.append(row)
        print(row) 

    CSV_Writer(header, content)

if __name__ == "__main__":
    main()  