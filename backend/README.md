# Horizon API

L’API peut être lancée localement avec `uvicorn app.main:app --reload --port 8000`.
Pour une utilisation depuis GitHub Pages ou un iPhone, elle doit être déployée sur une URL HTTPS publique, puis fournie au frontend via `VITE_API_URL` (par exemple `https://mon-api.example.com/api`).
