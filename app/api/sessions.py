from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.sessions import SessionLocal
from app.models.sessions import Session as SessionModel
from app.schemas.session_schema import SessionCreate, SessionUpdate, SessionResponse
from app.models.users import User
from app.core.auth import get_current_user

router = APIRouter()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get the current authenticated user
def get_user_from_token(current_user: User = Depends(get_current_user)):
    return current_user

# Create Session
@router.post("/sessions", response_model=SessionResponse)
def create_session(
    session: SessionCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_user_from_token)
):
    if current_user.role != "coach":
        raise HTTPException(status_code=403, detail="Only coaches can create sessions")
    
    new_session = SessionModel(
        coach_id=current_user.id,
        coachee_id=session.coachee_id,
        topic=session.topic,
        location=session.location,
        capacity=session.capacity,
        time=session.time,
        status=session.status
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session

@router.put("/sessions/{session_id}", response_model=SessionResponse)
def update_session(
    session_id: int,
    session: SessionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_user_from_token)
):
    # Ensure only coaches can update sessions
    if current_user.role != "coach":
        raise HTTPException(status_code=403, detail="Only coaches can update sessions")

    existing_session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not existing_session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Update the session fields
    if session.topic:
        existing_session.topic = session.topic
    if session.location:
        existing_session.location = session.location
    if session.capacity:
        existing_session.capacity = session.capacity
    if session.time:
        existing_session.time = session.time
    if session.status:
        existing_session.status = session.status

    db.commit()
    db.refresh(existing_session)

    return existing_session

@router.get("/sessions/{session_id}", response_model=SessionResponse)
def get_session(session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Make sure the user is authorized to view the session
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session

@router.delete("/sessions/{session_id}", status_code=204)
def delete_session(session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_user_from_token)):
    # Ensure the user is authorized to delete the session (e.g., only coach can delete)
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    # Ensure the current user is the coach of this session or authorized to delete it
    if current_user.role != "coach" or session.coach_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this session")

    db.delete(session)
    db.commit()

    return {"message": "Session deleted successfully"}

@router.post("/session-requests", response_model=SessionResponse)
def request_session(
    session_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_user_from_token)
):
    if current_user.role != "coachee":
        raise HTTPException(status_code=403, detail="Only coachees can request sessions")

    # Find the session
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Update the session status to 'requested'
    session.status = "requested"
    db.commit()
    db.refresh(session)

    return session

# 2. Approve session request (by coach)
@router.post("/session-requests/{session_id}/approve", response_model=SessionResponse)
def approve_session(
    session_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_user_from_token)
):
    if current_user.role != "coach":
        raise HTTPException(status_code=403, detail="Only coaches can approve sessions")

    # Find the session
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.status != "requested":
        raise HTTPException(status_code=400, detail="Session is not in 'requested' status")

    # Approve the session
    session.status = "approved"
    db.commit()
    db.refresh(session)

    return session

# 3. Reject session request (by coach)
@router.post("/session-requests/{session_id}/reject", response_model=SessionResponse)
def reject_session(
    session_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_user_from_token)
):
    if current_user.role != "coach":
        raise HTTPException(status_code=403, detail="Only coaches can reject sessions")

    # Find the session
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.status != "requested":
        raise HTTPException(status_code=400, detail="Session is not in 'requested' status")

    # Reject the session
    session.status = "rejected"
    db.commit()
    db.refresh(session)

    return session

# 4. Get session status
@router.get("/session-requests/{session_id}/status", response_model=SessionResponse)
def get_session_status(
    session_id: int, 
    db: Session = Depends(get_db),
):
    # Find the session
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return session
