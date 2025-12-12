# 🚀 Quick Start Guide

Get your Brazilian Competitor Intelligence SaaS running in 5 minutes!

## Option 1: View Landing Page (Instant)

```bash
cd /Users/felipesilva/.gemini/antigravity/scratch/competitor-intel-br/landing
open index.html
```

Or use Python's HTTP server:
```bash
cd /Users/felipesilva/.gemini/antigravity/scratch/competitor-intel-br/landing
python3 -m http.server 8080
# Visit: http://localhost:8080
```

## Option 2: Run Full MVP

### Step 1: Start Backend (30 seconds)

```bash
cd /Users/felipesilva/.gemini/antigravity/scratch/competitor-intel-br/mvp

# Copy environment file
cp .env.example .env

# Start Docker containers
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f backend
```

✅ Backend API: http://localhost:8000
✅ API Docs: http://localhost:8000/api/docs

### Step 2: Start Frontend (1 minute)

```bash
cd /Users/felipesilva/.gemini/antigravity/scratch/competitor-intel-br/mvp/frontend

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Install dependencies (first time only)
npm install

# Start dev server
npm run dev
```

✅ Dashboard: http://localhost:3000

### Step 3: Test It!

1. Go to http://localhost:3000
2. Fill in the search form:
   - Category: **Padaria**
   - City: **São Paulo**
   - Radius: **5 km**
3. Click "Buscar Concorrentes 🔍"
4. See instant results with analytics!

## 🎯 Test Scenarios

Try these searches to see different results:

```
Category: Restaurante | City: Rio de Janeiro | Radius: 3km
Category: Farmácia | City: Belo Horizonte | Radius: 5km
Category: Cafeteria | City: São Paulo | Radius: 2km
```

## 🛑 Stopping Services

```bash
cd /Users/felipesilva/.gemini/antigravity/scratch/competitor-intel-br/mvp

# Stop Docker containers
docker compose down

# Stop frontend (Ctrl+C in terminal)
```

## 📚 Documentation

- **Full README**: See `README.md` in project root
- **API Docs**: http://localhost:8000/api/docs (when backend running)
- **Walkthrough**: Check artifacts for detailed walkthrough

## 🔧 Troubleshooting

**Docker not starting?**
- Make sure Docker Desktop is running
- Check ports 5432 and 8000 are not in use

**Frontend can't connect to backend?**
- Verify backend is running: `docker compose ps`
- Check .env.local has correct API URL
- Make sure CORS_ORIGINS in backend .env includes frontend URL

**Node packages not installing?**
- Try: `rm -rf node_modules package-lock.json && npm install`
- Make sure you have Node 18+: `node --version`

## 🎉 You're Ready!

Your complete SaaS platform is now running with:
- ✅ Professional landing page
- ✅ RESTful API with mock Brazilian business data
- ✅ Interactive dashboard with analytics
- ✅ Market intelligence and KPI recommendations
- ✅ All in Portuguese for the Brazilian market

**Next step:** Get feedback from Brazilian business owners and decide on real API integration!
