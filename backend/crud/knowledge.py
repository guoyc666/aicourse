from database import SessionLocal
from models import KnowledgePoint

def create_knowledge_point(id, name, category):
    db = SessionLocal()
    kp = KnowledgePoint(id=id, name=name, category=category)
    db.add(kp)
    db.commit()
    db.close()
    return kp

def get_knowledge_point(id):
    db = SessionLocal()
    kp = db.query(KnowledgePoint).filter(KnowledgePoint.id == id).first()
    db.close()
    return kp

def list_knowledge_points():
    db = SessionLocal()
    points = db.query(KnowledgePoint).all()
    db.close()
    return points

def delete_knowledge_point(id):
    db = SessionLocal()
    kp = db.query(KnowledgePoint).filter(KnowledgePoint.id == id).first()
    if kp:
        db.delete(kp)
        db.commit()
    db.close()