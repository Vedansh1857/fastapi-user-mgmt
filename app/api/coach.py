from app.schemas.coach_profile import CoachProfileCreate, CoachProfileUpdate, CoachProfileResponse
from app.models.coach_profile import CoachProfile
from fastapi import APIRouter, Depends, Query
from app.dependency.auth import role_required
from app.schemas.user_schema import UserResponse
from app.db.sessions import SessionLocal
from app.models.users import User
from app.core.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/coach-dashboard", response_model=UserResponse)
def get_coach_dashboard(user: UserResponse = Depends(role_required("coach"))):
    return user  # Return coach data

# Dependency to get the current authenticated user
def get_user_from_token(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/coach-profile", response_model=CoachProfileResponse)
def create_coach_profile(
    profile: CoachProfileCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_user_from_token)
):
    # Ensure the current user has the 'coach' role
    if current_user.role != "coach":
        raise HTTPException(status_code=403, detail="Only coaches can create a profile")

    # Check if the coach profile already exists
    existing_profile = db.query(CoachProfile).filter(CoachProfile.user_id == current_user.id).first()
    if existing_profile:
        raise HTTPException(status_code=400, detail="Coach profile already exists")
    
    # Create new coach profile
    new_profile = CoachProfile(
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

@router.put("/coach-profile", response_model=CoachProfileResponse)
def update_coach_profile(
    profile: CoachProfileUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_user_from_token)
):
    # Ensure the current user has the 'coach' role
    if current_user.role != "coach":
        raise HTTPException(status_code=403, detail="Only coaches can update their profile")
    
    # Check if the coach profile exists
    existing_profile = db.query(CoachProfile).filter(CoachProfile.user_id == current_user.id).first()
    if not existing_profile:
        raise HTTPException(status_code=404, detail="Coach profile not found")
    
    # Update the fields of the coach profile
    existing_profile.bio = profile.bio if profile.bio is not None else existing_profile.bio
    existing_profile.expertise = profile.expertise if profile.expertise is not None else existing_profile.expertise
    existing_profile.location = profile.location if profile.location is not None else existing_profile.location
    existing_profile.availability = profile.availability if profile.availability is not None else existing_profile.availability
    existing_profile.image_url = profile.image_url if profile.image_url is not None else existing_profile.image_url

    db.commit()
    db.refresh(existing_profile)

    return existing_profile

# 3. Get Coach Profile
@router.get("/coach-profile", response_model=CoachProfileResponse)
def get_coach_profile(db: Session = Depends(get_db), current_user: User = Depends(get_user_from_token)):
    if current_user.role != "coach":
        raise HTTPException(status_code=403, detail="Only coaches can view their profile")
    
    profile = db.query(CoachProfile).filter(CoachProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Coach profile not found")
    
    return profile

# 4. Delete Coach Profile
@router.delete("/coach-profile", status_code=204)
def delete_coach_profile(db: Session = Depends(get_db), current_user: User = Depends(get_user_from_token)):
    if current_user.role != "coach":
        raise HTTPException(status_code=403, detail="Only coaches can delete their profile")
    
    profile = db.query(CoachProfile).filter(CoachProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Coach profile not found")
    
    db.delete(profile)
    db.commit()

    return {"message": "Profile deleted successfully"}

# Search/Filter Coaches
@router.get("/search-coaches", response_model=list[CoachProfileResponse])
def search_coaches(
    expertise: str = Query(None, alias="expertise"),
    availability: str = Query(None, alias="availability"),
    location: str = Query(None, alias="location"),
    db: Session = Depends(get_db)
):
    query = db.query(CoachProfile)

    if expertise:
        query = query.filter(CoachProfile.expertise.ilike(f"%{expertise}%"))
    
    if availability:
        query = query.filter(CoachProfile.availability == availability)
    
    if location:
        query = query.filter(CoachProfile.location.ilike(f"%{location}%"))

    coaches = query.all()
    
    return coaches
