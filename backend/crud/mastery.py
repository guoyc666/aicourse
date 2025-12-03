import json
from models import Mastery, QuestionRecord, Question
from neo4j import get_graph
from sqlalchemy.orm import Session
from crud.graph import get_all_knowledge_points, get_all_students

def get_mastery(db: Session, student_id: int, knowledge_id: str):
    mastery = db.query(Mastery).filter(
        Mastery.student_id == student_id,
        Mastery.knowledge_id == knowledge_id
    ).first()
    if not mastery:
        return {
            "knowledge_id": knowledge_id,
            "mastery": 0.0
        }
    return mastery

def list_mastery(db: Session, student_id: int):
    # 获取所有知识点
    all_knowledge_points = get_all_knowledge_points()
    masteries = db.query(Mastery).filter(
        Mastery.student_id == student_id
    ).all()
    mastery_map = {m.knowledge_id: m.mastery for m in masteries}
    mastery_list = [
        {
            "knowledge_id": kp_id,
            "mastery": mastery_map.get(kp_id, 0.0)
        }
        for kp_id in all_knowledge_points
    ]
    return mastery_list

def get_mastery_list(db: Session, knowledge_id: str):
    students = get_all_students(db)
    masteries = db.query(Mastery).filter(
        Mastery.knowledge_id == knowledge_id
    ).all()
    result = []
    for s in students:
        mastery_record = next((m for m in masteries if m.student_id == s.id), None)
        mastery_value = mastery_record.mastery if mastery_record else 0.0
        result.append({
            "knowledge_id": knowledge_id,
            "mastery": mastery_value,
            "student_id": s.id,
            "student_name": s.full_name
        })
    return result

def list_mastery_list(db: Session):
    students = get_all_students(db)
    # 获取所有知识点
    all_knowledge_points = get_all_knowledge_points()
    # 获取所有掌握度
    all_masteries = db.query(Mastery).all()
    # 构建掌握度映射
    mastery_map = {}
    for m in all_masteries:
        mastery_map.setdefault(m.knowledge_id, {})[m.student_id] = m.mastery

    result = []
    for kp_id in all_knowledge_points:
        for s in students:
            mastery_value = mastery_map.get(kp_id, {}).get(s.id, 0.0)
            result.append({
                "knowledge_id": kp_id,
                "mastery": mastery_value,
                "student_id": s.id,
                "student_name": s.full_name
            })
    return result

def get_average_mastery(db: Session, knowledge_id: str):
    masteries = db.query(Mastery).filter(Mastery.knowledge_id == knowledge_id).all()
    if not masteries:
        return {
            "knowledge_id": knowledge_id,
            "average_mastery": 0.0
        }
    total = sum(m.mastery for m in masteries)
    return {
        "knowledge_id": knowledge_id,
        "average_mastery": total / len(masteries)
    }

def list_average_mastery(db: Session):
    all_knowledge_points = get_all_knowledge_points()
    avg_mastery_list = []
    for kp_id in all_knowledge_points:
        avg_mastery = get_average_mastery(db, kp_id)
        avg_mastery_list.append({
            "knowledge_id": kp_id,
            "average_mastery": avg_mastery["average_mastery"]
        })
    return avg_mastery_list


# 掌握度计算依赖于答题结果
# M = (加权正确率) * (平均答题速度)
# 题目有0-1的难度系数，题目类型为choice、fill或code
#    加权正确率 = Σ(已回答题目难度系数 * 是否正确) / Σ(题库中所有题目难度系数)
#    平均答题速度设置：若学生平均答题时间小于等于标准时间，则为1分；
#                    若学生平均答题时间大于标准时间，则分数线性递减，最低为0.6分
def calc_mastery(student_id: str, db: Session):
    # 从QuestionRecord表中获取该学生的答题记录，从Question表中获取题库
    # question_record: [{'id', 'student_id', 'submit_time', 'duration', 'detail', 'total_questions'}]
    # 其中detail字段为JSON格式，包含question_id和is_correct等信息
    # 将question_record转换为更易处理的格式：[{'question_id', 'is_correct', 'submit_time', 'duration'}]，每个题目只保留最新的一次答题记录
    all_records = db.query(QuestionRecord).filter(QuestionRecord.student_id == student_id).all()
    record_map = {}
    for rec in all_records:
        detail = json.loads(rec.detail)
        for q in detail:
            qid = q['question_id']
            is_correct = q['is_correct']
            if qid not in record_map or rec.submit_time > record_map[qid]['submit_time']:
                record_map[qid] = {
                    'question_id': qid,
                    'correct': is_correct,
                    'submit_time': rec.submit_time,
                    'time': rec.duration/q['total_questions']  # 平均每题用时
                }
    
    # 获取知识点列表
    all_knowledge_points = get_all_knowledge_points()

    # 获取题库
    # question: [{'question_id', 'type', 'difficulty', 'knowledge_id'}]
    # 其中knowledge_id为JSON格式的知识点ID列表
    # 对于all_knowledge_points中的每个知识点，在all_questions中找到相关题目列表，从record_map中找到对应的答题记录，计算加权正确率和平均答题速度
    all_questions = db.query(Question).all()
    mastery_results = {}
    for kp_id in all_knowledge_points:
        related_questions = [q for q in all_questions if kp_id in json.loads(q.knowledge_id)]
        if not related_questions:
            mastery_results[kp_id] = 0.0
            continue
        
        total_difficulty = 0.0
        weighted_correctness = 0.0
        total_time = 0
        answered_count = 0

        for q in related_questions:
            total_difficulty += q.difficulty
            if q.question_id in record_map:
                rec = record_map[q.question_id]
                answered_count += 1
                weighted_correctness += q.difficulty * (1.0 if rec['correct'] else 0.0)
                total_time += rec['time']
        
        if answered_count == 0 or total_difficulty == 0:
            mastery_results[kp_id] = 0.0
            continue

        weighted_accuracy = weighted_correctness / total_difficulty

        avg_time = total_time / answered_count
        # 假设标准答题时间为60秒
        standard_time = 60
        if avg_time <= standard_time:
            speed_score = 1.0
        else:
            speed_score = max(0.6, 1.0 - (avg_time - standard_time) / (5 * standard_time))

        mastery_score = weighted_accuracy * speed_score
        mastery_results[kp_id] = mastery_score

        # 写入数据库 
        mastery_obj = db.query(Mastery).filter(
            Mastery.student_id == student_id,
            Mastery.knowledge_id == kp_id
        ).first()
        if mastery_obj:
            mastery_obj.mastery = mastery_score
        else:
            mastery_obj = Mastery(
                student_id=student_id,
                knowledge_id=kp_id,
                mastery=mastery_score
            )
            db.add(mastery_obj)
    db.commit()
    
    return mastery_results