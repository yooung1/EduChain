from fastapi import APIRouter, status, Depends
from app.klass.schemas import KlassSchemaPublic, KlassSchemaPost
from app.auth.service import CheckRole
from app.user.service import UserRole
from typing import Annotated, List
from sqlmodel import Session, select
from app.db.database import get_db
from app.klass.models import Klass
from app.klass.service import create_new_klass
from app.klass.exceptions import KlassDoesNotExist


klass_router = APIRouter(prefix="/klass", tags=["Klass"])
db = Annotated[Session, Depends(get_db)]


@klass_router.get("/", status_code=status.HTTP_202_ACCEPTED, response_model=List[KlassSchemaPublic])
def get_klasses(db: db,  allowed_rolles: UserRole = Depends(CheckRole([UserRole.ADMIN, UserRole.TEACHER]))) -> Session:
    statement = select(Klass)
    return db.exec(statement).all()


@klass_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=KlassSchemaPublic)
def create_klass(klass: KlassSchemaPost, db: db, allowed_rolles: UserRole = Depends(CheckRole([UserRole.ADMIN, UserRole.TEACHER]))):
    return create_new_klass(db=db, new_klass=klass)



@klass_router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_klass(db: db, id: int, allowed_roles: UserRole = Depends(CheckRole([UserRole.ADMIN, UserRole.TEACHER]))):
    klass = db.get(Klass, id)
    
    if not klass:
        raise KlassDoesNotExist
    
    db.delete(klass)
    db.commit()

    return None