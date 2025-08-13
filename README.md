# ⚛️ NuChain - Nuclear Investment Simulation Platform

A fullstack web application that simulates a decentralized investment platform for fictional nuclear power plants. Users receive mock crypto tokens ($NUC) to invest in virtual reactor projects while tracking simulated ROI and carbon offset impact.

## 🌟 Project Overview

NuChain bridges climate tech, energy infrastructure, and DeFi simulation by offering an interactive educational experience that connects users to clean energy funding mechanics and crypto-style investing. The platform helps demystify both nuclear energy and tokenomics in a visually compelling and approachable way.

### Key Features

- **🔐 User Authentication**: Secure JWT-based login/registration system
- **💰 Mock Token Wallet**: Every user starts with 25,000 $NUC tokens
- **⚡ Reactor Marketplace**: Browse and invest in 6 unique fictional nuclear reactors
- **📊 Portfolio Dashboard**: Track investments, ROI projections, and carbon offset impact
- **🌱 Environmental Impact**: Monitor CO₂ emissions offset through clean energy investments
- **📈 Interactive Charts**: Visualize investment performance over multiple time periods (1, 2, 5, 10 years)

## 🏗️ Architecture

### Technology Stack

**Frontend:**

- React 19.1 with TypeScript
- Vite for build tooling
- Recharts for data visualization
- React Router for navigation
- Axios for API communication

**Backend:**

- Django 5.2.4 with Django REST Framework
- PostgreSQL database
- JWT authentication with token blacklisting
- Comprehensive test suite (95%+ coverage)

**Deployment:**

- Render (Backend)
- Vercel (Frontend)
- PostgreSQL (Production database)

### Project Structure

``` bash
nuchain/
├── nuchain-backend/         # Django REST API
│   ├── apps/
│   │   ├── users/           # User authentication & profiles
│   │   ├── reactors/        # Nuclear reactor models & data
│   │   └── investments/     # Investment logic & portfolio tracking
│   ├── nuchain_backend/     # Django project settings
│   └── requirements.txt
├── nuchain-frontend/        # React TypeScript application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Main application pages
│   │   ├── services/        # API communication
│   │   ├── contexts/        # React context providers
│   │   └── utils/           # Helper functions & constants
│   └── package.json
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.11+
- PostgreSQL 14+
- Git

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/nuchain.git
   cd nuchain
   ```

2. **Backend Setup**

   ```bash
   cd nuchain-backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Set up environment variables
   cp .env.example .env
   # Edit .env with your database credentials
   
   # Run migrations and create sample data
   python manage.py migrate
   python manage.py create_reactors
   
   # Start development server
   python manage.py runserver
   ```

3. **Frontend Setup**

   ```bash
   cd nuchain-frontend
   npm install
   
   # Set up environment variables
   cp .env.example .env
   # Edit .env with your API URL
   
   # Start development server
   npm run dev
   ```

4. **Access the application**
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API: [http://localhost:8000](http://localhost:8000)

## 🎮 How to Use

1. **Create Account**: Sign up with a username, email, and password
2. **Explore Reactors**: Browse the 6 available nuclear reactor projects
3. **Make Investments**: Allocate your 25,000 $NUC starting balance across reactors
4. **Track Performance**: Monitor your portfolio's ROI and carbon offset projections
5. **Reset & Retry**: Use the wallet reset feature to start over with fresh capital

## 🧪 Reactor Profiles

The platform features 6 unique fictional reactors with varying characteristics:

- **NuWave**: Advanced pressurized water reactor small modular reactor (SMR) (4.5% ROI)
- **Helios FusionDrive**: Experimental fusion-fission hybrid reactor (-1.5% ROI, high carbon offset)
- **Phoenix RegenX-7**: Next-generation molten salt reactor (MSR) (6.8% ROI)
- **Fermi-III**: Lead-cooled fast breeder reactor (LCFBR) (2.2% ROI)
- **Atucha Q-Tronix**: Quantum-assisted traveling wave reactor (QTWR) (4.2% ROI)
- **Nexus CORE**: High-temperature gas-cooled reactor (HTGR) (3.8% ROI)

## 🧪 Testing

**Backend Tests:**

```bash
cd nuchain-backend
python manage.py test
```

**Frontend Tests:**

```bash
cd nuchain-frontend
npm test
```

## 🚀 Deployment

### Backend (Render)

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure environment variables
4. Deploy with the provided `build.sh` script

### Frontend (Vercel)

1. Connect your repository
2. Set build command: `npm run build`
3. Set output directory: `dist`
4. Configure environment variables

## 🔧 Environment Variables

### Backend (.env)

```env
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:port/dbname
ALLOWED_HOSTS=yourdomain.com,localhost
CORS_ALLOWED_ORIGINS=https://yourfrontend.com
```

### Frontend (.env)

```env
VITE_API_URL=https://your-backend-api.com/api
VITE_CLOUD_NAME=your-cloudinary-name
```

## 🙏 Acknowledgments

- Nuclear reactor designs inspired by real-world Gen IV reactor concepts
- Simulated climate data designed for educational purposes
- User interface and investment process inspired by leading decentralized finance protocols

## ⚠️ Disclaimer

NuChain is an educational simulation platform. No real investments, transactions, or nuclear reactors are involved. All reactor data, financial data, and projections are fictional and for demonstration purposes only.

---

### Built with ⚛️ by Camille DuBois
