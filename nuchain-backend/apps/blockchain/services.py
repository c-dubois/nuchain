from web3 import Web3
from eth_account import Account
from decimal import Decimal
from django.conf import settings
from .abi import NUC_TOKEN_ABI
from .exceptions import (
    ConnectionError,
    TransactionError,
    InsufficientBalanceError,
    InsufficientGasError
)

class BlockchainService:
    """Service for interacting with NUC Token smart contract on Base Sepolia"""

    def __init__(self):
        # Connect to Base Sepolia
        self.w3 = Web3(Web3.HTTPProvider(settings.BASE_SEPOLIA_RPC_URL))

        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to Base Sepolia")
        
        # Load NucToken contract
        self.contract_address = Web3.to_checksum_address(settings.NUC_CONTRACT_ADDRESS)
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=NUC_TOKEN_ABI
        )

        # Load admin account
        self.admin = Account.from_key(settings.ADMIN_PRIVATE_KEY)

        # Token decimals (18 decimals for NUC)
        self.decimals = 18

    def _to_wei(self, amount):
        """Convert NUC amount to wei (smallest unit of NUC)"""
        return int(Decimal(amount) * Decimal(10 ** self.decimals))

    def _from_wei(self, wei_amount):
        """Convert wei to NUC amount"""
        return Decimal(wei_amount) / Decimal(10 ** self.decimals)

    def _send_transaction(self, function, *args):
        """Send a transaction to the blockchain"""
        try:
            # Check admin has enough ETH for gas
            admin_balance = self.w3.eth.get_balance(self.admin.address)
            if admin_balance < self.w3.to_wei(0.001, 'ether'):
                raise InsufficientGasError("Admin wallet has insufficient ETH for gas")
        
            # Build transaction
            nonce = self.w3.eth.get_block_transaction_count(self.admin.address)
            gas_price = self.w3.eth.gas_price

            transaction = function(*args).build_transaction({
                'from': self.admin.address,
                'nonce': nonce,
                'gas': 300000,
                'gasPrice': gas_price,
                'chainID': 84532  # Base Sepolia
            })

            # Sign transaction
            signed = self.w3.eth.account.sign_transaction(transaction, self.admin.key)

            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)

            # Wait for confirmation
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

            if receipt.status != 1:
                raise TransactionError("Transaction reverted")
            
            return {
                'success': True,
                'tx_hash': tx_hash.hex(),
                'block_number': receipt.blockNumber
            }
        
        except Exception as e:
            if isinstance(e, (InsufficientGasError, TransactionError)):
                raise
            raise TransactionError(f"Transaction failed: {str(e)}")