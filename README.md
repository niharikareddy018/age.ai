# Blockchain-secured Academic Certificate Vault

A comprehensive platform for issuing, storing, and verifying academic certificates using blockchain technology. This system provides tamper-proof certificate storage and instant verification capabilities through a combination of Flask backend, React frontend, and Ethereum-based smart contracts.

## Features

- 🔐 **Blockchain Verification**: Certificates are hashed and stored on the Ethereum blockchain for immutable verification
- 👥 **Role-based Access Control**: Issuer and user roles with different permissions
- 🔗 **Time-limited Sharing**: Shareable links with expiration dates
- 📜 **Certificate Lifecycle Management**: Issue, verify, revoke certificates
- 🔒 **JWT Authentication**: Secure authentication with token-based access
- 📱 **Responsive Design**: Modern UI that works on all devices

## System Architecture

### Backend (Flask)

- RESTful API with Flask
- SQLAlchemy for database management
- JWT authentication
- Web3.py for blockchain integration
- PostgreSQL/SQLite database support

### Frontend (React)

- React 18 with React Router
- Context API for state management
- Axios for API calls
- Responsive CSS design

### Smart Contract (Solidity)

- Ethereum smart contract for certificate storage
- Hash-based certificate indexing
- Verification functions
- Event emission for tracking

## Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL (for production) or SQLite (for development)
- Ethereum node or Infura/Alchemy account
- Docker and Docker Compose (for containerized deployment)

## Installation

### Backend Setup

1. Navigate to the backend directory:

```bash
cd backend
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file:

```bash
cp .env.example .env
```

5. Update `.env` with your configuration:

```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=sqlite:///certificates.db
ETHEREUM_RPC_URL=http://localhost:8545
CONTRACT_ADDRESS=your-contract-address
PRIVATE_KEY=your-private-key
ACCOUNT_ADDRESS=your-account-address
```

6. Initialize the database:

```bash
python app.py
```

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Create a `.env` file:

```env
REACT_APP_API_URL=http://localhost:5000
```

4. Start the development server:

```bash
npm start
```

### Smart Contract Deployment

1. Install Solidity compiler:

```bash
pip install py-solc-x
```

2. Update blockchain configuration in `backend/.env`

3. Deploy the contract:

```bash
python scripts/deploy_contract.py
```

4. Update `CONTRACT_ADDRESS` in `.env` with the deployed contract address

## Docker Deployment

### Using Docker Compose

1. Update environment variables in `docker-compose.yml` or create a `.env` file

2. Build and start all services:

```bash
docker-compose up -d
```

3. The application will be available at:
   - Frontend: http://localhost
   - Backend API: http://localhost:5000
   - PostgreSQL: localhost:5432

### Individual Docker Images

#### Backend

```bash
docker build -f Dockerfile.backend -t certificate-vault-backend .
docker run -p 5000:5000 --env-file backend/.env certificate-vault-backend
```

#### Frontend

```bash
docker build -f Dockerfile.frontend -t certificate-vault-frontend .
docker run -p 80:80 certificate-vault-frontend
```

## Cloud Deployment

### AWS Deployment

1. **EC2 Setup**:

   - Launch an EC2 instance with Ubuntu
   - Install Docker and Docker Compose
   - Clone the repository
   - Configure security groups to allow HTTP/HTTPS traffic

2. **RDS Setup**:

   - Create a PostgreSQL RDS instance
   - Update `DATABASE_URL` in environment variables

3. **Elastic Beanstalk** (Alternative):
   - Use EB CLI to deploy the backend
   - Configure environment variables
   - Set up load balancer

### Google Cloud Platform

1. **Cloud Run**:

   - Build Docker images
   - Deploy to Cloud Run
   - Configure environment variables
   - Set up Cloud SQL for PostgreSQL

2. **App Engine**:
   - Use `app.yaml` for backend deployment
   - Use `app.yaml` for frontend deployment

### Azure Deployment

1. **Container Instances**:

   - Build Docker images
   - Push to Azure Container Registry
   - Deploy to Container Instances

2. **App Service**:
   - Deploy backend as App Service
   - Deploy frontend as Static Web App
   - Configure Azure Database for PostgreSQL

## Usage

### Register an Account

1. Navigate to the registration page
2. Choose role: "User" or "Issuer"
3. Fill in username, email, and password
4. Click "Register"

### Issue a Certificate (Issuer Only)

1. Login as an issuer
2. Navigate to "Issue Certificate"
3. Select the owner (student)
4. Fill in certificate details
5. Click "Issue Certificate"
6. The certificate will be stored on the blockchain

### Verify a Certificate

1. Navigate to "Verify" page
2. Enter Certificate ID or Hash
3. Click "Verify Certificate"
4. View verification results

### View Certificates

1. Login to your account
2. Navigate to "Dashboard"
3. View all your certificates (or issued certificates if you're an issuer)

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user
- `GET /api/auth/users` - Get all users (Issuer only)

### Certificates

- `POST /api/certificates/issue` - Issue a certificate (Issuer only)
- `POST /api/certificates/verify` - Verify a certificate
- `GET /api/certificates/my-certificates` - Get user's certificates
- `GET /api/certificates/issued` - Get issued certificates (Issuer only)
- `GET /api/certificates/:certificate_id` - Get certificate details
- `POST /api/certificates/:certificate_id/share` - Create share link
- `GET /api/certificates/share/:link_token` - Get shared certificate
- `POST /api/certificates/:certificate_id/revoke` - Revoke certificate (Issuer only)

## Security Considerations

1. **Authentication**: JWT tokens with expiration
2. **Password Hashing**: Werkzeug security for password hashing
3. **Blockchain**: Immutable certificate records
4. **CORS**: Configured for secure cross-origin requests
5. **Environment Variables**: Sensitive data stored in environment variables

## Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Style

```bash
# Backend
black backend/
flake8 backend/

# Frontend
npm run lint
```

## Troubleshooting

### Backend Issues

1. **Database Connection**: Check DATABASE_URL in .env
2. **Blockchain Connection**: Verify ETHEREUM_RPC_URL is correct
3. **Contract Address**: Ensure CONTRACT_ADDRESS is set after deployment

### Frontend Issues

1. **API Connection**: Check REACT_APP_API_URL
2. **CORS Errors**: Verify CORS configuration in backend
3. **Authentication**: Check token storage in localStorage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.

## Acknowledgments

- Flask framework
- React library
- Web3.py for blockchain integration
- Ethereum blockchain
