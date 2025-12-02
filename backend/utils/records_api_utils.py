import requests
import random
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api"

resource_ids = [
    "test_resource_1", "test_resource_2",
]
students = [1, 2, 3]
start_date = datetime(2025, 6, 1)
days = 30

records = []

for student_id in students:
    for i in range(days):
        day = start_date + timedelta(days=i)
        study_times = random.randint(2, 6)
        total_day_seconds = random.randint(0, 21600)
        if total_day_seconds < 600:
            continue
        remain_seconds = total_day_seconds
        for k in range(study_times):
            if k == study_times - 1:
                session_seconds = remain_seconds
            else:
                max_this = min(remain_seconds - (study_times - k - 1) * 600, 3600)
                min_this = min(600, max_this)
                if max_this < min_this or max_this <= 0:
                    session_seconds = max_this if max_this > 0 else 0
                else:
                    session_seconds = random.randint(min_this, max_this)
                remain_seconds -= session_seconds
            resource_id = random.choice(resource_ids)
            # 只有分页资源才生成 page_times
            if resource_id.startswith("ppt_") or resource_id.startswith("ML_"):
                page_num = random.randint(1, 5)
                page_times = []
                remain = session_seconds
                for j in range(page_num):
                    if j == page_num - 1:
                        page_times.append(remain)
                    else:
                        t = random.randint(0, remain)
                        page_times.append(t)
                        remain -= t
            else:
                page_times = []
            hour = random.randint(8, 22)
            minute = random.randint(0, 59)
            timestamp = day.replace(hour=hour, minute=minute)
            records.append({
                "student_id": student_id,
                "resource_id": resource_id,
                "status": 1,
                "total_time": session_seconds,
                "page_times": page_times,
                "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S")
            })

# 批量提交
resp = requests.post(f"{BASE_URL}/records/batch", json=records)
print("批量提交学习记录：", resp.status_code, resp.json())