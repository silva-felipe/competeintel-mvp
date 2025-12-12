# CompeteIntel - Brazilian Competitor Intelligence SaaS

> Inteligência Competitiva para o Mercado Brasileiro

A comprehensive SaaS platform that helps Brazilian businesses understand their competitive landscape through location-based analysis, competitor discovery, and market intelligence.

## 🎯 Project Overview

This MVP includes:
- **Landing Page**: Modern, conversion-optimized landing page in Portuguese
- **Backend API**: FastAPI service with mock data (ready for real API integration)
- **Frontend Dashboard**: Next.js application with interactive maps and analytics
- **Docker Setup**: Containerized PostgreSQL database and backend

## 🏗️ Project Structure

```
competitor-intel-br/
├── landing/                  # Landing page
│   ├── index.html           # Main landing page
│   └── styles.css           # Premium CSS with animations
├── mvp/
│   ├── docker-compose.yml   # Docker services
│   ├── Dockerfile           # Backend container
│   ├── .env.example         # Environment template
│   ├── backend/             # FastAPI application
│   │   ├── main.py          # Main API routes
│   │   ├── requirements.txt
│   │   ├── models/
│   │   │   └── schemas.py   # Pydantic models
│   │   ├── services/
│   │   │   ├── competitor_service.py
│   │   │   ├── analysis_service.py
│   │   │   └── cnpj_service.py
│   │   └── data/
│   │       └── mock_competitors.py
│   └── frontend/            # Next.js application
│       ├── app/
│       ├── components/
│       └── lib/
│           └── api.ts       # API client
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Docker Desktop installed
- Node.js 18+ and npm
- (Optional) Python 3.11+ for local backend development

### 1. View Landing Page

```bash
# Open the landing page in your browser
open landing/index.html
```

Or use a simple HTTP server:
```bash
cd landing
python3 -m http.server 8080
# Visit http://localhost:8080
```

### 2. Start Backend Services

```bash
cd mvp

# Copy environment file
cp .env.example .env

# Start Docker services (PostgreSQL + Backend)
docker-compose up -d

# Check logs
docker-compose logs -f backend

# API will be available at http://localhost:8000
# API Documentation: http://localhost:8000/api/docs
```

### 3. Start Frontend

```bash
cd mvp/frontend

# Install dependencies (if not already done)
npm install

# Start development server
npm run dev

# Visit http://localhost:3000
```

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Database
DATABASE_URL=postgresql://competeintel:dev_password_change_in_prod@localhost:5432/competitor_intel

# Application
ENVIRONMENT=development
USE_MOCK_DATA=true  # Set to false when ready for real APIs

# CORS (for frontend)
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Frontend Configuration

Create `mvp/frontend/.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📊 Features

### Current Implementation (MVP)

✅ **Landing Page**
- Hero section with Brazilian market messaging
- Features showcase
- Pricing tiers (Freemium, Professional, Enterprise)
- CTA and demo request form
- Fully responsive design
- Modern animations and glassmorphism effects

✅ **Backend API**
- FastAPI with automatic OpenAPI docs
- Mock competitor data for 10 major Brazilian cities
- 8 business categories (Padaria, Restaurante, Farmácia, etc.)
- Realistic Brazilian business data (CNAE, CNPJ, addresses)
- Market density analysis
- Competitive positioning metrics
- KPI recommendations (Portuguese)
- CNPJ validation service

✅ **Data & Analytics**
- Market saturation scoring
- Revenue estimation (proxy-based)
- Distance calculations
- Online presence scoring
- Payment methods (PIX, cards)
- Delivery availability

✅ **Docker Infrastructure**
- PostgreSQL database container
- Backend API container
- Volume persistence
- Health checks

### Ready for Integration (Commented/Structured)

🔄 **Google Maps/Places API**
- Structure ready in `competitor_service.py`
- Just needs API key and toggling `USE_MOCK_DATA=false`

🔄 **CNPJ API**
- Validation logic implemented
- ReceitaWS integration ready (commented code)
- Just needs API selection and implementation

🔄 **Frontend Components** (Partially implemented)
- API client created
- Component structure ready
- Map integration via Leaflet
- Charts via Chart.js

## 🎨 Design Highlights

### Landing Page
- **Brazilian-themed color palette**: Green/blue gradient inspired by Brazilian flag
- **Glassmorphism effects**: Modern, premium feel
- **Smooth animations**: Fade-in-up on scroll
- **Mobile-first responsive**: Works beautifully on all devices
- **SEO optimized**: Proper meta tags, semantic HTML

### Dashboard (To be completed)
- **Interactive map**: Leaflet + OpenStreetMap
- **Data visualization**: Chart.js charts
- **Real-time analytics**: Market density, positioning
- **KPI cards**: Actionable recommendations

## 🗺️ Supported Locations

