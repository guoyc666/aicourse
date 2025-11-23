from models import Resource
from database import SessionLocal

def get_resource_by_id(resource_id: str):
    db = SessionLocal()
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    db.close()
    return resource