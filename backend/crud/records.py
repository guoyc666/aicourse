from database import SessionLocal
from models import LearningRecord
import json
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from crud.graph import get_all_knowledge_points, get_resources_by_knowledge, get_all_students

def create_learning_record(db: Session, record):
    obj = LearningRecord(
        student_id=record.student_id,
        resource_id=record.resource_id,
        status=record.status,
        total_time=record.total_time,
        page_times=json.dumps(record.page_times),
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def create_learning_records_batch(db: Session, records):
    objs = []
    for rec in records:
        obj = LearningRecord(
            student_id=rec.student_id,
            resource_id=rec.resource_id,
            status=rec.status,
            total_time=rec.total_time,
            page_times=json.dumps(rec.page_times),
        )
        db.add(obj)
        objs.append(obj)
    db.commit()
    for obj in objs:
        db.refresh(obj)
    return objs

def get_learning_records_by_student(db: Session, student_id):
    records = db.query(LearningRecord).filter(LearningRecord.student_id == student_id).all()
    # 反序列化 page_times
    for r in records:
        r.page_times = json.loads(r.page_times) if r.page_times else []
    return records

def get_all_learning_records(db: Session,):
    records = db.query(LearningRecord).all()
    # 反序列化 page_times
    for r in records:
        r.page_times = json.loads(r.page_times) if r.page_times else []
    return records

def get_learning_records_by_date(db: Session, date_str):
    start = datetime.fromisoformat(date_str)
    end = start + timedelta(days=1)
    records = db.query(LearningRecord).filter(
        LearningRecord.timestamp >= start,
        LearningRecord.timestamp < end
    ).all()
    for r in records:
        r.page_times = json.loads(r.page_times) if r.page_times else []
    return records

def get_learning_records_by_date_and_student(db: Session, date_str, student_id):
    start = datetime.fromisoformat(date_str)
    end = start + timedelta(days=1)
    records = db.query(LearningRecord).filter(
        LearningRecord.student_id == student_id,
        LearningRecord.timestamp >= start,
        LearningRecord.timestamp < end
    ).all()
    for r in records:
        r.page_times = json.loads(r.page_times) if r.page_times else []
    return records

def delete_learning_records_by_year(db: Session, year):
    start = datetime(year, 1, 1)
    end = datetime(year + 1, 1, 1)
    db.query(LearningRecord).filter(
        LearningRecord.timestamp >= start,
        LearningRecord.timestamp < end
    ).delete(synchronize_session=False)
    db.commit()

def delete_learning_records_by_year_and_student(db: Session, year, student_id):
    start = datetime(year, 1, 1)
    end = datetime(year + 1, 1, 1)
    db.query(LearningRecord).filter(
        LearningRecord.student_id == student_id,
        LearningRecord.timestamp >= start,
        LearningRecord.timestamp < end
    ).delete(synchronize_session=False)
    db.commit()

def delete_learning_records_by_date(db: Session, date_str):
    start = datetime.fromisoformat(date_str)
    end = start + timedelta(days=1)
    db.query(LearningRecord).filter(
        LearningRecord.timestamp >= start,
        LearningRecord.timestamp < end
    ).delete(synchronize_session=False)
    db.commit()

def delete_learning_records_by_date_and_student(db: Session, date_str, student_id):
    start = datetime.fromisoformat(date_str)
    end = start + timedelta(days=1)
    db.query(LearningRecord).filter(
        LearningRecord.student_id == student_id,
        LearningRecord.timestamp >= start,
        LearningRecord.timestamp < end
    ).delete(synchronize_session=False)
    db.commit()

def delete_learning_records_by_resource(db: Session, resource_id: str):
    db.query(LearningRecord).filter(LearningRecord.resource_id == resource_id).delete(synchronize_session=False)
    db.commit()


def get_study_time(db: Session, student_id: int, knowledge_id: str):
    resource_ids = get_resources_by_knowledge(knowledge_id)
    if not resource_ids:
        return {
            "knowledge_id": knowledge_id,
            "student_id": student_id,
            "study_time": 0
        }
    records = db.query(LearningRecord).filter(
        LearningRecord.student_id == student_id,
        LearningRecord.resource_id.in_(resource_ids)
    ).all()
    total_time = sum(r.total_time for r in records)
    return {
        "knowledge_id": knowledge_id,
        "student_id": student_id,
        "study_time": total_time
    }

def list_study_time(db: Session, student_id: int):
    all_knowledge_points = get_all_knowledge_points()
    result = []
    for kp_id in all_knowledge_points:
        info = get_study_time(db, student_id, kp_id)
        result.append(info)
    return result

def get_study_time_list(db: Session, knowledge_id: str):
    students = get_all_students(db)
    result = []
    for s in students:
        info = get_study_time(db, s.id, knowledge_id)
        result.append({
            "knowledge_id": knowledge_id,
            "study_time": info["study_time"],
            "student_id": s.id,
            "student_name": s.full_name
        })
    return result

def list_study_time_list(db: Session):
    all_knowledge_points = get_all_knowledge_points()
    students = get_all_students(db)
    result = []
    for kp_id in all_knowledge_points:
        for s in students:
            info = get_study_time(db, s.id, kp_id)
            result.append({
                "knowledge_id": kp_id,
                "study_time": info["study_time"],
                "student_id": s.id,
                "student_name": s.full_name
            })
    return result

def get_average_study_time(db: Session, knowledge_id: str):
    students = get_all_students(db)
    student_ids = [s.id for s in students]
    total_time = 0
    for student_id in student_ids:
        info = get_study_time(db, student_id, knowledge_id)
        total_time += info["study_time"]
    average_time = total_time / len(student_ids) if student_ids else 0
    return {
        "knowledge_id": knowledge_id,
        "average_study_time": average_time
    }

def list_average_study_time(db: Session):
    all_knowledge_points = get_all_knowledge_points()
    result = []
    for kp_id in all_knowledge_points:
        avg_info = get_average_study_time(db, kp_id)
        result.append(avg_info)
    return result