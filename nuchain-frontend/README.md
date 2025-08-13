# ⚛️ NuChain Frontend - React TypeScript Application

The frontend interface for the NuChain nuclear investment simulation platform, built with React 19 and TypeScript.

## 🏗️ Architecture

### Technology Stack

- **Framework**: React 19.1 with TypeScript
- **Build Tool**: Vite 7.0
- **Routing**: React Router DOM 7.7
- **Charts**: Recharts 3.1
- **HTTP Client**: Axios 1.11
- **Styling**: CSS Modules with CSS Variables
- **State Management**: React Context + useState
- **Type Safety**: TypeScript 5.8

### Project Structure

``` bash
nuchain-frontend/
├── public/
│   ├── vite.svg
├── src/
│   ├── components/         # Reusable UI components
│   │   ├── auth/           # Authentication forms
│   │   ├── common/         # Shared components (Header, Footer, etc.)
│   │   ├── dashboard/      # Portfolio dashboard components
│   │   └── reactors/       # Reactor-related components
│   ├── contexts/           # React Context providers
│   │   ├── AuthContext.tsx
│   │   └── AuthContextBase.tsx
│   ├── hooks/              # Custom React hooks
│   │   └── useAuth.ts
│   ├── pages/              # Main application pages
│   │   ├── Dashboard.tsx
│   │   ├── Profile.tsx
│   │   ├── Reactors.tsx
│   │   └── Welcome.tsx
│   ├── services/           # API communication
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   └── investments.ts
│   ├── styles/             # Global styles and themes
│   │   └── globals.css
│   ├── types/              # TypeScript type definitions
│   │   ├── auth.ts
│   │   ├── investment.ts
│   │   └── reactor.ts
│   ├── utils/              # Helper functions and constants
│   │   ├── constants.ts
│   │   └── helpers.ts
│   ├── App.tsx             # Main application component
│   └── main.tsx            # Application entry point
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── .env                    # Environment variables
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm/yarn
- Running NuChain backend API

### Installation

1. **Install dependencies**

   ```bash
   npm install
   # or
   yarn install
   ```

2. **Start development server**

   ```bash
   npm run dev
   # or
   yarn dev
   ```

3. **Access application**
   Open [http://localhost:3000](http://localhost:3000) in your browser

## 🔧 Environment Variables

Create a `.env` file in the project root:

```env
VITE_API_URL=http://localhost:8000/api
VITE_CLOUD_NAME=your-cloudinary-name
```

### Production Environment

```env
VITE_API_URL=https://your-backend-api.com/api
VITE_CLOUD_NAME=your-cloudinary-name
```

## 🎨 Design System

### Color Palette

The application uses a nuclear energy-inspired color scheme:

```css
:root {
  --color-primary: #daff02;    /* Nuclear green */
  --color-accent: #fe572a;     /* Energy orange */
  --color-secondary: #685bc7;  /* Tech purple */
  --color-light: #f3f0eb;      /* Off-white */
  --color-dark: #201e1f;       /* Dark gray */
  --color-dark-bg: #2a2829;    /* Background */
  --color-medium: #3a3839;     /* Medium gray */
  --color-success: #4ade80;    /* Success green */
  --color-error: #f87171;      /* Error red */
}
```

### Typography

- **Primary Font**: System font stack (-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto')
- **Headings**: Bold weights with subtle text shadows
- **Body Text**: Regular weight with 1.6 line height

### Component Library

#### Buttons

- `btn-primary`: Main action button (nuclear green)
- `btn-secondary`: Secondary actions (tech purple)
- `btn-accent`: Accent actions (energy orange)
- `btn-danger`: Destructive actions (red)

#### Cards

- `card`: Base card component with hover effects
- `summary-card`: Dashboard summary cards
- `reactor-card`: Reactor information cards

## 🧩 Key Components

### Authentication

**LoginForm** (`src/components/auth/LoginForm.tsx`)

- Handles user login with validation
- Integrates with JWT authentication

**RegisterForm** (`src/components/auth/RegisterForm.tsx`)

- User registration with form validation
- Password confirmation and strength checking

### Dashboard

**PortfolioSummary** (`src/components/dashboard/PortfolioSummary.tsx`)

- Displays total invested, projected returns, carbon offset
- Time period selector for projections

**InvestmentChart** (`src/components/dashboard/InvestmentChart.tsx`)

- Line/bar charts showing ROI projections
- Carbon offset visualization
- Portfolio distribution pie chart

### Reactors

**ReactorCard** (`src/components/reactors/ReactorCard.tsx`)

- Displays reactor information and metrics
- Investment button and funding progress
- Supports both browse and portfolio variants

**InvestmentModal** (`src/components/reactors/InvestmentModal.tsx`)

- Investment form with amount validation
- Percentage buttons for quick selection
- Real-time ROI and carbon offset preview

## 🛣️ Routing

```tsx
Routes:
/                    -> Welcome page (unauthenticated)
/dashboard           -> Portfolio dashboard (protected)
/invest              -> Reactor marketplace (protected)
/profile             -> User profile management (protected)
```

### Protected Routes

The `ProtectedRoute` component wraps authenticated pages:

```tsx
<ProtectedRoute>
  <Dashboard />
