# X-EA Awards 🏆

> A comprehensive platform for analyzing and ranking X (Twitter) accounts from East Africa based on various metrics including engagement, follower count, and AI-based ranking.

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-v0.104.1-green.svg)
![React](https://img.shields.io/badge/react-v18.0.0-blue.svg)
![TypeScript](https://img.shields.io/badge/typescript-v4.9.5-blue.svg)

[![Follow on X](https://img.shields.io/twitter/follow/emertechlabs?style=social)](https://twitter.com/emertechlabs)
[![GitHub stars](https://img.shields.io/github/stars/polymathuniversata/X-EA-Awards?style=social)](https://github.com/polymathuniversata/X-EA-Awards/stargazers)

</div>

<div align="center">
    <p>
        <a href="https://twitter.com/emertechlabs">
            <img src="https://img.shields.io/badge/Powered_by-EmerTech_Labs-1da1f2?style=for-the-badge&logo=twitter&logoColor=white" alt="Powered by EmerTech Labs" />
        </a>
    </p>
</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [API Documentation](#-api-documentation)
- [Influencer Categories](#-influencer-categories)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🔹 Backend Features
- **AI-Powered Analysis**
  - Advanced account ranking using machine learning
  - Multi-metric evaluation system
  - Intelligent engagement scoring

- **Regional Focus**
  - Specialized for East African countries
  - Location verification system
  - Country-specific insights

- **Performance Metrics**
  - Engagement rate tracking
  - Posting intensity analysis
  - Thread creation monitoring
  - Follower growth patterns

- **Technical Features**
  - Rate limit handling with progress indicators
  - Results caching for better performance
  - Data export in multiple formats (CSV/JSON)

### 🔸 Frontend Features
- **Modern UI/UX**
  - Clean, responsive design
  - Dark/Light mode support
  - Real-time updates

- **Interactive Components**
  - Dynamic dashboard
  - Sortable leaderboards
  - Advanced search interface
  - Data visualization with Chart.js

## 🛠 Tech Stack

### Backend Infrastructure
```
Python 3.8+ │ FastAPI │ Tweepy v2 │ Pandas │ Scikit-learn
```

### Frontend Framework
```
React 18 │ TypeScript │ Tailwind CSS │ HeadlessUI │ Chart.js │ Axios
```

## 🚀 Installation

### Backend Setup

1. **Clone and Navigate**
   ```bash
   git clone <repository-url>
   cd Xbot
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   # Create .env file in project root
   touch .env

   # Add your X API credentials
   API_KEY=your_api_key
   API_KEY_SECRET=your_api_key_secret
   BEARER_TOKEN=your_bearer_token
   ACCESS_TOKEN=your_access_token
   ACCESS_TOKEN_SECRET=your_access_token_secret
   ```

4. **Launch Server**
   ```bash
   python run_api.py
   # API available at http://localhost:8000
   ```

### Frontend Setup

1. **Navigate to Frontend**
   ```bash
   cd frontend
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Start Development Server**
   ```bash
   npm start
   # Frontend available at http://localhost:3000
   ```

## 📚 API Documentation

### Core Endpoints

| Endpoint | Description | Method |
|----------|-------------|--------|
| `/` | Health check | GET |
| `/search` | Account search with filters | GET |
| `/leaderboard/{category}` | Category-based rankings | GET |
| `/dashboard/stats` | Analytics & statistics | GET |
| `/countries` | Supported countries list | GET |
| `/categories` | Influencer categories | GET |

### Search Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|-----------|
| `topic` | string | Search keyword | Yes |
| `country` | string | Country filter | No |
| `category` | string | Influencer category | No |
| `min_followers` | integer | Minimum followers | No |
| `min_engagement` | float | Minimum engagement rate | No |
| `sort_by` | string | Sort parameter | No |
| `page` | integer | Page number | No |
| `limit` | integer | Results per page | No |

## 👥 Influencer Categories

### Nano Influencers (1K - 10K followers)
- High engagement rates
- Niche market focus
- Strong community interaction

### Micro Influencers (10K - 100K followers)
- Balanced reach and engagement
- Growing authority
- Active community management

### Macro Influencers (100K+ followers)
- Extensive reach
- Established authority
- Broad market influence

## 💻 Development

### Testing
```bash
# Run backend tests
python -m pytest

# Run frontend tests
cd frontend && npm test
```

### Production Build
```bash
# Build frontend
cd frontend && npm run build
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create your feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. Push to the branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
<p>Developed by <a href="https://github.com/polymathuniversata">Polymath Universata</a></p>
<p>Powered by <a href="https://twitter.com/emertechlabs">EmerTech Labs</a> 🚀</p>
<p>Made with ❤️ in Tanzania</p>
</div> 