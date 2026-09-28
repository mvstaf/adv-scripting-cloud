import boto3
sts = boto3.client('sts')

hFile = open('creditial-check.txt','w')

result =sts.get_caller_identity()

print(str(result))

hFile.close(cre)