</ProtectedRoute>
```

## 📊 State Management

### Authentication Context

Global authentication state managed through React Context:

```tsx
interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  updateUser: (user: User) => void;
}
```

### Component State

Local state management using `useState` and `useEffect`:

- Form data and validation
- Loading states
- Error handling
- Modal visibility

## 🔗 API Integration

### HTTP Client Setup

Axios instance with automatic JWT token handling:

```typescript
// Automatic token injection
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Automatic token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    // Handle 401 errors and refresh tokens
  }
);
```

### Service Layer

**authService** (`src/services/auth.ts`)

- User authentication operations
- Profile management
- Wallet operations

**reactorService** (`src/services/reactors.ts`)

- Reactor data fetching
- Investment operations

**investmentService** (`src/services/investments.ts`)

- Portfolio operations
- Investment tracking

## 📱 Responsive Design

### Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1200px
- **Desktop**: > 1200px

### Mobile-First Approach

```css
/* Mobile styles first */
.component {
  /* Mobile styles */
}

@media (min-width: 768px) {
  .component {
    /* Tablet styles */
  }
}

@media (min-width: 1200px) {
  .component {
    /* Desktop styles */
  }
}
```

## 🎯 Performance Optimization

### Code Splitting

- Route-based code splitting with React.lazy()
- Component lazy loading for modals

### Image Optimization

- Cloudinary integration for reactor images
- Fallback images with error handling
- Responsive image loading

### Bundle Optimization

- Tree shaking with Vite
- Production build optimization
- Asset compression

## 🧪 Testing

### Test Setup

```bash
npm test
# or
npm run test:watch
```

### Testing Strategy

- **Unit Tests**: Component logic and utilities
- **Integration Tests**: API interactions
- **E2E Tests**: User workflows (optional)

### Mocking

Mock API responses for testing:

```typescript
// Mock axios for testing
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;
```

## 🚀 Build & Deployment

### Development Build

```bash
npm run dev
```

### Production Build

```bash
npm run build
npm run preview  # Preview production build
```

### Deployment Options

#### Vercel

1. Connect GitHub repository
2. Configure build settings:
   - Build Command: `npm run build`
   - Output Directory: `dist`
3. Set environment variables
4. Deploy

#### Netlify

1. Connect GitHub repository
2. Configure build settings:
   - Build Command: `npm run build`
   - Publish Directory: `dist`
3. Set environment variables
4. Deploy

## 🔧 Development Tools

### VS Code Extensions

Recommended extensions for development:

- ES7+ React/Redux/React-Native snippets
- TypeScript Importer
- Prettier - Code formatter
- ESLint
- Auto Rename Tag

### Scripts

```json
{
  "dev": "vite",
  "build": "tsc -b && vite build",
  "lint": "eslint .",
  "preview": "vite preview"
}
```

## 🎨 Styling Guidelines

### CSS Organization

- Global styles in `src/styles/globals.css`
- Component-specific styles alongside components
- CSS variables for theming
- BEM-like naming conventions

### Animation

Subtle animations for better UX:

```css
.card {
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}
```

## 🐛 Debugging

### Development Tools

- React Developer Tools extension
- Redux DevTools (if using Redux)
- Browser network tab for API debugging

### Common Issues

1. **CORS errors**: Check backend CORS configuration
2. **API connection**: Verify VITE_API_URL environment variable
3. **Authentication**: Check token storage and expiration
4. **Build errors**: Clear node_modules and reinstall

### Logging

```typescript
// Development logging
if (import.meta.env.DEV) {
  console.log('Debug info:', data);
}
```

## 🤝 Contributing

### Code Style

- Use TypeScript for all new components
- Follow existing naming conventions
- Write meaningful component and prop names
- Add JSDoc comments for complex functions

### Component Guidelines

1. **Functional Components**: Use function declarations
2. **Props Interface**: Define TypeScript interfaces
3. **Default Props**: Use ES6 default parameters
4. **Exports**: Use named exports for components

```typescript
interface ComponentProps {
  title: string;
  onClick?: () => void;
}

export const Component: React.FC<ComponentProps> = ({ 
  title, 
  onClick 
}) => {
  return <div onClick={onClick}>{title}</div>;
};
```

---

## Happy coding! ⚛️
