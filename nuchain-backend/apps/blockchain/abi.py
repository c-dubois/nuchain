NUC_TOKEN_ABI = [
    {
        "type": "constructor",
        "inputs": [],
        "stateMutability": "nonpayable"
    },
    {
        "type": "function",
        "name": "mintSignup",
        "inputs": [{"name": "to", "type": "address", "internalType": "address"}],
        "outputs": [],
        "stateMutability": "nonpayable"
    },
    {
        "type": "function",
        "name": "lock",
        "inputs": [
            {"name": "user", "type": "address", "internalType": "address"},
            {"name": "amount", "type": "uint256", "internalType": "uint256"}
        ],
        "outputs": [],
        "stateMutability": "nonpayable"
    },
    {
        "type": "function",
        "name": "resetPortfolio",
        "inputs": [{"name": "user", "type": "address", "internalType": "address"}],
        "outputs": [],
        "stateMutability": "nonpayable"
    },
    {
        "type": "function",
        "name": "burnAccount",
        "inputs": [{"name": "from", "type": "address", "internalType": "address"}],
        "outputs": [],
        "stateMutability": "nonpayable"
    },
    {
        "type": "function",
        "name": "balanceOf",
        "inputs": [{"name": "account", "type": "address", "internalType": "address"}],
        "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
        "stateMutability": "view"
    },
    {
        "type": "function",
        "name": "lockedBalances",
        "inputs": [{"name": "", "type": "address", "internalType": "address"}],
        "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
        "stateMutability": "view"
    },
    {
        "type": "function",
        "name": "availableBalanceOf",
        "inputs": [{"name": "account", "type": "address", "internalType": "address"}],
        "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
        "stateMutability": "view"
    },
    {
        "type": "function",
        "name": "owner",
        "inputs": [],
        "outputs": [{"name": "", "type": "address", "internalType": "address"}],
        "stateMutability": "view"
    },
    {
        "type": "function",
        "name": "name",
        "inputs": [],
        "outputs": [{"name": "", "type": "string", "internalType": "string"}],
        "stateMutability": "view"
    },
    {
        "type": "function",
        "name": "symbol",
        "inputs": [],
        "outputs": [{"name": "", "type": "string", "internalType": "string"}],
        "stateMutability": "view"
    },
    {
        "type": "function",
        "name": "decimals",
        "inputs": [],
        "outputs": [{"name": "", "type": "uint8", "internalType": "uint8"}],
        "stateMutability": "view"
    },
    {
        "type": "event",
        "name": "TokensLocked",
        "inputs": [
            {"name": "user", "type": "address", "indexed": True, "internalType": "address"},
            {"name": "amount", "type": "uint256", "indexed": False, "internalType": "uint256"}
        ],
        "anonymous": False
    },
    {
        "type": "event",
        "name": "TokensUnlocked",
        "inputs": [
            {"name": "user", "type": "address", "indexed": True, "internalType": "address"},
            {"name": "amount", "type": "uint256", "indexed": False, "internalType": "uint256"}
        ],
        "anonymous": False
    },
    {
        "type": "event",
        "name": "AccountDeleted",
        "inputs": [
            {"name": "user", "type": "address", "indexed": True, "internalType": "address"},
            {"name": "amount", "type": "uint256", "indexed": False, "internalType": "uint256"}
        ],
        "anonymous": False
    }
]