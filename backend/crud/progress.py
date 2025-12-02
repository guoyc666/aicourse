from models import LearningRecord
from crud.graph import get_all_knowledge_points, get_resources_by_knowledge, get_all_students
from sqlalchemy.orm import Session

def get_progress(db: Session, student_id: int, knowledge_id: str):
    resource_ids = get_resources_by_knowledge(knowledge_id)
    if not resource_ids:
        return {
            "knowledge_id": knowledge_id,
            "progress": 0.0
        }
    records = db.query(LearningRecord).filter(
        LearningRecord.student_id == student_id,
        LearningRecord.resource_id.in_(resource_ids)
    ).all()
    finished_resource_ids = set()
    for r in records:
        if r.status == 1:
            finished_resource_ids.add(r.resource_id)
    finished_count = len(finished_resource_ids)
    progress = finished_count / len(resource_ids)
    return {
        "knowledge_id": knowledge_id,
        "progress": progress
    }

def list_progress(db: Session, student_id: int):
    all_knowledge_points = get_all_knowledge_points()
    progress_list = []
    for kp_id in all_knowledge_points:
        progress_info = get_progress(db, student_id, kp_id)
        progress_list.append(progress_info)
    return progress_list

def get_progress_list(db: Session, knowledge_id: str):
    students = get_all_students(db)
    result = []
    for s in students:
        progress_info = get_progress(db, s.id, knowledge_id)
        result.append({
            "knowledge_id": knowledge_id,
            "progress": progress_info["progress"],
            "student_id": s.id,
            "student_name": s.full_name
        })
    return result

def list_progress_list(db: Session):
    all_knowledge_points = get_all_knowledge_points()
    students = get_all_students(db)
    result = []
    for kp_id in all_knowledge_points:
        for s in students:
            progress_info = get_progress(db, s.id, kp_id)
            result.append({
                "knowledge_id": kp_id,
                "progress": progress_info["progress"],
                "student_id": s.id,
                "student_name": s.full_name
            })
    return result

def get_average_progress(db: Session, knowledge_id: str):
    students = get_all_students(db)
    student_ids = [s.id for s in students]
    total_progress = 0.0
    for student_id in student_ids:
        progress_info = get_progress(db, student_id, knowledge_id)
        total_progress += progress_info["progress"]
    average_progress = total_progress / len(student_ids) if student_ids else 0.0
    return {
        "knowledge_id": knowledge_id,
        "average_progress": average_progress
    }

def list_average_progress(db: Session):
    all_knowledge_points = get_all_knowledge_points()
    result = []
    for kp_id in all_knowledge_points:
        avg_progress_info = get_average_progress(db, kp_id)
        result.append(avg_progress_info)
    return result