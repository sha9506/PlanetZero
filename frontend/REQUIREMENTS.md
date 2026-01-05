# Frontend Dependencies

This file lists all the npm packages required for the PlanetZero React frontend.

## Installation

```bash
npm install
```

## Dependencies

### Core
- **react** (^18.2.0) - JavaScript library for building user interfaces
- **react-dom** (^18.2.0) - React package for working with the DOM
- **react-scripts** (5.0.1) - Scripts and configuration used by Create React App

### Routing
- **react-router-dom** (^6.20.0) - Declarative routing for React applications

### Icons
- **react-icons** (^4.12.0) - Popular icon library for React (Font Awesome, Material Design, etc.)

### Testing
- **@testing-library/react** (^13.4.0) - Simple and complete testing utilities for React
- **@testing-library/jest-dom** (^5.17.0) - Custom jest matchers for DOM assertions
- **@testing-library/user-event** (^13.5.0) - Fire events the same way the user does

### Performance
- **web-vitals** (^2.1.4) - Library for measuring web vitals metrics

## DevDependencies

None - All development dependencies are managed through react-scripts

## Scripts

```json
{
  "start": "react-scripts start",
  "build": "react-scripts build",
  "test": "react-scripts test",
  "eject": "react-scripts eject"
}
```

## Environment Variables

Create a `.env` file in the frontend directory with:

```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_ENV=development
REACT_APP_ENABLE_AUTH=true
REACT_APP_ENABLE_COMMUNITIES=true
REACT_APP_ENABLE_NOTIFICATIONS=true
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Node Version

- **Minimum**: Node.js 14.x or higher
- **Recommended**: Node.js 18.x or higher

## Package Manager

- **npm** (recommended) or **yarn**

## Build Size (Production)

- Estimated bundle size: ~500KB (gzipped)
- Main chunk: ~200KB
- Vendor chunk: ~300KB

## Future Additions

Consider adding these packages for enhanced functionality:

- **axios** - Promise-based HTTP client (alternative to fetch)
- **chart.js** or **recharts** - For dashboard charts
- **react-query** - Server state management
- **formik** + **yup** - Form management and validation
- **socket.io-client** - Real-time WebSocket communication
- **react-toastify** - Toast notifications
- **framer-motion** - Advanced animations
- **date-fns** or **dayjs** - Date manipulation

## Notes

- All icons are from `react-icons` library (Font Awesome subset)
- No UI framework (Material-UI, Bootstrap, etc.) - using custom CSS
- State management is handled with React Context API and hooks
- No Redux or external state management library needed for current scope
