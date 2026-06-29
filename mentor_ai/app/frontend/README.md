# Frontend (placeholder)

Phase 1 includes a placeholder frontend. The real frontend will be a React app inside Electron or Tauri and will consume the backend `/chat` endpoint.

Development note:

```powershell
# Example: query the backend
curl -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d '{"message":"hello"}'
```

Frontend app (Vite + React) is available at `app/frontend/react-app`.

To run the frontend:

```powershell
cd app/frontend/react-app
npm install
npm run dev
```

