import math
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_active_user,verify_permission, check_role
from models import FileResource, User
from schemas_.records import AverageStudyTimeOut, LearningRecordCreate, StudyTimeOut, StudyTimeListOut
from datetime import datetime, date, timedelta
from crud.records import (
    create_learning_record,
    create_learning_records_batch,
    get_learning_records_by_student,
    get_all_learning_records,
    get_learning_records_by_date,
    get_learning_records_by_date_and_student,
    delete_learning_records_by_year,
    delete_learning_records_by_year_and_student,
    delete_learning_records_by_date,
    delete_learning_records_by_date_and_student,
    get_study_time,
    list_study_time,
    get_study_time_list,
    list_study_time_list,
    get_average_study_time,
    list_average_study_time,
)

router = APIRouter()

@router.post("/records/")
def add_record(rec: LearningRecordCreate, db: Session = Depends(get_db)):
    obj = create_learning_record(db, rec)
    return {"success": True, "id": obj.id}

@router.post("/records/batch")
def add_records_batch(records: list[LearningRecordCreate], db: Session = Depends(get_db)):
    objs = create_learning_records_batch(db, records)
    return {"success": True, "ids": [obj.id for obj in objs]}

@router.get("/records/detail/{date}")
def get_all_students_daily_records(
    date: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    records = get_learning_records_by_date(db, date)
    result = {}
    # 按学生分组
    from collections import defaultdict
    student_events = defaultdict(list)
    for r in records:
        student_events[r.student_id].append(r)
    # 对每个学生的事件按时间排序，并id递增
    for student_id, events in student_events.items():
        events = sorted(events, key=lambda r: r.timestamp)
        result[student_id] = []
        for idx, r in enumerate(events, start=1):
            resource = db.query(FileResource).filter(FileResource.file_id == r.resource_id).first()
            resource_name = resource.title if resource else "未知资源"
            dt = r.timestamp
            time_str = dt.strftime("%H:%M:%S")
            result[student_id].append({
                "id": idx,  # 从1开始递增
                "resource_id": r.resource_id,
                "resource_name": resource_name,
                "time": time_str,
                "duration": math.ceil(r.total_time / 60),  # 向上取整，单位为分钟
            })
    return result

@router.get("/records/detail/{date}/{student_id}")
def get_daily_records(
    date: str,
    student_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    records = get_learning_records_by_date_and_student(db, date, student_id)
    # 按时间排序
    records = sorted(records, key=lambda r: r.timestamp)
    result = []
    for idx, r in enumerate(records, start=1):
        resource = db.query(FileResource).filter(FileResource.file_id == r.resource_id).first()
        resource_name = resource.title if resource else "未知资源"
        dt = r.timestamp
        time_str = dt.strftime("%H:%M:%S")
        result.append({
            "id": idx,  # 从1开始递增
            "resource_id": r.resource_id,
            "resource_name": resource_name,
            "time": time_str,
            "duration": math.ceil(r.total_time / 60),  # 转为分钟
        })
    return result

@router.get("/records/{year}")
def get_all_year_records(year: int, db: Session = Depends(get_db)):
    records = get_all_learning_records(db)
    summary = {}
    student_ids = set()
    # 汇总每天每个学生的学习时长
    for r in records:
        ts = r.timestamp
        dt = datetime.fromisoformat(ts) if isinstance(ts, str) else ts
        if dt.year == year:
            day_str = dt.strftime("%Y-%m-%d")
            key = (r.student_id, day_str)
            summary[key] = summary.get(key, 0) + r.total_time
            student_ids.add(r.student_id)
    # 补全所有学生全年日期
    start = date(year, 1, 1)
    end = date(year + 1, 1, 1)
    all_days = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days)]
    student_records = []
    # 每个学生
    for student_id in student_ids:
        records_list = [
            [day_str, math.ceil(summary.get((student_id, day_str), 0) / 60)]  # 转为分钟
            for day_str in all_days
        ]
        student_records.append({
            "student_id": student_id,
            "records": records_list
        })
    # 计算所有学生的平均
    avg_records = [
        [day_str,
         math.ceil(
             sum(
                 summary.get((sid, day_str), 0) for sid in student_ids
             ) / len(student_ids) / 60  # 转为分钟
         )]
        for day_str in all_days
    ]
    student_records.append({
        "student_id": -1,
        "records": avg_records
    })
    return student_records

