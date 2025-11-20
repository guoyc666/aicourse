from database import SessionLocal
from models import LearningRecord, KnowledgeResourceLink

def calc_progress(student_id, knowledge_id):
    db = SessionLocal()
    links = db.query(KnowledgeResourceLink).filter(
        KnowledgeResourceLink.knowledge_id == knowledge_id
    ).all()
    resource_ids = [link.resource_id for link in links]
    if not resource_ids:
        db.close()
        return 0, 0
    records = db.query(LearningRecord).filter(
        LearningRecord.student_id == student_id,
        LearningRecord.resource_id.in_(resource_ids)
    ).all()
    finished_resource_ids = set()
    for r in records:
        if r.status == 1:
            finished_resource_ids.add(r.resource_id)
    finished_count = len(finished_resource_ids)
    db.close()
    return len(resource_ids), finished_count

def calc_average_progress(knowledge_id):
    db = SessionLocal()
    links = db.query(KnowledgeResourceLink).filter(
        KnowledgeResourceLink.knowledge_id == knowledge_id
    ).all()
    resource_ids = [link.resource_id for link in links]
    if not resource_ids:
        db.close()
        return 0
    student_ids = db.query(LearningRecord.student_id).distinct().all()
    student_ids = [sid[0] for sid in student_ids]
    total_progress = 0
    for student_id in student_ids:
        total_count, finished_count = calc_progress(student_id, knowledge_id)
        progress = finished_count / total_count if total_count > 0 else 0
        total_progress += progress
    average_progress = total_progress / len(student_ids) if student_ids else 0
    db.close()
    return int(average_progress * 100)