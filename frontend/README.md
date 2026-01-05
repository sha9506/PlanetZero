# PlanetZero Frontend

React-based frontend for PlanetZero carbon footprint tracking platform.

## 🚀 Quick Start

### Prerequisites
- Node.js 14+ (Recommended: 18+)
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Start development server
npm start
```

The app will open at http://localhost:3000

## 📦 Project Structure

```
frontend/
├── public/
│   ├── index.html
│   ├── manifest.json
│   └── robots.txt
├── src/
│   ├── App.jsx
│   ├── App.css
│   ├── index.js
│   ├── index.css
│   ├── pages-styles.css
│   ├── assets/
│   ├── components/
│   │   ├── ChartCard.jsx
│   │   ├── EmissionCard.jsx
│   │   ├── Footer.jsx/css
│   │   ├── Navbar.jsx/css
│   │   └── RecommendationCard.jsx/css
│   ├── context/
│   │   └── UserContext.jsx
│   ├── pages/
│   │   ├── Consent.jsx
│   │   ├── DailyLog/
│   │   ├── Dashboard.jsx
│   │   ├── History.jsx/css
│   │   ├── Intro.jsx/css
│   │   ├── Landing.jsx/css
│   │   ├── Leaderboard.jsx/css
│   │   ├── Login.jsx
│   │   ├── Onboarding.jsx
│   │   ├── Profile.jsx
│   │   ├── Recommendations.jsx
│   │   ├── Signup.jsx
│   │   └── Community/
│   ├── services/
│   │   └── api.js
│   └── styles/
│       ├── global.css
│       ├── theme.js
│       └── variables.css
├── package.json
├── .env.example
└── REQUIREMENTS.md
```

## 🛠️ Technologies

- **React** 18.2.0
- **React Router** 6.20.0
- **React Icons** 4.12.0
- **Custom CSS** (No framework)

## 📝 Available Scripts

### `npm start`
Runs the app in development mode at http://localhost:3000

### `npm test`
Launches the test runner in interactive watch mode

### `npm run build`
Builds the app for production to the `build` folder

### `npm run eject`
⚠️ **Warning:** This is a one-way operation. Once you eject, you can't go back!

## 🔌 Backend Integration

The frontend connects to the FastAPI backend at `http://localhost:8000/api`

Configure the API URL in `.env`:
```env
REACT_APP_API_URL=http://localhost:8000/api
```

## 🎨 Styling

- Custom CSS with CSS variables
- Pastel color palette
- Glass-morphism effects
- Gradient accents
- Smooth animations
- Fully responsive design

## 📱 Pages

- **Landing** - Marketing page
- **Intro** - Onboarding introduction
- **Login/Signup** - Authentication
- **Consent** - Data privacy consent
- **Onboarding** - User setup
- **Dashboard** - Overview and analytics
- **DailyLog** - Activity logging
- **History** - Past logs
- **Recommendations** - Eco-friendly tips
- **Community** - Social platform
- **Leaderboard** - Rankings and badges
- **Profile** - User settings

## 🔐 Authentication

Uses JWT tokens stored in localStorage. Configure UserContext to connect to backend API.

## 📊 State Management

- **Local State**: useState
- **Side Effects**: useEffect
- **Global State**: Context API (UserContext)

## 🌐 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## 📄 License

MIT
