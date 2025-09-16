## Backend API — Quick Local Run

This guide helps you get the backend running locally for frontend development

---

### Prerequisites

- **Python**: 3.11+

---

### 1. Clone & Navigate

Open a terminal in the project root (where you cloned the repo):

```bash
cd path/to/your/cloned/repo
```

---

### 2. Create Virtual Environment & Install Dependencies

Windows (PowerShell):

```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Linux / macOS:

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

If `requirements.txt` is incomplete, install the basics manually:

```bash
pip install fastapi "uvicorn[standard]"
```

---

### 3. Configure Environment Variables

Create a `.env` file in the `backend/` folder with at least these values:

```env
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/dbname
SECRET_KEY=dev-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

### 4. Run the API (with Hot Reload)

Windows (PowerShell):

```powershell
uvicorn app.main:app --reload
```

Linux / macOS:

```bash
uvicorn app.main:app --reload
```

---

### 5. Verify It Works

- Swagger UI → http://localhost:8000/docs
- ReDoc → http://localhost:8000/redoc
- Health Check → http://localhost:8000/health
