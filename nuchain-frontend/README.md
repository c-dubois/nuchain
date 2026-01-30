# ⚛️ NuChain Frontend

React TypeScript frontend for the NuChain nuclear investment simulation platform — a portfolio project demonstrating full-stack development with blockchain integration.

## 🎯 Overview

NuChain simulates a decentralized investment platform for fictional nuclear reactors. This frontend provides an interactive interface where users can:

- Create accounts and receive blockchain-backed $NUC tokens
- Browse and invest in nuclear reactor projects
- Track portfolio performance with ROI and carbon offset projections
- Verify wallet balances on Base Sepolia testnet via BaseScan

## 🛠️ Tech Stack

| Technology | Purpose |
| ------------ | --------- |
| React 19 | Component-based UI with hooks |
| TypeScript | Type safety and better DX |
| Vite | Fast builds and hot module replacement |
| React Router | Client-side routing with protected routes |
| Recharts | Data visualization (line, bar, pie charts) |
| Axios | HTTP client with JWT interceptors |
| CSS Variables | Theming without external dependencies |

## ✨ Features Implemented

- **JWT Authentication** — Login/register flow with automatic token refresh
- **Protected Routes** — Auth-guarded pages with loading states
- **Portfolio Dashboard** — Investment tracking with configurable time projections (1, 2, 5, 10 years)
- **Data Visualization** — ROI projections, carbon offset charts, portfolio distribution
- **Investment Modal** — Real-time validation, percentage shortcuts, live ROI preview
- **Blockchain Display** — Wallet addresses with BaseScan verification links
- **Responsive Design** — Mobile-first CSS Grid/Flexbox layout

<!-- markdownlint-disable MD033 -->

### Screenshots

<p align="center">
  <strong>Welcome page</strong><br><br>
  <a href="../docs/screenshots/welcome.png">
    <img src="../docs/screenshots/welcome.png" alt="Welcome Page" width="450">
  </a>
</p>

<p align="center">________</p>

<p align="center">
  <strong>Portfolio dashboard</strong><br><br>
  <a href="../docs/screenshots/dashboard.png">
    <img src="../docs/screenshots/dashboard.png" alt="Portfolio Dashboard" width="450">
  </a>
</p>

<p align="center">________</p>

<p align="center">
  <strong>Reactor marketplace</strong><br><br>
  <a href="../docs/screenshots/reactors.png">
    <img src="../docs/screenshots/reactors.png" alt="Reactor Marketplace" width="450">
  </a>
</p>

<p align="center">________</p>

<p align="center">
  <strong>Investment modal</strong><br><br>
  <a href="../docs/screenshots/investment-modal.png">
    <img src="../docs/screenshots/investment-modal.png" alt="Investment Modal" width="450">
  </a>
</p>

<p align="center">________</p>

<p align="center">
  <strong>Profile with wallet info</strong><br><br>
  <a href="../docs/screenshots/profile.png">
    <img src="../docs/screenshots/profile.png" alt="Profile & Wallet" width="450">
  </a>
</p>

<!-- markdownlint-enable MD033 -->

## 🚀 Local Development

### Prerequisites

- Node.js 18+
- Running [NuChain Backend](../nuchain-backend)

### Setup

```bash
npm install
cp .env.example .env
npm run dev
```

### Environment Variables

```env
VITE_API_URL=http://localhost:8000/api
VITE_CLOUD_NAME=your-cloudinary-name
```

For Vercel deployment, set these in Settings → Environment Variables.

## 📁 Project Structure

``` bash
src/
├── assets/             # Static assets
│   └── images/
├── components/         # Reusable UI components
│   ├── auth/           # LoginForm, RegisterForm
│   ├── common/         # Header, Footer, LoadingSpinner, ProtectedRoute, ScrollToTop
│   ├── dashboard/      # PortfolioSummary, InvestmentChart, TimeButtonGroup
│   └── reactors/       # ReactorCard, ReactorList, InvestmentModal
├── contexts/           # Auth state management
│   ├── AuthContext.tsx
│   └── AuthContextBase.tsx
├── hooks/              # Custom React hooks
│   └── useAuth.ts
├── pages/              # Route-level components
│   ├── Dashboard.tsx
│   ├── Profile.tsx
│   ├── Reactors.tsx
│   └── Welcome.tsx
├── services/           # API integration layer
│   ├── api.ts          # Axios instance with JWT interceptors
│   ├── auth.ts
│   ├── investments.ts
│   └── reactors.ts
├── styles/             # Global styles
│   └── globals.css
├── types/              # TypeScript interfaces
│   ├── auth.ts
│   ├── investment.ts
│   └── reactor.ts
└── utils/              # Helpers and constants
    ├── constants.ts
    └── helpers.ts
```

## 🧪 Testing

<!-- TODO -->

## 🔗 Related

- [NuChain Backend](../nuchain-backend) — Django REST API
- [NuChain Contracts](../nuchain-contracts) — Solidity smart contracts
- [Live Demo](https://nuchain.vercel.app)

---

Built with ⚛️ by [Camille DuBois](https://github.com/c-dubois)
