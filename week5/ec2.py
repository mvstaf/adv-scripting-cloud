import boto3

def get_latest_amazon_linux_2_ami():
    client = boto3.client('ec2')
    filters = [
        {
            'Name': 'description',
            'Values': ['Amazon Linux 2 AMI*']
        },
        {
            'Name': 'architecture',
            'Values': ['x86_64']
        },
        {
            'Name': 'owner-alias',
            'Values': ['amazon']
        }
    ]

    image_data = client.describe_images(Filters=filters)
    images = sorted(
        image_data['Images'],
        key=lambda image: image['CreationDate'],
        reverse=True
    )
    return images[0]['ImageId']

def create_ec2_instance(image_id):
    ec2 = boto3.resource('ec2')
    instance = ec2.create_instances(
        ImageId=image_id,
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=1,
        DryRun=False
    )
    print(f"EC2 instance created successfully with ID: {instance[0].id}")
    return instance[0]

def print_instance_details(instance):
    print(f"Instance ID: {instance.id}")
    print(f"State: {instance.state['Name']}")
    print(f"Public IP: {instance.public_ip_address}")
    print(f"Public DNS: {instance.public_dns_name}")
    print(f"Launch Time: {instance.launch_time}")
    print(f"Tags before update: {instance.tags}")


def main():
    image_id = get_latest_amazon_linux_2_ami()
    print(f"Latest Amazon Linux 2 AMI ID retrieved successfully.")
    print(f"ImageID: {image_id}")

    instance = create_ec2_instance(image_id)
    instance.wait_until_running()
    instance.reload()

    print_instance_details(instance)
    instance.create_tags(
        Tags=[
            {
                'Key': 'Name',
                'Value': 'Mustaf'
            }
        ]
    )
    instance.reload()
    print(f"Updated tags: {instance.tags}")

    # instance.terminate()
    # print(f"EC2 instance with ID: {instance.id} has been terminated.")
    
if __name__ == "__main__":
    main()
    