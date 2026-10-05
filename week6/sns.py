import boto3


def CreateSNSTopic(topic_name):
    sns_client = boto3.client("sns")

    response = sns_client.create_topic(
        Name=topic_name
    )

    print(f"SNS topic created: {response['TopicArn']}")

    return response["TopicArn"]


def SubscribeEmail(arn, email):
    sns_client = boto3.client("sns")

    response = sns_client.subscribe(
        TopicArn=arn,
        Protocol="email",
        Endpoint=email
    )

    print("Email subscription created.")

    return response["SubscriptionArn"]