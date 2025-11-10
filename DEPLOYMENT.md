# Deployment Guide

This guide provides step-by-step instructions for deploying the Certificate Vault application to various cloud platforms.

## Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Docker Deployment](#docker-deployment)
3. [AWS Deployment](#aws-deployment)
4. [Google Cloud Platform Deployment](#google-cloud-platform-deployment)
5. [Azure Deployment](#azure-deployment)
6. [Environment Variables](#environment-variables)
7. [Blockchain Setup](#blockchain-setup)

## Local Development Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL (optional, SQLite for development)
- Ethereum node or Infura/Alchemy account

### Backend Setup

1. Navigate to backend directory:

```bash
cd backend
```

2. Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create `.env` file:

```bash
cp .env.example .env
```

5. Update `.env` with your configuration

6. Initialize database:

```bash
python ../scripts/init_db.py --init-db
```

7. Create issuer user:

```bash
python ../scripts/init_db.py --create-issuer --username admin --email admin@example.com --password admin123
```

8. Run backend:

```bash
python app.py
```

### Frontend Setup

1. Navigate to frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Create `.env` file:

```env
REACT_APP_API_URL=http://localhost:5000
```

4. Run frontend:

```bash
npm start
```

## Docker Deployment

### Prerequisites

- Docker
- Docker Compose

### Steps

1. Clone the repository:

```bash
git clone <repository-url>
cd certificate-vault
```

2. Create `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=postgresql://postgres:postgres@db:5432/certificates
ETHEREUM_RPC_URL=http://localhost:8545
CONTRACT_ADDRESS=your-contract-address
PRIVATE_KEY=your-private-key
ACCOUNT_ADDRESS=your-account-address
```

3. Build and start services:

```bash
docker-compose up -d
```

4. Initialize database:

```bash
docker-compose exec backend python ../scripts/init_db.py --init-db
```

5. Create issuer user:

```bash
docker-compose exec backend python ../scripts/init_db.py --create-issuer --username admin --email admin@example.com --password admin123
```

6. Access the application:

- Frontend: http://localhost
- Backend API: http://localhost:5000

## AWS Deployment

### Option 1: EC2 + RDS

1. **Launch EC2 Instance**:

   - Choose Ubuntu Server
   - Configure security groups (HTTP, HTTPS, SSH)
   - Launch instance

2. **Install Docker on EC2**:

```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
sudo apt-get update
sudo apt-get install docker.io docker-compose -y
sudo usermod -aG docker ubuntu
```

3. **Create RDS PostgreSQL Instance**:

   - Create RDS PostgreSQL instance
   - Note the endpoint and credentials
   - Configure security group to allow EC2 access

4. **Deploy Application**:

```bash
git clone <repository-url>
cd certificate-vault
# Update docker-compose.yml with RDS endpoint
docker-compose up -d
```

5. **Configure Environment Variables**:

```bash
# Update .env file with RDS connection string
DATABASE_URL=postgresql://user:password@rds-endpoint:5432/certificates
```

### Option 2: Elastic Beanstalk

1. **Install EB CLI**:

```bash
pip install awsebcli
```

2. **Initialize EB**:

```bash
eb init -p docker certificate-vault
```

3. **Create environment**:

```bash
eb create certificate-vault-env
```

4. **Configure environment variables**:

```bash
eb setenv SECRET_KEY=your-secret-key JWT_SECRET_KEY=your-jwt-secret-key
```

5. **Deploy**:

```bash
eb deploy
```

## Google Cloud Platform Deployment

### Option 1: Cloud Run

1. **Install gcloud CLI**:

```bash
# Follow instructions at https://cloud.google.com/sdk/docs/install
```

2. **Set project**:

```bash
gcloud config set project YOUR_PROJECT_ID
```

3. **Enable APIs**:

```bash
gcloud services enable run.googleapis.com
gcloud services enable sqladmin.googleapis.com
```

4. **Create Cloud SQL instance**:

```bash
gcloud sql instances create certificate-vault-db \
    --database-version=POSTGRES_15 \
    --tier=db-f1-micro \
    --region=us-central1
```

5. **Create database**:

```bash
gcloud sql databases create certificates --instance=certificate-vault-db
```

6. **Build and push images**:

```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/certificate-vault-backend
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/certificate-vault-frontend
```

7. **Deploy to Cloud Run**:

```bash
gcloud run deploy certificate-vault-backend \
    --image gcr.io/YOUR_PROJECT_ID/certificate-vault-backend \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

### Option 2: App Engine

1. **Create app.yaml**:

```yaml
runtime: python39
entrypoint: gunicorn -w 4 -b 0.0.0.0:8080 app:app

env_variables:
  DATABASE_URL: postgresql://user:password@/certificates?host=/cloudsql/PROJECT:REGION:INSTANCE
```

2. **Deploy**:

```bash
gcloud app deploy
```

## Azure Deployment

### Option 1: Container Instances

1. **Install Azure CLI**:

```bash
# Follow instructions at https://docs.microsoft.com/cli/azure/install-azure-cli
```

2. **Login to Azure**:

```bash
az login
```

3. **Create resource group**:

```bash
az group create --name certificate-vault-rg --location eastus
```

4. **Create Azure Container Registry**:

```bash
az acr create --resource-group certificate-vault-rg --name certificatevault --sku Basic
```

5. **Build and push images**:

```bash
az acr build --registry certificatevault --image certificate-vault-backend:latest .
az acr build --registry certificatevault --image certificate-vault-frontend:latest .
```

6. **Create Azure Database for PostgreSQL**:

```bash
az postgres server create \
    --resource-group certificate-vault-rg \
    --name certificate-vault-db \
    --location eastus \
    --admin-user adminuser \
    --admin-password YourPassword123! \
    --sku-name B_Gen5_1
```

7. **Create container instances**:

```bash
az container create \
    --resource-group certificate-vault-rg \
    --name certificate-vault-backend \
    --image certificatevault.azurecr.io/certificate-vault-backend:latest \
    --registry-login-server certificatevault.azurecr.io \
    --registry-username certificatevault \
    --registry-password YOUR_ACR_PASSWORD \
    --dns-name-label certificate-vault-backend \
    --ports 5000
```

### Option 2: App Service

1. **Create App Service Plan**:

```bash
az appservice plan create --name certificate-vault-plan --resource-group certificate-vault-rg --sku B1 --is-linux
```

2. **Create Web App**:

```bash
az webapp create --resource-group certificate-vault-rg --plan certificate-vault-plan --name certificate-vault-backend --deployment-container-image-name certificatevault.azurecr.io/certificate-vault-backend:latest
```

## Environment Variables

### Backend Environment Variables

```env
# Flask Configuration
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production

# Database Configuration
DATABASE_URL=postgresql://user:password@host:5432/certificates

# Blockchain Configuration
ETHEREUM_RPC_URL=https://goerli.infura.io/v3/YOUR_INFURA_PROJECT_ID
CONTRACT_ADDRESS=0x...
PRIVATE_KEY=your-private-key-for-transactions
ACCOUNT_ADDRESS=your-account-address

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### Frontend Environment Variables

```env
REACT_APP_API_URL=http://localhost:5000
```

## Blockchain Setup

### Option 1: Local Development (Ganache)

1. **Install Ganache**:

```bash
npm install -g ganache-cli
```

2. **Start Ganache**:

```bash
ganache-cli
```

3. **Update .env**:

```env
ETHEREUM_RPC_URL=http://localhost:8545
```

4. **Deploy Contract**:

```bash
python scripts/deploy_contract.py
```

### Option 2: Testnet (Goerli/Sepolia)

1. **Get Infura/Alchemy Account**:

   - Sign up at https://infura.io or https://alchemy.com
   - Create a new project
   - Get the RPC URL

2. **Get Test ETH**:

   - Use a faucet: https://goerlifaucet.com
   - Fund your account

3. **Update .env**:

```env
ETHEREUM_RPC_URL=https://goerli.infura.io/v3/YOUR_PROJECT_ID
```

4. **Deploy Contract**:

```bash
python scripts/deploy_contract.py
```

### Option 3: Mainnet

1. **Get Mainnet RPC URL**:

   - Use Infura/Alchemy mainnet endpoint
   - Ensure you have sufficient ETH for gas

2. **Update .env**:

```env
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/YOUR_PROJECT_ID
```

3. **Deploy Contract**:

```bash
python scripts/deploy_contract.py
```

## Security Checklist

- [ ] Change all default secrets and keys
- [ ] Use strong passwords for database
- [ ] Enable SSL/TLS for database connections
- [ ] Configure CORS properly
- [ ] Use environment variables for sensitive data
- [ ] Enable firewall rules
- [ ] Regular security updates
- [ ] Backup database regularly
- [ ] Monitor logs for suspicious activity
- [ ] Use HTTPS in production

## Troubleshooting

### Database Connection Issues

- Check database credentials
- Verify network connectivity
- Check firewall rules
- Verify database is running

### Blockchain Connection Issues

- Verify RPC URL is correct
- Check network connectivity
- Verify contract address is set
- Check account has sufficient funds (for transactions)

### Docker Issues

- Check Docker is running
- Verify docker-compose.yml configuration
- Check container logs: `docker-compose logs`
- Verify environment variables are set

## Support

For deployment issues, please check:

1. Application logs
2. Container logs
3. Cloud provider logs
4. GitHub Issues
