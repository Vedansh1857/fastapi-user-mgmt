from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.sessions import SessionLocal
from app.schemas.coachee_profile import CoacheeProfileCreate, CoacheeProfileUpdate, CoacheeProfileResponse
from app.models.coachee_profile import CoacheeProfile
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

@router.post("/coachee-profile", response_model=CoacheeProfileResponse)
def create_coachee_profile(
    profile: CoacheeProfileCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_user_from_token)
):
    # Ensure the current user has the 'coachee' role
    if current_user.role != "coachee":
        raise HTTPException(status_code=403, detail="Only coachees can create a profile")

    # Check if the coachee profile already exists
    existing_profile = db.query(CoacheeProfile).filter(CoacheeProfile.user_id == current_user.id).first()
    if existing_profile:
        raise HTTPException(status_code=400, detail="Coachee profile already exists")
    
    # Create new coachee profile
    new_profile = CoacheeProfile(
        user_id=current_user.id,
        bio=profile.bio,
        expertise=profile.expertise,
        location=profile.location,
        availability=profile.availability,
        image_url=profile.image_url
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile

@router.put("/coachee-profile", response_model=CoacheeProfileResponse)
def update_coachee_profile(
    profile: CoacheeProfileUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_user_from_token)
):
    # Ensure the current user has the 'coachee' role
    if current_user.role != "coachee":
        raise HTTPException(status_code=403, detail="Only coachees can update their profile")
    
    # Check if the coachee profile exists
    existing_profile = db.query(CoacheeProfile).filter(CoacheeProfile.user_id == current_user.id).first()
    if not existing_profile:
        raise HTTPException(status_code=404, detail="Coachee profile not found")
    
    # Update the fields of the coachee profile
    existing_profile.bio = profile.bio if profile.bio is not None else existing_profile.bio
    existing_profile.expertise = profile.expertise if profile.expertise is not None else existing_profile.expertise
    existing_profile.location = profile.location if profile.location is not None else existing_profile.location
    existing_profile.availability = profile.availability if profile.availability is not None else existing_profile.availability
    existing_profile.image_url = profile.image_url if profile.image_url is not None else existing_profile.image_url

    db.commit()
    db.refresh(existing_profile)

    return existing_profile
