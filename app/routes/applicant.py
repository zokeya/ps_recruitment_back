from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app import schemas, database, models, oauth2

router = APIRouter(
    tags=["Applicant"]
)


@router.post('/applicant', status_code=status.HTTP_201_CREATED)
async def create_or_update_applicant(
        applicant: schemas.ApplicantBase,
        db: Session = Depends(database.get_db),
        login_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        existing_applicant = db.query(models.Applicant).filter(models.Applicant.user_id == login_user.id).first()

        if existing_applicant:
            for field, value in applicant.dict().items():
                if field not in ["qualifications", "skills"]:
                    setattr(existing_applicant, field, value)
            if applicant.qualifications:
                existing_applicant.qualifications.clear()
                existing_applicant.qualifications = [
                    models.Qualification(**qual.dict(), applicant_id=existing_applicant.id) for qual in applicant.qualifications
                ]
            if applicant.skills:
                existing_applicant.skills.clear()
                existing_applicant.skills = [
                    models.Skill(**skill.dict(), applicant_id=existing_applicant.id) for skill in applicant.skills
                ]
            db.commit()
            db.refresh(existing_applicant)
            return existing_applicant
        else:
            # Create a new applicant
            new_applicant = models.Applicant(user_id=login_user.id, **applicant.dict(exclude={"qualifications", "skills"}))
            if applicant.qualifications:
                new_applicant.qualifications = [
                    models.Qualification(**qual.dict(), applicant_id=new_applicant.id) for qual in applicant.qualifications
                ]
            if applicant.skills:
                new_applicant.skills = [
                    models.Skill(**skill.dict(), applicant_id=new_applicant.id) for skill in applicant.skills
                ]
            db.add(new_applicant)
            db.commit()
            db.refresh(new_applicant)
            return new_applicant

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/applicants', response_model=list[schemas.Applicant])
async def get_applicants(db: Session = Depends(database.get_db), skip: int = 0, limit: int = 100):
    applicants = db.query(models.Applicant).offset(skip).limit(limit).all()
    return applicants
