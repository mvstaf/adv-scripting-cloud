# Week 10 - EC2 Automation
# lambda_start.py
# Creates the StartEC2 Lambda function and invokes it.

# Import boto3
import boto3

# Create an IAM client and a Lambda client
iam_client = boto3.client('iam')
lambda_client = boto3.client('lambda')


# Creates a new Lambda function with the given name
def Create_Lambda(function_name):
    # Get the LabRole role
    role_response = iam_client.get_role(RoleName='LabRole')

    # Open the zip file for read ('rb' reads it in as bytes)
    with open('lambda_start_function.zip', 'rb') as file_data:
        # Read the zip file into a string
        zipped_code = file_data.read()

    # Create the Lambda function
    response = lambda_client.create_function(
        FunctionName=function_name,
        Timeout=15,
        Role=role_response['Role']['Arn'],
        Publish=True,
        PackageType='Zip',
        Runtime='python3.9',
        Code={
            'ZipFile': zipped_code
        },
        Handler='lambda_start_function.lambda_handler'
    )
    print('Created Lambda function:', response['FunctionName'])


# Invokes (runs) the Lambda function with the given name
def Invoke_Lambda(function_name):
    response = lambda_client.invoke(FunctionName=function_name)
    # The function's return value comes back in the Payload
    print(response['Payload'].read().decode())


# Main function
def main():
    function_name = 'StartEC2'

    # Get the list of Lambda functions
    response = lambda_client.list_functions()

    # Check if the function name already exists
    exists = False
    for function in response['Functions']:
        if function['FunctionName'] == function_name:
            exists = True

    # If it doesn't exist, create it
    if not exists:
        Create_Lambda(function_name)
    else:
        print(function_name, 'already exists')

    # Invoke the Lambda function
    Invoke_Lambda(function_name)


# Only runs main() when this script is run directly
if __name__ == '__main__':
    main()