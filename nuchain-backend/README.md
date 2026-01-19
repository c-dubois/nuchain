# ⚛️ NuChain Backend

Django REST API for the NuChain nuclear investment simulation platform — a portfolio project demonstrating full-stack development with blockchain integration.

## 🎯 Overview

This backend handles all server-side logic for NuChain, including:

- User authentication with JWT tokens
- Nuclear reactor data and investment management
- Portfolio calculations with ROI and carbon offset projections
- On-chain token operations via Web3.py (mint, lock, unlock, burn)

## 🛠️ Tech Stack

| Technology | Purpose |
| ------------ | --------- |
| Django 5.2 | Web framework |
| Django REST Framework | RESTful API design |
| PostgreSQL | Production database |
| SimpleJWT | JWT authentication with token blacklisting |
| Web3.py | Ethereum/Base Sepolia blockchain integration |
| Gunicorn | Production WSGI server |
| python-decouple | Environment variable management |

## ✨ Features Implemented

- **JWT Authentication** — Access/refresh tokens with blacklisting on logout
- **User Profiles** — Balance tracking, wallet address storage
- **Reactor Management** — CRUD operations with funding calculations
- **Investment Logic** — Validation, balance deduction, portfolio aggregation
- **Portfolio Projections** — ROI and carbon offset calculations across time periods
- **Blockchain Integration** — Real ERC20 token operations on Base Sepolia testnet

## ⛓️ Blockchain Integration

NuChain uses a custom ERC20 token (NUC) deployed on Base Sepolia testnet.

| Property | Value |
| ---------- | ------- |
| Token | NuChain Token (NUC) |
| Contract | `0x7a8ed93c1eA030eC8F283e93Ff1BB008e57D4791` |
| Network | Base Sepolia (Chain ID: 84532) |

### Token Operations

| Action | Blockchain Effect |
| -------- | ------------------- |
| Register | Mint 25,000 NUC to new wallet |
| Invest | Lock tokens (cannot transfer) |
| Reset Wallet | Unlock all tokens |
| Delete Account | Burn all tokens |

All transactions verifiable on [BaseScan](https://sepolia.basescan.org/address/0x7a8ed93c1eA030eC8F283e93Ff1BB008e57D4791).

> **Note:** This is a testnet simulation — no real value is involved.

## 📡 API Endpoints

### Authentication `/api/auth/`

| Method | Endpoint | Description |
| -------- | ---------- | ------------- |
| POST | `/register/` | Create account + mint 25,000 NUC tokens |
| POST | `/login/` | Authenticate user |
| POST | `/logout/` | Logout and blacklist refresh token |
| POST | `/token/refresh/` | Refresh access token |
| GET | `/profile/` | Get user profile |
| PUT | `/profile/update/` | Update profile |
| POST | `/password/change/` | Change password |
| POST | `/wallet/reset/` | Reset wallet + unlock all tokens on blockchain |
| DELETE | `/account/delete/` | Delete account + burn all tokens on blockchain |

### Reactors `/api/reactors/`

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| GET | `/` | List all active reactors |
| GET | `/{id}/` | Get specific reactor details |

### Investments `/api/investments/`

| Method | Endpoint | Description |
| -------- | ---------- | ------------- |
| GET | `/` | List user's investments |
| POST | `/` | Create investment + lock tokens on blockchain |
| GET | `/portfolio_summary/` | Get portfolio summary with projections |

## 🏗️ Data Models

### UserProfile

- Extends Django User model
- Tracks $NUC token balance (default: 25,000)
- Stores Ethereum wallet address (`wallet_address`)
- Handles balance deduction and wallet reset
- Syncs with on-chain NUC token contract on Base Sepolia

### Reactor

- Name, type, location, description
- Annual ROI rate and carbon offset metrics per NUC
- Funding capacity and current funding
- Computed properties: funding percentage, is fully funded
- Investment validation methods

### Investment

- Links user to reactor with investment amount
- Tracks creation timestamp
- Calculation methods for ROI and carbon offset projections

## 🚀 Local Development

### Prerequisites

- Python 3.11+
- PostgreSQL 14+

### Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Database setup
python manage.py migrate
python manage.py create_reactors

# Run server
python manage.py runserver
```

> **Tip:** Admin interface available at `/admin/` when `DEBUG=True`

### Environment Variables

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Database
DB_NAME=nuchain_db
DB_USER=nuchain_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Blockchain
BASE_SEPOLIA_RPC_URL=https://base-sepolia-rpc.publicnode.com
NUC_CONTRACT_ADDRESS=0x7a8ed93c1eA030eC8F283e93Ff1BB008e57D4791
ADMIN_PRIVATE_KEY=your-admin-wallet-private-key
```

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

Test coverage includes:

- User authentication flows
- Investment validation logic
- Portfolio calculations
- API endpoint responses

## 📁 Project Structure

``` bash
apps/
├── blockchain/         # Web3.py integration
│   ├── abi.py          # NUC token contract ABI
│   ├── exceptions.py
│   └── services.py     # BlockchainService class
├── common/             # Shared test utilities
│   └── tests/
├── investments/        # Investment logic and portfolio
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests/
├── reactors/           # Reactor data and endpoints
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── management/     # create_reactors command
│   └── tests/
└── users/              # Authentication and profiles
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    └── tests/

nuchain_backend/        # Django project config
├── settings.py
├── urls.py
└── wsgi.py
```

## 🔗 Related

- [NuChain Frontend](../nuchain-frontend) — React TypeScript UI
- [NuChain Contracts](../nuchain-contracts) — Solidity smart contracts
- [Live API](https://nuchain-backend.onrender.com)

---

Built with ⚛️ by [Camille DuBois](https://github.com/c-dubois)
