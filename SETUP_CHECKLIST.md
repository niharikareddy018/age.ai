# Setup Checklist

Use this checklist to ensure your Certificate Vault is properly set up and configured.

## Prerequisites

- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] Docker installed (optional, for containerized deployment)
- [ ] Ethereum node or Infura/Alchemy account (for blockchain features)
- [ ] Git installed

## Backend Setup

- [ ] Backend directory created
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created from `env.example`
- [ ] `SECRET_KEY` set in `.env`
- [ ] `JWT_SECRET_KEY` set in `.env`
- [ ] `DATABASE_URL` configured in `.env`
- [ ] Database initialized (`python scripts/init_db.py --init-db`)
- [ ] Issuer user created (`python scripts/init_db.py --create-issuer`)
- [ ] Backend server starts without errors
- [ ] Health check endpoint works (`/api/health`)

## Frontend Setup

- [ ] Frontend directory created
- [ ] Dependencies installed (`npm install`)
- [ ] `.env` file created with `REACT_APP_API_URL`
- [ ] Frontend server starts without errors
- [ ] Frontend connects to backend API
- [ ] Login page loads correctly
- [ ] Register page loads correctly

## Blockchain Setup

- [ ] Ethereum node running or Infura/Alchemy account configured
- [ ] `ETHEREUM_RPC_URL` set in `.env`
- [ ] Account funded with ETH (for testnet/mainnet)
- [ ] `PRIVATE_KEY` set in `.env` (if using transactions)
- [ ] `ACCOUNT_ADDRESS` set in `.env` (if using transactions)
- [ ] Smart contract deployed (`python scripts/deploy_contract.py`)
- [ ] `CONTRACT_ADDRESS` set in `.env`
- [ ] Contract ABI loaded correctly
- [ ] Test certificate issuance works
- [ ] Test certificate verification works

## Database Setup

- [ ] Database connection working
- [ ] Tables created (users, certificates, share_links)
- [ ] Can create users
- [ ] Can create certificates
- [ ] Can query certificates
- [ ] Database backups configured (production)

## Authentication

- [ ] User registration works
- [ ] User login works
- [ ] JWT tokens generated correctly
- [ ] Token expiration works
- [ ] Protected routes require authentication
- [ ] Role-based access control works (Issuer vs User)

## Certificate Management

- [ ] Issuers can issue certificates
- [ ] Certificates stored in database
- [ ] Certificates stored on blockchain
- [ ] Certificate verification works
- [ ] Certificate details display correctly
- [ ] Share links can be created
- [ ] Share links work and expire correctly
- [ ] Certificate revocation works

## Frontend Features

- [ ] Login page works
- [ ] Register page works
- [ ] Dashboard displays certificates
- [ ] Issue certificate page works (for issuers)
- [ ] Verify certificate page works
- [ ] Certificate detail page works
- [ ] Share link functionality works
- [ ] Navigation works correctly
- [ ] Responsive design works on mobile

## Security

- [ ] Passwords are hashed
- [ ] JWT tokens are secure
- [ ] CORS configured correctly
- [ ] Environment variables not committed to git
- [ ] Secrets are not hardcoded
- [ ] Database credentials secure
- [ ] Private keys stored securely
- [ ] HTTPS enabled (production)

## Deployment

- [ ] Docker images build successfully
- [ ] Docker Compose works locally
- [ ] Environment variables configured for production
- [ ] Database migrated to production database
- [ ] Backend deployed to cloud
- [ ] Frontend deployed to cloud
- [ ] Domain name configured
- [ ] SSL certificate installed
- [ ] Monitoring set up
- [ ] Logging configured

## Testing

- [ ] Backend API tests pass
- [ ] Frontend component tests pass
- [ ] Integration tests pass
- [ ] End-to-end tests pass
- [ ] Performance tests pass
- [ ] Security tests pass

## Documentation

- [ ] README.md updated
- [ ] DEPLOYMENT.md updated
- [ ] QUICKSTART.md updated
- [ ] API documentation updated
- [ ] Code comments added
- [ ] Environment variables documented

## Production Readiness

- [ ] All environment variables set
- [ ] Database backups configured
- [ ] Monitoring and alerting set up
- [ ] Logging configured
- [ ] Error handling implemented
- [ ] Rate limiting configured
- [ ] Security headers configured
- [ ] Performance optimized
- [ ] Scalability considered

## Post-Deployment

- [ ] Application accessible via domain
- [ ] All features working in production
- [ ] SSL certificate valid
- [ ] Database connections stable
- [ ] Blockchain connections stable
- [ ] Monitoring shows healthy status
- [ ] User can register and login
- [ ] Certificates can be issued
- [ ] Certificates can be verified
- [ ] Share links work

## Troubleshooting

If any item is not checked:

1. Check the relevant documentation
2. Review error logs
3. Verify configuration
4. Test in development environment
5. Check cloud provider documentation
6. Open an issue on GitHub

## Support

For help with setup:

- Check README.md
- Check DEPLOYMENT.md
- Check QUICKSTART.md
- Review error logs
- Open an issue on GitHub
