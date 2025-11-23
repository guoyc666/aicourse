from database import SessionLocal
from models import LearningRecord
import json
from datetime import datetime, timedelta

def create_learning_record(record):
    db = SessionLocal()
    obj = LearningRecord(
        student_id=record.student_id,
        resource_id=record.resource_id,
        status=record.status,
        total_time=record.total_time,
        page_times=json.dumps(record.page_times),
        timestamp=record.timestamp
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    db.close()
    return obj

def create_learning_records_batch(records):
    db = SessionLocal()
    objs = []
    for rec in records:
        obj = LearningRecord(
            student_id=rec.student_id,
            resource_id=rec.resource_id,
            status=rec.status,
            total_time=rec.total_time,
            page_times=json.dumps(rec.page_times),
            timestamp=rec.timestamp
        )
        db.add(obj)
        objs.append(obj)
    db.commit()
    for obj in objs:
        db.refresh(obj)
    db.close()
    return objs

def get_learning_records_by_student(student_id):
    db = SessionLocal()
    records = db.query(LearningRecord).filter(LearningRecord.student_id == student_id).all()
    db.close()
    # 反序列化 page_times
    for r in records:
        r.page_times = json.loads(r.page_times) if r.page_times else []
    return records

def get_all_learning_records():
    db = SessionLocal()
    records = db.query(LearningRecord).all()
    db.close()
    # 反序列化 page_times
    for r in records:
        r.page_times = json.loads(r.page_times) if r.page_times else []
    return records

def get_learning_records_by_date(date_str):
    db = SessionLocal()
    start = datetime.fromisoformat(date_str)
    end = start + timedelta(days=1)
    records = db.query(LearningRecord).filter(
        LearningRecord.timestamp >= start,
        LearningRecord.timestamp < end
    ).all()
    db.close()
    for r in records:
        r.page_times = json.loads(r.page_times) if r.page_times else []
    return records

def get_learning_records_by_date_and_student(date_str, student_id):
    db = SessionLocal()
    start = datetime.fromisoformat(date_str)
    end = start + timedelta(days=1)
    records = db.query(LearningRecord).filter(
        LearningRecord.student_id == student_id,
        LearningRecord.timestamp >= start,
        LearningRecord.timestamp < end
    ).all()
    db.close()
    for r in records:
        r.page_times = json.loads(r.page_times) if r.page_times else []
    return records

def delete_learning_records_by_year(year):
    db = SessionLocal()
    start = datetime(year, 1, 1)
    end = datetime(year + 1, 1, 1)
    db.query(LearningRecord).filter(
        LearningRecord.timestamp >= start,
        LearningRecord.timestamp < end
    ).delete(synchronize_session=False)
    db.commit()
    db.close()

def delete_learning_records_by_year_and_student(year, student_id):
    db = SessionLocal()
    start = datetime(year, 1, 1)
    end = datetime(year + 1, 1, 1)
    db.query(LearningRecord).filter(
        LearningRecord.student_id == student_id,
        LearningRecord.timestamp >= start,
        LearningRecord.timestamp < end
    ).delete(synchronize_session=False)
    db.commit()
    db.close()

def delete_learning_records_by_date(date_str):
    db = SessionLocal()
    start = datetime.fromisoformat(date_str)
    end = start + timedelta(days=1)
    db.query(LearningRecord).filter(
        LearningRecord.timestamp >= start,
        LearningRecord.timestamp < end
    ).delete(synchronize_session=False)
    db.commit()
    db.close()

def delete_learning_records_by_date_and_student(date_str, student_id):
    db = SessionLocal()
    start = datetime.fromisoformat(date_str)
    end = start + timedelta(days=1)
    db.query(LearningRecord).filter(
        LearningRecord.student_id == student_id,
        LearningRecord.timestamp >= start,
        LearningRecord.timestamp < end
    ).delete(synchronize_session=False)
    db.commit()
    db.close()