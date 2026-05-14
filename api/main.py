from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

# --- Config ---
SECRET_KEY = "supersecretkey123"  # Change in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI(title="J.A.K.E API", version="0.2.0")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Fake user DB (replace with real DB later)
fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "hashed_password": pwd_context.hash("admin123"),
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class QueryRequest(BaseModel):
    question: str

class ReportRequest(BaseModel):
    focus_areas: list = None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401)
        return username
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/query")
async def query_knowledge(request: QueryRequest, user=Depends(get_current_user)):
    from core.query import JAKEQuery
    result = JAKEQuery().ask(request.question, use_vector=True)
    return {"user": user, "answer": result}

@app.post("/report")
async def generate_report(request: ReportRequest, user=Depends(get_current_user)):
    from core.intelligence_report import IntelligenceReport
    report = IntelligenceReport().generate_daily_report(request.focus_areas)
    return {"user": user, "report": report}

@app.get("/health")
async def health_check(user=Depends(get_current_user)):
    return {"status": "healthy", "user": user, "timestamp": datetime.utcnow()}