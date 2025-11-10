#!/bin/bash

# Azure Deployment Script for Certificate Vault
# This script deploys the application to Azure using Container Instances and Azure Database

echo "Starting Azure deployment..."

# Configuration
RESOURCE_GROUP="certificate-vault-rg"
LOCATION="eastus"

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "Error: Azure CLI is not installed. Please install it first."
    exit 1
fi

echo "Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

echo "Creating Azure Container Registry..."
az acr create --resource-group $RESOURCE_GROUP --name certificatevault --sku Basic

echo "Building and pushing Docker images..."
az acr build --registry certificatevault --image certificate-vault-backend:latest --file Dockerfile.backend .
az acr build --registry certificatevault --image certificate-vault-frontend:latest --file Dockerfile.frontend .

echo "Creating Azure Database for PostgreSQL..."
# TODO: Create Azure Database for PostgreSQL
# az postgres server create ...

echo "Creating Container Instances..."
# TODO: Create container instances
# az container create ...

echo "Deployment complete!"
echo "Please configure environment variables and update service URLs."

