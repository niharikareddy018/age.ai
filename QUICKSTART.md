# Quick Start Guide

This guide will help you get the Certificate Vault up and running quickly.

## Prerequisites

- Python 3.8+
- Node.js 16+
- Docker (optional, for containerized deployment)
- Ethereum node or Infura/Alchemy account (for blockchain features)

## Quick Start with Docker

The fastest way to get started is using Docker Compose:

1. **Clone the repository**:

```bash
git clone <repository-url>
cd certificate-vault
```

2. **Create environment file**:

```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your configuration
```

3. **Start services**:

```bash
docker-compose up -d
```

4. **Initialize database**:

```bash
docker-compose exec backend python ../scripts/init_db.py --init-db
docker-compose exec backend python ../scripts/init_db.py --create-issuer --username admin --email admin@example.com --password admin123
```

5. **Access the application**:
   - Frontend: http://localhost
   - Backend API: http://localhost:5000

## Quick Start (Local Development)

### Backend Setup

1. **Navigate to backend**:

```bash
cd backend
```

2. **Create virtual environment**:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Create .env file**:

```bash
# Copy .env.example to .env and update values
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=sqlite:///certificates.db
ETHEREUM_RPC_URL=http://localhost:8545
```

5. **Initialize database**:

```bash
python ../scripts/init_db.py --init-db
python ../scripts/init_db.py --create-issuer --username admin --email admin@example.com --password admin123
```

6. **Run backend**:

```bash
python app.py
```

### Frontend Setup

1. **Navigate to frontend**:

```bash
cd frontend
```

2. **Install dependencies**:

```bash
npm install
```

3. **Create .env file**:

```env
REACT_APP_API_URL=http://localhost:5000
```

4. **Run frontend**:

```bash
npm start
```

## First Steps

1. **Register an Account**:

   - Go to http://localhost:3000 (or http://localhost if using Docker)
   - Click "Register"
   - Choose "Issuer" role
   - Create your account

2. **Login**:

   - Use your credentials to login
   - You'll be redirected to the dashboard

3. **Issue a Certificate** (Issuer only):

   - Click "Issue Certificate"
   - Select a user (or register a user first)
   - Fill in certificate details
   - Click "Issue Certificate"
   - The certificate will be stored on the blockchain

4. **Verify a Certificate**:
   - Go to "Verify" page
   - Enter Certificate ID or Hash
   - Click "Verify Certificate"
   - View verification results

## Blockchain Setup (Optional)

For full functionality, you need to set up blockchain:

### Option 1: Local Ganache

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

5. **Update .env with contract address**:

```env
CONTRACT_ADDRESS=0x...
```

### Option 2: Testnet (Goerli)

1. **Get Infura account**:

   - Sign up at https://infura.io
   - Create a new project
   - Get the RPC URL

2. **Get test ETH**:

   - Use a faucet: https://goerlifaucet.com
   - Fund your account

3. **Update .env**:

```env
ETHEREUM_RPC_URL=https://goerli.infura.io/v3/YOUR_PROJECT_ID
PRIVATE_KEY=your-private-key
ACCOUNT_ADDRESS=your-account-address
```

4. **Deploy Contract**:

```bash
python scripts/deploy_contract.py
```

5. **Update .env with contract address**:

```env
CONTRACT_ADDRESS=0x...
```

## Troubleshooting

### Backend won't start

- Check if port 5000 is available
- Verify database connection in .env
- Check Python version (3.8+)

### Frontend won't start

- Check if port 3000 is available
- Verify Node.js version (16+)
- Check REACT_APP_API_URL in .env

### Database errors

- Verify DATABASE_URL in .env
- Run database initialization script
- Check database permissions

### Blockchain errors

- Verify ETHEREUM_RPC_URL is correct
- Check if contract is deployed
- Verify CONTRACT_ADDRESS is set
- Check account has sufficient funds (for transactions)

## Next Steps

- Read the [README.md](README.md) for detailed documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for cloud deployment instructions
- Explore the API endpoints in the backend code
- Customize the frontend UI

## Support

For issues and questions:

- Check the troubleshooting section
- Review application logs
- Open an issue on GitHub
