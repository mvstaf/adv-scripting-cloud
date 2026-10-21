import boto3
import datetime
import pytz

# Create the IAM client
iam = boto3.client("iam")

# Get the IAM roles
roles = iam.list_roles()

# Loop through all roles
for role in roles["Roles"]:

    # Only show roles created in the last 90 days
    if role["CreateDate"] > (
        pytz.utc.localize(datetime.datetime.utcnow())
        - datetime.timedelta(days=90)
    ):

        role_name = role["RoleName"]

        # Print the role name and creation date
        print(f"\nRole: {role_name}")
        print(f"Created: {role['CreateDate']}")

        # Get managed policies attached to the role
        try:
            managed_policies = iam.list_attached_role_policies(
                RoleName=role_name
            )

            for policy in managed_policies["AttachedPolicies"]:
                print(f"Managed Policy: {policy['PolicyName']}")

        except Exception:
            print("Unable to view managed policies.")

        # Get inline policies attached to the role
        try:
            inline_policies = iam.list_role_policies(
                RoleName=role_name
            )

            for policy in inline_policies["PolicyNames"]:
                print(f"Inline Policy: {policy}")

        except Exception:
            print("Unable to view inline policies.")