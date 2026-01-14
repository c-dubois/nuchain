# ⚛️ NuChain Backend - Django REST API

The backend API for NuChain nuclear investment simulation platform, built with Django REST Framework.

## 🏗️ Architecture

### Technology Stack

- **Framework**: Django 5.2.4 with Django REST Framework 3.16
- **Database**: PostgreSQL with psycopg2
- **Authentication**: JWT with SimpleJWT and token blacklisting
- **Testing**: Django's built-in testing framework
- **Deployment**: Render with Gunicorn
- **Environment**: Python 3.11+
- **Blockchain**: Web3.py for Base Sepolia integration

### Project Structure

``` bash
nuchain-backend/
├── apps/
│   ├── common/             # Shared utilities and base classes
│   │   └── tests/          # Common test utilities
│   ├── users/              # User authentication and profiles
│   │   ├── models.py       # User profile model
│   │   ├── serializers.py  # User data serialization
│   │   ├── views.py        # Authentication endpoints
│   │   └── tests/          # User app tests
│   ├── reactors/           # Nuclear reactor management
│   │   ├── models.py       # Reactor model and calculations
│   │   ├── serializers.py  # Reactor data serialization
│   │   ├── views.py        # Reactor API endpoints
│   │   ├── management/     # Management commands
│   │   └── tests/          # Reactor app tests
│   ├── investments/        # Investment logic and portfolio
│   │   ├── models.py       # Investment model
│   │   ├── serializers.py  # Investment serialization
│   │   ├── views.py        # Investment endpoints
│   │   └── tests/          # Investment app tests
│   └── blockchain/         # Blockchain integration
│       ├── abi.py          # NUC Token contract ABI
│       ├── exceptions.py   # Custom blockchain exceptions
│       └── services.py     # BlockchainService class
├── nuchain_backend/
│   ├── settings.py         # Django configuration
│   ├── urls.py             # URL routing
│   └── wsgi.py             # WSGI application
├── requirements.txt        # Python dependencies
├── build.sh                # Render deployment script
└── manage.py               # Django management
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- pip and virtualenv

### Installation

1. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Database setup**

   ```bash
   python manage.py migrate
   python manage.py create_reactors  # Load sample reactor data
   ```

4. **Create superuser (optional)**

   ```bash
   python manage.py createsuperuser
   ```

5. **Run development server**

   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000`

## 🔧 Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-very-secret-key-here
DEBUG=True
DB_NAME=nuchain_db
DB_USER=nuchain_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Production Environment

```env
SECRET_KEY=production-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:port/dbname
ALLOWED_HOSTS=yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourfrontend.com
```

### Blockchain Environment

```env
BASE_SEPOLIA_RPC_URL=https://sepolia.base.org
NUC_CONTRACT_ADDRESS=0x7a8ed93c1eA030eC8F283e93Ff1BB008e57D4791
ADMIN_PRIVATE_KEY=your-admin-wallet-private-key
```

## 📡 API Endpoints

### Authentication (`/api/auth/`)

| Method | Endpoint | Description |
|--------|----------|-------------|

| POST | `/register/` | Create account + mint 25,000 NUC tokens |
| POST | `/login/` | User authentication |
| POST | `/logout/` | Logout and blacklist token |
| POST | `/token/refresh/` | Refresh access token |
| GET | `/profile/` | Get user profile |
| PUT | `/profile/update/` | Update user profile |
| POST | `/password/change/` | Change password |
| POST | `/wallet/reset/` | Reset wallet + unlock all tokens on blockchain |
| DELETE | `/account/delete/` | Delete account + burn all tokens on blockchain |

### Reactors (`/api/reactors/`)

| Method | Endpoint | Description |
|--------|----------|-------------|

| GET | `/` | List all active reactors |
| GET | `/{id}/` | Get specific reactor details |

### Investments (`/api/investments/`)

| Method | Endpoint | Description |
|--------|----------|-------------|

| GET | `/` | List user's investments |
| POST | `/` | Create investment + lock tokens on blockchain |
| GET | `/portfolio_summary/` | Get portfolio summary with projections |

## 🏢 Data Models

### User Profile

