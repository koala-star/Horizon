# Horizon — un espace scolaire plus clair

Horizon est une alternative d’interface pour les données accessibles depuis Pronote. Elle ne contourne aucun mécanisme de protection et n’affiche jamais de données inventées : lorsqu’une donnée n’est pas disponible, l’interface l’indique.

## Démarrage

### API
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Interface
```powershell
cd frontend
npm install
npm run dev
```

Les statuts personnels des devoirs sont stockés localement dans SQLite, dans le dossier de données de l’application (`%LOCALAPPDATA%/Horizon` sous Windows).
