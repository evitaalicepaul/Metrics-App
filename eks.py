from kubernetes import client, config
from kubernetes.client.exceptions import ApiException

# Load Kubernetes configuration
config.load_kube_config()

# Create a Kubernetes API client
api_client = client.ApiClient()

# Define the deployment
deployment = client.V1Deployment(
    metadata=client.V1ObjectMeta(name="my-flask-app"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={"app": "my-flask-app"}
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app": "my-flask-app"}
            ),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="my-flask-container",
                        image="923777007287.dkr.ecr.us-east-1.amazonaws.com/my-ecr-repo:latest",
                        ports=[client.V1ContainerPort(container_port=5001)]
                    )
                ]
            )
        )
    )
)

# Create the deployment
api_instance = client.AppsV1Api(api_client)
try:
    api_instance.create_namespaced_deployment(
        namespace="default",
        body=deployment
    )
    print("Deployment created.")
except ApiException as e:
    if e.status == 409:  # Conflict
        print("Deployment already exists. Skipping...")
    else:
        raise

# Define the service
service = client.V1Service(
    metadata=client.V1ObjectMeta(name="my-flask-service"),
    spec=client.V1ServiceSpec(
        selector={"app": "my-flask-app"},
        ports=[client.V1ServicePort(port=5000)]
    )
)

# Create the service
api_instance = client.CoreV1Api(api_client)
try:
    api_instance.create_namespaced_service(
        namespace="default",
        body=service
    )
    print("Service created.")
except ApiException as e:
    if e.status == 409:  # Conflict
        print("Service already exists. Skipping...")
    else:
        raise