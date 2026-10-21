import boto3
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "-s",
    "--security-group",
    help="Security group name"
)

args = parser.parse_args()

ec2 = boto3.client("ec2")

security_groups = ec2.describe_security_groups()

for security_group in security_groups["SecurityGroups"]:

    group_name = security_group["GroupName"]

    if args.security_group and group_name != args.security_group:
        continue

    print(f"\nSecurity Group: {group_name}")

    if len(security_group["IpPermissions"]) == 0:
        print("No inbound rules.")

    for rule in security_group["IpPermissions"]:

        from_port = rule.get("FromPort", "All")
        to_port = rule.get("ToPort", "All")

        for ip_range in rule.get("IpRanges", []):

            cidr = ip_range["CidrIp"]

            print(f"Range: {cidr}")
            print(f"Ports: {from_port}-{to_port}")

            if cidr == "0.0.0.0/0":
                print("WARNING: Open to the public internet!")