@router.get("/records/{year}/{student_id}")
def get_student_year_records(year: int, student_id: int, db: Session = Depends(get_db)):
    records = get_learning_records_by_student(db, student_id)
    day_summary = {}
    for r in records:
        dt = datetime.fromisoformat(r.timestamp) if isinstance(r.timestamp, str) else r.timestamp
        if dt.year == year:
            day_str = dt.strftime("%Y-%m-%d")
            day_summary[day_str] = day_summary.get(day_str, 0) + r.total_time
    start = date(year, 1, 1)
    end = date(year + 1, 1, 1)
    return [
        [d.strftime("%Y-%m-%d"), math.ceil(day_summary.get(d.strftime("%Y-%m-%d"), 0) / 60)]
        for d in (start + timedelta(days=i) for i in range((end - start).days))
    ]

@router.delete("/records/{year}")
def delete_all_students_yearly_records(year: int, db: Session = Depends(get_db)):
    delete_learning_records_by_year(db, year)
    return {"success": True}

@router.delete("/records/{year}/{student_id}")
def delete_yearly_records(year: int, student_id: int, db: Session = Depends(get_db)):
    delete_learning_records_by_year_and_student(db, year, student_id)
    return {"success": True}

@router.delete("/records/detail/{date}")
def delete_all_students_daily_records(date: str, db: Session = Depends(get_db)):
    delete_learning_records_by_date(db, date)
    return {"success": True}

@router.delete("/records/detail/{date}/{student_id}")
def delete_daily_records(date: str, student_id: int, db: Session = Depends(get_db)):
    delete_learning_records_by_date_and_student(db, date, student_id)
    return {"success": True}

@router.get("/study_time", response_model=StudyTimeOut)
def get_study_time_by_knowledge(
    knowledge_id: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not knowledge_id:
        raise HTTPException(status_code=400, detail="knowledge_id is required")
    if not check_role(db, current_user.id, "student"):
        raise HTTPException(status_code=403, detail="Not authorized")
    result = get_study_time(db, current_user.id, knowledge_id)
    return result

@router.get("/study_time/all", response_model=list[StudyTimeOut])
def list_study_time_all(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not check_role(db, current_user.id, "student"):
        raise HTTPException(status_code=403, detail="Not authorized")
    result = list_study_time(db, current_user.id)
    return result

@router.get("/study_time/list", response_model=list[StudyTimeListOut])
def get_study_time_list_by_knowledge(
    knowledge_id: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not knowledge_id:
        raise HTTPException(status_code=400, detail="knowledge_id is required")
    if not check_role(db, current_user.id, "teacher") and not check_role(db, current_user.id, "admin"):
        raise HTTPException(status_code=403, detail="Not authorized")
    result = get_study_time_list(db, knowledge_id)
    return result

@router.get("/study_time/list/all", response_model=list[StudyTimeListOut])
def list_study_time_list_all(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not check_role(db, current_user.id, "teacher") and not check_role(db, current_user.id, "admin"):
        raise HTTPException(status_code=403, detail="Not authorized")
    result = list_study_time_list(db)
    return result

@router.get("/study_time/average", response_model=AverageStudyTimeOut)
def get_average_study_time_by_knowledge(
    knowledge_id: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not knowledge_id:
        raise HTTPException(status_code=400, detail="knowledge_id is required")
    result = get_average_study_time(db, knowledge_id)
    return result

@router.get("/study_time/average/all", response_model=list[AverageStudyTimeOut])
def list_average_study_time_all(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    result = list_average_study_time(db)
    return result