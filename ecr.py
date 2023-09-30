import boto3

# Create an ECR client
ecr_client = boto3.client('ecr')

ecr_client = boto3.client('ecr', region_name='us-east-1')

print(boto3.Session().region_name)


# Create a new ECR repository
repository_name = 'my-ecr-repo'
response = ecr_client.create_repository(repositoryName=repository_name)

# Print the repository URI
repository_uri = response['repository']['repositoryUri']
print(repository_uri)