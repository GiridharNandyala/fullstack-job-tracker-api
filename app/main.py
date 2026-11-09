from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app import models, schemas, database, auth

# Initialize FastAPI app
app = FastAPI(title="Job Tracker API", version="2.0")

# Enable CORS for Frontend (React.js / Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # మీరు కావాలంటే నిర్దిష్టమైన URL కూడా పెట్టుకోవచ్చు ఉదా: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper to get current authenticated user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user


# --- USER AUTHENTICATION ENDPOINTS ---

@app.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# --- JOB MANAGEMENT ENDPOINTS (CRUD & BULK & FILTER) ---

# 1. Create Single Job
@app.post("/jobs", response_model=schemas.JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_job = models.Job(**job.dict(), user_id=current_user.id)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job


# 2. Create Multiple Jobs (Bulk Insert)
@app.post("/jobs/bulk", response_model=List[schemas.JobResponse], status_code=status.HTTP_201_CREATED)
def create_multiple_jobs(jobs: List[schemas.JobCreate], db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    created_jobs = []
    for job_data in jobs:
        new_job = models.Job(**job_data.dict(), user_id=current_user.id)
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
        created_jobs.append(new_job)
    return created_jobs


# 3. Get All Jobs (with optional Status Filter)
@app.get("/jobs", response_model=List[schemas.JobResponse])
def get_jobs(status: Optional[str] = Query(None, description="Filter jobs by status (e.g., Applied, Interviewing, Offered, Rejected)"), db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    query = db.query(models.Job).filter(models.Job.user_id == current_user.id)
    if status:
        query = query.filter(models.Job.status == status)
    return query.all()


# 4. Update Job (PUT)
@app.put("/jobs/{job_id}", response_model=schemas.JobResponse)
def update_job(job_id: int, updated_job: schemas.JobUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    job_query = db.query(models.Job).filter(models.Job.id == job_id, models.Job.user_id == current_user.id)
    job = job_query.first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found or not authorized to update")
    
    update_data = updated_job.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(job, key, value)
        
    db.commit()
    db.refresh(job)
    return job


# 5. Delete Job (DELETE)
@app.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    job_query = db.query(models.Job).filter(models.Job.id == job_id, models.Job.user_id == current_user.id)
    job = job_query.first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found or not authorized to delete")
    
    db.delete(job)
    db.commit()
    return None