# Port Architecture

## Understanding Haven's Port Configuration

### Service Ports (Internal)
- **Frontend (Vite)**: Port 3000
- **Backend API**: Port 8080
- **PostgreSQL**: Port 5432

### Proxy Ports (External Access)
- **Option 1 - Port 9000** (no sudo): `just run-proxy`
  - Access via: http://haven.local:9000
- **Option 2 - Port 80** (requires sudo): `just start-proxy`
  - Access via: http://haven.local (no port needed)

## How It Works

```
User Browser
     |
     v
Caddy Proxy (port 80 or 9000)
     |
     +---> Routes *.haven.local to Frontend (localhost:3000)
     |
     +---> Routes api.haven.local to Backend (localhost:8080)
```

## Important Notes

1. **Port 3000 is correct** - This is the internal port where the frontend dev server runs
2. **You should NOT access port 3000 directly** - Always use the proxy
3. **http://haven.local:3000 bypasses the proxy** - This is why it works but isn't the intended usage

## Correct URLs

### With `just start-proxy` (Port 80):
- http://haven.local
- http://web.haven.local
- http://api.haven.local
- http://api.haven.local/docs

### With `just run-proxy` (Port 9000):
- http://haven.local:9000
- http://web.haven.local:9000
- http://api.haven.local:9000
- http://api.haven.local/docs

### Direct Access (Development Only):
- http://localhost:3000 - Frontend directly
- http://localhost:8080 - Backend directly

## Troubleshooting

If http://haven.local isn't working but http://haven.local:3000 is:
1. The proxy isn't running on port 80
2. Run `just start-proxy` and enter your sudo password
3. If port 80 is blocked, check with: `sudo lsof -i :80`