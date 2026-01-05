# 🌍 PlanetZero

**A comprehensive carbon footprint tracking and community engagement platform empowering individuals to take action towards a carbon-neutral future.**

---

## 📖 Project Overview

PlanetZero is a React-based web application designed to help users monitor, reduce, and offset their carbon emissions through daily activity tracking, personalized recommendations, and community-driven initiatives. The platform combines data visualization, gamification, and social features to make sustainability engaging and achievable.

## Key Features

### Core Functionality
- **Daily Activity Logging** - Track transportation, energy usage, food consumption, and shopping habits
- **Edit Daily Logs** - Review and modify today's entries with inline editing
- **Carbon Footprint Calculation** - Real-time CO₂ emissions estimates based on user activities
- **Interactive Dashboard** - Visual insights into emissions trends and category breakdowns with Chart.js
- **History Tracking** - Monitor progress over time with detailed logs and analytics
- **Personalized Recommendations** - Smart suggestions to reduce environmental impact
- **Data Visualization** - Monthly trend charts, category breakdown (doughnut charts), and emission tracking

### Gamification & Engagement
- **Leaderboard System** - Compete with others and track your environmental ranking
- **Achievement Badges** - Earn 9+ badges including:
  - Newcomer, Tracker, Earth Lover (earned through onboarding)
  - Top Performer, Green Hero, Recycling Champion
  - Bike Master, Energy Saver, Community Founder
- **Points & Rankings** - Motivate sustainable behavior through friendly competition

### Community Features
- **Discover Communities** - Find and join groups aligned with your interests
- **Create Communities** - Start your own sustainability initiative
- **Community Roles** - Structured leadership with Leaders, Event Coordinators, Moderators, and Members
- **Group Activities** - Participate in cleanups, workshops, rides, and advocacy
- **Community Chat** - Connect with like-minded individuals (coming soon)
- **Categories** - Gardening, Recycling, Transport, Energy, Conservation

### Real-time Notifications
- **Smart Notifications** - Stay updated on achievements, community events, and milestones
- **Notification Types**:
  - Achievement notifications (badges earned)
  - Community updates (events, invitations)
  - Personalized recommendations
  - Milestone celebrations (CO₂ saved)
- **Unread Badges** - Visual indicators for new notifications
- **Notification Management** - Mark as read, delete, or mark all as read

### User Experience
- **Modern UI/UX** - Clean, minimalist design with pastel color palette
- **Responsive Design** - Optimized for desktop, tablet, and mobile devices
- **Smooth Animations** - Engaging transitions and hover effects
- **Accessibility** - Intuitive navigation and clear visual hierarchy

## Technology Stack

### Frontend
- **Framework**: React 18+
- **Routing**: React Router DOM
- **Charts**: Chart.js with react-chartjs-2
- **Icons**: React Icons (Font Awesome)
- **Styling**: Custom CSS with CSS Variables
- **State Management**: React Hooks (useState, useEffect, useLocation)
- **Context API**: User authentication context

### Backend
- **Framework**: FastAPI (Python)
- **Database**: MongoDB with Motor (async driver)
- **Authentication**: JWT with OAuth2
- **Password Hashing**: bcrypt
- **API Documentation**: Swagger/OpenAPI
- **Chart Generation**: Chart.js compatible JSON structures
- **Emission Calculations**: Custom service with activity-based factors
- **Collections**: users, user_consents, profiles, daily_logs, carbon_footprints, recommendations, communities, leaderboard, notifications, badges

## �️ Technologies Used

- **React.js** - Component-based UI framework for building interactive interfaces
- **FastAPI** - High-performance Python web framework for building RESTful APIs
- **MongoDB** - NoSQL database for flexible data storage and retrieval
- **Chart.js** - JavaScript charting library for data visualization and analytics
- **JWT Authentication** - Secure token-based user authentication and authorization
- **React Router** - Client-side routing for seamless navigation between pages

## �🚀 Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Python 3.8+ (for backend)
- MongoDB (local or cloud)

### Frontend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/sha9506/PlanetZero.git
   cd PlanetZero/frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env if needed (default settings work with local backend)
   ```

4. **Start development server**
   ```bash
   npm start
   ```

5. **Open browser**
   ```
   http://localhost:3000
   ```

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB connection and settings
   ```

5. **Initialize database**
   ```bash
   python init_db.py
   ```

6. **Start backend server**
   ```bash
   python main.py
   ```

7. **API Documentation**
   ```
   http://localhost:8000/docs
   ```

## 📊 Key Features Walkthrough

### 1. Daily Log & Editing
- Navigate to "Daily Log" from the navbar
- Add transportation, energy usage, and food entries
- View "Today's Entries" section showing all logged activities
- Click "✏️ Edit Entries" to modify existing data
- Emissions are calculated automatically and saved to database
- Dashboard and History update automatically after saving

### 2. Dashboard Analytics
- View total emissions with breakdown by category
- Interactive charts show trends over time
- Doughnut chart displays emission distribution
- Click "🔄 Refresh Data" to manually update
- Real-time data from MongoDB carbon_footprints collection

### 3. History Tracking
- See day-by-day emission breakdown
- Visual bar charts for each day
- Detailed table with transport, energy, and food emissions
- Filter and analyze patterns over time

### 4. Community Engagement
- Browse and join existing communities
- Create your own sustainability group
- Participate in events and challenges
- Earn badges and climb the leaderboard

## 🏗️ Project Structure

