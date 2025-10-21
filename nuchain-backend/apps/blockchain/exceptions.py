class BlockchainError(Exception):
    """Base exception for all blockchain operations"""
    pass

class ConnectionError(BlockchainError):
    """Failed to connect to blockchain network"""
    pass


class TransactionError(BlockchainError):
    """Transaction failed or reverted"""
    pass


class InsufficientBalanceError(BlockchainError):
    """User doesn't have enough available tokens"""
    pass


class InsufficientGasError(BlockchainError):
    """Admin wallet doesn't have enough ETH for gas"""
    pass