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

    # === WRITE FUNCTIONS ===

    def mint_signup(self, wallet_address):
        """
        Mint 25,000 NUC tokens to a new user's wallet.
        Called during user signup.
        """
        address = Web3.to_checksum_address(wallet_address)
        return self._send_transaction(self.contract.functions.mintSignup, address)

    def lock_tokens(self, wallet_address, amount):
        """
        Lock tokens when user invests in a reactor.
        
        Args:
            wallet_address: User's Ethereum address
            amount: Amount of NUC to lock (Decimal or float)
        """
        address = Web3.to_checksum_address(wallet_address)
        wei_amount = self._to_wei(amount)

        # Check if user has sufficient available balance
        available = self.get_available_balance(address)
        if available < Decimal(amount):
            raise InsufficientBalanceError(
                f"Insufficient balance. Available: {available} NUC, Required: {amount} NUC"
            )
        
        return self._send_transaction(self.contract.functions.lock, address, wei_amount)

    def reset_portfolio(self, wallet_address):
        """
        Unlock all locked tokens for a user.
        Called when user resets their wallet.
        """
        address = Web3.to_checksum_address(wallet_address)
        return self._send_transaction(self.contract.functions.resetPortfolio, address)

    def burn_account(self, wallet_address):
        """
        Burn all tokens for a user.
        Called when user deletes their account.
        """
        address = Web3.to_checksum_address(wallet_address)
        return self._send_transaction(self.contract.functions.burnAccount, address)

    # ==== READ FUNCTIONS (no gas required) ====

    def get_balance(self, wallet_address):
        """Get total balance for a user (in NUC)"""
        address = Web3.to_checksum_address(wallet_address)
        balance_wei = self.contract.functions.balanceOf(address).call()
        return self._from_wei(balance_wei)

    def get_locked_balance(self, wallet_address):
        """Get locked balance for a user (in NUC)"""
        address = Web3.to_checksum_address(wallet_address)
        locked_wei = self.contract.functions.lockedBalances(address).call()
        return self._from_wei(locked_wei)

    def get_available_balance(self, wallet_address):
        """Get available (unlocked) balance for a user (in NUC)"""
        address = Web3.to_checksum_address(wallet_address)
        available_wei = self.contract.functions.availableBalanceOf(address).call()
        return self._from_wei(available_wei)

    def get_all_balances(self, wallet_address):
        """
        Get all balance information for a user.
        
        Returns:
            dict: {'total': Decimal, 'locked': Decimal, 'available': Decimal}
        """
        address = Web3.to_checksum_address(wallet_address)
        return {
            'total': self.get_balance(address),
            'locked': self.get_locked_balance(address),
            'available': self.get_available_balance(address)
        }

# Singleton instance
_service = None

def get_blockchain_service():
    """Get or create singleton blockchain service instance"""
    global _service
    if _service is None:
        _service = BlockchainService()
    return _service