**10 Major Brazilian Cities:**
- Sao Paulo (SP)
- Rio de Janeiro (RJ)
- Belo Horizonte (MG)
- Brasília (DF)
- Curitiba (PR)
- Porto Alegre (RS)
- Salvador (BA)
- Fortaleza (CE)
- Recife (PE)
- Manaus (AM)

**8 Business Categories:**
- Padaria (Bakery)
- Restaurante (Restaurant)
- Farmácia (Pharmacy)
- Supermercado (Supermarket)
- Cafeteria (Coffee Shop)
- Academia (Gym)
- Pet Shop
- Lanchonete (Snack Bar)

## 📡 API Endpoints

### `POST /api/search`
Search for competitors and get analytics

**Request:**
```json
{
  "business_name": "Minha Padaria",
  "category": "Padaria",
  "city": "São Paulo",
  "radius_km": 5.0,
  "max_results": 10
}
```

**Response:**
```json
{
  "competitors": [...],
  "analytics": {
    "market_density": {...},
    "kpi_recommendations": [...]
  },
  "total_found": 10
}
```

### `GET /api/cnpj/{cnpj}`
Look up CNPJ information (currently mock data)

### `GET /api/categories`
Get list of supported business categories

### `GET /api/cities`
Get list of supported cities

## 🔐 Mock Data

The MVP uses realistic mock data that simulates:
- Brazilian CNPJ numbers (with valid format)
- Brazilian phone numbers (DDD + 9-digit mobile)
- Brazilian addresses (street types, neighborhoods, CEP)
- Business ratings (3.5-5.0 stars)
- Review counts (10-500 reviews)
- Social media presence (Instagram, Facebook, Website)
- Revenue estimates (category-based with factors)
- Payment methods (PIX acceptance, cards)

## 📈 Analytics Logic

### Market Density
- Calculates competitors per km²
- Classifies as Low/Medium/High/Very High
- Saturation score (0-100)

### Revenue Estimation
Uses proxy metrics:
- Base revenue by category
- Rating factor (higher ratings = more revenue)
- Review count factor (social proof)
- Random variance for realism

### KPI Recommendations
Personalized recommendations based on:
- Rating vs. competitors
- Review count
- Online presence gaps
- Payment method adoption
- Delivery availability
- Market saturation

## 🔄 Next Steps / Future Enhancements

### Phase 2: Real Data Integration
- [ ] Integrate Google Maps/Places API
- [ ] Connect to CNPJ data provider (ReceitaWS or Brasil API)
- [ ] Add social media APIs (Instagram, Facebook)
- [ ] Implement web scraping for pricing data

### Phase 3: Enhanced Features
- [ ] User authentication and profiles
- [ ] Save and track competitors over time
- [ ] Automated alerts for new competitors
- [ ] Export reports (PDF/Excel)
- [ ] Multi-location support
- [ ] Pricing intelligence
- [ ] Review sentiment analysis (Portuguese NLP)

### Phase 4: Advanced Analytics
- [ ] AI-powered market predictions
- [ ] Trend analysis
- [ ] Benchmarking dashboards
- [ ] Custom KPI tracking
- [ ] SEO comparison tools

## 💰 Monetization Strategy

**Freemium Model:**
- Free: 1 analysis, basic competitor list
- Professional (R$149/month): Unlimited analyses, full analytics, monthly updates
- Enterprise (R$499/month): Multi-location, API access, priority support

## 🌐 Deployment

### Production Checklist
- [ ] Set up managed PostgreSQL (AWS RDS, Supabase, etc.)
- [ ] Deploy backend to Railway/Render/Fly.io
- [ ] Deploy frontend to Vercel
- [ ] Configure custom domain
- [ ] Set up SSL certificates
- [ ] Enable error tracking (Sentry)
- [ ] Configure analytics (Google Analytics, Mixpanel)
- [ ] Set up monitoring (Uptime Robot, Better Stack)
- [ ] Implement rate limiting
- [ ] Add API caching (Redis)

### Recommended Stack
- **Frontend**: Vercel (zero-config Next.js deployment)
- **Backend**: Railway or Render (Docker support, easy scaling)
- **Database**: Supabase or AWS RDS (managed PostgreSQL)
- **File Storage**: AWS S3 or Cloudflare R2 (for reports)
- **CDN**: Cloudflare

## 🧪 Testing

```bash
# Backend tests (when implemented)
cd mvp/backend
pytest

# Frontend tests
cd mvp/frontend
npm test

# End-to-end tests
npm run test:e2e
```

## 📝 License

Proprietary - All rights reserved

## 🤝 Contributing

This is a private SaaS project. Internal contributions welcome.

## 📞 Support

For questions or issues:
- Email: support@competeintel.com.br
- Documentation: /api/docs

---

**Built with ❤️ for the Brazilian market**

🇧🇷 Feito no Brasil
