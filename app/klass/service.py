from app.klass.schemas import KlassSchemaPost
from sqlmodel import Session
from app.klass.models import Klass

def create_new_klass(db: Session, new_klass: KlassSchemaPost):
    new_klass = Klass(
        name=new_klass.name,
        video=new_klass.video,
        description=new_klass.description,
        course_id=new_klass.course_id
    )


    db.add(new_klass)
    db.commit()
    db.refresh(new_klass)

    return new_klass