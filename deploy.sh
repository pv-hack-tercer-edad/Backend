#!/bin/bash
set -e

# Configuration
AWS_ACCOUNT_ID="145001347266"
AWS_REGION="us-east-2" # e.g., us-east-1
ECR_REPOSITORY_NAME="platanus-hack"
IMAGE_TAG="latest"
CLUSTER_NAME="platanus-hack-cluster"
SERVICE_NAME="hackathon-platanus-service"
TASK_DEFINITION_NAME="platanus-hack-task"

# Step 1: Authenticate Docker to AWS ECR
echo "Authenticating Docker with AWS ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

# Step 2: Build the Docker image
echo "Building the Docker image..."
docker build -t "${ECR_REPOSITORY_NAME}:${IMAGE_TAG}" .

# Step 3: Tag the Docker image
echo "Tagging the Docker image..."
docker tag "${ECR_REPOSITORY_NAME}:${IMAGE_TAG}" "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}:${IMAGE_TAG}"

# Step 4: Push the image to ECR
echo "Pushing the image to ECR..."
docker push "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}:${IMAGE_TAG}"

# Step 5: Update the ECS Task Definition
echo "Updating ECS Task Definition..."
NEW_TASK_DEFINITION=$(aws ecs register-task-definition \
    --cli-input-json file://task-definition.json \
    --query 'taskDefinition.taskDefinitionArn' --output text)

echo "New Task Definition ARN: $NEW_TASK_DEFINITION"

# Step 6: Update ECS Service with the New Task Definition
echo "Updating ECS Service..."
aws ecs update-service \
    --cluster $CLUSTER_NAME \
    --service $SERVICE_NAME \
    --task-definition $NEW_TASK_DEFINITION \
    --no-cli-pager

# Step 7: Wait for the service to stabilize
echo "Waiting for the service to stabilize..."
aws ecs wait services-stable \
    --cluster $CLUSTER_NAME \
    --services $SERVICE_NAME

echo "Deployment to ECS completed successfully!"
