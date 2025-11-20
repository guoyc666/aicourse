from fastapi import APIRouter
from crud.progress import calc_progress
from crud.knowledge import list_knowledge_points

router = APIRouter()

@router.get("/progress/average")
def get_all_average_progress():
    knowledge_points = list_knowledge_points()
    average_progress_data = []
    for kp in knowledge_points:
        # This is a placeholder function. Actual implementation would depend on how progress is stored.
        average_progress = 0.75  # Dummy value
        average_progress_data.append({
            "knowledge_id": kp.id,
            "progress": average_progress,
        })
    return {"progress_data": average_progress_data}

@router.get("/progress/average/{knowledge_id}")
def get_average_progress(knowledge_id: str):
    # This is a placeholder function. Actual implementation would depend on how progress is stored.
    # For now, we return a dummy value.
    average_progress = 0.75  # Dummy value
    return {
        "knowledge_id": knowledge_id,
        "progress": average_progress,
    }

@router.get("/progress/{student_id}")
def get_all_progress(student_id: int):
    knowledge_points = list_knowledge_points()
    progress_data = []
    for kp in knowledge_points:
        total, finished = calc_progress(student_id, kp.id)
        progress_data.append({
            "knowledge_id": kp.id,
            "progress": finished / total if total > 0 else 0,
        })
    return {"student_id": student_id, "progress_data": progress_data}

@router.get("/progress/{student_id}/{knowledge_id}")
def get_progress(student_id: int, knowledge_id: str):
    total, finished = calc_progress(student_id, knowledge_id)
    return {
        "student_id": student_id,
        "knowledge_id": knowledge_id,
        "progress": finished / total if total > 0 else 0,
    }