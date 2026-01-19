# ⚛️ NuChain Contracts

Solidity smart contracts for the NuChain nuclear investment simulation platform — a portfolio project demonstrating ERC-20 token development with custom locking mechanics on Base Sepolia testnet.

## 🎯 Overview

NuChain uses a custom ERC-20 token (NUC) to simulate blockchain-backed investments in fictional nuclear reactors. The contract implements a **locking mechanism** that restricts token transfers when users "invest" — tokens remain in the user's wallet but cannot be moved until unlocked via portfolio reset.

This design mirrors real DeFi staking patterns while keeping all operations verifiable on-chain.

## 📋 Deployed Contract

| Property | Value |
| -------- | ----- |
| Name | NuChain Token |
| Symbol | NUC |
| Decimals | 18 |
| Network | Base Sepolia |
| Chain ID | 84532 |
| Address | `0x7a8ed93c1eA030eC8F283e93Ff1BB008e57D4791` |
| Explorer | [BaseScan](https://sepolia.basescan.org/address/0x7a8ed93c1eA030eC8F283e93Ff1BB008e57D4791) |

> **Note:** This is a testnet deployment for educational purposes — tokens have no real monetary value.

## 🛠️ Tech Stack

| Technology | Purpose |
| ---------- | ------- |
| Solidity 0.8.28 | Smart contract language |
| OpenZeppelin 5.4 | ERC-20 and Ownable base contracts |
| Hardhat 3 | Development framework and testing |
| Hardhat Ignition | Declarative deployment system |
| Base Sepolia | Layer 2 testnet (Optimism stack) |

## 📜 Contract Functions

### Public Functions

| Function | Returns | Description |
| -------- | ------- | ----------- |
| `balanceOf(address)` | `uint256` | Total token balance (inherited from ERC-20) |
| `availableBalanceOf(address)` | `uint256` | Balance minus locked amount |
| `lockedBalances(address)` | `uint256` | Amount currently locked |
| `transfer(address, uint256)` | `bool` | Transfer tokens (reverts if insufficient unlocked balance) |
| `transferFrom(address, address, uint256)` | `bool` | Transfer on behalf (reverts if insufficient unlocked balance) |

### Admin Functions (onlyOwner)

| Function | Description |
| -------- | ----------- |
| `mintSignup(address to)` | Mint 25,000 NUC to new user wallet |
| `lock(address user, uint256 amount)` | Lock tokens when user invests in reactor |
| `resetPortfolio(address user)` | Unlock all locked tokens for user |
| `burnAccount(address from)` | Burn all tokens on account deletion |

### Disabled Functions

| Function | Reason |
| -------- | ------ |
| `renounceOwnership()` | Reverts with "Ownership cannot be renounced!" — prevents orphaned contract |

## 📡 Events

| Event | Parameters | Emitted When |
| ----- | ---------- | ------------ |
| `TokensLocked` | `address indexed user, uint256 amount` | Tokens locked via `lock()` |
| `TokensUnlocked` | `address indexed user, uint256 amount` | Tokens unlocked via `resetPortfolio()` |
| `AccountDeleted` | `address indexed user, uint256 amount` | Tokens burned via `burnAccount()` |
| `Transfer` | `address indexed from, address indexed to, uint256 value` | Standard ERC-20 transfer (inherited) |

## 🔐 Design Decisions

### Locking vs. Burning for Investments

Tokens are **locked** rather than burned when users invest. This approach:

- Keeps tokens visible in user's wallet (better UX)
- Allows portfolio reset without re-minting
- Mirrors real staking/vesting contract patterns
- All state changes verifiable on-chain

### Admin-Controlled Operations

All token operations (mint, lock, unlock, burn) require `onlyOwner` access. The backend service holds the admin private key and executes transactions on behalf of users. This simplifies the UX — users don't need browser wallets or testnet ETH.

### Disabled Ownership Renunciation

`renounceOwnership()` is overridden to revert. This prevents accidental loss of admin access, which would brick the contract since all meaningful operations require owner privileges.

## 🚀 Local Development

### Prerequisites

- Node.js 22+
- npm

### Setup

```bash
npm install
```

### Compile Contracts

```bash
npx hardhat compile
```

### Run Tests

```bash
# Run all tests (Solidity + TypeScript)
npx hardhat test

# Run only Solidity tests (Foundry-style)
npx hardhat test solidity

# Run only TypeScript tests (Mocha)
npx hardhat test mocha
```

### Deploy to Local Network

```bash
npx hardhat ignition deploy ignition/modules/NucToken.ts
```

### Deploy to Base Sepolia

```bash
# Set private key (interactive prompt)
npx hardhat keystore set NUCHAIN_PRIVATE_KEY

# Deploy
npx hardhat ignition deploy --network baseSepolia ignition/modules/NucToken.ts
```

### Verify on BaseScan

```bash
npx hardhat verify --network baseSepolia <CONTRACT_ADDRESS>
```

## 🔧 Configuration

### Environment Variables

Set via Hardhat keystore or environment:

| Variable | Description |
| -------- | ----------- |
| `BASE_SEPOLIA_RPC_URL` | RPC endpoint for Base Sepolia |
| `NUCHAIN_PRIVATE_KEY` | Deployer wallet private key |
| `BASESCAN_API_KEY` | API key for contract verification |

### hardhat.config.ts

```typescript
networks: {
  baseSepolia: {
    type: "http",
    url: configVariable("BASE_SEPOLIA_RPC_URL"),
    accounts: [configVariable("NUCHAIN_PRIVATE_KEY")],
    chainId: 84532,
  },
},
```

## 📁 Project Structure

```bash
nuchain-contracts/
├── contracts/
│   ├── NucToken.sol        # Main ERC-20 contract
│   └── NucToken.t.sol      # Foundry-style Solidity tests
├── ignition/
│   ├── modules/
│   │   └── NucToken.ts     # Deployment module
│   └── deployments/
│       └── chain-84532/    # Base Sepolia deployment artifacts
├── hardhat.config.ts
├── package.json
└── tsconfig.json
```

## 🧪 Test Coverage

The test suite (`NucToken.t.sol`) covers:

- Initial state verification (name, symbol, decimals, owner)
- Minting tokens to new users
- Locking and unlocking token balances
- Transfer restrictions on locked tokens
- Account deletion (burn)
- Access control (non-owner rejection)
- Ownership renunciation prevention

## 🔗 Related

- [NuChain Backend](../nuchain-backend) — Django REST API with Web3.py integration
- [NuChain Frontend](../nuchain-frontend) — React TypeScript UI
- [Live Contract](https://sepolia.basescan.org/address/0x7a8ed93c1eA030eC8F283e93Ff1BB008e57D4791)

---

Built with ⚛️ by [Camille DuBois](https://github.com/c-dubois)
