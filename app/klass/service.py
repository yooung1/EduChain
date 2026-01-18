from app.klass.schemas import KlassSchemaPost
from sqlmodel import Session
from app.klass.models import Klass
from typing import List

def create_new_klass(db: Session, new_klass: List[KlassSchemaPost]):
    new_klasses_models = [Klass(**item.model_dump()) for item in new_klass]

    db.add_all(new_klasses_models)

    db.commit()

    for k in new_klasses_models:
        db.refresh(k)

    return new_klasses_models