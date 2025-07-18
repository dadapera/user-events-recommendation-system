# Docker Quick Start Guide

## 🚀 Getting Started

### 1. Start Docker Desktop
Make sure Docker Desktop is running on your Windows machine.

### 2. Open Terminal
```bash
cd C:\Users\devid\Desktop\repo\vaimo_recom_sys
```

### 3. Choose Your Mode

#### Development Mode (Recommended for coding)
```bash
docker-compose -f docker-compose.dev.yml up --build
```
- ✅ Hot reload when you edit files
- ✅ Volume mounts for live code changes
- ✅ Development environment variables

#### Production Mode
```bash
docker-compose up --build
```
- ✅ Production optimized
- ✅ Better performance
- ✅ Production environment variables

### 4. Access Your App
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Events**: http://localhost:8000/events/
- **Recommendations**: http://localhost:8000/users/user_1/recommendations/

## 🛠️ Useful Commands

### View Logs
```bash
# Follow logs in real-time
docker-compose logs -f

# View logs for specific service
docker-compose logs app
```

### Stop Services
```bash
# Stop and remove containers
docker-compose down

# Stop but keep containers
docker-compose stop
```

### Rebuild After Changes
```bash
# Force rebuild
docker-compose up --build --force-recreate

# Or for development
docker-compose -f docker-compose.dev.yml up --build --force-recreate
```

### Run Tests
```bash
# Run tests inside container
docker-compose exec app python tests/test_recommendations.py

# Or enter container shell
docker-compose exec app bash
```

## 🐛 Troubleshooting

### Container Won't Start
```bash
# Check if Docker is running
docker version

# Check container status
docker-compose ps

# View detailed logs
docker-compose logs app
```

### Port Already in Use
```bash
# Stop all containers
docker-compose down

# Or change port in docker-compose.yml
ports:
  - "8001:8000"  # Use port 8001 instead
```

### Code Changes Not Reflecting
```bash
# Make sure you're using dev mode
docker-compose -f docker-compose.dev.yml up --build

# Or force recreate
docker-compose down && docker-compose -f docker-compose.dev.yml up --build
```