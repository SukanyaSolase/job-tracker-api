from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.application import Application
from app.models.user import User
from app.schemas.application import ApplicationCreate, ApplicationOut, ApplicationUpdate

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("", response_model=ApplicationOut, status_code=201)
def create_application(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    app_obj = Application(
        user_id=current_user.id,
        company=payload.company,
        role=payload.role,
        status=payload.status.value,
        link=str(payload.link) if payload.link else None,
        notes=payload.notes,
    )
    db.add(app_obj)
    db.commit()
    db.refresh(app_obj)
    return app_obj


@router.get("", response_model=list[ApplicationOut])
def list_applications(
    status: str | None = None,
    company: str | None = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(Application).filter(Application.user_id == current_user.id)

    if status:
        q = q.filter(Application.status == status)
    if company:
        q = q.filter(Application.company.ilike(f"%{company}%"))

    apps = q.order_by(Application.created_at.desc()).limit(limit).offset(offset).all()
    return apps


@router.get("/{app_id}", response_model=ApplicationOut)
def get_application(
    app_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    app_obj = (
        db.query(Application)
        .filter(Application.id == app_id, Application.user_id == current_user.id)
        .first()
    )
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    return app_obj


@router.put("/{app_id}", response_model=ApplicationOut)
def update_application(
    app_id: int,
    payload: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    app_obj = (
        db.query(Application)
        .filter(Application.id == app_id, Application.user_id == current_user.id)
        .first()
    )
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")

    if payload.company is not None:
        app_obj.company = payload.company
    if payload.role is not None:
        app_obj.role = payload.role
    if payload.status is not None:
        app_obj.status = payload.status.value
    if payload.link is not None:
        app_obj.link = str(payload.link)
    if payload.notes is not None:
        app_obj.notes = payload.notes

    db.commit()
    db.refresh(app_obj)
    return app_obj


@router.delete("/{app_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    app_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    app_obj = (
        db.query(Application)
        .filter(Application.id == app_id, Application.user_id == current_user.id)
        .first()
    )
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(app_obj)
    db.commit()
    return None