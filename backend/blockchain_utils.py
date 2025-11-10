from web3 import Web3
from web3.middleware import geth_poa_middleware
import hashlib
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Blockchain configuration
ETHEREUM_RPC_URL = os.getenv('ETHEREUM_RPC_URL', 'http://localhost:8545')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS', '')
PRIVATE_KEY = os.getenv('PRIVATE_KEY', '')
ACCOUNT_ADDRESS = os.getenv('ACCOUNT_ADDRESS', '')

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(ETHEREUM_RPC_URL))

# Add PoA middleware if needed (for networks like Goerli, Mumbai, etc.)
if 'goerli' in ETHEREUM_RPC_URL.lower() or 'mumbai' in ETHEREUM_RPC_URL.lower():
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Load contract ABI from deployment file if available
CONTRACT_ABI = None
CONTRACT_INFO_PATH = os.path.join(os.path.dirname(__file__), '..', 'contracts', 'contract_info.json')

try:
    if os.path.exists(CONTRACT_INFO_PATH):
        with open(CONTRACT_INFO_PATH, 'r') as f:
            contract_info = json.load(f)
            CONTRACT_ABI = contract_info.get('abi')
            if not CONTRACT_ADDRESS:
                CONTRACT_ADDRESS = contract_info.get('address', '')
except Exception as e:
    print(f"Warning: Could not load contract info: {e}")

# Fallback ABI if contract info not available
if not CONTRACT_ABI:
    CONTRACT_ABI = [
        {
            "inputs": [
                {"internalType": "string", "name": "_certificateId", "type": "string"},
                {"internalType": "string", "name": "_hash", "type": "string"},
                {"internalType": "string", "name": "_studentName", "type": "string"},
                {"internalType": "string", "name": "_courseName", "type": "string"},
                {"internalType": "string", "name": "_issueDate", "type": "string"}
            ],
            "name": "issueCertificate",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {"internalType": "string", "name": "_hash", "type": "string"}
            ],
            "name": "verifyCertificate",
            "outputs": [
                {"internalType": "bool", "name": "", "type": "bool"}
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {"internalType": "string", "name": "_hash", "type": "string"}
            ],
            "name": "getCertificate",
            "outputs": [
                {"internalType": "string", "name": "certificateId", "type": "string"},
                {"internalType": "string", "name": "studentName", "type": "string"},
                {"internalType": "string", "name": "courseName", "type": "string"},
                {"internalType": "string", "name": "issueDate", "type": "string"},
                {"internalType": "uint256", "name": "timestamp", "type": "uint256"}
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "anonymous": False,
            "inputs": [
                {"indexed": True, "internalType": "string", "name": "certificateId", "type": "string"},
                {"indexed": True, "internalType": "string", "name": "hash", "type": "string"},
                {"indexed": False, "internalType": "string", "name": "studentName", "type": "string"}
            ],
            "name": "CertificateIssued",
            "type": "event"
        }
    ]

def get_contract():
    """Get the contract instance"""
    if not CONTRACT_ADDRESS:
        raise ValueError("CONTRACT_ADDRESS not set in environment variables")
    
    if not w3.is_connected():
        raise ConnectionError("Cannot connect to Ethereum network")
    
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    return contract

def calculate_certificate_hash(student_name, course_name, issue_date, issuer_id, owner_id):
    """Calculate SHA-256 hash of certificate data"""
    data_string = f"{student_name}|{course_name}|{issue_date}|{issuer_id}|{owner_id}"
    return hashlib.sha256(data_string.encode()).hexdigest()

def store_certificate_on_blockchain(certificate_id, certificate_hash, student_name, course_name, issue_date):
    """Store certificate hash on blockchain"""
    try:
        if not CONTRACT_ADDRESS:
            # For development/testing without blockchain
            print("Warning: CONTRACT_ADDRESS not set. Certificate not stored on blockchain.")
            return "0x" + "0" * 64  # Mock transaction hash
        
        contract = get_contract()
        
        if not PRIVATE_KEY or not ACCOUNT_ADDRESS:
            raise ValueError("PRIVATE_KEY and ACCOUNT_ADDRESS must be set for blockchain transactions")
        
        # Build transaction
        nonce = w3.eth.get_transaction_count(ACCOUNT_ADDRESS)
        
        transaction = contract.functions.issueCertificate(
            certificate_id,
            certificate_hash,
            student_name,
            course_name,
            issue_date
        ).build_transaction({
            'from': ACCOUNT_ADDRESS,
            'nonce': nonce,
            'gas': 200000,
            'gasPrice': w3.eth.gas_price
        })
        
        # Sign transaction
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
        
        # Send transaction
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # Wait for transaction receipt
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        if receipt.status == 1:
            return receipt.transactionHash.hex()
        else:
            raise Exception("Transaction failed on blockchain")
    
    except Exception as e:
        print(f"Error storing certificate on blockchain: {str(e)}")
        raise

def verify_certificate_on_blockchain(certificate_hash):
    """Verify certificate hash on blockchain"""
    try:
        if not CONTRACT_ADDRESS:
            # For development/testing without blockchain
            print("Warning: CONTRACT_ADDRESS not set. Cannot verify on blockchain.")
            return False
        
        contract = get_contract()
        
        # Call the verify function
        is_verified = contract.functions.verifyCertificate(certificate_hash).call()
        
        return is_verified
    
    except Exception as e:
        print(f"Error verifying certificate on blockchain: {str(e)}")
        return False

def get_certificate_from_blockchain(certificate_hash):
    """Get certificate data from blockchain"""
    try:
        if not CONTRACT_ADDRESS:
            return None
        
        contract = get_contract()
        
        # Call the getCertificate function
        result = contract.functions.getCertificate(certificate_hash).call()
        
        return {
            'certificate_id': result[0],
            'student_name': result[1],
            'course_name': result[2],
            'issue_date': result[3],
            'timestamp': result[4]
        }
    
    except Exception as e:
        print(f"Error getting certificate from blockchain: {str(e)}")
        return None