```
PlanetZero/
├── frontend/
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   │   ├── Navbar.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── EmissionCard.jsx
│   │   │   └── ChartCard.jsx
│   │   ├── pages/             # Page components
│   │   │   ├── Landing.jsx
│   │   │   ├── Dashboard.jsx  # Charts & emissions summary
│   │   │   ├── DailyLog.jsx   # Activity tracking & editing
│   │   │   ├── History.jsx    # Historical data view
│   │   │   ├── Leaderboard.jsx
│   │   │   └── Profile.jsx
│   │   ├── services/          # API integration
│   │   │   └── api.js         # Backend API calls
│   │   ├── context/           # React Context
│   │   │   └── UserContext.jsx
│   │   └── styles/            # Global styles
│   └── package.json
│
├── backend/
│   ├── routes/                # API endpoints
│   │   ├── auth.py            # Authentication
│   │   ├── daily_log.py       # Activity logging
│   │   ├── charts.py          # Chart data generation
│   │   ├── history.py         # Historical data
│   │   └── communities.py
│   ├── services/              # Business logic
│   │   ├── emission_service.py  # CO₂ calculations
│   │   └── chart_service.py     # Chart data formatting
│   ├── schemas/               # Pydantic models
│   ├── db_utils/              # Database utilities
│   ├── database.py            # MongoDB connection
│   ├── main.py                # FastAPI app
│   └── requirements.txt
│
└── README.md
```

## 🔑 Environment Variables

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000/api
```

### Backend (.env)
```env
DATABASE_URL=mongodb://localhost:27017
DATABASE_NAME=planetzero_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🧪 Testing

### Test User Credentials
```
Email: ravi.kumar@example.com
Password: Password123
```

### Testing Flow
1. Start backend: `cd backend && python main.py`
2. Start frontend: `cd frontend && npm start`
3. Login with test credentials
4. Complete consent and onboarding (if first time)
5. Navigate to Daily Log
6. Add activities (e.g., 200km diesel car = 34.2 kg CO₂)
7. Check Dashboard for updated charts
8. View History for day-by-day breakdown
9. Edit today's entries and see auto-refresh

## 📈 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/signup` - User registration

### Daily Activities
- `POST /api/daily-log` - Create/Update daily log
- `GET /api/daily-log/{date}` - Get specific date log

### Analytics
- `GET /api/dashboard/summary` - Dashboard summary
- `GET /api/charts?days=30` - Chart data
- `GET /api/history?limit=30` - Historical logs

### Community
- `GET /api/communities` - List communities
- `POST /api/communities` - Create community
- `POST /api/communities/{id}/join` - Join community

### User
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update profile
- `GET /api/notifications` - Get notifications

## Current Status

**✅ Fully Implemented & Integrated**:

### Backend (FastAPI + MongoDB)
- ✅ User authentication with JWT tokens
- ✅ User consent management
- ✅ Profile creation and onboarding
- ✅ Daily activity logging with emission calculations
- ✅ Carbon footprint tracking and storage
- ✅ Chart data generation (monthly trends, category breakdowns)
- ✅ History API with day-by-day breakdown
- ✅ Dashboard summary endpoint
- ✅ Recommendations system
- ✅ Community platform
- ✅ Leaderboard rankings
- ✅ Notifications system
- ✅ Badge management

### Frontend (React)
- ✅ User authentication flow (Login/Signup)
- ✅ User consent page
- ✅ Onboarding wizard
- ✅ Daily Log page with activity tracking
- ✅ **Today's Entries Display** - View and edit today's logged activities
- ✅ **Inline Editing** - Modify entries without losing data
- ✅ Dashboard with real-time data
- ✅ **Chart.js Integration** - Line and Doughnut charts
- ✅ **Auto-refresh** - Dashboard and History update after log changes
- ✅ History page with detailed breakdown
- ✅ Recommendations page
- ✅ Community discovery and management
- ✅ Leaderboard with rankings
- ✅ Notifications center
- ✅ Profile management
- ✅ Responsive design

### Recent Updates (January 2026)
- ✅ **Edit Daily Logs** - Users can now edit their daily entries
- ✅ **Today's Entries Section** - Shows current day's logged activities with emissions breakdown
- ✅ **Smart Refresh** - Dashboard and History auto-update after changes
- ✅ **Manual Refresh Buttons** - Added 🔄 Refresh Data buttons for user control
- ✅ **Chart Data Flow** - Complete integration from Daily Log → Backend Calculation → Database → Dashboard Charts
- ✅ **Navigation State Management** - Location-aware data refreshing

**🚧 In Development**:
- Real-time community chat (WebSocket)
- Carbon offset marketplace
- Mobile app (React Native)
- Advanced analytics and insights
- Social sharing features

**📋 Upcoming Features**:
- AI-powered emission predictions
- Integration with smart home devices
- Carbon offset purchase integration
- Multi-language support
- Dark mode theme

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Guidelines
- Follow existing code structure and naming conventions
- Add comments for complex logic
- Test all changes locally before submitting
- Update README if adding new features
- Ensure backend and frontend stay in sync

## 📝 Changelog

### v1.2.0 (January 2026)
- ✨ Added edit functionality for daily logs
- ✨ Implemented "Today's Entries" display section
- ✨ Auto-refresh for Dashboard and History after updates
- ✨ Manual refresh buttons for user control
- 🐛 Fixed data flow from Daily Log to Charts
- 🐛 Fixed navigation state management

### v1.1.0 (December 2025)
- ✨ Integrated Chart.js for data visualization
- ✨ Backend chart data generation service
- ✨ Carbon footprints collection for analytics
- 🐛 Fixed authentication and database issues

### v1.0.0 (November 2025)
- 🎉 Initial release
- ✨ Complete backend API with FastAPI
- ✨ React frontend with routing
- ✨ MongoDB integration
- ✨ User authentication and onboarding

## License

This project is licensed under the MIT License.

## Author

**Sabnam Hazari**
- GitHub: [@sha9506](https://github.com/sha9506)

---

**PlanetZero** - *Empowering individuals to make a difference, one action at a time.* 🌱
