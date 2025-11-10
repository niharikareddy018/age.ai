#!/usr/bin/env python3
"""
Script to deploy the CertificateVerification smart contract to Ethereum network
"""
import os
import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
from solcx import compile_source, install_solc
from dotenv import load_dotenv

load_dotenv()

# Configuration
ETHEREUM_RPC_URL = os.getenv('ETHEREUM_RPC_URL', 'http://localhost:8545')
PRIVATE_KEY = os.getenv('PRIVATE_KEY', '')
ACCOUNT_ADDRESS = os.getenv('ACCOUNT_ADDRESS', '')

def compile_contract():
    """Compile the Solidity contract"""
    print("Compiling smart contract...")
    
    # Read the contract source code
    with open('contracts/CertificateVerification.sol', 'r') as f:
        contract_source = f.read()
    
    # Install Solidity compiler if needed
    try:
        install_solc('0.8.0')
    except:
        pass
    
    # Compile the contract
    compiled_sol = compile_source(contract_source, solc_version='0.8.0')
    contract_interface = compiled_sol['<stdin>:CertificateVerification']
    
    return contract_interface

def deploy_contract():
    """Deploy the contract to the blockchain"""
    print("Connecting to Ethereum network...")
    
    # Initialize Web3
    w3 = Web3(Web3.HTTPProvider(ETHEREUM_RPC_URL))
    
    if not w3.is_connected():
        raise ConnectionError("Cannot connect to Ethereum network")
    
    # Add PoA middleware if needed
    if 'goerli' in ETHEREUM_RPC_URL.lower() or 'mumbai' in ETHEREUM_RPC_URL.lower():
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    
    # Check account balance
    if PRIVATE_KEY and ACCOUNT_ADDRESS:
        balance = w3.eth.get_balance(ACCOUNT_ADDRESS)
        print(f"Account balance: {w3.from_wei(balance, 'ether')} ETH")
        
        if balance == 0:
            print("Warning: Account has zero balance. You may need to fund it.")
    
    # Compile contract
    contract_interface = compile_contract()
    
    # Get contract class
    CertificateVerification = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']
    )
    
    # Deploy contract
    print("Deploying contract...")
    
    if PRIVATE_KEY and ACCOUNT_ADDRESS:
        # Build transaction
        nonce = w3.eth.get_transaction_count(ACCOUNT_ADDRESS)
        
        transaction = CertificateVerification.constructor().build_transaction({
            'from': ACCOUNT_ADDRESS,
            'nonce': nonce,
            'gas': 2000000,
            'gasPrice': w3.eth.gas_price
        })
        
        # Sign transaction
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
        
        # Send transaction
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"Transaction hash: {tx_hash.hex()}")
        
        # Wait for receipt
        print("Waiting for transaction confirmation...")
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        contract_address = tx_receipt.contractAddress
        print(f"Contract deployed at address: {contract_address}")
        
    else:
        # For local development with Ganache
        transaction_hash = CertificateVerification.constructor().transact({
            'from': w3.eth.accounts[0]
        })
        tx_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
        contract_address = tx_receipt.contractAddress
        print(f"Contract deployed at address: {contract_address}")
    
    # Save contract address and ABI
    contract_info = {
        'address': contract_address,
        'abi': contract_interface['abi'],
        'transaction_hash': tx_receipt.transactionHash.hex()
    }
    
    with open('contracts/contract_info.json', 'w') as f:
        json.dump(contract_info, f, indent=2)
    
    print("\nContract deployment successful!")
    print(f"Contract Address: {contract_address}")
    print("\nPlease update your .env file with:")
    print(f"CONTRACT_ADDRESS={contract_address}")
    
    return contract_address, contract_interface['abi']

if __name__ == '__main__':
    try:
        deploy_contract()
    except Exception as e:
        print(f"Error deploying contract: {str(e)}")
        import traceback
        traceback.print_exc()

