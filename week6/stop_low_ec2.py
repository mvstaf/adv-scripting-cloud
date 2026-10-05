import boto3
import ec2
import sns


# Get AWS account ID
sts_client = boto3.client("sts")
account_id = sts_client.get_caller_identity()["Account"]


# Get latest Amazon Linux 2 AMI
image_id = ec2.get_latest_amazon_linux_2_ami()
print(f"Image ID: {image_id}")


# Create EC2 instance using the function from ec2.py
instance = ec2.create_ec2_instance(image_id)

# Get the actual instance ID
instance_id = instance.id
print(f"Instance ID: {instance_id}")


# Create SNS topic
topic_arn = sns.CreateSNSTopic("MustafTopic")

# Subscribe your email
sns.SubscribeEmail(
    topic_arn,
    "mhussein@madisoncollege.edu"
)


# Create CloudWatch client
cw_client = boto3.client("cloudwatch")


# Create low CPU CloudWatch alarm
cw_client.put_metric_alarm(
    AlarmName="Web_Server_LOW_CPU_Utilization",
    ComparisonOperator="LessThanOrEqualToThreshold",
    EvaluationPeriods=1,
    MetricName="CPUUtilization",
    Namespace="AWS/EC2",
    Period=300,
    Statistic="Average",
    Threshold=10.0,
    ActionsEnabled=True,
    AlarmActions=[
        f"arn:aws:swf:us-east-1:{account_id}:action/actions/AWS_EC2.InstanceId.Stop/1.0",
        topic_arn
    ],
    AlarmDescription="Alarm when server CPU is lower than 10%",
    Dimensions=[
        {
            "Name": "InstanceId",
            "Value": instance_id
        }
    ]
)

print("CloudWatch low CPU alarm created successfully.")
print("Check your email and confirm the SNS subscription.")