- Extends Django's User model
- Tracks $NUC token balance (default: 25,000)
- Stores Ethereum wallet address (`wallet_address`)
- Handles balance deduction and wallet reset
- Syncs with NUC token contract on Base Sepolia

### Reactor

- Name, type, location, description
- ROI rate and carbon offset metrics
- Funding capacity and current funding
- Investment validation methods

### Investment

- Links user to reactor with investment amount
- Tracks creation timestamp
- Calculates ROI and carbon offset projections

## ⛓️ Blockchain Integration

NuChain uses a custom ERC20 token (NUC) deployed on Base Sepolia testnet.

### Smart Contract

| Property | Value |
|----------|-------|

| Token Name | NuChain Token (NUC) |
| Contract Address | `0x7a8ed93c1eA030eC8F283e93Ff1BB008e57D4791` |
| Network | Base Sepolia (Testnet) |
| Chain ID | 84532 |
| Decimals | 18 |

### Token Flow

1. **Registration**: User receives 25,000 NUC tokens (minted on-chain)
2. **Investment**: Tokens are locked on-chain when investing
3. **Reset Wallet**: All locked tokens are unlocked on-chain
4. **Delete Account**: All tokens are burned on-chain

### Verification

All transactions are verifiable on [BaseScan](https://sepolia.basescan.org/address/0x7a8ed93c1eA030eC8F283e93Ff1BB008e57D4791).

> ⚠️ **Note**: This is a testnet simulation only. No real tokens or transactions are involved.

## 🧪 Testing

### Run all tests

```bash
python manage.py test
```

### Run specific app tests

```bash
python manage.py test apps.users
python manage.py test apps.reactors
python manage.py test apps.investments
```

### Run with coverage

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generates HTML coverage report
```

### Test Categories

- **Unit Tests**: Model methods and business logic
- **Integration Tests**: API endpoints and workflows
- **Authentication Tests**: JWT token management
- **Validation Tests**: Data validation and error handling

## 🔒 Security Features

### Authentication

- JWT access and refresh tokens
- Token blacklisting on logout
- Automatic token refresh handling
- Password strength validation

### API Security

- CORS configuration
- Request rate limiting (production)
- SQL injection protection via ORM
- XSS protection headers

### Data Validation

- Serializer-based input validation
- Custom business logic validation
- Decimal precision for financial calculations

## 🚀 Deployment

### Render Deployment

1. **Connect repository** to Render
2. **Environment variables** set in Render dashboard
3. **Build script** configured in `build.sh`:

   ```bash
   pip install -r requirements.txt
   python manage.py collectstatic --no-input
   python manage.py migrate
   python manage.py create_reactors
   ```

4. **Start command**: `gunicorn nuchain_backend.wsgi:application`

### Database Migration

For production deployments:

```bash
python manage.py migrate
python manage.py create_reactors
```

## 🛠️ Management Commands

### Create Sample Reactors

```bash
python manage.py create_reactors
```

Loads 6 fictional nuclear reactors with predefined characteristics.

### Custom Management Commands

You can create additional management commands in:

``` bash
apps/{app_name}/management/commands/
```

## 🔧 Development

### Code Style

- Follow PEP 8 guidelines
- Use Django's naming conventions
- Document complex business logic
- Write descriptive commit messages

### Adding New Features

1. **Create models** in appropriate app
2. **Write serializers** for data transformation
3. **Implement views** with proper permissions
4. **Add URL routing**
5. **Write comprehensive tests**
6. **Update documentation**

### Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 🐛 Debugging

### Common Issues

1. **Database connection errors**
   - Check PostgreSQL is running
   - Verify database credentials
   - Ensure database exists

2. **JWT token errors**
   - Check SECRET_KEY consistency
   - Verify token expiration settings
   - Ensure proper CORS configuration

3. **Import errors**
   - Check Python path configuration
   - Verify virtual environment activation

### Logging

Configure Django logging in `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
    },
}
```

## 📊 Performance

### Database Optimization

- Indexed foreign keys
- Efficient querysets with select_related
- Database connection pooling in production

### API Optimization

- Pagination for list endpoints
- Caching for static reactor data
- Optimized serializer queries

---

**Admin Interface**: Available at `/admin/` when running with `DEBUG=True` for managing users, reactors, and investments
