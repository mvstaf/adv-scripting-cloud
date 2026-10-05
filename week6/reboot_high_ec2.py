import boto3
import ec2
import sns


# Get AWS account ID
sts_client = boto3.client("sts")
account_id = sts_client.get_caller_identity()["Account"]


# Get latest Amazon Linux 2 AMI
image_id = ec2.get_latest_amazon_linux_2_ami()
print(f"Image ID: {image_id}")


# Create EC2 web server
instance = ec2.create_ec2_instance(image_id)

instance_id = instance.id
print(f"Instance ID: {instance_id}")


# Create SNS topic
topic_arn = sns.CreateSNSTopic("MustafTopic")

# Subscribe email
sns.SubscribeEmail(
    topic_arn,
    "mhussein@madisoncollege.edu"
)


# Create CloudWatch client
cw_client = boto3.client("cloudwatch")


# Create HIGH CPU alarm
cw_client.put_metric_alarm(
    AlarmName="Web_Server_HIGH_CPU_Utilization",
    ComparisonOperator="GreaterThanOrEqualToThreshold",
    EvaluationPeriods=2,
    MetricName="CPUUtilization",
    Namespace="AWS/EC2",
    Period=300,
    Statistic="Average",
    Threshold=70.0,
    ActionsEnabled=True,
    AlarmActions=[
        f"arn:aws:swf:us-east-1:{account_id}:action/actions/AWS_EC2.InstanceId.Reboot/1.0",
        topic_arn
    ],
    AlarmDescription="Alarm when server CPU is higher than 70%",
    Dimensions=[
        {
            "Name": "InstanceId",
            "Value": instance_id
        }
    ]
)

print("High CPU CloudWatch alarm created successfully.")
print("Wait for the EC2 instance to pass 2/2 checks.")