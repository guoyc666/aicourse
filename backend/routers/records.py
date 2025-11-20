import math
from fastapi import APIRouter, Body
from crud.resource import get_resource_by_id
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
)
from schemas_.records import LearningRecordCreate
from datetime import datetime, date, timedelta

router = APIRouter()

@router.post("/records/")
def add_record(rec: LearningRecordCreate):
    obj = create_learning_record(rec)
    return {"success": True, "id": obj.id}

@router.post("/records/batch")
def add_records_batch(records: list[LearningRecordCreate]):
    objs = create_learning_records_batch(records)
    return {"success": True, "ids": [obj.id for obj in objs]}

@router.get("/records/detail/{date}")
def get_all_students_daily_records(date: str):
    records = get_learning_records_by_date(date)
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
            resource_name = get_resource_by_id(r.resource_id).name if get_resource_by_id(r.resource_id) else "未知资源"
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
def get_daily_records(date: str, student_id: int):
    records = get_learning_records_by_date_and_student(date, student_id)
    # 按时间排序
    records = sorted(records, key=lambda r: r.timestamp)
    result = []
    for idx, r in enumerate(records, start=1):
        resource_name = get_resource_by_id(r.resource_id).name if get_resource_by_id(r.resource_id) else "未知资源"
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
def get_all_year_records(year: int):
    records = get_all_learning_records()
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
def get_student_year_records(year: int, student_id: int):
    records = get_learning_records_by_student(student_id)
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
def delete_all_students_yearly_records(year: int):
    delete_learning_records_by_year(year)
    return {"success": True}

@router.delete("/records/{year}/{student_id}")
def delete_yearly_records(year: int, student_id: int):
    delete_learning_records_by_year_and_student(year, student_id)
    return {"success": True}

@router.delete("/records/detail/{date}")
def delete_all_students_daily_records(date: str):
    delete_learning_records_by_date(date)
    return {"success": True}

@router.delete("/records/detail/{date}/{student_id}")
def delete_daily_records(date: str, student_id: int):
    delete_learning_records_by_date_and_student(date, student_id)
    return {"success": True}